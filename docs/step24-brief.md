# Step 24 brief: resources and the world commodity market

The full spec is the "Step 24" section of `docs/annales-plan-3.md`. This brief splits it into four parts, lists the existing code each part touches, and fixes the numbers so nothing has to be guessed. Do **one part per session**, in order. Line numbers are for Build 23 and drift as edits land; search for the quoted text instead.

## Existing resource code (Build 23)

| What | Where (search for) | Notes |
|---|---|---|
| Old deposit resources | `const RESDEF = {` (about line 2476) | oil, gas, rare, grain. `RESDEF[r].v` is the income value. |
| Deposits by country | `const PRODUCERS = {` | a3 → number of provinces that get the deposit. |
| Deposits by province | `const RES = PROV.map(() => []);` then `RESP`, `RESIDX`, `RES_SUPPLY0` | `RES[i]` is the list of resource keys in province `i`. |
| Is a province producing | `function producing(i)` | false in battle, siege, occupied, or blockaded coastal. |
| Old price update | `function resourcesMonth()` | sets `G.price[r]` (index around 1). Called in `simulateMonth0` after `populationMonth()`. |
| Resource income | `const resIncome = id =>` | used by `econ`. |
| Access check | `function hasRes(id, r)` and `const access = (id, r)` | 'own', 'trade', 'market' or null. |
| Shortage effects | in `function econ(n)`: `const grain = access(n.id, 'grain')` and `!access(n.id, 'gas')` | grain → stability, gas → growth. |
| Production-line inputs | `const RESK = [` and `const RINP = {` and `function resAv(n, r)` (about line 7645) | steel, oil, rare, chips, comp. |
| Buildings | `const BLD = {` (about line 1233): `refinery`, `steel`, `elec`, `chem`, `mine` | `bldN(id, t)` = staffed count of a building type in a country. `bldResMul(i, r)` = deposit multiplier from refineries and mines. |
| Market prices | `function marketMonth()` (about line 5177) | old oil/gas price shocks. |
| Economy tab | `function resourcesHTML()` (about line 10222) | |
| Save upgrade | `function upgrade()` (about line 2146) | add defaults here. |

Useful helpers: `gdpOf(id)` ($B a month), `n.pop` (millions), `n.tech` (fielded quality, about 0.6–1.3), `tl(n, line)` (research level of a tech line, e.g. `tl(n, 'nuc')`, `tl(n, 'chip')`), `G.nations` (filter `n.alive`), `ownedP(id)`, `clamp(x, a, b)`, `G.units` (`u.t` is 'a' army, 'f' fleet, 'w' air wing; `u.n` owner; `u.str` size).

## Part 1: the 8 resources, stocks, production and demand (no effects yet)

Goal: every living nation gets a stock of each of the 8 resources, with monthly production and demand computed and stored. **Nothing reads them yet**, so the game plays exactly as before. Effects, the market and the UI come in parts 2–4.

**New section** `/* ================= step 24: resources and markets ================= */`, placed right after the existing `function resourcesMonth() { … }` block.

**Resources** (`const RS8`): keys and labels, in this order:
`oil` Oil, `gas` Natural gas, `uran` Uranium, `steel` Steel, `alu` Aluminium, `rare` Rare earths, `chips` Semiconductors, `grain` Food. (Keep the existing keys `oil`, `gas`, `rare`, `grain` so old code still matches.)

