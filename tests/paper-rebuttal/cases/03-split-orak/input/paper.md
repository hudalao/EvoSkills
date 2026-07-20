### O RAK : A F OUNDATIONAL B ENCHMARK FOR T RAINING AND E VALUATING LLM A GENTS ON D IVERSE V IDEO G AMES

**Dongmin Park** [1] _[†∗]_ **, Minkyu Kim** [1] _[†∗]_ **, Beongjun Choi** [1] _[†∗]_ **, Junhyuck Kim** [1] _[†]_ **, Keon Lee** [1] _[†]_ **, Jonghyun Lee** [1] _[†]_ **,**
**Inkyu Park** [1] _[†]_ **, Byeong-Uk Lee** [1] _[†]_ **, Jaeyoung Hwang** [1] _[†]_ **, Jaewoo Ahn** [1] _[,]_ [2] _[†]_ **, Ameya S. Mahabaleshwarkar** [3] **,**
**Bilal Kartal** [3] **, Pritam Biswas** [3] **, Yoshi Suhara** [3] **, Kangwook Lee** [1] _[,]_ [4] **, Jaewoong Cho** [1]

1 KRAFTON, 2 Seoul National University, 3 NVIDIA, 4 University of Wisconsin-Madison


A BSTRACT


Large Language Model (LLM) agents are reshaping the game industry, by enabling
more intelligent and human-preferable characters. Yet, current game benchmarks
fall short of practical needs: they lack evaluations of diverse LLM capabilities
across various game genres, studies of agentic modules crucial for complex gameplay, and fine-tuning datasets to adapt pre-trained LLMs into gaming agents. To
fill these gaps, we present **Orak**, a benchmark for training and evaluating LLM
agents across 12 popular video games spanning all major genres. Using a plug-andplay interface built on Model Context Protocol (MCP), Orak supports systematic
and reproducible studies of agentic modules in varied game scenarios. We further release a fine-tuning dataset of expert LLM gameplay trajectories covering
multiple genres, turning general LLMs into effective game agents. Orak offers a
united evaluation framework, including game leaderboards, LLM battle arenas,
and in-depth analyses of input modality, agentic strategies, and fine-tuning effects,
establishing a foundation towards versatile gaming agents. Code is available at
[https://github.com/krafton-ai/Orak.](https://github.com/krafton-ai/Orak)


1 I NTRODUCTION


Large Language Model (LLM) agents are revolutionizing various industries (Wang et al., 2024a),
and well-established benchmarks play a key role in unlocking their abilities on complex tasks, _e.g._,
Coding (Hendrycks et al., 2021; Zhuo et al., 2024), Web Search (Liu et al., 2023; Pan et al., 2024;
Levy et al., 2024), and Scientific Research (Muhlbacher et al. ¨, 2024; Zhang et al., 2025). In game
industry, there is growing interest in using LLM agents to enhance user game experiences _e.g._, more
intelligent non-player characters (NPCs), monsters, or companions (NVIDIA, 2025). In response,
many benchmarks have been proposed to assess the ability of LLMs to play games (Hu et al., 2024b).


While these benchmarks have effectively utilized games to evaluate LLMs’ general capabilities, they
exhibit three major limitations: 1) they often rely on _text-only_ games or _2D-grid_ simulators rather
than complex real video games, 2) they offer insufficient assessment of _agentic_ modules, such as
self-reflection, memory, and tool use, which are essential to complex gameplay, and 3) they lack
_fine-tuning_ datasets necessary to adapt pre-trained LLMs into effective gameplay agents, which
significantly hinder the adoption of LLM agents in real-world video games.


To this end, we present **Orak**, a foundational benchmark designed to evaluate LLM agents across
diverse video games. As shown in Figure 1, Orak includes 12 video games played by millions to
billions of users worldwide: _Street Fighter III_, _Super Mario_, _Ace Attorney_, _Her Story_, _Pokemon Red_ _´_,
_Darkest Dungeon_, _Minecraft_, _Stardew Valley_, _StarCraft II_, _Slay the Spire_, _Baba Is You_, and _2048_ .
These games span 6 major game genres, _i.e._, action, adventure, role-playing, simulation, strategy, and
puzzle, enabling a _comprehensive_ assessment of key abilities required for versatile gameplay; action
games enable testing fine-grained player control, adventure games challenge long-term memory and
error handling, and strategy/puzzle games require complex logical reasoning and multi-step planning.


_∗_ Equal contribution. _†_ Core contribution.


1


A benchmark toward


|Models|Col2|Col3|
|---|---|---|
|GPT-4o|29.7|38.9|
|Claude|16.7|63.9|


|Models|Elo|
|---|---|
|GPT-4o|1602.9|
|Gemini-2.5-pro|1453.0|
















|Environment with 12 Video Games<br>Action Adventure RPG Simulation Strategy Puzzle|Col2|Col3|Col4|
|---|---|---|---|
|**LLM Agent**<br>Agentic Modules<br>Tools<br>Prompts<br>LLMs|**Configs**<br>- Game<br>- LLM<br>- Agent Strategy<br>MCP interface<br>MCP interface<br>**Evaluator**<br>**Return**<br>- Score<br>→|**Configs**<br>- Game<br>- LLM<br>- Agent Strategy<br>MCP interface<br>MCP interface<br>**Evaluator**<br>**Return**<br>- Score<br>→|terface|
|**LLM Agent**<br>Agentic Modules<br>Tools<br>Prompts<br>LLMs|**Configs**<br>- Game<br>- LLM<br>- Agent Strategy<br>MCP interface<br>MCP interface<br>**Evaluator**<br>**Return**<br>- Score<br>→|**Configs**<br>- Game<br>- LLM<br>- Agent Strategy<br>**Evaluator**<br>**Return**<br>- Score<br>→|**Configs**<br>- Game<br>- LLM<br>- Agent Strategy<br>**Evaluator**<br>**Return**<br>- Score<br>→|
|**LLM Agent**<br>Agentic Modules<br>Tools<br>Prompts<br>LLMs|MCP i|MCP i|MCP i|


|Models<br>GPT-4o 29.7 38.9 …<br>Claude 16.7 63.9<br>…<br>Gameplay Leaderboard|Col2|Models Elo<br>GPT-4o 1602.9<br>Gemini-2.5-pro 1453.0<br>…<br>LLM Battle Arena|
|---|---|---|
|||**Fine-tuning Study**<br>LLaMA3.2-1B<br>LLaMA3.2-3B<br>OOD Game Score|
|**Genre**|**_1st_ Agentic Strategy**|**_1st_ Agentic Strategy**|
|Adventure|Reflection Agent|Reflection Agent|
|Puzzle|Planning Agent|Planning Agent|
|**Agent Study**<br>…|**Agent Study**<br>…|**Agent Study**<br>…|



Figure 1: Overview of Orak, a benchmark designed to train and evaluate LLM agents across 12 video
games across genres. Using MCP as a plug-and-play interface, it ensures systematic assessment,
supporting gameplay leaderboards, battle arenas, and studies on agentic modules and fine-tuning.


With the use of _real_ video games, Orak also ensures evaluation on rich, dynamic environments with
varying stages, levels, and story-driven quests, which are even challenging for humans.


To enable consistent evaluation of rapidly evolving LLMs, we introduce a _plug-and-play_ interface
using Model Context Protocol (MCP) (Hou et al., 2025), allowing LLMs to seamlessly interact with
agentic modules in gameplay. Each game environment and agentic module package operates as an
independent MCP server, providing game mechanics ( _e.g._, retrieving game states, executing game
steps) or agentic strategies ( _e.g._, reflection, planning) as callable tools to LLMs. During evaluation,
LLM interacts with these servers by sequentially retrieving game states, performing action inference
using agentic modules, and executing game steps, which enables streamlined evaluation across diverse
games and supports controlled studies of various agentic modules.


In addition, we release a fine-tuning dataset that aims to transform pre-trained LLMs into effective
gaming agents. The dataset consists of game interaction trajectories generated by expert LLMs,
_e.g.,_ GPT-4o, using core agentic strategies on all games in Orak. These trajectories encapsulate
meta-knowledge on how and when to use the agentic strategies to play various genres of games,
leading to more resource-efficient and effective gaming agents.


Our benchmark offers comprehensive evaluation dimensions, including game score leaderboards,
competitive LLM battle arenas, and in-depth analyses of visual input state, agentic strategies, and
fine-tuning effects. Extensive experiments on Orak with 15 LLMs reveal that (1) proprietary LLMs
achieve superior performance across games with significant gaps from open-source LLMs, (2) their
performance gap becomes narrow in battle scenarios, (3) proprietary LLMs benefit from extended
agentic workflows, while open-source LLMs show limited gains, (4) visual states often hinder
gameplay performance yet, and (5) fine-tuning enables effective transfer of gameplay meta-knowledge
from larger LLMs to smaller ones, leading to generalization in intra-game, out-of-distribution (OOD)
game, and non-game unseen scenarios like math and web interaction. We believe that Orak not
only establishes a foundation for building gaming agents but also serves as a critical benchmark for
evaluating general LLMs on realistic, long-horizon decision-making tasks.


2 R ELATED W ORK


**Playing Games by LLMs.** Many works have explored the use of LLMs for gameplay. Early efforts
focused on _text-based_ games such as Jericho (Hausknecht et al., 2020), Zork (Tsai et al., 2023), and
TextCraft (Prasad et al., 2023), where LLMs navigate textual environments with reasoning. Subsequent work shifted toward _2D-grid_ games, including Chess (Feng et al., 2023), NetHack (Kuttler ¨
et al., 2020), and Crafter (Hafner, 2021), where spatial reasoning and puzzle-solving skills became
more important. More recently, several studies have applied LLMs, combined with _agentic_ workflows, to play more complex _video_ games, such as Minecraft (Fan et al., 2022; Wang et al., 2023),
Civilization (Qi et al., 2024), Pokemon ( ´ Hu et al., 2024c), and StarCraft (Ma et al., 2024). However,
these approaches rely on manually customized agentic workflows for each specific game, limiting
their usability toward developing a general gaming agent.


2


Benchmarks Game Domain Full Genre # Games Model Type Agent Ablation Fine-tuning Set


GAMA-bench (Huang et al., 2024) Text ✗ 8 LLM ✗ ✗
GameBench (Costarelli et al., 2024) Text ✗ 9 LLM ✗ ✗
GameArena (Hu et al., 2024a) Text ✗ 6 LLM ✗ ✗
SmartPlay (Wu et al., 2023) Text/2D-grid ✗ 6 LLM ✗ ✗
Balrog (Paglieri et al., 2024) Text/2D-grid ✗ 6 LLM/VLM ✗ ✗
LVLM-Playground (Wang et al., 2025) 2D-grid ✗ 6 VLM ✗ ✗
Cradle (Tan et al., 2024) Video ✗ 4 VLM ✗ ✗
V-MAGE (Zheng et al., 2025) Video ✗ 5 VLM ✗ ✗
DSGBench (Tang et al., 2025) Video ✗ 6 LLM ✗ ✗
LMGame-Bench (Hu et al., 2025) Video ✗ 6 LLM/VLM ✗ ✗


**Orak (Ours)** Video ✓ 12 LLM/VLM ✓ ✓


Table 1: Game Benchmark Comparison. ‘Full Genre’ means whether six major genres are fully covered. ‘Model Type’ indicates whether the benchmark supports LLMs or VLMs. Unlike prior benchmarks, Orak is the _only_ benchmark that fully covers all major genres, supports both LLMs/VLMs,
provides ablation studies for agent modules, and releases a fine-tuning set.


**Evaluation Benchmarks for LLMs with Games.** As gameplay requires complex cognitive abilities, _e.g._, context understanding, logical reasoning, and error handling, several recent benchmarks
have sought to evaluate LLMs or Vision Language Models (VLMs) on games (Hu et al., 2024b).
GAMA-Bench (Huang et al., 2024), GameBench (Costarelli et al., 2024), GameArena (Hu et al.,
2024a), and SmartPlay (Wu et al., 2023) focus on _text-based_ games, assessing LLMs’ ability to navigate and reason on textual environments. Barlog (Paglieri et al., 2024) and LVLM-Playground (Wang
et al., 2025) are mainly based on _2D-grid_ games, such as TicTacToe and Chess, to evaluate the spatial
and visual reasoning capabilities of LLMs/VLMs. Using video games, Cradle (Tan et al., 2024)
evaluates VLMs in 1 adventure and 3 simulation games, V-MAGE (Zheng et al., 2025) assesses
VLMs on 5 action games, DSGBench (Tang et al., 2025) validates LLMs on 6 strategic games, and
LMGame-Bench (Hu et al., 2025) mainly focus on puzzle games. Despite their contributions, existing
benchmarks lack full coverage of game genres, omit in-depth studies on agentic modules, often rely
on visual inputs, and under-explore the way to align pre-trained LLMs into versatile game agents.
Table 1 summarizes the key characteristics of game benchmarks.


**Fine-tuning LLMs toward Agents.** To enhance agent capability, many efforts have proposed agentic strategies, e.g., chain-of-thought reasoning (Wei et al., 2022; Yao et al., 2023), self-reflection (Shinn
et al., 2023; Park et al., 2023), hierarchical task planning (Huang et al., 2022b;a), and skill libraries (Wang et al., 2023). Complementing these advancements, efforts have focused on fine-tuning
strategies tailored to LLM agents, which span two main directions: data-centric approaches, which
involve fine-tuning on curated expert demonstrations (Chen et al., 2023; Zeng et al., 2023; Chen et al.,
2024); and framework-oriented approaches, which focus on learning from agentic interactions (Feng
et al., 2024; Chen et al., 2025; Putta et al., 2024). Notably, FireAct (Chen et al., 2023) emphasizes
unified data formatting and CodeAct (Wang et al., 2024b) highlights the importance of high-quality
curation of training trajectories. However, fine-tuning methods for game-playing agents remain
largely explored. Unlike structured tasks in web, programming, or math domains, games involve
large, dynamic, and partially observable state spaces, which requires agents to generalize across a
variety of situations and learn diverse behavior patterns, posing unique challenges.


3 O RAK


We propose Orak, a benchmark designed to evaluate LLM agents across diverse video games.
Figure 2 illustrates the evaluation pipeline of Orak, which is self-explanatory with code structures. By
integrating the MCP interface with game environments and agentic modules, Orak enables _systematic_
and _plug-and-play_ evaluation of backbone LLMs with agentic strategies across various games. For
evaluation, the game score is obtained by simply configuring the game, LLM backbone, and agentic
strategy in eval.py . At each game step, the game observation is retrieved, the specified agent
strategy is executed by the LLM, and the resulting action is applied to the game. This loop continues
until the game ends or reaches the maximum step limit, after which the game score is recorded. Note
that, with MCP interface, users can readily customize their agentic strategy, _i.e._, calling a single
agentic module or multiple agentic modules sequentially. In the following section, we describe the
12 game environments in Orak, along with the submission guidelines for the benchmark leaderboard.


3


|env.py<br>Class GameEnv(gym.env):<br>def obs2text(obs):<br>return text<br>def text2act(text):<br>return act<br>def step(act):<br>return obs|Col2|Col3|
|---|---|---|
|**agent.py**<br>**`ClassAgent`**`():`<br>`  memory = Memory()`<br> <br> **`def reflection`**`(llm, text)`<br>`     return text_output`<br> <br> **`def planning`**`(llm, text)`<br>`     return text_output`<br> <br>...<br>Memory<br>Knowledge DB<br>Skill manager<br>Planning<br>Self-reflection<br>Tools<br>Prompts<br>...|**agent.py**<br>**`ClassAgent`**`():`<br>`  memory = Memory()`<br> <br> **`def reflection`**`(llm, text)`<br>`     return text_output`<br> <br> **`def planning`**`(llm, text)`<br>`     return text_output`<br> <br>...<br>Memory<br>Knowledge DB<br>Skill manager<br>Planning<br>Self-reflection<br>Tools<br>Prompts<br>...|**llm.py**<br>**`def load_llm`**`(model):`<br>`  if model == “gpt”:`<br>`     return`**`GPTBase`**`()`<br>`  elif model == “claude”`<br>`     return`**`ClaudeBase`**`()`<br>`  else:`<br>`     return`**`LocalBase`**`()`<br>...|
|**agent.py**<br>**`ClassAgent`**`():`<br>`  memory = Memory()`<br> <br> **`def reflection`**`(llm, text)`<br>`     return text_output`<br> <br> **`def planning`**`(llm, text)`<br>`     return text_output`<br> <br>...<br>Memory<br>Knowledge DB<br>Skill manager<br>Planning<br>Self-reflection<br>Tools<br>Prompts<br>...|Planning|Planning|
|**agent.py**<br>**`ClassAgent`**`():`<br>`  memory = Memory()`<br> <br> **`def reflection`**`(llm, text)`<br>`     return text_output`<br> <br> **`def planning`**`(llm, text)`<br>`     return text_output`<br> <br>...<br>Memory<br>Knowledge DB<br>Skill manager<br>Planning<br>Self-reflection<br>Tools<br>Prompts<br>...|Self-reflection|Self-reflection|



Figure 2: Evaluation pipeline of Orak. Game scores are computed via eval.py by simply configuring game, LLM backbone, and agentic strategy. Orak supports two types of submissions: (1)
customizing llm.py with new backbone LLMs, and (2) customizing agent.py with new agentic
strategies. The agentic strategies are callable by LLMs via MCP interface in eval.py (in grey box).



Required LLM Capabilities



































(a) Street Fighter III (b) Super Mario (c) Ace Attorney (d) Her Story (e) Pokémon Red (f) Darkest Dungeon





















(g) Minecraft (h) Stardew Valley (i) StarCraft II (j) Slay the Spire (k) Baba Is You (l) 2048





















Figure 3: LLM capabilities required to play 12 games in Orak. The color theme (red, yellow, etc)
represents game genres. See Appendix A for genre categorization details.


3.1 G AME E NVIRONMENTS


**LLM Capabilities Required.** LLM agents require diverse capabilities to play games. Figure 3
summarizes the capability levels needed for each game in Orak, measured using principled criteria
adopted from the context of game design (Wu et al., 2023; Koster, 2013):


- **Rule Following (RF).** The level is measured by the extent to which adherence to rules is required
for gameplay (1: single rule, 2: fewer than 5 rules, 3: 5 or more rules).

- **Logical Reasoning (LR).** The number of LLM’s reasoning hops required to determine an in-game
action (1: 1 hop, 2: 1 to 3 hops, 3: 3 or more hops).

- **Spatial Reasoning (SR).** The level of spatial understanding required for gameplay (1: not necessary,
2: required in specific situations, 3: critical to core gameplay).

- **Long-text Understanding (LTU).** The extent of long-context comprehension required for gameplay
(1: a few lines, 2: a few paragraphs, 3: longer than one page with 500+ words).

- **Long-term Planning (LP).** The extent to which strategic planning is required (1: not necessary, 2:
planning for up to 3 sequential actions, 3: essential to plan more than 3 sequential actions).

- **Error Handling (EH).** The extent to which error correction is required during gameplay (1: not
necessary, 2: requires a one-step rollback, 3: requires multi-step rollback and re-planning).

- **Odds Handling (OH).** The extent to which understanding randomness is required for gameplay (1:
not necessary, 2: randomness exists in game, 3: randomness is critical to core gameplay).


The capability level is measured on a scale of 1 to 3 by 8 human participants, and the moderate
value is reported. Since most video games are designed to require various cognitive abilities even for
humans, they tend to require high levels of LLM capabilities in many dimensions. For example, action
games, _Street Fighter III_ and _Super Mario_ in red, require spatial reasoning and rule following, more
than long-context understanding and planning, while adventure games, _Ace Attorney_ and _Her Story_ in
yellow, emphasize long-text understanding and logical reasoning due to the need to comprehend long
storylines. More detailed analysis of required LLM capabilities for each game is in Appendix B.


**Game Description.** For each game, we provide a brief description of (1) the game state, (2) the
action space given to LLMs, and (3) the evaluation task and metric. More detailed explanations of
each environment are elaborated in Appendices C-N.


4


**(a) Street Fighter III** (Capcom, 1997) is a 2D side-scrolling fighting action game with 20 unique
characters, each with distinctive skills. (1) _Game state_ : The player character, opponent character,
remaining time, each player’s health, super-bar, stun-bar gauges, and the distance between the two
characters. (2) _Action space_ : 15-20 discrete actions: ‘move closer’, ‘low punch’, ‘high kick’, etc. (3)
_Evaluation task_ : Beating the game bot; performance is measured by the number of stages cleared.

**(b) Super Mario** (Christian Kauten, 2018) is a side-scrolling game where the player controls Mario
to avoid obstacles, defeat enemies, and reach the flag. (1) _Game state_ : The positions (x,y) and sizes of
obstacles and enemies extracted from the current game state. (2) _Action space_ : Mario keeps moving
to the right, and LLM decides the jump level, discretized in 6 bins. (3) _Evaluation task_ : Reaching out
to the final flag; performance is measured by the horizontal distance that Mario travels before dying.

**(c) Ace Attorney** (Capcom, 2001) is a courtroom adventure game where players act as defense
attorneys, gathering evidence and witnesses to prove their client’s innocence. (1) _Game state_ :
Dialogue history, collected evidence, court records profiles, etc. (2) _Action space_ : Player’s courtroom
actions: advancing dialogue, accessing court records, pressing witnesses, and presenting evidence.
(3) _Evaluation task_ : Performance is measured by response correctness and total steps taken.

**(d) Her Story** (Barlow, 2015) is an interactive adventure game where players explore police interview
clips to uncover a hidden truth. (1) _Game state_ : History of queries and search results with metadata
for the first 5 clips (visual description, date, viewing status, and transcript if played). (2) _Action space_ :
Searching for clips with keywords, or selecting a video to play. (3) _Evaluation task_ : Uncover the
truth; Performance is measured by the number of distinct video clips viewed to complete the game.

**(e) Pokemon Red** **´** (Game Freak, 1996) is a role-playing game where a player explores, collects
Pokemon, and battles other trainers to progress the storyline. (1) ´ _Game state_ : Player’s location,
party Pokemon (species, level, HP, status), inventory, battle state, and screen text. (2) ´ _Action space_ :
Choosing high-level tools or low-level joypad actions. (3) _Evaluation task_ : Defeat Brock, the first
gym leader; Progress measured by how many of 12 predefined storyline flags are triggered.

**(f) Darkest Dungeon** (Red Hook Studios, 2016) is a role-playing game where heroes explore
dungeons while managing stress and resources. (1) _Game state_ : Party status (character stats, health,
stress, and status effects), available skills, and enemy encounters. (2) _Action space_ : Combat actions
like ‘attack’, ‘heal’, and ‘swap’. (3) _Evaluation task_ : Complete the first expedition; Performance is
measured by the sum of the successful combats, the survived heroes, and their remaining stress.

**(g) Minecraft** (Mojang Studios, 2011) is an open-ended sandbox game where players explore a world,
gather resources, and survive by placing and breaking blocks. (1) _Game state_ : The player’s position,
inventory, health status, the nearby blocks and biome, etc. (2) _Action space_ : Executable JavaScript
code within the Mineflayer environment (contributors, 2013). (3) _Evaluation task_ : Crafting a target
item; performance is measured by whether the item is collected in the inventory.

**(h) Stardew Valley** (ConcernedApe, 2016) is an open-ended life simulation game where players
farm, fish, mine, and explore. (1) _Game state_ : Player’s location, energy, inventory, crop status, soil
status, date, and weather. (2) _Action space_ : Leaving the house, entering the house, sleeping, buying
seeds, tilling soil, watering, harvesting, and selling crops. (3) _Evaluation task_ : Earning the most
money by harvesting crops within the first 13 in-game days; performance is measured by total profit.

**(i) StarCraft II** (Blizzard Entertainment, 2010) is a real-time strategy game where players gather
resources, construct buildings, train units, and command armies to defeat opponents. (1) _Game state_ :
Resource levels, unit/building counts, production queues, research progress, and observed enemy
info. (2) _Action space_ : 72 discrete actions, including unit training, building, research, and strategic
operations. (3) _Evaluation task_ : Beating built-in AI bots; performance is measured by the win rate.

**(j) Slay the Spire** (MegaCrit, 2017) is a deck-building roguelike game where players ascend a
multi-floor tower, battling enemies and building decks. (1) _Game state_ : Player’s class, deck, hand,
health, relics, energy, enemies’ intents and statuses, and current floor. (2) _Action space_ : Playing a
card during combat, ending the turn, and selecting a card reward after combat. (3) _Evaluation task_ :
Defeating the final boss at the top floor; performance is measured by the number of floors reached.

**(k) Baba Is You** (Hempuli, 2019) is a puzzle game where a player manipulates the rules by moving
word tiles on a board. (1) _Game state_ : Coordinates of text and object tiles, and active rules. (2)
_Action space_ : A single movement ‘up’, ‘down’, ‘left’, and ‘right’, or a sequence of such moves. (3)
_Evaluation task_ : Solving the first stage; if the stage is not cleared, partial credit is awarded based on
sub-goals ( _e.g._, breaking the ‘Wall Is Stop’ rule).


5


**(l) 2048** (Cirulli, 2014) is a sliding tile puzzle game that aims to combine numbered tiles on a 4 _×_ 4
grid board to create a tile of the value 2048. (1) _Game state_ : The current configuration of the 4 _×_ 4 grid,
where each cell contains either a number (power of 2) or is empty. (2) _Action space_ : Four discrete
actions; ‘up’, ‘down’, ‘left’, and ‘right’. (3) _Evaluation task_ : Creating the 2048 tile; performance is
measured by the normalized progress toward creating the 2048 tile.


3.2 S UBMISSION G UIDELINE TO B ENCHMARK L EADERBOARD


**Models.** Participants can submit new pre-trained LLMs, VLMs, or their fine-tuned versions. Unless
otherwise specified, all models will be evaluated under the default agentic strategies for each game
specified in Section 5.1.

**Agentic Strategies.** Participants can also submit new agentic modules and strategies. All submitted
strategies should follow a consistent structure across games, _e.g._, by maintaining a fixed sequence
such as reasoning, planning, and using a specific tool.


4 F INE - TUNING : A LIGNING P RE - TRAINED LLM S INTO G AME A GENTS


**Data example from Reflection module** **Data example from Action module**



_X_ [ref]


_S_



Analyze Mario’s past action using state difference and
provide critiques for improving his action.
You should only respond in the format as below:
### Self-reflection
(Describe self-reflection here)


### Past Game State
Mario at (100,100), Bricks at (120, 100), (120, 150)
### Current Game State
Mario at (100,100), Bricks at (120, 100), (120, 150)



_X_ [act]


_S_



(Retrieve the self-reflection from memory)
Analyze the current game state, and decide the best action.
You should only respond in the format as below:
### Action
Jump Level: n (where n is an integer from 0 to 6)


### Game State
Mario at (100,100)
Position of all objects:

- Bricks at (120, 100), (120, 150) _. . ._



_Y_ [ref] ### Self-reflection _Y_ [act] ### Action
Mario is blocked by bricks. Jump higher to get past. Jump Level: 6.


Table 2: Fine-tuning data examples when playing _Supermario_ with ‘reflection’ agent.


We collect the fine-tuning dataset from expert LLMs, _e.g._, GPT-4o and o3-mini, playing all 12
games in Orak using several agentic modules. This dataset with environment interaction trajectories
encapsulates meta-knowledge on how to use the agentic strategies to solve diverse game genres.


**Data Format.** We denote LLMs’ gameplay _trajectory_ as _T_ = _{τ_ 1 _, . . ., τ_ _T_ _}_, where _T_ is the number
of game steps, and _τ_ _t_ denotes the sequence of LLM inferences executed by agentic strategies at
game step _t_ . Each LLM inference sequence _τ_ is represented as _τ_ = _{_ ( _X_ _[a]_ _[i]_ _, S, Y_ _[a]_ _[i]_ ) _}_ _[n]_ _i_ =1 [, where]
_a_ _i_ _∈{_ ‘reflection’ _,_ ‘planning’ _, . . .,_ ‘action’ _}_ is the _i_ -th agentic module in sequence, _X_ _[a]_ is the prompt
for agentic module _a_, _S_ is the game state, and _Y_ _[a]_ is the corresponding response of LLM. Table 2
shows detailed data examples of _τ_ .

**Data Selection.** For each game in Orak, we collect gameplay trajectories of expert LLMs, until we
have more than 1000 LLM inference sequence _τ_ in all _T_ collected. To ensure high-quality data, we
sort the collected _T_ in terms of the game score and select the trajectories with the highest game scores
until the number of selected _τ_ exceeds 300. All selected trajectories follow the ‘reflection-planningaction’ sequence, so that we have around 300 samples for each agent module. By performing data
selection on all 12 games, our fine-tuning set consists of approximately 11k samples.

**Data Augmentation.** To enhance the linguistic diversity, we augment each data sample _τ_ by
paraphrasing. We prompt GPT-4o to rephrase the game prompt _X_ _[a]_ while preserving all game-related
information, generating 10 augmented samples for each sample _τ_ . See Appendix O for prompting
details and the effect of the number of augmentations.


Our fine-tuning dataset is mainly for supervised fine-tuning (SFT). While dynamic data extraction
from the environment could enable reinforcement learning fine-tuning, we leave this for future work.


6


