# Annales World

A real-time grand strategy game of the modern world (2026 start), modelled on the Hearts of Iron IV mod Millennium Dawn. It runs as one self-contained HTML page.

**Current build:** Build 23 "Garibaldi" (2026-10-31).
**Live game:** https://claude.ai/artifact/FSn6D2BJ3UP4Yzg9N8AxMi

## Layout

| Path | What it is |
|---|---|
| `src/world.src.html` | All the game code (HTML, CSS and JavaScript, about 10,800 lines). Edit this. |
| `src/gamedata.json` | Map data (provinces, borders). Rarely changes. |
| `src/flags.b64` | Flag sprite, base64. Rarely changes. |
| `tools/build_world.py` | Puts the data back into the source and writes `annales-world.html`. |
| `tools/split_world.py` | The reverse: splits a published `annales-world.html` into `src/`. |

## Build

```bash
python3 tools/build_world.py      # writes annales-world.html (not committed)
```

Open `annales-world.html` in a browser to play. It loads d3 7.9.0 and topojson-client 3.1.0 from jsDelivr; keep them there.

## Rules for changing the code

- **Patch, never rewrite.** Edit `src/world.src.html` in place. Each system has its own section starting with a `/* ===== name ===== */` comment; grep for it.
- **All input goes through commands:** `sendCmd` → `applyCmd` → `order()` → `act`. Never change `G` straight from a click. `act` must stay synchronous and free of side effects outside `G`.
- **New state needs a default in `upgrade()`** (or is created lazily), so old saves keep loading.
- **New monthly system:** write `fooMonth()` in its own section and add one call in `simulateMonth0`.
- **CSS goes in the game's own stylesheet** (the second `<style>` block, the one with `/* Layout: a war-room table`). The host replaces the first `<style>` tag on publish.
- **Never put a `//` comment in the middle of a line** that continues with code.
- No placeholder buttons or decorative numbers; unfinished parts are labelled "In progress".

## Docs

- `GEMINI.md`: how to hand back code changes (find-and-replace edits) and what not to do.
- `docs/step24-brief.md`: step 24 split into four parts, the existing code each part touches, and exact formulas for part 1.
- `docs/annales-plan-3.md`: the round 3 plan (steps 24–31).

The full code map, development plan (steps 1–31), build notes and test kit live in the Claude project "Pus boys inc." (`claude/annales-code-map.md`, `claude/annales-plan.md`, `claude/annales-plan-3.md`, `claude/annales-build-21.md` to `-23.md`, `claude/annales-test-kit*.md`). Next planned work: step 24, resources and the world commodity market.

## Workflow

Code can come from anywhere (Claude, Gemini, by hand). Claude tests each change in a headless browser, commits it here, and publishes the final build to the live game.
