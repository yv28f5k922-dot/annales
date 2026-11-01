# Annales World: development plan, round 3 (Steps 24–31)

**Continues `claude/annales-plan.md`.** Its build-name rules, session rules, testing rules and core game rules all still apply; read it and the code map first. Builds 21–23 were fixes without plan steps (see `claude/annales-build-21.md` to `-23.md`; the code map still says Build 20, so read those addenda too). Steps here are numbered from 24 so step and build numbers line up again. New code sections are named `/* ===== step NN: … ===== */` as before.

Each session gets one short prompt:
> Read the Project docs claude/annales-code-map.md, claude/annales-plan.md, claude/annales-build-21.md to -23.md and claude/annales-plan-3.md, then do step N.

One step per session, in order. Steps 24 and 26 are large; split them across two sessions if needed.

**Agreed with the owner (2026-10-31):** resource overhaul with a real-currency world market and 8 core resources, energy politics, a nuclear escalation ladder, HOI4-style peace conferences, militias outside the Middle East, refugees, a monthly newspaper, two log fixes (AI buys on the equipment market; counter-insurgency in occupied foreign land). National focus trees are on the back burner. Images come later (Step 31 is a placeholder; don't start it until the owner says so).

## Status
- [x] 24 Resources and the world commodity market — Build 24 "Nehru" (2026-11-01), published. Code by Gemini 3.8, applied, fixed and tested by Claude (see docs/step24-brief.md): rework (resources, `RINP` inputs, `resAv`, resource access), new (8 core resources, world prices, farms, semiconductor fabs, buying with treasury money, AI equipment purchases).
- [ ] 25 Energy politics: new (pipelines, LNG, producer cartels, strategic reserves, energy cut-offs), patch (step 24's market, blockades, summits).
- [ ] 26 Nuclear escalation ladder: rework (nuclear weapons, untouched since early builds), new (uranium and enrichment, inspections, alert levels, deterrence, escalation), patch (summits, sanctions reasons, step 18 strikes).
- [ ] 27 Peace conferences: rework (`autoTerms`, `applyPeace` for player wars), new (war score spending, conference screen, AI bids).
- [ ] 28 Militias 3.0: new (playable groups outside the Middle East), patch (counter-insurgency in occupied foreign land, group nations).
- [ ] 29 Refugees and migration: new (refugee flows, camps, asylum policy), patch (population, stability, UN aid items).
- [ ] 30 The monthly newspaper: new (front page from the month's events).
- [ ] 31 Images and visual identity (later, owner's call).

---

## Step 24: Resources and the world commodity market — Build 24 "Nehru" (2026-11-01) (done)
**Rework:** the current resources (province resources and multipliers, `access`, `resAv`, `RINP`, `lineRes`, the gas and grain shortage effects, the steel mill, electronics and chemical plants) and the "imports at 72–82%" rule. **New:** 8 core resources with stocks, a world market with prices in real currency that move with supply and demand, farms, semiconductor fabs. **Patch:** `bldLedger`, `econ` (spending), trade (`tradeWeb`), blockades (`G.blk`), sanctions (technology and full embargoes), step 16's lines, AI building (`aiBuild`), `stratBudget`.
**At risk:** production lines and their efficiency (step 16), munition lines (step 18), the gas-shortage growth penalty and grain-shortage stability loss, the balance targets (GDP ×1.7–2.0 over 10 years, treasury about 4 months), AI budgets, `REVC` caching, speed, old saves.

**The 8 core resources** (owner approved 2026-10-31):
1. **Oil:** from wells on province deposits. Used by armies, aircraft and ships (fuel), refineries, plastics.
2. **Natural gas:** from wells on deposits. Used by power, heating, fertiliser (farms).
3. **Uranium:** from mines on real deposits (Kazakhstan, Canada, Australia, Namibia, Niger, Uzbekistan, Russia). Fuels nuclear power plants from the start; Step 26 adds enrichment and weapons on top. Licensed: selling to a country outside the non-proliferation treaty is a sanctions reason from this step on.
4. **Steel:** made in steel mills from iron and coal deposits (both part of a mine deposit, not traded resources; coal is not a market resource). Used by tanks, ships, artillery, construction and railways.
5. **Aluminium:** made in smelters from bauxite deposits and power. Used by aircraft, missiles, vehicles. Step 16's composites fold into it.
6. **Rare earths and critical minerals:** from mines on deposits (China dominant). Used by electronics, missiles, magnets, fabs.
7. **Semiconductors:** made only in **semiconductor fab** buildings (the electronics plant becomes the fab). Fabs need the microchip tech line, rare earths, power and a large build cost; each fab's output and chip quality scale with the microchip level researched. Taiwan, South Korea, Japan, the US and China start with real fabs. Used by every modern weapon, research labs, the digital economy.
8. **Food (grain):** made only by **farm** buildings, each producing a small amount (so a breadbasket needs many farms). Farms need gas (fertiliser) and arable land; output varies with terrain and a yearly harvest roll. Starting farms are seeded from real output so Ukraine, the US, Brazil, Russia, Argentina, Canada, Australia and India are the big producers. Population eats food every month.

**Coal** (owner, 2026-10-31: uranium replaces it in the 8) stays only as a local deposit feeding steel mills and coal power plants in the country that mines it; it is not traded on the market. Coal power is cheap and dirty (climate fund, green programmes).

**Power** in this step: each country's power plants burn gas, oil, local coal or uranium (nuclear plants) and renewables use none; shortages of a fuel cut that plant's output. Step 25 deepens energy politics.

**Production and stocks.**
- Every nation has a stock per resource (`n.rs[k]`), production per month from its buildings, and demand per month from its economy (population, industry, power), production lines (step 16's per-family input weights, remapped to the 8 resources), fuel for armies, wings and fleets, and construction.
- Each month: production goes into the stock, demand comes out. A shortfall is bought on the world market with treasury money (automatically, up to the player's import limit per resource); what can't be bought or shipped (blockade, embargo, no money) is a real shortage. A surplus can be sold automatically above a stock target.
- Shortages cut what uses the resource, in proportion (lines, power, growth, food → stability and population growth), replacing the flat percentages of step 16.
- Extraction buildings sit on province deposits (oil and gas wells, coal mines, bauxite and rare-earth mines). Seed deposits from real reserves. Steel mills, smelters, refineries, fabs and farms are built anywhere with the inputs.

**The world market.**
- One market per resource (`G.mkt[k]`: price, last month's world supply and demand, history for a chart). Prices are in real currency, indexed to world GDP so 2040 prices stay readable: `price = base × index × (demand ÷ supply)^e`, with elasticity `e` per resource (food and oil steep, steel and aluminium gentle).
- **Stability rules (owner: no late-game spiral):** price stays within 0.4×–3× base; it moves at most 8% a month; it drifts 3% a month back toward its fair level; high prices raise extraction and building output after a lag (operators run harder, and the AI builds wells, mines, farms and fabs when a resource has been above 1.5× for six months), low prices idle the least profitable producers. Run a 30-year check that no price sits at a band edge for more than two years in a row.
- **Trade:** buying and selling go through the trade web: a seller's exports and a buyer's imports, so tariffs, sanctions, embargoes, blockades and step 18's convoys matter. A nation can only buy from countries that trade with it; a full embargo by the big producers of a resource leaves the grey market (+40% price, reputation, as munitions do now).
- Sales earn real revenue for the seller (exports, the resource royalty tax from step 3); purchases are real spending.

**Player controls (Economy tab, new section "Resources and markets").** Per resource: stock, production, demand, net, price with a 24-month chart, top producers and buyers, our import limit and export policy (free, restricted, banned), stock target. Build buttons for the matching buildings link to Construction.

**AI.** AI countries set import limits and export policies by posture, build extraction and processing when prices are high or they are short, and keep stock targets. **AI equipment purchases (log fix):** AI countries short of kit at war or under threat buy on step 16's equipment market (`eqtrade`) from friendly suppliers, judged like player sales.

**Old saves.** `upgrade()` seeds deposits, farms, fabs, stocks (three months of demand) and market prices from the map; step 16 lines remap their inputs; the old steel, electronics and chemical plants become steel mill, fab and smelter.

**Done when:** a farm adds a small amount of food; a fab produces semiconductors only with the microchip tech and rare earths; a shortage bought on the market costs real treasury money; a blockade or embargo turns the purchase into a shortage that cuts output; a demand spike raises the price and new supply brings it back; a 30-year run keeps every price inside the band without sitting at an edge for two years; the AI buys equipment on the market; the balance targets still hold.

## Step 25: Energy politics
**New:** pipelines, LNG terminals and tankers, producer cartels, strategic reserves, energy cut-offs. **Patch:** step 24's oil, gas and uranium markets, the trade web, blockades and convoys (step 18), summits (step 19), sanctions reasons (step 13).
**At risk:** step 24's prices and balance, convoys, the gas-shortage effects, summit agendas.
- **Pipelines:** gas (and some oil) moves between neighbours by pipeline: a province link like railways (`G.pipe`), seeded from real pipelines, built as an order. Gas without a pipeline needs LNG export and import terminals and travels by convoy, so it is dearer and blockades hit it.
- **Cartels:** an OPEC+ style producers' bloc using the existing blocs: members agree a production quota at its summit (a step 19 recommendation); cutting raises the price and members' revenue, cheating earns more and costs trust when found out.
- **Strategic reserves:** a reserve per resource beyond the normal stock; filled when cheap, released by order in a crisis (raises supply, lowers the price for everyone).
- **Energy cut-off:** a seller can cut a buyer off (act `ecut`): the buyer must find other sellers at market price or suffer the shortage; the seller loses the revenue and relations. Cutting off a bloc member is an emergency-summit trigger and a sanctions reason. The AI uses it as a lever against rivals who depend on it.
- **Power:** step 24's plants (gas, oil, local coal, nuclear on uranium, renewables) now set an electricity price per country that feeds industry costs and growth; building nuclear or renewables cuts exposure to gas cut-offs.

**Done when:** a pipeline carries gas cheaper than LNG; a blockade cuts LNG but not pipeline gas; a cartel quota cut raises the price; releasing a reserve lowers it; a cut-off forces the buyer onto the market or into shortage and opens an emergency bloc summit.

## Step 26: Nuclear escalation ladder
**Rework:** nuclear weapons (the existing warhead stock, testing and use, untouched since early builds). **New:** uranium and enrichment, inspections, alert levels, deterrence, escalation. **Patch:** summits (step 19 already reads nuclear tests and use), sanctions reasons (step 13), step 18 strikes and interception, the AI's war choices (`stratWar`).
**At risk:** existing nuclear use and its effects, nuclear-armed AI behaviour, summit triggers, old saves with warheads.
- **Material:** uranium is already a core resource (step 24). This step adds what it is used for beyond power: enrichment levels and the weapons path; buying uranium in quantities beyond a country's reactors is noticed by intelligence and inspections.
- **Programme:** civil reactors (power, Step 25) → enrichment facilities (a building; low enrichment is civil, high enrichment is a weapons path) → warhead design (tech) → testing → delivery (step 15's missiles, bombers, submarines). Each stage takes years and money and can be found by intelligence networks (step 7).
- **Inspections:** an inspection agency at the UN: inspections are agreed in treaties or demanded by resolutions; refusing or hiding enrichment is found with some chance and brings resolutions and sanctions. Strikes on enrichment sites use step 18's targeting.
- **Alert level:** each nuclear power has an alert level 5 → 1. Raising it deters attacks and costs relations; level 1 allows use. The AI raises it when its capital or core is threatened.
- **Deterrence:** second-strike capability (submarines, mobile launchers, dispersed bombers, survivable against a first strike) makes a country much harder to attack; the AI weighs it in `stratWar`. Missile defence (step 18) reduces but doesn't cancel it.
- **Escalation ladder:** tactical use on a battlefield → strategic use on military targets → cities. Each step brings summits, world reaction, sanctions and the chance of retaliation in kind; the AI answers by a doctrine per country (no first use, ambiguous, first use when the state is threatened).

**Done when:** a programme climbs from reactor to warhead over years; an inspection finds hidden enrichment and a resolution follows; raising the alert level makes the AI less likely to attack; a second-strike force deters an otherwise winning attacker; tactical use brings an emergency summit and a doctrine-based answer.

## Step 27: Peace conferences
**Rework:** automatic peace terms for the player's wars (`autoTerms`, `applyPeace`; the AI keeps `stratPeace` but uses the new terms). **New:** HOI4-style peace conference: war score as points, turn-based bids, a conference screen.
**At risk:** war goals (step 13), capitulation (`surrenderMonth`), puppets, breakaways and recognition, partial peace, group wars (`ins`, `noPeace`), truces.
- When a war ends (capitulation or an agreed peace), the winners get points from their war score and contribution (battles, occupation, step 18 strike hits); a capitulated loser gives more.
- Demands with costs: annex a province (by development, cheaper if occupied or claimed by our war goal), puppet, release a nation, regime change, reparations (a share of revenue for years), demilitarised zone, disarmament (army and equipment caps for years), give up nuclear programme (Step 26), war crimes tribunal, return of occupied land.
- Turn order by contribution; each winner bids in turn until points run out. AI winners bid by their interests; conflicting bids on the same province go to the bigger contributor. A negotiated peace before capitulation uses the war score both ways (the loser can keep points to refuse demands).
- The screen in the Military tab (or a pop-up via `popAlert`) shows the map of claims, points, bids and each side's stance; the clock pauses.
- Big land grabs raise world tension and sanctions reasons ("unjustified annexation").

**Done when:** a capitulation opens a conference with points from war score; two winners bid in turn and a shared claim goes to the bigger contributor; reparations pay for years; a negotiated peace lets the loser keep land with its points.

## Step 28: Militias 3.0
**New:** playable armed groups outside the Middle East. **Patch:** group nations (Builds 22–23), counter-insurgency (step 14's `coinDay`), `MIL0`/`MILX`, the choice screen.
**At risk:** Middle Eastern groups and their balance, takeovers (`gnTakeover`), group supply, sponsors (`gnAskMore`, `gnLump`).
- **Playable groups:** real groups in the Sahel (JNIM is jihadist, so not playable; Tuareg movements yes), Myanmar (Arakan Army, Kachin Independence Army, People's Defence Forces), Colombia (ELN, FARC dissidents), the eastern DRC (M23), Ethiopia (Fano), and others with real leaders, aims and backers. Remove the "In progress" label for each region as it's done.
- **Counter-insurgency in occupied foreign land (log fix):** an occupier can run counter-insurgency against groups in land it occupies, with the same two approaches; groups resisting an occupation get more recruits and foreign backers.
- Each region's groups get fitting tunnels/terrain bonuses (jungle, mountains, desert) and sponsor tendencies.

**Done when:** at least one group in each new region is playable with its own leader, aims and backers; an occupier clears a group in occupied land; Middle Eastern balance is unchanged over 5 years.

## Step 29: Refugees and migration
**New:** refugee flows, camps, asylum policy. **Patch:** population (`G.pop`, `movePop`), stability, the UN's aid items (step 19), bloc summits, breakaways.
**At risk:** population totals, step 19's refugee aid agenda (already reads occupied land), economy and labour.
- Wars, occupation, famine (Step 24 food shortages), group takeovers and collapses push people out of provinces each month toward safe neighbours (and further along routes).
- Host countries choose an asylum policy: open, limited, closed (border guards, relations with the origin and bloc partners). Refugees in camps cost money and stability; integrated refugees add workers after a few years.
- Refugees return after peace if their province is safe.
- UN aid resolutions fund hosts; a refugee surge into a bloc member is a bloc summit item (burden sharing).

**Done when:** a war moves people to neighbours; a closed border sends them elsewhere; camps cost money and stability; refugees return after peace; a UN aid resolution pays the host.

## Step 30: The monthly newspaper
**New:** a front page each month. **Patch:** the Annals tab, `llm()` (another caller), pop-ups.
**At risk:** play without an AI provider, the Annals.
- At the start of each month a newspaper pop-up shows a front page built from the past month's biggest events (wars, battles, summits, elections, coups, price shocks, strikes, refugees), ranked by importance and our involvement.
- One headline story, three to five smaller stories, a market box (Step 24 prices), and a short editorial. The paper's name and slant fit our country (a state paper under one-party rule praises the government).
- With an AI provider, one `llm()` call writes the stories from game data; without one, templates write them. Real people are never named except real leaders still in office in the game.
- Past front pages are kept (last 24) in the Annals; the pop-up can be turned off in settings.

**Done when:** a front page appears each month with the month's biggest events; it works with and without an AI provider; a one-party state's paper reads differently from a democracy's.

## Step 31: Images and visual identity (later, owner's call)
Don't start until the owner asks. Agreed direction (2026-10-31): artifacts can't load outside images and no real photos of leaders are used, so:
1. Procedural SVG art in code in one consistent style: generated leader and minister portraits (not resembling real people), icons for buildings, units, resources and battalions, event illustrations, the newspaper masthead.
2. The owner's own art uploaded to the artifact's asset store and wired into events, the choice screen and profiles, replacing the SVG where provided.
3. Map polish: terrain texture, city markers, unit counters, drawn in code.
