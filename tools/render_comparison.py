from pathlib import Path
import numpy as np,cv2,mujoco,json,subprocess,ast,sys,yaml,xml.etree.ElementTree as ET
from scipy.optimize import least_squares
site=Path(__file__).resolve().parents[1];out=site/'media';repo=Path(sys.argv[1]).resolve();fit=json.loads((out/'matched-motion-scene.json').read_text());x=np.array(fit['camera_and_q']);arm0=np.array(fit['arm_points'],np.float32);pix=np.array(fit['pixel_points'])
engine=repo/Path('physical-ai-studio/application/backend/src/so101_architecture/engine.py')
tree=ast.parse(engine.read_text(encoding='utf-8'));bowls=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.AnnAssign) and getattr(n.target,'id','')=='DEFAULT_WORKSPACE_BOWLS')
standalone=yaml.safe_load((repo/'configs/sim-scene.yaml').read_text())['plates']
assert all(role in standalone and role in bowls for role in ['source','good','defective'])
original_bowls=json.loads(json.dumps(bowls))
for (role,b),wp in zip(bowls.items(),fit['world_points'][:3]):b['pos_world_m']=[wp[0],wp[1],0.]
scene=ET.parse(repo/'artifacts/block_inspector/mjcf/cell_cluster_3.xml').getroot()
wrist=scene.find(".//body[@name='Body3']")
held=ET.SubElement(wrist,'body',name='held_white_part',pos='0.008 0 -0.09',quat='0 0.7071067811865476 0.7071067811865476 0')
ET.SubElement(held,'geom',name='held_white_part_visual',type='mesh',mesh='duplo_2x4_3011',pos='0 0 -0.0118',rgba='0.95 0.95 0.91 1',contype='0',conaffinity='0',group='1')
m=mujoco.MjModel.from_xml_string(ET.tostring(scene,encoding='unicode'));d=mujoco.MjData(m)
for role,b in bowls.items():m.body_pos[m.body('plate_'+role).id]=b['pos_world_m']
adr=[m.jnt_qposadr[m.joint(n).id] for n in fit['joint_names']];bids=[m.body(n).id for n in fit['body_names']]
rot=cv2.Rodrigues(x[:3])[0];cp=-rot.T@x[3:6];cid=m.camera('hero').id;m.cam_pos[cid]=cp;quat=np.empty(4);mujoco.mju_mat2Quat(quat,(rot.T@np.diag([1,-1,-1])).flatten());m.cam_quat[cid]=quat;m.cam_mat0[cid]=(rot.T@np.diag([1,-1,-1])).flatten();m.cam_fovy[cid]=np.degrees(2*np.arctan(464/(2*x[6])))
K=np.array([[x[6],0,416],[0,x[6],232],[0,0,1]],float)
world=np.array(fit['world_points']);projected=cv2.projectPoints(world,x[:3],x[3:6],K,None)[0][:,0,:]
H0=np.eye(3)
for i in range(m.ngeom):
    name=m.geom(i).name
    if name.startswith('vis_') and np.mean(m.geom_rgba[i,:3])>.5:m.geom_rgba[i]=[.37,.16,.65,1]
    if name=='table':m.geom_matid[i]=-1;m.geom_rgba[i]=[.48,.32,.14,1];m.geom_size[i,:2]=[5,5]
    if 'housing' in name:m.geom_rgba[i,3]=0
for role,b in bowls.items():m.geom_rgba[m.geom('plate_'+role+'_vis').id]=b['rgba']
def plane(uv,z):
    uv=cv2.perspectiveTransform(np.array([[uv]],np.float32),np.linalg.inv(H0))[0,0]
    ray=rot.T@np.array([(uv[0]-416)/x[6],(uv[1]-232)/x[6],1.]);return cp+(z-cp[2])/ray[2]*ray
for name,uv,col in [('block_0',[446,431],[.8,.02,.03,1]),('block_1',[435,288],[.95,.85,.04,1]),('block_2',[420,326],[.6,.4,.7,1])]:
    bid=m.body(name).id;j=m.body_jntadr[bid];a=m.jnt_qposadr[j];d.qpos[a:a+3]=plane(uv,.016);d.qpos[a+3:a+7]=[1,0,0,0]
    for g in np.where(m.geom_bodyid==bid)[0]:m.geom_rgba[g]=col
m.vis.global_.offwidth=832;m.vis.global_.offheight=464
source=repo/'demo_media/WhatsApp Video 2026-11-18 at 01.19.03 (5).mp4';cap=cv2.VideoCapture(str(source));cap.set(cv2.CAP_PROP_POS_MSEC,28800)
frames=[]
for i in range(144):
    ok,frame=cap.read()
    if not ok:break
    frames.append(frame)
