# Instructions for Gemini

You write code changes for `src/world.src.html`. You cannot run the game or push to this repo. Another assistant (Claude) applies your edits, runs the game's tests in a headless browser, commits, and publishes. So:

- **Do not run a dev server, scaffold a project, or "fix" errors you see in your own environment.** The game is one HTML file that runs in a browser with d3 and topojson; it has no build step, no framework and no server. Errors from running parts of it elsewhere (for example "addEventListener on null") are not bugs in the game. Do not add functions the game does not have (for example there is no `clockStop`; the clock uses `setRun(false)`).
- **Patch, never rewrite.** Never return the whole file or a whole function you did not change. The file is 1.4 MB.
- **Read before you write.** Every edit must find text that really exists in `src/world.src.html`. If you can't see the part of the file you need, say so and name what you need; don't guess its contents.
- **Ask when the spec is unclear.** Don't invent rules the spec doesn't give; the step brief (`docs/step24-brief.md`) gives exact formulas.

## Hand-back format

Return a numbered list of edits. Each edit has exactly these four parts:

1. **Where:** the section name (the nearest `/* ===== … ===== */` header above it) and the function, if any.
2. **Find:** the exact existing code, copied character for character, in a code block. Long enough to occur **once** in the file (usually one to three whole lines). Never shorten it with `...`.
3. **Replace with:** the new code, in a code block. It replaces the Find text completely, so repeat any part of the Find text you want to keep.
4. **Why:** one line.

For **new code** (a new section or function), use an insert edit: Find is an existing line to insert after, and Replace with is that same line followed by the new code.

End with:
- **New state:** every new field on `G` or on nations, and the line you added to `upgrade()` for it.
- **Not done / questions:** anything you skipped or are unsure of.

### Example

**Edit 1**
- **Where:** `economy` section, `simulateMonth0`
- **Find:**
```js
  populationMonth(); for (const p in G.battleAt) displace(+p, .03); G.battleAt = {}; resourcesMonth();
```
- **Replace with:**
```js
  populationMonth(); for (const p in G.battleAt) displace(+p, .03); G.battleAt = {}; resourcesMonth(); rsMonth();
```
- **Why:** runs the new step 24 resource stocks once a month, right after the old price update.

## Code rules (from the project)

- All player input goes through `sendCmd` → `applyCmd` → `order()` → `act`; never change `G` straight from a click. `act` stays synchronous with no side effects outside `G`.
- New state needs a default in `upgrade()` or must be created lazily.
- Cache anything computed inside a nation × nation loop; don't call `gdpOf` inside one.
- Never put a `//` comment in the middle of a line that continues with code.
- CSS goes in the game's second `<style>` block (the one with `/* Layout: a war-room table`).
- No placeholder buttons or made-up numbers on screen.
