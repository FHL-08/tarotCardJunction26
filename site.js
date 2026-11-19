const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const videos = [...document.querySelectorAll('video')];
const manuallyPaused = new WeakSet();

function syncButton(video) {
  const button = document.querySelector(`[data-video="${video.id}"]`);
  if (!button) return;
  button.textContent = video.paused ? 'Play' : 'Pause';
  button.setAttribute('aria-label', `${video.paused ? 'Play' : 'Pause'} hero video`);
}

for (const video of videos) {
  if (reducedMotion.matches) {
    video.autoplay = false;
    video.pause();
  }
  video.addEventListener('play', () => syncButton(video));
  video.addEventListener('pause', () => syncButton(video));
  syncButton(video);
}

for (const button of document.querySelectorAll('[data-video]')) {
  const video = document.getElementById(button.dataset.video);
  button.addEventListener('click', () => {
    if (video.paused) {
      manuallyPaused.delete(video);
      video.play().catch(() => syncButton(video));
    } else {
      manuallyPaused.add(video);
      video.pause();
    }
  });
}

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    for (const { target: video, isIntersecting } of entries) {
      if (!isIntersecting) {
        video.pause();
      } else if (!reducedMotion.matches && !manuallyPaused.has(video)) {
        video.play().catch(() => syncButton(video));
      }
    }
  }, { threshold: 0.25 });
  videos.forEach(video => observer.observe(video));

  const sectionObserver = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      document.querySelectorAll('.nav-links a').forEach(link => {
        if (link.hash === `#${entry.target.id}`) link.setAttribute('aria-current', 'true');
        else link.removeAttribute('aria-current');
      });
    }
  }, { rootMargin: '-15% 0px -65% 0px', threshold: 0 });
  document.querySelectorAll('main section[id]').forEach(section => sectionObserver.observe(section));
}


// Playback controls for the recorded sweep and its frame-matched visual reconstruction.
const comparisonVideos = [...document.querySelectorAll('#robot-comparison video')];
const comparisonToggle = document.getElementById('comparison-toggle');
function syncComparisonButton() {
  if (!comparisonToggle) return;
  const playing = comparisonVideos.some(video => !video.paused);
  comparisonToggle.textContent = playing ? 'Pause' : 'Play';
  comparisonToggle.setAttribute('aria-label', playing ? 'Pause comparison' : 'Play comparison');
}
comparisonVideos.forEach(video => {
  video.addEventListener('play', syncComparisonButton);
  video.addEventListener('pause', syncComparisonButton);
});
comparisonToggle?.addEventListener('click', () => {
  const shouldPause = comparisonVideos.some(video => !video.paused);
  comparisonVideos.forEach(video => {
    if (shouldPause) {
      manuallyPaused.add(video);
      video.pause();
    } else {
      manuallyPaused.delete(video);
      video.play().catch(syncComparisonButton);
    }
  });
  syncComparisonButton();
});
document.getElementById('comparison-restart')?.addEventListener('click', () => {
  comparisonVideos.forEach(video => {
    video.currentTime = 0;
    manuallyPaused.delete(video);
    video.play().catch(syncComparisonButton);
  });
});
syncComparisonButton();


const geometryReveal = document.getElementById('geometry-reveal');
const geometryWipe = document.querySelector('.video-wipe');
geometryReveal?.addEventListener('input', () => {
  geometryWipe.style.setProperty('--reveal', `${geometryReveal.value}%`);
});


// Keep both rendered views on the same recorded-frame timeline.
const matchedReal = document.getElementById('matched-real-video');
const matchedSim = document.getElementById('matched-sim-video');
let comparisonFrameHandle = null;
function alignComparisonFrame() {
  if (Math.abs(matchedReal.currentTime - matchedSim.currentTime) > 0.05) {
    matchedSim.currentTime = matchedReal.currentTime;
  }
  if (!matchedReal.paused && matchedReal.requestVideoFrameCallback) {
    comparisonFrameHandle = matchedReal.requestVideoFrameCallback(alignComparisonFrame);
  }
}
matchedReal?.addEventListener('play', () => {
  if (comparisonFrameHandle !== null && matchedReal.cancelVideoFrameCallback) {
    matchedReal.cancelVideoFrameCallback(comparisonFrameHandle);
  }
  alignComparisonFrame();
});
matchedReal?.addEventListener('pause', () => {
  if (comparisonFrameHandle !== null && matchedReal.cancelVideoFrameCallback) {
    matchedReal.cancelVideoFrameCallback(comparisonFrameHandle);
    comparisonFrameHandle = null;
  }
});
matchedReal?.addEventListener('seeked', () => {
  matchedSim.currentTime = matchedReal.currentTime;
});
if (geometryWipe && geometryReveal) {
  const revealAtPointer = event => {
    const rect = geometryWipe.getBoundingClientRect();
    const value = Math.max(0, Math.min(100, (event.clientX - rect.left) / rect.width * 100));
    geometryReveal.value = String(value);
    geometryWipe.style.setProperty('--reveal', `${value}%`);
  };
  geometryWipe.addEventListener('pointerdown', event => {
    geometryWipe.setPointerCapture(event.pointerId);
    revealAtPointer(event);
  });
  geometryWipe.addEventListener('pointermove', event => {
    if (geometryWipe.hasPointerCapture(event.pointerId)) revealAtPointer(event);
  });
  geometryWipe.addEventListener('pointerup', event => {
    if (geometryWipe.hasPointerCapture(event.pointerId)) geometryWipe.releasePointerCapture(event.pointerId);
  });
}