cap.release();prev=cv2.cvtColor(frames[0],cv2.COLOR_BGR2GRAY);mask=np.ones(prev.shape,np.uint8)*255;mask[70:450,390:820]=0
static0=cv2.goodFeaturesToTrack(prev,180,.02,15,mask=mask);static=static0.copy();track=arm0.reshape(-1,1,2);tracks=[];Hs=[];Hbg=np.eye(3)
for n,frame in enumerate(frames):
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    if n:
        ns,st,_=cv2.calcOpticalFlowPyrLK(prev,gray,static,None,winSize=(31,31),maxLevel=3);keep=st[:,0].astype(bool);static0=static0[keep];static=ns[keep]
        if len(static)>8:
            hh,_=cv2.findHomography(static0[:,0,:],static[:,0,:],cv2.RANSAC,3)
            if hh is not None:Hbg=hh
        nt,ts,_=cv2.calcOpticalFlowPyrLK(prev,gray,track,None,winSize=(31,31),maxLevel=3);track=np.where(ts[:,:,None]>0,nt,track)
    tracks.append(track[:,0,:].copy());Hs.append(Hbg@H0);prev=gray
# Endpoint annotations keep the optical-flow estimate attached to the same visible joints.
last=np.array([[599,309],[565,204],[445,149],[400,162],[375,179]],float);correction=last-tracks[-1]
lo=np.array([m.joint(n).range[0] for n in fit['joint_names']]);hi=np.array([m.joint(n).range[1] for n in fit['joint_names']]);q=x[7:].copy()
rr=mujoco.Renderer(m,464,832);opt=mujoco.MjvOption();opt.geomgroup[3]=0

def encoder(name):return subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','832x464','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(out/name)],stdin=subprocess.PIPE)
sim=encoder('matched-motion-sim.mp4');real=encoder('matched-motion-real.mp4');records=[]
try:
    for n,frame in enumerate(frames):
        targetimg=tracks[n]+correction*n/(len(frames)-1);H=Hs[n];target=cv2.perspectiveTransform(targetimg.astype(np.float32).reshape(-1,1,2),np.linalg.inv(H))[:,0,:];prior=q.copy()
        def resid(qq):
            d.qpos[adr]=qq;mujoco.mj_forward(m,d);w=np.vstack([d.xpos[bids],d.site_xpos[m.site('jaw_fixed_site').id]]);uv=cv2.projectPoints(w,x[:3],x[3:6],K,None)[0][:,0,:]
            return np.r_[(uv-target).ravel(),(qq-prior)*3]
        q=least_squares(resid,q,bounds=(lo,hi),max_nfev=60).x;d.qpos[adr]=q;d.qpos[m.jnt_qposadr[m.joint('Revolute_5').id]]=-.38;mujoco.mj_forward(m,d)
        rr.update_scene(d,camera='hero',scene_option=opt);render=cv2.warpPerspective(rr.render(),H,(832,464),borderMode=cv2.BORDER_REPLICATE)
        sim.stdin.write(render.tobytes());real.stdin.write(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB).tobytes())
        records.append({'frame':n,'joint_positions_rad':q.tolist(),'view_alignment':H.tolist(),'held_part_world_position_m':d.xpos[m.body('held_white_part').id].tolist()})
finally:
    sim.stdin.close();real.stdin.close();sim.wait();real.wait();rr.close()
meta={'synthetic':True,'source':source.name,'source_start_seconds':28.8,'frames':len(records),'fps':30,'workspace_configuration':str(engine.relative_to(repo)),'configured_bowls':bowls,'bowl_positions_changed_from_configuration':True,'original_studio_bowls':original_bowls,'repository_configuration_modified':False,'method':'Kinematic visual reconstruction with a separate video-fitted plate layout, estimated camera and image-tracked arm motion; repository defaults are unchanged. Not telemetry or dynamics validation.','fit':fit,'reference_view_alignment':H0.tolist(),'endpoint_annotations':last.tolist(),'joint_sweep_rad':(np.array([r['joint_positions_rad'] for r in records]).max(0)-np.array([r['joint_positions_rad'] for r in records]).min(0)).tolist(),'records':records}
previous=json.loads((out/'matched-motion-provenance.json').read_text()) if (out/'matched-motion-provenance.json').exists() else {}
meta={**previous,**meta,'held_part':{'mesh':'duplo_2x4_3011','colour':'white','parent_body':'Body3','parent_offset_m':[.008,0,-.09],'parent_quaternion_wxyz':[0,.7071067811865476,.7071067811865476,0],'gripper_position_rad':-.38,'attachment':'Fixed visual attachment for the reconstruction; not a contact-grasp validation'}}
(out/'matched-motion-provenance.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps({k:v for k,v in meta.items() if k not in ['records','fit','configured_bowls','reference_view_alignment','endpoint_annotations']}),flush=True)


