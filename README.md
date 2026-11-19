# Autonomous part inspection: Junction 2026

Showcase for the inspection cell built at the Intel Physical AI Challenge, Junction 2026.

- Site: https://fhl-08.github.io/tarotCardJunction26/
- Implementation: https://github.com/ecemguvener/JunctionHack

## Team

Faisal Lawan, Ecem Guvener and Jack Marshall â€” University of Manchester.
Daniel Jiang â€” Royal College of Art.

## Method

The page describes the task-specific STRIPS-style planner, expected-effect monitoring,
Frax-based inverse kinematics, camera-guided grasping, MuJoCo simulation, actuator-model
identification, and calibrated PatchCore inspection. It distinguishes the SymSkill-inspired
execution hierarchy from SymSkill's learned predicate and skill discovery.

Measurements link to the implementation's validation record. The page separates live CPU
inference timing, depth-perception timing, export parity and held-out image classification.

## Files

- `index.html`: page content and semantic structure.
- `styles.css`: responsive layout and university marks in their original colours.
- `site.js`: visibility-aware video playback, hero pause control and reduced-motion support.
- `media/`: edited clips, poster images, photographs and institution logos.
- `media-edits.json`: original recording names and retained time intervals.

Physical motion reels use hard cuts to omit waiting intervals and retain native motion speed.
The development timelapse is identified separately. Edited footage does not measure cycle time.
Original recordings remain in the implementation repository's `demo_media/` directory.

No build step or package installation is required to serve the site. GitHub Pages serves the
repository root.

## Verification

The November 18 revision was checked in headless Microsoft Edge at widths of 375, 539, 768,
1024 and 1440 pixels. All seven video sources decoded, images and internal links resolved,
no horizontal document overflow or JavaScript errors were found, and hero pause and
reduced-motion behaviour passed. Deployment status must be checked separately after push.

## Junction revision — 18 November 2026

Renamed public branding; visually compared reference and local desktop layouts,
then revised hero composition, typography, palette and spacing. Added explicit
data provenance and demonstration frames labelled separately from training data.
Archived training images are unavailable locally. Five viewport checks passed
(375–1440 pixels), with seven decoded videos, resolved images/anchors, no page
errors, working pause and reduced-motion support. Publication not performed.

## Section and simulation revision

Rebuilt perception around one main grasp video and three plain-language steps;
removed redundant image captions and the repeated integration section. Team
photography uses its natural aspect ratio, without cropping. Existing physical
footage is reused for context in the simulation section.

Rendered a new 12.334-second simulation using MuJoCo 4.0.1 and the project’s
SO101InspectionTwin/CogManInspectionAgent: 370 control steps, simulated pick,
presentation, rotation and placement. No trained anomaly detector was used.
The simulated outcome is not physical inspection evidence. Provenance is in
media/simulation-cycle.json and media-edits.json.

Checks: five widths, eight video elements decoded, images and internal links
resolved, full photograph aspect ratio verified, pause/reduced motion passed,
no page errors. Shared-browser snapshots timed out; local Edge screenshots
were inspected instead. No publication performed.

## Model and real/simulation figures

Added a 48-frame contact sheet sampled from the inspection demo, explicitly
separate from archived fitting data. Real and simulated motion are paired with
shared pause/play/restart controls and labelled as independent runs, not a
frame-aligned replay. Added overall system and PatchCore fitting/scoring
diagrams, model settings, test metrics, recall bars and the confusion matrix.
Accuracy (65%), defect recall (25%) and clean specificity (75%) are derived
from the existing 20-image test record; no model was retrained or reevaluated.
Machine-readable provenance and counts: model-results.json.

Verified five viewport widths (375–1440), eight decoded videos, decoded images,
internal anchors, paired playback controls and reduced motion with no page
errors. Inspected desktop sections and mobile model figures in local Edge
screenshots following a shared-preview snapshot timeout. Not published.

## Moving comparison and editorial revision

Removed the event/team section and the requested montage caption. Trimmed the
reconstruction excerpt to 105–114.5 seconds of its original source, excluding
the thank-you title card. Runtime now has one main observation and a scope table.

Replaced the still-image slider and independent motion recordings with a
72-frame moving reveal comparison. The physical approach (10.6–13.0 seconds
of the supplied grasp recording) is paired with a local MuJoCo reconstruction.
The camera, plate positions, arm appearance and joint poses were fitted to
visible image landmarks, with optical flow accounting for camera/image motion.
This is a kinematic visual reconstruction, not recorded joint telemetry, an
autonomous simulated rollout or dynamics validation. Metadata retains source
and model hashes, camera fit, joint poses and per-frame image transforms.
The slider supports direct dragging and keyboard control; paired videos share
the same frame timeline and playback controls.

Accuracy was audited against the frozen test record: (12+1)/20 = 65%. Validation
accuracy is (9+12)/26 = 80.8%. Neither supports an 85% accuracy claim. No model
was retrained, threshold changed or test set reevaluated.

Moving comparison QA: five widths (375–1440), seven decoded videos, decoded
images and valid anchors, direct/keyboard wipe controls, pause/play/restart
and reduced motion all passed without page errors. Local paired playback
drift was 0.0078 s in the test interval. Visually inspected comparison/runtime
sections and confirmed the shortened reconstruction ends before the title card.
Core Python tests and Ruff were not run; only the separate static showcase
changed. Publication not performed.

## Closing links, Intel credit and moving sweep

Added closing Open source cards for JunctionHack and the verified Physical AI
Studio contribution PR #1425. Intel credit uses the unmodified colour logo from
Intel’s official press asset archive; source and copyright are retained locally.

The comparison now uses a 4.8-second / 144-frame continuous arm sweep. Reviewed
both configs/sim-scene.yaml and Studio DEFAULT_WORKSPACE_BOWLS: these are
different scene defaults and neither is treated as the saved physical layout.
A shared display scene is fitted to the recording’s camera, plate centres/rims
and arm landmarks, with per-frame camera/image tracking and joint estimates.
Both repository configurations remain unchanged. This is visual reconstruction,
not a measured calibration, telemetry replay or dynamics validation.

The fitted scene and per-frame results are in media/matched-motion-scene.json
and media/matched-motion-provenance.json. An existing architecture environment
can reproduce the render with tools/render_comparison.py <repository-root>;
it requires the original recording and generated MuJoCo model in that repo.

White-part correction: removed the requested comparison caption and rerendered
the sweep with a white part attached between the simulated jaws. Attachment
parameters and per-frame held-part positions are in the media provenance.
First/late frames visually checked; revised 4.8-second playback, paired pause
and caption removal passed browser checks at 375/1440 without overflow/errors.

## Narrative and learning revision - 19 November 2026

Rewrote the page copy around results and how the system learned: new hero
headline, a four-number results strip, a SymSkill lineage section with a
side-by-side table citing the ICRA 2026 talk, three learning cards
(appearance, dynamics, demonstration) and a facts row under the twin
comparison. Section order: Overview, Approach, How it learned, Perception,
Digital twin, Inspection, Runtime, Open source.

Every figure comes from the implementation's validation record; no model was
retrained or re-evaluated. The 9/9 physical run is labelled as using the
dark-mark check, not the learned inspector. Held-out metrics (65% accuracy,
25% defect recall) and the twin's limits remain on the page.

Checks in headless Edge with verify_site.py: widths 375, 539, 768, 1024 and
1440 without overflow, seven videos decoded, images and internal anchors
resolved, hero pause and reduced motion passed, no page errors. Desktop
full-page screenshot inspected. Not published.
