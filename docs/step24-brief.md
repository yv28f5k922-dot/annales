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

## Part 2: the world market and prices

`G.mkt[r]` = {price, sup, dem, hist (last 24 prices)}. Price in real dollars indexed to world GDP (`price = base × index × (dem ÷ sup)^e`), elasticity per resource (grain and oil steep, steel and aluminium gentle), stability rules from the spec (band 0.4×–3× base, at most 8% a month, 3% drift back to fair). Old `G.price` keeps working as a 1.0-centred index derived from the new prices. Details to be written before this part starts.

## Part 3: buying, selling and shortages

Shortfalls bought with treasury money through the trade web; blockades, embargoes and no money turn them into real shortages; shortages replace the flat gas, grain and import-share rules (`econ`, `resAv`, `RINP` remapped to the 8). Details to be written before this part starts.

## Part 4: buildings, UI, AI and old saves

Farms and semiconductor fabs (the electronics plant becomes the fab, the chemical plant the smelter), the Economy tab section "Resources and markets", AI import limits, building and equipment purchases, `upgrade()` conversion. Details to be written before this part starts.
