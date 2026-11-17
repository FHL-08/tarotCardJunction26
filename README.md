# Brickcell — Pick · Inspect · Sort

Showcase site for **Brickcell**, the autonomous DUPLO pick–inspect–sort cell built at the
Intel Physical AI Challenge, Junction 2026, by a team from the University of Manchester
and the Royal College of Art.

**Live site:** https://fhl-08.github.io/brickcell/

**Project repo:** https://github.com/ecemguvener/JunctionHack

## What it shows

- The method: perception → catalog ICP localisation → wrist jaw-corridor grasp servoing →
  7-view PatchCore inspection → threshold sort (good/defective/safe-stop).
- The fitted MuJoCo digital twin rebuilt from one depth camera.
- Runtime numbers labeled by where they were actually measured.

## Layout

- `index.html` — the whole site, no build step.
- `media/` — cut demo clips (`pick`, `scan`, `sort`, `method`, `twin`), stills and logos.

Videos are trimmed and sped up (1.3–1.5×) to remove wait times; sources live in
`demo_media/` in the project repo.