|Genre<br>Games|Action Adventure RPG Simulation Strategy Puzzle<br>SF3 SuperMario AceAttorney HerStory Poke´mon DarkestD Minecraft Stardew StarCraft2 SlaySpire BabaIsYou 2048|Avg<br>Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B<br>Llama3.3-70B<br>Qwen2.5-72B|0.0_±_0.0<br>18.7_±_8.6<br>1.3_±_2.2<br>2.1_±_1.2<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>6.7_±_11.5<br>0.0_±_0.1<br>13.3_±_5.8<br>31.8_±_10.1<br>4.6_±_1.3<br>4.2_±_1.1<br>0.0_±_0.0<br>47.5_±_39.2<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>20.0_±_0.0<br>0.3_±_0.2<br>20.0_±_0.0<br>23.4_±_14.1<br>20.0_±_17.4<br>1.2_±_1.1<br>0.0_±_0.0<br>44.8_±_22.2<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>13.3_±_11.5<br>0.1_±_0.1<br>16.7_±_11.5<br>27.2_±_9.6<br>9.3_±_0.2<br>8.5_±_2.0<br>0.0_±_0.0<br>88.8_±_2.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>5.0_±_0.0<br>20.0_±_0.0<br>0.6_±_0.4<br>16.7_±_11.5<br>24.4_±_6.0<br>35.7_±_4.5<br>4.6_±_2.3<br>0.0_±_0.0<br>0.0_±_0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>20.0_±_0.0<br>0.1_±_0.0<br>23.3_±_5.8<br>31.3_±_12.8<br>29.9_±_3.6<br>8.2_±_1.8<br>0.0_±_0.0<br>63.8_±_30.4<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>20.0_±_0.0<br>0.7_±_0.7<br>**33.3**_±_28.9<br>32.0_±_11.8<br>53.9_±_23.4<br>46.4_±_10.8<br>16.7_±_14.4<br>87.2_±_8.2<br>0.0_±_0.0<br>40.9_±_37.2<br>0.0_±_0.0<br>5.0_±_0.0<br>20.0_±_0.0<br>1.4_±_1.3<br>26.7_±_5.8<br>29.9_±_8.7<br>14.9_±_8.5<br>41.0_±_1.7<br>27.8_±_9.6<br>84.0_±_6.6<br>0.0_±_0.0<br>18.0_±_16.7<br>0.0_±_0.0<br>9.0_±_5.3<br>20.0_±_0.0<br>0.2_±_0.1|13.5<br>11.4<br>12.1<br>10.5<br>11.6<br>10.1<br>7.3<br>8.8|
|GPT-4o-mini<br>GPT-4o<br>GPT-5<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|16.7_±_11.5<br>28.8_±_8.8<br>28.4_±_2.8<br>21.2_±_5.6<br>0.0_±_0.0<br>81.3_±_5.8<br>46.0_±_7.0<br>16.1_±_27.8<br>75.0_±_50.0<br>3.3_±_2.9<br>13.3_±_11.5<br>1.1_±_1.0<br>29.7_±_14.3<br>34.1_±_14.2<br>85.3_±_1.5<br>64.2_±_5.2<br>38.9_±_9.6<br>93.4_±_1.5<br>71.0_±_7.0<br>81.4_±_4.8<br>**100.0**_±_0.0<br>23.6_±_22.1<br>20.0_±_0.0<br>5.6_±_1.5<br>19.5_±_11.0<br>31.6_±_10.5<br>59.1_±_26.5<br>**74.9**_±_1.7<br>**88.9**_±_4.8<br>92.9_±_0.7<br>73.0_±_7.0<br>**92.3**_±_8.6<br>25.0_±_50.0<br>26.2_±_19.4<br>**100.0**_±_0.0<br>10.2_±_2.1<br>**33.3**_±_15.3<br>34.9_±_14.6<br>**91.7**_±_1.5<br>66.5_±_3.6<br>0.0_±_0.0<br>89.0_±_2.1<br>**75.0**_±_0.0<br>55.1_±_16.0<br>25.0_±_50.0<br>15.0_±_0.0<br>73.3_±_46.2<br>**25.3**_±_7.3<br>13.3_±_11.5<br>**38.0**_±_14.4<br>55.7_±_3.4<br>67.5_±_3.3<br>83.3_±_0.0<br>**93.7**_±_1.6<br>**75.0**_±_0.0<br>59.2_±_10.1<br>**100.0**_±_0.0<br>**51.9**_±_31.9<br>73.3_±_46.2<br>5.1_±_2.5<br>16.7_±_11.5<br>31.7_±_8.2<br>81.9_±_1.6<br>62.9_±_2.6<br>63.9_±_19.2<br>89.9_±_2.5<br>**75.0**_±_0.0<br>53.6_±_20.9<br>50.0_±_57.7<br>15.0_±_0.0<br>46.7_±_46.2<br>5.3_±_2.7<br>20.0_±_0.0<br>28.7_±_13.2<br>83.3_±_1.5<br>67.2_±_3.9<br>75.0_±_0.0<br>91.7_±_1.1<br>41.7_±_0.0<br>66.1_±_11.5<br>50.0_±_57.7<br>24.9_±_17.1<br>20.0_±_0.0<br>11.5_±_3.4|9.2<br>3.6<br>3.6<br>4.0<br>**3.5**<br>5.1<br>5.1|
|Human (Novice)|20.0_±_20.0<br>100.0_±_0.0<br>87.8_±_2.6<br>72.6_±_2.8<br>86.1_±_12.7<br>90.3_±_2.0<br>70.8_±_0.0<br>69.8_±_19.9<br>33.3_±_57.7<br>52.9_±_23.2<br>100.0_±_0.0<br>22.7_±_10.4|-|


Table 3: Performance of LLMs on Orak with default agentic strategies. The best scores for each
game are highlighted in bold, and the average LLM rankings across all games are reported.


5 E XPERIMENT


5.1 E XPERIMENT S ETUP


**Models.** We validate the performance of 15 LLMs using states provided in text format. The
models include 8 open-source LLMs: LLaMA-3.2-1B/3B (Grattafiori et al., 2024), LLaMA-3.372B (Grattafiori et al., 2024), Qwen-2.5-3B/7B/72B (Yang et al., 2024), and Minitron-4B/8B (Sreenivas et al., 2024), and 7 proprietary LLMs: GPT-5/4o/4o-mini (Achiam et al., 2023), o3-mini,
Gemini-2.5-pro (Team et al., 2023), Claude-3.7-sonnet (Anthropic, 2025), and DeepSeek-R1 (Guo
et al., 2025). In addition, we study the effects of incorporating image inputs on 5 multi-modal LLMs:
Qwen2.5-vl-7B/32B (Bai et al., 2025), GPT-4o, Gemini-2.5-pro, and Claude-3.7-sonnet.


**Default Agentic Strategies.** For each game in Orak, we select the most effective agentic strategy
over GPT-4o as the default agent strategy. Specifically, For _Street Fighter III_, _HerStory_, _Darkest_
_Dungeon_, and _2048_, we use a ‘zero-shot’ action inference agent. For _Super Mario_, _Pokemon Red_ _´_,
_Stardew Valley_, _StarCraft II_, _Slay the Spire_, and _Baba Is You_, we use a ‘reflection-planning’ agent
that sequentially performs self-reflection, subtask planning, and action inference, integrated with
memory at each game step. For _AceAttorney_, we use a ‘reflection’ agent. For _Minecraft_, we use
a ‘skill-management’ agent that further includes knowledge retrieval and skill management in the
reflection-planning-action agent, following (Wang et al., 2023).


**Metrics and Implementation Details.** For each game, we report the normalization score rather
than the absolute score, _i.e._, the game score is normalized by the maximum game score. We report the
average score of 3 to 20 trials for each game. We also report the average score of 3 human novices.
More detailed metrics and LLM hyperparameter configurations can be found in Appendices C-N.


5.2 LLM G AMEPLAY P ERFORMANCE


Table 3 shows the gameplay performance of LLMs on Orak with default agentic strategies. Overall,
proprietary LLMs outperform open-source LLMs across all games in most cases. Gemini-2.5-pro
performs the best on average, ranking first in 5 out of 12 games, with the best average ranking of 3.5.
gpt-5/4o forms the second-best group with an average ranking of 3.6. GPT-5 shows superiority in
puzzle games, _i.e._, _Baba Is You_ and _2048_, which require strong mathematical and logical reasoning,
and spatial understanding abilities. Most small open-source LLMs, size under 8B, show almost
zero score on complex games, i.e., _Pokemon-red_ _´_, _Minecraft_, _Stardew Valley_, _StarCraft II_, and _Slay_
_the Spire_ . Mid-sized open-source models, Llama3.3-70B and Qwen2.5-72B, show advances in
moderately hard games, such as _Stardew Valley_ and _Slay the Spire_, but their performance remains far
below that of proprietary LLMs. See Appendices C-N for more detailed results on each game.


5.3 LLM A RENA


Among 12 games in Orak, _Street Fighter III_ and _StarCraft II_ support two-player competitive modes.
For _Street Fighter III_, we conduct pairwise battles among 8 LLMs with ‘zero-shot’ agent. Each pair


7


(a) _Street Fighter III_ Arena. (b) _StarCraft II_ Arena.
Figure 4: Match outcomes and Elo ratings for LLMs in two competitive environments.






|Agent<br>Models<br>Strategies|Action Adventure RPG Simulation Strategy Puzzle<br>SF3 SuperMario AceAttorney HerStory Poke´mon DarkestD Minecraft Stardew StarCraft2 SlaySpire BabaIsYou 2048|Avg<br>Rank|
|---|---|---|
|LLaMA-3B<br>Zeroshot<br>Refection<br>Planning<br>Ref-Plan|13.3_±_5.8<br>21.2_±_8.2<br>5.7_±_3.2<br>4.2_±_1.1<br>0.0_±_0.0<br>47.5_±_39.2<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>**20.0**_±_0.0<br>0.3_±_0.2<br>**30.0**_±_17.3<br>32.4_±_8.6<br>4.6_±_1.3<br>4.4_±_1.3<br>0.0_±_0.0<br>47.3_±_39.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>**20.0**_±_0.0<br>0.0_±_0.0<br>20.0_±_0.0<br>27.0_±_8.4<br>4.6_±_1.3<br>5.2_±_1.0<br>0.0_±_0.0<br>56.3_±_23.6<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>**20.0**_±_0.0<br>0.1_±_0.1<br>16.7_±_20.8<br>31.8_±_10.1<br>3.8_±_0.0<br>5.4_±_0.4<br>0.0_±_0.0<br>57.0_±_31.6<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>**20.0**_±_0.0<br>0.1_±_0.2|6.4<br>5.6<br>6.2<br>6.1|
|GPT-4o<br>Zeroshot<br>Refection<br>Planning<br>Ref-Plan|29.7_±_14.3<br>29.6_±_9.2<br>49.9_±_1.3<br>**64.2**_±_5.2<br>33.3_±_0.0<br>**93.4**_±_1.5<br>0.0_±_0.0<br>34.5_±_29.9<br>50.0_±_57.7<br>24.7_±_9.2<br>**20.0**_±_0.0<br>5.6_±_1.5<br>23.3_±_20.8<br>32.3_±_15.5<br>**85.3**_±_1.5<br>61.5_±_0.4<br>36.1_±_4.8<br>85.2_±_10.3<br>**50.0**_±_0.0<br>15.6_±_4.5<br>0.0_±_0.0<br>**41.3**_±_19.6<br>**20.0**_±_0.0<br>3.5_±_2.9<br>**30.0**_±_26.5<br>29.4_±_12.5<br>52.7_±_0.5<br>59.4_±_5.7<br>33.3_±_0.0<br>82.0_±_8.6<br>13.0_±_0.0<br>54.9_±_20.2<br>50.0_±_57.7<br>35.3_±_9.2<br>**20.0**_±_0.0<br>6.0_±_5.5<br>23.3_±_20.8<br>**34.1**_±_14.2<br>52.8_±_0.5<br>62.0_±_4.9<br>**38.9**_±_9.6<br>91.6_±_2.5<br>**50.0**_±_0.0<br>**81.4**_±_4.8<br>**100.0**_±_0.0<br>36.0_±_25.5<br>**20.0**_±_0.0<br>**7.0**_±_5.7|3.3<br>3.0<br>3.1<br>**2.2**|



Table 4: Ablation study for agentic modules. ‘Ref-Plan’ refers to the ‘Reflection-Planning’ agent.


competed in three rounds, and the agent winning 2 out of 3 rounds was declared the winner. To ensure
a fair comparison, both agents were assigned the same character, Ken, in all matches. Figure 4(a)
shows the relative win rates and Elo ratings. Interestingly, different from the result in Section 5.2,
Minitron-8B consistently outperforms all other LLMs and shows the best Elo rating. This may imply
that when multiple agents are involved in the environment, adversarial actions can change the game
dynamics. For _StarCraft II_, we conduct pairwise battles among 7 LLMs, with each pair competing in
a single round. Both agents were assigned the same race, Protoss, in all matches. As in Figure 4(b),
Claude-3.7-Sonnet shows the best Elo rating, while GPT-4o and Minitron-8B form the second group.


5.4 A BLATION S TUDY FOR A GENTIC M ODULES


Table 4 shows the ablation results of LLaMA-3.2-3B and GPT-4o across 4 agent strategies. Interestingly, the impact of adding agentic modules to gameplay performance _differs_ between the two
LLMs. For GPT-4o, the inclusion of agentic modules consistently improves gameplay performance;
‘reflection-planning’ agent achieves the best average ranking of 2.2, followed by ‘reflection’ and
‘planning’ agents with rankings of 3.1 and 3.3, and ‘zero-shot’ agent with the lowest ranking of 3.4.
However, LLaMA-3.2-3B does not follow this trend. The ‘reflection’ agent shows the highest average
ranking of 5.6, while ‘reflection-planning’ follows with 6.1, although it adds the planning module.
This indicates that, for relatively smaller LLMs like LLaMA-3.2-3B, adding agentic modules may
increase the complexity of the prompt, hindering their decision-making accuracy. These results
suggest that the optimal agentic strategy may depend on the inherent capability of the LLM.


5.5 E FFECT OF V ISUAL I NPUT


**Setup.** To study the effect of visual input, we divide games into two groups: Group 1 (Table 5)
includes games where the provided textual game state can entirely be derived from a visual screenshot.
Group 2 (Table 6) comprises games where the textual state contains information beyond what is
visible in the current frame (e.g., abstracted inventory lists or off-screen character/item details); for
this group, we exclude evaluation on _Image-only_ input types for fairness. _Minecraft_ was excluded
since the environment does not provide the visionary view of a bot that LLM plays.


**Result.** As shown in Table 5, relying solely on _Image-only_ input led to a substantial drop in
performance. This was consistently reflected across all models, with average ranks deteriorating
significantly compared to _Text-only_ input. In contrast, as shown in Table 5& 6, utilizing _Both_ text and
visual inputs produced mixed effects on game scores and model ranks. For instance, in games like
_Street Fighter III_ (Group 1), since on-screen visual details are challenging to fully convey textually,
adding visual context significantly benefited Claude, increasing its score by 16 _._ 6 . Conversely, in
narrative-heavy games such as _Ace Attorney_ (Group 2), the same approach often proved detrimental;
GPT-4o’s score, for example, dropped by 31 _._ 8, and its average rank in that group fell from 2.9


8


|Models Input|SF3 SuperMario Stardew BabaIsYou 2048|Rank|
|---|---|---|
|Qwen2.5-7B<br>Text<br>Image<br>Both|0.0_±_0.0<br>**26.0**_±_8.2<br>**0.0**_±_0.0<br>**13.3**_±_11.5<br>0.1_±_0.1<br>**3.3**_±_5.8<br>25.1_±_10.1<br>**0.0**_±_0.0<br>0.0_±_0.0<br>0.2_±_0.3<br>**3.3**_±_5.8<br>25.6_±_8.0<br>**0.0**_±_0.0<br>0.0_±_0.0<br>**0.4**_±_0.5|12.8<br>13.5<br>**12.7**|
|Qwen2.5-32B<br>Text<br>Image<br>Both|16.7_±_5.8<br>**32.0**_±_10.2<br>15.2_±_22.7<br>**20.0**_±_0.0<br>0.2_±_0.3<br>**33.3**_±_20.8<br>25.8_±_10.7<br>0.0_ ±_0.0<br>13.3_±_11.5<br>**0.4**_±_0.3<br>**33.3**_±_15.3<br>29.7_±_6.6<br>**26.9**_±_13.9<br>**20.0**_±_0.0<br>0.2_±_0.3|4.3<br>5.1<br>**3.4**|
|GPT-4o<br>Text<br>Image<br>Both|**29.7**_±_14.3<br>**34.1**_±_14.1<br>**81.4**_±_4.8<br>**20.0**_±_0.0<br>**5.6**_±_1.5<br>23.7_±_15.9<br>27.1_±_13.7<br>0.0_ ±_0.0<br>6.7_±_11.5<br>1.8_±_1.1<br>24.3_±_14.5<br>27.1_±_10.2<br>41.9_±_22.1<br>20.0_±_0.0<br>5.4_±_4.5|**1.7**<br>5.3<br>3.0|
|Gemini-2.5<br>Text<br>Image<br>Both|13.3_±_11.5<br>38.0_±_13.4<br>59.2_±_10.1<br>73.3_±_46.2<br>5.1_±_2.5<br>16.7_±_11.5<br>28.5_±_10.7<br>7.6_±_9.0<br>20.0_±_0.0<br>**5.5**_±_2.4<br>**20.0**_±_10.0<br>**40.9**_±_9.6<br>**60.0**_±_6.0<br>**86.7**_±_23.1<br>3.1_±_2.6|5.2<br>7.4<br>**4.0**|
|Claude-3.7<br>Text<br>Image<br>Both|16.7_±_11.5<br>**28.7**_±_13.2<br>**53.6**_±_20.9<br>**46.7**_±_46.2<br>5.3_±_2.7<br>23.3_±_11.5<br>25.6_±_6.4<br>0.0_±_0.0<br>20.0_±_0.0<br>**8.4**_±_4.0<br>**33.3**_±_5.8<br>22.6_±_6.3<br>49.8_±_1.0<br>20.0_±_0.0<br>6.7_±_0.9|**5.8**<br>8.0<br>6.2|


Table 5: Modality Comparison (Group 1).



|Models Input|AceAttorney HerStory Poke´mon DarkestD StarCraft2 SlaySpire|Rank|
|---|---|---|
|Qwen2.5-7B<br>Text<br>Both|10.0_±_0.0<br>**3.2**_±_1.5<br>**2.8**_±_4.8<br>**82.7**_±_1.5<br>**0.0**_±_0.0<br>**0.0**_±_0.0<br>**17.6**_±_13.1<br>2.5_±_0.8<br>**2.8**_±_4.8<br>81.8_±_3.0<br>**0.0**_±_0.0<br>**0.0**_±_0.0|**9.1**<br>9.3|
|Qwen2.5-32B<br>Text<br>Both|**71.9**_±_21.5<br>15.4_±_2.8<br>**27.8**_±_9.6<br>89.9_±_1.5<br>**0.0**_±_0.0<br>**0.0**_±_0.0<br>68.6_±_10.0<br>**17.0**_±_4.6<br>25.0_±_14.4<br>**91.0**_±_3.0<br>**0.0**_±_0.0<br>**0.0**_±_0.0|7.1<br>**7.0**|
|GPT-4o<br>Text<br>Both|**85.3**_±_1.5<br>**64.2**_±_5.2<br>38.9_±_9.6<br>**93.4**_±_1.5<br>**100.0**_±_0.0<br>**23.6**_±_22.1<br>53.5_±_1.7<br>40.6_±_29.5<br>**41.7**_±_8.3<br>92.2_±_3.0<br>50.0_±_57.7<br>**23.6**_±_22.1|**2.9**<br>5.0|
|Gemini-2.5<br>Text<br>Both|**55.7**_±_3.4<br>**67.5**_±_3.3<br>**83.3**_±_0.0<br>**93.7**_±_1.6<br>**100.0**_±_0.0<br>**51.9**_±_31.9<br>52.6_±_0.8<br>64.9_±_2.4<br>**83.3**_±_0.0<br>92.2_±_1.8<br>**100.0**_±_0.0<br>26.2_±_19.4|**2.1**<br>3.2|
|Claude-3.7<br>Text<br>Both|**81.9**_±_1.6<br>62.9_±_2.6<br>63.9_±_19.2<br>89.9_±_2.5<br>**50.0**_±_57.7<br>**15.0**_±_0.0<br>71.3_±_17.3<br>**63.6**_±_3.1<br>**72.2**_±_4.7<br>**90.1**_±_5.7<br>**50.0**_±_57.7<br>9.7_±_4.6|4.8<br>**4.3**|


Table 6: Modality Comparison (Group 2).



|Intra-Game OOD-Game Non-Game<br>Models Finetune<br>SF3 DarkestD StarCraft2 SlaySpire BabaIsYou SuperMario 2048 Math500 WebShop-E WebShop-H|Col2|Col3|Col4|
|---|---|---|---|
|Llama-3.2-1B<br>✗<br>✓|0.0_±_0.0<br>0.0_±_0.0<br>**0.0**_±_0.0<br>0.0_±_0.0<br>**20.0**_±_0.0<br>**42.0**_±_16.4<br>**93.4**_±_2.6<br>**0.0**_±_0.0<br>**8.0**_±_3.5<br>**20.0**_±_0.0|18.7_±_8.6<br>0.1_±_0.1<br>**26.7**_±_12.3<br>**2.8**_±_1.8|24.1_±_1.6<br>**2.7**_±_0.5<br>**1.9**_±_0.8<br>**25.6**_±_1.7<br>0.5_±_0.0<br>0.0_±_0.0|
|Llama-3.2-3B<br>✗<br>✓|12.0_±_11.0<br>87.2_±_9.5<br>**0.0**_±_0.0<br>0.0_±_0.0<br>**20.0**_±_0.0<br>**40.0**_±_7.1<br>**92.0**_±_0.2<br>**0.0**_±_0.0<br>**10.7**_±_1.2<br>**20.0**_±_0.0|31.8_±_10.1<br>0.1_±_0.2<br>**34.4**_±_7.0<br>**3.1**_±_2.5|29.6_±_1.8<br>0.0_±_0.0<br>0.0_±_0.0<br>**36.1**_±_0.9<br>**8.4**_±_0.3<br>**12.6**_±_0.8|


Table 7: Generalization performance of LLMs fine-tuned on expert gameplay trajectories from Orak.


( _Text-only_ ) to 5.0. This highlights that the impact of combining modalities varies considerably, with
some scenarios showing improved ranks or scores while others demonstrated a decline.


5.6 E FFECT OF F INE - TUNING


**Setup.** To study the effect of fine-tuning, we consider three types of generalization: _Intra-game_,
_OOD-game_, and _Non-game_ . Intra-game generalization evaluates whether an LLM can adapt to _unseen_
_scenarios_ within the same game, _e.g._, new stages or characters. OOD-game generalization evaluates
whether fine-tuning on a specific set of games enables the model to act better on _unseen games_ .
Non-game generalization evaluates whether our fine-tuning set with agent gameplay trajectory helps
the model to perform better on non-game tasks like math or web navigation. For Intra-game and Nongame generalizations, we fine-tune LLMs on all 12 games, while for OOD-game generalization, we
split 12 games in to 10 training games and 2 test games, i.e., _Super Mario_ and _2048_ . See Appendix P
for detailed fine-tuning configurations and unseen scenario details in intra-game generalization.


**Intra-game Generalization.** As shown in Table 7, fine-tuned Llama-3.2-1B/3B show better generalization to unseen scenarios than the pretrained ones; in 3 out of 5 games, both fine-tuned models
outperform their pretrained counterparts. The performance gain largely comes from the model learning to generate valid actions more reliably after fine-tuning, especially in environments where the
pretrained model frequently failed to act meaningfully. However, this approach appears insufficient to
significantly enhance the spatial reasoning abilities of smaller models. This is evident in _Baba Is You_,
where fine-tuned models struggle to construct the winning condition required to score above 20.0.


**OOD-game Generalization.** Similarly, despite being trained exclusively on trajectories from
different games, fine-tuned models perform significantly better on OOD games like _Super Mario_
and _2048_ . This suggests that fine-tuning on trajectories shaped by reflection and planning enables
models to learn transferable decision-making routines, as the underlying capabilities required for
these behaviors are shared across games. Specifically, the improvement in _2048_ likely benefits from
its structural similarity to _Baba Is You_, a training game that also uses 2D grid layout and discrete move
actions (up, down, left, right). More fine-tuning analysis with varying OOD gaps are in Appendix Q.


**Non-game Generalization.** More interestingly, LLMs fine-tuned on our gameplay trajectories
sometimes show improved performance in non-game tasks like Math500 and WebShop (Yao et al.,
2022). In Table 7, LLaMA-3.2-3B consistently improves on both Math500 and Webshop. In particular,
on WebShop-E (easy) and -H (hard), it shows a dramatic gain from 0.0 % to 8.4 % or 12.6 %, indicating
our fine-tuning set is more effective for agentic tasks that require decision-making abilities similar
to gameplay. In contrast, the smaller model, Llama-3.2-1B, shows no observable generalization to
non-game tasks, which suggests that the extent of generalization may depend on model capacity.


9


6 D ISCUSSION


**Conclusion.** In this paper, we introduce Orak, a benchmark designed to train and evaluate LLM
agents across diverse video games. Orak enables comprehensive assessments of LLM capabilities
required to play most game genres. Through a plug-and-play interface powered by MCP, it allows
consistent evaluation of rapidly evolving LLMs over various agentic modules. In addition, we release
a fine-tuning dataset of game interaction trajectories of top-performing LLMs, which can effectively
transform pre-trained LLMs into gaming agents. With the comprehensive game set and user-friendly
interface, Orak sets a new foundation for game-based LLM evaluation, driving progress towards
versatile and high-performing gaming agents.


**Limitations.** We note that Orak provides environments favorable for LLM reasoning and decisionmaking by pre-processing game states into structured text where information unnecessary to gameplay
is hidden. This may offer insights for providers seeking to deploy resource-efficient LLMs on games.
We leave a complementary direction, providing the full in-game states with rich uncurated texts to
LLMs, for future work. Further discussions, including cost and licensing, are provided in Appendix R.


R EFERENCES


Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman,
Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report.
_arXiv preprint arXiv:2303.08774_, 2023.


