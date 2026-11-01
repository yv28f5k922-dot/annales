# Step 24.2: where the resources are

Build 24.2 "Ho Chi Minh" (2026-11-01) replaced the random placement of deposits (a hash of province names inside each producing country) with their real locations. The table lives in `src/world.src.html` as `DEPW` (resource → country → map province → weight). A weight is that province's share of the country's output in deposit units; each country's total equals its old deposit count, so world supply, prices and balance are unchanged. Iron ore and bauxite only switch on the steel and aluminium bonus, so their weights are unused. `rsProd` and `resIncome` multiply each province's output by its weight (`depW`).

The map's provinces are large regions, so a deposit sits in the region that contains it (for example Brazil's `Espírito Santo` region also covers Rio de Janeiro and its offshore pre-salt fields, Kazakhstan's `Zhambyl` region covers Turkistan's uranium fields, and Guinea's `Gaoual` region covers the Boké bauxite district).

## Oil

- **SAU:** Eastern Province 2.6, Riyadh .4
- **RUS:** Khanty-Mansiy 1.8, Yamal-Nenets .6, Tatarstan .4, Orenburg .4, Bashkortostan .2, Komi .2, Tomsk .2, Sakha (Yakutia) .2
- **USA:** Texas 1.5, New Mexico .5, Arkansas .4, Kansas .25, Alaska .2, Colorado .15
- **IRQ:** Basra 1.5, Kirkuk .3, Maysan .2
- **IRN:** Khuzestan 1.6, Kohgiluyeh .2, Bushehr .2
- **ARE:** Abu Dhabi 1
- **KWT:** Kuwait 1
- **CAN:** Alberta 1.6, Saskatchewan .3, Newfoundland and Labrador .1
- **VEN:** Anzoátegui 1.3, Zulia .7
- **NGA:** Cross River 1
- **LBY:** Ajdabiya .6, Murzuq .25, Al Kufrah .15
- **KAZ:** Aqtöbe .85, Qyzylorda .15
- **NOR:** Oslo .6, Hedmark .3, Finnmark .1
- **MEX:** Campeche .8, Chiapas .2
- **BRA:** Espírito Santo .8, São Paulo .2
- **QAT:** Al Rayyan 1
- **DZA:** Ouargla 1
- **AGO:** Luanda .6, Uíge .4
- **OMN:** Al Wusta .4, Al Dhahira .3, Dhofar .3
- **CHN:** Heilongjiang .5, Xinjiang .5, Shaanxi .4, Shandong .3, Beijing .3
- **GBR:** Highland 1
- **AZE:** Baku 1
- **COL:** Casanare .6, Vichada .4
- **ECU:** Pastaza 1

## Natural gas

- **RUS:** Yamal-Nenets 2.4, Orenburg .2, Sakha (Yakutia) .2, Khabarovsk .2
- **USA:** Texas .6, New York .6, Arkansas .3, New Mexico .2, Kansas .15, Washington .15
- **IRN:** Bushehr 1.4, Khuzestan .3, Hormozgan .2, Razavi Khorasan .1
- **QAT:** Doha 1
- **CAN:** Alberta .7, British Columbia .3
- **CHN:** Sichuan .4, Shaanxi .3, Xinjiang .3
- **AUS:** Western Australia 1.4, Queensland .5, Northern Territory .1
- **NOR:** Oslo .5, Hedmark .35, Finnmark .15
- **SAU:** Eastern Province 1
- **DZA:** Ouargla .7, Illizi .3
- **TKM:** Chardzhou .7, Balkan .2, Ashgabat .1
- **MYS:** Sarawak .7, Sabah .3
- **EGY:** Port Said .5, Beheira .3, Matrouh .2
- **IDN:** Kalimantan Timur .4, Papua Barat .3, Sumatera Selatan .3
- **UZB:** Kashkadarya .6, Navoi .4
- **NGA:** Cross River 1
- **ARE:** Abu Dhabi 1
- **NLD:** Amsterdam 1

## Rare earths

- **are:** Inner Mongol 1.9, Sichuan .5, Jiangxi .4, Guangdong .1, Guangxi .1
- **USA:** California 1
- **MMR:** Sagaing 1
- **AUS:** Western Australia 1
- **THA:** Northern .6, Southern .4
- **VNM:** Son La 1
- **IND:** Odisha .5, Tamil Nadu .5
- **RUS:** Murmansk 1
- **BRA:** Minas Gerais .6, Brasília .4
- **MDG:** Sofia .6, Atsimo-Andrefana .4
- **ZAF:** Cape Town .6, Limpopo .4
- **COD:** Nord-Kivu .5, Katanga .5

