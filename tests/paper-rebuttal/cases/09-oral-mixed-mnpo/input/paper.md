Preprint, Under Review

## M ULTIPLAYER N ASH P REFERENCE O PTIMIZATION


**Fang Wu** _[♡∗]_ **, Xu Huang** _[♠∗]_ **, Weihao Xuan** _[∇][,][△]_ **, Zhiwei Zhang** _[♣]_ **, Yijia Xiao** _[♢]_

**Guancheng Wan** _[♢]_, **Xiaomin Li** [□], **Bing Hu** _[◦]_, **Peng Xia** _[⋆]_, **Jure Leskovec** _[♡]_, **Yejin Choi** _[♡†]_

_♡_ Stanford University, _♠_ Georgia Institute of Technology, _∇_ The University of Tokyo

_△_ RIKEN AIP, _♣_ Pennsylvania State University, _♢_ University of California, Los Angeles,

 - Harvard University, _◦_ Independent Researcher, _⋆_ UNC–Chapel Hill
fangwu@stanford.edu, xu.huang@gatech.edu, yejin@cs.stanford.edu


A BSTRACT


Reinforcement learning from human feedback (RLHF) has emerged as the standard
paradigm for aligning large language models (LLMs) with human preferences.
However, reward-based methods built on the Bradley–Terry assumption struggle to
capture the non-transitive and heterogeneous nature of real-world preferences. To
address this, recent studies have reframed alignment as a two-player Nash game,
giving rise to Nash learning from human feedback (NLHF). While this perspective
has inspired algorithms such as INPO, ONPO, and EGPO with strong theoretical
and empirical guarantees, they remain fundamentally restricted to two-player interactions, creating a single-opponent bias that fails to capture the full complexity
of realistic preference structures. In this work, we introduce Multiplayer Nash
Preference Optimization (MNPO), a novel framework that generalizes NLHF to
the multiplayer regime. It formulates alignment as an _n_ -player game, where each
policy competes against a population of opponents while being regularized toward
a reference model. Our framework establishes well-defined Nash equilibria in
multiplayer settings and extends the concept of duality gap to quantify approximation quality. We demonstrate that MNPO inherits the equilibrium guarantees
of two-player methods while enabling richer competitive dynamics and improved
coverage of diverse preference structures. Through comprehensive empirical evaluation, we show that MNPO consistently outperforms existing NLHF baselines
on instruction-following benchmarks, achieving superior alignment quality under
heterogeneous annotator conditions and mixed-policy evaluation scenarios. Together, these results establish MNPO as a principled and scalable framework for
aligning LLMs with complex, non-transitive human preferences. Code is available
[at https://github.com/smiles724/MNPO.](https://github.com/smiles724/MNPO)


1 I NTRODUCTION


Large language models (LLMs) have achieved remarkable progress in instruction following and openended reasoning, primarily through reinforcement learning from human feedback (RLHF) (Christiano
et al., 2017). In RLHF, annotators provide preference comparisons between model outputs, and these
signals are used to align LLMs with human expectations. While reward-based RLHF pipelines built
upon the _Bradley-Terry_ (Bradley & Terry, 1952) model have enabled widely deployed systems (e.g.,
InstructGPT (Ouyang et al., 2022), Claude (Bai et al., 2022), and Gemini (Team et al., 2023)), they
assume transitive preferences and scalar reward functions. Recent empirical studies in LLM alignment have revealed that human preferences often exhibit non-transitive patterns and heterogeneous
structures that challenge these assumptions (Ethayarajh et al., 2024; Wu et al., 2024).


This limitation has motivated recent attempts to develop _game-theoretic formulations of alignment_ .
Rather than relying on scalar rewards that enforce transitivity constraints, recent work treats preference
optimization as finding Nash equilibria in games defined by general preference oracles (Munos et al.,
2023). In this Nash learning from human feedback (NLHF) paradigm, a well-aligned policy represents


_∗_ Equal contribution.

_†_ Corresponding authors.


1


Preprint, Under Review


an optimal strategy that cannot be exploited by competing policies. At equilibrium, policies achieve
a balanced win rate that reflects strategic optimality rather than mediocrity. Subsequent studies
have explored this paradigm through various algorithmic lenses. For instance, Zhang et al. (2025b)
leverages no-regret learning to approximate the Nash equilibrium via self-play. Zhang et al. (2025a)
accelerates convergence using optimistic mirror descent. Zhou et al. (2025) establishes last-iterate
convergence with extragradient updates. These approaches advance both theoretical guarantees and
empirical stability compared to traditional RLHF.


Despite advances, the existing NLHF remains constrained to _two-player settings_ where a single policy
competes against one opponent. However, real-world preference alignment often involves diverse
annotators, heterogeneous evaluation criteria, or mixtures of historical model checkpoints - contexts
that are better modeled as multiplayer games (Freund & Schapire, 1999). Extending NLHF to the
multiplayer regime raises new challenges: _(i)_ how to formulate objectives that balance fairness and
competitiveness among multiple policies, _(ii)_ how to design algorithms that converge to multiplayer
Nash equilibria, and _(iii)_ how to ensure tractability when scaling to larger LLMs (Sokota et al., 2022).


We address these challenges by proposing _Multiplayer Nash Preference Optimization (MNPO)_, a
principled framework that generalizes two-player preference optimization to _n_ -player games. In
MNPO, each policy simultaneously competes against all other policies while being regularized
toward a reference policy, creating a competitive equilibrium that balances performance against the
population with adherence to a trusted baseline. Our contributions are threefold:


- **Theoretical Framework** : We establish that MNPO admits natural equilibrium characterizations,
including well-defined Nash policies and duality gaps that measure alignment quality. We prove
that MNPO inherits the desirable convergence properties of existing two-player formulations while
enabling richer equilibrium dynamics.


- **Algorithmic Innovation** : We introduce time-dependent MNPO (TD-MNPO), where opponent
sets evolve adaptively using weighted combinations of historical policies. This approach enables
models to dynamically incorporate past knowledge while maintaining training stability.


- **Empirical Validation** : Through comprehensive experiments on instruction-following and reasoning benchmarks, we demonstrate that MNPO consistently outperforms existing NLHF baselines,
particularly excelling in scenarios involving diverse preferences and complex evaluation criteria.


Our analysis reveals that MNPO provides a unifying perspective on preference optimization, subsuming many existing methods as special cases while offering improved robustness in multi-agent
alignment scenarios. By bridging recent advances in NLHF with the practical demands of aligning
LLMs to diverse and potentially non-transitive human preferences, MNPO establishes a scalable
foundation for next-generation alignment techniques.


2 RLHF P RELIMINARIES


**Notation.** _x ∈X_ denotes a prompt and _X_ is the prompt space. _x_ is assumed to be sampled from a
fixed but unknown distribution _d_ 0 . An LLM is characterized by a policy _π_ : _X →_ ∆( _Y_ ) that takes a
prompt _x_ as input and outputs a distribution over the response space _Y_ . The response _y ∈Y_ is then
sampled from the distribution _π_ ( _· | x_ ).


**Bradley-Terry Model Assumption.** The prevalent RLHF framework (Christiano et al., 2017;
Ouyang et al., 2022) assumes the Bradley-Terry model. It assumes that there exists a reward function

_r_ _[∗]_ such that for any _x ∈X_ and _y_ [1] _, y_ [2] _∈Y_, we have P � _y_ [1] _≻_ _y_ [2] _| x_ � = exp( _r_ _[∗]_ (exp _x,y_ ( [1] _r_ ))+exp( _[∗]_ ( _x,y_ [1] )) _r_ _[∗]_ ( _x,y_ [2] )) [=]
_σ_ � _r_ _[∗]_ [�] _x, y_ [1] [�] _−_ _r_ _[∗]_ [�] _x, y_ [2] [��] _._


After learning a reward function _R_ ( _·, ·_ ), RLHF algorithms aim to maximize the following KLregularized objective with preference optimization RL algorithms such as PPO (Schulman et al.,
2017):
_J_ ( _π_ ) = E _x∼d_ 0 �E _y∼π_ ( _·|x_ ) [ _R_ ( _x, y_ )] _−_ _τ_ KL ( _π_ ( _· | x_ ) _∥π_ ref ( _· | x_ ))� _._ (1)


Here _π_ ref is the reference policy, which is usually a supervised fine-tuned LLM, and _τ >_ 0 is the
regularization parameter. By maximizing the objective, the obtained policy simultaneously achieves


2


Preprint, Under Review


a high reward and stays close to _π_ ref, which can mitigate reward hacking (Tien et al., 2022; Skalse
et al., 2022) to some extent.


**General Preference Oracle.** The aforementioned algorithms rely on the Bradley-Terry model
assumption, which may not always hold in practice. Recent studies (Munos et al., 2023; Calandriello et al., 2024; Ye et al., 2024; Zhang et al., 2025b;a) have instead directly considered
the general preference distribution P without imposing additional assumptions, framing the preference optimization problem as a two-player game. These works assume the existence of a
_preference oracle_ P : _X × Y × Y →_ [0 _,_ 1] . It can be queried to obtain binary preference
signals as _z ∼_ Ber �P � _y_ [1] _≻_ _y_ [2] _| x_ ��, where _z_ = 1 indicates that _y_ [1] is preferred to _y_ [2], and
_z_ = 0 indicates the opposite. The preference distribution is introduced as _λ_ P ( _x, y, y_ _[′]_ ) =
( _y, y_ _[′]_ ) _·_ I [ _U <_ P ( _y ≻_ _y_ _[′]_ _| x_ )] + ( _y_ _[′]_ _, y_ ) _·_ I [ _U ≥_ P ( _y ≻_ _y_ _[′]_ _| x_ )], where _U ∼_ Uniform(0 _,_ 1) is a
random variable.


Given two policies _π_ 1 and _π_ 2, LLMs are aligned using this general preference oracle. Consequently,
the game objective is written as:
_J_ ( _π_ 1 _, π_ 2 ) = E _x∼D_ [E _y_ 1 _∼π_ 1 _,y_ 2 _∼π_ 2 [P ( _y_ 1 _≻_ _y_ 2 _| x_ )] _−_ _τ_ KL ( _π_ 1 _∥π_ ref ) + _τ_ KL ( _π_ 2 _∥π_ ref )] (2)
where the max-player _π_ 1 aims to maximize the objective, and the min-player _π_ 2 aims to minimize
the objective. The goal of both players is to maximize their winning rates against the opponent while
not deviating too far from _π_ ref, which shares a similar spirit with the objective of Eq. 1.


**Nash Policy and Duality Gap.** Without loss of generality, we restrict our attention to the policy
class Π containing the policies with the same support set as _π_ ref . The Nash equilibrium of the game
in Eq. 2 is then defined as:
_π_ 1 _[∗]_ _[, π]_ 2 _[∗]_ [:= argmax] argmin _J_ ( _π_ 1 _, π_ 2 ) _._ (3)
_π_ 1 _∈_ Π _π_ 2 _∈_ Π


Due to the symmetry of the two players, their Nash policies are unique and coincide, meaning
_π_ 1 _[∗]_ [=] _[ π]_ 2 _[∗]_ [=] _[ π]_ _[∗]_ [(Ye et al., 2024). Interestingly,] _[ J]_ [ (] _[π]_ _[∗]_ _[, π]_ [)] _[ ≥]_ [0] _[.]_ [5] [ always holds for] _[ ∀][π][ ∈]_ [Π] [, as]
_J_ ( _π_ _[∗]_ _, π_ _[∗]_ ) = 0 _._ 5 indicates that _π_ _[∗]_ is the best response against itself. To quantify how well a policy _π_
approximates the Nash policy _π_ _[∗]_, we define the duality gap as:
DualGap( _π_ ) := max (4)
_π_ 1 _[J]_ [ (] _[π]_ [1] _[, π]_ [)] _[ −]_ [min] _π_ 2 _[J]_ [ (] _[π, π]_ [2] [)] _[ .]_


The duality gap is nonnegative and DualGap( _π_ ) = 0 if and only if _π_ = _π_ _[∗]_ . Hence, our goal is to
find a policy that minimizes the duality gap. Once we achieve DualGap( _π_ ) _≤_ _ϵ_, we say that _π_ is an
_ϵ-approximate Nash policy_ .


3 M ETHOD


3.1 RLHF AS M ULTIPLAYER G AMES


To extend the two-player preference optimization objective to a multiplayer setting _{π_ 1 _, π_ 2 _, ..., π_ _n_ _}_,
we consider a framework where each policy seeks to maximize its average preference probability
against all other policies while regularizing toward a reference policy. We present the formulation of
multiplayer games under two distinct assumptions: _(i)_ the preference ranking assumption and _(ii)_ the
general preference oracle.


**Plackett-Luce Reward Learning Assumption.** To generalize the maximum-likelihood reward
learning objective for the Bradley-Terry model to one-vs-many comparisons, we adopt the _Plackett-_
_Luce_ framework. Specifically, we replace the pairwise logistic term log _σ_ � _R_ � _x, y_ [1] [�] _−_ _R_ � _x, y_ [2] [��]

with a _softmax_ over multiple alternatives, extending the Bradley-Terry model to accommodate listwise
comparisons. This Plackett-Luce model (Debreu, 1960; Plackett, 1975) maintains the interpretability
of reward-based preferences while scaling to more complex decision-making scenarios. Formally,
given a learned reward function _r_ ( _x, y_ ) and a dataset _D_ containing tuples � _x,_ � _y_ [1] _, y_ [2] _, . . ., y_ _[k]_ [��],
where � _y_ [1] _, y_ [2] _, . . ., y_ _[k]_ [�] are a pool of _k_ to-be-ranked items, the probability that _y_ _[i]_ is preferred over
the remaining pool of entities � _y_ _[j]_ [�] _j_ = _̸_ _i_ [under the Plackett-Luce model is:]


_̸_ _̸_



_̸_

P � _y_ _[i]_ _≻_ � _y_ _[j]_ [�] _̸_ _̸_



_̸_


_j_ = _̸_ _i_ _̸_



_̸_

_x_ = exp( _R_ � _x, y_ _[i]_ [�] ) (5)

_̸_ ��� � exp( _R_ ( _x, y_ _[i]_ )) + ~~[�]~~ _j_ = _̸_ _i_ [exp(] _[R]_ [ (] _[x, y]_ _[j]_ [))] _[.]_


3


Preprint, Under Review


The corresponding negative log-likelihood for a single comparison is:


_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_ � _j_ = _̸_ _i_ exp � _R_ � _x, y_ _[j]_ [��] 


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_−_ log P _y_ _[i]_ _≻_ _y_ _[j]_ [�]
� � _̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_






_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_ _−_ _R_ � _x, y_ _[i]_ [�] _._ (6)

_̸_ 


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_j_ = _̸_ _i_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_x_ = log

_̸_ ��� �

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_ exp � _R_ � _x, y_ _[i]_ [��] + � _j_ = _̸_ _i_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


The generalized reward learning objective becomes:


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


ˆ
_R ←_ arg max _R∈R_ [E][(] _[x,]_ _[{]_ _[y]_ [1:] _[k]_ _[}]_ [)] _[∼D]_ [E] _[y]_ _[i]_ _[∈]_ _[{]_ _[y]_ [1:] _[k]_ _[}]_  _R_ � _x, y_ _[i]_ [�] _−_ log

 _̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_





_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


exp � _R_ � _x, y_ _[i]_ [��] + �
 _j_ = _̸_ _i_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


� exp � _R_ � _x, y_ _[j]_ [��] 

_j_ = _̸_ _i_ 


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


_̸_ 


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_




_̸_ 


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


_._


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


_̸_


� ~~�~~ � �
Per-comparison log-likelihood

(7)
Several key observations arise from this formulation. First, when _k_ = 2 for a one-vs-one comparison,
Eq. 7 reduces to the vanilla Bradley-Terry objective, given by log _σ_ ( _R_ ( _x, y_ ) _−_ _R_ ( _x, y_ _[′]_ )), since
_e_ _[a]_
_σ_ ( _a_ ) = 1+ _e_ _[a]_ [. Second, this objective maximizes the gap between the reward of] _[ y]_ [ and the log-sum-exp]
(LSE) of all alternatives, effectively applying a soft maximum over competitors. This penalizes cases
where _y_ _[i]_ fails to dominate the collective "strength" of the dispreferred items � _y_ _[j]_ [�] _j_ = _̸_ _i_ [.]


**Multiplayer General Preference Optimization.** In addition to the Plackett-Luce assumption, we
consider _n_ -player preference optimization and leverage a _universal preference oracle_ P : _X × Y ×_
_{Y}_ _[n][−]_ [1] _→_ [0 _,_ 1] . It directly compares _y_ _[i]_ with a group of responses _{y_ _[j]_ _}_ _j_ = _̸_ _i_, leading to the binary

preference signals _z ∼_ Ber �P � _y_ _[i]_ _≻_ � _y_ _[j]_ [�] _j_ = _̸_ _i_ _[|][ x]_ �� . Subsequently, each policy _π_ _i_ competes against

other _n −_ 1 players, and the objective function becomes:


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_ _̸_ �P � _y_ _[i]_ _≻_ � _y_ _[j]_ [�] _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_J_ � _π_ _i_ _, {π_ _j_ _}_ _j_ = _̸_ _i_ � = E _x∼D_ _̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_ �E _y_ _i_ _∼π_ _i_ _,_ _{_ _y_ _j_ _|y_ _j_ _∼π_ _j_ _}_ _j_ = _̸_ _i_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_ _̸_ _j_ = _̸_ _i_


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_ _̸_ _̸_ ��� _x_ �� _−_ _τ_ KL ( _π_ _i_ ( _· | x_ ) _∥π_ ref ( _· | x_ ))� _._


_̸_


_[̸]_ _[̸]_


_[̸]_



_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_

(8)
Here, each policy _π_ _i_ seeks to maximize its expected preference over all other policies _{π_ _j_ _}_ _j_ = _̸_ _i_ . Meanwhile, the regularization term is kept to penalize _π_ _i_ with a KL divergence from the reference policy
_π_ ref weighted by _τ_ . This ensures that policies remain anchored to _π_ ref to prevent overoptimization
and maintain behavioral consistency. Regarding the dynamics of this multiplayer game, all policies
_{π_ _i_ _}_ _[n]_ _i_ =1 [are updated concurrently. Each policy] _[ π]_ _[i]_ [ optimizes its own] _[ J]_ [, leading to a competitive]
equilibrium where policies balance performance against the population and adherence to _π_ ref .


Eq.8 has several key properties. _(i)_ The symmetric treatment. All policies are treated equally,
competing in a symmetric fashion. Therefore, _π_ 1 _[∗]_ [=] _[ π]_ 2 _[∗]_ [=] _[ ...]_ [ =] _[ π]_ _n_ _[∗]_ [.] _[ (ii)]_ [ Decentralized optimization.]
Each policy’s update depends only on its own actions and aggregate opponent behavior, avoiding
complex interdependencies. _(iii)_ Generalization of the two-player case. When _n_ = 2, each policy’s
objective reduces to maximizing its pairwise preference probability minus its own KL penalty as in
Eq. 2, aligning conceptually with competitive regularization.


**Nash Equilibrium and Duality Gap.** In this _n_ -player game, the Nash equilibrium is a policy _π_ _[∗]_
where no player can improve their objective by unilaterally deviating. Formally, for all _π_ _i_ _∈_ Π :

_J_ � _π_ _i_ _[∗]_ _[,][ {][π]_ _j_ _[∗]_ _[}]_ _[j][̸]_ [=] _[i]_ � _≥_ _J_ � _π_ _i_ _, {π_ _j_ _[∗]_ _[}]_ _[j][̸]_ [=] _[i]_ � _,_ _∀i ∈{_ 1 _, . . ., n}._ (9)


Due to symmetry, and assuming the KL terms vanish, the average win rate of the equilibrium policy
_π_ _[∗]_ against _n −_ 1 copies of itself is _n_ [1] [. That is,] _[ J]_ [ (] _[π]_ _[∗]_ _[,][ {][π]_ _[∗]_ _[}]_ _[j][̸]_ [=] _[i]_ [) =] _n_ [1] [, analogous to the two-player]


case.


The _duality gap_ quantifies how far a given policy _π_ is from the Nash policy _π_ _[∗]_ . Extending the
two-player definition to an _n_ -player setting, we define the set of opponent players as _O_ _π_ = _{π_ _j_ _}_ _[n]_ _j_ =1 _[−]_ [1] [.]
The duality gap in multiplayer games is then given by:



_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_


DualGap( _π_ ) := E _π_ _j_ _∈O_ _π_



_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_


max min _J_ ( _π_ _j_ _, π ∪_ _O_ _π_ _\ π_ _j_ ) _−_ min (10)
� _π_ _j_ _O_ _π_ _\π_ _j_ � _O_ _π_ _[J]_ [ (] _[π, O]_ _[π]_ [)] _[ .]_



_̸_

_̸_


_̸_


_̸_


_̸_


_̸_


_̸_

_̸_ _̸_


_̸_


_[̸]_ _[̸]_


_[̸]_


This gap quantifies the maximum advantage a player could gain by unilaterally deviating from _π_
against the worst-case configuration of opponents, relative to the minimum payoff _π_ could incur
if the opponents themselves deviate. Notably, the equilibrium condition is satisfied if and only if
DualGap ( _π_ _[∗]_ ) = 0, ensuring no player has an incentive to deviate unilaterally. Furthermore, if
DualGap( _π_ ) _≤_ _ϵ_, then _π_ is defined as an _ϵ_ -approximate Nash policy in the multiplayer setting.


4


Preprint, Under Review


**Multiplayer Nash Preference Optimization.** There are well-known algorithms that approximately
solve the Nash equilibrium in a constant-sum multiplayer game. In this work, we follow (Freund &
Schapire, 1999) to establish an iterative framework that can asymptotically converge to the optimal
policy on average. Given a learning rate _η_ of online mirror descent update, we start with a theoretical
analysis that conceptually solves the multiplayer game as follows [1] :


_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_



1
_n−_ 1

exp


_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_



 _η_

_n −_ 1

_̸_  _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_



� P � _y ≻_ _π_ _j_ [(] _[t]_ [)] _| x_ �

_̸_ _j_ = _̸_ _i_ 


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_



�

_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_






_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_



_π_ _i_ [(] _[t]_ [+1)] ( _y | x_ ) _∝_


_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_






_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_



 [�] _j_ = _̸_ _i_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_



_π_ _j_ [(] _[t]_ [)] [(] _[y][ |][ x]_ [)]

[�] _j_ = _̸_ _i_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_





_̸_  _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_



(11)

_̸_ _̸_ 


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_



_̸_ _̸_


Eq. 11 is an iterative framework that relies on the multiplicative weight update and enjoys a clear
structure. Initially, we have a base policy _π_ [(0)], usually from some supervised fine-tuned model _π_ ref .
In each iteration _t_, the updated policy _π_ [(] _[t]_ [+1)] is obtained from the reference policy _π_ [(] _[t]_ [)] following the
multiplicative weight update. Particularly, a response _y_ should have a higher probability weight if it
has a higher average advantage over the current policy _π_ [(] _[t]_ [)] . Equivalently, Eq. 11 can be written as

1

_π_ _i_ [(] _[t]_ [+1)] ( _y | x_ ) = Π _j_ = _̸_ _i_ _π_ _j_ [(] _[t]_ [)] [(] _[y][ |][ x]_ [)] _n−_ 1 exp � _n−η_ 1 [P] � _y ≻_ _π_ _j_ [(] _[t]_ [)] _| x_ �� _/Z_ _π_ ( _t_ ) ( _x_ ), where _Z_ _π_ ( _t_ ) ( _x_ ) is the

normalization factor (a.k.a, the partition function). Then for any fixed _x_ and _y_, each ideal update
policy _π_ _i_ [(] _[t]_ [+1)] should satisfy:


_̸_ _̸_


_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


1

_n −_ 1

_̸_ _̸_


_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


� log _[π]_ _i_ [(] _[t]_ [+1)] ( _y_ _| x_ )

_j_ = _̸_ _i_ _π_ _j_ [(] _[t]_ [)] [(] _[y][ |][ x]_ [)] _̸_


_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


� P � _y ≻_ _π_ _j_ [(] _[t]_ [)] _| x_ � _−_ log _Z_ _π_ ( _t_ ) _._ (12)

_̸_ _j_ = _̸_ _i_


_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


�

_̸_ _̸_


_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


_i_ _y_ _x_ = _η_
_̸_ _π_ _j_ [(] _[t]_ [)] [(] _[y][ |][ x]_ [)] _n −_ 1 _̸_


_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


Note that direct computation of _π_ [(] _[t]_ [+1)] involves a normalization factor, which is intractable for the
exponentially large response space _Y_ . To avoid computing this normalization factor, we consider the
logarithmic ratio between response pair _y_ and _y_ _[′]_, and define the function _h_ _t_ ( _π, y, y_ _[′]_ ) as:


_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_ _π_ _j_ [(] _[t]_ [)] [(] _[y]_ _[′]_ _[ |][ x]_ [)]


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_h_ _t_ � _π, y, y_ _[′]_ [�] = log _π_ _[π]_ ( [(] _y_ _[y]_ _[′]_ _[|]_ _|_ _[ x]_ _x_ [)] ) _[−]_ _n −_ 1 1

_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


�

_j_ = _̸_ _i_


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_ �


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


log _[π]_ _j_ [(] _[t]_ [)] [(] _[y][ |][ x]_ [)]


_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_ �


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_._ (13)


_̸_


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


From Eq.12, we know that the following equality holds for any response pair _y, y_ _[′]_ _∈_ Supp ( _π_ ref ):


_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_h_ _t_ � _π_ [(] _[t]_ [+1)] _, y, y_ _[′]_ [�] = _n −η_ 1

_̸_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


� P � _y ≻_ _π_ _j_ [(] _[t]_ [)] _| x_ � _−_ P � _y_ _[′]_ _≻_ _π_ _j_ [(] _[t]_ [)] _| x_ � (14)

_j_ = _̸_ _i_


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


Based on this observation, we define the loss function _L_ _t_ ( _π_ ) and update the policy _π_ [(] _[t]_ [+1)] as:


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


�

_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


� P � _y ≻_ _π_ _j_ [(] _[t]_ [)] � _−_ P � _y_ _[′]_ _≻_ _π_ _j_ [(] _[t]_ [)] �

_j_ = _̸_ _i_ 



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


 _h_ _t_ ( _π, y_ _w_ _, y_ _l_ ) _−_ _η_

_n −_ 1
 _̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_





_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_π_ [(] _[t]_ [+1)] _←_ argmin E _y_ _w_ _,y_ _l_ _∼D_ _t_

_π_ _̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_




 _̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_ 



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


2 []


_̸_ 



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


(15)


_̸_



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_


� �� �

_L_ _t_ ( _π_ )


It is clear to see that _π_ [(] _[t]_ [+1)] is the minimizer of _L_ _t_ ( _π_ ) since _L_ _t_ � _π_ [(] _[t]_ [+1)] [�] = 0 . Furthermore, in the
following lemma, we show that _π_ [(] _[t]_ [+1)] is the unique minimizer of _L_ _t_ within the policy class Π.

**Lemma 1.** _For each t ∈_ [ _T_ ] _, π_ _t_ +1 _in Eq. 15 is the unique minimizer of L_ _t_ ( _π_ ) _within_ Π _._


The proof is deferred to Appendix E.1. Moreover, we replace the tricky term P � _y ≻_ _π_ _j_ [(] _[t]_ [)] � with a
hyperparameter _η_ and propose the following loss to bypass it:



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_


� 2 [�]



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_


_L_ _[′]_ _t_ [(] _[π]_ [) =][ E] _y,y_ _[′]_ _∼π_ _t_ _, y_ _w_ _,y_ _l_ _∼λ_ P ( _y,y_ _[′]_ )



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_


_h_ _t_ ( _π, y_ _w_ _, y_ _l_ ) _−_ [1]

2 _η_

��



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_


_._ (16)



_̸_ _̸_


_̸_


_̸_ _̸_


_̸_


_̸_


_̸_


**Proposition 1.** _For any policy_ _π ∈_ Π _and any iteration_ _t ∈_ [ _T_ ] _,_ _L_ _[′]_ _t_ [(] _[π]_ [)] _[ is equivalent to]_ _[ L]_ _[t]_ [(] _[π]_ [)] _[,]_
_differing only by an additive constant that is independent of π._


See the proof in Appendix E.2. Here, the response pair ( _y, y_ _[′]_ ) is directly sampled from the current
policy _π_ [(] _[t]_ [)], which is crucial for the equivalence between _L_ _[′]_ _t_ [(] _[π]_ [)][ and] _[ L]_ _[t]_ [(] _[π]_ [)][.]


1 For notational conciseness and avoiding confusion, we use a superscript to denote time here, so that _π_ ( _t_ ) is
equivalent to _π_ _t_ .


5


Preprint, Under Review


Table 1: Time-dependent MNPO recovers many existing offline or online preference optimization
algorithms. We denote the target reward gap as _δ_ _r_ _⋆_ := _η_ ( _r_ _[⋆]_ ( _x, y_ 1 ) _−_ _r_ _[⋆]_ ( _x, y_ 2 )) . D [sq] and D [bwd]
represent the squared distance and backward Bernoulli KL divergence, respectively.














|Algorithm|Num. Players Opponents Importance Weights Dist. Target Reward Gap|
|---|---|
|SimPO<br>DPO<br>Distill-DPO<br>DNO<br>SPIN<br>SPPO<br>IPO<br>INPO|_n_ = 1<br>–<br>–<br>Dbwd<br>_∞_<br>_n_ = 2<br>_π_ref<br>_λj_ = 1<br>Dbwd<br>_∞_<br>_n_ = 2<br>_π_ref<br>_λj_ = 1<br>Dsq<br>_∞_<br>_n_ = 2<br>_πt_<br>_λj_ = 1<br>Dbwd<br>_∞_<br>_n_ = 2<br>_πt_<br>_λj_ =_ β_<br>Dbwd<br>_∞_<br>_n_ = 2<br>_πt_<br>_λj_ = 1<br>Dsq<br>_η_<br><br>b_P_ (_y ≻πt | x_)_ −_1<br>2<br><br>_n_ = 2<br>_π_ref<br>_λj_ = 1<br>Dsq<br>1<br>2_τ_<br>_n_ = 3<br>_πt, π_ref<br>_λj_ =<br>(<br>_τ_<br>_η_ _,_<br>if_ j_ =_ t_<br>_η−τ_<br>_η_ _,_<br>if_ j_ = 1<br>Dsq<br>1<br>2_τ_|



3.2 M ULTIPLAYER N ASH P REFERENCE O PTIMIZATION


**Reward-Enhanced MNPO.** While our framework is motivated by moving beyond the limitations
of purely scalar reward-based approaches, this does not preclude the beneficial incorporation of
reward information when available. The key distinction lies in how rewards are utilized: rather than
relying solely on reward-based rankings with implicit transitivity assumptions (as in classical RLHF),
MNPO can leverage reward information as auxiliary guidance while maintaining the flexibility to
handle non-transitive preferences through its game-theoretic structure.


Reward-aware preference optimization (RPO) (Sun et al., 2025) demonstrates how _quantitative_
reward signals can complement _qualitative_ preference comparisons. This approach aligns learned
implicit preference models with explicit reward models that provide graded assessments of response
quality. This shift allows MNPO to move beyond binary preference margins and instead minimize
discrepancies between the learned reward function _r_ _π_ _θ_ ( _x, y_ ) and the target explicit reward model
_r_ _[⋆]_ ( _x, y_ ) . Concretely, instead of optimizing only the preference order between two responses, RPO
defines the loss over preference pairs as:


_L_ [D] RPO � _π_ _θ_ _,_ � _x, y_ [1] _, y_ [2] [�] _| r_ _[⋆]_ _, π_ ref _, β, η_ � =: D � _r_ _π_ _θ_ � _x, y_ [1] [�] _−_ _r_ _π_ _θ_ � _x, y_ [2] [�] _∥ηr_ _[⋆]_ [�] _x, y_ [1] [�] _−_ _ηr_ _[⋆]_ [�] _x, y_ [2] [��] _,_ (17)


where � _x, y_ [1] _, y_ [2] [�] represents a preference pair and the distance metric D : R _×_ R _→_ R _[∗]_ measures
alignment between the model’s implicit reward differences and the scaled reference reward differences.
The hyperparameters _η ∈_ R _[∗]_ and _β ∈_ R _[∗]_ control the reward scale and regularization, respectively.
This formulation directly encourages the policy _π_ _θ_ to internalize human-aligned reward values,
bridging qualitative preference optimization with quantitative reward modeling.


Importantly, the loss function Eq. 16 can be interpreted as a special case of RPO under a squared distance metric D [sq] . Specifically, _L_ _[′]_ _t_ [(] _[π]_ [)] [ employs a learned reward model] _[ r]_ _[π]_ _θ_ [=][ E] _[π]_ _j_ �log _π_ _[π]_ _j_ [(] ( _[y]_ _y_ _[|]_ _|_ _[x]_ _x_ [)] ) � and a

1
reference reward model gap _δ_ _r_ _⋆_ := _η_ ( _r_ _[⋆]_ ( _x, y_ 1 ) _−_ _r_ _[⋆]_ ( _x, y_ 2 )) = 2 _η_ [. This connection highlights how]
integrating reward-awareness into multiplayer preference games enhances stability, interpretability,
and alignment fidelity.


**Time-dependent Multiplayers** A central challenge in multiplayer optimization lies in defining

_n−_ 1
and updating the set of opponent players � _π_ _j_ [(] _[t]_ [)] � _j_ =1 [in Eq.14. Inspired by recent iterative preference]

optimization methods such as DNO (Rosset et al., 2024), SPIN (Chen et al., 2024), and INPO (Zhang
et al., 2025b), which typically rely on past policy iterations (e.g., _π_ ref and _π_ [(] _[t][−]_ [1)] ) to construct
opponents, we adopt a time-dependent opponent selection mechanism.


At any iteration _t_, we construct the opponent set from a mixture of recent historical policies _{π_ _t−j_ _}_ _[t]_ _j_ =0
( _n ≤_ _t_ + 1 ), weighted by coefficients _λ_ _j_ with _λ_ _j_ _∈_ [0 _,_ 1] and optionally [�] _j_ _[λ]_ _[j]_ _[ ≤]_ [1] [. The resulting]
time-dependent MNPO (TD-MNPO) loss is formulated as follows:



_π_ ( _y_ _l_ _| x_ ) _[−]_



_π_ _t−j_ ( _y_ _l_ _| x_ )





 _,_ (18)



_L_ _[t,]_ TD-MNPO [D] [(] _[π][|][β,][ {][λ]_ _[j]_ _[}][, η]_ [) =][ D]








_[|][ x]_ [)]
log _[π]_ [(] _[y]_ _[w]_
 _π_ ( _y_ _l_ _| x_ )



_n−_ 2
�




_[|][ x]_ [)]

� _j_ =0 _λ_ _j_ log _[π]_ _π_ _[t]_ _t_ _[−]_ _−_ _[j]_ _j_ [(] ( _[y]_ _y_ _[w]_ _l_ _| x_ )



_ηδ_ _⋆_
����



6


Preprint, Under Review


where _δ_ _[⋆]_ encodes the target reward gap. By blending multiple past policies, this formulation stabilizes
training, mitigates overfitting to transient fluctuations, and preserves temporal consistency.


**Connections to Existing RLHF.** This unified MNPO formulation in Eq. 18 reveals that many
preference optimization algorithms can be recovered as special cases by varying the number of
players _n_, choice of opponents _O_ _π_, distance metric D, and target reward gap _δ_ _[⋆]_ .


For instance, DPO emerges by setting _n_ = 2, _O_ _π_ = _π_ ref, and _λ_ _j_ = 1 . Table 1 summarizes these
reductions, showing how time-dependent MNPO unifies offline and online preference optimization
under one principled framework. We provide a broader overview of RLHF objectives in Appendix D.


Compared to static reference-based approaches, the reward-aware multiplayer formulation offers:
_(i) Smoother policy evolution._ Unlike methods that rely solely on the most recent past policy,
MNPO gradually incorporates multiple past policies, preventing abrupt shifts and stabilizing policy
updates. _(ii)_ Greater robustness. By a weighted mixture of historical opponents, MNPO mitigates
the risk of overfitting to transient fluctuations in recent iterations. _(iii) Unified interpretation._ TDMNPO seamlessly extends existing approaches into a unified formulation, allowing for flexible
adaptation to different training scenarios. _(iv) Stable convergence._ . The weighting scheme ensures
that recent policies exert a stronger influence while preserving the broader learning trajectory, leading
to more stable convergence. By dynamically leveraging historical policies as opponent players,
TD-MNPO enhances preference optimization, making it more adaptable and robust in evolving
learning environments. The pseudo-algorithm is described in Appendix B.


4 E XPERIMENTAL S ETUP


**Models and Training Settings.** We implement an online RLHF framework (Dong et al., 2024) with
Gemma-2-9B-it (Team et al., 2024) as the base model. Our MNPO training consists of _T_ = 3
iterations, where each iteration generates responses from the current policy on a fresh prompt set and
updates the policy using preference feedback. To eliminate the need for costly human annotations, we
employ the reward model ArmoRM-Llama3-8B-v0.1 (Wang et al., 2024a) to provide preference
signals. Hyperparameter optimization proves critical, as optimal configurations vary both across
different base models and between iterations of the same model. Through empirical analysis, we find
that maintaining _β_ within the range [0 _._ 01 _,_ 10] consistently produces strong results. Furthermore, we
observe that gradually increasing _β_ throughout training effectively mitigates training degradation
while enabling continued model improvement. Complete implementation details and hyperparameter
specifications are provided in Appendix C.


**Evaluation Benchmarks.** We evaluate primarily on three widely used open-ended instructionfollowing benchmarks: MT-Bench (Zheng et al., 2023), AlpacaEval 2 (Li et al., 2023), and ArenaHard v0.1 (Li et al., 2024). As suggested by Dubois et al. (2024), we report the win rate (WR) for
Arena-Hard and the length-controlled (LC) WR for AlpacaEval 2, as judged by GPT-5-mini rather
than the outdated GPT-4 Turbo (Preview-1106).


Since RLHF alignment is known to sometimes degrade reasoning, calibration, and factual accuracy (Ouyang et al., 2022; Dong et al., 2024), we further assess performance on a broader set of
eleven academic benchmarks. These benchmarks span multiple abilities, including explicit instruction
following (Zhou et al., 2023), general knowledge (Clark et al., 2018; Rein et al., 2024; Hendrycks
et al., 2020), commonsense reasoning (Sakaguchi et al., 2021; Lin et al., 2021; Zellers et al., 2019),
and math/coding problem solving (Lewkowycz et al., 2022; Chen et al., 2021).


In addition, we compare MNPO with a group of open-source LLMs, including
LLaMA-3.1-8B-it (Dubey et al., 2024), Tulu-2-DPO-70B, LLaMA-3.3-70B-it,
Mixtral-8x22B-it, and Qwen3-235B-it (Yang et al., 2025), and closed-source LLMs such
as Gemini-2.5-Pro, GPT-5, and Claude-Sonnet-4.


5 E MPIRICAL R ESULTS


**Instruction-Following and Preference Alignment.** Table 2 presents the performance of MNPO
compared to existing preference optimization methods on three widely-used instruction-following


7


Preprint, Under Review


Table 2: Performance of various models on instruction-following and preference-alignment benchmarks (AlpacaEval 2.0, Arena-Hard, and MT-Bench), evaluated using GPT-5-mini as the judge.

|Model|Size|AlpacaEval 2.0 Arena-Hard MT-Bench|
|---|---|---|
|SFT Model<br>DPO<br>SimPO<br>SPPO<br>INPO|9B<br>9B<br>9B<br>9B<br>9B|50.15<br>44.97<br>6.49<br>54.35<br>45.63<br>6.87<br>55.16<br>45.04<br>6.87<br>55.97<br>43.89<br>6.86<br>56.09<br>48.03<br>6.95|
|MNPO<br>9B<br>**57.27**<br>**52.26**<br>**7.03**|MNPO<br>9B<br>**57.27**<br>**52.26**<br>**7.03**|MNPO<br>9B<br>**57.27**<br>**52.26**<br>**7.03**|
|LLaMA-3.1-8B-it<br>8B<br>5.24<br>39.16<br>5.37<br>Tulu-2-DPO-70B<br>70B<br>8.82<br>27.88<br>5.91<br>LLaMA-3.3-70B-it<br>70B<br>29.44<br>59.21<br>7.73<br>Mixtral-8x22B-it<br>141B<br>9.57<br>40.98<br>6.90<br>Qwen3-235B-it<br>235B<br>84.97<br>88.71<br>8.27|LLaMA-3.1-8B-it<br>8B<br>5.24<br>39.16<br>5.37<br>Tulu-2-DPO-70B<br>70B<br>8.82<br>27.88<br>5.91<br>LLaMA-3.3-70B-it<br>70B<br>29.44<br>59.21<br>7.73<br>Mixtral-8x22B-it<br>141B<br>9.57<br>40.98<br>6.90<br>Qwen3-235B-it<br>235B<br>84.97<br>88.71<br>8.27|LLaMA-3.1-8B-it<br>8B<br>5.24<br>39.16<br>5.37<br>Tulu-2-DPO-70B<br>70B<br>8.82<br>27.88<br>5.91<br>LLaMA-3.3-70B-it<br>70B<br>29.44<br>59.21<br>7.73<br>Mixtral-8x22B-it<br>141B<br>9.57<br>40.98<br>6.90<br>Qwen3-235B-it<br>235B<br>84.97<br>88.71<br>8.27|
|OpenAI/GPT-5<br>-<br>72.80<br>41.42<br>8.46<br>Anthropic/Claude-Sonnet-4<br>-<br>62.24<br>77.58<br>8.26<br>Google/Gemini-2.5-Pro<br>-<br>90.93<br>86.98<br>7.78|OpenAI/GPT-5<br>-<br>72.80<br>41.42<br>8.46<br>Anthropic/Claude-Sonnet-4<br>-<br>62.24<br>77.58<br>8.26<br>Google/Gemini-2.5-Pro<br>-<br>90.93<br>86.98<br>7.78|OpenAI/GPT-5<br>-<br>72.80<br>41.42<br>8.46<br>Anthropic/Claude-Sonnet-4<br>-<br>62.24<br>77.58<br>8.26<br>Google/Gemini-2.5-Pro<br>-<br>90.93<br>86.98<br>7.78|



Table 3: Model performance on instruction, knowledge, and commonsense benchmarks.

|Instruction Knowledge Commonsense<br>Model AVG<br>IFEval GPQA MMLU ARC HellaSwag TruthfulQA Winogrande|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|SFT Model<br>DPO<br>SimPO<br>SPPO<br>INPO|72.27<br>72.96<br>73.79<br>75.47<br>73.20|28.28<br>75.35<br>91.29<br>29.29<br>75.77<br>91.26<br>32.32<br>76.79<br>91.09<br>26.26<br>75.37<br>91.17<br>27.78<br>74.79<br>91.07|80.30<br>70.75<br>73.72<br>80.37<br>71.24<br>73.88<br>78.90<br>63.40<br>72.93<br>80.10<br>71.48<br>73.48<br>80.22<br>71.24<br>73.48|70.28<br>70.68<br>69.60<br>70.19<br>70.25|
|MNPO|73.94|33.33<br>75.63<br>91.15|80.18<br>70.26<br>73.09|**71.08**|



benchmarks: AlpacaEval 2.0 (Length-Controlled Win Rate, %), Arena-Hard (Win Rate, %), and
MT-Bench (Score/10). All models were evaluated using GPT-5-mini as the judge. MNPO consistently
outperforms all baseline methods across all three benchmarks. On AlpacaEval 2.0, MNPO achieves a
score of 57.27, representing improvements of 2.92 points over DPO (54.35), 2.11 points over SimPO
(55.16), 1.30 points over SPPO (55.97), and 1.18 points over INPO (56.09). The improvements are
even more pronounced on Arena-Hard, where MNPO scores 52.26 compared to the next best method
INPO at 48.03, representing a 4.23-point improvement. Notably, on this challenging benchmark,
MNPO not only excels over other preference optimization algorithms but also demonstrates strong
competitiveness against much larger open-source fine-tuned models and even lastest closed-source
models. It surpasses prominent models like Tulu2-DPO (70B) and Mixtral-it (141B), and, surprisingly,
even outperforms GPT-5. On MT-Bench, MNPO achieves 7.03, outperforming all baselines, with the
closest competitor being INPO at 6.95. These results demonstrate that the multiplayer formulation in
MNPO provides significant advantages for instruction-following tasks. The consistent improvements
across all three benchmarks suggest that the framework’s ability to handle diverse preferences
and non-transitive relationships leads to better alignment with human expectations in open-ended
generation tasks.


**Knowledge and Reasoning Capabilities.** Table 3 evaluates model performance on academic benchmarks covering instruction following, knowledge, and commonsense reasoning. The results show
that MNPO maintains strong performance across diverse cognitive tasks while achieving preference
alignment. MNPO achieves the highest average score of 71.08 across all benchmarks, outperforming
the SFT baseline (70.28) and all other preference optimization methods. Notably, MNPO achieves
the best performance on GPQA (33.33), demonstrating strong graduate-level reasoning capabilities.
The method also performs competitively on instruction-following (IFEval: 73.94) and maintains
solid performance on knowledge benchmarks like MMLU (75.63) and commonsense reasoning
tasks. Importantly, unlike some preference optimization methods that show degradation on certain


8


Preprint, Under Review


Table 4: Model performance on math and coding benchmarks.

|Math Code<br>Model AVG<br>GSM8K Minerva-Math AIME-24 HumanEval|Col2|Col3|Col4|
|---|---|---|---|
|SFT Model<br>DPO<br>SimPO<br>SPPO<br>INPO|81.96<br>44.12<br>0<br>82.03<br>45.96<br>0<br>82.56<br>43.38<br>0<br>82.11<br>47.43<br>0<br>82.94<br>46.32<br>0|60.37<br>59.76<br>57.32<br>59.76<br>59.15|46.61<br>46.94<br>45.82<br>47.33<br>47.10|
|MNPO|82.64<br>44.85<br>3.33|61.59|**48.10**|



academic benchmarks (e.g., SimPO’s drop to 63.40 on TruthfulQA), MNPO maintains relatively
stable performance across all domains. This suggests that the multiplayer framework helps preserve
the model’s foundational capabilities while improving preference alignment.


**Mathematical and Coding Performance.** Table 4 presents results on mathematical reasoning and
coding benchmarks. MNPO achieves the highest average score of 48.10 across math and coding
tasks, outperforming all baseline methods, including SPPO (47.33) and INPO (47.10). On the
challenging AIME-24 benchmark, MNPO is the only method to achieve non-zero performance (3.33),
while all other methods including the SFT baseline score 0. This demonstrates MNPO’s superior
capability in handling complex mathematical reasoning tasks. On HumanEval, MNPO achieves
61.59, representing the best coding performance among all methods. The results on GSM8K and
Minerva-Math show that MNPO maintains competitive performance with existing methods while
achieving superior results on the most challenging tasks. This pattern suggests that the multiplayer
optimization framework is particularly beneficial for complex reasoning tasks that require handling
multiple solution strategies or approaches.


6 R ELATED W ORK


**Reward-model–based RLHF.** Classical RLHF trains a reward model on human preference data
and optimizes a policy with KL-regularized policy gradients (e.g., PPO) (Christiano et al., 2017;
Ouyang et al., 2022; Bai et al., 2022; Schulman et al., 2017). While effective, PPO-style updates
suffer from instability and high memory cost. To address this, GRPO removes the critic for more
stable and memory-efficient training at scale (e.g., DeepSeek-R1) (Shao et al., 2024; Guo et al.,
2025), and DAPO further improves sample efficiency through dynamic sampling and refined loss
objectives (Yu et al., 2025). VAPO shows that value learning can strengthen RLHF when done
properly (Yuan et al., 2025). Nonetheless, optimizing against imperfect reward proxies remains
vulnerable to reward hacking (Weng, 2024; Wen et al., 2024).


**RLHF with General Preference.** DPO bypasses reward modeling by directly optimizing a logodds margin between preferred and dispreferred responses (Rafailov et al., 2023). This idea has
inspired a family of extensions, including IPO (Azar et al., 2024), KTO (Ethayarajh et al., 2024),
SimPO (Meng et al., 2024), and WPO (Zhou et al., 2024), which refine the constraint, scaling, or
sampling strategy. Iterative and online forms introduce exploration and continual updates (Xiong
et al., 2023; Dong et al., 2024; Xie et al., 2024), but most remain limited to static pairwise supervision.


7 C ONCLUSION


We introduce Multiplayer Nash Preference Optimization, extending Nash learning from human
feedback to multiplayer settings. Our framework admits well-defined Nash equilibria and unifies
existing preference optimization methods as special cases. Empirically, MNPO outperforms baselines
across instruction-following and reasoning benchmarks. These results validate that multiplayer
formulations better capture heterogeneous human preferences and provide more robust alignment for
LLMs.


9


Preprint, Under Review


R EFERENCES


Mohammad Gheshlaghi Azar, Zhaohan Daniel Guo, Bilal Piot, Remi Munos, Mark Rowland, Michal
Valko, and Daniele Calandriello. A general theoretical paradigm to understand learning from
human preferences. In _International Conference on Artificial Intelligence and Statistics_, pp.
4447–4455. PMLR, 2024.


Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain,
Stanislav Fort, Deep Ganguli, Tom Henighan, et al. Training a helpful and harmless assistant with
reinforcement learning from human feedback. _arXiv preprint arXiv:2204.05862_, 2022.


Ralph Allan Bradley and Milton E Terry. Rank analysis of incomplete block designs: I. the method
of paired comparisons. _Biometrika_, 39(3/4):324–345, 1952.


Daniele Calandriello, Daniel Guo, Remi Munos, Mark Rowland, Yunhao Tang, Bernardo Avila Pires,
Pierre Harvey Richemond, Charline Le Lan, Michal Valko, Tianqi Liu, et al. Human alignment of
large language models through online preference optimisation. _arXiv preprint arXiv:2403.08635_,
2024.


Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared
Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. Evaluating large
language models trained on code. _arXiv preprint arXiv:2107.03374_, 2021.


Zixiang Chen, Yihe Deng, Huizhuo Yuan, Kaixuan Ji, and Quanquan Gu. Self-play fine-tuning
converts weak language models to strong language models. _arXiv preprint arXiv:2401.01335_,
2024.


Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei. Deep
reinforcement learning from human preferences. _Advances in neural information processing_
_systems_, 30, 2017.


Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot, Ashish Sabharwal, Carissa Schoenick, and
Oyvind Tafjord. Think you have solved question answering? try arc, the ai2 reasoning challenge.
_arXiv preprint arXiv:1803.05457_, 2018.


Ganqu Cui, Lifan Yuan, Ning Ding, Guanming Yao, Wei Zhu, Yuan Ni, Guotong Xie, Zhiyuan Liu,
and Maosong Sun. UltraFeedback: Boosting language models with high-quality feedback. _arXiv_
_preprint arXiv:2310.01377_, 2023.


Gerard Debreu. Individual choice behavior: A theoretical analysis, 1960.


Hanze Dong, Wei Xiong, Bo Pang, Haoxiang Wang, Han Zhao, Yingbo Zhou, Nan Jiang, Doyen
Sahoo, Caiming Xiong, and Tong Zhang. Rlhf workflow: From reward modeling to online rlhf.
_arXiv preprint arXiv:2405.07863_, 2024.


Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha
Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models.
_arXiv e-prints_, pp. arXiv–2407, 2024.


Yann Dubois, Balázs Galambosi, Percy Liang, and Tatsunori B Hashimoto. Length-controlled
alpacaeval: A simple way to debias automatic evaluators. _arXiv preprint arXiv:2404.04475_, 2024.


Kawin Ethayarajh, Winnie Xu, Niklas Muennighoff, Dan Jurafsky, and Douwe Kiela. Kto: Model
alignment as prospect theoretic optimization. _arXiv preprint arXiv:2402.01306_, 2024.


Adam Fisch, Jacob Eisenstein, Vicky Zayats, Alekh Agarwal, Ahmad Beirami, Chirag Nagpal, Pete
Shaw, and Jonathan Berant. Robust preference optimization through reward model distillation.
_arXiv preprint arXiv:2405.19316_, 2024.


Yoav Freund and Robert E Schapire. Adaptive game playing using multiplicative weights. _Games_
_and Economic Behavior_, 29(1-2):79–103, 1999.


Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms
via reinforcement learning. _arXiv preprint arXiv:2501.12948_, 2025.


10


Preprint, Under Review


Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and
Jacob Steinhardt. Measuring massive multitask language understanding. _arXiv preprint_
_arXiv:2009.03300_, 2020.


Jiwoo Hong, Noah Lee, and James Thorne. Orpo: Monolithic preference optimization without
reference model. _arXiv preprint arXiv:2403.07691_, 2024.


Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, et al. Solving quantitative
reasoning problems with language models. _Advances in neural information processing systems_,
35:3843–3857, 2022.


Tianle Li, Wei-Lin Chiang, Evan Frick, Lisa Dunlap, Banghua Zhu, Joseph E Gonzalez, and Ion
Stoica. From live data to high-quality benchmarks: The arena-hard pipeline. _Blog post.[Accessed_
_07-02-2025]_, 2024.


Xuechen Li, Tianyi Zhang, Yann Dubois, Rohan Taori, Ishaan Gulrajani, Carlos Guestrin, Percy
Liang, and Tatsunori B Hashimoto. Alpacaeval: An automatic evaluator of instruction-following
models, 2023.


Stephanie Lin, Jacob Hilton, and Owain Evans. Truthfulqa: Measuring how models mimic human
falsehoods. _arXiv preprint arXiv:2109.07958_, 2021.


Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint_
_arXiv:1711.05101_, 2017.


Xufei Lv, Haoyuan Sun, Xuefeng Bai, Min Zhang, Houde Liu, and Kehai Chen. The hidden link
between rlhf and contrastive learning. _arXiv preprint arXiv:2506.22578_, 2025.


Yu Meng, Mengzhou Xia, and Danqi Chen. Simpo: Simple preference optimization with a referencefree reward. _Advances in Neural Information Processing Systems_, 37:124198–124235, 2024.


Rémi Munos, Michal Valko, Daniele Calandriello, Mohammad Gheshlaghi Azar, Mark Rowland,
Zhaohan Daniel Guo, Yunhao Tang, Matthieu Geist, Thomas Mesnard, Andrea Michi, et al. Nash
learning from human feedback. _arXiv preprint arXiv:2312.00886_, 18, 2023.


Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong
Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. Training language models to follow
instructions with human feedback. _Advances in neural information processing systems_, 35:27730–
27744, 2022.


Junshu Pan, Wei Shen, Shulin Huang, Qiji Zhou, and Yue Zhang. Pre-dpo: Improving data utilization
in direct preference optimization using a guiding reference model. _arXiv preprint arXiv:2504.15843_,
2025.


Ryan Park, Rafael Rafailov, Stefano Ermon, and Chelsea Finn. Disentangling length from quality in
direct preference optimization. _arXiv preprint arXiv:2403.19159_, 2024.


Robin L Plackett. The analysis of permutations. _Journal of the Royal Statistical Society Series C:_
_Applied Statistics_, 24(2):193–202, 1975.


Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea
Finn. Direct preference optimization: Your language model is secretly a reward model. _Advances_
_in Neural Information Processing Systems_, 36:53728–53741, 2023.


David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani,
Julian Michael, and Samuel R Bowman. Gpqa: A graduate-level google-proof q&a benchmark. In
_First Conference on Language Modeling_, 2024.


Corby Rosset, Ching-An Cheng, Arindam Mitra, Michael Santacroce, Ahmed Awadallah, and
Tengyang Xie. Direct nash optimization: Teaching language models to self-improve with general
preferences. _arXiv preprint arXiv:2404.03715_, 2024.


11


Preprint, Under Review


Keisuke Sakaguchi, Ronan Le Bras, Chandra Bhagavatula, and Yejin Choi. Winogrande: An
adversarial winograd schema challenge at scale. _Communications of the ACM_, 64(9):99–106,
2021.


John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy
optimization algorithms. _arXiv preprint arXiv:1707.06347_, 2017.


Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
Mingchuan Zhang, YK Li, Y Wu, et al. Deepseekmath: Pushing the limits of mathematical
reasoning in open language models. _arXiv preprint arXiv:2402.03300_, 2024.


Joar Skalse, Nikolaus Howe, Dmitrii Krasheninnikov, and David Krueger. Defining and characterizing
reward gaming. _Advances in Neural Information Processing Systems_, 35:9460–9471, 2022.


Samuel Sokota, Ryan D’Orazio, J Zico Kolter, Nicolas Loizou, Marc Lanctot, Ioannis Mitliagkas,
Noam Brown, and Christian Kroer. A unified approach to reinforcement learning, quantal response
equilibria, and two-player zero-sum games. _arXiv preprint arXiv:2206.05825_, 2022.


Shengyang Sun, Yian Zhang, Alexander Bukharin, David Mosallanezhad, Jiaqi Zeng, Soumye
Singhal, Gerald Shen, Adithya Renduchintala, Tugrul Konuk, Yi Dong, et al. Reward-aware
preference optimization: A unified mathematical framework for model alignment. _arXiv preprint_
_arXiv:2502.00203_, 2025.


Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut,
Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. Gemini: a family of highly
capable multimodal models. _arXiv preprint arXiv:2312.11805_, 2023.


Gemma Team, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya
Bhupatiraju, Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, et al.
Gemma 2: Improving open language models at a practical size. _arXiv preprint arXiv:2408.00118_,
2024.


ModelScope Team. EvalScope: Evaluation framework for large models, 2024. URL [https:](https://github.com/modelscope/evalscope)
[//github.com/modelscope/evalscope.](https://github.com/modelscope/evalscope)


Jeremy Tien, Jerry Zhi-Yang He, Zackory Erickson, Anca D Dragan, and Daniel S Brown. Causal
confusion and reward misidentification in preference-based reward learning. _arXiv preprint_
_arXiv:2204.06601_, 2022.


Chaoqi Wang, Yibo Jiang, Chenghao Yang, Han Liu, and Yuxin Chen. Beyond reverse kl: Generalizing direct preference optimization with diverse divergence constraints. _arXiv preprint_
_arXiv:2309.16240_, 2023.


Haoxiang Wang, Wei Xiong, Tengyang Xie, Han Zhao, and Tong Zhang. Interpretable preferences
via multi-objective reward modeling and mixture-of-experts. In _EMNLP_, 2024a.


Mingzhi Wang, Chengdong Ma, Qizhi Chen, Linjian Meng, Yang Han, Jiancong Xiao, Zhaowei
Zhang, Jing Huo, Weijie J Su, and Yaodong Yang. Magnetic preference optimization: Achieving
last-iterate convergence for language model alignment. _arXiv preprint arXiv:2410.16714_, 2024b.


Jiaxin Wen, Ruiqi Zhong, Akbir Khan, Ethan Perez, Jacob Steinhardt, Minlie Huang, Samuel R
Bowman, He He, and Shi Feng. Language models learn to mislead humans via rlhf. _arXiv preprint_
_arXiv:2409.12822_, 2024.


Lilian Weng. Reward hacking in reinforcement learning. _lilianweng.github.io_, Nov 2024. URL
[https://lilianweng.github.io/posts/2024-11-28-reward-hacking/.](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/)


Yue Wu, Zhiqing Sun, Huizhuo Yuan, Kaixuan Ji, Yiming Yang, and Quanquan Gu. Self-play
preference optimization for language model alignment. _arXiv preprint arXiv:2405.00675_, 2024.


Tengyang Xie, Dylan J Foster, Akshay Krishnamurthy, Corby Rosset, Ahmed Awadallah, and
Alexander Rakhlin. Exploratory preference optimization: Harnessing implicit q*-approximation
for sample-efficient rlhf. _arXiv preprint arXiv:2405.21046_, 2024.


12


Preprint, Under Review


Wei Xiong, Hanze Dong, Chenlu Ye, Ziqi Wang, Han Zhong, Heng Ji, Nan Jiang, and Tong Zhang.
Iterative preference learning from human feedback: Bridging theory and practice for rlhf under
kl-constraint. _arXiv preprint arXiv:2312.11456_, 2023.


Haoran Xu, Amr Sharaf, Yunmo Chen, Weiting Tan, Lingfeng Shen, Benjamin Van Durme, Kenton
Murray, and Young Jin Kim. Contrastive preference optimization: Pushing the boundaries of llm
performance in machine translation. _arXiv preprint arXiv:2401.08417_, 2024.


An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang
Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_,
2025.


Chenlu Ye, Wei Xiong, Yuheng Zhang, Hanze Dong, Nan Jiang, and Tong Zhang. Online iterative
reinforcement learning from human feedback with general preference model. _Advances in Neural_
_Information Processing Systems_, 37:81773–81807, 2024.


Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Tiantian Fan, Gaohong
Liu, Lingjun Liu, Xin Liu, et al. Dapo: An open-source llm reinforcement learning system at scale.
_arXiv preprint arXiv:2503.14476_, 2025.


Hongyi Yuan, Zheng Yuan, Chuanqi Tan, Wei Wang, Songfang Huang, and Fei Huang. Rrhf: Rank
responses to align language models with human feedback. _Advances in Neural Information_
_Processing Systems_, 36:10935–10950, 2023.


Yufeng Yuan, Qiying Yu, Xiaochen Zuo, Ruofei Zhu, Wenyuan Xu, Jiaze Chen, Chengyi Wang,
TianTian Fan, Zhengyin Du, Xiangpeng Wei, et al. Vapo: Efficient and reliable reinforcement
learning for advanced reasoning tasks. _arXiv preprint arXiv:2504.05118_, 2025.


Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi. Hellaswag: Can a machine
really finish your sentence? _arXiv preprint arXiv:1905.07830_, 2019.


Yuheng Zhang, Dian Yu, Tao Ge, Linfeng Song, Zhichen Zeng, Haitao Mi, Nan Jiang, and Dong Yu.
Improving llm general preference alignment via optimistic online mirror descent. _arXiv preprint_
_arXiv:2502.16852_, 2025a.


Yuheng Zhang, Dian Yu, Baolin Peng, Linfeng Song, Ye Tian, Mingyue Huo, Nan Jiang, Haitao
Mi, and Dong Yu. Iterative nash policy optimization: Aligning LLMs with general preferences
via no-regret learning. In _The Thirteenth International Conference on Learning Representations_,
[2025b. URL https://openreview.net/forum?id=Pujt3ADZgI.](https://openreview.net/forum?id=Pujt3ADZgI)


Yao Zhao, Rishabh Joshi, Tianqi Liu, Misha Khalman, Mohammad Saleh, and Peter J Liu. Slic-hf:
Sequence likelihood calibration with human feedback. _arXiv preprint arXiv:2305.10425_, 2023.


Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang,
Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al. Judging llm-as-a-judge with mt-bench and
chatbot arena. _Advances in neural information processing systems_, 36:46595–46623, 2023.


Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny
Zhou, and Le Hou. Instruction-following evaluation for large language models. _arXiv preprint_
_arXiv:2311.07911_, 2023.


Runlong Zhou, Maryam Fazel, and Simon S Du. Extragradient preference optimization (egpo):
Beyond last-iterate convergence for nash learning from human feedback. _arXiv preprint_
_arXiv:2503.08942_, 2025.


Wenxuan Zhou, Ravi Agrawal, Shujian Zhang, Sathish Reddy Indurthi, Sanqiang Zhao, Kaiqiang
Song, Silei Xu, and Chenguang Zhu. Wpo: Enhancing rlhf with weighted preference optimization.
_arXiv preprint arXiv:2406.11827_, 2024.


13


Preprint, Under Review


A A DDITIONAL R ELATED W ORK ON G AME - THEORETIC RLHF


Another perspective casts preference optimization as a game between the model and its opponents,
where equilibrium-seeking methods provide stronger last-iterate guarantees. Self-play methods
like SPIN (Chen et al., 2024), SPPO (Wu et al., 2024), and INPO (Zhang et al., 2025b) use noregret dynamics, while Pre-DPO (Pan et al., 2025) and MPO (Wang et al., 2024b) adapt mirror
descent. More recent methods, such as ONPO (Zhang et al., 2025a) and EGPO (Zhou et al., 2025),
introduce optimism and extragradient techniques for stable convergence under noisy preferences.
These advances primarily focus on two-player games but highlight the importance of equilibrium
views in preference optimization. Extending RLHF to multiplayer interactions, as pursued by
MNPO, generalizes beyond pairwise dynamics and opens the door to richer equilibrium structures
for alignment.


B P SEUDO -A LGORITHM OF MNPO


**Algorithm 1** Multiplayer Nash Preference Optimization (MNPO)

1: **Require:** Number of iterations _T_, distance metric D, weight coefficients _{λ_ _j_ _}_, reward scaling
parameter _η_, regularization parameter _β_, external policy _{π_ _j_ _}_, reference policy _π_ ref, policy class
Π, preference oracle P.
2: **for** iteration _t_ = 1 _,_ 2 _, . . ., T_ **do**
_m_
3: Use current policy _π_ _t_ to generate response pairs � _y_ _i_ [1] _[, y]_ _i_ [2] � _i_ =1 [where] _[ y]_ _i_ [1] _[, y]_ _i_ [2] _[∼]_ _[π]_ _[t]_ [.]

4: Query the preference oracle P to get the preference dataset _D_ _t_ = � _y_ _i_ [+] _[, y]_ _i_ _[−]_ � _mi_ =1 [.]

5: Calculate _π_ _t_ +1 as: _π_ _t_ +1 _←_ argmin _L_ _[t,]_ TD-MNPO [D]
_π∈_ Π

6: **end for**
7: **Output** _π_ _T_ +1


C E XPERIMENTAL D ETAILS


**Hardware and Implementation** All experiments are conducted on 8 NVIDIA H100 GPUs with
96GB memory. For the implemented algorithms, DPO (Rafailov et al., 2023) is trained using the
official Hugging Face DPO Trainer, while SimPO (Meng et al., 2024) [2] and SPPO (Wu et al., 2024) [3]
follow their official GitHub implementations. INPO (Zhang et al., 2025b) is reproduced according to
the settings described in the paper.


**Hyperparameters** For MNPO, we adopt hyperparameters consistent with SimPO and INPO,
using a cosine learning-rate scheduler with a peak learning rate of 5 _×_ 10 _[−]_ [7], a warmup ratio
of 0.1, and a global batch size of 128. The optimizer is AdamW (Loshchilov & Hutter, 2017)
without weight decay. We further perform a grid search for history weights at timesteps 1 and
2, selecting from _{_ 0 _,_ 0 _._ 1 _,_ 0 _._ 333 _,_ 0 _._ 5 _,_ 0 _._ 667 _,_ 0 _._ 9 _}_ . In addition, we perform a grid search for _η_ over
_{_ 0 _._ 1 _,_ 0 _._ 01 _,_ 0 _._ 0075 _,_ 0 _._ 005 _,_ 0 _._ 002 _}_, and set _η_ = 0 _._ 0075.


**Training Data** For training data, we use Gemma2-Ultrafeedback-Armorm (Cui et al., 2023) [4],
which contains approximately 60K training samples and 2K test samples. We retain both prompts
and responses in iteration 1, while only prompts are used in iterations 2 and 3.


**Evaluation Framework** For evaluation, we adopt the EvalScope framework (Team, 2024) [5] (version
1.0.2) across all datasets in Tables 3 and 4, and also applied it for AlpacaEval 2.0 and Arena-Hard in
Table 2. MT-Bench [6] is tested and implemented following its official GitHub repository. The LLM


2 [https://github.com/princeton-nlp/SimPO](https://github.com/princeton-nlp/SimPO)
3 [https://github.com/uclaml/SPPO](https://github.com/uclaml/SPPO)
4 [https://huggingface.co/datasets/princeton-nlp/gemma2-ultrafeedback-armorm](https://huggingface.co/datasets/princeton-nlp/gemma2-ultrafeedback-armorm)
5 [https://github.com/modelscope/evalscope](https://github.com/modelscope/evalscope)
6 [https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge)


14


Preprint, Under Review


judge is configured with gpt5-mini-aug7-2025, where the reasoning effort is set to “minimal,”
and all other parameters follow the default EvalScope settings.


D F ORMULATIONS OF P REFERENCE O PTIMIZATION O BJECTIVES


Table 5 provides a consolidated overview of various preference optimization objectives that have
been proposed in the literature. Each method is presented in terms of its optimization objective
given preference data _D_ = ( _x, y_ [+] _, y_ _[−]_ ), where _x_ denotes the input prompt, and _y_ [+] and _y_ _[−]_ denote
the preferred (winning) and dispreferred (losing) responses, respectively. The table also specifies
whether the method explicitly depends on a reference policy _π_ ref, whether it leverages the current
policy _π_ _t_ during training, and whether the algorithm falls into the _offline_ or _online_ reinforcement
learning regime.


Table 5: Various preference optimization objectives given preference data _D_ = ( _x, y_ [+] _, y_ _[−]_ ), where
_x_ is an input, and _y_ [+] and _y_ _[−]_ are the winning and losing responses. _f_ is a class of divergence
functions. Γ( _x, y_ ) is the uncertainty estimator. _l_ is a convex decreasing loss function. _P_ [�] ( _y ≻_ _π_ _t_ _| x_ )
is the win rate over the distribution estimated by the average win rate over all the sampled responses
_y_ 1: _K_ _∼_ _π_ _t_ ( _· | x_ ).


Method Objective _π_ ref _π_ _t_ RL Type



DPO (Rafailov et al., 2023) E ( _x,y_ + _,y_ _−_ ) _∼D_ _−_ log _σ_ ~~�~~ _β_ log _ππ_ ref _θ_ ( ( _yy_ [+][+] _||xx_ ) ) _[−]_ _[β]_ [ log] _ππ_ ref _θ_ ( ( _yy_ _[−][−]_ _||xx_ ) )



_f_ -DPO (Wang et al., 2023) E ( _x,y_ + _,y_ _−_ ) _∼D_ _−_ log _σ_ ~~�~~ _βf_ _[′]_ ~~�~~ _ππ_ ref _θ_ ( ( _yy_ [+][+] _|x|x_ ) )



~~�~~ _−_ _βf_ _[′]_ ~~�~~ _ππ_ ref _θ_ ( ( _yy_ _[−][−]_ _|x|x_ ) )



✓ ✗ Offline
~~�~~

) ~~��~~ ✓ ✗ Offline



R-DPO (Park et al., 2024) E ( _x,y_ + _,y_ _−_ ) _∼D_ _−_ log _σ_ ~~�~~ _β_ log _ππ_ ref _θ_ ( ( _yy_ [+][+] _||xx_ ) ) _[−]_ _[β]_ [ log] _ππ_ ref _θ_ ( ( _yy_ _[−][−]_ _||xx_ ) ) [+ (] _[α][ |][y]_ [+] _[| −]_ _[α][ |][y]_ _[−]_ _[|]_ [)] ~~�~~ ✓ ✗ Offline



Distill-DPO (Fisch et al., 2024) E ( _x,y_ + _,y_ _−_ ) _∼D_



2
~~�~~ log _ππ_ ref _θ_ ( ( _yy_ [+][+] _||xx_ ) ) _[−]_ [log] _ππ_ ref _θ_ ( ( _yy_ _[−][−]_ _||xx_ ) ) _[−]_ [(] _[r]_ _[∗]_ [(] _[x, y]_ [+] [)] _[ −]_ _[r]_ _[∗]_ [(] _[x, y]_ _[−]_ [))] ~~�~~ ✓ ✗ Offline



GSHF (Xiong et al., 2023) E ( _x,y_ + _,y_ _−_ ) _∼D_ _−_ log _σ_ ~~�~~ _β_ log _ππ_ ref _θ_ ( ( _yy_ [+][+] _||xx_ ) ) _[−]_ _[β]_ [ log] _ππ_ ref _θ_ ( ( _yy_ _[−][−]_ _||xx_ ) ) ~~�~~ + (Γ ( _x, y_ [+] ) _−_ Γ ( _x, y_ _[−]_ )) ✓ ✗ Offline



KTO (Ethayarajh et al., 2024) E ( _x,y_ + _,y_ _−_ ) _∼D_ _−_ _λ_ _w_ _σ_ ~~�~~ _β_ log _π_ _[π]_ ref _[θ]_ ( [(] _[y]_ _y_ [+][+] _[|]_ _|_ _[ x]_ _x_ [)] )



_,_
~~�~~



_π_ ref ( _y_ [+] _| x_ ) _[−]_ _[z]_ [ref]



+ _λ_ _l_ _σ_ _z_ ref _−_ _β_ log _[π]_ _[θ]_ [(] _[y]_ _[−]_ _[|][ x]_ [)]
~~�~~ ~~�~~ _π_ ref ( _y_ _[−]_ _| x_ )



_π_ ref ( _y_ _[−]_ _| x_ )



_π_ ref ( _y_ [+] _| x_ ) _π_ ref ( _y_ _[−]_ _| x_ ) ✓ ✗ Offline

where _z_ ref = E ( _x,y_ ) _∼D_ [ _β_ KL ( _π_ _θ_ ( _y | x_ ) _∥π_ ref ( _y | x_ ))]



2

✓ ✗ Offline
~~�~~



IPO (Azar et al., 2024) E ( _x,y_ + _,y_ _−_ ) _∼D_



_π_ _θ_ ( _y_ [+] _|x_ ) _π_ _θ_ ( _y_ _[−]_ _|x_ ) 1
~~�~~ log _π_ ref ( _y_ [+] _|x_ ) _[−]_ [log] _π_ ref ( _y_ _[−]_ _|x_ ) _[−]_ 2 _τ_



SLiC-HF (Zhao et al., 2023) E ( _x,y_ + _,y_ _−_ ) _∼D_ max (0 _, δ −_ log _π_ _θ_ ( _y_ [+] _| x_ ) + log _π_ _θ_ ( _y_ _[−]_ _| x_ )) _−_ _λ_ log _π_ _θ_ ( _y_ [+] _| x_ ) ✗ ✗ Offline

RRHF (Yuan et al., 2023) E ( _x,y_ + _,y_ _−_ ) _∼D_ max ~~�~~ 0 _, −_ _|y_ 1 [+] _|_ [log] _[ π]_ _[θ]_ [ (] _[y]_ [+] _[ |][ x]_ [) +] _|y_ 1 _[−]_ _|_ [log] _[ π]_ _[θ]_ [ (] _[y]_ _[−]_ _[|][ x]_ [)] ~~�~~ _−_ _λ_ log _π_ _θ_ ( _y_ [+] _| x_ ) ✗ ✗ Offline

SimPO (Meng et al., 2024) E ( _x,y_ + _,y_ _−_ ) _∼D_ _−_ log _σ_ ~~�~~ _|yβ_ [+] _|_ [log] _[ π]_ _[θ]_ [ (] _[y]_ [+] _[ |][ x]_ [)] _[ −]_ _|yβ_ _[−]_ _|_ [log] _[ π]_ _[θ]_ [ (] _[y]_ _[−]_ _[|][ x]_ [)] _[ −]_ _[γ]_ ~~�~~ ✗ ✗ Offline

CPO (Xu et al., 2024) E ( _x,y_ + _,y_ _−_ ) _∼D_ _−_ log _σ_ ( _β_ log _π_ _θ_ ( _y_ [+] _| x_ ) _−_ _β_ log _π_ _θ_ ( _y_ _[−]_ _| x_ )) _−_ _λ_ log _π_ _θ_ ( _y_ [+] _| x_ ) ✗ ✗ Offline



E ( _x,y_ + _,y_ _−_ ) _∼D_ _−_ log _p_ _θ_ � _y_ [+] _| x_ � _−_ _λ_ log _σ_ ~~�~~ log 1 _−p_ _θ_ _p_ ( _θ_ _y_ ( [+] _y_ [+] _| x|_ ) _x_ ) _[−]_ [log] 1 _−p_ _θ_ _p_ ( _θ_ _y_ ( _[−]_ _y_ _[−]_ _| x|_ ) _x_ )
ORPO (Hong et al., 2024)



_,_
~~�~~



1 ✗ ✗ Offline

_|y|_ [log] _[ π]_ _[θ]_ [(] _[y][ |][ x]_ [)] �



1
where _p_ _θ_ ( _y | x_ ) = exp
� _|y_



~~��~~ ✗ ✓ Online

��



~~��~~



E ( _x,y_ _t_ _[′]_ _[,y]_ _t_ _[′′]_ [)] _[∼D]_ _[t]_ _[ −]_ _[σ]_ [ (] _[r]_ _[t]_ [ (] _[x, y]_ _t_ _[′]_ [)] _[ −]_ _[r]_ _[t]_ [(] _[x, y]_ _t_ _[′′]_ [)) log] ~~�~~ _σ_ ~~�~~ _η_ log _π_ _[π]_ _t_ ( [(] _[y]_ _y_ _t_ _[′]_ _t_ _[′]_ _[|][|][ x][ x]_ [)][)] _[ −]_ _[η]_ [ log] _π_ _[π]_ _t_ ( [(] _[y]_ _y_ _t_ _[′′]_ _t_ _[′′]_ _[|][|][ x][ x]_ [)][)]
DNO (Rosset et al., 2024)

_−σ_ ( _r_ _t_ ( _x, y_ _t_ _[′′]_ [)] _[ −]_ _[r]_ _[t]_ [(] _[x, y]_ _t_ _[′]_ [)) log] � _σ_ � _η_ log _π_ _[π]_ _t_ [(] ( _[y]_ _y_ _t_ _[′′]_ _t_ _[′′]_ _[|][|][ x][ x]_ [)][)] _[ −]_ _[η]_ [ log] _π_ _[π]_ _t_ [(] ( _[y]_ _y_ _t_ _[′]_ _t_ _[′]_ _[|][|][ x][ x]_ [)][)]



E ( _x,y_ _t_ _[′]_ _[,y]_ _t_ _[′′]_ [)] _[∼D]_ _[t]_ _[ −]_ _[σ]_ [ (] _[r]_ _[t]_ [ (] _[x, y]_ _t_ _[′]_ [)] _[ −]_ _[r]_ _[t]_ [(] _[x, y]_ _t_ _[′′]_ [)) log] ~~�~~ _σ_ ~~�~~ _η_ log _π_ _[π]_ _t_ ( [(] _[y]_ _y_ _t_ _[′]_ _t_ _[′]_ _[|][|][ x][ x]_ [)][)] _[ −]_ _[η]_ [ log] _π_ _[π]_ _t_ ( [(] _[y]_ _y_ _t_ _[′′]_ _t_ _[′′]_ _[|][|][ x][ x]_ [)][)]
DNO (Rosset et al., 2024)



DNO-Prct (Rosset et al., 2024) E( _x,y_ _t_ + _[,y]_ _t_ _[−]_ [)] _[∼D]_ _[t]_ _[ −]_ [log] ~~�~~ _σ_ ~~�~~ _η_ � log _ππ_ _t_ (( _yy_ _t_ [+] _t_ [+] _[|][|][x][x]_ [)][)] _[ −]_ _[η]_ [�][ log] _ππ_ _t_ (( _yy_ _t_ _[−]_ _t_ _[−]_ _[|][|][x][x]_ [)][)] ~~��~~ ✗ ✓ Online



SPIN (Chen et al., 2024) E( _x,y,y_ _t−_ [)] _[∼D]_ _[t]_ _[ −]_ _[ℓ]_ ~~�~~ _β_ log _[π]_ _π_ _[θ]_ _t_ ( [(] _y_ _[y]_ _|_ _[|]_ _x_ _[x]_ ) [)]



_π_ _[θ]_ _t_ ( [(] _y_ _[y]_ _[′][′]_ _|_ _[|]_ _x_ _[x]_ ) [)] ~~�~~ ✗ ✓ Online




_[π]_ _π_ _[θ]_ _t_ ( [(] _y_ _[y]_ _|_ _[|]_ _x_ _[x]_ ) [)] _[−]_ _[β]_ [ log] _[ π]_ _π_ _[θ]_ _t_ ( [(] _y_ _[y]_ _[′][′]_ _|_ _[|]_ _x_ _[x]_ ) [)]



SPPO (Wu et al., 2024) E( _x,y,_ � _P_ ( _y≻π_ _t_ _|x_ ) ) _∼D_ _t_ _[−]_ ~~�~~ log _[π]_ _π_ _[θ]_ _t_ ( [(] _y_ _[y]_ _|_ _[|]_ _x_ _[x]_ ) [)]




_[π]_ _π_ _[θ]_ _t_ ( [(] _y_ _[y]_ _|_ _[|]_ _x_ _[x]_ ) [)] _[−]_ _[η]_ ~~�~~ _P_ � ( _y ≻_ _π_ _t_ _| x_ ) _−_ [1] 2



2

[1] 2 ~~��~~ ✗ ✓ Online



INPO (Zhang et al., 2025b) E( _x,y_ _t_ + _[,y]_ _t_ _[−]_ [)] _[∼][D]_ _[t]_ _[ −]_ ~~�~~ _τη_



~~�~~ log _ππ_ ref _θ_ (( _yy_ _t_ [+] _t_ [+] [)][)] _[ −]_ [log] _ππ_ ref _θ_ (( _yy_ _t_ _[−]_ _t_ _[−]_ [)][)] ~~�~~ + _[η][−]_ _η_ _[τ]_



_π_ _θ_ ( _y_ _t_ [+] [)] _π_ _θ_ ( _y_ _t_ _[−]_ [)]
~~�~~ log _π_ _t_ ( _y_ _t_ [+] [)] _[−]_ [log] _π_ _t_ ( _y_ _t_ _[−]_ [)]



_−_ 21 _τ_
~~�~~



2

✓ ✓ Online
~~�~~




_[π]_ _[θ]_ _y_ _t_ _−_ _[η]_

_π_ _t_ _[′]_ ~~�~~ _y_ _t_ _[−]_ ~~�~~ 2



2



~~�~~ 2



E( _x,y_ _t_ + _[,y]_ _t_ _[−]_ [)] _[∼][D]_ _[t]_



~~�~~



log _[π]_ _[θ]_ ~~�~~ _y_ _t_ [+] ~~�~~




_[π]_ _[θ]_ ~~�~~ _y_ _t_ [+] ~~�~~ _−_ log _[π]_ _[θ]_ ~~�~~ _y_ _t_ _[−]_ ~~�~~

_π_ _t_ _[′]_ ~~�~~ _y_ _t_ [+] ~~�~~ _π_ _t_ _[′]_ ~~�~~ _y_ _t_ _[−]_ ~~�~~



_,_



ONPO (Zhang et al., 2025a)




_[π]_ _y_ _t_ _−_ _[η]_

_π_ _t_ ~~�~~ _y_ _t_ _[−]_ ~~�~~ 2



2



where _π_ _t_ _[′]_ [= argmin] _π_ E( _x,y_ _t_ + _[,y]_ _t_ _[−]_ [)] _[∼][D]_ _[t]_



�



log _[π]_ � _y_ _t_ [+] �




_[π]_ � _y_ _t_ [+] � _−_ log _[π]_ � _y_ _t_ _[−]_ �

_π_ _t_ ~~�~~ _y_ _t_ [+] ~~�~~ _π_ _t_ ~~�~~ _y_ _t_ _[−]_ ~~�~~



� 2 ✗ ✓ Online



~~�~~ + [1] 2 [log] ~~�~~ 1 + _ππ_ ref _θ_ ( ( _yy_ [+][+] _||xx_ ) )



+ [1] 2
~~�~~



~~�~~ + [1] 2 [log] ~~�~~ 1 + _ππ_ ref _θ_ ( ( _yy_ _[−][−]_ _||xx_ ) )



+ [1] 2
~~�~~



✓ ✓ Offline
~~��~~



MIO (Lv et al., 2025) E ( _x,y_ + _,y_ _−_ ) _∼D_



~~�~~ log ~~�~~ 1 + _ππ_ ref _θ_ ( ( _yy_ [+][+] _||xx_ ) )



15


Preprint, Under Review


E M ATHEMATICAL A NALYSIS


E.1 P ROOF OF L EMMA 1


_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_



_Proof._ First, by construction _L_ _t_ ( _π_ [(] _[t]_ [+1)] ) = 0, hence _π_ [(] _[t]_ [+1)] is a minimizer. Suppose, for contradiction, there exists ˜ _π ∈_ Π with ˜ _π ̸_ = _π_ [(] _[t]_ [+1)] and _L_ _t_ (˜ _π_ ) = 0 . Then for every pair _y, y_ _[′]_ _∈_ Supp( _π_ ref ), we
must have
_η_
_h_ _t_ (˜ _π, y, y_ _[′]_ ) = _n −_ 1 ��P( _y ≻_ _π_ _j_ [(] _[t]_ [)] [)] _[ −]_ [P][(] _[y]_ _[′]_ _[ ≻]_ _[π]_ _j_ [(] _[t]_ [)] [)] � _._

_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_



�P( _y ≻_ _π_ _j_ [(] _[t]_ [)] [)] _[ −]_ [P][(] _[y]_ _[′]_ _[ ≻]_ _[π]_ _j_ [(] _[t]_ [)] [)] � _._

_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_



�

_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_



_j_ = _̸_ _i_

Unrolling _h_ _t_ and rearranging yields the pairwise ratio identity


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


˜ _η_
_π_ ( _y_ _| x_ ) exp� _n−_ 1 � _̸_ _̸_
_π_ ˜( _y_ _[′]_ _| x_ ) [=] _η_

_̸_ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


_j_ = _̸_ _i_ [P][(] _[y][ ≻]_ _[π]_ _j_ [(] _[t]_ [)] _| x_ )�� _̸_

_j_ = _̸_ _i_ [P][(] _[y]_ _[′]_ _[ ≻]_ _[π]_ _j_ [(] _[t]_ [)] _| x_ ) ~~��~~ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


1 _._

_n−_ 1

_̸_ _j_ = _̸_ _i_ _[π]_ _j_ [(] _[t]_ [)] [(] _[y]_ _[′]_ _[ |][ x]_ [)]


_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


1

_n−_ 1

_̸_ _j_ = _̸_ _i_ _[π]_ _j_ [(] _[t]_ [)] [(] _[y][ |][ x]_ [)]


_̸_ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_η_
exp ~~�~~ _n−_ 1 ~~�~~ _j̸_ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


Because Supp(˜ _π_ ) = Supp( _π_ ref ) and [�] _y_ _[π]_ [˜][(] _[y][ |][ x]_ [) = 1] [, these pairwise ratios determine] [ ˜] _[π]_ [(] _[· |][ x]_ [)]

uniquely—and that unique solution is exactly the normalized distribution implied by Eq. 11 and 12,
i.e., _π_ [(] _[t]_ [+1)] . Hence ˜ _π_ = _π_ [(] _[t]_ [+1)], a contradiction. Therefore the minimizer is unique.


E.2 P ROOF OF P ROPOSITION 1


_Proof._ Introduce an indicator _I ∼_ Ber(P( _y ≻_ _y_ _[′]_ _| x_ )) for a pair ( _y, y_ _[′]_ ) _∼_ _π_ [(] _[t]_ [)] _× π_ [(] _[t]_ [)] . Consider


� 2
_L_ _t_ ( _π_ ) = E _y,y_ _′_ _∼π_ ( _t_ ) _, I_ � _h_ _t_ ( _π, y, y_ _[′]_ ) _−_ _η_ _[I]_ � _._

Expanding and comparing _L_ [�] _t_ ( _π_ ) with _L_ _t_ ( _π_ ) shows the only difference lies in the cross-term
E[ _h_ _t_ ( _π, y, y_ _[′]_ )(P( _y ≻_ _π_ [(] _[t]_ [)] ) _−_ P( _y_ _[′]_ _≻_ _π_ [(] _[t]_ [)] )) ] versus E[ _h_ _t_ ( _π, y, y_ _[′]_ ) _I_ ] . One verifies these are equal
by writing _h_ _t_ as a linear form in log _π_, log _π_ _j_ [(] _[t]_ [)] and using that _y_ and _y_ _[′]_ are i.i.d. draws from _π_ [(] _[t]_ [)] :

E _y,y_ _[′]_ [�] _h_ _t_ ( _π, y, y_ _[′]_ )�P( _y ≻_ _π_ [(] _[t]_ [)] ) _−_ P( _y_ _[′]_ _≻_ _π_ [(] _[t]_ [)] )�� = E _y,y_ _[′]_ _,I_ � _h_ _t_ ( _π, y, y_ _[′]_ ) _I_ � _._


(See INPO Appendix A.5 for the algebraic steps; the same symmetry argument applies verbatim.)
Now expand _L_ _[′]_ _t_ [(] _[π]_ [)][ by conditioning on][ (] _[y, y]_ _[′]_ [)][ and the preference sampler] _[ λ]_ [P] [(] _[y, y]_ _[′]_ [)][:]


2 2
_L_ _[′]_ _t_ [(] _[π]_ [) =][ E] _[y,y]_ _[′]_ �P( _y ≻_ _y_ _[′]_ )� _h_ _t_ ( _π, y, y_ _[′]_ ) _−_ 21 _η_ � + �1 _−_ P( _y ≻_ _y_ _[′]_ )� [�] _h_ _t_ ( _π, y_ _[′]_ _, y_ ) _−_ 21 _η_ � � _._

Using _h_ _t_ ( _π, y_ _[′]_ _, y_ ) = _−h_ _t_ ( _π, y, y_ _[′]_ ) and completing the square shows _L_ _[′]_ _t_ [(] _[π]_ [) =][ �] _[L]_ _[t]_ [(] _[π]_ [) + const] [, where]
the constant depends only on the distribution of ( _y, y_ _[′]_ ) and P( _·_ ), not on _π_ . Combining with the
equality of cross-terms above gives _L_ _[′]_ _t_ [(] _[π]_ [) =] _[ L]_ _[t]_ [(] _[π]_ [) + const][, as claimed.]


E.3 T HEORETICAL A NALYSIS OF E Q . 11


Here, we provide a theoretical analysis of the iterative update in Eq. 11:


_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


� _P_ � _y ≻_ _π_ _j_ [(] _[t]_ [)] ��� _x_ � [�]

_̸_ _j_ = _̸_ _i_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


1

_n−_ 1

exp

_̸_ � _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_π_ _i_ [(] _[t]_ [+1)] ( _y | x_ ) _∝_


_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


�� _j_ = _̸_ _i_ _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_π_ _j_ [(] _[t]_ [)] [(] _[y][ |][ x]_ [)]

_j_ = _̸_ _i_ _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_η_

_n −_ 1

_̸_ � _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


�

_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_._ (19)


_̸_ _̸_


_̸_


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


**Derivation from Mirror Descent.** Eq. 19 can be viewed as an instance of online mirror descent
(OMD) with the KL divergence as the Bregman potential. At each step, player _i_ seeks to maximize
the expected win probability against the population � _π_ _j_ [(] _[t]_ [)] � _j_ = _̸_ _i_ [subject to a KL regularization toward]


_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_

the opponent mixture:


_π_ _i_ [(] _[t]_ [+1)] = arg max
_π∈_ Π _̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_

_̸_ ������ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


��

_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


1

_n−_ 1
_π_ [(] _[t]_ [)] 
_j_ �

_̸_ _j_ = _̸_ _i_ 



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


1

_n −_ 1

_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


�

_j_ = _̸_ _i_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


� _π, P_ ( _· ≻_ _π_ _j_ [(] _[t]_ [)] [)] � _−_ [1]

_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


_η_ _[D]_ [KL]

_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


 _π_

_̸_  _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_





_̸_ _̸_



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


_._

_̸_ _̸_ 



_̸_


_̸_ _̸_


_̸_ _̸_


_̸_ _̸_


_̸_


_̸_ _̸_


Taking first-order conditions yields exactly the multiplicative-weights update in Eq. 19. Thus, the
MNPO update inherits the regret guarantees of OMD: the average regret after _T_ rounds scales as
_O_ (1 _/√T_ ), ensuring convergence to equilibrium in the no-regret learning sense.


16


Preprint, Under Review


**Pairwise Ratio Dynamics.** To avoid computing the intractable partition function, we analyze the
pairwise log-ratio


_̸_


_̸_



_h_ _t_ ( _π, y, y_ _[′]_ ) = log _[π]_ [(] _[y]_ _[|][ x]_ [)] 1

_π_ ( _y_ _[′]_ _| x_ ) _[−]_ _n −_ 1

_̸_


_̸_



� log _π_ _j_ [(] _[t]_ [)] [(] _[y][ |][ x]_ [)]

_j_ = _̸_ _i_ _π_ _j_ [(] _[t]_ [)] [(] _[y]_ _[′]_ _[ |][ x]_


_̸_



�

_̸_


_̸_



_._

_̸_ _π_ _j_ [(] _[t]_ [)] [(] _[y]_ _[′]_ _[ |][ x]_ [)]


_̸_



_̸_


Eq. 12 in the main text shows that at the fixed point _π_ [(] _[t]_ [+1)], these ratios satisfy


_̸_



_̸_


_η_
_h_ _t_ � _π_ [(] _[t]_ [+1)] _, y, y_ _[′]_ [�] = _n −_ 1

_̸_



_̸_


�� _P_ ( _y ≻_ _π_ _j_ [(] _[t]_ [)] _| x_ ) _−_ _P_ ( _y_ _[′]_ _≻_ _π_ _j_ [(] _[t]_ [)] _| x_ )� _._

_̸_



_̸_


� _P_ ( _y ≻_ _π_ _j_ [(] _[t]_ [)] _| x_ ) _−_ _P_ ( _y_ _[′]_ _≻_ _π_ _j_ [(] _[t]_ [)] _| x_ )� _._

_̸_



_̸_


_j_ = _̸_ _i_


Hence the log-ratio dynamics correspond to a consistent linearization of the preference margins
across all opponents, ensuring that the update increases probability mass on responses with strictly
higher average advantage.


**Equilibrium Properties.** By standard arguments in no-regret game dynamics (Freund & Schapire,
1999), if all players update according to Eq. 19, the joint empirical distribution converges to an
_n_ -player Nash equilibrium. Moreover, because the update is multiplicative in form, probabilities
remain strictly positive on the support of _π_ ref, preventing premature collapse.


**Interpretation.** Eq. 19 admits two complementary interpretations:


    - _Population averaging:_ the geometric mean term aggregates beliefs of all opponents, ensuring
stability against heterogeneous policies.


    - _Advantage weighting:_ the exponential term amplifies responses that consistently outperform
others, with learning rate _η_ controlling the exploration–exploitation trade-off.


Together, these properties explain why MNPO achieves robust convergence in multiplayer preference
optimization while generalizing the two-player INPO update.


F L IMITATIONS AND F UTURE W ORK


Like other algorithms in the RLHF paradigm, the performance of MNPO is fundamentally linked to
the quality of its preference data. Two primary limitations warrant consideration for future work.


First, the fidelity of the preference oracle serves as a performance ceiling. As the policy model
improves and its generations become consistently high-quality, the task of distinguishing between
chosen and rejected responses becomes increasingly difficult for the preference oracle in practice.
This diminishing discriminative capability can become a bottleneck for further improvement.


Second, the paradigm of simply increasing the probability of chosen responses and decreasing that of
rejected ones may face diminishing returns as the preference gap narrows. When rejected responses
are themselves of high quality, the binary preference signal becomes less informative, potentially
slowing down or stalling the convergence of the policy model. Future research could explore more
nuanced feedback mechanisms to address learning in this high-performance regime.


F.1 E XTERNAL O PPONENT P LAYERS


**Formulation.** An alternative to using past-time policies as opponents is leveraging external LLMs
to introduce a broader range of competitive dynamics. Given a set of _n −_ 1 LLM policies _{π_ _j_ _}_ _[n]_ _j_ =1 _[−]_ [1] [,]
these opponent models can come from different sources: they may belong to distinct model families,
have varying parameter scales within the same architecture, be trained on different data distributions,
or specialize in different domains. The external opponent MNPO (EO-MNPO) loss in this case is
defined as:



_̸_


_̸_


_λ_ _j_

_j_



_̸_


_̸_


 _._ (20)





_̸_


_̸_


_π_ _j_ ( _y_ _[′]_ _| x_ )



_̸_


_̸_


_L_ _[t,]_ EO-MNPO [D] [(] _[π][|][β,][ {][λ]_ _[j]_ _[}][, η]_ [) =][ D]



_̸_


_̸_






_̸_


_̸_


 [�] _j_



_̸_


_̸_


_[|][ x]_ [)]
log _[π]_ [(] _[y]_
� _π_ _j_ ( _y | x_ )



_̸_


_̸_


_[|][ x]_ [)] _[|][ x]_ [)]

_[π]_ [(] _[y]_ _[π]_ [(] _[y]_ _[′]_

_π_ _j_ ( _y | x_ ) _[−]_ [log] _π_ _j_ ( _y_ _[′]_ _| x_ )



_̸_


_̸_


_ηδ_ _⋆_
�����



_̸_


_̸_


17


Preprint, Under Review


Here, the constraint [�] _j_ _[λ]_ _[j]_ [ = 1] [ ensures that the contributions of different opponent policies are appro-]

priately weighted. This formulation introduces a key advantage: it enables preference optimization
across diverse knowledge sources rather than being restricted to a single training trajectory.


To better interpret this formulation, we can draw parallels to knowledge distillation. Specifically,
consider a scenario where we have a collection of teacher models � _π_ _i_ [teacher] � and seek to refine an
updated policy _π_ that remains close to both these teacher models and the original reference model
_π_ ref . The objective function can be expressed as:



_τ_ _i_ KL _π∥π_ _i_ [teacher]
� � [�]
_i_



_J_ ( _π_ ) = E _x∼d_ 0



�



E _y∼π_ [ _R_ ( _x, y_ )] _−_ _τ_ 0 KL ( _π∥π_ ref ) _−_ �



_._ (21)



This formulation illustrates that MNPO with external opponent players can be viewed as an extension
of knowledge distillation, where the learned policy integrates information from multiple expert
models while balancing divergence from the reference model. Using the same derivation technique as
DPO, we can recover Eq. 20, linking preference optimization to a generalized knowledge alignment
framework.


**Proposition 2.** _The optimal solution to the maximum reward objective in Eq. 21 is equivalent to the_
_learned reward model in Eq. 20._



It is straightforward to show that the solution to the maximum reward objective in Eq. 21 takes
the form: _π_ _[⋆]_ ( _y | x_ ) = _Z_ (1 _x_ ) [exp(] _[R]_ [(] _[x, y]_ [)] _[/τ]_ [)] _[π]_ [ref] [(] _[y][ |][ x]_ [)] _[τ]_ [0] _[/τ]_ [ �] _i_ _[π]_ _i_ [teacher] ( _y | x_ ) _[τ]_ _[i]_ _[/τ]_, where _Z_ ( _x_ ) is the



the form: _π_ _[⋆]_ ( _y | x_ ) = _Z_ (1 _x_ ) [exp(] _[R]_ [(] _[x, y]_ [)] _[/τ]_ [)] _[π]_ [ref] [(] _[y][ |][ x]_ [)] _[τ]_ [0] _[/τ]_ [ �] _i_ _[π]_ _i_ [teacher] ( _y | x_ ) _[τ]_ _[i]_ _[/τ]_, where _Z_ ( _x_ ) is the

partition function and _τ_ = _τ_ 0 + [�] _i_ _[τ]_ _[i]_ [.]



_i_ _[τ]_ _[i]_ [.]



**Analysis.** EO-MNPO gains several benefits. Firstly, Unlike the self-comparison TD-MNPO, using
a diverse pool of external LLMs exposes the policy to a broader range of feedback, leading to more
robust optimization. Secondly, leveraging domain-specific expert models allows MNPO to fine-tune
policies for specialized applications, improving generalization. Thirdly, this framework aligns with
broader trends in multi-agent RL, where agents iteratively refine their strategies against multiple
opponents, driving more sophisticated decision-making. By considering a dynamic set of external
LLMs as opponent players, EO-MNPO extends beyond self-referential optimization, making it a
more flexible and generalizable approach for preference optimization in LLMs.


G T HE U SE OF L ARGE L ANGUAGE M ODELS (LLM S )


We used large language models, including ChatGPT, Gemini, and Claude as writing assistants
in the preparation of this manuscript. Their role was strictly confined to language enhancement
tasks, such as polishing grammar, improving readability, and generating alternative phrasings. All
intellectual contributions, such as research ideas, experimental designs, analyses, and conclusions,
were developed solely by the authors, who take full responsibility for the content of this paper.


18