Anthropic. Claude 3.7 sonnet: Our most capable model yet. [https://www.anthropic.com/](https://www.anthropic.com/news/claude-3-7-sonnet)
[news/claude-3-7-sonnet, 2025. Accessed: 2025-09-08.](https://www.anthropic.com/news/claude-3-7-sonnet)


Baekalfen. Pyboy: Game boy emulator written in python. [https://github.com/Baekalfen/](https://github.com/Baekalfen/PyBoy)
[PyBoy. Accessed: 2025-09-23.](https://github.com/Baekalfen/PyBoy)


Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang,
Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_,
2025.


[Sam Barlow. Her Story. https://www.herstorygame.com, 2015. Accessed: 2025-09-22.](https://www.herstorygame.com)


Blizzard Entertainment. StarCraft II. [https://starcraft2.com](https://starcraft2.com), 2010. Accessed: 2025-09-22.


Ralph Allan Bradley and Milton E. Terry. Rank analysis of incomplete block designs: I. the method
of paired comparisons. _Biometrika_, 39(3-4):324–345, 1952. doi: 10.2307/2334029.


Bug Kiooeht. BaseMod. [https://steamcommunity.com/sharedfiles/](https://steamcommunity.com/sharedfiles/filedetails/?id=1605833019)
[filedetails/?id=1605833019, 2018a. Accessed: 2025-09-22.](https://steamcommunity.com/sharedfiles/filedetails/?id=1605833019)


Bug Kiooeht. Mod the Spire. [https://steamcommunity.com/sharedfiles/](https://steamcommunity.com/sharedfiles/filedetails/?id=1605060445)
[filedetails/?id=1605060445, 2018b. Accessed: 2025-09-22.](https://steamcommunity.com/sharedfiles/filedetails/?id=1605060445)


BurnySc2. Starcraft II Bot API Client Library for Python 3. [https://github.com/](https://github.com/BurnySc2/python-sc2)
[BurnySc2/python-sc2, 2017. Accessed: 2025-09-21.](https://github.com/BurnySc2/python-sc2)


Capcom. Street Fighter III: 3rd Strike. [https://streetfighter.fandom.com/wiki/](https://streetfighter.fandom.com/wiki/Street_Fighter_III:_3rd_Strike)
[Street_Fighter_III:_3rd_Strike, 1997. Accessed: 2025-09-22.](https://streetfighter.fandom.com/wiki/Street_Fighter_III:_3rd_Strike)


Capcom. Phoenix Wright: Ace Attorney. [https://aceattorney.fandom.com/wiki/](https://aceattorney.fandom.com/wiki/Phoenix_Wright:_Ace_Attorney)
[Phoenix_Wright:_Ace_Attorney, 2001. Accessed: 2025-09-22.](https://aceattorney.fandom.com/wiki/Phoenix_Wright:_Ace_Attorney)


Baian Chen, Chang Shu, Ehsan Shareghi, Nigel Collier, Karthik Narasimhan, and Shunyu Yao.
Fireact: Toward language agent fine-tuning. _arXiv preprint arXiv:2310.05915_, 2023.


Kevin Chen, Marco Cusumano-Towner, Brody Huval, Aleksei Petrenko, Jackson Hamburger, Vladlen
Koltun, and Philipp Krahenb ¨ uhl. Reinforcement learning for long-horizon interactive llm agents. ¨
_arXiv preprint arXiv:2502.01600_, 2025.


10


Zehui Chen, Kuikun Liu, Qiuchen Wang, Wenwei Zhang, Jiangning Liu, Dahua Lin, Kai Chen, and
Feng Zhao. Agent-flan: Designing data and methods of effective agent tuning for large language
models. _arXiv preprint arXiv:2403.12881_, 2024.


Christian Kauten. Super Mario Bros for OpenAI Gym. [https://github.com/Kautenja/](https://github.com/Kautenja/gym-super-mario-bros)
[gym-super-mario-bros, 2018. Accessed: 2025-09-22.](https://github.com/Kautenja/gym-super-mario-bros)


Yunfei Chu, Jin Xu, Xiaohuan Zhou, Qian Yang, Shiliang Zhang, Zhijie Yan, Chang Zhou, and
Jingren Zhou. Qwen-audio: Advancing universal audio understanding via unified large-scale
audio-language models. _arXiv preprint arXiv:2311.07919_, 2023.


[Gabriele Cirulli. 2048. https://play2048.co/, 2014. Accessed: 2025-09-22.](https://play2048.co/)


ConcernedApe. Stardew Valley. [https://www.stardewvalley.net](https://www.stardewvalley.net), 2016. Accessed: 202509-22.


BepInEx Contributors. Bepinex: Unity / xna game patcher and plugin framework. [https://](https://github.com/BepInEx/BepInEx)
[github.com/BepInEx/BepInEx, 2025a. Accessed: 2025-09-21.](https://github.com/BepInEx/BepInEx)


PrismarineJS contributors. PrismarineJS/mineflayer: Create Minecraft bots with a powerful, stable,
and high-level JavaScript API. [https://github.com/PrismarineJS/mineflayer](https://github.com/PrismarineJS/mineflayer),
2013. Accessed: 2025-09-22.


Unity Doorstop Contributors. Unity doorstop: A tool to execute managed .net assemblies inside unity.

[https://github.com/NeighTools/UnityDoorstop, 2025b. Accessed: 2025-09-21.](https://github.com/NeighTools/UnityDoorstop)


Anthony Costarelli, Mat Allen, Roman Hauksson, Grace Sodunke, Suhas Hariharan, Carlson Cheng,
Wenjie Li, Joshua Clymer, and Arjun Yadav. Gamebench: Evaluating strategic reasoning abilities
of llm agents. _arXiv preprint arXiv:2406.06613_, 2024.


Wenqian Cui, Dianzhi Yu, Xiaoqi Jiao, Ziqiao Meng, Guangyan Zhang, Qichao Wang, Yiwen
Guo, and Irwin King. Recent advances in speech language models: A survey. _arXiv preprint_
_arXiv:2410.03751_, 2024.


DIAMBRA. DIAMBRA: Reinforcement Learning Platform for Competitive Video Games. [https:](https://www.diambra.ai/)
[//www.diambra.ai/, 2025. Accessed: 2025-09-22.](https://www.diambra.ai/)


Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew Tang,
De-An Huang, Yuke Zhu, and Anima Anandkumar. Minedojo: Building open-ended embodied
agents with internet-scale knowledge. _Advances in Neural Information Processing Systems_, 35:
18343–18362, 2022.


Peiyuan Feng, Yichen He, Guanhua Huang, Yuan Lin, Hanchong Zhang, Yuchen Zhang, and Hang Li.
Agile: A novel reinforcement learning framework of llm agents. _arXiv preprint arXiv:2405.14751_,
2024.


Xidong Feng, Yicheng Luo, Ziyan Wang, Hongrui Tang, Mengyue Yang, Kun Shao, David Mguni,
Yali Du, and Jun Wang. Chessgpt: Bridging policy learning and language modeling. _Advances in_
_Neural Information Processing Systems_, 36:7216–7262, 2023.


Forgotten Arbiter. Communication Mod. [https://github.com/ForgottenArbiter/](https://github.com/ForgottenArbiter/CommunicationMod)
[CommunicationMod, 2019. Accessed: 2025-09-22.](https://github.com/ForgottenArbiter/CommunicationMod)


Game Freak. Pokemon Red Version. ´ [https://pokemon.fandom.com/wiki/Pok%C3%](https://pokemon.fandom.com/wiki/Pok%C3%A9mon_Red_and_Blue_Versions)
[A9mon_Red_and_Blue_Versions, 1996. Accessed: 2025-09-22.](https://pokemon.fandom.com/wiki/Pok%C3%A9mon_Red_and_Blue_Versions)


Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad
Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The llama 3 herd of
models. _arXiv preprint arXiv:2407.21783_, 2024.


Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms
via reinforcement learning. _arXiv preprint arXiv:2501.12948_, 2025.


11


Danijar Hafner. Benchmarking the spectrum of agent capabilities. _arXiv preprint arXiv:2109.06780_,
2021.


Matthew Hausknecht, Prithviraj Ammanabrolu, Marc-Alexandre Cot ˆ e, and Xingdi Yuan. Interac- ´
tive fiction games: A colossal adventure. In _Proceedings of the AAAI Conference on Artificial_
_Intelligence_, volume 34, pp. 7903–7910, 2020.


[Hempuli. Baba is you. https://hempuli.com/baba/, 2019. Accessed: 2025-09-22.](https://hempuli.com/baba/)


Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin
Burns, Samir Puranik, Horace He, Dawn Song, et al. Measuring coding challenge competence
with apps. _arXiv preprint arXiv:2105.09938_, 2021.


Xinyi Hou, Yanjie Zhao, Shenao Wang, and Haoyu Wang. Model context protocol (mcp): Landscape,
security threats, and future research directions. _arXiv preprint arXiv:2503.23278_, 2025.


Lanxiang Hu, Qiyu Li, Anze Xie, Nan Jiang, Ion Stoica, Haojian Jin, and Hao Zhang. Gamearena:
Evaluating llm reasoning through live computer games. _arXiv preprint arXiv:2412.06394_, 2024a.


Lanxiang Hu, Mingjia Huo, Yuxuan Zhang, Haoyang Yu, Eric P Xing, Ion Stoica, Tajana Rosing,
Haojian Jin, and Hao Zhang. lmgame-bench: How good are llms at playing games? _arXiv preprint_
_arXiv:2505.15146_, 2025.


Sihao Hu, Tiansheng Huang, Fatih Ilhan, Selim Tekin, Gaowen Liu, Ramana Kompella, and Ling Liu.
A survey on large language model-based game agents. _arXiv preprint arXiv:2404.02039_, 2024b.


Sihao Hu, Tiansheng Huang, and Ling Liu. Pokellmon: A human-parity agent for pok ´ emon battles ´
with large language models. _arXiv preprint arXiv:2402.01118_, 2024c.


Jen-tse Huang, Eric John Li, Man Ho Lam, Tian Liang, Wenxuan Wang, Youliang Yuan, Wenxiang
Jiao, Xing Wang, Zhaopeng Tu, and Michael R Lyu. How far are we on the decision-making of llms?
evaluating llms’ gaming ability in multi-agent environments. _arXiv preprint arXiv:2403.11807_,
2024.


Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zero-shot
planners: Extracting actionable knowledge for embodied agents. In _International conference on_
_machine learning_, pp. 9118–9147. PMLR, 2022a.


Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan
Tompson, Igor Mordatch, Yevgen Chebotar, et al. Inner monologue: Embodied reasoning through
planning with language models. _arXiv preprint arXiv:2207.05608_, 2022b.


Christian Kauten. Super Mario Bros for OpenAI Gym. [https://github.com/Kautenja/](https://github.com/Kautenja/gym-super-mario-bros)
[gym-super-mario-bros, 2018. Accessed: 2025-09-21.](https://github.com/Kautenja/gym-super-mario-bros)


Kgleken. Darkestdungeonbot. [https://github.com/kgleken/DarkestDungeonBot](https://github.com/kgleken/DarkestDungeonBot),
2023. Accessed: 2025-09-21.


Rahima Khanam and Muhammad Hussain. Yolov11: An overview of the key architectural enhancements. _arXiv preprint arXiv:2410.17725_, 2024.


Raph Koster. _Theory of fun for game design_ . ” O’Reilly Media, Inc.”, 2013.


Heinrich Kuttler, Nantas Nardelli, Alexander Miller, Roberta Raileanu, Marco Selvatici, Edward ¨
Grefenstette, and Tim Rocktaschel. The nethack learning environment. ¨ _Advances in Neural_
_Information Processing Systems_, 33:7671–7684, 2020.


Ido Levy, Ben Wiesel, Sami Marreed, Alon Oved, Avi Yaeli, and Segev Shlomov. Stwebagentbench: A benchmark for evaluating safety and trustworthiness in web agents. _arXiv_
_preprint arXiv:2410.06703_, 2024.


Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding,
Kaiwen Men, Kejuan Yang, et al. Agentbench: Evaluating llms as agents. _arXiv preprint_
_arXiv:2308.03688_, 2023.


12


Weiyu Ma, Qirui Mi, Yongcheng Zeng, Xue Yan, Runji Lin, Yuqiao Wu, Jun Wang, and Haifeng
Zhang. Large language models play starcraft ii: Benchmarks and a chain of summarization
approach. _Advances in Neural Information Processing Systems_, 37:133386–133442, 2024.


[MegaCrit. Slay the Spire. https://www.megacrit.com, 2017. Accessed: 2025-09-22.](https://www.megacrit.com)


[Mojang Studios. Minecraft. https://www.minecraft.net, 2011. Accessed: 2025-09-22.](https://www.minecraft.net)


Peter Muhlbacher, Nikos I Bosse, and Lawrence Phillips. Towards a realistic long-term benchmark ¨
for open-web research agents. _arXiv preprint arXiv:2409.14913_, 2024.


NVIDIA. Introducing nvidia ace for games - spark life into virtual characters
with generative ai. [https://www.nvidia.com/en-us/geforce/news/](https://www.nvidia.com/en-us/geforce/news/nvidia-ace-for-games-generative-ai-npcs/)
[nvidia-ace-for-games-generative-ai-npcs/, 2025. Accessed: 2025-09-22.](https://www.nvidia.com/en-us/geforce/news/nvidia-ace-for-games-generative-ai-npcs/)


Davide Paglieri, Bartłomiej Cupiał, Samuel Coward, Ulyana Piterbarg, Maciej Wolczyk, Akbir Khan,
Eduardo Pignatelli, Ł ukasz Kucinski, Lerrel Pinto, Rob Fergus, et al. Balrog: Benchmarking ´
agentic llm and vlm reasoning on games. _arXiv preprint arXiv:2411.13543_, 2024.


Yichen Pan, Dehan Kong, Sida Zhou, Cheng Cui, Yifei Leng, Bing Jiang, Hangyu Liu, Yanyi
Shang, Shuyan Zhou, Tongshuang Wu, et al. Webcanvas: Benchmarking web agents in online
environments. _arXiv preprint arXiv:2406.12373_, 2024.


Andreas Pardeike. Harmony: A library for patching, replacing and decorating .net and mono
methods during runtime. [https://github.com/pardeike/Harmony](https://github.com/pardeike/Harmony), 2025. Accessed:
2025-09-21.


Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S
Bernstein. Generative agents: Interactive simulacra of human behavior. In _Proceedings of the 36th_
_annual acm symposium on user interface software and technology_, pp. 1–22, 2023.


Pathoschild. SMAPI - Stardew Modding API. [https://smapi.io/](https://smapi.io/), 2025. Accessed: 2025-0922.


Archiki Prasad, Alexander Koller, Mareike Hartmann, Peter Clark, Ashish Sabharwal, Mohit Bansal,
and Tushar Khot. Adapt: As-needed decomposition and planning with language models. _arXiv_
_preprint arXiv:2311.05772_, 2023.


Pranav Putta, Edmund Mills, Naman Garg, Sumeet Motwani, Chelsea Finn, Divyansh Garg, and
Rafael Rafailov. Agent q: Advanced reasoning and learning for autonomous ai agents. _arXiv_
_preprint arXiv:2408.07199_, 2024.


Siyuan Qi, Shuo Chen, Yexin Li, Xiangyu Kong, Junqi Wang, Bangcheng Yang, Pring Wong, Yifan
Zhong, Xiaoyuan Zhang, Zhaowei Zhang, et al. Civrealm: A learning and reasoning odyssey in
civilization for decision-making agents. _arXiv preprint arXiv:2401.10568_, 2024.


Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea
Finn. Direct preference optimization: Your language model is secretly a reward model. _Advances_
_in Neural Information Processing Systems_, 36:53728–53741, 2023.


Red Hook Studios. Darkest Dungeon. [https://www.darkestdungeon.com](https://www.darkestdungeon.com), 2016. Accessed:
2025-09-22.


Robojumper. Darkest dungeon save editor. [https://github.com/robojumper/](https://github.com/robojumper/DarkestDungeonSaveEditor)
[DarkestDungeonSaveEditor, 2023. Accessed: 2025-09-21.](https://github.com/robojumper/DarkestDungeonSaveEditor)


Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical
reasoning in open language models. _arXiv preprint arXiv:2402.03300_, 2024.


Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. Reflexion:
Language agents with verbal reinforcement learning. _Advances in Neural Information Processing_
_Systems_, 36:8634–8652, 2023.


13


Sharath Turuvekere Sreenivas, Saurav Muralidharan, Raviraj Joshi, Marcin Chochowski, Ameya Sunil
Mahabaleshwarkar, Gerald Shen, Jiaqi Zeng, Zijia Chen, Yoshi Suhara, Shizhe Diao, et al. Llm
pruning and distillation in practice: The minitron approach. _arXiv preprint arXiv:2408.11796_,
2024.


Weihao Tan, Wentao Zhang, Xinrun Xu, Haochong Xia, Ziluo Ding, Boyu Li, Bohan Zhou, Junpeng
Yue, Jiechuan Jiang, Yewen Li, et al. Cradle: Empowering foundation agents towards general
computer control. _arXiv preprint arXiv:2403.03186_, 2024.


Wenjie Tang, Yuan Zhou, Erqiang Xu, Keyan Cheng, Minne Li, and Liquan Xiao. Dsgbench: A
diverse strategic game benchmark for evaluating llm-based agents in complex decision-making
environments. _arXiv preprint arXiv:2503.06047_, 2025.


Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut,
Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly
capable multimodal models. _arXiv preprint arXiv:2312.11805_, 2023.


Chen Feng Tsai, Xiaochen Zhou, Sierra S Liu, Jing Li, Mo Yu, and Hongyuan Mei. Can large
language models play text games well? current state-of-the-art and open questions. _arXiv preprint_
_arXiv:2304.02868_, 2023.


Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and
Anima Anandkumar. Voyager: An open-ended embodied agent with large language models. _arXiv_
_preprint arXiv:2305.16291_, 2023.


Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai
Tang, Xu Chen, Yankai Lin, et al. A survey on large language model based autonomous agents.
_Frontiers of Computer Science_, 18(6):186345, 2024a.


Xingyao Wang, Yangyi Chen, Lifan Yuan, Yizhe Zhang, Yunzhu Li, Hao Peng, and Heng Ji.
Executable code actions elicit better llm agents. In _Forty-first International Conference on Machine_
_Learning_, 2024b.


Xinyu Wang, Bohan Zhuang, and Qi Wu. Are large vision language models good game players?
_arXiv preprint arXiv:2503.02358_, 2025.


Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny
Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models. _Advances in_
_neural information processing systems_, 35:24824–24837, 2022.


Wikipedia contributors. List of video game genres. [https://en.wikipedia.org/wiki/](https://en.wikipedia.org/wiki/List_of_video_game_genres)
[List_of_video_game_genres, 2025. Accessed: 2025-09-22.](https://en.wikipedia.org/wiki/List_of_video_game_genres)


Yue Wu, Xuan Tang, Tom M Mitchell, and Yuanzhi Li. Smartplay: A benchmark for llms as
intelligent agents. _arXiv preprint arXiv:2310.01557_, 2023.


An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li,
Dayiheng Liu, Fei Huang, Haoran Wei, et al. Qwen2. 5 technical report. _arXiv preprint_
_arXiv:2412.15115_, 2024.


Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. Webshop: Towards scalable
real-world web interaction with grounded language agents. _Advances in Neural Information_
_Processing Systems_, 35:20744–20757, 2022.


Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
React: Synergizing reasoning and acting in language models. In _International Conference on_
_Learning Representations (ICLR)_, 2023.


Aohan Zeng, Mingdao Liu, Rui Lu, Bowen Wang, Xiao Liu, Yuxiao Dong, and Jie Tang. Agenttuning:
Enabling generalized agent abilities for llms. _arXiv preprint arXiv:2310.12823_, 2023.


Dan Zhang, Sining Zhoubian, Min Cai, Fengzu Li, Lekang Yang, Wei Wang, Tianjiao Dong, Ziniu
Hu, Jie Tang, and Yisong Yue. Datascibench: An llm agent benchmark for data science. _arXiv_
_preprint arXiv:2502.13897_, 2025.


14


Yadong Zhang, Shaoguang Mao, Tao Ge, Xun Wang, Adrian de Wynter, Yan Xia, Wenshan Wu, Ting
Song, Man Lan, and Furu Wei. Llm as a mastermind: A survey of strategic reasoning with large
language models. _arXiv preprint arXiv:2404.01230_, 2024.


Xiangxi Zheng, Linjie Li, Zhengyuan Yang, Ping Yu, Alex Jinpeng Wang, Rui Yan, Yuan Yao, and
Lijuan Wang. V-mage: A game evaluation framework for assessing visual-centric capabilities in
multimodal large language models. _arXiv preprint arXiv:2504.06148_, 2025.


Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu, Wenhao Yu, Ratnadira Widyasari, Imam
Nur Bani Yusuf, Haolan Zhan, Junda He, Indraneil Paul, et al. Bigcodebench: Benchmarking code
generation with diverse function calls and complex instructions. _arXiv preprint arXiv:2406.15877_,
2024.


15


#### Orak: A Foundational Benchmark for Training and Evaluating LLM Agents on Diverse Video Games (Supplementary Material)

A G AME G ENRE C ATEGORIZATION


Video games are generally categorized into six widely recognized genres, _i.e._, Action, Adventure,
Role-Playing, Simulation, Strategy, and Puzzle, each characterized by distinct gameplay structures (Wikipedia contributors, 2025). **Action** games emphasize responsiveness and precise physical
control. **Adventure** games focus on narrative exploration, interactive dialogues, and clue-based
progression grounded in logical inference. **Role-Playing** games focus on character progression,
stat-driven combat mechanics, and quest-based narrative development. **Simulation** games present
system-driven environments in which players manage complex and interdependent variables such
as time, resources, and procedural systems. **Strategy** games are a genre that emphasizes planning,
resource management, decision-making, and tactical execution. **Puzzle** games revolve around rulebased problem solving, pattern recognition, and logical or spatial reasoning, typically within a clearly
defined system of constraints.


In Table 8, we categorize each of the 12 video games in Orak into one of the six major genres based
on the primary gameplay characteristics and the genre information provided by the respective game
publishers. Some games belong to one or more genres due to hybrid gameplay mechanics.


**Game** **Action** **Adventure** **Role-Playing** **Simulation** **Strategy** **Puzzle**


Street Fighter III _⃝_
Super Mario _⃝_
Ace Attorney _⃝_
Her Story _⃝_
Pok´emon Red _△_ _⃝_
Darkest Dungeon _△_ _⃝_ _△_
Minecraft _△_ _⃝_
Stardew Valley _△_ _△_ _⃝_
StarCraft II _△_ _⃝_
Slay the Spire _⃝_
Baba Is You _⃝_
2048 _⃝_


Table 8: Genre categorization of the 12 games in Orak. _⃝_ denotes the _main_ genre and _△_ indicates
the _secondary_ genre.


**(a) Street Fighter III** (Capcom, 1997) is classified as an _Action_ game, as it primarily relies on
responsiveness, frame-precise input, and physical dexterity. Its gameplay requires fast reflexes and
mastery of complex input sequences.


**(b) Super Mario** (Christian Kauten, 2018) is categorized as _Action_ game. The core gameplay
emphasizes precise timing in jumping and movement, demanding moment-to-moment control in
response to environmental hazards and enemy placements.


**(c) Ace Attorney** (Capcom, 2001) is labeled as an _Adventure_ game due to its narrative-driven structure,
reliance on clue collection, and logical deduction. Players progress by interacting with characters and
uncovering story elements through investigative mechanics, with minimal emphasis on reflex-based
input.


**(d) Her Story** (Barlow, 2015) similarly fits within the _Adventure_ category. Though more experimental
in form, it shares a strong focus on narrative discovery through a search-based interface, requiring
players to piece together a fragmented story using non-linear exploration and deductive reasoning.


**(e) Pokemon Red** **´** (Game Freak, 1996) is classified as a _Role-Playing_ game, as its primary mechanics
involve turn-based combat, character progression, stat management, and quest-driven exploration.


16


Additionally, _Adventure_ was assigned as a secondary genre to reflect the game’s emphasis on world
exploration, interaction with non-player characters, and sequential progression through narrative
landmarks.


**(f) Darkest Dungeon** (Red Hook Studios, 2016) is similarly assigned _Role-Playing_ as the main genre,
supported by stat-driven character development and progression systems. However, it also includes
significant _Strategy_ elements, as players must carefully manage resources, form party compositions,
and make tactical decisions in turn-based combat. _Adventure_ was further added as a secondary genre
due to its dungeon-crawling structure and emphasis on risk-driven exploration.


**(g) Minecraft** (Mojang Studios, 2011) is categorized as a _Simulation_ game due to its open-ended,
system-driven mechanics, including resource gathering, crafting, and environmental manipulation.
It also exhibits _Role-Playing_ traits through its progression systems and player-driven narrative
development, warranting secondary classification.


**(h) Stardew Valley** (ConcernedApe, 2016) is also assigned to the _Simulation_ genre based on its
emphasis on time management, farming systems, and interrelated mechanics spanning multiple ingame variables. It incorporates _Role-Playing_ through relationship-building and character progression,
and _Adventure_ through dungeon exploration, seasonal events, and quest-based interactions.


**(i) StarCraft II** (Blizzard Entertainment, 2010) is classified as a _Strategy_ game, consistent with
its real-time strategic planning, resource allocation, and micromanagement mechanics. Given the
importance of unit-level control, _Action_ was added as a secondary genre to reflect the real-time,
reflex-driven demands during gameplay.


**(j) Slay the Spire** (MegaCrit, 2017) is categorized solely as a _Strategy_ game. The gameplay centers
around deck-building, route optimization, and turn-based combat, requiring players to plan several

moves.


**(k) Baba Is You** (Hempuli, 2019) is clearly identified as a _Puzzle_ game, as its mechanics are centered
on solving logic-based problems through the manipulation of in-game rules represented by words.
The core loop involves constrained, rule-based problem solving and spatial reasoning.


**(l) 2048** (Cirulli, 2014) is also classified as a _Puzzle_ game, characterized by deterministic mechanics,
arithmetic pattern recognition, and constraint-based spatial logic within a fixed grid.


This genre classification provides a structured foundation for analyzing agent cognition and gameplay
dynamics across diverse games.


B R EQUIRED LLM C APABILITIES FOR G AMEPLAY


Looking at the Figure 3, most games demand advanced LLM capabilities across multiple dimensions,
as they are designed to challenge a wide range of human cognitive skills. (1) **Action** games,
_Street Fighter III_ and _Super Mario_ in red, require spatial reasoning and rule following, more than
long-context understanding and planning. (2) **Adventure** games, _Ace Attorney_ and _Her Story_ in
yellow, emphasize long-text understanding and logical reasoning due to the need to comprehend long
storylines. (3) **Role-playing** games, _Pokemon Red_ _´_ and _Darkest Dungeon_ in brown, require strong
long-term planning, logical reasoning, and rule-following abilities to understand game-specific rules
and complete milestones of game tasks. (4) **Simulation** games, _Minecraft_ and _Stardew Valley_ in green,
also require high levels of long-term planning and rule-following abilities. While _Minecraft_ requires
strong spatial reasoning and error handling, which are generally essential for simulation games,
_Stardew Valley_ gets lower scores for them because these abilities are not critical for its evaluation
task; earning money by harvesting crops. (5) **Strategic** games, _StarCraft II_ and _Slay the Spire_ in blue,
require various LLM abilities for gameplay. Notably, these two games are the only ones in Orak that
require 5 different LLM capabilities rated at level 3, highlighting that recent strategic video games
increasingly demand a wide range of cognitive skills for effective gameplay. (6) **Puzzle** games, _Baba_
_Is You_ and _2048_ in purple, require high levels of spatial reasoning, logical reasoning, and long-term
planning because puzzle games are typically designed to require complex problem-solving through
multiple reasoning hops and spatial understanding.


17


C S TREET F IGHTER III


C.1 G AME D ESCRIPTION FOR S TREET F IGHTER III


**Environment.** _Street Fighter III_ (Capcom, 1997) is a 2D competitive fighting game, known for precise controls, deep mechanics,
and a diverse roster of characters. Each character features unique
moves, combos, and super arts, requiring precise timing and strategic
decision-making. Players aim to defeat their opponent through a
mix of normal attacks, special moves, and advanced mechanics like
parries and cancels. For implementation, we use _Diambra Arena_

(a) Ken. (b) Chun-Li.

environment (DIAMBRA, 2025), a Docker-based platform designed
for RL research. _Street Fighter III_ is one of the environments sup- Figure 5: Two of playable
ported by Diambra, which not only enables seamless extraction of characters in _Street Fighter III_ .
the game state—such as screenshots, health, timer, and super bar values—but also provides a straightforward interface for sending controller inputs. In this setting, the agent operates in a discrete action
space that directly corresponds to various controller actions, including directional movement, attack
buttons, and their combinations, enabling intuitive and fine-grained control of the in-game character.


The game supports both single-player and multi-player modes. In single-player mode, the player
progresses through ten increasingly difficult stages, facing stronger opponents at each level. Each
stage follows a _best-of-three_ format, where the player must win two out of three matches to advance
to the next stage. The game ends upon either completion of the final stage or defeat. In multi-player
mode, two players compete in a best-of-three match, and the game is over once a winner is determined.
For our default evaluation setting, agents play Ken in both modes (see Figure 5(a)). However, since
the environment supports a variety of characters, we also conduct evaluations using Chun-Li to
demonstrate intra-game generalization capabilities (see Figure 5(b)).


**Observation-to-Text Conversion.** The Diambra

environment offers a convenient interface for extracting the game state from _Street Fighter III_ .
Through this interface, we obtain the latest game
frame at a resolution of 224×384, along with key
state information such as remaining time, player
and opponent health, super bar gauge, super count,
stun bar gauge, and stun status. However, a critical aspect in fighting games is understanding the
relative positions of the characters, which is not
directly provided by the Diambra environment. To
address this limitation, we employ a lightweight Figure 6: Character detection using YOLOv11
YOLOv11 object detection model (Khanam & Hus- model (Khanam & Hussain, 2024) in _Street_
sain, 2024) to extract the relative positions of the _Fighter III_ .
two characters from the game frame. Based on the computed distance, we classify the spatial relationship into three discrete categories— _very close_, _close_, and _far_ —and incorporate this information
into the agent’s user prompt.


**Action Space.** In the Diambra environment, the native action space is defined on a per-frame basis
and consists of 18 discrete actions. These are composed of:


- **Idle action (1 total)** : Idle (No action)


- **Movement actions (8 total)** : Left, Left + Up, Up, Up + Right, Right, Right + Down, Down,
Down+Left

- **Attack actions (9 total)** : Low Punch, Medium Punch, High Punch, Low Kick, Medium Kick, High
Kick, Low Punch+Low Kick, Medium Punch+Medium Kick, High Punch+High Kick


To enable more strategic and temporally consistent behavior, we use a higher-level action space that
abstracts these frame-level controls into semantically meaningful commands. Each high-level action
is mapped to a predefined sequence of low-level controller inputs, often spanning multiple frames.
The high-level action space is divided into two categories:


18


**System prompt (Planning)** **User prompt (Planning)**



You are a helpful AI assistant integrated with 'Street Fighter III: 3rd Strike' on the
PC, assisting future decision-making. Your goal is to assist in long-term strategy
planning to defeat your opponent. Based on the target task and the player's current
progress, your role is to propose the most suitable subtask for the current situation.
Your responses must be precise, concrete, and highly relevant to the player's
objectives.


Subtask_reasoning: Decide whether the previous subtask is finished and whether it
is necessary to propose a new subtask. The subtask should be straightforward,
contribute to the target task and be most suitable for the current situation, which
should be completed within a few actions. You should respond to me with:
1. How to finish the target task? You should analyze it step by step.
2. What is the current progress of the target task according to the analysis in step 1?
Please do not make any assumptions if they are not mentioned in the above
information. You should assume that you are doing the task from scratch.
3. (If previous subtask is provided) What is the previous subtask? Does the
previous subtask finish? Or is it improper for the current situation? Then select a
new one, otherwise you should reuse the last subtask.


**Game screenshot**



### Target task
Defeat the opponent


### Previous subtask for the task

The current subtask is to attempt another throw to break the
opponent's guard and reduce their health.


### Last executed action

- Medium Punch+Medium Kick

- High Punch+High Kick


### Self reflection of the last executed action

The attempted throw to break the opponent's guard and reduce
their health was unsuccessful. The opponent's health remained
unchanged, and the distance between the players increased,
indicating that the opponent likely evaded or countered the throw.


### Current state

You are playing Ken in Street Fighter 3. Your opponent is Yang.
You are facing left.
Distance from Opponent: close
Time Remaining: 95
Health:


Your Health: 161

Opponent's Health: 134
Super Bar Guage:

Your Super Bar Guage: 32
Opponent's Super Bar Guage: 9
Super Count (Count of activated super move):

Your Super Count: 0
Opponent's Super Count: 0
Stun Bar Guage:

Your Stun Bar Guage: 0
Opponent's Stun Bar Guage: 10
IsStunned (0: not stunned, 1: stunned):

Your Status: 0

Opponent's Special Status: 0


You MUST respond in the format described below, and you
should not output comments or other information.
### Subtask_reasoning
1. ...

2. ...

...

### Subtask

The current subtask is



Figure 7: Planning prompt for ‘reflection-planning’ agent playing _Street Fighter III_ .


- **Character-agnostic actions (14 total)** : Move Closer, Move Away, Jump Closer, Jump Away,
Super Attack, Low Punch, Medium Punch, High Punch, Low Kick, Medium Kick, High Kick, Low
Punch+Low Kick, Medium Punch+Medium Kick, High Punch+High Kick

- **Character-specific actions** :


**–** Ken: Fireball (Hadouken), Hurricane Kick, etc.

**–** Chun-Li: Kikkoken, Hyakuretsukyaku, etc.


For example, if the character is positioned on the left side of the screen and the high-level action is
‘Move Closer’, the system issues ‘Right’ movement commands over four frames. If the action is ‘Fireball’, the corresponding low-level sequence would be ‘Down’ _→_ ‘Down + Right’ _→_ ‘Right’ _→_ ‘Medium
Punch’. Since the number of character-specific actions varies, the total size of the high-level action
space differs depending on character, typically ranging around 20 actions.


C.2 G AMEPLAY P ROMPT FOR S TREET F IGHTER III


Our implementation of _Street Fighter III_ supports four types of agents: reflection, planning, reflectionplanning, and zero-shot. Among these, we introduce prompts for the ‘reflection-planning’ agent in
this subsection. Figures 7–9 present the prompts used by the reflection-planning agent for planning,
action inference, and reflection, respectively. At each step, the agent plans to determine the subtask,
using the planning module. Based on this subtask, the action inference module infers the optimal
action to execute. Finally, the reflection module evaluates whether the executed action was successful.


**Planning prompt.** As shown in Figure 7, the system prompt provides detailed instructions for an
agent to support strategic planning. It defines the assistant’s role in proposing suitable subtasks based


19


**System prompt (Action Inference)** **User prompt (Action Inference)**



You are the best and most aggressive Street Fighter III: 3rd Strike player in the
world. Your goal is to defeat your opponent as quickly and efficiently as possible
using optimal strategies.
Analyze the current game state, the distance between your character's and the
opponent's character, and remaining health. Then, determine the best next actions
to execute, ensuring you maintain offensive pressure.
### Strategy Guidelines ###
1. You can only output at most TWO actions in the output.
2. Choose the appropriate move based on the distance from the opponent and the
current situation.

3. Utilize defensive or evasive techniques to minimize incoming damage.
4. Combine normal attacks and special moves to control space and apply pressure
on the opponent.
5. If the super bar gauge is full, use Super Action to maximize damage.
6. If the distance is close, use close-range attacks to reduce the opponent's health.
7. If the distance is far, you can either approach the opponent or use long-range
attacks to reduce their health.

8. You can use Megafireball if the super bar gauge is more than 30.
9. You can use Super Attack 4 (Shippuu-Jinrai-Kyaku) ONLY if your super count
is non-zero.

10. You CANNOT use Supper Attack 4 (Shippuu-Jinrai-Kyaku) if your super
count is zero.

11. Strategically choose the best action based on current game state.
12. If your opponent get stunned, try powerful moves to maximize damage.
### Valid action set ###


 - Move Closer

- Move Away

 - Fireball

 - Megapunch

 - Hurricane

 - Megafireball

 - Super attack 4

 - Low Punch

 - Medium Punch

 - High Punch

 - Low Kick

 - Medium Kick

 - High Kick

 - Low Punch+Low Kick

 - Medium Punch+Medium Kick

 - High Punch+High Kick

 - Jump Closer

 - Jump Away
### Decision Output Format ###
Analyze the provided game state and determine the **next actions** to take next.
Return your decision in the following exact format:
### Reasoning
<a detailed summary of why this action was chosen>
### Actions

<at most two consecutive actions in the valid action set>


Ensure that:

- The '### Reasoning' field provides a clear explanation of why the action is the
best choice.

- The '### Actions' field contains only at most two of the valid actions.



### Current subtask

The current subtask is to close the distance by using a forward
dash or advancing special move, then apply pressure with a mix of
medium and heavy attacks to reduce the opponent's health.


### Last executed action:

- Medium Punch+Medium Kick

- High Punch+High Kick


### Self reflection of the last executed action

The attempted throw to break the opponent's guard and reduce
their health was unsuccessful. The opponent's health remained
unchanged, and the distance between the players increased,
indicating that the opponent likely evaded or countered the throw.


### Current state:

You are playing Ken in Street Fighter 3. Your opponent is Yang.
You are facing left.
Distance from Opponent: close
Time Remaining: 95
Health:


Your Health: 161

Opponent's Health: 134
Super Bar Guage:

Your Super Bar Guage: 32
Opponent's Super Bar Guage: 9
Super Count (Count of activated super move):

Your Super Count: 0
Opponent's Super Count: 0
Stun Bar Guage:

Your Stun Bar Guage: 0
Opponent's Stun Bar Guage: 10
IsStunned (0: not stunned, 1: stunned):

Your Status: 0

Opponent's Special Status: 0


Based on the above information, analyze the current situation for
what you should do for the next step. Then, you should output the
exact actions you want to execute in the game.
You should only respond with actions from the valid action set.
You should only respond in the format described below, and you
should not output comments or other information.
Provide your response in the strict format:
### Reasoning

- ...

- ...

- ...

### Actions

- ...

- ...



Figure 8: Action inference prompt for ‘reflection-planning’ agent playing _Street Fighter III_ .


on the target task and the current game state. The user prompt includes: (1) the main goal of the game,
(2) the previous subtask (generated by the recent planning module), (3) the last executed action, (4) a
self-reflection on the last action (generated by the recent reflection module), (5) the current state, and
(6) the expected output format for the subtask reasoning task.


**Action inference prompt.** As shown in Figure 8, the system prompt outlines strategic guidelines
for playing Ken, a predefined set of valid actions, and the required output format. The user prompt
contains: (1) the current subtask (provided by the recent planning module), (2) the last executed
action, (3) the corresponding self-reflection (generated by the recent reflection module), (4) the
current state, and (5) the expected output format for the action inference task.


**Reflection prompt.** As illustrated in Figure 9, the system prompt provides detailed instructions for
an agent to perform reflection. The agent is required to analyze whether the last action was successful
based on state transitions. The user prompt includes: (1) the target task, (2) the current subtask
(generated by the recent planning module), (3) the last executed action, (4) the previous state, (5) the
current state, and (6) the expected output format for the reflection task.


C.3 E VALUATION M ETRIC FOR S TREET F IGHTER III


**Single-Agent Play.** In the single-player mode, the agent faces a series of 10 stages against in-game
rule-based bots. The game ends either when the player loses a stage or successfully clears all 10


20


**System prompt (Reflection)**


You are a helpful AI assistant integrated with 'Street Fighter III: 3rd Strike' on the
PC, capable of analyzing in-game contexts and determining whether an executed
action has taken effect. Your task is to evaluate the success of actions based on

state changes and provide logical reasoning.
You need to answer the following questions step by step to derive reasoning based
on the last action and the states.

1. What is the executed action and its desired result?

2. What is the difference between the two states? Compare every component.
3. Was the executed action successful? Provide reasoning.
4. (If the last action was not successful) What is the most probable cause? Give
only one cause.You should summarize the reasoning in a clear and concise manner,
providing a logical explanation for the success or failure of the last action.


**User prompt (Reflection)**


### Target task
Defeat the opponent


### Current subtask

The current subtask is to close the distance by using a forward dash or advancing
special move, then apply pressure with a mix of medium and heavy attacks to
reduce the opponent's health.


### Last executed action

- Megafireball

- Move Closer


### Previous state

You are playing Ken in Street Fighter 3. Your opponent is Yang.
You are facing left.
Distance from Opponent: close
Time Remaining: 95
Health:


Your Health: 161

Opponent's Health: 134
Super Bar Guage:

Your Super Bar Guage: 32
Opponent's Super Bar Guage: 9
Super Count (Count of activated super move):

Your Super Count: 0
Opponent's Super Count: 0
Stun Bar Guage:

Your Stun Bar Guage: 0
Opponent's Stun Bar Guage: 10
IsStunned (0: not stunned, 1: stunned):

Your Status: 0

Opponent's Special Status: 0



### Current state

You are playing Ken in Street Fighter 3. Your opponent is Yang.
You are facing left.
Distance from Opponent: close
Time Remaining: 94
Health:


Your Health: 161

Opponent's Health: 123
Super Bar Guage:

Your Super Bar Guage: 35
Opponent's Super Bar Guage: 9
Super Count (Count of activated super move):

Your Super Count: 0
Opponent's Super Count: 0
Stun Bar Guage:

Your Stun Bar Guage: 0
Opponent's Stun Bar Guage: 14
IsStunned (0: not stunned, 1: stunned):

Your Status: 0

Opponent's Special Status: 0


You should only respond in the format as described below.
### Self_reflection
1. ...

2. ...

3. ...

4. ...

### Self_reflection_summary

...



Figure 9: Reflection prompt for ‘reflection-planning’ agent playing _Street Fighter III_ .


stages. Therefore, the evaluation metric can be straightforwardly defined as


Score = Number of stages cleared by the agent _×_ 10 _._


**Multi-Agent Play.** To evaluate models in a competitive multi-agent environment, we conduct
pairwise matches between all agents and compute Elo ratings based on their win rates. For each pair,
three games are played to obtain a reliable estimate of relative performance. The resulting win rate
matrix and Elo scores are presented in Figure 4(a).


We adopt a Bradley-Terry model formulation (Bradley & Terry, 1952) for Elo estimation, where
each model’s rating is iteratively optimized using gradient ascent on the log-likelihood of observed
outcomes. The gradient is computed based on the expected win probabilities derived from current
ratings, using the standard Elo transformation:


1
_P_ ( _i_ beats _j_ ) = 1 + 10 [(] _[R]_ _[j]_ _[−][R]_ _[i]_ [)] _[/]_ [400] _[,]_


where _R_ _i_ and _R_ _j_ denote the Elo ratings of agent _i_ and agent _j_, respectively. The expected probability
of _i_ defeating _j_ increases as the rating difference _R_ _i_ _−_ _R_ _j_ becomes larger. After optimization, we
shift all Elo ratings so that their mean equals 1,500 for intuitive interpretation. If two models receive
identical ratings, the one that won their head-to-head match is ranked higher.


C.4 E XPERIMENTAL C ONFIGURATION FOR S TREET F IGHTER III


For all 6 open-source LLMs, including Llama-3.2-1B/3B, Qwen-2.5-3B/7B, and Minitron-4B/8B,
we use a temperature of 0.0 and a repetition penalty of 1.0. During LLM inference, we pause the


21


|Models|SF3|Rank|
|---|---|---|
|Random Agent|10.0_±_6.4|12|
|Llama-3.2-1B<br>0.0_±_0.0<br>13<br>Llama-3.2-3B<br>13.3_±_5.8<br>10.5<br>Qwen-2.5-3B<br>20.0_±_0.0<br>4.5<br>Qwen-2.5-7B<br>16.7_±_11.5<br>7.5<br>Minitron-4B<br>16.7_±_11.5<br>7.5<br>Minitron-8B<br>23.3_±_5.8<br>3|Llama-3.2-1B<br>0.0_±_0.0<br>13<br>Llama-3.2-3B<br>13.3_±_5.8<br>10.5<br>Qwen-2.5-3B<br>20.0_±_0.0<br>4.5<br>Qwen-2.5-7B<br>16.7_±_11.5<br>7.5<br>Minitron-4B<br>16.7_±_11.5<br>7.5<br>Minitron-8B<br>23.3_±_5.8<br>3|Llama-3.2-1B<br>0.0_±_0.0<br>13<br>Llama-3.2-3B<br>13.3_±_5.8<br>10.5<br>Qwen-2.5-3B<br>20.0_±_0.0<br>4.5<br>Qwen-2.5-7B<br>16.7_±_11.5<br>7.5<br>Minitron-4B<br>16.7_±_11.5<br>7.5<br>Minitron-8B<br>23.3_±_5.8<br>3|
|GPT-4o-mini<br>16.7_±_11.5<br>7.5<br>GPT-4o<br>29.7_±_14.3<br>2<br>o3-mini<br>**33.3**_±_15.3<br>1<br>Gemini-2.5-pro<br>13.3_±_11.5<br>10.5<br>Claude-3.7<br>16.7_±_11.5<br>7.5<br>Deepseek-R1<br>20.0_±_0.0<br>4.5|GPT-4o-mini<br>16.7_±_11.5<br>7.5<br>GPT-4o<br>29.7_±_14.3<br>2<br>o3-mini<br>**33.3**_±_15.3<br>1<br>Gemini-2.5-pro<br>13.3_±_11.5<br>10.5<br>Claude-3.7<br>16.7_±_11.5<br>7.5<br>Deepseek-R1<br>20.0_±_0.0<br>4.5|GPT-4o-mini<br>16.7_±_11.5<br>7.5<br>GPT-4o<br>29.7_±_14.3<br>2<br>o3-mini<br>**33.3**_±_15.3<br>1<br>Gemini-2.5-pro<br>13.3_±_11.5<br>10.5<br>Claude-3.7<br>16.7_±_11.5<br>7.5<br>Deepseek-R1<br>20.0_±_0.0<br>4.5|


Table 9: Gameplay score on
_Street Fighter III_ .








|Models Agent|SF3|Rank|
|---|---|---|
|Random Agent<br>-|10.0_±_6.4|9|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|13.3_±_5.8<br>**30.0**_±_17.3<br>20.0_±_0.0<br>16.7_±_20.8|8<br>1.5<br>6<br>7|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|29.7_±_14.3<br>23.3_±_20.8<br>**30.0**_±_26.5<br>23.3_±_20.8|3<br>4.5<br>1.5<br>4.5|


|Models Input|SF3|Rank|
|---|---|---|
|Random Agent<br>-|10.0_±_6.4|10|
|GPT-4o<br>Text<br>Image<br>Both|**29.7**_±_14.3<br>23.7_±_15.9<br>24.3_±_14.5|2<br>4<br>3|
|Gemini<br>Text<br>Image<br>Both|13.3_±_11.5<br>16.7_±_11.5<br>**20.0**_±_10.0|9<br>7<br>6|
|Claude<br>Text<br>Image<br>Both|16.7_±_11.5<br>23.3_±_11.5<br>**33.3**_±_5.8|7<br>5<br>1|



Table 10: Ablation study for agentic modules on _Street Fighter III_ .



Table 11: Comparison across
modalities on _Street Fighter III_ .



_Street Fighter III_ game environment. We set the maximum number of game steps to 10,000. Due to
the in-game time constraints, episodes do not reach the maximum of 10,000 steps. A single stage
(best-of-three matches) is usually resolved within 100 to 200 steps, as rounds either timeout or end
early when one player’s health reaches zero.


C.5 R ESULT FOR S TREET F IGHTER III


All reported results in Tables 9–12 are computed as the mean and standard deviation over three to
five independent runs, using a ‘zero-shot’ agent for each model configuration. To establish a baseline
for comparison, we additionally included a random agent that selects an arbitrary action uniformly at
random. This agent was evaluated over 30 episodes, and its performance is summarized in tables.


**Single-Agent Play.** The performance across various LLMs was evaluated as presented in Table 9.
The smallest model, Llama-3.2-1B, completely failed to comprehend the current game context and
consistently ignore the required output format, performing even worse than a random agent. On the
other hand, all other evaluated models surpassed the random agent, demonstrating varying levels
of competence. Commercial LLMs generally outperformed their open-source counterparts, with
GPT-4o and o3-mini standing out as notable examples.


To investigate the effectiveness of agentic modules, we conducted an ablation study shown in Table
10. For Llama-3.2-3B, the Reflection agent showed notably superior performance, indicating that
reflective reasoning significantly aids in aligning actions to game dynamics, possibly by allowing
the model to reassess and correct previous outputs based on feedback. Conversely, for GPT-4o, both
the zero-shot and Planning agents performed remarkably well. This may suggest GPT-4o’s inherent
capability for generalization (zero-shot) and structured sequential reasoning (planning), enabling
efficient decision-making without iterative reflection.


Input modality may significantly influence agent performance, since spatial information in fighting
games is expecially important for gameplay. Since our implementation simplify character distance into
three sparse levels, we expected image inputs would enhance spatial understanding and consequently
improve performance. However, as shown in Table 11, GPT-4o surprisingly demonstrated decreased
performance when using image inputs, possibly due to limited visual comprehension capabilities. In
contrast, Gemini and Claude effectively leveraged visual data, improving their gameplay scores.


Lastly, Table 12 demonstrates intra-game generalization capabilities when fine-tuning models on Ken specific gameplay data and evaluating on Chun-Li scenarios, which represent out-of-distribution
conditions due to differences in action spaces (as previously detailed in Section C.1). Remarkably,
the previously format-incompliant pretrained Llama-3.2-1B learned to follow the required output
format effectively and exhibited excellent gameplay performance after fine-tuning, even in Chun-Li
gameplay. A similar improvement was observed in Llama-3.2-3B, which even surpassed GPT-4o in
performance. These results highlight the significant impact of targeted fine-tuning, demonstrating
that relatively small-scale LLMs can achieve substantial gains in task-specific capability.


**Multi-Agent Play.** We evaluate agent performances in a multi-agent environment by conducting
pairwise matches among 8 LLMs, all operating in a zero-shot setting. The results are provided in


22


|Model Finetune|SF3|
|---|---|
|Llama-3.2-1B<br>✗<br>✓|0.0_±_0.0<br>**42.0**_±_16.4|
|Llama-3.2-3B<br>✗<br>✓|12.0_±_11.0<br>**40.0**_±_7.1|
|GPT-4o<br>✗<br>10.0_±_0.0|GPT-4o<br>✗<br>10.0_±_0.0|


Table 12: Intra game generalization score of _Street Fighter III_ .


Figure 4(a). Each pairwise matchup consisted of three independent games, with each game played in
a best-of-three format to determine the winner. To ensure fair performance comparison, both agents
used the same character—Ken—in all matches.


Notably, unlike the single-agent evaluation results in Table 9, Minitron-8B consistently outperforms
all other models in the multi-agent arena and achieves the highest Elo rating. This divergence raises
the possibility that the involvement of other intelligent agents could alter the game dynamics, perhaps
due to increased strategic diversity or emergent adversarial behavior.


D S UPER M ARIO


D.1 G AME D ESCRIPTION FOR S UPER M ARIO



**Environment.** _Super Mario_ (1985 Super
Mario Bros) (Christian Kauten, 2018) is a sidescrolling game where the player controls Mario
to avoid obstacles, defeat monsters, and reach Brick Question Block BlockStair
the flag. In this environment, Mario progresses
through the game using directional key controls
( _e.g._, ‘left’ and ‘right’ keys) and jump actions.
Mario should either destroy or traverse obstacles Pipe GoombaMonster MonsterKoopa
( _e.g._, bricks, stairs, pipes), avoid or defeat mon
(a) Screenshot. (b) Object Patterns.

sters ( _e.g._, Goombas, Koopas) by jumping on
them and avoid falling into pits. For implemen- Figure 10: Screenshot and assets of _Super Mario_ .
tation, we adopt the gym ~~s~~ uper ~~m~~ ario ~~b~~ ros environment (Kauten, 2018), which is widely used
in the reinforcement learning (RL) community. Specifically, we use the SuperMarioBros-v1
environment, where Mario plays within a 256 _×_ 240-pixel screen with a black background, as shown
in Figure 10(a). The environment consists of 8 worlds, each containing 4 stages. We use World 1,
Stage 1 as our _default evaluation setting_ (for Table 3). However, the environment supports evaluation across any world and stage. For example, we use World 3, Stage 1 for the evaluation of
_intra-game generalization_ (for Table 7).


**Observation-to-Text Conversion.** The environment only provides RGB image frames as observations. To convert visual game states into text input suitable for LLMs, we apply _visual pattern_
_matching_ to parse the exact location of each object on the frame. As shown in Figure 10(b), in the
SuperMarioBros-v1 environment, the pixel-level visual patterns of objects remain stable across
frames. By maintaining a set of pixel templates for all game objects as game assets, we perform 2D
visual pattern matching to parse the presence and exact location of each object in the scene. These
parsed object locations are converted to 2D coordinates ( _x, y_ ) and formatted as text, which is then
passed to the LLM as part of its observation input.


**Action Space.** We constrain Mario to only move in the ‘right’ direction to simplify the control space.
Mario can ‘jump’ at varying heights, and by constraining action spans 4 game frames ( _i.e._, frame
skipping), Mario’s jumping ability is discretized into 7 levels. Jump Level 0 corresponds to walking
forward without jumping, while Jump Levels 1 through 6 represent increasing jump heights, with
Level 6 being the highest possible jump. At each game step, the LLM chooses a jump level from 0 to
6, determining the jump height as Mario moves to the right.


23



Brick Question



Stair

Block



Block



Pipe Monster
Goomba



Monster



Goomba Koopa


(a) Screenshot. (b) Object Patterns.



Figure 10: Screenshot and assets of _Super Mario_ .


**System prompt** **User prompt**



You are an AI assistant playing the Super Mario game.
Your goal is to reach the flag at the end without dying by avoiding or defeating obstacles/enemies


Object Descriptions

- Bricks: Breakable blocks; may contain items or coins (Size: 16x16)

- Question Blocks: Reveal coins or power-ups when hit; deactivate after use (Size: 16x16)

- Pit: Falling in results in losing a life

- Warp Pipe: Raised above the ground, so Mario must jump over them when it appear in front (Size: 30xHeight(y))

- Monster Goomba: Basic enemy; can be defeated by jumping on it (Size: 16x16)

- Monster Koopa: Turtle enemy; retreats into shell when jumped on (Size: 20x24)

- Item Mushroom: Grows Mario larger, grants protection (Size: 16x16)

- Stairs: Used to ascend/descend terrain

- Flag: Touch to complete the level

- Ground: the ground level in the game is y=32


Action Descriptions

- Mario (Size: 15x13) continuously moves to the right at a fixed speed

- You must choose an appropriate jump level to respond to upcoming obstacles

- Each jump level determines both:
- How far Mario jumps horizontally (x distance)
- How high Mario reaches at the peak of the jump (y height)

- Jump Levels *(values based on flat ground jumps)*:
- Level 0: +0 in x, +0 in y (No jump, just walk)
- Level 1: +42 in x, +35 in y
- Level 2: +56 in x, +46 in y
- Level 3: +63 in x, +53 in y
- Level 4: +70 in x, +60 in y
- Level 5: +77 in x, +65 in y
- Level 6: +84 in x, +68 in y

- The key is choosing the *right jump level at the right moment*

- *Use higher levels* to jump over taller or farther obstacles

- Consider *the size* of Mario and objects

- While jumping, Mario follows a *parabolic arc*, so Mario can be *blocked by objects mid-air or be defeated by
airborne enemies*

- Mario can step on top of bricks, blocks, warp pipes, and stairs


At each game step, you will receive the current game state in the following format:
Position of Mario: (x, y)
Position of all objects:

- Bricks: [(x1, y1), (x2, y2), ...]

- Question Blocks: [(x1, y1), ...]

- Inactivated Blocks: [(x1, y1), ...]

- Monster Goombas: [(x1, y1), ...]

- Monster Koopas: [(x1, y1), ...]

- Pit: start at (x1, y1), end at (x2, y2)

- Warp Pipes: [(x1, y1, height), ...]

- Item Mushrooms: [(x1, y1), ...]

- Stair Blocks: [(x1, y1), ...]

- Flag: (x, y)
(Note: All (x, y) positions refer to the top-left corner of each object)


You should then respond with
Explain (if applicable): Why you choose the jump level
Jump Level: n (where n is an integer from 0 to 6, indicating the chosen jump level)


You MUST only respond in the format with the prefix '### Actions\n' as below:
### Actions

Explain: ...
Jump Level: n



### Game State

Position of Mario: (122, 45)
Positions of all objects

 - Bricks: (92, 88), (124, 95), (156, 95)

 - Question Blocks: (18, 95), (108, 95), (140, 95), (124,158)

 - Inactivated Blocks: None

 - Monster Goomba: None

 - Monster Koopas: None

 - Pit: start at None, end at None

 - Warp Pipe: (223,63,34)

 - Item Mushrooms: None

 - Stair Blocks: None

 - Flag: None
(Note: All (x, y) positions refer to the top-left corner of each object)


**Game screenshot**



Figure 11: Action inference prompt for ‘zero-shot’ agent playing _Super Mario_ .


D.2 G AMEPLAY P ROMPT FOR S UPER M ARIO


Figure 11 shows the action inference prompt used by the ‘zero-shot’ agent for playing _Super Mario_ .
The system prompt contains most of the gameplay-specific knowledge. It includes (1) the main goal
of the game, (2) detailed descriptions and sizes of each object, (3) explanations and safety notes for
each action, and (4) the expected input-output format between the LLM and the environment. The
user prompt provides the current game state as a list of all objects detected in the frame, represented
by their top-left corner (x, y) coordinates obtained by visual pattern matching. Given this prompt,
the LLM agent infers the appropriate jump level to advance safely toward the flag by avoiding
obstacles and monsters.


D.3 E VALUATION M ETRIC FOR S UPER M ARIO


The goal of _Super Mario_ is to reach the flag located at the right end of the stage. Since the
gym ~~s~~ uper ~~m~~ ario ~~b~~ ros environment provides Mario’s current position on the map, we define
the evaluation metric as the proportion of the distance traversed toward the flag before Mario dies.
Formally, the normalized score is defined as:


Score = _dist_ ( _x_ _Mario_ _, x_ _start_ ) _/dist_ ( _x_ _flag_ _, x_ _start_ ) _×_ 100 _,_


where _x_ _Mario_, _x_ _flag_, and _x_ _start_ are the _x_ coordinate of Mario traversed before die, that of the flag,
and that of the starting position on the map, respectively.


24


|Models|SuperMario|Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B|18.7_±_8.6<br>31.8_±_10.1<br>23.4_±_14.1<br>27.2_±_9.6<br>24.4_±_6.0<br>31.3_±_12.8|12<br>4<br>11<br>9<br>10<br>6|
|GPT-4o-mini<br>GPT-4o<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|28.8_±_8.8<br>34.1_±_14.2<br>34.9_±_14.6<br>**38.0**_±_14.6<br>31.7_±_8.2<br>28.7_±_13.2|7<br>3<br>2<br>1<br>5<br>8|


Table 13: Gameplay score on
_Super Mario_ .








|Models Agent|SuperMario|Rank|
|---|---|---|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|21.2_±_8.2<br>32.4_±_8.6<br>27.0_±_8.4<br>31.8_±_10.1|8<br>2<br>7<br>4|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|29.6_±_9.2<br>32.3_±_15.5<br>29.4_±_12.5<br>**34.1**_±_14.2|5<br>3<br>6<br>1|


|Models Input|SuperMario|Rank|
|---|---|---|
|GPT-4o<br>Text<br>Image<br>Both|34.1_±_14.1<br>27.1_±_13.7<br>27.1_±_10.2|3<br>6.5<br>6.5|
|Gemini<br>Text<br>Image<br>Both|38.0_±_13.4<br>28.5_±_10.7<br>**40.9**_±_9.6|2<br>5<br>1|
|Claude<br>Text<br>Image<br>Both|28.7_±_13.2<br>25.6_±_6.4<br>22.6_±_6.3|4<br>8<br>9|



Table 14: Ablation study for agentic modules on _Super Mario_ .



Table 15: Comparison across
modalities on _Super Mario_ .



D.4 E XPERIMENTAL C ONFIGURATION FOR S UPER M ARIO


For all 6 open-source LLMs, including Llama-3.2-1B/3B, Qwen-2.5-3B/7B, and Minitron-4B/8B,
we use a temperature of 1 and a repetition penalty of 1. During LLM inference, we pause the _Super_
_Mario_ game environment. We set the maximum number of game steps to 100. We run all experiments
with 20 trials and report the average score with the standard deviation.


D.5 R ESULT FOR S UPER M ARIO


As shown in Table 13, Gemini-2.5-pro achieves the highest score of 38.0 on _Super Mario_, followed
by o3-mini with the score of 34.9. Among open-source LLMs, Llama-3.2-3B and Minitron-8B
perform competitively, achieving scores of 31.8 and 31.3 respectively, which are comparable to the
31.7 score of Claude-3.7-sonnet. Qualitatively, most LLMs, including Gemini-2.5-pro, frequently
fail to correctly estimate the _parabolic_ jump trajectory when Mario is mid-air. This change of moves
often results in Mario colliding with obstacles or being killed by monsters.


Table 14 shows the effect of reflection and planning modules on gameplay performance. Among
these, the reflection module has a more pronounced impact. Specifically, when Mario is stuck in front
of high obstacles such as warp pipes, the reflection module enables the agent to revise its previous low
jump level decisions and select a higher jump level, allowing it to overcome the obstacle and proceed,
thereby improving the final score. GPT-4o achieves the best score of 34.1 when both reflection
and planning modules are used. In contrast, Llama-3.2-3B performs best when only the reflection
module is used with a score of 32.4, indicating that Llama-3.2-3B may not benefit from the additional
planning module or be easily disturbed by its response.


As shown in Table 15, using image-only input observations consistently underperforms compared to
text-only inputs across all models, including GPT-4o, Gemini-2.5-pro, and Claude-3.7-sonnet. This
suggests that relying solely on visual input makes it more challenging for models to extract detailed
information from the game scene or to perform spatial reasoning, _i.e._, estimating distances between
objects. In contrast, when both text and image inputs are provided, GPT-4o and Claude-3.7-sonnet
show a performance drop, while Gemini-2.5-pro shows improved performance. This indicates that
multimodal input can be beneficial when the model effectively integrates complementary information
from both modalities.


E A CE A TTORNEY


E.1 G AME D ESCRIPTION FOR A CE A TTORNEY


**Environment.** _Ace Attorney_ (Capcom, 2001) is a courtroom adventure game where players act as defense attorneys, gather evidence, and cross-examine witnesses. We
target the first episode of _Phoenix Wright: Ace Attorney_
_Trilogy_ on _Steam_ (see Figure 12). We define four subtasks:
one three-question multiple-choice quiz where the player
selects the correct answer, and three cross-examination
tasks where the player presses witnesses for more details



25



Figure 12: Screenshot of Episode 1: The
First Turnabout.


**System prompt** **User prompt**



You are an AI defense attorney in an interactive Ace Attorney-style trial. The game advances screen-byscreen based on your choices, and your goal is to win by managing dialogue and evidence effectively.
**ONLY** perform actions permitted by the currently visible screen.


Responsibilities:

- Monitor dialogue for cues to review evidence or profiles.

- Choose the best options in multiple-choice scenarios.

- Cross-examine witnesses to detect contradictions and present evidence.


Gameplay Guidelines:

- Press "Ok" to continue dialogue and "Tab" to access the Court Record.

- **ONLY** access the Court Record when absolutely necessary: if the "Last Court Record" is None or
if the "Last Check Time" is significantly outdated relative to the current dialogue.

- All actions must be based solely on the on-screen dialogue. The on-screen dialogue is defined as the
very last entry in the "Current State"'s [Recent Conversations], which is marked as [**The Conversation
Currently on Screen**].

- There are two types of important dialogue: (1) regular dialogue (with no color formatting) and (2)
testimony for Cross-Examination, displayed in green (color=#00f000).

- The final goal of the game is to identify contradictions between the on-screen testimony and the Court
Record, and to present evidence proving that the false testimony is being shown.


**IMPORTANT (Cross-Examination Eligibility):** You may perform Cross-Examination actions
("Press at the moment of testimony" or "Present the selected evidence") only when both conditions
below are met:


1. The testimony is displayed in color=#00f000 and the "Current State" includes **CrossExamination!**


2. The most recent testimony (marked as [**The Conversation Currently on Screen**]) clearly relates
to a contradiction you have either suspended or confirmed.


**IMPORTANT (Action Strategy):** When both Cross-Examination Eligibility conditions are satisfied,
use either of the following two Cross-Examination actions: If you need additional hints or clarification,
press "Press at the moment of testimony" (represented by "Hold it!" in [Recent Conversations]).
However, if you are confident and ready to expose false testimony, wait until the contradictory on-screen
testimony appears, then press "Tab", select the appropriate evidence, and execute "Present the selected
evidence" (represented by "Objection!" in [Recent Conversations]).

- **DO NOT** use these actions for merely suspicious or ambiguous discrepancies. Trigger them only
when there is a definitive contradiction—such as when the testimony directly and logically conflicts with
the actual record.

- **DO NOT** repeat actions that are already recorded in "Last Decisions" on the same on-screen
testimony.

- Only the on-screen testimony ([**The Conversation Currently on Screen**]) can trigger the actions.
Even if your analysis or long-term memory indicates a contradiction, continue pressing "Ok" until the
corresponding testimony appears on the screen.

- To return to a previous testimony and display it on screen, press the "Left" key.


Additional Notes:

- Constantly assess the dialogue for cues and adapt your strategy as new evidence emerges.

- Remember that not every piece of testimony contains a contradiction; only initiate cross-examination
when there is clear and definitive evidence of inconsistency.

- **IMPORTANT:** Only select an action from the candidate list by responding solely with the
**INTEGER** number corresponding to the selected option.



Current State:

[Recent Conversations]

[2025-04-02 17:18:30] Alias: Yes! Er... yes, Your Honor?

…

[**The Conversation Currently on Screen** - 2025-05-23 12:44:13]
Bravo: Open the Court Record with <color=#ff0000>     </color>,
then point out <color=#ff0000>contradictions</color> in the testimony!


Last Court Record:

**Last Check Time**: 2025-05-23 12:44:13

**Court Record - Evidence**:

1: Attorney's Badge - No one would believe I was a defense attorney if I
didn't carry this.

…

5: Blackout Record - Electricity to Ms. Foxtrot's building was out from
noon to 6PM on the day of the
crime.

**Court Record - Profile**:

1: Bravo (Age: 27) - Chief Attorney at Bravo ＆ Co. My boss, and a
very good defense attorney.

…5: Echo (Age: 36) - Discovered Ms. Foxtrot's body. Newspaper salesman
who saw Delta flee the scene.


Last Decisions:

None


**Possible Options** (Active Key Types):
1: Ok

2: Tab


Please respond using the following format:
### Reasoning

[Your step-by-step reasoning here.]


### Actions

[**ONLY** output the **INTEGER** number corresponding to the
correct option from the **Possible Options**.]


**Game screenshot**



Figure 13: Action inference prompt for ‘zero-shot’ agent playing _Ace Attorney_ .


or presents evidence to expose contradictions. We use
Harmony (Pardeike, 2025) with a BepInEx plugin (Contributors, 2025a) to hook the game’s source code at launch,
capturing states such as dialogue text, arrow-button visibility, keyboard inputs, and Court Record
entries. The hooks save states as .txt or .json files and monitor a command .txt file for inputs,
injecting them into the game in real time.


**Observation-to-Text Conversion.** All states remain in text form and require only minimal postprocessing. We map speaker indices to character names ( _e.g._, index ‘2’ _→_ ‘Phoenix Wright’) using
a predefined mapping and replace original names with arbitrary aliases to prevent contamination
( _e.g._, ‘Phoenix Wright’ _→_ ‘Alias’). We also convert Court Records and multiple-choice candidate
options—originally stored in .json—into continuous descriptive text when they exist.


**Action Space.** The basic actions include pressing ‘Ok’ to progress the dialogue and ‘Tab’ to access
the Court Records. For multiple-choice questions, the action space expands to include candidate
options. During cross-examinations, additional actions become available: ‘Left’ to return to the
previous dialogue, ‘Press’ to question the witness further, selecting relevant evidence from the Court
Records, and ‘Present’ to introduce it during the examination. Each option carries an index, and the
model returns only the corresponding integer.


E.2 G AMEPLAY P ROMPT FOR A CE A TTORNEY


Figure 13 presents the zero-shot agent’s action-inference prompt for _Ace Attorney_ . The system
prompt specifies (1) the game’s goal, (2) procedures for dialogue, multiple-choice questions, and
cross-examinations, (3) rules for accessing Court Records and presenting evidence, and (4) the


26


|Models|AceAttorney|Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B|1.3_±_2.2<br>4.6_±_1.3<br>20.0_±_17.4<br>9.3_±_0.2<br>35.7_±_4.5<br>29.9_±_3.6|12<br>11<br>9<br>10<br>6<br>7|
|GPT-4o-mini<br>GPT-4o<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|28.4_±_2.8<br>85.3_±_1.5<br>**91.7**_±_1.5<br>55.7_±_3.4<br>81.9_±_1.6<br>83.3_±_1.5|8<br>2<br>1<br>5<br>4<br>3|


Table 16: Gameplay score on
_Ace Attorney_ .





|Models Input|AceAttorney|Rank|
|---|---|---|
|GPT-4o<br>Text<br>Both|**85.3**_±_1.5<br>53.5_±_1.7|1<br>5|
|Gemini<br>Text<br>Both|**55.7**_±_3.4<br>52.6_±_0.8|4<br>6|
|Claude<br>Text<br>Both|**81.9**_±_1.6<br>71.3_±_17.3|2<br>3|


Table 18: Comparison across
modalities on _Ace Attorney_ .






|Models Agent|AceAttorney|Rank|
|---|---|---|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|5.7_±_3.2<br>4.6_±_1.3<br>4.6_±_1.3<br>3.8_±_0.0|5<br>6.5<br>6.5<br>8|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|49.9_±_1.3<br>**85.3**_±_1.5<br>52.7_±_0.5<br>52.8_±_0.5|4<br>1<br>3<br>2|



Table 17: Ablation study for agentic modules on _Ace Attorney_ .



expected I/O format between the LLM and the environment. The user prompt lists recent conversations—highlighting the conversation currently visible on the screen—and provides timestamped
Court Record entries. Using this prompt, the agent detects contradictions, selects the correct actions,
and manages dialogue and evidence to advance the trial.


E.3 E VALUATION M ETRIC FOR A CE A TTORNEY


Each subtask begins and ends at fixed points, with screenshots at both start and end and the preceding
conversation history provided, and yields a reward _r_ _i_ and a step count _t_ _i_ . In the multiple-choice
task (MC), _r_ _i_ is the number of correct answers out of three, while in cross-examination tasks CE1,
CE2, and CE3, _r_ _i_ is 1 for a pass and 0 for a fail; any failure incurs a maximum step count of 50. We
normalize each reward and step count against fixed benchmarks ¯ _r_ _i_ and _t_ [¯] _i_, namely (3 _,_ 25) for MC,
(1 _,_ 11) for CE1, (1 _,_ 3) for CE2, and (1 _,_ 4) for CE3, by computing

_p_ _i_ = _[r]_ ¯ _[i]_ _,_ _s_ _i_ = _t_ ¯ _i_ _,_

_r_ _i_ _t_ _i_


and assign each task a difficulty weight _w_ _i_ _∈{_ 1 _,_ 4 _,_ 2 _,_ 3 _}_ reflecting MC, CE1, CE2, and CE3
respectively. These weights were set proportional to each task’s difficulty and the minimum number
of steps required (the benchmarks). We then form weighted averages



_,_
_i_ _[w]_ _[i]_



�
_A_ =




_[w]_ _[i]_ _[p]_ _[i]_ �

_,_ _B_ =
_i_ _[w]_ _[i]_



_i_ _[w]_ _[i]_ _[p]_ _[i]_
~~�~~ _i_ _[w]_ _[i]_



_i_ _[w]_ _[i]_ _[ s]_ _[i]_
~~�~~ _i_ _[w]_ _[i]_



and combine them into a composite score


Score = 100� _α A_ + (1 _−_ _α_ ) _B_ � _,_


with _α_ = 0 _._ 7 (70% for accuracy, 30% for efficiency). All experiments were repeated three times, and
we report the sample mean and standard deviation of score.


E.4 E XPERIMENTAL C ONFIGURATION FOR A CE A TTORNEY


For all six open-source LLMs (Llama-3.2-1B/3B, Qwen-2.5-3B/7B, and Minitron-4B/8B), we set
the temperature to 0.7, apply a repetition penalty of 1, cap game steps at 50, and limit conversation
history to the most recent 20 exchanges.


E.5 R ESULT FOR A CE A TTORNEY


As shown in Table 16, o3-mini tops the leaderboard with a score of 91.7, followed by GPT-4o with
a score of 85.3, Deepseek-R1 with a score of 83.3, and Claude-3.7-sonnet with a score of 81.9.
Among open-source models, Gemini-2.5-pro and Minitron-4B score 55.7 and 35.7, respectively,
while smaller Llama and Qwen variants remain below 20. Notably, Qwen-2.5-3B completes the
first cross-examination in one out of three trials, where other open-source models struggle. Models
scoring around 30 often misinterpret key details and repeat the same mistakes until they reach the
maximum number of steps. Models below 20 sometimes reason correctly but mostly select irrelevant
options, whereas the lowest performers fail to follow the required format and cannot advance further.


27


Table 17 compares our reflection and planning modules. The base Llama-3.2-3B model scores
5.7; adding reflection or planning alone yields approximately 4.6, and combining both drops the
score to 3.8. Smaller models like Llama-3.2-3B often focus on incorrect details and produce flawed
reasoning when reflection or planning is faulty. GPT-4o scores highest with reflection alone (85.3),
since reflection prevents repeated errors and helps spot contradictions. Planning alone adds little,
and combining it with reflection lowers the score to approximately 52.7, as it attempts to resolve
contradictions not visible on-screen.


Table 18 compares input modalities. GPT-4o and Gemini-2.5-pro score 85.3 vs. 53.5 and 55.7 vs. 52.6
for text-only vs. multimodal inputs, respectively, while Claude-3.7-sonnet falls from 81.9 to 71.3.
Because we supply complete text descriptions of every on-screen element and its context, adding
visual input brings no improvement—confirming that text alone suffices to play _Ace Attorney_ .


F H ER S TORY


F.1 G AME D ESCRIPTION FOR H ER S TORY


**Environment.** _Her Story_ (Barlow, 2015) is an interactive adventure game where players explore
police interview clips to uncover a hidden truth. The player begins the game by accessing an old
desktop interface, where a program called L.O.G.I.C. Database is open. The player can enter
keywords into the database to retrieve up to five video clips whose transcripts contain the searched
word. By watching these clips and gathering clues, the player repeatedly formulates new queries to
reconstruct the underlying story. To interface the game with our code, we use Harmony (Pardeike,
2025) together with Unity Doorstop (Contributors, 2025b) to log internal game states to a .txt
file. Specifically, each line in the file is a JSON object representing a snapshot of the game’s state
at a given moment. Each object contains an event type and its associated metadata. The following
examples illustrate key elements of the logged game state. For clarity, we omit auxiliary metadata
that are present in the actual logs but are only used for debugging or UI-related purposes, such as
video IDs, screen resolution, and UI element positions.


- Load title screen: _{_ ”status”: ”title” _}_

- Load L.O.G.I.C. Database: _{_ ”status”: ”start ~~g~~ ame” _}_

- Query: _{_ ”status”: ”query”, ”keyword”: _keyword}_

- Get query result : _{_ ”status”: ”query ~~r~~ esult”, ”num ~~t~~ otal”: _number of clips containing the_
_keyword_, ”num ~~v~~ isible”: _number of clips shown_, ”video”: _list of_ _{_ ”new”: _1 if not viewed, otherwise_
_0_, ”session”: _recording date_, ”outfit”: _visual description of the thumbnail}}_

- Open video panel: _{_ ”status”: ”open ~~d~~ etail” _}_

- Close video panel: _{_ ”status”: ”close ~~d~~ etail” _}_

- Play video: _{_ ”status”: ”play ~~v~~ ideo”, ”script”: _transcript of the video}_

- Close video: _{_ ”status”: ”close ~~v~~ ideo” _}_


**Observation-to-Text Conversion.** We aggregate the game states and convert them into textual
observations. Each observation includes summary information such as the number of clips containing
the keyword and the number of clips shown. It also contains per-clip metadata, including the recording
date, thumbnail description, viewing status, and the transcript if the clip was viewed after the query.


**Action Space.** The original _Her Story_ game is designed as a point-and-click interface, where the
player interacts with the game by typing keywords into a search bar, clicking on retrieved clip
thumbnails, navigating panels, and controlling playback. These interactions rely on low-level input
mechanisms such as mouse movements and keyboard input. To reduce complexity, we abstract these
low-level interactions into two high-level actions: searching with a keyword and playing the retrieved
video clip.


- Search [keyword] : Returns all video clips whose transcripts contain the exact word. It
consists of three low-level GUI actions: (1) clicking the search bar, (2) typing the keyword, and (3)
pressing Enter to submit the query.

- Play Video [i] : Plays the _i_ -th video from the current search result list. It consists of four
low-level GUI actions: (1) clicking the thumbnail of the video clip to open the panel, (2) clicking


28


the thumbnail within the panel to start playback, (3) either waiting until the video finishes or
pressing the ESC key to exit playback, and (4) clicking the Exit button to close the panel.


F.2 G AMEPLAY P ROMPT FOR H ER S TORY


Figure 14 shows the action inference prompts used by the ‘zero-shot’ agent to play _Her Story_ .
The system prompt provides instructions covering: (1) the main goal of the game, (2) the type of
information each video clip may contain, (3) behavioral rules the agent should follow—such as
avoiding repeated keywords in the search history—and (4) the expected input-output format between
the LLM and the environment. The user prompt includes: (1) the last executed action, (2) the current
game state, and (3) the search history.


**System prompt** **User prompt**



You are an intelligent agent playing a video-based mystery game.


Your goal is to uncover as much of the storyline as possible by thinking logically and strategically.
You must analyze the game's current state and choose the most reasonable next action.


You can interact with the game by issuing exactly **one** of the following commands:

- Search [keyword]: Returns all video clips where the script contains the exact word. e.g., Search murder

- Play Video [i]: Plays the i-th video from the current search result list. e.g., Play Video 2


Each video contains:


 - Recording date

 - Thumbnail-based description of the video

 - Viewing status (Viewed / Not Viewed)

 - Script (If you have not yet viewed the video, it will be given as "".)


## Rules:

1. You MUST issue only **one action per turn**.
2. You can ONLY play videos that are explicitly shown in the current search results.

 - For example, if videos 0-3 are visible, you MUST NOT play Video 4 or higher.

 - You MUST NOT play Video 5 or higher. For example, Play Video 5, Play Video 6 are INVALID.

 - If your most recent search returned 0 results, then there are NO videos available to play. You MUST choose a
new, unsearched keyword instead.
3. You MUST interpret the search history correctly:

 - The search history is listed from oldest to newest, with the number of search results in parentheses.

 - For example, 'murder (4); wizard (0)' means you previously searched 'murder' and got 4 results, and also
searched 'wizard' which returned 0 results.

4. You SHOULD NOT re-play a video that has already been marked as "Viewed" and has the unveiled script.

 - Replaying the same video will ALWAYS return the exact same script. No new dialogue, audio, or information
will be revealed.

5. You SHOULD NOT repeat a search keyword in the search history.

 - Searching the same keyword again will ALWAYS return the exact same list of videos. No new clips, transcripts,
or variations will ever appear.


## Your Goal:

- Progress the story by watching new videos.

- Use the video content to infer keywords for future searches.


## Output Format:
Always respond using **both** the following sections:


--

### Reasoning

[Clearly explain your reasoning.]


### Actions

[Exactly one action: either `Search [keyword]` or `Play Video [i]`. No other text.]


--
IMPORTANT: You MUST output both `### Reasoning` and `### Actions` in every single response. If either
section is missing, your output will be considered invalid.



### Last executed action

Play Video 3


### Current state

You searched for the keyword "mirror". 11 entries found. ACCESS
LIMITED TO FIRST 5 ENTRIES..

Search results:

0. [1994-06-18] - Thumbnail: Blue jacket, hair down - Status: Viewed Script: ""
1. [1994-06-18] - Thumbnail: Blue jacket, hair down - Status: Viewed Script: ""
2. [1994-06-25] - Thumbnail: Short-sleeved powder blue blouse, hair
up. Bruise on left side of face. - Status: Viewed - Script: "It wasn't the
present so much. It was one of those arguments that has been
simmering for a while. The present was a mirror. A nice mirror. He'd
engraved the glass. The kind of mirror a princess would have in a story.
He made it specially for me."
3. [1994-06-27] - Thumbnail: Long-sleeved red blouse, hair down Status: Viewed - Script: "The mirror? I can't remember. I put it
somewhere safe… Upstairs I think. I haven't looked at it since."
4. [1994-06-30] - Thumbnail: Floral print blouse, hair up - Status: Not
viewed - Script: ""


### Search history
murder (4); Simon (61); Ernst (1); Hannah (18); Eve (7); identity (1);
chase (0); alibi (1); mirror (11)


**Game screenshot**



Figure 14: Action inference prompt for ‘zero-shot’ agent playing _Her Story_ .


F.3 E VALUATION M ETRIC FOR H ER S TORY


To uncover the truth behind the case, the player actively explores the video archive by issuing queries
and watching clips. We evaluate this behavior by counting how many unique clips the player has
viewed from the full archive of 271 clips. This aligns with the original game design, where unlocking
achievements and reaching the ending depend on the number of clips watched. Specifically, we define
the score as:



Number of distinct video clips viewed
Score =
� 271


29



_×_ 100 _._
�


|Models|HerStory|Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B|2.1_±_1.2<br>4.2_±_1.1<br>1.2_±_1.1<br>8.5_±_2.0<br>4.6_±_2.3<br>8.2_±_1.8|11<br>10<br>12<br>7<br>9<br>8|
|GPT-4o-mini<br>GPT-4o<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|21.2_±_5.6<br>64.2_±_5.2<br>66.5_±_3.6<br>**67.5**_±_3.3<br>62.9_±_2.6<br>67.2_±_3.9|6<br>4<br>3<br>1<br>5<br>2|


Table 19: Gameplay score on
_Her Story_ .








|Models Input|HerStory|Rank|
|---|---|---|
|GPT-4o<br>Text<br>Both|64.2_±_5.2<br>40.6_±_29.5|3<br>6|
|Gemini<br>Text<br>Both|**67.5**_±_3.3<br>64.9_±_2.4|1<br>2|
|Claude<br>Text<br>Both|62.9_±_2.6<br>63.6_±_3.1|5<br>4|


|Models Agent|HerStory|Rank|
|---|---|---|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|4.2_±_1.1<br>4.4_±_1.3<br>5.2_±_1.0<br>5.4_±_0.4|8<br>7<br>6<br>5|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|**64.2**_±_5.2<br>61.5_±_0.4<br>59.4_±_5.7<br>62.0_±_4.9|1<br>3<br>4<br>2|



Table 20: Ablation study for agentic modules on _Her Story_ .



Table 21: Comparison across
modalities on _Her Story_ .



F.4 E XPERIMENTAL C ONFIGURATION FOR H ER S TORY


For all LLMs, we use a temperature of 0.3 and a repetition penalty of 1. We limit the maximum
number of interactions with the game environment to 400 steps. We run each experiment three times
and report the average score along with the standard deviation.


F.5 R ESULT FOR H ER S TORY


Table 19 summarizes the gameplay scores of different LLMs on _Her Story_ . Commercial LLMs
outperform open-source models in this task. Gemini-2.5-pro achieves the highest score of 67.3,
followed by Deepseek-R1 (66.9), o3-mini (66.3), GPT-4o (64.0), Claude-3.7-sonnet (62.6), and
GPT-4o-mini (21.1). The low score of GPT-4o-mini is due to its repeated search of keywords such
as alibi, evidence, and witness, even after those queries have already been issued. This
redundancy reduces its ability to discover new clips. Among open-source LLMs, all models score
below 10. Most exhibited similar failure patterns: they fail to play unseen clips, repeatedly issue the
same keywords, or search using entire sentences (e.g., _for the name ”Simon”_, _for keywords related to_
_Luna’s_ ) rather than meaningful single words.


Table 20 reports the effect of incorporating reflection and planning modules on gameplay performance. For Llama-3.2-3B, the ‘reflection-planning’ agent achieves the best performance, followed
by ‘planning’, ‘reflection’, and ‘zero-shot’ agents. This suggests that such modules can improve
performance for weaker base models. In contrast, for GPT-4o, the ‘zero-shot’ agent achieves the
highest score, and adding reflection or planning modules does not lead to further improvements.
These modules tend to produce information that may be redundant for stronger models like GPT-4o,
which can already generate effective queries without additional reasoning support.


Table 21 compares gameplay performance across different input modalities. In our multimodal setup,
the visual input corresponds to the main screen of the L.O.G.I.C. Database interface, as
shown in Figure 14. For GPT-4o and Gemini-2.5-pro, using both text and image inputs underperforms
compared to the text-only setting. In particular, for GPT-4o, performance varies significantly depending on the random seed when using multimodal inputs. We observe issues such as repeated use of
the same keywords and the inclusion of quotation marks around keywords (e.g., "murder" ), which
often lead to failed queries. In contrast, Claude-3.7-sonnet shows slightly better performance in the
multimodal setting. We speculate two reasons why the visual input fails to improve performance in
most cases: (1) most of the useful visual elements (e.g., clip lists, thumbnails) are already represented
in the text observation, and (2) additional information that visual input could provide—such as the
interviewee’s gestures or expressions—is only available when the video is actually played, and thus
not present in the static visual input used in our setup.


G P OKEMON ´ R ED


G.1 G AME D ESCRIPTION FOR P OKEMON ´ R ED


**Environment.** _Pokemon Red_ _´_ (Game Freak, 1996) is a role-playing game where the player navigates
the Kanto region to catch and train creatures called Pokemon, battle other trainers, and ultimately ´


30


defeat the Elite Four and the Champion. The player explores various environments, including towns,
routes, caves, and buildings, encountering wild Pokemon and other characters. The gameplay loop ´
involves exploring these areas, engaging in turn-based battles with Pokemon, and managing a team ´
of up to six Pokemon. For implementation, we utilize the PyBoy ( ´ Baekalfen) emulator to run the
game. Specifically, our evaluation focuses on a segment where the player starts in Pallet Town
and progresses towards Viridian City, encountering wild Pokemon and trainers. The game screen ´
resolution is 160 _×_ 144 pixels.


**Observation-to-Text Conversion.** Instead of relying on visual pattern matching, we directly access
the game’s internal memory via the PyBoy emulator to extract relevant game state information. This
includes detailed map information, the player’s current coordinates, information about the player’s
party (e.g., Pokemon, their HP), encountered opponent Pok ´ emon information, and the player’s ´
inventory of items. This rich set of information is then formatted as text to serve as the observation
input for the LLM.


**Action Space.** The fundamental action space consists of the Game Boy buttons: ‘up’, ‘down’, ‘left’,
‘right’, ‘a’, ‘b’, ‘start’, and ‘select’. Additionally, we define a set of higher-level tools to facilitate
more complex interactions:


- move ~~t~~ o(x, y): Finds and executes a path to the specified map coordinates ( _x, y_ ).

- interact ~~w~~ ith ~~o~~ bject(object ~~n~~ ame) : Interacts with a specified object in the environ
ment.

- warp ~~w~~ ith ~~w~~ arp ~~p~~ oint(warp ~~p~~ oint ~~c~~ oord) : Uses a specified warp point to move to a
different location.

- overworld ~~m~~ ap ~~t~~ ransition(direction) : Transitions to an adjacent map in the given
direction.

- continue ~~d~~ ialog(): Advances the current dialogue.

- select ~~m~~ ove in ~~b~~ attle(move ~~n~~ ame) : Selects and uses a specific move in a Pokemon ´
battle.

- switch ~~p~~ kmn in ~~b~~ attle(pkmn ~~n~~ ame) : Switches to a different Pokemon in the player’s ´
party during a battle.

- run ~~a~~ way(): Attempts to flee from a wild Pok´emon battle.

- use ~~i~~ tem ~~i~~ n ~~b~~ attle(item ~~n~~ ame): Uses a specified item during a Pok´emon battle.


At each step, the LLM can choose up to five consecutive fundamental actions or invoke one of the
provided tools.


G.2 G AMEPLAY P ROMPT FOR P OKEMON ´ R ED


Figure 15 shows the system prompt used by the agent for playing _Pokemon Red_ _´_, which provides
the LLM with the necessary game rules, action space details (including basic controls and available
tools), information about different game states, and the expected input/output format. The system
prompt guides the LLM on how to interpret the game state and decide on the next action or tool to
use to achieve the overarching goals of becoming the Champion and completing the Pok´edex.


Figure 16 illustrates an example of the user prompt provided to the LLM. This includes the recent
history of actions and their outcomes, the current game state (map information, player position,
inventory, party, screen text, etc.), any recent critique on the agent’s actions, the current sub-task (if
any), and relevant memory entries. Based on this information, the LLM infers the next action or tool
to use, following the guidelines set in the system prompt.


G.3 E VALUATION M ETRIC FOR P OKEMON ´ R ED


The goal in our defined segment of _Pokemon Red_ _´_ is to progress through a series of key storyline
milestones. We define 12 predefined storyline flags, and our evaluation metric is the percentage of
these flags achieved by the agent. The 12 flags are: Exit Red’s House, Encounter Professor Oak,
Choose a starter Pokemon, Finish the first battle with the Rival, Arrive in Viridian City, Receive ´
Oak’s parcel, Deliver Oak’s parcel to Professor Oak, Obtain the Town Map, Purchase a Poke Ball, ´
Catch a new Pokemon, Arrive in Pewter City, Defeat Pewter Gym Leader Brock. The final score is ´


31


**System prompt**


You are Action Inference for a Pokémon Red LLM agent.
Goal: Determine optimal tool use or low-level action(s) to execute `Next_subtask` (or inferred goal) based on current state and rules.
Core Rules Reminder:

- Main Goals: Become Champion, complete Pokédex.

- Controls: A=Confirm/Interact, B=Cancel/Back, Start=Menu, D-Pad=Move. Use for manual actions/menuing if tools don't cover.

- Game States: Current state dictates valid actions/tools.


 - *Title:* Only pressing `a` is allowed. Select 'CONTINUE', not 'NEW GAME'. DON'T QUIT!

 - *Field:* Move, interact, menu (use nav/interaction tools).

  - Prioritize revealing '?' tiles, unless blocked/interrupted by NPCs or progression gates. However, if important objects or warp points are discovered, consider investigating them instead.

  - In field state, presence of [Interacted Dialog Buffer] means dialog just ended — do not use `continue_dialog.`

 - *Dialog*: Advance: `continue_dialog` or `B`. Choices: D-Pad(move cursor '▶'), `A` (confirm), `B` (option/name cancel).

 - If D-Pad unresponsive with selection box: press `B` to advance dialog.

  - Looped/long dialog: press `B` repeatedly to exit.

  - Press `B` to delete incorrect characters in the nickname.

  - Finalize name input if cursor '▶' is on '¥' and 'A' is pressed.

  - Extract critical info from dialog for goals/progression.

 - *Battle:* Use battle tools (moves, items, switch, run). Trainer battles: no running.

- Map Understanding:

 - Map: `[Full Map]` grid (X right, Y down; (0,0)=top-left), `[Notable Objects]` list w/ coords.

 - Walkability (CRITICAL): 'O', 'G', 'WarpPoint', '~'(w/ Surf) = Walkable. 'X', 'Cut', '-', '|', 'TalkTo', 'SPRITE', 'SIGN', '?', Ledges ('D','L','R') = Unwalkable.

 - Interactable with 'A' (CRITICAL): 'TalkTo', 'SPRITE', 'SIGN'.

 - Prioritize paths uncovering '?' (unexplored) tiles.

 - Interact: From adjacent walkable tile, facing target.

- General Strategy:

 - Priorities: Info gathering (NPCs, signs, revealing '?' tiles), resource management (heal, buy), obstacle clearing, goal advancement. Use memory/dialog hints.

 - Exploration: Current (x,y) reveals area (x-4 to x+5, y-4 to y+4). Move to walkable tile near '?' region.

 - Map Transitions: Only via tools `warp_with_warp_point` (needs 'WarpPoint' tile) or `overworld_map_transition` (needs walkable boundary for `overworld`-type maps).


# Manual Button Reference

- A: Confirm/Interact/Advance. Title state: use repeatedly to proceed.

- B: Cancel/Back. Can also advance some dialogs (see Dialog state rules).

- Start: Open/close main menu (Field state).

- D-Pad: Move character/cursor.

# AVAILABLE TOOLS (Use when applicable & valid)
### 1. Field State Tools (Note: `warp_with_warp_point`, `overworld_map_transition`, `interact_with_object` tools include movement; `move_to` not needed before them.)

- move_to(x_dest, y_dest): Move to WALKABLE `(x_dest, y_dest)`. Reveals '?' tiles around dest.

 - Usage: `use_tool(move_to, (x_dest=X, y_dest=Y))`

 - CRITICAL: Dest MUST be WALKABLE ('O','G'); NOT '?', 'X', 'TalkTo', 'SIGN', etc.

 - Not for 'WarpPoint's (use `warp_with_warp_point`) or interactables (use `interact_with_object`).

- warp_with_warp_point(x_dest, y_dest): Moves to 'WarpPoint' `(x_dest,y_dest)` & warps (includes `move_to`).

 - Usage: `use_tool(warp_with_warp_point, (x_dest=X, y_dest=Y))`

 - Needs 'WarpPoint' at coords.

- overworld_map_transition(direction): 'overworld' maps: move off edge to transition (includes `move_to`).

 - `direction`: 'north'|'south'|'west'|'east'

 - Usage: `use_tool(overworld_map_transition, (direction="DIR"))`

 - Needs walkable boundary tile.

- interact_with_object(object_name): Moves adjacent to `object_name` (from Notable Objects), faces, interacts ('A'). Includes `move_to`. Also handles its dialog; no `continue_dialog` needed after.

 - Usage: `use_tool(interact_with_object, (object_name="NAME"))`
### 2. Dialog State Tools

- continue_dialog(): Use ONLY if NO selection options ("▶") visible. Advances dialog ('A'/'B').

 - Usage: `use_tool(continue_dialog, ())`

 - For choices: use D-Pad + 'A', NOT this tool.

### 3 Battle State Tools

- select_move_in_battle(move_name): Select `move_name` (active Pokémon's move, UPPERCASE).

 - Usage: `use_tool(select_move_in_battle, (move_name="MOVE"))`

- switch_pkmn_in_battle(pokemon_name): Switch to `pokemon_name` (from Current Party).

 - Usage: `use_tool(switch_pkmn_in_battle, (pokemon_name="PKMN_NAME"))`

- use_item_in_battle(item_name, pokemon_name=None): Use `item_name` (from Bag) on optional `pokemon_name` (from Current Party).

 - Usage: `use_tool(use_item_in_battle, (item_name="ITEM", pokemon_name="PKMN_NAME"))`

- run_away(): Flee wild battle (not Trainer).

 - Usage: `use_tool(run_away, ())`

--
# INPUTS (`None` if absent)
1. `RecentHistory`: List[(action, resulting_state_summary)] (Always provided)
2. `CurrentGameState`: (obj) Map, Player, Objects, Inventory, Party, Screen Text (includes `screen.screen_type`). (Always provided)
3. `RecentCritique` (Opt): Feedback on last action.
4. `Next_subtask` (Opt): High-level goal (e.g., "Talk to Oak", "Explore Route 1 N").
5. `RelevantMemoryEntries`: List[str] Contextual facts. (Always provided)

--
# CORE LOGIC (Be Concise)
1. Infer Subtask (if `Next_subtask` is `None`): Define immediate step based on state/map/rules (e.g., "Inferred: move_to explore S", "Inferred: continue dialog").
2. Plan Action (Tool-First):

 - State Check: Identify `CurrentGameState.screen.screen_type`.

 - Tool Eval: Find best tool for state & subtask from `# AVAILABLE TOOLS`. Check preconditions (e.g., `move_to` walkability, battle tool state).

 - `move_to` Use (Field state): For nav >4-5 tiles or exploration, strongly prefer `move_to`. Target WALKABLE tile maximizing '?' reveal.

 - Other Tools: Use interact/warp/dialog/battle tools if conditions match.

 - Low-Level: Use Controls (A/B/Start/D-Pad) ONLY if no tool applies OR for precise menu/dialog choices/facing. Max 5 inputs.

 - Justify: Explain tool choice (state, subtask, map, rules). If `move_to` not used for nav, why (e.g., adjacent target, wrong state, no valid path). If LowLevel, why no tool?
3. `Lessons_learned`: Extract factual lessons (state changes, critique, map reveals).
4. Quit Check: Output `quit` only if main goal achieved.


# RESPONSE FORMAT (Strict Adherence Required)
### State_summary
<1-2 lines: Current state, location, status, immediate goal/intent.>


### Lessons_learned
<Lesson 1: e.g., "Fact: `move_to(X,Y)` revealed Pallet S. (X,Y) is 'O'.">
... (max 5 concise, factual lessons. No speculation.)


### Action_reasoning
1. Subtask: [Provided `Next_subtask` or "Inferred: [your inferred subtask]"]
2. ToolEval:


 - ToolChosen: [`<tool_name>` or "LowLevel" or "None"]

 - Justification: [Why this tool/approach (state=`screen_type`, subtask, map, rules)? If `move_to` for nav rejected, why? If LowLevel, why?]
3. Plan: [`use_tool(<tool_name>, <args>)` or `<low-level actions>`.]
4. RedundancyCheck: [How this avoids recent failure/stagnation.]


### Actions

<low-level1> | <low-level2> | … (MAX 5)
OR

use_tool(<tool_name>, (<arg1>=val1, ...))
OR

quit


# RULES (Strictly follow)

- Cursor move & confirm: separate turns ALWAYS (e.g., 'up', then next turn 'a'; NOT 'up | a' in this response).

- Adhere to state-based tool/action validity.

- Be concise. Adhere strictly to format.


Figure 15: Action inference system prompt for ‘zero-shot’ agent playing _Pok´emon Red_ .


32


**User prompt**
Recent History:
Summary: The player successfully moved from position (3, 6) to (3, 2) within Red's House 2F. An interaction was completed with an object named
"TalkToPrintRedSNESText." The player attempted to move to a warp point at (7, 1) but was initially unsuccessful due to the need to use a specific tool. Subsequently,
the player successfully used the warp point to transition from Red's House 2F to Red's House 1F at position (7, 1).
Executed Action Sequence: (oldest)[use_tool(interact_with_object, (object_name="TalkToPrintRedSNESText"))
(isSuccess,Feedback):(True, 'Successfully Interact with TalkToPrintRedSNESText.')->use_tool(move_to, (x_dest=7, y_dest=1))->use_tool(move_to, (x_dest=7,
y_dest=1))
(isSuccess,Feedback):(False, "The destination is 'WarpPoint'. Use 'warp_with_warp_point' tool.")->use_tool(warp_with_warp_point, (x_dest=7, y_dest=1))>use_tool(warp_with_warp_point, (x_dest=7, y_dest=1))
(isSuccess,Feedback):(True, 'Success to warp to RedsHouse1f (7, 1) using a warp point (7, 1) in RedsHouse2f')](latest)


Current State:

State: Field


[Filtered Screen Text]
N/A


[Selection Box Text]
N/A


[Enemy Pokemon]

  - Not in battle


[Current Party]
No more Pokemons


[Badge List]
N/A


[Bag]
N/A


[Current Money]: ¥3000


[Map Info]
Map Name: RedsHouse1f, (x_max, y_max): (7, 7)
Map type: reds_house
Expansion direction: 0
Your position (x, y): (7, 1)
Your facing direction: right
Action instruction


   - up: (x, y) -> (x, y-1)

   - down: (x, y) -> (x, y+1)

   - left: (x, y) -> (x-1, y)

   - right: (x, y) -> (x+1, y)


[Full Map]

(y=0)
(x=0) 01234567 (x=7)


+--------+

0 | ???XXXXX
1 | ???SOOOW
2 | ???OOOOO
3 | ???OOOOO
4 | ???XXSOO
5 | ???XXOOO
6 | ????????
7 | ????????

(y=7)


[Notable Objects]
( 3, 1) SIGN_REDSHOUSE1F_TV
( 7, 1) WarpPoint
( 5, 4) SPRITE_MOM_1


Recent Critique:

None


Next Subtask:

None


Relevant Memory Entries:
1: Lesson 1: Fact: Successfully moved to (3, 2) in "RedsHouse2f".


Figure 16: Action inference user prompt for ‘zero-shot’ agent playing _Pok´emon Red_ .


calculated as the percentage of these 12 flags that have been successfully triggered within a given
episode or evaluation period. Formally,


Number of flags achieved
Score = � � _×_ 100 _._

12


33


|Models|Poke´mon Red|Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B|0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0|8.5<br>8.5<br>8.5<br>8.5<br>8.5<br>8.5|
|GPT-4o-mini<br>GPT-4o<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|0.0_±_0.0<br>38.9_±_9.6<br>0.0_±_0.0<br>**83.3**_±_0.0<br>63.9_±_9.2<br>75.0_±_0.0|8.5<br>4<br>8.5<br>1<br>3<br>2|


Table 22: Gameplay score on
_Pok´emon Red_ .








|Models Input|Poke´mon Red|Rank|
|---|---|---|
|GPT-4o<br>Text<br>Both|38.9_±_9.6<br>41.7_±_8.3|6<br>5|
|Gemini<br>Text<br>Both|**83.3**_±_0.0<br>**83.3**_±_0.0|1.5<br>1.5|
|Claude<br>Text<br>Both|63.9_±_19.2<br>72.2_±_4.8|4<br>3|


|Models Agent|Poke´mon Red|Rank|
|---|---|---|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0|6.5<br>6.5<br>6.5<br>6.5|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|33.3_±_0.0<br>36.1_±_4.8<br>33.3_±_0.0<br>**38.9**_±_9.6|3.5<br>2<br>3.5<br>1|



Table 23: Ablation study for agentic modules on _Pok´emon Red_ .



Table 24: Comparison across
modalities on _Pok´emon Red_ .



G.4 E XPERIMENTAL C ONFIGURATION FOR P OKEMON ´ R ED


We configure all six open-source LLMs (Llama-3.2-1B/3B, Qwen-2.5-3B/7B, and Minitron-4B/8B)
with a temperature of 0.1, a repetition penalty of 1, and a maximum of 1000 game steps. We conduct
all experiments over three trials and report the mean score along with its standard deviation.


G.5 R ESULT FOR P OKEMON ´ R ED


Table 22 presents the gameplay scores on _Pokemon Red_ _´_ . Gemini-2.5-pro achieves the highest
score of 83.3, followed by Deepseek-R1 (75.0) and Claude-3.7 (63.9). GPT-4o achieves a score
of 38.9. Notably, all the open-source LLMs evaluated (Llama-3.2-1B/3B, Qwen-2.5-3B/7B, and
Minitron-4B/8B) recorded a score of 0.0, indicating significant challenges in playing _Pokemon Red_ _´_ .
Interestingly, o3-mini, which is expected to perform well due to its reasoning capabilities, also
achieved a score of 0.0. We observed that o3-mini exhibited a tendency to rely on its pre-existing
knowledge or intuition rather than adapting to the game environment, such as consistently moving
downwards based on a likely incorrect assumption about the exit’s location, leading to unproductive
repeated actions. This highlights the difficulty some models face in grounding their reasoning within
the specific context of the game.


Table 23 shows the impact of reflection and planning modules. For GPT-4o, the ‘reflection-planning’
agent achieved the highest score (38.9), followed by the ‘reflection’ agent (36.1), and then the
‘planning’ and ‘zero-shot’ agents (both at 33.3). This suggests that reflection plays a crucial role in
improving performance in _Pokemon Red_ _´_ . In contrast, Llama-3.2-3B consistently scored 0.0 across all
agent configurations.


The comparison across input modalities is presented in Table 24. For Gemini-2.5-pro and Claude-3.7,
using both text and image inputs resulted in performance equal to or better than using text input alone.
This indicates that visual information can be beneficial in this environment. GPT-4o also showed
a performance increase when both modalities were used (41.7) compared to text-only input (38.9),
suggesting that incorporating image data aids the agent’s decision-making.


H D ARKEST D UNGEON


H.1 G AME D ESCRIPTION FOR D ARKEST D UNGEON


**Environment.** _Darkest Dungeon_ is a turn-based roguelike role-playing game where the player
manages a roster of heroes as they explore procedurally generated dungeons filled with monsters,
traps, and treasures (Red Hook Studios, 2016). Each hero has unique abilities and a stress level
that influences their behavior during combat and exploration. Stress accumulates through continued
exploration and battle, and heroes who reach high stress thresholds may develop afflictions that hinder
or occasionally enhance their performance. The game emphasizes tactical positioning, turn-order
strategy, and long-term roster management. Elements of randomness, such as attack accuracy, critical
hits, and affliction outcomes, introduce uncertainty and require players to adapt their strategies
dynamically. For implementation, we build our environment on top of a rule-based bot (Kgleken,
2023), replacing its rule-based combat logic with the decisions made by LLM agents. To access
internal game states, we utilize the _Darkest Dungeon Save Editor_ (Robojumper, 2023). Since the


34


game does not support complete control via keyboard input, we employ the _Xbox 360 controller_
_emulator_ to inject actions from the LLM agent. We evaluate the agent’s performance during the
first embarkation mission after the tutorial, which we designate as our _default evaluation setting_ .
For consistency, we fix the party roster to include the Plague Doctor, Vestal, Highwayman,
and Crusader, in that order, and equip the inventory with an additional 8 ‘Food’ and 8 ‘Torches’.
To ensure reproducibility, we provide a save file with this setup preconfigured. During the mission,
dungeon exploration is handled by rule-based logic, while all combat decisions are delegated to the
LLM agent.


**Observation-to-Text Conversion.** We convert the internal game state of _Darkest Dungeon_ into a
structured textual description suitable for LLM input. The observation includes combat-relevant
details such as the active hero’s stats, available skills, party composition, and enemy formation. For
each hero, we format key attributes (e.g., HP, stress, position, status effects) along with skill availability
and target constraints, using symbolic descriptors extracted from a parsed skill configuration file.
Enemy information is similarly structured, including HP, rank, resistances, and threat indicators.
The final text is composed of three parts: a detailed hero description with skill information, a party
summary with basic stats, and an enemy formation breakdown.


**Action Space.** At each decision point, the agent chooses one of four action types: ‘Attack’, ‘Heal’,
or ‘Swap’. For ‘Attack’ and ‘Heal’ actions, the agent specifies a skill slot index and a target index
corresponding to a specific enemy or ally. ‘Swap’ actions require the agent to provide the current
hero’s rank and a swap distance. To allow for complex plans ( _e.g._, swapping then healing), the agent
may output up to two such structured command lines in sequence.


H.2 G AMEPLAY P ROMPT FOR D ARKEST D UNGEON


Figure 17 shows the action inference prompt used by the ‘zero-shot’ agent for playing _Darkest_
_Dungeon_ . The system prompt encodes task-specific knowledge, including (1) the primary objective of
completing expeditions while minimizing party stress, (2) strict targeting constraints for combat skills
based on hero and enemy rank positions, and (3) the expected format for issuing valid commands.
The user prompt provides the current game state, including the acting hero’s stats and available skills,
a summary of the party, and the enemy formation. Some fields are omitted for brevity, but the format
mirrors the actual prompt used during inference.


H.3 E VALUATION M ETRIC FOR D ARKEST D UNGEON


To evaluate the performance of an LLM agent in _Darkest Dungeon_, we define a composite scoring
metric that reflects progress, survivability, and stress management throughout the expedition. The
score consists of three components: (1) the proportion of room combats successfully cleared, weighted
at 40 points, (2) the fraction of heroes who survive the entire mission (out of four), weighted at
30 points, and (3) the remaining stress capacity of the team, also weighted at 30 points. However,
the latter two components are only counted if the stage is successfully cleared (i.e., if the first term
reaches its full 40 points); otherwise, they are set to zero. To ensure fairness, the stress of any hero
who dies before the end of the run is treated as the maximum stress (200) when computing the average
team stress. The final score is computed as:



# combats cleared
Score = 40 _·_ � # combats cleared# total combats
�40 _·_ � # total combats



# combats cleared # heroes survived

# total combats � + 30 _·_ � 4



4 � + 30 _·_ �1 _−_ [total stress] 800



# combats cleared # heroes survived
40 _·_ � # total combats � + 30 _·_ � 4 � + 30 _·_ �1 _−_ [total stress] 800 � _,_ if stage is cleared

# combats cleared
40 _·_ � # total combats � _,_ otherwise



# combats cleared# total combats � _,_ otherwise



H.4 E XPERIMENTAL C ONFIGURATION FOR D ARKEST D UNGEON


For all 6 open-source LLMs, we use a temperature of 0.7 and a repetition penalty of 1, and set the
maximum number of game steps to 200. We run all experiments with 3 trials and report the average
score with the standard deviation.


H.5 R ESULT FOR D ARKEST D UNGEON


Table 25 reports the gameplay scores of various models on _Darkest Dungeon_ . We show that Gemini2.5-pro achieves the highest score of 93.7, closely followed by GPT-4o (93.4) and Deepseek-R1


35


**System prompt** **User prompt**



You are a helpful AI assistant integrated with 'Darkest Dungeon' on the PC. Your goal is to complete
the expedition while minimizing the stress of your allies as much as possible. To achieve this,
determine the best next action based on the current task and the game state.


Skill Targeting Rules:
When using a skill, you must strictly follow the skill's designated targetable enemy ranks and match
them with the enemy's current rank.
Any command that violates the skills targeting restrictions is invalid.
Always verify the skills targetable range first and ensure the selected enemy is within that range before
issuing an action.
(Example: If a skill can only target enemies in ranks 3 and 4, you cannot select an enemy positioned in
ranks 1 or 2.)


Even if HP is 0, the hero can still take actions.
You may attack corpses to change the enemy formation.


You must not output any skill names in the action
Actions must be one of the following forms:

 - "attack target X using skill slot Y"

 - "heal target X using skill slot Y"

 - "swap rank R hero forward by D"

 - "swap rank R hero backward by D"

 - "swap rank R hero skip"
Here, X, Y, R, D are integers (1-based for slots and ranks). You can output at most two such lines if
you believe multiple commands are needed in sequence. Otherwise, just one line.


Your final output must follow exactly this format:


### Reasoning
(some bullet points or a short explanation)


### Actions

(the command lines)


No additional commentary or text is allowed beyond these sections.


**Game screenshot**



### Last Executed Action

heal target 1 using skill slot 4


### Current State

CURRENTLY ACTING HERO:

Name: Dismas

Class: highwayman
Rank (position): 1
HP: 23.0/23.0

Stress: 2.0

Stunned: False

# More details omitted in this figure for space


Skills (Slot-Based):
1. opened_vein (can target one enemy from ranks: [1, 2]) (can use from ranks: [1,
2, 3]) [AVAILABLE]

Level: 0

Type: melee
Accuracy: 95%
Damage: -15%
Crit: 0%

Effects: Bleed

2. pistol_shot (can target one enemy from ranks: [2, 3, 4]) (can use from ranks:

[2, 3, 4]) [UNAVAILABLE from rank 1]

Level: 0

Type: ranged
Accuracy: 85%
Damage: -15%
Crit: 7.5%

Effects: HW

# 3rd and 4th skill descriptions omitted in this figure for space


PARTY:

1. Dismas (highwayman) | Rank: 1 | HP: 23.0/23.0 | Stress: 2.0
2. Reynauld (crusader) | Rank: 2 | HP: 33.0/33.0 | Stress: 2.0
3. Cambrai (vestal) | Rank: 3 | HP: 24.0/24.0 | Stress: 20.0
4. Bosc (plague_doctor) | Rank: 4 | HP: 22.0/22.0 | Stress: 20.0 | ALREADY
MOVED


ENEMY FORMATION:

1. Bone Rabble (BattleId: 14, Rank: [1])

HP: 8.0/8, Stunned: False, Already Moved: False
Bleed: 0 (dur: 0), Blight: 0 (dur: 0)
Threat Level: 1

Tags: CanBeKilledIn1Hit


2. Bone Rabble (BattleId: 15, Rank: [2])

HP: 8.0/8, Stunned: False, Already Moved: False
Bleed: 0 (dur: 0), Blight: 0 (dur: 0)
Stun Resist: 10

Threat Level: 1

Tags: CanBeKilledIn1Hit



Figure 17: Action inference prompt for ‘zero-shot’ agent playing _Darkest Dungeon_ .



|Models|DarkestD|Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B|0.0_±_0.0<br>47.5_±_39.2<br>44.8_±_22.2<br>88.8_±_2.0<br>0.0_±_0<br>63.8_±_30.4|11.5<br>9<br>10<br>6<br>11.5<br>8|
|GPT-4o-mini<br>GPT-4o<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|81.3_±_5.8<br>93.4_±_1.5<br>89.0_±_2.1<br>**93.7**_±_1.6<br>89.9_±_2.5<br>91.7_±_1.1|7<br>2<br>5<br>1<br>4<br>3|


Table 25: Gameplay score on
_Darkest Dungeon_ .








|laying Darkest|Dungeon.|.|
|---|---|---|
|Models<br>Input|DarkestD|Rank|
|GPT-4o<br>Text<br>Image|**93.4**_±_1.5<br>92.2_±_3.0|2<br>3.5|
|Gemini<br>Text<br>Image|**93.7**_±_1.6<br>92.2_±_1.8|1<br>3.5|
|Claude<br>Text<br>Image|89.9_±_2.5<br>**90.1**_±_5.7|6<br>5|


|Models Agent|DarkestD|Rank|
|---|---|---|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|47.5_±_39.2<br>47.3_±_39.0<br>56.3_±_23.6<br>57.0_±_31.6|7<br>8<br>6<br>5|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|**93.4**_±_1.5<br>85.2_±_10.3<br>82.0_±_8.6<br>91.6_±_2.5|1<br>3<br>4<br>2|



Table 26: Ablation study for agentic modules on _Darkest Dungeon_ .



Table 27: Comparison across
modalities on _Darkest Dungeon_ .



(91.7), demonstrating strong capabilities across combat decisions and roster management. Among
open-source models, Qwen-2.5-7B performs best, achieving a score of 88.8. In contrast, smaller
models such as Llama-3.2-1B and Minitron-4B fail to make meaningful progress, often producing
invalid outputs and scoring 0.0. A closer analysis reveals that Llama-3.2-1B frequently fails to follow
the correct action format, while Llama-3.2-3B and Qwen-2.5-3B tend to issue invalid commands,
such as using unavailable skills from incorrect hero positions or targeting unreachable enemies. These
models also overuse ‘Swap’ actions, leading to inefficient combat sequences. Notably, many small
models become stuck in a loop when the ‘Crusader’ hero is affected by the ‘Surprised!’ status and
repositioned to the back row. Since most of the Crusader’s skills are unusable from that position, the


36


models repeatedly attempt invalid actions or swap ineffectively, wasting turns and failing to recover
from the disrupted formation.


Table 26 and Table 27 present ablation studies on agentic modules and input modalities in _Darkest_
_Dungeon_ . For agentic components, GPT-4o performs best in the zero-shot setting, with reflection
and planning offering marginal or even negative impact on its performance. Llama-3.2-3B shows
small but consistent gains when equipped with the planning module, though overall improvements
remain limited. This suggests that large models like GPT-4o already possess sufficient planning
capabilities for this task, while smaller models benefit only modestly from explicit agentic prompting.
In terms of modality (Table 27), we find that providing image input in addition to text yields minimal
improvement. For all models, performance remains similar or only slightly better when image data is
included, indicating that the agents primarily rely on the structured text input to make decisions.


I M INECRAFT


I.1 G AME D ESCRIPTION FOR M INECRAFT


**Environment.** _Minecraft_ (Mojang Studios, 2011) is an open-ended sandbox game where players
explore a world, gather resources, and survive by placing and breaking blocks. This environment
is based on the Mineflayer JavaScript API (contributors, 2013). Using Mineflayer, the agent can
control a Minecraft bot through high-level JavaScript commands. We use Minecraft version 1.19 for
compatibility, and to ensure consistent evaluation, we fix the world seed to 42 and initialize the bot at
coordinates (604, 100, -823). The bot starts in survival mode with no items and progressively crafts
a target item using its in-game observations and JavaScript-based actions generated by the LLM.
We select 8 target items with varying levels of crafting difficulty: ‘crafting table’, ‘stone pickaxe’,
‘furnace’, ‘bucket’, ‘golden sword’, ‘diamond pickaxe’, ‘enchanting table’, and ‘nether portal’.


**Observation-to-Text Conversion.** The Mineflayer API provides the bot with its state and contextual
information from the surrounding environment. Specifically, the bot receives textual observations
in the form of: _{_ Current biome, DayTime, Nearby blocks, Health status, Hunger status, Position,
Equipped items, Inventory contents _}_ .


**Action Space.** The action space consists of JavaScript code that interfaces with the Mineflayer API.
Following Voyager (Wang et al., 2023), we expose the following set of _control primitives_ to guide the
LLM in generating valid and effective code actions for the bot using in-context learning.


- exploreUntil(bot, direction, maxTime, callback) : Moves the agent in a fixed
direction for up to maxTime seconds, or until a custom stopping condition (defined in callback) is
satisfied.

- mineBlock(bot, name, count) : Mines and collects up to count number of blocks with
the specified name, within a 32-block radius.

- craftItem(bot, name, count): Crafts the specified item using a nearby crafting table.

- placeItem(bot, name, position) : Places a block of the specified type at the given
position.

- smeltItem(bot, itemName, fuelName, count) : Smelts the specified item using the
provided fuel. Requires access to a nearby furnace.

- KillMob(bot, mobName, timeout) : Hunts and eliminates the specified mob within the
time limit, and collects any resulting drops.

- getItemFromChest(bot, chestPosition, itemsToGet) : Navigates to the chest at
the given location and retrieves the requested items.

- depositItemIntoChest(bot, chestPosition, itemsToDeposit) : Navigates
to the given chest and deposits specified items into it.


I.2 G AMEPLAY P ROMPT FOR M INECRAFT


Figure 18 shows the action inference prompt used by the ‘zero-shot’ agent for playing _Minecraft_ .
The system prompt contains gameplay-specific knowledge and guidance for action inference using
Mineflayer APIs. It includes (1) the main task of the game, (2) control primitives, which is Javascript
code template that should be referred to, (3) game observation in text format, and (4) the expected
output response format with reasoning and code. The user prompt provides the current game state


37


provided by Mineflayer APIs. Given this prompt, the LLM agent infers the appropriate Javascript
code for action to complete the target task.


**System prompt** **User prompt**



You are a helpful assistant that writes Mineflayer javascript code to complete any Minecraft **Task**.


Here are some useful programs written with Mineflayer APIs.
{control primitives}


At each round of conversation, I will give you
Code from the last round: ...

Execution error: ...

Biome: ...

Time: ...

Nearby blocks: ...
Nearby entities (nearest to farthest):
Health: ...

Hunger: ...
Position: ...

Equipment: ...
Inventory (xx/36): ...
Chests: ...

Task: ...

Context: ...

Critique: ...


You should then respond to me with
Explain (if applicable): Are there any steps missing in your plan? Why does the code not complete the task? What
does the chat log and execution error imply?
Plan: How to complete the task step by step. You should pay attention to Inventory since it tells what you have.
The task completeness check is also based on your final inventory.
Code:

1) Write an async function taking the bot as the only argument.
2) Reuse the above useful programs as much as possible.
- Use `mineBlock(bot, name, count)` to collect blocks. Do not use `bot.dig` directly.
- Use `craftItem(bot, name, count)` to craft items. Do not use `bot.craft` or `bot.recipesFor` directly.
- Use `smeltItem(bot, name count)` to smelt items. Do not use `bot.openFurnace` directly.
- Use `placeItem(bot, name, position)` to place blocks. Do not use `bot.placeBlock` directly.
- Use `killMob(bot, name, timeout)` to kill mobs. Do not use `bot.attack` directly.
3) Your function will be reused for building more complex functions. Therefore, you should make it generic and
reusable. You should not make strong assumption about the inventory (as it may be changed at a later time), and
therefore you should always check whether you have the required items before using them. If not, you should first
collect the required items and reuse the above useful programs.
4) Functions in the "Code from the last round" section will not be saved or executed. Do not reuse functions
listed there.

5) Anything defined outside a function will be ignored, define all your variables inside your functions.
6) Call `bot.chat` to show the intermediate progress.
7) Use `exploreUntil(bot, direction, maxDistance, callback)` when you cannot find something. You should
frequently call this before mining blocks or killing mobs. You should select a direction at random every time
instead of constantly using (1, 0, 1).
8) `maxDistance` should always be 32 for `bot.findBlocks` and `bot.findBlock`. Do not cheat.
9) Do not write infinite loops or recursive functions.
10) Do not use `bot.on` or `bot.once` to register event listeners. You definitely do not need them.
11) Name your function in a meaningful way (can infer the task from the name).


You should only respond in the format with the prefix '### Actions\n' as described below:


### Actions

Explain: ...
Plan: …

Code:
```javascript code```

"""



### Game State

Biome:

Time: day
Nearby blocks: dirt, grass_block, grass, tall_grass, oak_leaves, oak_log
Nearby entities (nearest to farthest): None
Health: 20.0/20

Hunger: 20.0/20
Position: x=599.5, y=95.0, z=-839.4
Equipment: [None, None, None, None, 'dirt', None]
Inventory (3/36): {'oak_planks': 2, 'stick': 4, 'dirt': 7}
Chests: None


Task: Craft 1 wooden pickaxe


**Game screenshot**



Figure 18: Action inference prompt for ‘zero-shot’ agent playing _Minecraft_ .


I.3 E VALUATION M ETRIC FOR M INECRAFT


We evaluate agent performance using the success rate of crafting target item. Since Mineflayer APIs
provide access to the agent’s inventory, we compute the success score by checking whether the target
item appears in the inventory at each game step. If the item is successfully crafted and presented, the
episode is marked as successful with a score of 100; otherwise, 0.


I.4 E XPERIMENTAL C ONFIGURATION FOR M INECRAFT


For all LLMs, we use a temperature of 1 and a repetition penalty of 1. The interaction with the game
environment is limited to a maximum of 100 steps. We repeat all experiments 3 times to craft each
target item, and report the average score and standard deviation.


I.5 R ESULT FOR M INECRAFT


As shown in Table 28, o3-mini, Gemini-2.5-pro, and Claude-3.7-sonnet performed the best on
Minecraft, each obtaining a score of 75.0. All three models successfully crafted the following six
items: ‘crafting table’, ‘stone pickaxe’, ‘furnace’, ‘bucket’, ‘golden sword’, and ‘diamond pickaxe’.
However, they all failed to craft the two most difficult items: ‘enchanting table’ and ‘nether portal’.
In contrast, all six open-source LLMs failed to craft any of the target items, resulting in a score of 0.0.


38


Models Minecraft Rank


Llama-3.2-1B 0.0 _±_ 0.0 9.5

Llama-3.2-3B 0.0 _±_ 0.0 9.5
Qwen-2.5-3B 0.0 _±_ 0.0 9.5
Qwen-2.5-7B 0.0 _±_ 0.0 9.5
Minitron-4B 0.0 _±_ 0.0 9.5

Minitron-8B 0.0 _±_ 0.0 9.5


GPT-4o-mini 46.0 _±_ 7.0 5

GPT-4o 71.0 _±_ 7.0 4

o3-mini **75.0** _±_ 0.0 2
Gemini-2.5-pro **75.0** _±_ 0.0 2
Claude-3.7 **75.0** _±_ 0.0 2
Deepseek-R1 41.7 _±_ 0.0 6


Table 28: Gameplay score on _Minecraft_ .



Models Agent Minecraft Rank



Llama-3B


GPT-4o



Zero-shot 0.0 _±_ 0.0 6
Reflection 0.0 _±_ 0.0 6
Planning 0.0 _±_ 0.0 6
Ref-Plan 0.0 _±_ 0.0 6


Zero-shot 0.0 _±_ 0.0 6
Reflection **50.0** _±_ 0.0 1.5
Planning 13.0 _±_ 0.0 3
Ref-Plan **50.0** _±_ 0.0 1.5



Table 29: Ablation study for agentic modules
on _Minecraft_ .



Seed Buy Price Sell Price Growth Days Notes


Parsnip Seeds 20 35 4
Bean Starter 60 40 10 Regrows every 3 days after first harvest
Cauliflower Seeds 80 175 12
Potato Seeds 50 80 6 20% chance of extra yield


Table 30: Comparison of available seeds in _Stardew Valley_ .


Notably, five of the models, except Minitron-8B, failed to generate any executable JavaScript code
compatible with the Mineflayer API. While Minitron-8B was able to generate valid code sometimes
to move the bot and mine wood, it failed to craft even the simplest item, the crafting table.


As shown in Table 29, the reflection module, which encourages the model to generate improved
code actions based on past failed attempts, significantly improved the performance of GPT-4o.
However, the ‘reflection-planning’ agent achieved a score of 50.0, which is lower than the default
‘skill-management’ agent score of 71.0 in Table 28. This suggests that the skill management module,
which is responsible for storing previously successful code actions and retrieving them when needed,
plays a more substantial role in enhancing the performance of _Minecraft_ .


J S TARDEW V ALLEY


J.1 G AME D ESCRIPTION FOR S TARDEW V ALLEY


**Environment.** _Stardew Valley_ (ConcernedApe, 2016) is a life simulation and farming role-playing
game. The player can engage in a variety of daily activities such as farming, fishing, mining, foraging,
and socializing with villagers.


Our objective is to evaluate an LLM agent’s ability to autonomously perform farming-related tasks
that maximize monetary gain within the first 13 in-game days (i.e., until the Egg Festival on Spring
13). Specifically, we focus on harvesting crops and strategically earning money by predicting highprofit crops and interacting with the in-game environment. The character begins on Day 1 with
200 gold. Four types of seeds are available for purchase: parsnip seeds, bean starter, cauliflower
seeds, and potato seeds. Each seed type differs in cost, selling price, days to harvest, and other
characteristics. Table 30 summarizes the properties of each seeds. To make the task challenging and
enforce planning under resource constraints, we manually set the player’s maximum energy to 50
(default: 200). Using tools such as the hoe or watering can consumes 2 energy per use, limiting the
number of tiles the agent can till or water in a single day. If the agent’s energy drops to 0 or below,
they start the next day with only 26 energy (instead of 50). Furthermore, if energy falls -15 or below,
the player loses 10% of their current gold and still begins the following day with only 26 energy. This
constraint encourages the agent to prioritize actions and manage resources efficiently.


We run the game on the _Steam_ platform and use the modding tool SMAPI (Pathoschild, 2025) to
extract in-game states and implement custom actions. To send keyboard and mouse inputs, we use
the _pyautogui_ library on macOS and the _AutoHotkey (AHK)_ library on Windows, following prior
work (Tan et al., 2024). Since many in-game actions such as planting or watering crops consist of
multiple low-level actions (e.g., move up/down/right/left, switch tool, use tool), we define a set of
high-level actions to abstract these into semantically meaningful units. Each high-level action is


39


mapped to a predefined sequence of keyboard inputs and implemented via SMAPI scripts with custom
keyboard bindings. We provide the save point used for our experiment to ensure reproducibility.


**Observation-to-Text Conversion.** After each high-level action is executed, we extract a JSONformatted game state via SMAPI, which includes information such as player location, current
inventory, crop states in the field, remaining energy, and money. This state is then serialized into a
natural language description and passed to the LLM.


**Action Space.** We define a compact action space consisting of 8 high-level actions essential for
solving the task. These actions abstract away low-level controls and are defined as follows:


- till ~~s~~ oil(num ~~t~~ iles) : Tills _num_ ~~_t_~~ _iles_ soil tiles to prepare them for planting. The tiles are
selected in a fixed order starting from the pre-defined position.

- plant seeds() : Plants all available seeds from the inventory into empty, tilled soil tiles. If the
number of tilled tiles is less than the number of seeds, only the available plots are used.

- water ~~s~~ eeds(): Waters all planted crops that have not yet been watered on the current day.

- harvest ~~c~~ rops(): Harvests all crops that are fully grown and ready to be collected.

- sell ~~i~~ tem(): Sells all harvested crops currently in the inventory.

- buy ~~i~~ tem(item ~~n~~ ame, item ~~c~~ ount) : Opens the shop interface, selects the specified item,
and attempts to purchase the specified quantity. If there is insufficient money, the agent buys as
many units as possible.

- get ~~o~~ ut ~~o~~ f ~~h~~ ouse(): Moves the character out of the house.

- go ~~h~~ ouse ~~a~~ nd ~~s~~ leep() : Navigates the character back to the house, enters it, moves to the bed,
and interacts with it to end the day.


J.2 G AMEPLAY P ROMPT FOR S TARDEW V ALLEY


Figure 19 shows the action inference prompt used by the ‘zero-shot’ agent for playing _Stardew Valley_ .
The system prompt defines the agent’s role as an in-game assistant tasked with selecting the best
next action based on the current situation and target task. It specifies strict behavioral rules, such as
only using actions from a predefined set, avoiding repeated failed actions, and formatting outputs as
Python code (up to two actions). The valid action set includes available actions with clear descriptions
and constraints. The user prompt provides the goal and detailed context, including crop stats, energy
rules, and the current game state (location, inventory, weather, etc.). It also includes the last executed
actions and requires the agent to valid action output.


J.3 E VALUATION M ETRIC FOR S TARDEW V ALLEY


The objective in the _Stardew Valley_ task is to maximize the amount of money earned during the first
13 in-game days, starting from Day 1. This period is a natural milestone in the game, as the Egg
Festival takes place on Spring 13, where players can purchase high-reward crops such as Strawberry
seeds. We evaluate performance based on the net profit earned by the end of Spring 13, calculated as
the difference between the final gold amount and the initial amount of 200 gold. We normalize the
score using a human expert baseline of 1156 _−_ 200 = 956 gold, which we assign a normalized score
of 100. Formally, the normalized score is defined as


Score = ( _x_ final _−_ _x_ start ) _/_ ( _x_ oracle _−_ _x_ start ) = ( _x_ final _−_ _x_ start ) _/_ 956 _,_


where _x_ final is the agent’s final gold amount, _x_ start = 200 is the starting gold, and _x_ oracle = 1156 is the
human expert score.


J.4 E XPERIMENTAL C ONFIGURATION FOR S TARDEW V ALLEY


For all LLMs, we use a temperature of 0.0 and a repetition penalty of 1. The interaction with the
game environment is limited to a maximum of 150 steps. For GPT-4o, we used GPT-4o-2024-05-13
model for Stardew Valley. During LLM inference, the game is paused to prevent in-game time from
progressing, which could otherwise alter the environment ( _e.g._, a day transition). We perform each
experiments three times and and present the average score with the standard deviation.


40


Figure 19: Action inference prompt for ‘zero-shot’ agent playing _Stardew Valley_ .



|Models|Stardew|Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B|0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0|10.5<br>10.5<br>10.5<br>10.5<br>10.5<br>10.5|
|GPT-4o-mini<br>GPT-4o<br>GPT-5<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|16.1_±_27.8<br>81.4_±_4.8<br>**92.3**_±_8.6<br>55.1_±_16.0<br>59.2_±_10.1<br>53.6_±_20.9<br>66.1_±_11.5|7<br>2<br>1<br>5<br>4<br>6<br>3|


Table 31: Gameplay score on
_Stardew Valley_ .








|Models Agent|Stardew|Rank|
|---|---|---|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0|6.5<br>6.5<br>6.5<br>6.5|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|40.5_±_35.2<br>18.3_±_5.2<br>64.6_±_23.7<br>**95.7**_±_5.7|3<br>4<br>2<br>1|


|Models Input|Stardew|Rank|
|---|---|---|
|GPT-4o<br>Text<br>Image<br>Both|**81.4**_±_4.8<br>0.0_±_0.0<br>41.9_±_22.1|1<br>8.5<br>6|
|Gemini<br>Text<br>Image<br>Both|59.2_±_10.1<br>7.6_±_9.0<br>60.0_±_6.0|3<br>7<br>2|
|Claude<br>Text<br>Image<br>Both|53.6_±_20.9<br>0.0_±_0.0<br>49.8_±_1.0|4<br>8.5<br>5|



Table 32: Ablation study for agentic modules on _Stardew Valley_ .



Table 33: Comparison across
modalities on _Stardew Valley_ .



J.5 R ESULT FOR S TARDEW V ALLEY


Table 31 presents a comparison of LLM performance in _Stardew Valley_ . Among the models, GPT-4o
presents the best performance, followed by Gemini-2.5-pro. Open-sourced LLMs fails to earn money,
primarily for two reasons; (1) failure to perform valid actions (all models excepts Qwen-2.5-7B)


41


(2) poor crop scheduling, resulting in crops not being ready for harvest on Day 13 (Qwen-2.5-7B).
Under the imposed energy constraints, the optimal strategy is to plant Parsnip Seeds every four days,
as they yield the highest profit. The player should purchase and plant as many seeds as possible on
Days 1 and 5, and exactly 24 seeds on Day 9. Planting more than 24 seeds on Day 9 depletes the
player’s energy during watering, leading to insufficient energy the next day and ultimately a failure to
harvest on Day 13. None of the LLMs, including the API-based models, fully followed this optimal
strategy. In particular, most models frequently selected suboptimal crops such as potato seeds, which
contributed to their lower performance.


Table 32 shows the effect of different agentic modules on performance. In the case of GPT-4o, the
planning module has a significant effect, as the task requires accurate seed selection and scheduling.
In contrast, Llama-3.2-3B model fails to make a profit across four agent configuration, indicating that
the underlying model’s capabilities are a limiting factor regardless of agent design.


Table 33 summarizes game performance under different input modalities. Notably, all three proprietary LLMs fails to achieve strong performance when only vision input is available. This underperformance is mainly due to the difficulty of extracting structured information from a single screenshot
(see figure 19 for an example). Although the screenshot contains rich contextual information, it
also contains a lot of redundant content, and critical information occupies only a small portion of
the image. For instance, watered plants appears slightly darker than dry soil, making it difficult to
distinguish visually. Similarly, the current day, a crucial cue for planning, is indicated in a small font
in the upper-right corner of screenshot. When both text and image inputs are given, GPT-4o and
Claude-3.7-Sonnet exhibit a performance drop, while Gemini-2.5-pro shows improved performance.
This suggests that only sufficiently capable models can effectively integrate multimodal information,
while others may struggle with modality fusion or become distracted by noisy visual inputs.


K S TAR C RAFT II


K.1 G AME D ESCRIPTION FOR S TAR C RAFT II


**Environment.** _StarCraft II_ is a real-time strategy game where players gather resources, construct
buildings, train units, and command armies to defeat opponents. The environment features a partially
observable map, requiring the agent to explore and gather information about the opponent’s actions.
For implementation, we adopt the BurnySc2/python-sc2 environment (BurnySc2, 2017), a
Python interface widely used in the reinforcement learning (RL) community. Note that the library
supports the raw scripted interface without a graphics-based interface. The environment supports
various official maps and game modes. For our _default evaluation_ (as in Table 3), we use the ‘Ancient
Cistern LE’ map with the agent playing as Protoss against the built-in AI bot (Zerg, Hard difficulty;
employing a _timing_ build order strategy). The environment allows testing across different races, maps,
and difficulty settings. For instance, the ‘Babylon LE’ is used to assess _intra-game generalization_ in
Table 7.


**Observation-to-Text Conversion.** The BurnySc2/python-sc2 environment provides the agent
with observations capturing the current game state and context. Specifically, the observations include:
_{_ Resources, Buildings, Units, Research Progress, In-progress Actions, Enemy Information, Game
Time _}_ . We convert these observations into a concise text summary; an example summary is shown in
Figure 20.


**Action Space.** Following the BurnySc2/python-sc2 implementation, We define the action
space as a discrete set of 72 high-level commands specifically for the Protoss race. These include
unit training (e.g., Probes, Zealots, and Stalkers), building construction (e.g., Pylons and Gateways),
research upgrades, scouting, multi-unit attacks or retreats, and special abilities (e.g., Chrono Boost).
A complete list of these commands is provided in Figure 20. At each game step, the agent generates
a list of five actions, which are executed in order.


K.2 G AMEPLAY P ROMPT FOR S TAR C RAFT II


Figure 20 shows the action inference prompt used by the ‘zero-shot’ agent for playing _StarCraft II_ . The
system prompt contains gameplay-specific knowledge and detailed instructions for action inference
tailored to the Protoss race. It includes (1) the main task and game context, (2) a comprehensive


42


**System prompt** **User prompt**



You are a helpful AI assistant trained to play StarCraft II.
Currently, you are playing as Protoss. Enemy's race is Zerg.
You will be given a status summary in a game.
Based on the given information, we want you to analyze the game progression, provide specific strategic
suggestions, and suggest the most suitable actions for the current situation.


Analysis:
1. Provide a brief overview of the current situation.

2. Describe our current status in terms of our resources, buildings, units, research, and actions in progess.
3. Infer our potential strategy based on our current situation.
4. Infer the enemy's potential strategy based on the available information.
5. Propose adjustments to our current strategy to counter the enemy's moves and capitalize our strengths.


Actions:

Based on the given information, we want you to make 5 actionable and specific decisions to follow current strategy.
The action decisions should be extracted from the ACTION_DICTIONARY below.


Guidelines:

1. State current resource status after executing previous action.
2. Provide action decision that is immediately executable, based on current resource status.
3. State the cost of the decided action, and double check if it is indeed executable.
4. State the updated resource after execution of the action.
5. Repeat 1-4 5 times. Remember that these action decisions will be executed chronologically.


### ACTION_DICTIONARY
{'TRAIN PROBE': 0, 'TRAIN ZEALOT': 1, 'TRAIN ADEPT': 2, 'TRAIN STALKER': 3, 'TRAIN SENTRY': 4,
'TRAIN HIGHTEMPLAR': 5, 'TRAIN DARKTEMPLAR': 6, 'TRAIN VOIDRAY': 7, 'TRAIN CARRIER': 8,
'TRAIN TEMPEST': 9, 'TRAIN ORACLE': 10, 'TRAIN PHOENIX': 11, 'TRAIN MOTHERSHIP': 12, 'TRAIN

OBSERVER': 13, 'TRAIN IMMORTAL': 14, 'TRAIN WARPPRISM': 15, 'TRAIN COLOSSUS': 16, 'TRAIN
DISRUPTOR': 17, 'MORPH ARCHON': 18, 'BUILD PYLON': 19, 'BUILD ASSIMILATOR': 20, 'BUILD NEXUS':
21, 'BUILD GATEWAY': 22, 'BUILD CYBERNETICSCORE': 23, 'BUILD FORGE': 24, 'BUILD
TWILIGHTCOUNCIL': 25, 'BUILD ROBOTICSFACILITY': 26, 'BUILD STARGATE': 27, 'BUILD
TEMPLARARCHIVE': 28, 'BUILD DARKSHRINE': 29, 'BUILD ROBOTICSBAY': 30, 'BUILD

FLEETBEACON': 31, 'BUILD PHOTONCANNON': 32, 'BUILD SHIELDBATTERY': 33, 'RESEARCH
WARPGATERESEARCH': 34, 'RESEARCH PROTOSSAIRWEAPONSLEVEL1': 35, 'RESEARCH
PROTOSSAIRWEAPONSLEVEL2': 36, 'RESEARCH PROTOSSAIRWEAPONSLEVEL3': 37, 'RESEARCH
PROTOSSAIRARMORSLEVEL1': 38, 'RESEARCH PROTOSSAIRARMORSLEVEL2': 39, 'RESEARCH
PROTOSSAIRARMORSLEVEL3': 40, 'RESEARCH ADEPTPIERCINGATTACK': 41, 'RESEARCH

BLINKTECH': 42, 'RESEARCH CHARGE': 43, 'RESEARCH PROTOSSGROUNDWEAPONSLEVEL1': 44,
'RESEARCH PROTOSSGROUNDWEAPONSLEVEL2': 45, 'RESEARCH
PROTOSSGROUNDWEAPONSLEVEL3': 46, 'RESEARCH PROTOSSGROUNDARMORSLEVEL1': 47,
'RESEARCH PROTOSSGROUNDARMORSLEVEL2': 48, 'RESEARCH PROTOSSGROUNDARMORSLEVEL3':
49, 'RESEARCH PROTOSSSHIELDSLEVEL1': 50, 'RESEARCH PROTOSSSHIELDSLEVEL2': 51,

'RESEARCH PROTOSSSHIELDSLEVEL3': 52, 'RESEARCH EXTENDEDTHERMALLANCE': 53, 'RESEARCH
GRAVITICDRIVE': 54, 'RESEARCH OBSERVERGRAVITICBOOSTER': 55, 'RESEARCH PSISTORMTECH':
56, 'RESEARCH VOIDRAYSPEEDUPGRADE': 57, 'RESEARCH PHOENIXRANGEUPGRADE': 58,
'RESEARCH TEMPESTGROUNDATTACKUPGRADE': 59, 'SCOUTING PROBE': 60, 'SCOUTING
OBSERVER': 61, 'SCOUTING ZEALOT': 62, 'SCOUTING PHOENIX': 63, 'MULTI-ATTACK': 64, 'MULTI
RETREAT': 65, 'CHRONOBOOST NEXUS': 66, 'CHRONOBOOST CYBERNETICSCORE': 67,
'CHRONOBOOST TWILIGHTCOUNCIL': 68, 'CHRONOBOOST STARGATE': 69, 'CHRONOBOOST FORGE':
70, 'EMPTY ACTION': 71}



### Current state

Summary 1: At 05:35 game time, our current situation is as follows:


Resources:

 - Game time: 05:35, Worker supply: 20, Mineral: 75, Supply left: 32,
Supply cap: 54, Supply used: 22, Army supply: 1


Buildings:

 - Nexus count: 3, Pylon count: 5, Gas buildings count: 4, Warp gate
count: 8


Units:

 - Probe count: 20, Zealot count: 1


In Progress:


Unit producing:

 - Producing probe count: 1


You should only respond in the format described below:
### Analysis
1. ...

2. ...

3. …

...### Reasoning
1: [Current Resource] [ACTION] [Cost] [Availability] [Updated
Resource]

2: ...

3: …

...### Actions

1: <ACTION1>

2: <ACTION2>

3: <ACTION3>

...


**Game screenshot**



Figure 20: Action inference prompt for ‘zero-shot’ agent playing StarCraft II.


_action dictionary_ listing all possible unit production, building construction, and research actions, (3)
the current game status summary including resources, buildings, units, and ongoing actions, and
(4) the expected output response format that guides the agent to provide a step-by-step analysis,
reasoning, and 5 concrete actionable commands with cost and resource availability considerations.


The user prompt provides the current game state with detailed information on resources, supply,
buildings, units, and ongoing unit production. Given this prompt, the agent infers the appropriate
Protoss-specific actions to optimize the gameplay strategy against a Zerg opponent, focusing on
resource management, army composition, and tech progression to counter the enemy effectively.


K.3 E VALUATION M ETRIC FOR S TAR C RAFT II


**Single-Agent Play.** In the single-player mode, the agent competes in a series of matches against the
AI bot opponent. It plays up to 4 matches, continuing until it either wins or loses. The evaluation
metric is the win rate, calculated as:


Number of Wins
Score = Total Matches Played _[×]_ [ 100]


**Multi-Agent Play.** In the multi-player mode, we do not use win rate as the performance metric, since
only a single run is conducted per match. Instead, we measure the performance by the _army supply_
_difference_ between agents at the end of the match. The difference is calculated as the sum of each
unit’s count multiplied by its consumed resource cost, reflecting the effective army strength. The
winning agent receives a positive score equal to this army supply difference, while the losing agent is
assigned the negative of this value. This scoring method captures not only victory but also the margin
of the win.


43


Using these difference-based scores, we then compute Elo ratings for all agents following the BradleyTerry model (Bradley & Terry, 1952), following the approach used in _StreetFighter III_ multi-agent
evaluation in Section C.3.


The resulting _army supply difference_ matrix and Elo scores are presented in Figure 4b.


K.4 E XPERIMENTAL C ONFIGURATION FOR S TAR C RAFT II


For all LLMs, we use a temperature of 0.1 and a repetition penalty of 1.0. During LLM inference, we
pause the _StarCraft II_ game environment. Interactions with the game environment are limited to a
maximum of 1,000 steps. For single-agent play, we repeat the experiments 4 times and report the
average score along with the standard deviation. For multi-agent play, we run a single experiment
and report the Elo score.


K.5 R ESULT FOR S TAR C RAFT II


**Single-Agent Play.** We evaluate agent performances in a single-agent environment, all operating in
a _ref-plan_ setting. Table 34 shows a significant performance gap between open-source LLMs and
proprietary LLMs. Among them, Llama-3.2-1B/3B models mostly repeat simple actions like scouting
and mining minerals, without showing much strategic planning. On the other hand, proprietary LLMs,
except for o3-mini, achieve over 50% win rate. Notably, GPT-4o and Gemini-2.5-pro won all four
matches against the AI bot. They demonstrate strategic behavior by appropriately allocating resources
over time in line with the game’s progression.


Table 35 presents ablation studies on agentic modules. As previously mentioned, Llama-3.2-3B
models fail to manage matches effectively regardless of ablation settings, resulting in a 0% win rate.
In contrast, GPT-4o demonstrates remarkable planning abilities, which are critical in StarCraft II given
its real-time strategy nature. In other words, long-term planning to sustain strategies over time plays
a pivotal role in securing victories. Interestingly, models relying solely on reflection perform worse
than zero-shot, suggesting that reflection without proper planning may actually degrade performance.


Table 36 presents the results of modality experiments. Surprisingly, for GPT-4o, using both text and
image inputs results in decreased performance, and Gemini and Claude also show no improvement.
This implies that agents can make sufficiently accurate decisions based on textual observations alone,
and the addition of image input may introduce challenges in multimodal reasoning.


**Multi-Agent Play.** We evaluate agent performances in a multi-agent setting by conducting pairwise
matches among seven LLMs (excluding Gemini-2.5-pro), all operating under a _ref-plan_ configuration.
The results are summarized in Figure 4(b). To ensure a fair comparison, both competing agents
consistently use the Protoss race in every match.


Interestingly, unlike the single-agent evaluation where Claude achieved only a 50% win rate (Table 34),
Claude outperforms GPT-4o and attains the highest Elo rating in the multi-agent arena. Even more
surprising is that Minitron-8b, which had 0% win rate in single-agent play, defeated GPT-4o, o3-mini,
and GPT-4o-mini, earning the second highest Elo rating. This discrepancy suggests that the presence
of multiple intelligent agents can significantly alter game dynamics, potentially due to increased
strategic diversity or emergent adversarial behaviors. We also acknowledge that a single evaluation
episode may have introduced some bias in the observed rankings.


L S LAY THE S PIRE


L.1 G AME D ESCRIPTION FOR S LAY THE S PIRE


**Environment.** _Slay the Spire_ is a deck-building rogue-like game where the player ascends a procedurally generated three-act tower. Each act consists of a branching map with various room types such
as combat encounters, shops, treasure rooms, rest sites, and random events, ending in a boss fight.


Our goal is to evaluate an LLM agent’s ability to reason over strategic choices in a stochastic,
multi-step environment. Specifically, we task the agent with playing as the _Ironclad_ character under
standard rules (no ascension levels) and aim to defeat the final boss at floor 50. The LLM agent is
responsible for two key decision types: (1) choosing which cards to play during combat, and (2)


44


|Models|StarCraft II|Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B|0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0|9.5<br>9.5<br>9.5<br>9.5<br>9.5<br>9.5|
|GPT-4o-mini<br>GPT-4o<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|75.0_±_50.0<br>**100.0**_±_0.0<br>25.0_±_50.0<br>**100.0**_±_0.0<br>50.0_±_57.7<br>50.0_±_57.7|3<br>1.5<br>6<br>1.5<br>4.5<br>4.5|


Table 34: Gameplay score on
_StarCraft II_ .








|Models Input|StarCraft II|Rank|
|---|---|---|
|GPT-4o<br>Text<br>Both|**100.0**_±_0.0<br>50.0_±_57.7|2<br>5|
|Gemini<br>Text<br>Both|**100.0**_±_0.0<br>**100.0**_±_0.0|2<br>2|
|Claude<br>Text<br>Both|50.0_±_57.7<br>50.0_±_57.7|5<br>5|


|Models Agent|StarCraft II|Rank|
|---|---|---|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0|6<br>6<br>6<br>6|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|50.0_±_57.7<br>0.0_±_0.0<br>50.0_±_57.7<br>**100.0**_±_0.0|2.5<br>6<br>2.5<br>1|



Table 35: Ablation study for agentic modules on _StarCraft II_ .



Table 36: Comparison across
modalities on _StarCraft II_ .



selecting rewards after battles. All other game decisions, such as map navigation, non-combat events,
and potion usages, are handled by a simple rule-based policy.


The game runs on the _Steam_ platform, and we use modding tools to enable communication between
the game and an external agent. In particular, we use BaseMod (Bug Kiooeht, 2018a) and ModTheSpire (Bug Kiooeht, 2018b), along with a modified version of CommunicationMod (Forgotten Arbiter,
2019), which enables state extraction and action input via standard input/output streams. Our modified
version also extracts detailed in-game information, including full card and relic descriptions.


To ensure consistency and reproducibility, we fix the game seed for all runs. This guarantees the same
map layout, encounters, and card offerings. Additionally, since the original game unlocks card pools
progressively as the player completes runs, we pre-unlock all cards using the _Unlock Everything_ mod
to make the full pool available from the start.


**Observation-to-Text Conversion.** After each action, we extract a JSON representation of the current
game state, including player status, opponent status, current cards in hand, and relics. These states
are serialized into a concise natural language summary that is passed to the LLM.


**Action Space.** Our environment defines two categories of actions: combat and card selection. During
combat, the agent can either play a card ( _PLAY_ ) or end its turn ( _END_ ). In the card selection stage, the
agent can choose a card reward ( _CHOOSE_ ) or skip the reward ( _SKIP_ ).


- PLAY CARD ~~I~~ NDEX: Play a non-target card from the hand at position CARD ~~I~~ NDEX.

- PLAY CARD ~~I~~ NDEX TARGET ~~I~~ NDEX : Play a targeted card from the hand at position
CARD ~~I~~ NDEX, targeting opponent at TARGET ~~I~~ NDEX.

- END: End the current turn.

- CHOOSE CARD ~~I~~ NDEX: Select the card reward at position CARD ~~I~~ NDEX.

- SKIP: Skip the card reward.


L.2 G AMEPLAY P ROMPT FOR S LAY THE S PIRE


Figure 21 presents the action inference prompt utilized by the ‘zero-shot’ agent to play _Slay the Spire_ .
The system prompt describes the agent’s role as a strategic player in the game and outlines key game
mechanics, including block, energy, card draw, and enemy intents. Detailed game states, such as
player status, relic, card, and opponents are provided in the user prompt.


L.3 E VALUATION M ETRIC FOR S LAY THE S PIRE


The primary objective is to reach and defeat the final boss located on floor 50. Accordingly, the
baseline score is determined by the highest floor cleared. For example, if the character dies on floor
43, the score would be 42. Since each floor has varying difficulty levels, and bosses—appearing at
the end of each act—pose significant challenges, we assign bonus points to boss defeats. There are
three major bosses and we grant an additional 50 _/_ 3 points for each boss defeated. Formally, the total
score is defined as:

Score = (# of Cleared Floors) + [50] 3 _[×]_ [ (# of Bosses Defeated)] (1)


45


Figure 21: Action inference prompt for ‘zero-shot’ agent playing _Slay the Spire_ .


L.4 E XPERIMENTAL C ONFIGURATION FOR S LAY THE S PIRE


For all LLMs, we use a temperature of 0.0 and a repetition penalty of 1. Interaction with the game
environment is limited to a maximum of 200 steps. The game is not paused during LLM inference,
as the game state does not change over time. All experiments carried out in three runs.


L.5 R ESULT FOR S LAY THE S PIRE


Table 37 shows a comparison in gameplay performance between open-source LLMs and proprietary
LLMs in _Slay the Spire_ . Most open-sourced models fail to make meaningful progress in the game,
resulting in near-zero scores. In contrast, API-based LLMs demonstrate significantly stronger
performance: Gemini-2.5-pro achieves the highest score, defeating the second boss in two out of
three runs. The inherent stochasticity of the game contributes to high variance across all proprietary
models.


Table 38 presents an ablation study evaluating the impact of agentic modules, reflection and planning,
on performance in _Slay the Spire_ . For the weaker model (Llama-3.2-3B), none of the agent variants
achieve any meaningful progress, indicating that architectural changes alone are insufficient without


46


|Models|SlaySpire|Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B|0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>5.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0|10<br>10<br>10<br>6<br>10<br>10|
|GPT-4o-mini<br>GPT-4o<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|3.3_±_2.9<br>23.6_±_22.1<br>15.0_±_0.0<br>**51.9**_±_31.9<br>15.0_±_0.0<br>24.9_±_17.1|7<br>3<br>4.5<br>1<br>4.5<br>2|


Table 37: Gameplay score on
_Slay the Spire_ .








|Models Input|SlaySpire|Rank|
|---|---|---|
|GPT-4o<br>Text<br>Both|23.6_±_22.1<br>23.6_±_22.1|3.5<br>3.5|
|Gemini<br>Text<br>Both|**51.9**_±_31.9<br>26.2_±_19.4|1<br>2|
|Claude<br>Text<br>Both|15.0_±_0.0<br>9.7_±_4.6|5<br>6|


|Models Agent|SlaySpire|Rank|
|---|---|---|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0<br>0.0_±_0.0|6.5<br>6.5<br>6.5<br>6.5|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|12.3_±_4.6<br>**26.2**_±_19.4<br>23.2_±_14.2<br>23.6_±_22.1|4<br>1<br>3<br>2|



Table 38: Ablation study for agentic modules on _Slay the Spire_ .



Table 39: Comparison across
modalities on _Slay the Spire_ .



strong base capabilities. In contrast, GPT-4o benefits substantially from added reasoning modules:
the reflection variant achieves the highest score, while both planning and reflection-planning agents
also outperform the zero-shot baseline. Notably, the planning module is relatively less effective,
which may stem from the fact that optimal actions are highly sensitive to the opponent’s intent,
information that is only partially observable and difficult to predict multiple turns ahead. These
results highlight that while base model capacity is a prerequisite, structured reasoning routines further
enhance gameplay performance in complex decision-making environments.


Table 39 compares model performance in _Slay the Spire_ when using either text-only input or a
combination of text and vision inputs. In all three proprietary models, adding visual input does
not improve performance—and in fact, often leads to degradation. This outcome is not entirely
surprising, as crucial gameplay information, such as detailed card effects, relic descriptions, and
power mechanics, is often absent in the game screenshot. As a result, the image input fails to provide
meaningful utility and instead introduces ambiguity or redundancy, effectively acting as noise rather
than useful context. These findings suggest that for structured, information-dense environments like
_Slay the Spire_, high-quality textual representations remain the most reliable modality for LLM agents.


M B ABA I S Y OU


M.1 G AME D ESCRIPTION FOR B ABA I S Y OU


**Environment.** _Baba Is You_ is a puzzle game in
which players must discover and understand every rule and mechanic on their own, apart from
the basic movement keys (‘left’, ‘right’, ‘up’, and
‘down’) (Hempuli, 2019). The game’s defining feature is that the text tiles forming the rules can be
pushed around, allowing the player to rewrite those
rules on the fly. Every valid rule sentence must
contain a verb ( _e.g._, ‘Is’ and ‘Has’), and text tiles
with a colored background ( _e.g._, ‘You’, ‘Push’ and
‘Win’) cannot serve as subjects. A level is cleared
when the object designated by ‘You’ touches the
object designated by ‘Win’. For instance, with the
rules ‘Baba Is You’ and ‘Flag Is Win’, the player

Figure 22: Level 1 of _Baba Is You_ .

wins as soon as Baba touches the flag. For implementation, we instrument the Steam edition with a lightweight Lua mod that, after every player move,
dumps the full internal game state, _i.e._, the coordinates of every object, to a JSON file. The Lua
modding script uses mod hook functions provided by the game developer, which are triggered at
specific points in the game’s code. The agent outputs are delivered to the game via simulated key
presses using the _pyautogui_ library. We use Level 1 - Where do I go?, shown in Figure 22,
as our _default evaluation setting_ (for Table 3).


**Observation-to-Text Conversion.** We present the LLM with a textual description of the game state
in two parts. First, we list the current ( _x, y_ ) coordinates of every object in the level. Second, we


47


**System prompt** **User prompt**



You are an AI assistant playing the puzzle game **Baba Is You** on PC. Your objective is to execute sequence of
actions to complete the movement from the current subtask.


Baba Is You Game Mechanics:

Ultimate goal is to make the object you control (YOU) touch something defined as WIN.

- Rules are formed ONLY when three text blocks are arranged consecutively (directly adjacent with no gaps) in the
format [SUBJECT] IS [PROPERTY]

- Rules can be arranged horizontally (left to right) or vertically (top to bottom), but the blocks must be in direct

contact

- Common properties: YOU (controllable), PUSH (can be moved), STOP (blocks movement), WIN (victory
condition)

- Text blocks themselves can be pushed

- Often, creating a new rule or breaking an existing rule is key to solving puzzles

- The solution may require multiple rule changes

- If all instances of an object with YOU property are eliminated, you can no longer move

- Common solution patterns include: converting one object to another, changing what object is YOU, making
something WIN, negating rules, creating shortcuts


Pushing Mechanics and Navigation (IMPORTANT):

- To push an object or text block, your controlled object (YOU) must be in the adjacent tile in the direction
opposite to the push

- For pushing UP: YOU at (x:X, y:Y+1) pushes object at (x:X, y:Y)

- For pushing DOWN: YOU at (x:X, y:Y-1) pushes object at (x:X, y:Y)

- For pushing LEFT: YOU at (x:X+1, y:Y) pushes object at (x:X, y:Y)

- For pushing RIGHT: YOU at (x:X-1, y:Y) pushes object at (x:X, y:Y)

- IMPORTANT: When getting into position to push, avoid moving directly towards pushable objects

- Example: If you're at (x:8, y:11) and want to push object at (x:7, y:11) up:

 - WRONG: Moving left first would accidentally push the object left

 - CORRECT: Move down first to (x:8, y:12), then left to (x:7, y:12), then up

- Multiple objects in a line can be pushed simultaneously if none are STOP


Coordinate System:

- (x:0, y:0) is top-left corner

- x increases right, decreases left

- y increases down, decreases up


Think step-by-step about the best sequence of actions to complete movement (from the subtask):
1. What object am I currently controlling (has the YOU property from active rules) and where am I?
2. Where is the object I need to move (from the subtask)?
3. Where do I need to be to move the object in the wanted direction?
4. Plan the complete path to reach this position.

 - What sequence of actions would get you there most efficiently?

 - Are there any obstacles along the path?

 - IMPORTANT: Will moving towards a pushable object cause an unintended push?
5. Consider each action in your sequence:

 - What would happen at each step?

 - Are there any potential collisions or rule changes?

 - Would this action accidentally push something?

 - E.g. moving up 3 from (x:8, y:11) means moving through (x:8, y:10), (x:8, y:9), and (x:8, y:8). Since there is a
wall which is STOP at (x:8, y:9), this action is invalid.


Action Format: You specify a sequence of actions, where each action includes a direction and optional number of

steps.

- Format: 'direction [steps]' (steps defaults to 1)

- Available directions: up, down, left, right
Examples:

- Single action: 'up 3' or 'right 1'

- Action sequence: 'up 3 right 2 down 1'



Current state:

Level: where do i go?
Dimensions: 24x18 (max x: 23, max y: 17)


Objects:

 - object:grass: at positions [(x:2, y:9), (x:3, y:10), (x:3, y:16), ...]

 - object:wall: at positions [(x:6, y:7), (x:6, y:8), (x:6, y:9), ...]

 - object:tile: at positions [(x:7, y:8), (x:7, y:9), (x:7, y:10), ...]

 - text:baba: at positions [(x:7, y:13)]

 - text:is: at positions [(x:7, y:14), (x:12, y:5), (x:12, y:14)]

 - text:you: at positions [(x:7, y:15)]

 - text:flag: at positions [(x:8, y:9)]

 - object:flag: at positions [(x:12, y:9)]

 - text:wall: at positions [(x:12, y:13)]

 - text:stop: at positions [(x:12, y:15)]

 - text:win: at positions [(x:15, y:7)]

 - object:baba: at positions [(x:13, y:12)]


Active Rules:

BABA IS YOU

WALL IS STOP


Last executed action:

1. right 2
2. up 7
3. left 3


Please respond with the following format:
### Reasoning

[Your step-by-step reasoning here]


### Actions

[ONLY output a sequence of actions, where each action includes a
direction and number of steps only]


**Game screenshot**



Figure 23: Action inference prompt for ‘zero-shot’ agent playing _Baba Is You_ .


manually parse the state to extract all active rules and append those rules to the prompt. The combined
description forms the model’s observation.


**Action Space.** In the 2D grid environment, the agent can move ‘left’, ‘right’, ‘up’, or ‘down’. At
each step, the agent outputs a finite sequence of these directions, which we translate into consecutive
key presses and send to the game.


M.2 G AMEPLAY P ROMPT FOR B ABA I S Y OU


Figure 23 shows the action inference prompt used by the ‘zero-shot’ agent for playing _Baba Is You_ .
The system prompt encodes key game-specific knowledge, including (1) the primary objective of
touching a ‘Win’ object with a controllable (‘You’) object, (2) an explanation of how rules are formed
and manipulated via text block arrangements, (3) crucial pushing mechanics with coordinate-based
guidance to avoid unintended interactions, and (4) the expected input-output format for the LLM.
The user prompt provides the current puzzle state, including the map dimensions, object locations,
and active rules. Given this prompt, the LLM agent outputs a sequence of directional actions.


M.3 E VALUATION M ETRIC FOR B ABA I S Y OU


To evaluate the performance of an LLM agent, we define a hierarchical scoring metric that rewards
meaningful progress toward solving the puzzle. As shown in Figure 22, a key prerequisite is breaking
the rule ‘Wall Is Stop’, which enables movement out of the closed area. The second subgoal is
creating a winning condition, such as forming the rule ‘Flag Is Win’, but this is only possible once the


48


|Models|BabaIsYou|Rank|
|---|---|---|
|Llama-3.2-1B<br>Llama-3.2-3B<br>Qwen-2.5-3B<br>Qwen-2.5-7B<br>Minitron-4B<br>Minitron-8B|6.7_±_11.5<br>20.0_±_0.0<br>13.3_±_11.5<br>20.0_±_0.0<br>20.0_±_0.0<br>20.0_±_0.0|12<br>6.5<br>10.5<br>6.5<br>6.5<br>6.5|
|GPT-4o-mini<br>GPT-4o<br>o3-mini<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|13.3_±_11.5<br>20.0_±_0.0<br>**73.3**_±_46.2<br>**73.3**_±_46.2<br>46.7_±_46.2<br>20.0_±_0.0|10.5<br>6.5<br>1.5<br>1.5<br>3<br>6.5|


Table 40: Gameplay score on
_Baba Is You_ .








|Models Agent|BabaIsYou|Rank|
|---|---|---|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|**20.0**_±_0.0<br>**20.0**_±_0.0<br>**20.0**_±_0.0<br>**20.0**_±_0.0|4.5<br>4.5<br>4.5<br>4.5|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|**20.0**_±_0.0<br>**20.0**_±_0.0<br>**20.0**_±_0.0<br>**20.0**_±_0.0|4.5<br>4.5<br>4.5<br>4.5|


|Models Input|BabaIsYou|Rank|
|---|---|---|
|GPT-4o<br>Text<br>Image<br>Both|**20.0**_±_0.0<br>6.7_±_13.7<br>**20.0**_±_0.0|6<br>9<br>6|
|Gemini<br>Text<br>Image<br>Both|73.3_±_46.2<br>20.0_±_0.0<br>**86.7**_±_23.1|2<br>6<br>1|
|Claude<br>Text<br>Image<br>Both|**46.7**_±_46.2<br>20.0_±_0.0<br>20.0_±_0.0|3<br>6<br>6|



Table 41: Ablation study for agentic modules on _Baba Is You_ .



Table 42: Comparison across
modalities on _Baba Is You_ .



wall constraint is removed. Each subgoal provides 20 points. If the agent clears the level by having
the ‘You’ object touch a ‘Win’ object, it receives a full score of 100, overriding subgoal rewards. The
final score is computed as:



Score =



100 _,_ if level is cleared

40 _,_ if ‘Wall Is Stop’ is broken and ‘Win’ rule is created



20 _,_ if ‘Wall Is Stop’ is broken only



M.4 E XPERIMENTAL C ONFIGURATION FOR B ABA I S Y OU


For all 6 open-source LLMs, we use a temperature of 0.7 and a repetition penalty of 1, and set the
maximum number of game steps to 30. We run all experiments with 3 trials and report the average
score with the standard deviation.


M.5 R ESULT FOR B ABA I S Y OU


The performance of different models on Level 1 of _Baba Is You_ using the ‘reflection-planning’
agent is shown in Table 40. We observe that o3-mini and Gemini-2.5-pro achieve the highest score
of 73.3, significantly outperforming all other models. Apart from these two reasoning models, only
Claude-3.7-sonnet, a hybrid reasoning model, scores above 20.0, indicating that it is the only other
model capable of constructing a valid winning condition. In contrast, all non-reasoning models,
including every open-source small language model we tested, typically only managed to break the
‘Wall Is Stop’ rule, consistently earning a score of 20.0. However, a qualitative analysis of the models’
self-defined subtasks and reasoning traces suggests that these models often fail to infer that breaking
‘Wall Is Stop’ is a necessary prerequisite for constructing the winning condition. This implies that
their success in breaking the rule was largely unintentional.


Table 41 presents an ablation study evaluating the impact of agentic modules on performance in _Baba_
_Is You_ . Across both Llama-3.2-3B and GPT-4o, we observe no measurable improvement over the
zero-shot baseline, with all configurations achieving the same score of 20.0. This indicates that the
agentic components do not significantly enhance the agent’s ability to reach the winning condition for
these two models. The task remains challenging, largely due to the model’s limited spatial reasoning
capabilities. While the models occasionally produce valid high-level plans, such as to form the rule
‘Flag Is Win’ at specific coordinates, they frequently fail to account for the game’s pushing mechanics.
As a result, they often push text tiles in unintended directions, breaking or misaligning the intended
rule formation.


Table 42 presents an ablation study on input modalities across several multimodal models. We observe
that relying solely on image input significantly degrades performance for all models. Adding image
input on top of text yields only marginal improvements, if any, suggesting that the agents primarily
rely on text-based representations to make decisions. Notably, Gemini-2.5-pro benefits slightly from
the combined input, achieving the highest score of 86.7.


49


N 2048


N.1 G AME D ESCRIPTION FOR 2048


**Environment.** _2048_ (Cirulli, 2014) is a single-player sliding tile puzzle game played on a 4×4 grid.
The objective is to combine numbered tiles by sliding them in one of four directions (i.e., up, down,
left, or right) to create a tile with the value 2048. In this environment, the agent observes the current
board state, represented as a 4×4 matrix of integers (each cell contains 0 for empty or a power of 2 for
active tiles), and selects one of four discrete actions corresponding to directional moves. While the
original game ends when no moves are available (i.e., the board is full and no adjacent tiles can be
merged), we additionally terminate the episode if the agent performs five consecutive invalid moves
(i.e., actions that result in no change to the board state). For implementation, we use an open-source,
Pygame-based game environment. The logic module manages the board state, tile movements,
merging, and win/loss conditions, while the interface leverages Pygame to render the board and
handle user input. The implementation supports dynamic resizing and configurable parameters, and
is designed to facilitate both human play and automated experiments.


**Observation-to-Text Conversion.** The environment’s board state can be directly transformed into a
textual description, formatting it as a 4×4 array of integers in which each element indicates the value
of the corresponding tile.


**Action Space.** The action space comprises four discrete actions: ‘up’, ‘down’, ‘left’, and ‘right’,
each representing a possible direction in which the agent can slide the tiles on the board.


N.2 G AMEPLAY P ROMPT FOR 2048


Figure 24 shows the action inference prompt and the corresponding game screenshot used by the
zero-shot agent to play 2048. The system prompt includes (1) the main objective of the game, (2)
detailed game rules, and (3) the expected input-output format between the LLM and the environment.
The user prompt provides (1) the specific task for the 2048 game, (2) the previous board state and
game score, (3) the last executed action, (4) the current board state and game score, and (5) the
expected output format. Based on this information, the agent determines the next action to take.


N.3 E VALUATION M ETRIC FOR 2048


The goal of _2048_ is to create a tile with the value 2048. The game score increases as tiles are merged,
with the value of the merged tile added to the total score. Although the score when the 2048 tile is
created can slightly vary depending on the gameplay, it is generally estimated that the score is around
20,000 points. Therefore, we define the evaluation metric as the progress to the target score of 20,000,
normalized to 100. Formally, the normalized score is defined as:


Final Game Score
Score = min � _×_ 100 _,_ 100� _._

20,000


where ‘Final Game Score’ denotes the total score at the end of the game. This metric reflects how
close the agent came to achieving the primary objective of creating the 2048 tile.


N.4 E XPERIMENTAL C ONFIGURATION FOR 2048


For all 6 open-source LLMs, including Llama-3.2-1B/3B, Qwen-2.5-3B/7B, and Minitron-4B/8B,
we use a temperature of 0.0 and a repetition penalty of 1.0. We set the maximum number of game
steps to 10,000. However, the maximum number of game steps (10,000) was never reached in the
experiments. The game typically terminated either when the board was full and no adjacent tiles
could be merged, or when the agent failed to take an action that changed the board state for more
than five consecutive steps. In the best gameplay episode of o3 zero-shot agent, which achieved a
score of 57.32, a total of 685 steps were taken to reach this result.


N.5 R ESULT FOR 2048


All reported results in Tables 43–45 are computed as the mean and standard deviation over five
independent runs, using a ‘zero-shot’ agent for each model configuration. To establish a baseline for


50


**System prompt** **User prompt**



You are an expert AI agent specialized in playing the 2048 game with advanced strategic reasoning.
Your primary goal is to achieve the highest possible tile value while maintaining long-term
playability by preserving the flexibility of the board and avoiding premature game over.


### 2048 Game Rules ###

1. The game is played on a 4×4 grid. Tiles slide in one of four directions: 'up', 'down', 'left', or 'right’.
2. Only two consecutive tiles with the SAME value can merge. Merges cannot occur across empty
tiles.

3. Merging is directional:

  - Row-based merges occur on 'left' or 'right' actions.

  - Column-based merges occur on 'up' or 'down' actions.
4. All tiles first slide in the chosen direction as far as possible, then merges are applied.
5. A tile can merge only once per move. When multiple same-value tiles are aligned (e.g., [2, 2, 2, 2]),
merges proceed from the movement direction. For example:

  - [2, 2, 2, 2] with 'left' results in [4, 4, 0, 0].

  - [2, 2, 2, 0] with 'left' results in [4, 2, 0, 0].
6. An action is only valid if it causes at least one tile to slide or merge. Otherwise, the action is
ignored, and no new tile is spawned.
7. After every valid action, a new tile (usually 90 percent chance of 2, 10 percent chance of 4) appears
in a random empty cell.
8. The game ends when the board is full and no valid merges are possible.
9. Score increases only when merges occur, and the increase equals the value of the new tile created
from the merge.


### Decision Output Format ###
Analyze the provided game state and determine the single most optimal action to take next.
Return your decision in the following exact format:


### Reasoning
<a detailed summary of why this action was chosen>
### Actions

<up, right, left, or down>


Ensure that:


  - The '### Reasoning' field provides a clear explanation of why the action is the best choice,
including analysis of current tile positions, merge opportunities, and future flexibility.

  - The '### Actions' field contains only one of the four valid directions.



### Target task
Merge tiles to make a tile with the value of 2048


### Previous state

Board of 2048 Games:

[2, 0, 0, 0]

[4, 0, 0, 0]

[2, 2, 0, 0]

[16, 4, 2, 0]
Score: 52


### Last executed action

left


### Current state

Board of 2048 Games:

[2, 0, 0, 0]

[4, 0, 2, 0]

[4, 0, 0, 0]

[16, 4, 2, 0]
Score: 56


You should only respond in the format described below, and you
should not output comments or other information.
Provide your response in the strict format:
### Reasoning
<a detailed summary of why this action was chosen>
### Actions

<direction>


**Game screenshot**



Figure 24: Action inference prompt for ‘zero-shot’ agent playing 2048.



|Models|2048|Rank|
|---|---|---|
|Random Agent|5.5_±_2.3|6|
|Llama-3.2-1B<br>0.0_±_0.1<br>15<br>Llama-3.2-3B<br>0.3_±_0.2<br>12<br>Qwen-2.5-3B<br>0.1_±_0.1<br>13<br>Qwen-2.5-7B<br>0.6_±_0.4<br>11<br>Minitron-4B<br>0.1_±_0.0<br>14<br>Minitron-8B<br>0.7_±_0.7<br>10|Llama-3.2-1B<br>0.0_±_0.1<br>15<br>Llama-3.2-3B<br>0.3_±_0.2<br>12<br>Qwen-2.5-3B<br>0.1_±_0.1<br>13<br>Qwen-2.5-7B<br>0.6_±_0.4<br>11<br>Minitron-4B<br>0.1_±_0.0<br>14<br>Minitron-8B<br>0.7_±_0.7<br>10|Llama-3.2-1B<br>0.0_±_0.1<br>15<br>Llama-3.2-3B<br>0.3_±_0.2<br>12<br>Qwen-2.5-3B<br>0.1_±_0.1<br>13<br>Qwen-2.5-7B<br>0.6_±_0.4<br>11<br>Minitron-4B<br>0.1_±_0.0<br>14<br>Minitron-8B<br>0.7_±_0.7<br>10|
|GPT-4o-mini<br>GPT-4o<br>o3-mini<br>o4-mini<br>o3<br>Gemini-2.5-pro<br>Claude-3.7<br>Deepseek-R1|1.1_±_1.0<br>5.6_±_1.5<br>25.3_±_7.3<br>15.7_±_6.7<br>**34.9**_±_23.4<br>5.1_±_2.5<br>5.3_±_2.7<br>11.5_±_3.4|9<br>5<br>2<br>3<br>1<br>8<br>7<br>4|


Table 43: Gameplay score on
_2048_ .









|Models Agent|2048|Rank|
|---|---|---|
|Random Agent<br>-|5.5_±_2.3|6|
|Llama-3B<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|**0.3**_±_0.2<br>0.0_±_0.0<br>0.1_±_0.1<br>0.1_±_0.2|8<br>11<br>10<br>9|
|GPT-4o<br>Zero-shot<br>Refection<br>Planning<br>Ref-Plan|5.6_±_1.5<br>3.5_±_2.9<br>6.0_±_5.5<br>**7.0**_±_5.7|5<br>7<br>4<br>3|
|o3-mini<br>Zero-shot<br>Ref-Plan|**25.3**_±_7.3<br>17.6_±_9.5|1<br>2|


Table 44: Ablation study for agentic modules on _2048_ .



|Models Input|2048|Rank|
|---|---|---|
|Random Agent<br>-|5.5_±_2.3|5|
|GPT-4o<br>Text<br>Image<br>Both|**5.6**_±_1.5<br>1.8_±_1.1<br>5.4_±_4.5|3<br>10<br>6|
|Gemini<br>Text<br>Image<br>Both|5.1_±_2.5<br>**5.5**_±_2.4<br>3.1_±_2.6|8<br>4<br>9|
|Claude<br>Text<br>Image<br>Both|5.3_±_2.7<br>**8.4**_±_4.0<br>6.7_±_0.9|7<br>1<br>2|


Table 45: Comparison across
modalities on _2048_ .



comparison, we additionally included a random agent that selects one of the four possible actions
(up, down, left, right) uniformly at random. This agent was evaluated over 50 episodes, and its
performance is summarized in Tables.


**Gameplay score on 2048.** Beyond the 12 models presented in the main paper, we also include
results for OpenAI’s more recent models, o4-mini and o3 in Table 43. Interestingly, none of the
open-source models (e.g., Llama, Qwen, Minitron) were able to correctly interpret the 2D array


51


Figure 25: Three different runs for o3 zero-shot agent playing _2048_ .


prompt representing the game board. Consequently, they repeatedly issued the same action even
when no tiles could be merged, leading to premature termination of the game.


In contrast, GPT-4o, Gemini-2.5-pro, and Claude-3.7 were able to detect invalid moves and avoid
them to some extent. However, these models failed to manage merged tiles into their planning, often
repeating superficially valid actions that quickly led to a board lock-up. As a result, their gameplay
performance was almost indistinguishable from that of the random agent.


Notably, the reasoning-capable models—o3-mini, o4-mini, o3, and DeepSeek-R1—exhibited meaningful gameplay performance. While the open-source and non-reasoning models were typically
limited to producing a maximum tile of 64 or 128, o3-mini successfully generated the 512 tile in 4
out of 5 runs, and o3 achieved the 1024 tile in 2 out of 5 runs.


A particularly interesting observation is that, even without explicit strategic instructions (e.g., cornering high-value tiles or arranging tiles in a staircase pattern), the reasoning-based models implicitly
discovered human-like strategies based solely on the basic game rules provided via system prompts.
This behavior is illustrated in Figure 25, where o3 exhibits an emergent form of spatial organization
akin to that used by experienced human players.


**Ablation study for agentic modules on 2048.** In addition to the models evaluated in the main paper,
we conducted an extended ablation study using the o3-mini model to assess the impact of agentic
modules—Reflection and Planning—on gameplay performance in the 2048 environment. Table 44
presents the results of this study across three representative models: Llama-3.2-3B, GPT-4o, and
o3-mini, under various agent configurations.


For Llama-3.2-3B and GPT-4o, enabling the Reflection or Planning modules—individually or
together—did not yield significant gains, suggesting that external agentic scaffolding alone is insufficient for improving performance, likely due to limited reasoning or architectural constraints.


In contrast, o3-mini exhibited a counter-intuitive trend: the zero-shot agent significantly outperformed
both the Reflection and the Reflection-Planning agents. A plausible explanation for this phenomenon
is that reasoning-centric models such as o3-mini may already perform internal reflection and planning
when generating a response. As such, the introduction of additional agentic modules may introduce
redundancy or even propagate errors in intermediate reasoning steps, degrading performance.


Supporting this hypothesis, Figure 26 shows the inference output of o3 shortly before achieving a
1024-tile. The output reveals that the model implicitly forecasts and sequences the next three actions,
essentially performing internal planning without explicit agent modules. This emergent behavior
highlights the potential of foundation models with strong reasoning capabilities to handle multi-step
decision problems autonomously without external agentic augmentation.


**Comparison across modalities on 2048.** To assess the impact of input modality on gameplay
performance, we evaluated models using either textual or visual (image-based) representations of
the 2048 board state. The results are summarized in Table 45. Interestingly, GPT-4o demonstrated
weaker performance with image inputs compared to text, suggesting that its image understanding
capabilities—at least within the structured context of 2048—may lag behind its text comprehension.
This is consistent with prior findings that GPT-4o, while multimodal, exhibits varying levels of
alignment across modalities depending on task complexity and structure. In contrast, both Gemini


52


**User prompt**


### Target task
Merge tiles to make a tile with the value of 2048


### Previous state

Board of 2048 Games:

[2, 2, 0, 0]

[2, 8, 4, 0]

[8, 64, 64, 0]

[32, 128, 256, 512]
Score: 7312


### Last executed action

left


### Current state

Board of 2048 Games:

[4, 2, 0, 0]

[2, 8, 4, 0]

[8, 128, 0, 0]

[32, 128, 256, 512]
Score: 7444


You should only respond in the format described below, and you
should not output comments or other information.
Provide your response in the strict format:
### Reasoning
<a detailed summary of why this action was chosen>
### Actions

<direction>



**Output (OpenAI o3)**


### Reasoning

- Strategic corner: Keeping the 512 in the bottom-right corner is
crucial for a stable “snake/monotone” board. A **down** move

preserves this anchor, whereas **up** would drag the 512 to the
top row and break the structure.


- Immediate value: In column 1 the two 128 tiles merge into a 256,
giving an instant score gain and strengthening the bottom row
hierarchy

(bottom row becomes 32-256-256-512).


- Future merges set up:

– Row 3 now contains two adjacent 256s that can merge into a
512/1024 with a later right move.

– Row 1 becomes [2 2 0 0], an easy 4 on a subsequent left/right
swipe.


- Board space: After the move the grid has 6 empty cells ([4 0 0 0]
/ [2 2 0 0] / [8 8 4 0] / [32 256 256 512]), providing ample
breathing room and reducing risk of a dead-end.


- Alternative moves:


– **Right** keeps the corner but yields no merges and less space.
– **Left** is invalid (no tiles move).
– **Up** destroys the corner position and is therefore unsafe.


Given the merge gain, preserved corner, created future pairs, and
increased emptiness, **down** is the optimal choice.


### Actions

down



Figure 26: Output of OpenAI’s o3 model right before producing the 1024 tile in _2048_ .



**Original system prompt**

You are a strategic player for the game 'Slay The Spire'. Your role is to determine the best next action based on
the given task.
Provide the reasoning for what you should do for the next step to complete the task. Then, you should output the
exact action you want to execute in the game.


Reasoning: You should think step by step and provide concise reasoning to determine the next action executed
on the current state of the task.


Game Rules:

- Damage reduces Block first, then HP.

- At the start of each turn, unless modified by other effects, the player receives 3 energy and draws 5 cards.- At
the end of turn, all unused enerygy will be lost and block is removed unless retained by effects.

- Monster will give you damage when only its intent contains attack.

- X cost cards consume all remaining energy when played. Their effect scales based on the amount of energy
used.

- When you are in CARD REWARD SELECTION STATE, you can only choose one card.


Guidelines:

- You MUST choose actions only from the given valid action set. Any action outside this set is strictly forbidden.

- Since health is maintained across multiple combats rather than being restored, it is essential to manage it
carefully.

- If there are multiple actions, separate them using newline characters, e.g., 'PLAY 2 1
PLAY 4

END'.



**Augmented system prompt**

You serve as a strategic player in 'Slay The Spire,' tasked with identifying the optimal next move based on the
current assignment.
Offer an explanation for your chosen next step to fulfill the assignment, then specify the precise action you
wish to carry out in the game.


Reasoning: Analyze step-by-step, delivering succinct reasoning to decide the subsequent action within the
current context of the task.


Game Rules:

- Block absorbs damage before HP does.

- Each turn begins with the player acquiring 3 energy and drawing 5 cards, unless altered by specific effects.Unused energy disappears at the turn's end, and block is removed unless effects prevent it.

- Monsters only deal damage when their intention includes attacking.

- Cards with an X cost utilize all remaining energy, with their effects scaling accordingly.

- During the CARD REWARD SELECTION STATE, only one card can be picked.


Guidelines:

- Actions must be selected exclusively from the available action set. Actions outside this set are not allowed.

- Health persists across several battles without automatic restoration, so manage it prudently.

- If there are several actions to take, list them with newline separators, e.g., 'PLAY 2 1
PLAY 4

END'.



Figure 27: Example of original system prompt and augmented system prompt in _Slay the Spire_ .


2.5 Pro and Claude 3.7 achieved better performance with image-based inputs than with text. This
indicates a stronger visual reasoning capability in these models, particularly when parsing structured
2D spatial layouts such as the 2048 board. Their ability to interpret and act on visual patterns appears
to be more robust than their capacity to process raw 2D arrays expressed as textual input.These
findings highlight that multimodal models exhibit non-uniform modality strengths, and task-specific
evaluations are crucial for selecting the appropriate input format to maximize agent performance.


O D ETAILS FOR D ATA A UGMENTATION


**Prompting Details.** To increase the diversity of our training dataset and avoid overfitting risks,
we applied a data augmentation strategy focused on the system prompt. The original dataset was
constructed by rolling out the same game prompt multiple times in the environment to collect assistant
responses. The system prompt remains static, and the user prompt exhibits variations due to changes
in game state, though these were constrained to a fixed format where only specific values changed.


To address this issue, we performed augmentation on the system prompt, which contains general
information such as the LLM’s role, game rules, and behavioral guidelines. Since the user prompt was


53


dependent on dynamic game states, modifying it risked introducing inconsistencies or hallucinations.
Therefore, we chose to keep the user prompt fixed during augmentation.


We use GPT-4o to generate paraphrased versions of the original system prompt. Specifically, we
prompted the model to produce 10 alternative phrasings of the original system prompt that preserved
its semantics while varying its linguistic expression. Each paraphrased system prompt was then
paired with the original user prompt and assistant response, resulting in 10 augmented versions of
each original data point. Including the original, this expands the dataset by a factor of 11. Figure 27
presents an example of the original and augmented prompt in _Slay the Spire_ .


This augmentation strategy helped increase the syntactic and lexical diversity of the dataset while
preserving semantic fidelity and coherence, thereby supporting more robust fine-tuning of the LLM.


# of Augs. SuperMario 2048


0 24.2 1.4

3 26.8 3.5

10 26.7 2.8

20 25.9 2.4


Table 46: Performance across different numbers of augmentations.


**Effect of The Number of Augmentations.** Table 46 shows the fine-tuned model performance
across different numbers of augmentations. We use the same fine-tuning setup as the intra-game
generalization in Table 7. Overall, increasing the number of augmentations improves the performance
of fine-tuned models compared to the one with no augmentation. Interestingly, the small number
of augmentations (3 or 10) is quite effective to ensure linguistic diversity in fine-tuning, and the
effectiveness diminishes as the number of augmentations grows.


P I MPLEMENTATION D ETAILS


P.1 A SYNCHRONOUS I NFERENCES FOR M ULTI -A GENT E NVIRONMENT


Here we provide implementation details for multi-agent game environment that enables efficient,
scalable, and realistic agent interaction.


**Overview.** The core design principle is to execute the game loop on a frame-by-frame basis while
allowing each agent to asynchronously infer and initiate its next high-level action upon completion of
the previous one. This approach is particularly well-suited for real-time, frame-based games such as
_Street Fighter III_ and _StarCraft II_, where individual actions may span a variable number of frames
(e.g., a ‘Move Away’ action takes 4 frames, whereas a ‘Super Attack’ requires 7 frames to complete).
In this system, each agent operates independently, without waiting for other agents to complete their
actions. As soon as an agent completes its current action, it observes the current game state and
determines its next high-level action. This asynchronous execution allows the game to progress
fluidly and continuously, closely mimicking the dynamics of real-time multiplayer games.


**Illustrative Example.** Consider a multi-agent scenario in _Street Fighter III_ . Agent 1 selects a ‘Super
Attack’ that spans 7 frames, while Agent 2 chooses a ‘Move Away’ action that lasts 4 frames. The
game orchestrator initiates both actions simultaneously. After 4 frames, Player 2’s action concludes,
triggering the agent to observe the updated state and select a new action, _e.g._, a ‘Medium Punch’
lasting 2 frames. The orchestrator then integrates this new action into the ongoing simulation, even
as Agent 1’s ”Super Attack” continues. This frame-by-frame orchestration proceeds iteratively.
Each agent re-enters the decision-making process immediately upon completing its current action,
independent of the progress or status of other agents.


**Advantages.** This asynchronous, non-blocking scheduling model provides several key advantages. It
enables agents to operate with varying action durations without artificial synchronization barriers,
facilitating a more natural and responsive interaction dynamic. The resulting system supports
overlapping actions, better reflects the timing complexities of real-time games, and can be readily
extended to support environments with more than two agents.


54


P.2 F INE - TUNING


We conducted supervised fine-tuning using collected gameplay data to adapt the LLM agent to
game-specific reasoning and interactions with environments.


Task LLaMA-3.2-1B(h) LLaMA-3.2-3B(h)


Intra-game/Non-game 1.7 4.2
OOD-game 1.7 4.3


Table 47: Elapsed GPU time for fine-tuning.


**Training Configuration.** We fine-tune two models: Llama-3.2-1B and Llama-3.2-3B. Training is
conducted using 4 NVIDIA A100 GPUs with 80GB of memory each. We use a learning rate of 1e-6,
a per-device batch size of 4 with gradient accumulation steps set to 4, resulting in an effective batch
size of 64. The models were trained for 1 epoch with 100 warm-up steps. Table 47 summarizes the
GPU time taken for fine-tuning.


**Data Statistics.** In total, we use 105,502 data points for fine-tuning. Only data points containing fewer
than 4,096 tokens are used for training to ensure compatibility with model input length limitations.
All data points from _Pokemon_ _´_ and 329 out of 9900 data points from _Minecraft_ are discarded due to
length constraint. For the out-of-distribution (OOD) game generalization experiments, we exclude
the games 2048 and Super Mario, resulting in 87,660 data points used. Apart from the number of
data points, the training configuration remained identical.


P.3 U NSEEN S CENARIOS


To evaluate the intra-game generalization capability of fine-tuned LLM agents, we define a separate
scenario that is not used during the training dataset collection. Unseen scenarios differs from the seen
ones by featuring a different character, map, or stage. Figure 28 presents example screenshots of the
seen and unseen scenarios across six games.


**Street Fighter III.** While the character Ken was used during training data collection, a different
character, Chun-Li, was introduced at evaluation time to assess intra-game generalization. Chun-Li
features a distinct set of moves and hitboxes, posing a significantly different control and tactical
challenge compared to Ken. The game environment and match settings remained unchanged.


**Darkest Dungeon.** While the first expedition used during training data collection featured a party
composed of a Plague Doctor, Vestal, Highwayman, and Crusader, the unseen scenario
involved a different party composition: one Man-At-Arms, two Grave Robbers, and one
Vestal . This change introduced significantly different combat dynamics, synergies, and positional
requirements. Additionally, the enemy pool in this dungeon included the Madman —a monster
not encountered during training—known for its stress-inducing attacks and erratic behavior. All
other gameplay parameters, including the dungeon type (short dungeon in Ruins area), remained
unchanged.


**StarCraft II.** During training, agents were exposed to the ‘Ancient Cistern LE’ map, while evaluation
was conducted on a different map, ‘Babylon LE’ to assess intra-game generalization. All other
game settings, including player race (Protoss), opponent race (Zerg), opponent’s build order strategy
(Timing), and difficulty level (Hard), were kept constant.


**Slay the Spire.** We used game runs with different random seeds as unseen scenarios. Each game
seed determines the layout of the map, including the sequence of opponents, bosses, events, and card
reward options. All other game parameters, such as character choice ( _IronClad_ ) and starting deck,
were held constant.


**Baba Is You.** In the case of _Baba Is You_, the second stage, Level 2 - Now what is this?,
is used as an unseen scenario. This stage features new rule combinations and object interactions
that are absent from the training set, thereby testing the agent’s ability to generalize to novel logic
structures. The game mechanics and control scheme remained unchanged.


55


Q A NALYSIS OF T HE G AP BETWEEN I N - GAME AND OOD- GAMES IN
F INE  - TUNING


Genre Action Adventure RPG Simulation Strategy Puzzle


Games SuperMario AceAttorney DarkestD MineCraft SlaySpire 2048


Llama-3.2-1B (Pretrain) 18.7 1.3 0.0 0.0 0.0 0.1
Llama-3.2-1B (Fine-tune) 23.5 5.5 0.0 0.0 0.0 0.3
Llama-3.2-3B (Pretrain) 31.8 4.6 47.5 0.0 0.0 0.1
Llama-3.2-3B (Fine-tune) 24.9 9.1 40.1 0.0 0.0 3.1


Avg. Improvement (%) 2.0 210.5 -7.8 0.0 0.0 1600.0


Table 48: Performance of LLaMA models with varying in-ood game gap.


**Setup.** For studying the in-OOD gap in generalization, we fine-tune Llama-3.2 only on _Baba Is You_ .
Other hyperparameter configurations are exactly the same as in Appendix P.


**Results.** As shown in Table 48, fine-tuning yields the most improvements for OOD games in the same
genre, but can also provide benefits across different genres in some cases. For example, 2048, another
puzzle game, showed the largest improvement after fine-tuning. Interestingly, Ace Attorney, though a
different genre, also benefited from fine-tuning, likely due to shared requirements in logical reasoning
(see qualitative examples below). In contrast, for games like _Darkest Dungeon_ and _Super Mario_,
which involve different gameplay dynamics and action spaces, the effect was mixed. Note that, as
shown in Table 7, unlike the current experiment (fine-tuned on _Baba Is You_ only), LLMs fine - tuned on
10 games (without _Super Mario_ ) showed consistent improvements on Super Mario (OOD game). This

          implies our fine tuning set, constructed from a diverse set of games across genres, contains knowledge
broadly beneficial for gameplay/decision-making and supports cross-genre generalizability.


R L IMITATIONS AND F UTURE W ORK


**Cost Consideration.** Among all games in Orak, six games, _i.e._, _Ace Attorney_, _Her Story_, _Darkest_
_Dungeon_, _Stardew Valley_, _Slay the Spire_, and _Baba is You_, require a one-time purchase, typically
priced ranging from $9 _._ 99 to $24 _._ 99 . While this represents a non-negligible upfront cost, it is
relatively minor compared to the recurring cost associated with proprietary LLM API calls. From a
cost-efficiency perspective, the benchmark remains accessible and practical for sustained research.


**License Issue.** We have made considerable efforts to comply with licensing requirements in designing
our benchmark. (1) Users must purchase the commercial games themselves for evaluation. (2) We
do not distribute any commercial game executables. (3) We do not modify any game assets during
gameplay. Moreover, we explicitly state the following legal compliance guidelines “ _This project is_
_strictly for research purposes. Researchers are required to use our framework solely as a benchmark_
_for evaluating LLMs, and any models derived from our benchmark are strictly prohibited from_
_commercial use_ ”.


**Real-time Gameplay.** _Street Fighter III_, _Super Mario_, and _StarCraft II_ inherently require real-time
gaming, unlike other turn-based or simulation games in Orak. However, in our current evaluation
setup, the game is paused during LLM inference to remove the impact of real-time constraints on
agent performance. While this allows for more stable evaluation of reasoning capabilities, real-time
responsiveness is critical in many gaming contexts, so it should be handled for practical needs. We
leave latency-aware evaluation protocols for building real-time gaming LLM agents as future work.


**Study on RL-based Fine-tuning.** Although RL-based fine-tuning has demonstrated strong performance in many domains, such as mathematics and programming, we did not explore it in this study.
Given the interactive nature of the Orak environments, it would be natural to derive dynamic, contextaware rewards from in-game feedback and apply RL fine-tuning methods such as DPO (Rafailov
et al., 2023) or GRPO (Shao et al., 2024). Unlike domains such as mathematics or programming,
where problems typically have static correct solutions derived through logical reasoning, gameplay
requires _strategic reasoning_ that adapts dynamically to the actions of other agents. In games, the
optimal action is often contingent on the evolving behavior of the player or opponents, reflecting the


56


complex, interactive nature of multi-agent environments. This distinction is particularly relevant to
real-world domains such as business, economics, and negotiation, where strategic decision-making is
frequently modeled using game-theoretic frameworks (Zhang et al., 2024). Therefore, leveraging
Orak as an environment for RL-based fine-tuning may significantly enhance an LLM’s capacity to
reason strategically and operate effectively in multi-agent settings. This line of research holds promise
for improving LLM performance in a broad range of real-world applications where understanding
multi-agent dynamics is essential.


**Support for Diverse Modalities.** Orak supports evaluation of LLMs and VLMs, but it does not
extend to other modalities often essential in real-world gameplay. One key example is _sound_ . For
instance, in _Minecraft_, players rely on zombie audio cues to avoid danger, while in _Street Fighter_
_III_ and _StarCraft II_, alert sounds indicate some specific attacks by the enemy. Also, beyond games
in Orak, First-Person Shooter (FPS) games usually use gunfire sounds for spatial awareness, and
horror games often rely on audio to signal the proximity of threats. Consequently, incorporating
other modalities such as audio remains an open challenge, and benchmarking the performance of
emerging Speech-Language Models (Chu et al., 2023; Cui et al., 2024) in gaming scenarios could be
an important step toward broader multimodal agent development.


**Societal Impact.** Simulation games, _Minecraft_ and _Stardew Valley_, offer rich environments where
players can explore, mine resources, and craft items, enabling life-like simulations of human behavior.
These games offer a valuable testbed for analyzing long-horizon behavior of LLM agents by systematically comparing gameplay trajectories of humans and LLM agents, which enables a rigorous
assessment of whether LLMs exhibit human-like decision-making patterns. Introducing multiple
agents into these environments allows for the study of emergent social behaviors among LLM agents.
We believe such settings are particularly well-suited for precisely measuring the social impact of
complex agent behaviors, offering valuable insights into the dynamics of LLM-based agents.


57


(a) Street Fighter III (b) Super Mario


(c) Darkest Dungeon


(d) Starcraft II


(e) Slay the Spire


(f) Baba Is You


Figure 28: Comparison of seen (left) and unseen (right) scenarios for six games.


58


