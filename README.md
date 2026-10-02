1| [![English](https://img.shields.io/badge/lang-en-red.svg)](#english)
2| [![Czech](https://img.shields.io/badge/lang-cz-blue.svg)](#čeština)
3| 
4| <a name="english"></a>
5| # Game of Life — Python Edition
6| 
7| <p align="center">
8|   <a href="https://github.com/hrosicka/game-of-life-python/blob/master/LICENSE">
9|     <img src="https://img.shields.io/badge/License-MIT-1f6feb?style=for-the-badge&logo=github" alt="License">
10|   </a>
11|   <a href="https://github.com/hrosicka/game-of-life-python/issues">
12|     <img src="https://img.shields.io/badge/Issues-0-ff6b6b?style=for-the-badge&logo=github" alt="Open Issues">
13|   </a>
14|   <a href="https://github.com/hrosicka/game-of-life-python/pulls">
15|     <img src="https://img.shields.io/badge/PRs-0-7c3aed?style=for-the-badge&logo=github" alt="Pull Requests">
16|   </a>
17|   <img src="https://img.shields.io/badge/Repo%20Size-15%20MB-ec4899?style=for-the-badge" alt="Repo Size">
18|   <img src="https://img.shields.io/badge/Last%20Commit-Updated-10b981?style=for-the-badge&logo=git" alt="Last Commit">
19|   <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python" alt="Python">
20|   <a href="https://github.com/hrosicka/game-of-life-python/actions/workflows/tests.yml">
21|     <img src="https://img.shields.io/github/actions/workflow/status/hrosicka/game-of-life-python/tests.yml?branch=master&label=Tests&style=for-the-badge" alt="Tests">
22|   </a>
23|   <a href="https://github.com/hrosicka/game-of-life-python/stargazers">
24|     <img src="https://img.shields.io/badge/Stars-★-ffd43b?style=for-the-badge&logo=github" alt="Stars">
25|   </a>
26|   <a href="https://github.com/hrosicka/game-of-life-python/network/members">
27|     <img src="https://img.shields.io/badge/Forks-↻-94a3b8?style=for-the-badge&logo=github" alt="Forks">
28|   </a>
29|   <a href="https://github.com/hrosicka/game-of-life-python/watchers">
30|     <img src="https://img.shields.io/badge/Watchers-👁-6ee7b7?style=for-the-badge" alt="Watchers">
31|   </a>
32| </p>
33| 
34| A set of small, focused Conway's Game of Life simulations implemented in Python. Each script runs a classic pattern (oscillators, gliders, Gosper glider gun, LWSS, etc.) and renders a live, animated board in the terminal using Rich.
35| 
36| This repository is intended to be:
37| - Educational: clear, simple code for studying Life rules and patterns.
38| - Visual: terminal-based live rendering with Rich.
39| - Extensible: add new patterns or tweak parameters by editing the scripts.
40| 
41| ---
42| 
43| ## Key implementation notes
44| 
45| - Rendering: uses Rich's live rendering (`rich.live.Live`) for smooth, colorful terminal output.
46| - Computation: uses `scipy.signal.convolve2d` to compute neighbor counts efficiently with small convolution kernels.
47| - Configuration: each script contains a `DEFAULT_CONFIG` dict (width, height, delay, characters) — edit these values in the script to change size, speed, and appearance.
48| - Exit: press `Ctrl+C` to stop any running simulation.
49| - Boundary handling:
50|   - Most scripts use toroidal wrap-around boundaries (`boundary='wrap'`) so the grid behaves like a donut (edges wrap).
51|   - The Gosper glider gun script uses non-wrapping / zero-filled boundary (`boundary='fill'`, `fillvalue=0`) to better match the classical presentation.
52| 
53| ---
54| 
55| ## Included scripts
56| 
57| - `game-of-life-pulsar.py` — Pulsar oscillator
58|   - Default config in the script: width 60, height 30, delay ~1.0s in the current main block.
59|   - Uses a full-block character for live cells (good for dense/large displays).
60|   - Places a Pulsar pattern via coordinate list and runs the simulation.
61| 
62| - `game-of-life-toad.py` — Toad oscillator
63|   - Typical config: width 30, height 15, delay 1.0s.
64|   - Uses two-character cell representation (`"o " / "  "`) for clearer spacing.
65| 
66| - `game-of-life-beacon.py` — Beacon oscillator (period 2)
67|   - Typical config: width 30, height 10, delay 1.0s.
67|   - Uses single-character live/dead representation.
68| 
69| - `game-of-life-blinker.py` — Blinker oscillator
70|   - Typical config: width 15, height 7, delay 0.5s.
71|   - Uses `"o " / "  "` style cells.
72| 
73| - `game-of-life-glider.py` — Glider patterns (several gliders)
74|   - Typical config: width 30, height 15, delay 0.5s.
75|   - Places two gliders and demonstrates toroidal wrap behavior.
76| 
77| - `game-of-life-gun.py` — Gosper Glider Gun
78|   - Typical config: width 100, height 40, low delay (e.g., 0.01s) for smooth glider motion.
79|   - Uses `boundary='fill'` (non-wrapping) so generated gliders travel across empty space.
79|   - Uses Rich Live with `screen=True` for an alternate buffer (full-screen-like display).
80| 
81| - `game-of-life-lwss.py` — Lightweight spaceship (LWSS) pattern
82|   - Implements the small ship pattern and renders it live (adjustable config inside the script).
| 
83| - `tests/` — placeholder directory for tests (currently empty)
84| 
85| ---
86| 
87| ## Requirements
88| 
89| - Python 3.8+ (recommended)
90| - numpy
91| - scipy
92| - rich
93| 
94| Install dependencies with pip:
95| 
96| ```bash
97| pip install numpy scipy rich
98| ```
99| 
100| (If you plan to run the scripts inside virtualenv or venv, create and activate it first.)
101| 
102| ---
103| 
104| ## Usage
105| 
106| Run any script from your terminal. Example:
107| 
108| ```bash
109| python game-of-life-pulsar.py
110| python game-of-life-toad.py
111| python game-of-life-beacon.py
112| python game-of-life-blinker.py
113| python game-of-life-glider.py
114| python game-of-life-gun.py
115| python game-of-life-lwss.py
116| ```
117| 
118| Tips:
119| - If SciPy is not installed, each script prints an error message and exits (scripts check for `scipy.signal.convolve2d`).
120| - To change grid size, speed, or characters, edit the `DEFAULT_CONFIG` dictionary near the top of the script you want to change.
121| - For the Gosper Glider Gun script, `screen=True` is enabled for Live; if your terminal behaves oddly try removing `screen=True` in the `Live(...)` call.
122| 
123| ---
124| 
125| ## Extending / Adding patterns
126| 
127| 1. Copy an existing script (e.g., `game-of-life-toad.py`) and rename it.
128| 2. Update the pattern coordinates or create a new coordinate list for your pattern.
129| 3. Adjust `DEFAULT_CONFIG` (width, height, delay, characters) if needed.
130| 4. Run the script and observe the pattern.
131| 5. If you'd like, open a PR to share new patterns.
132| 
133| ---
134| 
135| ## Troubleshooting
136| 
137| - Terminal rendering looks garbled:
138|   - Try a different font/terminal or adjust the cell character width in the script (some scripts use two-character cells like `"o "` for spacing).
139|   - If color/Unicode characters look off, change `live_cell_char`/`dead_cell_char` in the script to simpler ASCII characters.
140| - SciPy import error:
141|   - Install SciPy with `pip install scipy` (or `pip install numpy scipy`).
142| - Performance:
143|   - Very large grids with small delay may be CPU-heavy; increase `delay_seconds` or reduce grid size.
144|   
145| ---
146|   
147| ## About Conway’s Game of Life
148| 
149| Conway’s Game of Life is a zero-player game—set the rules and observe endless emergent complexity! With simple laws governing cell birth and death, patterns emerge, oscillate, and sometimes travel across the grid.
150| 
151| [Learn more about Conway’s Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).
152| 
153| ---
154| 
155| ## Author
156| 
157| Lovingly crafted by [Hanka Robovska](https://github.com/hrosicka) 👩‍🔬
158| 
159| ---
160| 
161| ## License
162| 
163| MIT License. This project is open for educational and entertainment use.
164| 
165| ---
166| ---
167| 
168| <a name="čeština"></a>
169| # Hra života — Python edice
170| 
171| <p align="center">
172|   <a href="https://github.com/hrosicka/game-of-life-python/blob/master/LICENSE">
173|     <img src="https://img.shields.io/badge/License-MIT-1f6feb?style=for-the-badge&logo=github" alt="License">
174|   </a>
175|   <a href="https://github.com/hrosicka/game-of-life-python/issues">
176|     <img src="https://img.shields.io/badge/Issues-0-ff6b6b?style=for-the-badge&logo=github" alt="Open Issues">
177|   </a>
178|   <a href="https://github.com/hrosicka/game-of-life-python/pulls">
179|     <img src="https://img.shields.io/badge/PRs-0-7c3aed?style=for-the-badge&logo=github" alt="Pull Requests">
180|   </a>
181|   <img src="https://img.shields.io/badge/Repo%20Size-15%20MB-ec4899?style=for-the-badge" alt="Repo Size">
182|   <img src="https://img.shields.io/badge/Last%20Commit-Updated-10b981?style=for-the-badge&logo=git" alt="Last Commit">
183|   <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python" alt="Python">
184|   <a href="https://github.com/hrosicka/game-of-life-python/actions/workflows/tests.yml">
185|     <img src="https://img.shields.io/github/actions/workflow/status/hrosicka/game-of-life-python/tests.yml?branch=master&label=Tests&style=for-the-badge" alt="Tests">
186|   </a>
187|   <a href="https://github.com/hrosicka/game-of-life-python/stargazers">
188|     <img src="https://img.shields.io/badge/Stars-★-ffd43b?style=for-the-badge&logo=github" alt="Stars">
189|   </a>
190|   <a href="https://github.com/hrosicka/game-of-life-python/network/members">
191|     <img src="https://img.shields.io/badge/Forks-↻-94a3b8?style=for-the-badge&logo=github" alt="Forks">
192|   </a>
193|   <a href="https://github.com/hrosicka/game-of-life-python/watchers">
194|     <img src="https://img.shields.io/badge/Watchers-👁-6ee7b7?style=for-the-badge" alt="Watchers">
195|   </a>
196| </p>
197| 
198| Sada malých, úzce zaměřených simulací Conwayovy hry života implementovaných v Pythonu. Každý skript spouští klasický vzor (oscilátory, kluzáky, Gosperovo dělo na kluzáky, LWSS atd.) a vykresluje živou, animovanou mřížku v terminálu s využitím Rich.
199| 
200| Tento repozitář má sloužit jako:
201| - **Vzdělávací pomůcka:** jasný a jednoduchý kód pro studium pravidel a vzorů Hry života.
202| - **Vizuální zážitek:** živé vykreslování v terminálu s využitím Rich.
203| - **Rozšiřitelný základ:** úpravou skriptů můžete snadno přidávat nové vzory nebo ladit parametry.
204| 
205| ---
206| 
207| ## Klíčové poznámky k implementaci
208| 
209| - **Vykreslování:** používá živé vykreslování (`rich.live.Live`) pro plynulý a barevný výstup v terminálu.
210| - **Výpočet:** využívá `scipy.signal.convolve2d` pro efektivní výpočet počtu sousedů pomocí malých konvolučních jader.
211| - **Konfigurace:** každý skript obsahuje slovník `DEFAULT_CONFIG` (šířka, výška, prodleva, znaky) — úpravou těchto hodnot přímo ve skriptu změníte velikost, rychlost a vzhled.
212| - **Ukončení:** libovolnou běžící simulaci zastavíte stisknutím `Ctrl+C`.
213| - **Zpracování okrajů:**
214|   - Většina skriptů používá toroidální (cyklické) hranice (`boundary='wrap'`), takže se mřížka chová jako povrch koblížku (okraje jsou propojené).
215|   - Skript pro Gosperovo dělo na kluzáky používá necyklické hranice vyplněné nulami (`boundary='fill'`, `fillvalue=0`), aby lépe odpovídal klasické prezentaci.
216| 
217| ---
218| 
219| ## Obsažené skripty
220| 
221| - `game-of-life-pulsar.py` — Oscilátor Pulsar
222|   - Výchozí konfigurace ve skriptu: šířka 60, výška 30, prodleva cca 1,0 s.
223|   - Používá znak plného bloku pro živé buňky (vhodné pro husté/velké zobrazení).
224|   - Umístí vzor Pulsar pomocí seznamu souřadnic a spustí simulaci.
225| 
226| - `game-of-life-toad.py` — Oscilátor Toad (Ropucha)
227|   - Typická konfigurace: šířka 30, výška 15, prodleva 1,0 s.
228|   - Používá dvouznakovou reprezentaci buněk (`"o " / "  "`) pro přehlednější rozestupy.
229| 
230| - `game-of-life-beacon.py` — Oscilátor Beacon (Maják, perioda 2)
231|   - Typická konfigurace: šířka 30, výška 10, prodleva 1,0 s.
232|   - Používá jednoznakovou reprezentaci pro živé/mrtvé buňky.
233| 
234| - `game-of-life-blinker.py` — Oscilátor Blinker (Blikač)
235|   - Typická konfigurace: šířka 15, výška 7, prodleva 0,5 s.
236|   - Používá styl buněk `"o " / "  "`.
237| 
238| - `game-of-life-glider.py` — Vzory kluzáků (několik Gliderů)
239|   - Typická konfigurace: šířka 30, výška 15, prodleva 0,5 s.
240|   - Umístí dva kluzáky a demonstruje chování toroidních hranic.
241| 
242| - `game-of-life-gun.py` — Gosper Glider Gun (Dělo na kluzáky)
243|   - Typická konfigurace: šířka 100, výška 40, nízká prodleva (např. 0,01 s) pro plynulý pohyb.
244|   - Používá `boundary='fill'` (necyklické), takže generované kluzáky cestují prázdným prostorem.
245|   - Využívá Rich Live s parametrem `screen=True` pro alternativní buffer (zobrazení přes celou obrazovku).
246| 
247| - `game-of-life-lwss.py` — Vzor Lightweight spaceship (LWSS, Malá vesmírná loď)
248|   - Implementuje vzor malé vesmírné lodi a vykresluje jej živě (nastavitelná konfigurace uvnitř skriptu).
249| 
250| - `tests/` — složka pro testy (aktuálně prázdná)
251| 
252| ---
253| 
254| ## Požadavky
255| 
256| - Python 3.8+ (doporučeno)
257| - numpy
258| - scipy
259| - rich
260| 
261| Nainstalujte závislosti pomocí pip:
262| 
263| ```bash
264| pip install numpy scipy rich
265| ```
266| 
267| (Pokud plánujete spouštět skripty ve virtuálním prostředí, nezapomeňte jej nejdříve vytvořit a aktivovat.)
268| 
269| ---
270| 
271| ## Použití
272| 
273| Spusťte libovolný skript z vašeho terminálu. Příklady:
274| 
275| ```bash
276| python game-of-life-pulsar.py
277| python game-of-life-toad.py
278| python game-of-life-beacon.py
279| python game-of-life-blinker.py
280| python game-of-life-glider.py
281| python game-of-life-gun.py
282| python game-of-life-lwss.py
283| ```
284| 
285| Tipy:
286| - Pokud není nainstalováno SciPy, skript vypíše chybu a ukončí se (vyžaduje se `scipy.signal.convolve2d`).
287| - Chcete-li změnit velikost mřížky, rychlost nebo použité znaky, upravte slovník `DEFAULT_CONFIG` v horní části daného skriptu.
288| - U skriptu Gosper Glider Gun je zapnut režim `screen=True` Pokud se váš terminál chová podivně, zkuste tento parametr z volání `screen=True` in the `Live(...)` odstranit.
289| 
290| ---
291| 
292| ## Rozšiřování a přidávání vzorů
293| 
294| 1. CZkopírujte existující skript (např. `game-of-life-toad.py`) a přejmenujte jej.
295| 2. Aktualizujte souřadnice vzoru nebo vytvořte vlastní seznam souřadnic.
296| 3. Podle potřeby upravte `DEFAULT_CONFIG` (šířka, výška, prodleva, znaky).
297| 4. Spusťte skript a sledujte výsledek.
298| 5. Budete-li chtít, otevřete Pull Request a sdílejte své nové vzory s ostatními!
299| 
300| ---
301| 
302| ## Řešení problémů
303| 
304| - Vykreslování v terminálu vypadá rozbitě:
305|   - Zkuste jiný font/terminál nebo upravte šířku znaků ve skriptu (některé používají dva znaky jako `"o "` pro lepší formátování).
306|   - Pokud jsou problémy s barvami nebo Unicode znaky, změňte `live_cell_char`/`dead_cell_char` ve skriptu na prosté ASCII znaky.
307| - Chyba při importu SciPy:
308|   - Nainstalujte knihovnu pomocí `pip install scipy` (or `pip install numpy scipy`).
309| - Výkon:
|   - Velmi velké mřížky s minimální prodlevou mohou být náročné na CPU. V takovém případě zvyšte `delay_seconds` nebo zmenšete rozměry mřížky.
310|  
311| ---
312| 
313| ## O Conwayově hře života
314| 
315| Conwayova hra života je hra pro nula hráčů — stačí nastavit pravidla a sledovat! Z jednoduchých pravidel pro zrod a zánik buněk vznikají vzory, které oscilují, cestují prostorem a vytvářejí rozmanité struktury.
316| 
317| [Learn more about Conway’s Game of Life](https://cs.wikipedia.org/wiki/Hra_života).
318| 
319| ---
320| 
321| ## Autor
322| 
323| S láskou vytvořila [Hanka Robovska](https://github.com/hrosicka) 👩‍🔬
324| 
325| ---
326| 
327| ## Licence
328| 
329| MIT Licence. Tento projekt je otevřen pro vzdělávací i zábavné účely.