**New deposits**: add `const DEP2 = { uran: {...}, iron: {...}, baux: {...} }` in the same a3 → count form as `PRODUCERS`, and a per-province list `DEP2P[r]` built the same way `RES` is (same hashing, so it's deterministic). Do **not** add them to `RES` or `RESDEF` (old code loops over those).
- uran: KAZ 3, CAN 2, AUS 2, NAM 1, NER 1, UZB 1, RUS 1
- iron (with coal; steel input, not traded): CHN 3, AUS 3, BRA 2, IND 2, RUS 2, UKR 1, USA 1, CAN 1, ZAF 1, SWE 1
- baux: AUS 3, GIN 3, CHN 2, BRA 1, IND 1, IDN 1, JAM 1

**Production per month** (`rsProd(n)` → object of the 8 keys), counting only provinces where `producing(i)` is true and `G.ctrl[i] === n.id`:
- oil, gas, rare: 1 per deposit province in `RES` × `bldResMul(i, r)`
- grain: 3 per grain deposit province (farms replace this in part 4)
- uran: 1 per `DEP2P.uran` province
- steel: `bldN(n.id, 'steel')` × (2 if the nation holds an iron province, else 1)
- alu: `bldN(n.id, 'chem')` × (1.5 if it holds a bauxite province, else 0.5)
- chips: `bldN(n.id, 'elec')` × (0.5 + 0.1 × `tl(n, 'chip')`)

**Demand per month** (`rsDem(n)`): a weight per resource times a world scale `G.rsK[r]`:
- oil: 0.6 × GDP + 0.002 × (troops in its armies + 5 × planes + 50 × ships)
- gas: 0.5 × GDP
- uran: GDP × `tl(n, 'nuc')` × 0.25 (0 without nuclear research)
- steel: 0.5 × GDP
- alu: 0.3 × GDP
- rare: 0.3 × GDP × `n.tech`
- chips: 0.4 × GDP × `n.tech`
- grain: `n.pop`

Here GDP is `gdpOf(n.id)`; compute each nation's GDP once per month, not inside a nation × nation loop.

**World scale** `G.rsK`: set once (`rsInit()`) so that, at that moment, world demand equals world production for each resource: `G.rsK[r] = world production ÷ world weight` (use 1 if the weight is 0). Called by `newGame` (at the end) and by `upgrade()` when `G.rsK` is missing.

**Stocks** `n.rs = {key: amount}`: set in `rsInit()` to 3 months of that nation's demand.

**Monthly** `rsMonth()`, called once in `simulateMonth0` right after `resourcesMonth();`: for every living nation, `n.rs[r] = max(0, n.rs[r] + prod − dem)`, and store `n.rsP` (production), `n.rsD` (demand) and `n.rsS` (shortfall: the part of demand the stock couldn't cover). Nations without `n.rs` (new states, armed-group nations in `G.gn`, which are not in `G.nations`) get it lazily at 3 months of their demand.

**Done when** (Claude tests): the page loads with no errors; after a new game every living nation has all 8 stocks; after 12 months stocks are finite and non-negative; world production ≈ world demand in month 1; Ukraine, the US and Brazil are among the top grain producers, Kazakhstan the top uranium producer; an old save loads and gets `G.rsK` and stocks; the 10-year benchmark is unchanged (nothing reads the stocks yet).

**Status: done (2026-11-01).** Written by Gemini 3.8, applied and tested by Claude. Results on seed 12345: every living nation and armed-group nation has all 8 stocks; no invalid values after 12 months; month-1 world production ≈ demand (oil 35/36.6, grain 90/90.1); top uranium KAZ 3, AUS/CAN 2; a 24-month run on seed 777 is identical to Build 23 (nothing reads the stocks yet); a Build 23 save loads and gets stocks.

**Known gap, fix in part 2:** no country starts with steel mills, electronics or chemical plants (`G.bld` is empty at a new game), so steel, aluminium and chips produce 0 everywhere and `G.rsK` is 0 for them, which would leave their demand at 0 forever. Part 2 must seed starting capacity for these three (before part 4's real buildings) and compute `G.rsK` from it. Also expected for now: without trade (part 3), producers pile up stock while most importers run dry within a year (after 12 months about 185 of 203 countries are short of oil, gas, rare earths and food).

## Part 2: starting industry, the world market and prices

Goal: steel, aluminium and chips get real starting output, and every resource gets a world price that moves with supply and demand. Still nothing pays or runs short (that is part 3), but the old price index `G.price` now comes from the new market.

**2a. Starting industry (fixes the part 1 gap).** Add `const RSBASE` in the step 24 section: real-world shares of output in percent, by a3.
- steel: CHN 54, IND 7, JPN 5, USA 4.5, RUS 4, KOR 3.5, DEU 2, TUR 2, BRA 2, IRN 1.5
- alu: CHN 58, IND 6, RUS 5, CAN 4, ARE 4, BHR 2, AUS 2, NOR 2, USA 1, SAU 1
- chips: TWN 45, KOR 20, USA 10, CHN 12, JPN 8

The rest of each resource (steel 14.5%, alu 15%, chips 5%) is shared among all other living nations by GDP. World totals in units a month: steel 40, alu 15, chips 10. In `rsInit()`, before computing `G.rsK`, set `n.rsBase = {steel, alu, chips}` = share% × world total ÷ 100 for every living nation. `rsProd(n)` adds `n.rsBase[r]` (0 if missing) to steel, alu and chips. `upgrade()`: if any living nation lacks `n.rsBase`, call `rsInit()` again (it resets stocks to 3 months, which is fine for saves from part 1).

**2b. The market.** `G.mkt[r]` for each of the 8 keys = `{ p, base, sup, dem, pm, hi, lo, hist }`:
- `base` (dollars, in $B per unit): oil 7, gas 4, uran 0.5, steel 6, alu 2, rare 0.5, chips 5, grain 3.
- `p` the price, starting at `base`. `sup`, `dem`: last month's world production and demand (sums of `rsP`, `rsD` over living nations).
- `pm` producers' response, starting at 1; `hi`, `lo`: months in a row the price has been above 1.3× or below 0.7× its fair level.
- `hist`: the last 24 prices (push each month, drop the oldest).

`G.wgdp0` = world GDP (sum of `gdpOf` over living nations) when the market is created. Each month the index is `idx = sqrt(world GDP ÷ G.wgdp0)` and the fair price is `fair = base × idx`.

**Monthly** `rsMarket()`, called at the end of `rsMonth()`:
1. `sup`, `dem` as above.
2. `target = fair × (dem ÷ max(sup, 0.01))^e`, with elasticity `e`: oil 1.5, gas 1.2, uran 0.8, steel 0.6, alu 0.6, rare 1.0, chips 1.0, grain 1.6.
3. Stability (owner's rule, no spirals): `target` is clamped to 0.4×–3× `fair`; the new price is `p + 0.5 × (target − p)`, then moved 3% of the way back toward `fair`, then limited to at most 8% above or below last month's `p`, then clamped again to 0.4×–3× `fair`.
4. Producers' response: if `p > 1.3 × fair`, `hi++` else `hi = 0`; if `p < 0.7 × fair`, `lo++` else `lo = 0`. When `hi ≥ 6`, `pm = min(1.5, pm + 0.02)`; when `lo ≥ 6`, `pm = max(0.7, pm − 0.02)`; otherwise `pm` moves 0.01 toward 1. `rsProd(n)` multiplies every resource by `G.mkt[r].pm` (1 if the market doesn't exist yet).
5. Old prices: for `oil`, `gas`, `rare`, `grain`, set `G.price[r] = p ÷ fair`, so code that reads `G.price` (income, crises, markets) sees the new market. Keep `resourcesMonth()` as it is; `rsMonth()` runs after it, so the new value wins.

Create `G.mkt` and `G.wgdp0` in `rsInit()` and, for saves without them, lazily at the top of `rsMarket()`.

**Done when:** every country's month-1 steel, alu and chips are above 0 and China, Taiwan and Korea lead them; prices start at `base`; over 30 years (360 months, no human player) no price leaves 0.4×–3× fair and none sits at a band edge for more than 24 months in a row; a price spike from a sudden supply cut (take away half the oil deposits for a year) rises and then falls back after they return; the game still runs at roughly the same speed.

## Part 3: buying, selling and shortages

Goal: countries buy what they're short of and sell what they have spare, through the trade web, with real money. Blockades, embargoes, war and empty treasuries turn purchases into real shortages, and shortages replace the old flat gas, grain and import rules.

**Per-nation settings** (lazy defaults): `n.rsLim[r]` import limit as a share of demand, default 1 (0 = never buy, 2 = up to twice demand); `n.rsExp[r]` export policy `'free'` (default), `'restr'` (only to countries with `rel(n.id, buyer) > 0` and no sanctions either way) or `'ban'`.

**Monthly** `rsTrade()`, called in `rsMonth()` after the stocks are updated and before `rsMarket()`:
1. **Offers.** Target stock `T = 3 × demand`. A nation offers `0.5 × (stock − T)` when that's above 0 and its policy isn't `'ban'`.
2. **Wants.** A nation wants its shortfall `rsS` plus `(T − stock) ÷ 6` when below target, but the refill part only if `n.gold > revenue(n)`. Cap the total at `n.rsLim[r] × demand`.
3. **Who can buy from whom.** A buyer can buy from a seller unless they are at war (`hostile(a, b)`), either has a full embargo on the other (`sancLv(from, to) >= 3`), or the seller's policy forbids it. Seaborne deliveries arrive × `(1 − (G.blk[buyer] || 0))`; a seller that is a land neighbour (`nbNations(buyer)` contains it) is not cut by the blockade. Compute `nbNations` once per buyer per month.
4. **Clearing.** Per resource, handle buyers in order of largest want first; each takes from its allowed sellers in proportion to their remaining offers, at price `G.mkt[r].p`. A buyer only buys what it can pay for: its gold never goes below 0 because of purchases.
5. **Money.** The buyer pays `qty × p` straight from `n.gold` (record `n.rsCost[r]`, and the month's total in `n.rsCostT`). The seller's earnings are recorded in `n.rsSold` (total $ this month); they reach the treasury through `econ` (below), so they are taxed like other resource income.
6. **Grey market.** A buyer that got nothing for a resource it is short of, while the world has offers left, may buy up to half its shortfall from any non-hostile seller at 1.4× the price, and loses 0.1 reputation that month (`repOf(n.id)` then `n.rep -= 0.1`).
7. Stocks move: the buyer's stock rises by what arrived, the seller's falls by what it sold. Recompute the shortfall after trade and store coverage `n.rsCov[r] = 1 − rsS ÷ demand` (1 when demand is 0).

**Replace the old rules** (coverage `c = n.rsCov ? n.rsCov[r] : 1`):
- **Income** in `econ`: replace `resIncome(n.id) * taxesOf(n).res / 20` with `(n.rsSold || 0) * taxesOf(n).res / 20`. Leave the `resIncome` function itself (other code shows it).
- **Food** in `econ`: replace the line starting `const grain = access(n.id, 'grain');` with a stability loss of `0.3 × (1 − c_grain) × max(0.2, 1 − 0.2 × tl(n, 'agri'))` when `n.pop > 30` (at half coverage this equals today's 0.15).
- **Gas** in `econ`: in the `gmul` line, replace the condition `!access(n.id, 'gas') && n.pcap > 15 ? X : 1` with `n.pcap > 15 ? 1 − (1 − X) × (1 − c_gas) : 1`, keeping `X` (the nuclear, renewables and green-programme factor) exactly as it is.
- **Production lines** `resAv(n, r)`: return the coverage of the matching resource, clamped to 0.3–1, with the old keys mapped: `steel → steel`, `oil → oil`, `rare → rare`, `chips → chips`, `comp → alu`. For `chips`, still multiply by `(1 − 2 × ((n.sfx && n.sfx.rp) || 0))` (technology sanctions). Keep the `RAVC` cache.
- **Labels:** in `RESK`, rename `['comp', 'Composites']` to `['comp', 'Aluminium']` (keep the key, so saved lines still work).

**Balance knob:** `const RSPAY = 1` multiplies every price paid and earned. If the 10-year balance targets break (world GDP ×1.7–2.0, median treasury 3–5 months of revenue), Claude tunes this one number.

**Done when:** an importer short of oil buys it and its gold falls by quantity × price; the seller's income rises the next month; a fully blockaded island gets nothing by sea and its coverage drops; an embargo by every oil producer sends the buyer to the grey market at 1.4× with a reputation loss; a country with 50% food coverage loses the same stability as today's "no grain"; production lines read coverage; after 12 months the number of countries short of oil and food is far below part 1's 185; the balance targets hold.

## Part 4: buildings, the Resources screen, AI building and old saves

**Buildings** (in `const BLD` and `const BJOB`):
- New `farm`: label Farm, cost 0.4, time 3, description "+1 food a month (needs gas for fertiliser)", jobs `[6, .01]`. Each staffed farm adds `1 × n.harv × (0.5 + 0.5 × c_gas)` grain to `rsProd`. `n.harv` is the yearly harvest roll: in January (`MOY() === 0`) set it to `0.85 + 0.3 × R()` for every living nation; default 1.
- `elec` becomes the **semiconductor fab**: label "Semiconductor fab", description "Makes semiconductors (needs microchip research and rare earths)". It can only be built where the owner has `tl(N_(G.owner[i]), 'chip') >= 1`. Its output in `rsProd` is multiplied by `c_rare` (no rare earths, no chips).
- `chem` becomes the **aluminium smelter**: label "Aluminium smelter", description "Makes aluminium (more with bauxite)". Its old missile-and-drone bonus stays.
- `steel` keeps its label; its description adds "Makes steel (more with iron ore)".

**AI building** in `aiBuild`, add to `want` (same `[priority, province, type]` form; use the most developed owned province with a free slot):
- `farm` priority 6 when `c_grain < 0.9`
- `steel` priority 5 when `c_steel < 0.8`, or when the steel price has been above 1.5× fair for 6 months (`G.mkt.steel.hi >= 6`)
- `elec` (fab) priority 5 under the same rule for chips, only with `tl(n, 'chip') >= 1`
- `chem` (smelter) priority 4 under the same rule for alu

AI countries keep the default import limit (1) and export policy (`'free'`).

**The Resources screen:** new `rsHTML()` in the Economy tab, placed right after `${resourcesHTML()}` in `renderEco`. One `sect` titled "Resources and markets". For each of the 8 resources, one row: name, stock, production, demand, net, coverage %, price (with a small 24-point line chart drawn as an inline SVG polyline from `G.mkt[r].hist`), what we bought and sold last month, our import limit as a `<select>` (0%, 50%, 100%, 200%) and export policy as a `<select>` (Free, Restricted, Banned), and a "Build" link to the Construction tab for the matching building (farm, steel mill, fab, smelter). Below the table, the top 3 producers and top 3 buyers of each resource. Use the existing `qrow`/`kv` styles; no new CSS unless needed (then in the game's second `<style>` block).

**Player actions:** the selects send commands, never change `G` directly. Add `case 'rslim'` (o.k resource, o.v share) and `case 'rsexp'` (o.k, o.v policy) to the **first** `switch` in `act`; each sets the field and calls `done(...)` with `o.free`. Wire the selects through the existing `change` listener on `document.body` (add `data-rslim` and `data-rsexp` attributes and send `{ kind: 'act', a: 'rslim', arg: null, o: { k, v } }`).

**Old saves** (`upgrade()`): fill `G.mkt`, `n.rsBase`, `n.rsLim`, `n.rsExp`, `n.harv` where missing. Existing `elec` and `chem` buildings simply become fabs and smelters (same type keys).

**Done when:** a farm adds about 1 food a month; a fab needs microchip research to build and makes nothing without rare earths; the Economy tab shows the table, charts and selects; changing the import limit to 0% stops our purchases the next month; the AI builds farms when hungry; a Build 23 save loads and plays 12 months.

**Status of parts 2–4 (2026-11-01):** written by Gemini 3.8, applied by Claude with these changes: the commodity market is `G.rmk` (`G.mkt` is the game's stock market); `upgrade()` re-runs `rsInit()` only when `G.rsK` or `G.rmk` is missing (new breakaway states lack `rsBase` and must not reset everyone's stocks); blockaded buyers pay only for what arrives; the Resources table puts its controls on a second line; demand and production both scale with `G.rsIdx` (the square root of world GDP growth, set each month in `rsMonth`), so prices stay near fair unless supply is disrupted. `RSPAY` is still being tuned (1 or 0.6).

## Part 5: AI equipment purchases (log fix)

Goal: AI countries at war or under threat that are short of equipment buy it on step 16's equipment market from friendly suppliers, judged like player sales.

This part touches code the brief hasn't mapped yet, so **first reply with a short plan, not edits**: read `function aiLendLease()`, `function eqWants(`, `const eqPrice`, and the `eqtrade` case in `act`, then propose how an AI buyer picks a family it is short of, picks a supplier (friendly, has stock, would sell by the same rules as a player sale), pays `eqPrice`, and records the deal in `G.armsT` like `aiLendLease` does. Limits to respect: at most one purchase per AI country per 3 months, never more than 25% of its gold, only while at war (`warsOf(n.id).length`) or with a war memory or threat posture. Claude reviews the plan, then you write the edits.

**Done when:** in a 10-year run, AI countries at war make equipment purchases from friends, pay for them, and the stock appears in their stockpile under the supplier's model; no purchases in peace without a threat; the balance targets hold.