## Food

- **ain:** Missouri .9, Kansas .7, Nebraska .7, Minnesota .4, Ohio .3
- **CHN:** Henan .6, Heilongjiang .6, Shandong .5, Jilin .3, Anhui .3, Jiangsu .3, Beijing .2, Sichuan .2
- **IND:** Uttar Pradesh .7, North .6, Madhya Pradesh .3, West Bengal .2, Bihar .2
- **RUS:** Rostov .9, Voronezh .4, Volgograd .3, Altay .2, Tatarstan .2
- **UKR:** k .5, Kharkiv .5, Odessa .4, Kyiv .3, Zhytomyr .3
- **BRA:** Mato Grosso .9, Rio Grande do Sul .4, São Paulo .3, Mato Grosso do Sul .2, Brasília .2
- **ARG:** Buenos Aires .8, Córdoba .6, Santa Fe .6
- **CAN:** Saskatchewan 1, Alberta .6, Manitoba .4
- **FRA:** Paris .5, Grand Est .3, Nouvelle-Aquitaine .2
- **AUS:** New South Wales .8, Western Australia .8, Victoria .2, South Australia .2
- **KAZ:** North Kazakhstan .5, Qostanay .35, Nur-Sultan .15
- **DEU:** Niedersachsen .5, Bayern .5
- **POL:** Greater Poland .5, Lublin .5
- **TUR:** Konya 1
- **PAK:** Punjab .8, Sind .2
- **IDN:** Jawa Timur 1
- **EGY:** Beheira .3, Kafr el-Sheikh .2, Dakahlia .2, Sharqia .2, Minya .1
- **ROU:** Bucharest .6, Timis .4
- **HUN:** Budapest .5, Somogy .5

## Uranium

- **ran:** Zhambyl 1.8, Qyzylorda 1, North Kazakhstan .2
- **CAN:** Saskatchewan 2
- **AUS:** South Australia 2
- **NAM:** Kunene 1
- **NER:** Agadez 1
- **UZB:** Navoi 1
- **RUS:** Irkutsk .7

## Iron ore and coal (steel input; yes/no)

- **ron:** Beijing 1, Liaoning 1, Sichuan 1, Inner Mongol 1
- **AUS:** Western Australia 1, South Australia 1
- **BRA:** Pará 1, Minas Gerais 1
- **IND:** Odisha 1, Jharkhand 1, Karnataka 1
- **RUS:** Voronezh 1, Murmansk 1, Sverdlovsk 1, Karelia 1
- **UKR:** k 1
- **USA:** Minnesota 1, Michigan 1
- **CAN:** Québec 1, Newfoundland and Labrador 1
- **ZAF:** Northern Cape 1
- **SWE:** Norrbotten 1

## Bauxite (aluminium input; yes/no)

- **aux:** Queensland 1, Western Australia 1, Northern Territory 1
- **GIN:** Gaoual 1, Faranah 1
- **CHN:** Shanxi 1, Henan 1, Guangxi 1, Guizhou 1
- **BRA:** Pará 1
- **IND:** Odisha 1
- **IDN:** Kepulauan Riau 1, Kalimantan Selatan 1
- **JAM:** Jamaica 1

## Sources

- Uranium in Kazakhstan (Turkistan, Kyzylorda and North Kazakhstan regions): [Astana Times, Kazakhstan's uranium industry: sites and production](https://astanatimes.com/2024/08/kazakhstans-uranium-industry-sites-and-production/)
- Rare earths in China (Inner Mongolia's Bayan Obo about 83% of reserves; Sichuan; ion-clay deposits in Jiangxi, Guangdong, Guangxi): [China Briefing](https://www.china-briefing.com/news/elementos-de-tierras-raras-comprendiendo-el-dominio-de-china-en-las-cadenas-de-suministro-mundiales/)
- Rare earths in Myanmar (Kachin State, Pangwa and Chipwi): [Frontier Myanmar](https://www.frontiermyanmar.net/en/strategic-bargaining-chips-kachins-rare-earth-mining-pause/)
- Bauxite in Guinea (Sangaredi, Boké, Fria, Dian-Dian, Debele): [USGS Minerals Yearbook 2019, Guinea](https://pubs.usgs.gov/myb/vol3/2019/myb3-2019-guinea.pdf)
- The rest (oil and gas fields, grain belts, iron ore and bauxite districts, other uranium mines) follows standard references: EIA country analyses, USGS Mineral Commodity Summaries, World Nuclear Association country profiles and FAO production statistics. Weights are rounded estimates of each region's share, not exact statistics.
