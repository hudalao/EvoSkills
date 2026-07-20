## **Not All Models Suit Expert Offloading: On Local** **Routing Consistency of Mixture-of-Expert Models**



**Jingcong Liang**
Fudan University
jcliang22@m.fudan.edu.cn



**Siyuan Wang**
University of Southern California
sw_641@usc.edu



**Miren Tian & Yitong Li & Duyu Tang**
Huawei Technologies Ltd.
tianmiren1,liyitong3,tangduyu@huawei.com



**Zhongyu Wei**
Fudan University
zywei@fudan.edu.cn



**Abstract**


Mixture-of-Experts (MoE) enables efficient scaling of large language models
(LLMs) with sparsely activated experts during inference. To effectively deploy
large MoE models on memory-constrained devices, many systems introduce _expert_
_offloading_ that caches a subset of experts in fast memory, leaving others on slow
memory to run on CPU or load on demand. While some research has exploited the
locality of expert activations, where consecutive tokens activate similar experts,
the degree of this **local routing consistency** varies across models and remains
understudied. In this paper, we propose two metrics to measure local routing
consistency of MoE models: (1) **Segment Routing Best Performance (SRP)**,
which evaluates how well a fixed group of experts can cover the needs of a segment
of tokens, and (2) **Segment Cache Best Hit Rate (SCH)**, which measures the
optimal segment-level cache hit rate under a given cache size limit. We analyzed 20
MoE LLMs with diverse sizes and architectures and found that models that apply
MoE on every layer and do not use shared experts exhibit the highest local routing
consistency. We further showed that domain-specialized experts contribute more to
routing consistency than vocabulary-specialized ones, and that most models can
balance between cache effectiveness and efficiency with cache sizes approximately
2x the active experts. These findings pave the way for memory-efficient MoE
design and deployment without compromising inference speed. We publish the
[code for replicating experiments at https://github.com/ljcleo/moe-lrc.](https://github.com/ljcleo/moe-lrc)


**1** **Introduction**


Mixture-of-Experts (MoE) is a widely adopted model architecture in many large language models
(LLMs) that enables efficient model size scaling through sparse activation(Fedus et al., 2022; Jiang
et al., 2024; Dai et al., 2024; Abdin et al., 2024). MoE models replace dense feed-forward networks
(FFNs) with multiple expert modules, with only a subset activated during inference. However, the
vanilla implementation requires all experts to be loaded into memory, restricting its application on
memory-constrained devices such as mobile phones. To address this limitation, the _expert offloading_
technique has been proposed to allow partial loading of expert modules during inference (Eliseev &
Mazur, 2023; Hwang et al., 2024; Yi et al., 2025). Specifically, expert offloading caches a subset of
experts in fast memory (e.g., GPU memory) based on predefined heuristics, while storing remaining
experts in slower but larger-capacity storage (e.g., CPU memory or disk). During inference, especially
in the decoding stage, if a token activates an expert not cached in fast memory, the system either
computes the expert forward results with CPU and slow memory (CPU offload) (Kamahori et al.,


Preprint. Under review.


2024; Tang et al., 2024), or unloads a cached expert according to specific rules such as Least Recently
Used (LRU), and replaces it with the demanded expert (on-demand loading) (Kong et al., 2024;
Zhong et al., 2025).


However, frequent CPU offloads or on-demand loading within a short period can significantly degrade
the efficiency of the expert offloading system and slow down inference, particularly when processing
lengthy contexts with inevitable topic shifts. Prior research has focused on optimizing the design
of the expert offloading system, aiming to strategically select which experts to cache in a given
context to maximize cache hit rates. Among them, some observed and exploited the locality of expert
activations, where similar routing choices appear within a consecutive segment of tokens, thereby
minimizing the need for CPU offloads and on-demand loading (Eliseev & Mazur, 2023; Xue et al.,
2024b; Zhang et al., 2025). This is especially beneficial during the decoding phase, where tokens are
generated one after another.


Nevertheless, not all MoE models exhibit such continuous routing patterns uniformly, and the degree
or frequency of this phenomenon varies across models. Understanding this variance may help design
MoE architectures that are friendly to expert offloading systems and vice versa. In this work, we
investigate the degree of this inherent consecutive routing property, which we term **local routing**
**consistency**, of different MoE-based LLMs to explore their potential effectiveness in segment-based
expert routing or caching. Figure 1 illustrates how different levels of local routing consistency reflect
different routing patterns. Specifically, we propose two metrics that quantitatively reflect the local
routing consistency of a specific model. (1) **Segment Routing Best Performance (SRP)** measures
how effectively a segment router that selects a fixed group of experts for all tokens in a segment can
approximate the original router’s decisions. SRP not only reflects local routing consistency _without_
_parameters other than segment length_, but also enables analyzing activation patterns of _individual_
_experts_ . (2) **Segment Cache Best Hit Rate (SCH)** represents the highest cache hit rate by any expert
offloading method that caches experts for whole segments, under a cache size limit related to the
number of active experts. SCH measures local routing consistency on model- and router-levels, yet is
more related to the performance of _real expert offloading systems_ as it accounts for the cache limit.


Figure 1: Routing results by GRIN-MoE (Liu et al., 2024b) layer 21 and Jamba-Mini-1.6 (Lenz
et al., 2025) layer 25 on the same input (Java code). Despite having similar model sizes and the same
number of experts, GRIN-MoE exhibits more consistent routing patterns than Jamba-Mini-1.6, with
multiple experts continuously activated, so expert caching with GRIN-MoE will be more feasible and
effective.


We conduct experiments on 20 MoE-based LLMs, covering parameter scales ranging from 3 billion
to 54 billion and encompassing diverse architectures. While most models exhibit similar local
routing consistency within a few tokens, the variance enlarges when the segment length increases.
Models that **apply MoE on every layer** and **do not use shared experts** exhibit the **highest local**
**routing consistency**, some of which even achieve load balance. Additionally, we investigate local
routing consistency across different context domains and assess its relationship with experts’ domain
and vocabulary preferences. The findings reveal that **domain-specialized experts**, if they exist,
**contribute more** to local routing consistency, whereas vocabulary specialization has less impact.
Finally, we verify the strong correlation between SRP and SCH, confirming that both metrics
effectively represent local routing consistency. We conclude that most MoE models can achieve


2


**optimal balance** between segment caching effectiveness and deployment efficiency with a **cache**
**size approximately 2x the number of active experts** . [*]


Overall, our contributions are threefold:


1. We propose _local routing consistency_, a property of MoE models that reflects the potential
efficiency of expert offloading for the model. We design two metrics to quantify local routing
consistency: segment routing best performance (SRP), which provides parameter-free fine-grained
analysis, and segment cache best hit rate (SCH), aligned with practical expert offloading.
2. We conduct empirical analysis across 20 MoE-based LLMs, demonstrating that models that apply
MoE on every layer and without shared experts show the highest local routing consistency. We
also reveal that domain-specialized experts contribute more to local routing consistency than
vocabulary-specialized experts.
3. We analyze SCH under different cache sizes relative to the number of active experts. Alongside
the optimal cache size derived from SRP results, we conclude that cache sizes 2x the size of active
parameters achieve the best segment caching results on most models.


**2** **Definitions**


**2.1** **Preliminary: mixture of experts**


Transformer-based language models have most parameters on feed-forward network (FFN) layers. As
the model size scales up, LLMs often replace them with sparse MoE layers to reduce computational
cost during inference. A typical MoE layer with _E_ experts can be parameterized by _E_ smaller FFNs
_F_ 1 (; _θ_ 1 ) _, . . ., F_ _E_ (; _θ_ _E_ ), where each _F_ _i_ : R _[d]_ _→_ R _[d]_ defines a single expert. There is also a router
_R_ : R _[d]_ _→_ R _[E]_ in the MoE layer to choose experts and give weights. For each token _x_ with hidden
representation _h_ _x_ _∈_ R _[d]_, its output is given by




[ _s_ 1 _, . . ., s_ _E_ ] = Softmax( _R_ ( _h_ _x_ )); [ _w_ 1 _, . . ., w_ _E_ ] = Top _k_ ( _s_ 1 _, . . ., s_ _E_ ); _o_ _x_ =



_E_
� _w_ _i_ _F_ _i_ ( _h_ _x_ ; _θ_ _i_ ) (1)


_i_ =1



where Top _k_ preserves the _k_ largest scores and sets others to 0 . Experts with a null score can be
effectively deactivated without calculating, thus saving computational resources. Other components
in the transformer architecture may also be replaced by their MoE variant, such as Mixture-ofAttention (Zhang et al., 2022) for self-attention and MixLoRA (Li et al., 2024a) for LoRA adapters.
Nevertheless, we focus on MoE layers that replace FFNs, as this is the most prominent and effective
design (in terms of the number of parameters). More discussions about MoE LLMs can be found in
Appendix B, where we also briefly review expert offloading for MoE models.


The above routing procedure is done token by token, which does not guarantee consecutive routing.
Since the consistency of consecutive routing decisions can benefit expert offloading systems, it is
necessary to investigate the degree of consecutive routing of different MoE-based LLMs. In the
following sections, we propose two metrics to measure this **local routing consistency** and compare
them across MoE models with different structure parameters.


**2.2** **Segment routing best performance (SRP)**


An intuitive way to measure local routing consistency is to compare the distribution of routing choices
between tokens in a continuous segment. However, typical metrics for distribution comparison, such
as the Kullback-Leibler divergence, work with two distributions and thus are unsuitable for our
demand. Instead, we measure how well a simplified, segment-based router can mimic the behavior of
the original token-based router. Here we define the **segment routing best performance (SRP)** of a
single expert _e_ and a group of experts _E_ (e.g., experts from the same MoE layer or model).


**Single expert** For any input sequence _T_ = [ _t_ 1 _, . . ., t_ _|T |_ ], we denote the activation sequence of
expert _e_ on _T_ as _A_ ( _e, T_ ) = [ _a_ 1 _, . . ., a_ _|T |_ ], where _a_ _i_ _∈{_ 0 _,_ 1 _}_ indicates whether _e_ is activated on _t_ _i_
( _a_ _i_ = 1 ) or not ( _a_ _i_ = 0 ). A segment-based router _R_ _e_ _[m]_ [with segment length] _[ m >]_ [ 0] [ for expert] _[ e]_ [ will]


   - We propose this insight from the aspect of model design, especially when building models for devices with
known memory constraints (e.g., mobile phones).


3


try to mimic [ _a_ _p_ _, . . ., a_ _p_ + _m−_ 1 ] for any _T_ and _p_, similar to expert-choice routing (Zhou et al., 2022).
Let _R_ _e_ _[m]_ [(] _[T, p]_ [) = [] _[b]_ [1] _[, . . ., b]_ _[m]_ []][ be its prediction, with the segment-prediction constraint:]


_b_ _i_ = 0 _, ∀i_ = 1 _, . . ., m_ or _b_ _i_ = 1 _, ∀i_ = 1 _, . . ., m_ (2)


In other words, _R_ _e_ _[m]_ [decides that] _[ e]_ [ is either always active or always inactive on] [ [] _[t]_ _[p]_ _[, . . ., t]_ _[p]_ [+] _[m][−]_ [1] []] [. For]
simplicity, we write _R_ _e_ _[m]_ [(] _[T, p]_ [) = 0] [ and] _[ R]_ _e_ _[m]_ [(] _[T, p]_ [) = 1] [ for the two cases respectively. By treating]
each segment routing attempt as a binary classification task with _m_ samples, and considering all
possible segments of all possible inputs, we can calculate the _F_ 1 score of _R_ _e_ _[m]_ [:]



_|T |−m_ +1

2 [�] _T_ � _p_ =1 _R_ _e_ _[m]_ [(] _[T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)]

_|T |−m_ +1

~~�~~ _T_ ~~�~~ =1 [ _m · R_ _e_ _[m]_ [(] _[T, p]_ [) +] _[ f]_ [(] _[e, T, p, m]_



2 [�]
_F_ 1 ( _R_ _e_ _[m]_ [) =]



_|T |−m_ +1 (3)
_T_ ~~�~~ _p_ =1 [ _m · R_ _e_ _[m]_ [(] _[T, p]_ [) +] _[ f]_ [(] _[e, T, p, m]_ [)]]



where _f_ ( _e, T, p, m_ ) = [�] _[p]_ _i_ = [+] _p_ _[m][−]_ [1] _A_ ( _e, T_ )[ _i_ ] is the active frequency of _e_ in the segment of _T_ with
length _m_ starting at position _p_ . We demonstrate the detailed process to obtain this equation in
Appendix C.1. We choose _F_ 1 score because we do not set up an upper bound on how many experts
_R_ _e_ _[m]_ [can be selected, so hit rate (recall) can go up to] [ 1] [ by selecting all experts. Moreover, missing]
major experts is worse than activating minor ones, as changing low-rank experts usually affects model
performance less (Kong et al., 2024; Skliar et al., 2024); therefore, we prefer _F_ 1 score to accuracy to
emphasize this difference.


Based on Equation 3, we define the segment routing best performance of _e_ under segment length _m_
as the maximum _F_ 1 score any _R_ _e_ _[m]_ [can achieve:] [ SRP(] _[e, m]_ [)][ ≜] [max] _[R]_ _e_ _[m]_ _[F]_ [1] [(] _[R]_ _e_ _[m]_ [)] [. Furthermore, in]
Appendix C.2 we prove that _F_ 1 ( _R_ _e_ _[m]_ [)] [ is maximized if and only if] _[ R]_ _e_ _[m]_ [gives active predictions for all]
segments that activates _e_ at least _α_ _e_ _[m]_ [times, where] _[ α]_ _e_ _[m]_ _[∈]_ [[0] _[, m]_ []][ is only related to] _[ e]_ [ and] _[ m]_ [:]



2 [�]
SRP( _e, m_ ) =



_T_ �



2 [�] _T_ � _f_ ( _e,T,p,m_ ) _≥α_ _[m]_ _e_ _[f]_ [(] _[e, T, p, m]_ [)]

_|T |−m_ +1

~~�~~ _T_ ~~�~~ =1 [ _m · I_ [ _f_ ( _e, T, p, m_ ) _≥_ _α_ _e_ _[m]_ [] +] _[ f]_



_|T |−m_ +1 _e_ (4)
_T_ ~~�~~ _p_ =1 [ _m · I_ [ _f_ ( _e, T, p, m_ ) _≥_ _α_ _e_ _[m]_ [] +] _[ f]_ [(] _[e, T, p, m]_ [)]]



Therefore, SRP( _e, m_ ) is an intrinsic property of the expert that reflects its local routing consistency,
unrelated to any specific segment routing methods.


**Expert group** For a group of experts _E_, let _R_ _E_ _[m]_ [be a segment-based router that decides whether]
each expert _e ∈_ _E_ should be activated in a segment of some input _T_ with length _m_ ; more specifically,
_R_ _E_ _[m]_ [(] _[e, T, p]_ [)] [ is a prediction sequence similar to] _[ R]_ _e_ _[m]_ [(] _[T, p]_ [)] [ that also follows the segment-prediction]
constraint (Equation 2). Following the same procedure in Appendix C.1, we have



_T_ � _|pT_ =1 _|−m_ +1 �



2 [�]
_F_ 1 ( _R_ _E_ _[m]_ [) =]



(5)
_e∈E_ [[] _[m][ ·][ R]_ _E_ _[m]_ [(] _[e, T, p]_ [) +] _[ f]_ [(] _[e, T, p, m]_ [)]]



2 [�] _T_ � _p_ =1 _m_ � _e∈E_ _[R]_ _E_ _[m]_ [(] _[e, T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)]

~~�~~ _T_ ~~�~~ _|T_ =1 _|−m_ +1 ~~�~~ _e_ _E_ [[] _[m][ ·][ R]_ _E_ _[m]_ [(] _[e, T, p]_ [) +] _[ f]_ [(] _[e, T, p, m]_



_T_ ~~�~~ _|pT_ =1 _|−m_ +1 ~~�~~



Again, _F_ 1 ( _R_ _E_ _[m]_ [)] [ is maximized if and only if] _[ R]_ _E_ _[m]_ [gives active predictions for all expert-segment pairs]
where the expert is activated at least _α_ _e_ _[m]_ [times in the segment, where] _[ α]_ _e_ _[m]_ [is decided by] _[ E]_ [ and] _[ m]_ [.]
Therefore we have



� _f_ ( _e, T, p, m_ )

_f_ ( _e,T,p,m_ ) _≥α_ _[m]_ _e_



SRP( _E, m_ ) ≜ max _F_ 1 ( _R_ _E_ _[m]_ [) =]
_R_ _E_ _[m]_ �

_T_



_|T |−m_ +1
� � [ _m · I_ [ _f_ ( _e, T, p, m_ ) _≥_ _α_ _e_ _[m]_ [] +] _[ f]_ [(] _[e, T, p, m]_ [)]]

_p_ =1 _e∈E_



2 [�]


_T_



(6)



SRP( _E, m_ ) measures how well a group of experts is coordinated by the original router(s) to achieve
layer-level or model-level local routing consistency.


**Segment routing size ratio** Consider the case where the expert group _E_ is the set of all experts
from an MoE layer that activate top- _k_ experts. When we use the prediction of _R_ _E_ _[m]_ [that achieves the]
highest _F_ 1 to route experts, for any segment of input _T_ with length _m_ starting at position _p_, only
experts that is activated at least _α_ _e_ _[m]_ [times by the original router will be chosen. Hence, the expectation]
of the number of routed experts for any segment is given by



_|T |−m_ +1
�

_p_ =1


4



� _I_ [ _f_ ( _e, T, p, m_ ) _≥_ _α_ _e_ _[m]_ []] (7)


_e∈E_



_k_ _m_ = �


_T_



1

_|T_ _| −_ _m_ + 1


That is, _R_ _E_ _[m]_ [will select] _[ k]_ _[m]_ [ experts on average. We define the ratio between] _[ k]_ _[m]_ [ and] _[ k]_ [ as the] **[ segment]**
**routing size ratio** : _ρ_ ( _E, m_ ) ≜ _k_ _m_ _/k_ . A small _ρ_ ( _E, m_ ) indicates that the local routing consistency
of the experts is high enough, so that segment routing does not need to select too many experts to
cover real demands under average cases. We use it as a supplementary metric to distinguish between
cases where groups of experts have similar segment routing best performances. Note that _ρ_ ( _E, m_ ) is
also available for the entire model as long as the total number of activated experts for each token is
also fixed.


Note that in the above definitions, _T_ is unbounded, causing SRP( _e, m_ ), SRP( _E, m_ ) and _ρ_ ( _E, m_ )
to be uncomputable. In experiments, we choose a fixed corpora _S_ (general or domain-specific)
and let _T ∈_ _S_, in which case we write SRP _S_ ( _e, m_ ), SRP _S_ ( _E, m_ ) and _ρ_ _S_ ( _E, m_ ) to indicate the
corpora. Furthermore, we only need to consider _α_ _e_ _[m]_ [and] _[ α]_ _E_ _[m]_ [that are integers, thus we can effectively]
enumerate from 0 to _m_ to find the corresponding _α_ _e_ _[m]_ [and] _[ α]_ _E_ _[m]_ [respectively.]


**2.3** **Segment cache best hit rate (SCH)**


The advantage of SRP as a local routing consistency metric is that it only relies on the expert _e_ (or
expert group _E_ ) and the segment length _m_, and is suitable to analyze individual experts. However, real
expert offloading scenarios usually have a hard cache size limit, so the best global _F_ 1 score may not be
achievable. Moreover, when considering caching performance, _F_ 1 score is not as straightforward as
hit rate (recall). Therefore, we propose another metric for local routing consistency, namely **segment**
**cache best hit rate (SCH)**, that is more related to expert offloading.


We use the same notations as above, and stick to the expert group case where _E_ denotes a group
of experts that activates _k_ experts for each token. Instead of a segment-based router _R_ _E_ _[m]_ [, here we]
consider a segment-based cache _C_ _E_ _[m,ρ]_ where _m_ is the segment length, and _ρ_ be the **segment cache**
**size ratio** ; in other words, _C_ _E_ _[m,ρ]_ has a cache size of _ρk_ . For any input _T_ and any of its sub-segments
of length _m_ starting at position _p_, _C_ _E_ _[m,ρ]_ will choose _ρk_ experts to cache throughout the segment,
without switching any experts. Let _C_ _E_ _[m,ρ]_ ( _e, T, p_ ) = 1 if an expert _e ∈_ _E_ is cached for the segment,
and _C_ _E_ _[m,ρ]_ ( _e, T, p_ ) = 0 otherwise, then the hit rate of _C_ _E_ _[m,ρ]_ across all segments of all possible inputs
is given by



(8)
_e∈E_ _[f]_ [(] _[e, T, p, m]_ [)]



_m_
=1 � _e_ = _E_ _[C]_ _E_ _[m,ρ]_ ( _e, T, p_ ) _· f_ ( _e, T, p, m_ )

~~�~~ _T_ ~~�~~ _|T_ =1 _|−m_ +1 ~~�~~ _e_ _E_ _[f]_ [(] _[e, T, p, m]_ [)]



_r_ ( _C_ _E_ _[m,ρ]_ ) =



�



_T_ � _|pT_ =1 _|−m_ +1 �



_T_ ~~�~~ _|pT_ =1 _|−m_ +1 ~~�~~



We define the segment cache best hit rate of _E_ under segment length _m_ and segment cache size ratio
_ρ_ as the maximum hit rate any _C_ _E_ _[m,ρ]_ can reach: SCH( _E, m, ρ_ ) = max _C_ _E_ _[m,ρ]_ _r_ ( _C_ _E_ _[m,ρ]_ ) . Note that in
Equation 8, the denominator is unrelated to _C_ _E_ _[m,ρ]_ ; therefore, to maximize _r_ ( _C_ _E_ _[m,ρ]_ ), we only need to
make sure that _C_ _E_ _[m,ρ]_ always caches the _ρk_ experts with the highest _f_ :



(9)
_e∈E_ _[f]_ [(] _[e, T, p, m]_ [)]



SCH( _E, m, ρ_ ) =



�



_|T |−m_ +1
_T_ � _p_ =1 � Top _ρk_ _{f_ ( _e, T, p, m_ ) _|e ∈_ _E}_
~~�~~ _T_ ~~�~~ _|T_ =1 _|−m_ +1 ~~�~~ _e_ _E_ _[f]_ [(] _[e, T, p, m]_ [)]



_T_ ~~�~~ _|pT_ =1 _|−m_ +1 ~~�~~



We write SCH _S_ ( _E, m, ρ_ ) when we limit _T_ to a fixed corpora _S_ .


**3** **SRP-based consistency analysis**


**3.1** **Experiment setup**


**Models** We conduct experiments on 20 MoE-based LLMs with model sizes ranging from 3B
to 57B, covering both popular (SwitchTransformers, Mixtral) and recent (DeepSeek-V2, Qwen3)
models. We list their architecture and configuration details in Appendix D.1. We may also use shorter
names (e.g., OLMoE and Qwen3) when there is no ambiguity.


Given that many models also have post-trained (e.g., SFT, RL) versions, we compared the local
routing consistency between base and post-trained versions of several models in Appendix E.1,
where we found no significant difference. Therefore, we always choose the base version in our main
experiments.


5


**Data** We construct our sample corpus _S_ from two sources: (1) **Generic Corpora:** We include
all 7 categories from RedPajama (Together Computer, 2023), including C4, CommonCrawl, Books,
Wikipedia, ArXiv, StackExchange, and GitHub. (2) **Downstream Application:** We append several
datasets with cases aligned with modern LLM applications, including arena-human-preference-140k
(LMArena; LMArena, 2025, OpenMathInstruct-2 (OpenMath; Toshniwal et al., 2025), OpenCodeInstruct (OpenCode; Ahmad et al., 2025), and OpenScienceReasoning-2 (OpenScience; NVIDIA
Corporation, 2025). We treat each RedPajama category and downstream application dataset as a
distinct domain, and refer to its subset corpus using the data source (Books, GitHub, etc.). The full corpus, referred to as _S_, contains 22,528 input samples, each sample having 512 tokens. Appendix D.2
gives more details on the data processing and input generation process.


**Method and configuration** We collect every MoE layer’s routing decisions for every input [†], and for
each expert, count the number of activated tokens _f_ in every segment. Although modern LLMs utilize
position encodings to distinguish tokens from different positions, we demonstrate in Appendix E.4
that segments from different positions have nearly identical SRP, except for the very first ones that
may contain special head tokens. Therefore, we perform calculations on all segments and do not
care about their positions. To obtain SRP, we count the number of segments with the same _f_ for
each expert (group), then compute the _F_ 1 score for every _α_ candidate, choose the _α_ that achieves
the highest _F_ 1 and finally obtain the segment routing best performance and size ratio. We run all
experiments on 8 NVIDIA GeForce RTX 4090 graphics cards and load model parameters with BF16
precision.


**3.2** **Overall results**


Figure 2 illustrates SRP( _E, m_ ) of each model under various segment lengths _m_ . While most models
have similar SRP and _ρ_ when _m_ = 4, the difference between models becomes significant as the
segment length increases. Meanwhile, the relative distribution of SRP across models appears similar
after _m_ = 16 . There is a gap between short-term ( _m_ = 4 ) and long-term ( _m ≥_ 16 ) local routing
consistency, where **many models exhibit the short-term one but only a few demonstrate the**
**long-term one** .


4





3.5


3


2.5


2


1.5


1




















































|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|QW1<br>QW1<br>QW1<br>QW1<br>QW1<br><br><br><br><br><br>STe<br>STe<br>STe<br>STe<br>STe<br>STd<br>STd<br>STd<br>STd<br>STd|QW2<br>QW2<br>QW2<br>QW2<br>QW2<br><br><br><br>JB<br>JB<br>JB<br>JB<br>JB<br>XV<br>XV<br>XV<br>XV<br>XV<br>~~DS1~~<br>~~DS1~~<br>~~DS1~~<br>~~DS1~~<br>~~DS1~~<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br><br><br><br><br><br>~~OP~~<br>~~OP~~<br>~~OP~~<br>~~OP~~<br>~~OP~~<br>JJ<br>JJ<br>J<br>~~LL1~~<br>~~LL~~<br>~~LL1~~<br>~~LL1~~<br>~~LL1~~|MX<br>MX<br>MX<br>MX<br>MX<br>MC<br>MC<br>MC<br>MC<br>MC<br>TT<br>TT<br>T<br><br><br><br><br><br>PW<br>PW<br>PW<br>PW<br>PW|||













PH ~~PW~~ NLe XV GR PWPH ~~NLe~~ XV GR PWPH



JBLL1 JT MCPW NLd XV GR NLd OL NLd









JBLL1 MCPW NLd XV GR NLd OL OL





QW3 LL2 QW3 LL2 QW3









~~LL2~~ ~~NLe~~ OL LL2 QW3 LL2 QW3 LL2















Y2 Y2 Y2 Y2



0.5 0.2 0.4 QW2 0.6 0.8


|Col1|Col2|SSSTTTeee|SSSSSTTTTTddddd<br>ee|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|||~~NL~~<br>~~NL~~<br>~~NLe~~<br>~~NL~~<br>~~NL~~<br>ST<br><br><br>ST<br>|~~NL~~<br>~~NL~~<br>~~NLe~~<br>~~NL~~<br>~~NL~~<br>ST<br><br><br>ST<br>|~~NL~~<br>~~NL~~<br>~~NLe~~<br>~~NL~~<br>~~NL~~<br>ST<br><br><br>ST<br>|~~NL~~<br>~~NL~~<br>~~NLe~~<br>~~NL~~<br>~~NL~~<br>ST<br><br><br>ST<br>|~~NL~~<br>~~NL~~<br>~~NLe~~<br>~~NL~~<br>~~NL~~<br>ST<br><br><br>ST<br>|
|||NL<br>NL<br>NL<br>NL<br>NL|d<br>d<br>d<br>d<br>d<br>QW1<br>QW1<br>QW1<br>QW1<br>QW1<br>OP<br>OP<br>OP<br>OP<br>OP||||
||||||||
||||QW2<br>QW2<br>QW2<br>QW2<br>QW2<br>JB<br>JB<br>JB<br>JB<br>JB<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>XV<br>XV<br>XV<br>XV<br>XV<br>DS1<br>DS1<br>DS1<br>DS1<br>DS1<br>DS<br>DS<br>DS<br>DS<br>DS<br>JJ<br>JJ<br>J<br>LL1<br>LL1<br>LL1<br>LL1<br>LL1|MX<br>MX<br>MX<br>MX<br>MX<br><br><br><br><br><br>PH<br>PH<br>PH<br>PH<br>PH<br>Y2<br>Y2<br>Y2<br>Y2<br>Y2<br>~~QW~~<br>~~Q~~<br>~~QW~~<br>~~Q~~<br>~~Q~~<br><br><br><br>2<br>2<br>2<br>2<br>2<br>MC<br>MC<br>MC<br>MC<br>MC<br>TT<br>TT<br>T<br>~~OL~~<br>~~OL~~<br>~~OL~~<br>~~OL~~<br>~~OL~~<br>PW<br>PW<br>PW<br>PW<br>PW|~~3~~<br>~~W3~~<br>~~3~~<br>~~W3~~<br>~~W3~~|~~LL2~~<br>~~LL2~~<br>~~LL2~~<br>~~LL2~~<br>~~LL2~~|


|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
||||||
|ST<br>ST<br>ST<br>ST<br>ST<br>ST<br>ST<br>ST<br>ST<br>ST|QW2<br>QW2<br>QW2<br>QW2<br>QW2<br>JB<br>JB<br>JB<br>JB<br>JB<br>DS1<br>DS1<br>DS1<br>DS1<br>DS1<br>QW1<br>QW1<br>QW1<br>QW1<br>QW1<br>OP<br>OP<br>OP<br>OP<br>OP<br>e<br>e<br>e<br>e<br>e<br>d<br>d<br>d<br>d<br>d<br>L<br>L<br>L<br>L<br>L|MX<br>MX<br>MX<br>MX<br>MX<br><br><br>~~MC~~<br>MC<br>MC<br>~~MC~~<br>MC<br>JTJT<br>JTJT<br>JT<br>L1<br>L1<br>L1<br>L1<br>L1<br>~~PW~~<br>~~PW~~<br>~~PW~~<br>~~PW~~<br>~~PW~~|||
||~~NLe~~<br>~~NLe~~<br>~~NLe~~<br>~~NLe~~<br>~~NLe~~<br>NLd<br>NLd<br>NLd<br>NLd<br>NLd<br>XV<br>XV<br>XV<br>XV<br>XV<br><br><br>|GR<br>GR<br>GR<br>GR<br>GR<br>PH<br>PH<br>PH<br>PH<br>PH<br>QW3<br>QW3<br>QW3<br>QW3<br>QW3<br><br><br><br><br><br>DS2<br>DS2<br>DS2<br>DS2<br>DS2<br>~~OL~~<br>~~OL~~<br>~~OL~~<br>~~OL~~<br>~~OL~~<br><br><br><br><br>|Y2<br>Y2<br>Y2<br>Y2<br>Y2<br>LL2<br>LL2<br>LL2<br>LL2<br>LL2||


|Col1|LLLLLLLLLL11111|Col3|Col4|Col5|
|---|---|---|---|---|
||~~JB~~<br>~~JB~~<br>~~JB~~<br>~~JB~~<br>~~JB~~<br><br><br><br><br><br>JTJT<br>JTJT<br>JT<br><br><br><br><br>||||
|~~NLe~~<br>NLe<br>NLe<br>~~NLe~~<br>~~NLe~~<br>QW<br>QW<br>QW<br>QW<br>QW<br>~~OP~~<br>O<br>OP<br>~~O~~<br>~~OP~~<br>STe<br>STe<br>STe<br>STe<br>STe|~~QW2~~<br>QW2<br>QW2<br>~~QW2~~<br>~~QW2~~<br><br><br><br>XV<br>XV<br>XV<br>XV<br>XV<br>DS1<br>DS1<br>DS1<br>DS1<br>DS1<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>1<br>1<br>1<br>1<br>1<br>MC<br>~~MC~~<br>~~MC~~<br>MC<br>~~MC~~<br><br>P<br><br>~~P~~<br>|MX<br>MX<br>MX<br>MX<br>MX<br><br><br>PW<br>PW<br>PW<br>PW<br>PW|||
|N<br><br>N<br><br>|Ld<br>NLd<br>Ld<br>NLd<br>NLd<br>GR<br>GR<br>GR<br>GR<br>GR<br>O<br>O<br>O<br>O<br>O|PH<br>PH<br>PH<br>PH<br>PH<br>Y<br>Y<br>Y<br>Y<br>Y<br>~~QW3~~<br>~~QW3~~<br>~~QW3~~<br>~~QW3~~<br>~~QW3~~<br>L<br>L<br>L<br>L<br>L|2<br>2<br>2<br>2<br>2<br>~~LL2~~<br>~~LL2~~<br>~~LL2~~<br>~~LL2~~<br>~~LL2~~||



0.2 0.4 0.6 0.8



0.2 0.4 0.6 0.8



0.2 0.4 0.6 0.8



SRP(E,4) SRP(E,16) SRP(E,64) SRP(E,256)


PowerMoE LLaMA-MoE-v1 OLMoE SwitchTransformers LLaMA-MoE-v2 JetMoE OpenMoE MiniCPM-MoE Qwen1.5-MoE DeepSeek-V2-Lite


DeepSeekMoE XVERSE-MoE Qwen3 Yuan2.0 Phi-3.5-MoE GRIN-MoE Mixtral-8x7B Jamba-Mini NLLB-MoE Qwen2


Figure 2: SRP( _E, m_ ) of each model on _S_, compared with the segment routing size ratio. Marker
size represents model size.


We roughly divide the models into four groups that have similar SRP characteristics, whose SRP
when _m_ = 16 are demonstrated in Table 1:


 - Group 1 (LLaMA-MoE-v2–OLMoE) has the highest SRP ( _>_ 0 _._ 5 when _m_ = 16 ) and _ρ_ ( _∼_ 1 _._ 25 )
across all segment lengths, showing strong long-term local routing consistency.

 - Group 2 (Mixtral-8x7B–LLaMA-MoE-v1) have the second highest SRP ( _∼_ 0 _._ 48 when _m_ = 16 ),
but their long-term _ρ_ becomes high ( _∼_ 2 _._ 5).

 - Group 3 (XVERSE-MoE–DeepSeekMoE) has a significantly lower SRP than group 2, especially
the long-term one ( _∼_ 0 _._ 36 when _m_ = 16), but their _ρ_ is a bit lower _∼_ 2 _._ 0.

 - Group 4 (NLLB-MoE–SwitchTransformers) have the lowest SRP ( _<_ 0 _._ 31 when _m_ = 16 );
contrasting other models, their short-term _ρ_ is already high, but their long-term _ρ_ becomes lower.


  - In encoder-decoder models, encoder layers only consider encoder input, and decoder layers likewise.


6


Table 1: SRP( _E,_ 16) on _S_ in descending order and several architecture parameters. “A:T”: ratio
between active and all experts; “S:A”: ratio between shared and active experts; “every _x_ ”: apply MoE
every _x_ layers; “after 1st”: apply MoE after the first layer.



Model SRP MoE A:T S:A


LLaMA-MoE-v2 78.16 all 1:4 0

Yuan2.0 63.48 all 1:16 0

PowerMoE 55.17 all 1:5 0
Qwen3 54.14 all 1:16 0
Phi-3.5-MoE 51.98 all 1:8 0

OLMoE 50.91 all 1:8 0

GRIN-MoE 50.39 all 1:8 0


Mixtral-8x7B 49.36 all 1:4 0

MiniCPM-MoE 48.85 all 1:4 0

JetMoE 47.45 all 1:4 0

LLaMA-MoE-v1 45.29 all 1:4 0


**3.3** **Analysis**



Model SRP MoE A:T S:A


XVERSE-MoE 38.58 all 3:32 1:3
Jamba-Mini 38.08 every 2 1:8 0
DeepSeek-V2-Lite 37.92 after 1st 3:32 1:3
DeepSeekMoE 36.94 after 1st 3:32 1:3
Qwen2 36.74 all 1:8 1:1


NLLB-MoE (encoder) 25.24 every 4 1:64 0
(decoder) 31.35
Qwen1.5-MoE 30.71 all 1:15 1:1
OpenMoE 28.77 every 6 1:16 1:2
SwitchTF (encoder) 19.33 every 2 1:128 0
(decoder) 19.27



**Which model architecture has the highest local routing consistency?** We compare the SRP
of different models with some architecture parameters in Table 1. Surprisingly, the least sparse
models **do not always** have very high local routing consistency, even though they activate experts
more frequently on average. Instead, we observe two common points that are possibly connected
to high local routing consistency: (1) **Apply MoE on every layer:** all models in groups 1 and 2
apply the MoE structure on every layer, while many group 3 and 4 models skip some layers (e.g.,
Jamba). (2) **No shared experts:** all models in groups 1 and 2 do not include any shared experts,
unlike many group 3 and 4 models (e.g., Qwen2). Both ensure that no dense modules (dense layers
or shared experts) are engaged. We conjecture that dense modules may interfere or weaken MoE
routing signals, resulting in (a) smoother routing distributions that cause inconsistency over edge
cases, and (b) less specialized experts that contribute to local routing consistency (see Section 4).
Thus, removing them effectively eliminates these negative factors. We also compare SRP with corpus
perplexity (Appendix E.2) and other model designs (Appendix E.3), where we find little correlation.


Table 2: SRP( _E,_ 16) on _S_, along with load balance (LB) measured by activation frequency standard
deviation of experts.


Model SRP LB Model SRP LB Model SRP LB


LLaMA-MoE-v2 78.16 29.04 Mixtral-8x7B 49.36 2.70 DeepSeekMoE 36.94 2.03
Yuan2.0 63.48 13.86 MiniCPM-MoE 48.85 2.59 Qwen2 36.74 6.74
PowerMoE 55.17 12.90 JetMoE 47.45 1.12 NLLB-MoE (en) 25.24 1.75
Qwen3 54.14 3.19 LLaMA-MoE-v1 45.29 2.66 (de) 31.35 2.13
Phi-3.5-MoE 51.98 4.90 XVERSE-MoE 38.58 2.71 Qwen1.5-MoE 30.71 0.58
OLMoE 50.91 6.79 Jamba-Mini 38.08 3.05 OpenMoE 28.77 2.56
GRIN-MoE 50.39 3.89 DeepSeek-V2-Lite 37.92 2.34 SwitchTF (en) 19.33 0.58
(de) 19.27 0.66


**Can local routing consistency live with load balance?** Load balance is a key feature for efficient
MoE inference (Lepikhin et al., 2021), but it is seemingly against local routing consistency. For
instance, both DeepSeek-AI et al. (2024b) and Skliar et al. (2024) suggest adding bias to router
outputs. Still, the former promotes _little activated_ experts for load balance and the latter promotes
_recently cached_ experts for effective caching. To investigate their relation, we compute the standard
deviation of all experts’ activation frequencies in a model and compare it with SRP in Table 2.
Many models with high SRP also exhibit imbalanced routing, which largely contributes to their local
routing consistency (details in Appendix E.9). However, models like Qwen3 and GRIN-MoE enjoy
high local routing consistency and moderate load balance simultaneously, in which we found strong
domain-specialized experts (see Section 4). Based on the observations, we claim that **local routing**
**consistency can coexist with load balance through domain-specialized experts.**


7


**4** **Local routing consistency and expert specialization**


**4.1** **Domain-wise local routing consistency**


LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE


+10%


SRP

(E,16)


-10%


LLaMA-MoE-v1 XVERSE-MoE Jamba-Mini DeepSeek-V2-Lite DeepSeekMoE Qwen2 NLLB-MoE Qwen1.5-MoE OpenMoE SwitchTransformers


+10%


SRP

(E,16)


-10%



C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS



Figure 3: SRP _D_ ( _E,_ 16) on each domain _D_, relative to SRP _S_ ( _E,_ 16) . C4: C4; CC: CommonCrawl;
BK: Books; WK: Wikipedia; AX: ArXiv; SE: StackExchange; GH: GitHub; LM: LMArena; OM:
OpenMath; OC: OpenCode; OS: OpenScience. For encoder-decoder models, light color represents
the encoder and dark color represents the decoder.


In Section 3, we analyze models on the full corpus _S_, which consists of text data from 7 different
domains. However, each domain has its token distributions, which may affect the router decision’s
distribution. Figure 3 illustrates the relative difference between domain-wise and global SRP of each
model when _m_ = 16, where we observe three different patterns among all models: (1) Models like
Phi-3.5-MoE, GRIN-MoE, and OLMoE have significantly **higher SRP on ArXiv, StackExchange**
**and GitHub**, whose SRP can be more than 10% higher than global SRP. They also exhibit higher SRP
on OpenMath and OpenCode, indicating specialized experts for math and coding tasks. (2) Models
like LLaMA-MoE-v2, Yuan2.0, and Qwen3 have significant **higher SRP on Wikipedia and other**
**generic domains** but lower on OpenMath and OpenCode. They seem to have specialized experts
for generic text (e.g., multilingual experts) instead of math or coding. (3) Models like Mixtral-8x7B,
MiniCPM-MoE and JetMoE have **similar SRP across all domains** with insignificant differences.
All of them have mediocre to low SRP. Above all, models exhibit balanced local routing consistency
across all domains or higher local routing consistency on certain domains with unique properties.


**4.2** **Expert specialization**


We argue that domain-wise local routing consistency patterns appear across models due to specialized
experts in each model. To clarify this, we consider two types of expert specialization, first introduced
by Muennighoff et al. (2025): (1) **Domain specialization:** the normalized frequency of an expert _e_
being activated on tokens from a specific domain _D_ . We compute the coefficient of variation (CV) of
activation frequency across all domains as a domain-free metric. (2) **Vocabulary specialization:** the
normalized frequency of an expert _e_ being activated on a specific token ID _x_ . We follow Muennighoff
et al. (2025) to obtain the vocabulary specialization of each expert. We compare each model’s SRP,
average expert specialization, and the correlation between experts’ specialization and SRP in Figure 4;
expert distribution between specialization and SRP is also demonstrated in Appendix E.9.



1


0.5


0


−0.5



Domain Specialization Input Vocabulary Specialization Pred. Output Vocab. Spec. G. T. Output Vocab. Spec.









~~OL~~ ~~OL~~











STe LL2





MC QW1 GR PH QW1









PH Y2 GR PH



Y2 GR PH Y2





JT





















OP DS2 MC













~~OP~~



QW2


























|Col1|O O O O O LL1 LL1 LL1 LL1 LL1|OL OL OL OL OL|Col4|DS1 DS1 DS1 DS2 DS2 DS2 DS2 DS2 MC MC MC MC MC OP OP OP OP OP|Col6|
|---|---|---|---|---|---|
||QW2<br>QW2<br>QW2<br>QW2<br>QW2<br>~~JB~~<br>~~JB~~<br>~~JB~~<br>~~JB~~<br>~~JB~~<br>MX<br>MX<br>MX<br>MX<br>MX<br>GR<br>GR<br>GR<br>GR<br>GR<br>DS1<br>DS1<br>DS1<br>DS1<br>DS1<br>DS2<br>DS2<br>DS2<br>DS2<br>DS2<br>QW1<br>QW1<br>QW1<br>QW1<br>QW1<br>MC<br>MC<br>MC<br>MC<br>MC<br><br><br><br><br><br><br><br><br><br><br><br><br>|PH<br>PH<br>PH<br>PH<br>PH<br>Y2<br>Y2<br>Y2<br>Y2<br>Y2<br>QW3<br>QW3<br>QW3<br>QW3<br>QW3<br><br><br><br><br><br><br><br><br><br><br>PW<br>PW<br>PW<br>PW<br>PW||QW2<br>QW2<br>QW2<br>QW2<br>QW2<br>MX<br>MX<br>MX<br>MX<br>MX<br><br><br><br>XV<br>XV<br>XV<br>XV<br>XV<br>DS1<br>DS1<br>DS1<br>DS1<br>DS1<br>MC<br><br><br>MC<br>MC<br><br><br><br><br><br>~~LL1~~<br>~~LL1~~<br>~~LL1~~<br>~~LL1~~<br>~~LL1~~|~~QW3~~<br>~~QW3~~<br>~~QW3~~<br>~~QW3~~<br>~~QW3~~<br>PW<br>PW<br>PW<br>PW<br>PW|
||XV<br>XV<br>XV<br>XV<br>XV<br>~~OP~~<br>~~OP~~<br>~~OP~~<br>~~OP~~<br>~~OP~~|||||









−1 0.2 0.4 0.6 0.8


|SSSSSTTTTTeeeee<br>SSSSSTTTTTddddd|DDDDDSSSSS11111DDDDDSSSSS22222 XXXXXVVVVVGGGGGRRRRR PPPPPHHHHH<br>QQQQQWWWWW11111 JJJJJTTTTTOOOOOQQLLQLQQLLWWWWW33333<br>NNNNNLLLLLddddd MMMMMCCCCC<br>OOOOOPPPPP JJJJJBBBBB MMMMMXXXXX|Col3|
|---|---|---|
||NLe<br>NLe<br>NLe<br>NLe<br>NLe<br><br><br><br><br><br>LL1<br>LL1<br>LL1<br>LL1<br>LL1<br>PW<br>PW<br>PW<br>PW<br>PW|~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br><br><br><br><br>|
||QW2<br>QW2<br>QW2<br>QW2<br>QW2|QW2<br>QW2<br>QW2<br>QW2<br>QW2|



0.2 0.4 0.6 0.8



0.2 0.4 0.6 0.8



0.2 0.4 0.6 0.8



SRP(E,16) SRP(E,16) SRP(E,16) SRP(E,16)


PowerMoE LLaMA-MoE-v1 OLMoE SwitchTransformers LLaMA-MoE-v2 JetMoE OpenMoE MiniCPM-MoE Qwen1.5-MoE DeepSeek-V2-Lite


DeepSeekMoE XVERSE-MoE Qwen3 Yuan2.0 Phi-3.5-MoE GRIN-MoE Mixtral-8x7B Jamba-Mini NLLB-MoE Qwen2


Figure 4: SRP( _E,_ 16) of each model, compared with average expert specialization (marker size) and
the correlation between expert specialization and SRP (y-axis).


8


**Domain specialization** Many models show a positive correlation between their experts’ domain
specialization and SRP. An exception is LLaMA-MoE-v2, which constantly activates a group of
experts, resulting in very high SRP. Other exceptions (Qwen2 and LLaMA-MoE) hardly have any
domain specialization. In contrast, Qwen3, Phi-3.5-MoE, GRIN-MoE, and OLMoE exhibit high
SRP, high average domain specialization, and strong correlation between them simultaneously. These
models also demonstrate good load balance (see Table 2), indicating that their **high proportion of**
**domain specialized experts contributes to both local routing consistency and load balance** .


**Vocabulary specialization** We consider three kinds of vocabulary specialization on the input,
the model’s predicted output, and the ground-truth, respectively (Muennighoff et al., 2025). Most
models demonstrate negative or insignificant correlation between _input_ vocabulary specialization
and SRP; LLaMA-MoE-v2 becomes the only exception, also due to the constantly activated experts.
On the other hand, SRP is slightly positively correlated to _prediction_ or _ground_ truth vocabulary
specialization. We conjecture that such specialization happens more in later layers (Muennighoff
et al., 2025) that process high-level information related to the context topic.


Above all, we can see that **domain specialization plays a more important role in forming local**
**routing consistency than vocabulary specialization**, especially on load-balanced models.


**5** **SCH-based consistency analysis**


**5.1** **Overall results**


As mentioned in Section 2.3, SRP has several flaws that hinder its application in expert offloading.
This section focuses on the segment cache best hit rate (SCH), which works with a size limit, to
obtain a more straightforward insight into expert offloading and cache management. Based on the
number of activated tokens in every input segment from the corpus for each expert, defined as _f_ in
Section 3.1, we calculate each model and each layer’s SCH on every possible cache size: At each
segment, we sort experts in each layer or model by their _f_ in descending order, and compute the
segment cache best hit rate at cache sizes ranging from 1 to _|E|_ .


Figure 5 illustrates SCH( _E, m, ρ_ ) of each model under different _m_ s and _ρ_ s. We can easily identify
the four groups of models mentioned in Section 3.2 starting from _m_ = 16 : Group 1 models have
the fastest growing SCH with respect to _rho_ when _ρ_ is small, as well as turning points near _ρ_ = 2,
after which they share similar SCH with group 2 models. Meanwhile, models from groups 3 and 4
have relatively low SCH, growing nearly linearly as _ρ_ increases. Since only group 1 models (with the
highest local routing consistency) have turning points on SCH, we claim that in general, _ρ_ = **2** **can**
**balance cache effectiveness and efficiency.**


1 m=4 m=16 m=64 m=256


0.8


0.6


0.4


0.2



00 1 2 3 4



0 1 2 3 4 0 1 2 3 4 0 1 2 3 4



ρ ρ ρ ρ



PowerMoE LLaMA-MoE-v1 OLMoE SwitchTransformers (Encoder)

SwitchTransformers (Decoder)



LLaMA-MoE-v2 JetMoE OpenMoE MiniCPM-MoE Qwen1.5-MoE DeepSeek-V2-Lite



DeepSeekMoE XVERSE-MoE Qwen3 Yuan2.0 Phi-3.5-MoE GRIN-MoE Mixtral-8x7B Jamba-Mini NLLB-MoE (Encoder)

NLLB-MoE (Decoder)



Qwen2



Figure 5: SCH( _E, m, ρ_ ) of each model on _S_ under different segment length _m_ and segment cache
size ratio _ρ_ . Solid line: group 1; dashed: group 2; dash-dotted: group 3; dotted: group 4.


**5.2** **SCH vs. common cache algorithm hit rate**


Since SCH is based on an ideal cache system that relies on oracle information, it is crucial to
understand how well it is correlated with real-world implementations. Table 3 lists the correlation
between SCH and the cache hit rate of several widely adopted cache algorithms. All compared cache
algorithms have hit rates highly correlated to SCH, even for short segments ( _m_ = 4 ). Furthermore,


9


Table 3: Correlation between SCH and the hit rate of common cache algorithms across all models.
LRU: least recently used; LFU: least frequently used; Fixed: fixed cache.


_m_ LRU LFU Fixed


4 81.20 77.39 76.26

16 90.43 88.70 89.79

64 93.10 92.82 95.50

256 97.52 99.20 97.91


Appendix E.6 reveals that SRP and SCH are also highly correlated with each other. This suggests
that models with higher local routing consistency tend to achieve higher expert cache hit rates, hence
greater performance gain with expert offloading.


**6** **Conclusion**


In this paper, we investigate the property of MoE LLMs where similar experts can be continuously
activated, namely _local routing consistency_ . We propose two metrics to measure this property:
segment routing best performance (SRP) and segment cache best hit rate (SCH). We compare SRP
and SCH between multiple models and identify several key designs that may help improve local
routing consistency of MoE LLMs. We further suggest that a cache size approximately 2x the number
of active experts can balance cache effectiveness and efficiency.


**Ethics statement** Our analytic methods and results still help design new MoE LLMs friendly to
expert offloading and enable deployment on resource-constrained edge devices. While our study will
likely have an indirect social impact, developers implementing local routing consistency to build
more powerful LLMs must take responsibility for their products’ societal implications.


**Reproducibility statement** We constructed our sample corpus _S_ with deterministic algorithms,
and we will publish the sampled _S_ to ensure reproducibility. We also conducted all experiments with
a deterministic configuration and will release relevant source code.


**References**


Marah Abdin, Jyoti Aneja, Hany Awadalla, Ahmed Awadallah, Ammar Ahmad Awan, Nguyen
Bach, Amit Bahree, Arash Bakhtiari, Jianmin Bao, Harkirat Behl, Alon Benhaim, Misha Bilenko,
Johan Bjorck, Sébastien Bubeck, Martin Cai, Qin Cai, Vishrav Chaudhary, Dong Chen, Dongdong
Chen, Weizhu Chen, Yen-Chun Chen, Yi-Ling Chen, Hao Cheng, Parul Chopra, Xiyang Dai,
Matthew Dixon, Ronen Eldan, Victor Fragoso, Jianfeng Gao, Mei Gao, Min Gao, Amit Garg,
Allie Del Giorno, Abhishek Goswami, Suriya Gunasekar, Emman Haider, Junheng Hao, Russell J.
Hewett, Wenxiang Hu, Jamie Huynh, Dan Iter, Sam Ade Jacobs, Mojan Javaheripi, Xin Jin,
Nikos Karampatziakis, Piero Kauffmann, Mahoud Khademi, Dongwoo Kim, Young Jin Kim, Lev
Kurilenko, James R. Lee, Yin Tat Lee, Yuanzhi Li, Yunsheng Li, Chen Liang, Lars Liden, Xihui
Lin, Zeqi Lin, Ce Liu, Liyuan Liu, Mengchen Liu, Weishung Liu, Xiaodong Liu, Chong Luo,
Piyush Madan, Ali Mahmoudzadeh, David Majercak, Matt Mazzola, Caio César Teodoro Mendes,
Arindam Mitra, Hardik Modi, Anh Nguyen, Brandon Norick, Barun Patra, Daniel Perez-Becker,
Thomas Portet, Reid Pryzant, Heyang Qin, Marko Radmilac, Liliang Ren, Gustavo de Rosa,
Corby Rosset, Sambudha Roy, Olatunji Ruwase, Olli Saarikivi, Amin Saied, Adil Salim, Michael
Santacroce, Shital Shah, Ning Shang, Hiteshi Sharma, Yelong Shen, Swadheen Shukla, Xia Song,
Masahiro Tanaka, Andrea Tupini, Praneetha Vaddamanu, Chunyu Wang, Guanhua Wang, Lijuan
Wang, Shuohang Wang, Xin Wang, Yu Wang, Rachel Ward, Wen Wen, Philipp Witte, Haiping Wu,
Xiaoxia Wu, Michael Wyatt, Bin Xiao, Can Xu, Jiahang Xu, Weijian Xu, Jilong Xue, Sonali Yadav,
Fan Yang, Jianwei Yang, Yifan Yang, Ziyi Yang, Donghan Yu, Lu Yuan, Chenruidong Zhang, Cyril
Zhang, Jianwen Zhang, Li Lyna Zhang, Yi Zhang, Yue Zhang, Yunan Zhang, and Xiren Zhou.
Phi-3 technical report: A highly capable language model locally on your phone. _arXiv preprint_,
April 2024. doi: 10.48550/ARXIV.2404.14219.


10


Wasi Uddin Ahmad, Aleksander Ficek, Mehrzad Samadi, Jocelyn Huang, Vahid Noroozi, Somshubra
Majumdar, and Boris Ginsburg. Opencodeinstruct: A large-scale instruction tuning dataset for
code llms. _arXiv preprint_, April 2025. doi: 10.48550/ARXIV.2504.04030.


Weilin Cai, Juyong Jiang, Fan Wang, Jing Tang, Sunghun Kim, and Jiayi Huang. A survey on mixture
of experts in large language models. _IEEE Transactions on Knowledge and Data Engineering_
_(TKDE) 2025_, pp. 1–20, June 2024. ISSN 2326-3865. doi: 10.1109/tkde.2025.3554028.


Shengzhuang Chen, Ying Wei, and Jonathan Richard Schwarz. Automatic expert discovery in llm
upcycling via sparse interpolated mixture-of-experts. _arXiv preprint_, June 2025. doi: 10.48550/A
RXIV.2506.12597.


Tianyu Chen, Shaohan Huang, Yuan Xie, Binxing Jiao, Daxin Jiang, Haoyi Zhou, Jianxin Li, and
Furu Wei. Task-specific expert pruning for sparse mixture-of-experts. _arXiv preprint_, June 2022.
doi: 10.48550/ARXIV.2206.00277.


Damai Dai, Chengqi Deng, Chenggang Zhao, R.x. Xu, Huazuo Gao, Deli Chen, Jiashi Li, Wangding
Zeng, Xingkai Yu, Y. Wu, Zhenda Xie, Y.k. Li, Panpan Huang, Fuli Luo, Chong Ruan, Zhifang Sui,
and Wenfeng Liang. DeepSeekMoE: Towards ultimate expert specialization in mixture-of-experts
language models. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), _Proceedings of the_
_62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_,
pp. 1280–1297, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi:
[10.18653/v1/2024.acl-long.70. URL https://aclanthology.org/2024.acl-long.70/.](https://aclanthology.org/2024.acl-long.70/)


DeepSeek-AI, Aixin Liu, Bei Feng, Bin Wang, Bingxuan Wang, Bo Liu, Chenggang Zhao, Chengqi
Dengr, Chong Ruan, Damai Dai, Daya Guo, Dejian Yang, Deli Chen, Dongjie Ji, Erhang Li,
Fangyun Lin, Fuli Luo, Guangbo Hao, Guanting Chen, Guowei Li, H. Zhang, Hanwei Xu, Hao
Yang, Haowei Zhang, Honghui Ding, Huajian Xin, Huazuo Gao, Hui Li, Hui Qu, J. L. Cai, Jian
Liang, Jianzhong Guo, Jiaqi Ni, Jiashi Li, Jin Chen, Jingyang Yuan, Junjie Qiu, Junxiao Song, Kai
Dong, Kaige Gao, Kang Guan, Lean Wang, Lecong Zhang, Lei Xu, Leyi Xia, Liang Zhao, Liyue
Zhang, Meng Li, Miaojun Wang, Mingchuan Zhang, Minghua Zhang, Minghui Tang, Mingming
Li, Ning Tian, Panpan Huang, Peiyi Wang, Peng Zhang, Qihao Zhu, Qinyu Chen, Qiushi Du, R. J.
Chen, R. L. Jin, Ruiqi Ge, Ruizhe Pan, Runxin Xu, Ruyi Chen, S. S. Li, Shanghao Lu, Shangyan
Zhou, Shanhuang Chen, Shaoqing Wu, Shengfeng Ye, Shirong Ma, Shiyu Wang, Shuang Zhou,
Shuiping Yu, Shunfeng Zhou, Size Zheng, T. Wang, Tian Pei, Tian Yuan, Tianyu Sun, W. L.
Xiao, Wangding Zeng, Wei An, Wen Liu, Wenfeng Liang, Wenjun Gao, Wentao Zhang, X. Q. Li,
Xiangyue Jin, Xianzu Wang, Xiao Bi, Xiaodong Liu, Xiaohan Wang, Xiaojin Shen, Xiaokang
Chen, Xiaosha Chen, Xiaotao Nie, Xiaowen Sun, Xiaoxiang Wang, Xin Liu, Xin Xie, Xingkai
Yu, Xinnan Song, Xinyi Zhou, Xinyu Yang, Xuan Lu, Xuecheng Su, Y. Wu, Y. K. Li, Y. X. Wei,
Y. X. Zhu, Yanhong Xu, Yanping Huang, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Li, Yaohui
Wang, Yi Zheng, Yichao Zhang, Yiliang Xiong, Yilong Zhao, Ying He, Ying Tang, Yishi Piao,
Yixin Dong, Yixuan Tan, Yiyuan Liu, Yongji Wang, Yongqiang Guo, Yuchen Zhu, Yuduan Wang,
Yuheng Zou, Yukun Zha, Yunxian Ma, Yuting Yan, Yuxiang You, Yuxuan Liu, Z. Z. Ren, Zehui
Ren, Zhangli Sha, Zhe Fu, Zhen Huang, Zhen Zhang, Zhenda Xie, Zhewen Hao, Zhihong Shao,
Zhiniu Wen, Zhipeng Xu, Zhongyu Zhang, Zhuoshu Li, Zihan Wang, Zihui Gu, Zilin Li, and Ziwei
Xie. Deepseek-v2: A strong, economical, and efficient mixture-of-experts language model. _arXiv_
_preprint_, May 2024a. doi: 10.48550/ARXIV.2405.04434.


DeepSeek-AI, Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang
Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, Damai Dai, Daya Guo, Dejian Yang, Deli
Chen, Dongjie Ji, Erhang Li, Fangyun Lin, Fucong Dai, Fuli Luo, Guangbo Hao, Guanting Chen,
Guowei Li, H. Zhang, Han Bao, Hanwei Xu, Haocheng Wang, Haowei Zhang, Honghui Ding,
Huajian Xin, Huazuo Gao, Hui Li, Hui Qu, J. L. Cai, Jian Liang, Jianzhong Guo, Jiaqi Ni, Jiashi
Li, Jiawei Wang, Jin Chen, Jingchang Chen, Jingyang Yuan, Junjie Qiu, Junlong Li, Junxiao Song,
Kai Dong, Kai Hu, Kaige Gao, Kang Guan, Kexin Huang, Kuai Yu, Lean Wang, Lecong Zhang,
Lei Xu, Leyi Xia, Liang Zhao, Litong Wang, Liyue Zhang, Meng Li, Miaojun Wang, Mingchuan
Zhang, Minghua Zhang, Minghui Tang, Mingming Li, Ning Tian, Panpan Huang, Peiyi Wang,
Peng Zhang, Qiancheng Wang, Qihao Zhu, Qinyu Chen, Qiushi Du, R. J. Chen, R. L. Jin, Ruiqi
Ge, Ruisong Zhang, Ruizhe Pan, Runji Wang, Runxin Xu, Ruoyu Zhang, Ruyi Chen, S. S. Li,
Shanghao Lu, Shangyan Zhou, Shanhuang Chen, Shaoqing Wu, Shengfeng Ye, Shengfeng Ye,
Shirong Ma, Shiyu Wang, Shuang Zhou, Shuiping Yu, Shunfeng Zhou, Shuting Pan, T. Wang, Tao


11


Yun, Tian Pei, Tianyu Sun, W. L. Xiao, Wangding Zeng, Wanjia Zhao, Wei An, Wen Liu, Wenfeng
Liang, Wenjun Gao, Wenqin Yu, Wentao Zhang, X. Q. Li, Xiangyue Jin, Xianzu Wang, Xiao Bi,
Xiaodong Liu, Xiaohan Wang, Xiaojin Shen, Xiaokang Chen, Xiaokang Zhang, Xiaosha Chen,
Xiaotao Nie, Xiaowen Sun, Xiaoxiang Wang, Xin Cheng, Xin Liu, Xin Xie, Xingchao Liu, Xingkai
Yu, Xinnan Song, Xinxia Shan, Xinyi Zhou, Xinyu Yang, Xinyuan Li, Xuecheng Su, Xuheng Lin,
Y. K. Li, Y. Q. Wang, Y. X. Wei, Y. X. Zhu, Yang Zhang, Yanhong Xu, Yanhong Xu, Yanping
Huang, Yao Li, Yao Zhao, Yaofeng Sun, Yaohui Li, Yaohui Wang, Yi Yu, Yi Zheng, Yichao Zhang,
Yifan Shi, Yiliang Xiong, Ying He, Ying Tang, Yishi Piao, Yisong Wang, Yixuan Tan, Yiyang Ma,
Yiyuan Liu, Yongqiang Guo, Yu Wu, Yuan Ou, Yuchen Zhu, Yuduan Wang, Yue Gong, Yuheng
Zou, Yujia He, Yukun Zha, Yunfan Xiong, Yunxian Ma, Yuting Yan, Yuxiang Luo, Yuxiang You,
Yuxuan Liu, Yuyang Zhou, Z. F. Wu, Z. Z. Ren, Zehui Ren, Zhangli Sha, Zhe Fu, Zhean Xu, Zhen
Huang, Zhen Zhang, Zhenda Xie, Zhengyan Zhang, Zhewen Hao, Zhibin Gou, Zhicheng Ma,
Zhigang Yan, Zhihong Shao, Zhipeng Xu, Zhiyu Wu, Zhongyu Zhang, Zhuoshu Li, Zihui Gu,
Zijia Zhu, Zijun Liu, Zilin Li, Ziwei Xie, Ziyang Song, Ziyi Gao, and Zizheng Pan. Deepseek-v3
technical report. _arXiv preprint_, December 2024b. doi: 10.48550/ARXIV.2412.19437.


Zhixu Du, Shiyu Li, Yuhao Wu, Xiangyu Jiang, Jingwei Sun, Qilin Zheng, Yongkai Wu, Ang
Li, Hai Helen Li, and Yiran Chen. Sida: Sparsity-inspired data-aware serving for efficient
and scalable large mixture-of-experts models. In P. Gibbons, G. Pekhimenko, and C. De Sa
(eds.), _Proceedings of Machine Learning and Systems_, volume 6, pp. 224–238, 2024. URL
[https://proceedings.mlsys.org/paper_files/paper/2024/file/698cfaf72a208aef2e](https://proceedings.mlsys.org/paper_files/paper/2024/file/698cfaf72a208aef2e78bcac55b74328-Paper-Conference.pdf)
[78bcac55b74328-Paper-Conference.pdf.](https://proceedings.mlsys.org/paper_files/paper/2024/file/698cfaf72a208aef2e78bcac55b74328-Paper-Conference.pdf)


Artyom Eliseev and Denis Mazur. Fast inference of mixture-of-experts language models with
offloading. _arXiv preprint_, December 2023. doi: 10.48550/ARXIV.2312.17238.


Zhiyuan Fang, Zicong Hong, Yuegui Huang, Yufeng Lyu, Wuhui Chen, Yue Yu, Fan Yu, and Zibin
Zheng. Accurate expert predictions in moe inference via cross-layer gate. _arXiv preprint_, February
2025. doi: 10.48550/ARXIV.2502.12224.


William Fedus, Barret Zoph, and Noam Shazeer. Switch transformers: Scaling to trillion parameter
models with simple and efficient sparsity. _Journal of Machine Learning Research_, 23(120):1–39,
[2022. URL http://jmlr.org/papers/v23/21-0998.html.](http://jmlr.org/papers/v23/21-0998.html)


Wenfeng Feng, Chuzhan Hao, Yuewei Zhang, Yu Han, and Hao Wang. Mixture-of-LoRAs: An
efficient multitask tuning method for large language models. In Nicoletta Calzolari, Min-Yen
Kan, Veronique Hoste, Alessandro Lenci, Sakriani Sakti, and Nianwen Xue (eds.), _Proceedings of_
_the 2024 Joint International Conference on Computational Linguistics, Language Resources and_
_Evaluation (LREC-COLING 2024)_, pp. 11371–11380, Torino, Italia, May 2024. ELRA and ICCL.
[URL https://aclanthology.org/2024.lrec-main.994/.](https://aclanthology.org/2024.lrec-main.994/)


Hongcan Guo, Haolang Lu, Guoshun Nan, Bolun Chu, Jialin Zhuang, Yuan Yang, Wenhao Che,
Sicong Leng, Qimei Cui, and Xudong Jiang. Advancing expert specialization for better moe. _arXiv_
_preprint_, May 2025. doi: 10.48550/ARXIV.2505.22323.


Xin He, Shunkang Zhang, Yuxin Wang, Haiyan Yin, Zihao Zeng, Shaohuai Shi, Zhenheng Tang,
Xiaowen Chu, Ivor Tsang, and Ong Yew Soon. Expertflow: Optimized expert activation and
token allocation for efficient mixture-of-experts inference. _arXiv preprint_, October 2024. doi:
10.48550/ARXIV.2410.17954.


Shengding Hu, Yuge Tu, Xu Han, Chaoqun He, Ganqu Cui, Xiang Long, Zhi Zheng, Yewei Fang,
Yuxiang Huang, Weilin Zhao, Xinrong Zhang, Zheng Leng Thai, Kaihuo Zhang, Chongyi Wang,
Yuan Yao, Chenyang Zhao, Jie Zhou, Jie Cai, Zhongwu Zhai, Ning Ding, Chao Jia, Guoyang Zeng,
Dahai Li, Zhiyuan Liu, and Maosong Sun. Minicpm: Unveiling the potential of small language
models with scalable training strategies. _arXiv preprint_, April 2024. doi: 10.48550/ARXIV.2404.
06395.


Haiyang Huang, Newsha Ardalani, Anna Sun, Liu Ke, Hsien-Hsin S. Lee, Anjali Sridhar, Shruti
Bhosale, Carole-Jean Wu, and Benjamin Lee. Towards moe deployment: Mitigating inefficiencies
in mixture-of-expert (moe) inference. _arXiv preprint_, March 2023. doi: 10.48550/ARXIV.2303.06
182.


12


Wei Huang, Yue Liao, Jianhui Liu, Ruifei He, Haoru Tan, Shiming Zhang, Hongsheng Li, Si Liu, and
Xiaojuan Qi. Mixture compressor for mixture-of-experts llms gains more. _arXiv preprint_, October
2024. doi: 10.48550/ARXIV.2410.06270.


Ranggi Hwang, Jianyu Wei, Shijie Cao, Changho Hwang, Xiaohu Tang, Ting Cao, and Mao Yang.
Pre-gated moe: An algorithm-system co-design for fast and scalable mixture-of-expert inference.
In _2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture (ISCA)_, pp.
1018–1031, June 2024. doi: 10.1109/ISCA59077.2024.00078.


Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris
Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand,
Gianna Lengyel, Guillaume Bour, Guillaume Lample, Lélio Renard Lavaud, Lucile Saulnier, MarieAnne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak, Teven Le
Scao, Théophile Gervet, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed.
Mixtral of experts. _arXiv preprint_, January 2024. doi: 10.48550/ARXIV.2401.04088.


Keisuke Kamahori, Yile Gu, Kan Zhu, and Baris Kasikci. Fiddler: CPU-GPU orchestration for fast
inference of mixture-of-experts models. In _5th Workshop on practical ML for limited/low resource_
_settings_ [, 2024. URL https://openreview.net/forum?id=WX7lxohjFe.](https://openreview.net/forum?id=WX7lxohjFe)


Rui Kong, Yuanchun Li, Qingtian Feng, Weijun Wang, Xiaozhou Ye, Ye Ouyang, Linghe Kong, and
Yunxin Liu. SwapMoE: Serving off-the-shelf MoE-based large language models with tunable
memory budget. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), _Proceedings of the_
_62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_,
pp. 6710–6720, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi:
[10.18653/v1/2024.acl-long.363. URL https://aclanthology.org/2024.acl-long.363/.](https://aclanthology.org/2024.acl-long.363/)


Barak Lenz, Opher Lieber, Alan Arazi, Amir Bergman, Avshalom Manevich, Barak Peleg, Ben
Aviram, Chen Almagor, Clara Fridman, Dan Padnos, Daniel Gissin, Daniel Jannai, Dor Muhlgay,
Dor Zimberg, Edden M. Gerber, Elad Dolev, Eran Krakovsky, Erez Safahi, Erez Schwartz, Gal
Cohen, Gal Shachaf, Haim Rozenblum, Hofit Bata, Ido Blass, Inbal Magar, Itay Dalmedigos,
Jhonathan Osin, Julie Fadlon, Maria Rozman, Matan Danos, Michael Gokhman, Mor Zusman,
Naama Gidron, Nir Ratner, Noam Gat, Noam Rozen, Oded Fried, Ohad Leshno, Omer Antverg,
Omri Abend, Or Dagan, Orit Cohavi, Raz Alon, Ro’i Belson, Roi Cohen, Rom Gilad, Roman
Glozman, Shahar Lev, Shai Shalev-Shwartz, Shaked Haim Meirom, Tal Delbari, Tal Ness, Tomer
Asida, Tom Ben Gal, Tom Braude, Uriya Pumerantz, Josh Cohen, Yonatan Belinkov, Yuval
Globerson, Yuval Peleg Levy, and Yoav Shoham. Jamba: Hybrid transformer-mamba language
models. In _The Thirteenth International Conference on Learning Representations_, 2025. URL
[https://openreview.net/forum?id=JFPaD7lpBD.](https://openreview.net/forum?id=JFPaD7lpBD)


Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu, Dehao Chen, Orhan Firat, Yanping Huang,
Maxim Krikun, Noam Shazeer, and Zhifeng Chen. GShard: Scaling giant models with conditional
computation and automatic sharding. In _International Conference on Learning Representations_,
[2021. URL https://openreview.net/forum?id=qrwe7XHTmYb.](https://openreview.net/forum?id=qrwe7XHTmYb)


Dengchun Li, Yingzi Ma, Naizheng Wang, Zhengmao Ye, Zhiyuan Cheng, Yinghao Tang, Yan Zhang,
Lei Duan, Jie Zuo, Cal Yang, and Mingjie Tang. Mixlora: Enhancing large language models
fine-tuning with lora-based mixture of experts. _arXiv preprint_, April 2024a. doi: 10.48550/ARX
IV.2404.15159.


Jiamin Li, Yimin Jiang, Yibo Zhu, Cong Wang, and Hong Xu. Accelerating distributed MoE training
and inference with lina. In _2023 USENIX Annual Technical Conference (USENIX ATC 23)_,
pp. 945–959, Boston, MA, July 2023. USENIX Association. ISBN 978-1-939133-35-9. URL
[https://www.usenix.org/conference/atc23/presentation/li-jiamin.](https://www.usenix.org/conference/atc23/presentation/li-jiamin)


Pingzhi Li, Zhenyu Zhang, Prateek Yadav, Yi-Lin Sung, Yu Cheng, Mohit Bansal, and Tianlong
Chen. Merge, then compress: Demystify efficient SMoe with hints from its routing policy.
In _The Twelfth International Conference on Learning Representations_, 2024b. URL [https:](https://openreview.net/forum?id=eFWG9Cy3WK)
[//openreview.net/forum?id=eFWG9Cy3WK.](https://openreview.net/forum?id=eFWG9Cy3WK)


Jiacheng Liu, Peng Tang, Wenfeng Wang, Yuhang Ren, Xiaofeng Hou, Pheng-Ann Heng, Minyi Guo,
and Chao Li. A survey on inference optimization techniques for mixture of experts models. _arXiv_
_preprint_, December 2024a. doi: 10.48550/ARXIV.2412.14219.


13


Liyuan Liu, Young Jin Kim, Shuohang Wang, Chen Liang, Yelong Shen, Hao Cheng, Xiaodong Liu,
Masahiro Tanaka, Xiaoxia Wu, Wenxiang Hu, Vishrav Chaudhary, Zeqi Lin, Chenruidong Zhang,
Jilong Xue, Hany Awadalla, Jianfeng Gao, and Weizhu Chen. Grin: Gradient-informed moe. _arXiv_
_preprint_, September 2024b. doi: 10.48550/ARXIV.2409.12136.


LMArena. arena-human-preference-140k, August 2025. URL [https://huggingface.co/dataset](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k)
[s/lmarena-ai/arena-human-preference-140k.](https://huggingface.co/datasets/lmarena-ai/arena-human-preference-140k)


Ka Man Lo, Zeyu Huang, Zihan Qiu, Zili Wang, and Jie Fu. A closer look into mixture-of-experts in
large language models. _arXiv preprint_, June 2024. doi: 10.48550/ARXIV.2406.18219.


Xudong Lu, Qi Liu, Yuhui Xu, Aojun Zhou, Siyuan Huang, Bo Zhang, Junchi Yan, and Hongsheng
Li. Not all experts are equal: Efficient expert pruning and skipping for mixture-of-experts large
language models. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), _Proceedings of the_
_62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_,
pp. 6159–6172, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi:
[10.18653/v1/2024.acl-long.334. URL https://aclanthology.org/2024.acl-long.334/.](https://aclanthology.org/2024.acl-long.334/)


Niklas Muennighoff, Luca Soldaini, Dirk Groeneveld, Kyle Lo, Jacob Morrison, Sewon Min, Weijia
Shi, Evan Pete Walsh, Oyvind Tafjord, Nathan Lambert, Yuling Gu, Shane Arora, Akshita Bhagia,
Dustin Schwenk, David Wadden, Alexander Wettig, Binyuan Hui, Tim Dettmers, Douwe Kiela,
Ali Farhadi, Noah A. Smith, Pang Wei Koh, Amanpreet Singh, and Hannaneh Hajishirzi. OLMoe:
Open mixture-of-experts language models. In _The Thirteenth International Conference on Learning_
_Representations_ [, 2025. URL https://openreview.net/forum?id=xXTkbTBmqq.](https://openreview.net/forum?id=xXTkbTBmqq)


Mohammed Muqeeth, Haokun Liu, and Colin Raffel. Soft merging of experts with adaptive routing.
_Transactions on Machine Learning Research_, 2024. ISSN 2835-8856. URL [https://openrevi](https://openreview.net/forum?id=7I199lc54z)
[ew.net/forum?id=7I199lc54z. Featured Certification.](https://openreview.net/forum?id=7I199lc54z)


NLLB Team, Marta R. Costa-jussà, James Cross, Onur Çelebi, Maha Elbayad, Kenneth Heafield,
Kevin Heffernan, Elahe Kalbassi, Janice Lam, Daniel Licht, Jean Maillard, Anna Sun, Skyler Wang,
Guillaume Wenzek, Al Youngblood, Bapi Akula, Loic Barrault, Gabriel Mejia Gonzalez, Prangthip
Hansanti, John Hoffman, Semarley Jarrett, Kaushik Ram Sadagopan, Dirk Rowe, Shannon Spruit,
Chau Tran, Pierre Andrews, Necip Fazil Ayan, Shruti Bhosale, Sergey Edunov, Angela Fan,
Cynthia Gao, Vedanuj Goswami, Francisco Guzmán, Philipp Koehn, Alexandre Mourachko,
Christophe Ropers, Safiyyah Saleem, Holger Schwenk, and Jeff Wang. No language left behind:
Scaling human-centered machine translation. _arXiv preprint_, July 2022. doi: 10.48550/ARXIV.2
207.04672.


NVIDIA Corporation. OpenScienceReasoning-2, June 2025. URL [https://huggingface.co/dat](https://huggingface.co/datasets/nvidia/OpenScienceReasoning-2)
[asets/nvidia/OpenScienceReasoning-2.](https://huggingface.co/datasets/nvidia/OpenScienceReasoning-2)


Quang Pham, Giang Do, Huy Nguyen, TrungTin Nguyen, Chenghao Liu, Mina Sartipi, Binh T.
Nguyen, Savitha Ramasamy, Xiaoli Li, Steven Hoi, and Nhat Ho. Competesmoe – effective
training of sparse mixture of experts via competition. _arXiv preprint_, February 2024. doi:
10.48550/ARXIV.2402.02526.


Xiaoye Qu, Daize Dong, Xuyang Hu, Tong Zhu, Weigao Sun, and Yu Cheng. Llama-moe v2:
Exploring sparsity of llama from perspective of mixture-of-experts with post-training. _arXiv_
_preprint_, November 2024. doi: 10.48550/ARXIV.2411.15708.


Qwen Team. Qwen1.5-moe: Matching 7b model performance with 1/3 activated parameters",
[February 2024. URL https://qwenlm.github.io/blog/qwen-moe/.](https://qwenlm.github.io/blog/qwen-moe/)


Samyam Rajbhandari, Conglong Li, Zhewei Yao, Minjia Zhang, Reza Yazdani Aminabadi, Ammar Ahmad Awan, Jeff Rasley, and Yuxiong He. DeepSpeed-MoE: Advancing mixture-ofexperts inference and training to power next-generation AI scale. In Kamalika Chaudhuri,
Stefanie Jegelka, Le Song, Csaba Szepesvari, Gang Niu, and Sivan Sabato (eds.), _Proceed-_
_ings of the 39th International Conference on Machine Learning_, volume 162 of _Proceed-_
_ings of Machine Learning Research_, pp. 18332–18346. PMLR, July 2022. URL [https:](https://proceedings.mlr.press/v162/rajbhandari22a.html)
[//proceedings.mlr.press/v162/rajbhandari22a.html.](https://proceedings.mlr.press/v162/rajbhandari22a.html)


14


Jie Ren, Dong Xu, Shuangyan Yang, Jiacheng Zhao, Zhicheng Li, Christian Navasca, Chenxi Wang,
Harry Xu, and Dong Li. Enabling large dynamic neural network training with learning-based
memory management. In _2024 IEEE International Symposium on High-Performance Computer_
_Architecture (HPCA)_, pp. 788–802, March 2024. doi: 10.1109/HPCA57654.2024.00066.


Noam Shazeer, *Azalia Mirhoseini, *Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton,
and Jeff Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer.
In _International Conference on Learning Representations_, 2017. URL [https://openreview.n](https://openreview.net/forum?id=B1ckMDqlg)
[et/forum?id=B1ckMDqlg.](https://openreview.net/forum?id=B1ckMDqlg)


Sheng Shen, Le Hou, Yanqi Zhou, Nan Du, Shayne Longpre, Jason Wei, Hyung Won Chung,
Barret Zoph, William Fedus, Xinyun Chen, Tu Vu, Yuexin Wu, Wuyang Chen, Albert Webson,
Yunxuan Li, Vincent Y. Zhao, Hongkun Yu, Kurt Keutzer, Trevor Darrell, and Denny Zhou.
Mixture-of-experts meets instruction tuning: A winning combination for large language models.
In _The Twelfth International Conference on Learning Representations_, 2024a. URL [https:](https://openreview.net/forum?id=6mLjDwYte5)
[//openreview.net/forum?id=6mLjDwYte5.](https://openreview.net/forum?id=6mLjDwYte5)


Yikang Shen, Zheyu Zhang, Tianyou Cao, Shawn Tan, Zhenfang Chen, and Chuang Gan. Moduleformer: Modularity emerges from mixture-of-experts. _arXiv preprint_, June 2023. doi:
10.48550/ARXIV.2306.04640.


Yikang Shen, Zhen Guo, Tianle Cai, and Zengyi Qin. Jetmoe: Reaching llama2 performance with
0.1m dollars. _arXiv preprint_, April 2024b. doi: 10.48550/ARXIV.2404.07413.


Yikang Shen, Matthew Stallone, Mayank Mishra, Gaoyuan Zhang, Shawn Tan, Aditya Prasad,
Adriana Meza Soria, David D. Cox, and Rameswar Panda. Power scheduler: A batch size and
token number agnostic learning rate scheduler. _arXiv preprint_, August 2024c. doi: 10.48550/ARX
IV.2408.13359.


Andrii Skliar, Ties van Rozendaal, Romain Lepert, Todor Boinovski, Mart van Baalen, Markus
Nagel, Paul Whatmough, and Babak Ehteshami Bejnordi. Mixture of cache-conditional experts
for efficient mobile device inference. _arXiv preprint_, November 2024. doi: 10.48550/ARXIV.241
2.00099.


Xiaoniu Song, Zihang Zhong, Rong Chen, and Haibo Chen. Promoe: Fast moe-based llm serving
using proactive caching. _arXiv preprint_, October 2024. doi: 10.48550/ARXIV.2410.22134.


Peng Tang, Jiacheng Liu, Xiaofeng Hou, Yifei Pu, Jing Wang, Pheng-Ann Heng, Chao Li, and Minyi
Guo. Hobbit: A mixed precision expert offloading system for fast moe inference. _arXiv preprint_,
November 2024. doi: 10.48550/ARXIV.2411.01433.


Together Computer. Redpajama: An open source recipe to reproduce llama training dataset, April
[2023. URL https://github.com/togethercomputer/RedPajama-Data.](https://github.com/togethercomputer/RedPajama-Data)


Shubham Toshniwal, Wei Du, Ivan Moshkov, Branislav Kisacanin, Alexan Ayrapetyan, and Igor
Gitman. Openmathinstruct-2: Accelerating AI for math with massive open-source instruction
data. In _The Thirteenth International Conference on Learning Representations_, 2025. URL
[https://openreview.net/forum?id=mTCbq2QssD.](https://openreview.net/forum?id=mTCbq2QssD)


Shaohua Wu, Jiangang Luo, Xi Chen, Lingjun Li, Xudong Zhao, Tong Yu, Chao Wang, Yue
Wang, Fei Wang, Weixu Qiao, Houbo He, Zeru Zhang, Zeyu Sun, Junxiong Mao, and Chong
Shen. Yuan 2.0-m32: Mixture of experts with attention router. _arXiv preprint_, May 2024. doi:
10.48550/ARXIV.2405.17976.


Fuzhao Xue, Zian Zheng, Yao Fu, Jinjie Ni, Zangwei Zheng, Wangchunshu Zhou, and Yang You.
Openmoe: An early effort on open mixture-of-experts language models. In _Forty-first International_
_Conference on Machine Learning_, 2024a. URL [https://openreview.net/forum?id=1YDeZU](https://openreview.net/forum?id=1YDeZU8Lt5)
[8Lt5.](https://openreview.net/forum?id=1YDeZU8Lt5)


Leyang Xue, Yao Fu, Zhan Lu, Luo Mai, and Mahesh Marina. Moe-infinity: Efficient moe inference
on personal machines with sparsity-aware expert cache. _arXiv preprint_, January 2024b. doi:
10.48550/ARXIV.2401.14361.


15


XVERSE Technology Inc. XVERSE-MoE-A4.2B, April 2024. URL [https://huggingface.co/x](https://huggingface.co/xverse/XVERSE-MoE-A4.2B)
[verse/XVERSE-MoE-A4.2B.](https://huggingface.co/xverse/XVERSE-MoE-A4.2B)


An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li,
Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang,
Jialin Wang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Ma, Jianxin Yang, Jin Xu, Jingren
Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming Lu, Keqin Chen, Kexin Yang,
Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize Gao, Runji Lin,
Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge, Xiaodong
Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu Zhang, Xipin Wei, Xuancheng Ren, Xuejing Liu,
Yang Fan, Yang Yao, Yichang Zhang, Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru
Zhang, Zhifang Guo, and Zhihao Fan. Qwen2 technical report. _arXiv preprint_, July 2024a. doi:
10.48550/ARXIV.2407.10671.


An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang
Gao, Chengen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan Zhou, Fei Huang, Feng Hu,
Hao Ge, Haoran Wei, Huan Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin
Yang, Jiaxi Yang, Jing Zhou, Jingren Zhou, Junyang Lin, Kai Dang, Keqin Bao, Kexin Yang,
Le Yu, Lianghao Deng, Mei Li, Mingfeng Xue, Mingze Li, Pei Zhang, Peng Wang, Qin Zhu, Rui
Men, Ruize Gao, Shixuan Liu, Shuang Luo, Tianhao Li, Tianyi Tang, Wenbiao Yin, Xingzhang
Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yinger
Zhang, Yu Wan, Yuqiong Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou, and Zihan
Qiu. Qwen3 technical report. _arXiv preprint_, May 2025. doi: 10.48550/ARXIV.2505.09388.


Cheng Yang, Yang Sui, Jinqi Xiao, Lingyi Huang, Yu Gong, Yuanlin Duan, Wenqi Jia, Miao Yin,
Yu Cheng, and Bo Yuan. MoE-i [2] : Compressing mixture of experts models through inter-expert
pruning and intra-expert low-rank decomposition. In Yaser Al-Onaizan, Mohit Bansal, and YunNung Chen (eds.), _Findings of the Association for Computational Linguistics: EMNLP 2024_, pp.
10456–10466, Miami, Florida, USA, November 2024b. Association for Computational Linguistics.
doi: 10.18653/v1/2024.findings-emnlp.612. URL [https://aclanthology.org/2024.findin](https://aclanthology.org/2024.findings-emnlp.612/)
[gs-emnlp.612/.](https://aclanthology.org/2024.findings-emnlp.612/)


Rongjie Yi, Liwei Guo, Shiyun Wei, Ao Zhou, Shangguang Wang, and Mengwei Xu. Edgemoe:
Empowering sparse large language models on mobile devices. _IEEE Transactions on Mobile_
_Computing_, pp. 1–16, 2025. ISSN 1558-0660. doi: 10.1109/TMC.2025.3546466.


Hanfei Yu, Xingqi Cui, Hong Zhang, Hao Wang, and Hao Wang. fmoe: Fine-grained expert offloading
for large mixture-of-experts serving. _arXiv preprint_, February 2025. doi: 10.48550/ARXIV.2502.
05370.


Xiaofeng Zhang, Yikang Shen, Zeyu Huang, Jie Zhou, Wenge Rong, and Zhang Xiong. Mixture of
attention heads: Selecting attention heads per token. In Yoav Goldberg, Zornitsa Kozareva, and
Yue Zhang (eds.), _Proceedings of the 2022 Conference on Empirical Methods in Natural Language_
_Processing_, pp. 4150–4162, Abu Dhabi, United Arab Emirates, December 2022. Association for
Computational Linguistics. doi: 10.18653/v1/2022.emnlp-main.278. URL [https://aclantholo](https://aclanthology.org/2022.emnlp-main.278/)
[gy.org/2022.emnlp-main.278/.](https://aclanthology.org/2022.emnlp-main.278/)


Yujie Zhang, Shivam Aggarwal, and Tulika Mitra. Daop: Data-aware offloading and predictive
pre-calculation for efficient moe inference. _arXiv preprint_, January 2025. doi: 10.48550/ARXIV.2
501.10375.


Shuzhang Zhong, Ling Liang, Yuan Wang, Runsheng Wang, Ru Huang, and Meng Li. Adapmoe:
Adaptive sensitivity-based expert gating and management for efficient moe inference. In _Proceed-_
_ings of the 43rd IEEE/ACM International Conference on Computer-Aided Design_, ICCAD ’24,
New York, NY, USA, 2025. Association for Computing Machinery. ISBN 9798400710773. doi:
[10.1145/3676536.3676741. URL https://doi.org/10.1145/3676536.3676741.](https://doi.org/10.1145/3676536.3676741)


Zexuan Zhong, Mengzhou Xia, Danqi Chen, and Mike Lewis. Lory: Fully differentiable mixture-ofexperts for autoregressive language model pre-training. In _First Conference on Language Modeling_,
[2024. URL https://openreview.net/forum?id=LKEJPySnlt.](https://openreview.net/forum?id=LKEJPySnlt)


16


Yanqi Zhou, Tao Lei, Hanxiao Liu, Nan Du, Yanping Huang, Vincent Zhao, Andrew M. Dai,
zhifeng Chen, Quoc V. Le, and James Laudon. Mixture-of-experts with expert choice routing. In
S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh (eds.), _Advances in Neural_
_Information Processing Systems_, volume 35, pp. 7103–7114. Curran Associates, Inc., 2022. URL
[https://proceedings.neurips.cc/paper_files/paper/2022/file/2f00ecd787b432c1d](https://proceedings.neurips.cc/paper_files/paper/2022/file/2f00ecd787b432c1d36f3de9800728eb-Paper-Conference.pdf)
[36f3de9800728eb-Paper-Conference.pdf.](https://proceedings.neurips.cc/paper_files/paper/2022/file/2f00ecd787b432c1d36f3de9800728eb-Paper-Conference.pdf)


Tong Zhu, Xiaoye Qu, Daize Dong, Jiacheng Ruan, Jingqi Tong, Conghui He, and Yu Cheng. LLaMAMoE: Building mixture-of-experts from LLaMA with continual pre-training. In Yaser Al-Onaizan,
Mohit Bansal, and Yun-Nung Chen (eds.), _Proceedings of the 2024 Conference on Empirical_
_Methods in Natural Language Processing_, pp. 15913–15923, Miami, Florida, USA, November
2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.emnlp-main.890. URL
[https://aclanthology.org/2024.emnlp-main.890/.](https://aclanthology.org/2024.emnlp-main.890/)


**A** **Use of LLMs**


We primarily employ LLMs to polish the writing of this paper, utilizing tools such as Grammarly and
Writeful. In all other cases, LLMs are the object of our experiments and analyses, and we do not use
them for other purposes.


**B** **Related work**


**B.1** **MoE-based LLM and expert analysis**


Since its introduction into large neural networks, MoE has become a critical strategy to build large
language models up to trillions of parameters (Shazeer et al., 2017; Fedus et al., 2022; Rajbhandari
et al., 2022). While some early models like SwitchTransformers (Fedus et al., 2022) and NLLB
(NLLB Team et al., 2022) employ encoder-decoder structures as their backbone, due to the success
of GPT-3, the most recent popular MoE-based LLMs use decoder-only structures (Jiang et al., 2024;
Yang et al., 2024a; DeepSeek-AI et al., 2024b; Abdin et al., 2024), replacing their original FFN
layers with MoE layers containing multiple experts (other components may be replaced too, e.g.,
self-attention (Shen et al., 2023, 2024b) and LoRA (Li et al., 2024a; Feng et al., 2024)). Cai et al.
(2024) systematically introduces MoE architectures and implementation in LLMs.


The popularity of MoE LLMs has triggered interest in understanding how experts are activated in
such models. Many model reports and individual studies focused on the relation between expert
selection and the input context. For example, Muennighoff et al. (2025) reported that OLMoE shows
a significant difference in expert activity across different domains. Contrastively, Xue et al. (2024a)
found that the routing choice of OpenMoE is highly related to the input token rather than the input
context. Other works investigated the similarity among expert activation patterns (Li et al., 2024b; Lu
et al., 2024), as well as the relation between expert output and routing choice (Pham et al., 2024; Lo
et al., 2024). Some further proposed methods to reinforce such patterns (Guo et al., 2025; Chen et al.,
2025). However, few of them have focused on the local activation pattern of experts. For example,
Jiang et al. (2024) reported that in Mixtral, experts are more likely to be activated consecutively,
compared to the random case. While their results provide fundamental support for many efficient
MoE inference systems Liu et al. (2024a), they only examined the case of 2 consecutive tokens,
which may be insufficient to ensure the consistency of expert activation in longer segments.


**B.2** **Efficient MoE inference and expert offloading**


The discrete nature of routers and redundant parameters has caused MoE models to infer more
slowly and consume more memory than dense models with the same number of activated parameters.
Many techniques have been proposed to boost the inference of MoE models, ranging from model
modifications like model compression (Chen et al., 2022; Huang et al., 2024; Yang et al., 2024b;
Rajbhandari et al., 2022) and soft routing (Muqeeth et al., 2024; Zhong et al., 2024) to system
implementations like load-balanced expert parallel (Lepikhin et al., 2021; Huang et al., 2023; Li
et al., 2023) and hardware adaptation (DeepSeek-AI et al., 2024b; Yi et al., 2025). Liu et al. (2024a)
provides an in-depth summary of various inference optimization strategies of MoE models.


17


In this paper, we mainly focus on the potential performance of expert offloading, which enables
lossless inference of MoE models on memory-constrained devices by caching only some experts
on (fast) memory while leaving others on slow memory or disk storage. Many such systems use
pretrained external models and/or information from previous layers to prefetch experts for upcoming
layers (Ren et al., 2024; Du et al., 2024; He et al., 2024; Song et al., 2024). Various expert offloading
systems propose curated heuristics to manage the expert cache (Skliar et al., 2024; Xue et al., 2024b;
Yu et al., 2025; Fang et al., 2025). Among them, some examine the locality of expert activations as
empirical support for expert caching efficiency:


 - Jiang et al. (2024) first observed that Mixtral-8x7B is likely to choose the same expert for the next
token, with probabilities higher than the random expectation. Eliseev & Mazur (2023) extended the
argument to 2-4 consecutive tokens through a case study, and boosted inference performance of the
same model with LRU caching (plus other techniques such as prefetching and quantization). These
works align with our settings, but their analyses are limited to a single model (Mixtral-8x7B),
short token spans, and lack a systematic and quantitative study.

 - Xue et al. (2024b) reported frequent expert reuse during decoding, and observed that the reused
experts depend on the prefilled input. Zhang et al. (2025) found similar routing choices between
prefilling and decoding stages. Both observations are utilized to back the effectiveness of expert
caching, yet are too coarse in terms of locality (at the input level instead of the token span level).


As more MoE LLMs emerge, understanding what models are more friendly to expert offloading
becomes important for the development of both MoE architectures and expert offloading methods.


**C** **Proofs**


**C.1** **Proof of equation 3**


In Section 2.2, we consider each routing decision of _R_ _e_ _[m]_ [for a segment of length] _[ m]_ [ as a binary]
classification task with _m_ samples. If we merge all samples from all segments of all possible inputs
into one global binary classification task, and define _f_ ( _e, T, p, m_ ) = [�] _[p]_ _i_ = [+] _p_ _[m][−]_ [1] _A_ ( _e, T_ )[ _i_ ] as in
Section 2.2, we will have the following prediction statistics:



TP(R [m] e [) =] �


_T_


=
�


_T_


FP(R [m] e [) =] �


_T_


=
�


_T_


FN(R [m] e [) =] �


_T_


=
�


_T_



_|T |−m_ +1
�

_p_ =1



_|T |−m_ +1
� [1 _−_ _R_ _e_ _[m]_ [(] _[T, p]_ [)]] _[f]_ [(] _[e, T, p, m]_ [)] (12)

_p_ =1


18



_m_
� _I_ [ _A_ ( _e, T_ )[ _p_ + _i −_ 1] = 1 _∧_ _R_ _e_ _[m]_ [(] _[T, p]_ [)[] _[i]_ [] = 1]]


_i_ =1



_|T |−m_ +1
� _R_ _e_ _[m]_ [(] _[T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)] (10)

_p_ =1



_|T |−m_ +1
�

_p_ =1



_m_
� _I_ [ _A_ ( _e, T_ )[ _p_ + _i −_ 1] = 0 _∧_ _R_ _e_ _[m]_ [(] _[T, p]_ [)[] _[i]_ [] = 1]]


_i_ =1



_|T |−m_ +1
� _R_ _e_ _[m]_ [(] _[T, p]_ [)[] _[m][ −]_ _[f]_ [(] _[e, T, p, m]_ [)]] (11)

_p_ =1



_|T |−m_ +1
�

_p_ =1



_m_
� _I_ [ _A_ ( _e, T_ )[ _p_ + _i −_ 1] = 1 _∧_ _R_ _e_ _[m]_ [(] _[T, p]_ [)[] _[i]_ [] = 0]]


_i_ =1


Therefore we have


1
_F_ 1 ( _R_ _e_ _[m]_ [) =] 1 _/_ Precision( _R_ _e_ _[m]_ [) + 1] _[/]_ [Recall(] _[R]_ _e_ _[m]_ [)]


1

=

[ _TP_ ( _R_ _e_ _[m]_ [) +] _[ FP]_ [(] _[R]_ _e_ _[m]_ [)]] _[/TP]_ [(] _[R]_ _e_ _[m]_ [) + [] _[TP]_ [(] _[R]_ _e_ _[m]_ [) +] _[ FN]_ [(] _[R]_ _e_ _[m]_ [)]] _[/TP]_ [(] _[R]_ _e_ _[m]_ [)]

= 2 _TP_ ( _R_ _e_ _[m]_ [)]

[ _TP_ ( _R_ _e_ _[m]_ [) +] _[ FP]_ [(] _[R]_ _e_ _[m]_ [)] + [] _[TP]_ [(] _[R]_ _e_ _[m]_ [) +] _[ FN]_ [(] _[R]_ _e_ _[m]_ [)]]


_̸_


_̸_


_̸_ _̸_



(13)


(14)


_̸_


_̸_


_̸_ _̸_



_|T |−m_ +1

2 [�] _T_ � _p_ =1 _R_ _e_ _[m]_ [(] _[T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)]


_|T |−m_ +1 _|T |−m_ +1

~~��~~ _T_ ~~�~~ _p_ =1 _m · R_ _e_ _[m]_ [(] _[T, p]_ [)] ~~�~~ + ~~��~~ _T_ ~~�~~ _p_ =1 _f_


_̸_


_̸_


_̸_ _̸_



2 [�]

=


_̸_


_̸_


_̸_ _̸_



_|T |−m_ +1
_T_ ~~�~~ _p_ =1 _f_ ( _e, T, p, m_ ) ~~�~~


_̸_


_̸_


_̸_ _̸_



_|T |−m_ +1
_T_ ~~�~~ _p_ =1 _m · R_ _e_ _[m]_ [(] _[T, p]_ [)] ~~�~~ + ~~��~~


_̸_


_̸_


_̸_ _̸_



_|T |−m_ +1

2 [�] _T_ � _p_ =1 _R_ _e_ _[m]_ [(] _[T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)]

_|T |−m_ +1

~~�~~ _T_ ~~�~~ =1 [ _m · R_ _e_ _[m]_ [(] _[T, p]_ [) +] _[ f]_ [(] _[e, T, p, m]_


_̸_


_̸_


_̸_ _̸_



2 [�]

=


_̸_


_̸_


_̸_ _̸_



_|T |−m_ +1
_T_ ~~�~~ _p_ =1 [ _m · R_ _e_ _[m]_ [(] _[T, p]_ [) +] _[ f]_ [(] _[e, T, p, m]_ [)]]


_̸_


_̸_


_̸_ _̸_



which gives Equation 3. _2_


**C.2** **Proof of equation 4**


Assume that _R_ _e_ _[m]_ [(] _[T]_ [0] _[, p]_ [0] [) = 0][ for some] _[ e]_ [,] _[ m >]_ [ 0][,] _[ R]_ _e_ _[m]_ [,] _[ T]_ [0] [and] _[ p]_ [0] [, then we have]


_̸_


_̸_


_̸_ _̸_



_|T |−m_ +1

2 [�] _T_ � _p_ =1 _R_ _e_ _[m]_ [(] _[T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)]

_|T |−m_ +1

~~�~~ _T_ ~~�~~ =1 [ _m · R_ _e_ _[m]_ [(] _[T, p]_ [) +] _[ f]_ [(] _[e, T, p, m]_


_̸_


_̸_


_̸_ _̸_



2 [�]
_F_ 1 ( _R_ _e_ _[m]_ [) =]


_̸_


_̸_


_̸_ _̸_



_|T |−m_ +1
_T_ ~~�~~ _p_ =1 [ _m · R_ _e_ _[m]_ [(] _[T, p]_ [) +] _[ f]_ [(] _[e, T, p, m]_ [)]]


_̸_


_̸_


_̸_ _̸_



_|T |−m_ +1

= 2 [�] _T_ � _p_ =1 _R_ _e_ _[m]_ [(] _[T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)]


_̸_


_̸_


_̸_ _̸_



_T_ ~~�~~ _|pT_ =1 _|−m_ +1 _R_ _e_ _[m]_ [(] _[T, p]_ [) +] ~~[�]~~


_̸_


_̸_


_̸_ _̸_



_m_ ~~[�]~~


_̸_


_̸_


_̸_ _̸_



_|T |−m_ +1
_T_ ~~�~~ _p_ =1 _f_ ( _e, T, p, m_ )


_̸_


_̸_


_̸_ _̸_



= 2 [�] _T ̸_ = _T_ 0 _∧p_ = _̸_ _p_ 0 _[R]_ _e_ _[m]_ [(] _[T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)]


_̸_


_̸_ _̸_



_̸_

_m_ ~~[�]~~ _T ̸_ = _T_ 0 _∧p_ = _̸_ _p_ 0 _[R]_ _e_ _[m]_ [(] _[T, p]_ [) +] ~~[�]~~ _T_ ~~�~~ _|pT_ =1 _|−m_ +1 _f_ ( _e, T, p, m_ )


_̸_ _̸_



_̸_


_̸_


where


_X_ =
�

_T ̸_ = _T_ 0

_p_ = _̸_ _p_ 0 _̸_



_̸_


_̸_


2 _X_

=
_mY_ + _Z_


_R_ _e_ _[m]_ [(] _[T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)] _[,]_ _Y_ = �

_T ̸_ = _T_ 0


_̸_ _p_ = _̸_ _p_ 0



_̸_


_̸_


_R_ _e_ _[m]_ [(] _[T, p]_ [)] _[,]_ _Z_ = �


_T_

_̸_ _̸_



_̸_


_̸_


_|T |−m_ +1
� _f_ ( _e, T, p, m_ )

_p_ =1

_̸_ _̸_



_̸_


_̸_


_̸_ _̸_


Let _R_ [�] _e_ _[m]_ [be a copy of] _[ R]_ _e_ _[m]_ [except that] _[ R]_ _e_ _[m]_ [(] _[T, p]_ [) = 1] [; all other routing decisions remain the same.]
Then the _F_ 1 score of the new segment router will be

_F_ 1 � _R_ � _e_ _[m]_ � = 2 [�] _|TT |−_ � _m|pT_ =1+1 _|−m_ +1 _R_ � _e_ _[m]_ [(] _[T, p]_ [)] _[ ·][ f]_ [(] _[e, T, p, m]_ [)]

~~�~~ _T_ ~~�~~ _p_ =1 ~~�~~ _m ·_ _R_ [�] _e_ _[m]_ [(] _[T, p]_ [) +] _[ f]_ [(] _[e, T, p, m]_ [)] ~~�~~



_̸_


_̸_


_̸_ _̸_


_[f]_ [(] _[e][,][ T]_ [0] _[,]_ _[p]_ [0] _[,][ m]_ [)]]
= [2][[] _[X]_ [ +]

_m_ ( _Y_ + 1) + _Z_

= [(] _[mY]_ [ +] _[ Z]_ [)] _[ ·][ F]_ [1] [(] _[R]_ _e_ _[m]_ [)][ + 2] _[f]_ [(] _[e][,][ T]_ [0] _[,]_ _[p]_ [0] _[,][ m]_ [)]
_m_ ( _Y_ + 1) + _Z_

= [(] _[mY]_ [ +] _[ Z]_ [)] _[ ·][ F]_ [1] [(] _[R]_ _e_ _[m]_ [)][ +] _[ m][ ·]_ [[][2] _[f]_ [(] _[e][,][ T]_ [0] _[,]_ _[p]_ [0] _[,][ m]_ [)] _[/][m]_ []]
( _mY_ + _Z_ ) + _m_



_̸_


_̸_


_̸_ _̸_


(15)



_̸_


_̸_


_̸_ _̸_


which is a weighted mean of _F_ 1 ( _R_ _e_ _[m]_ [)] [ and] [ 2] _[f]_ [(] _[e, T]_ [0] _[, p]_ [0] _[, m]_ [)] _[/m]_ [ with weights] _[ mY]_ [ +] _[ Z]_ [ and] _[ m]_ [. Note]

_|T |−m_ +1

that _Z_ = [�] _T_ � _p_ =1 _f_ ( _e, T, p, m_ ) _≥_ 0, and _Z_ = 0 if and only if _f_ ( _e, T, p, m_ ) = 0 for all _T_

and _p_ . If _Z_ = 0, then _e_ is inactive everywhere and _F_ 1 ( _R_ _e_ _[m]_ [) = 0] [ for any] _[ R]_ _e_ _[m]_ -, thus SRP( _e, m_ ) = 0


  - If _Y_ = _R_ _em_ [(] _[T, p]_ [) = 0][ for all] _[ T]_ [ and] _[ p]_ [, then] _[ F]_ 1 [(] _[R]_ _e_ _[m]_ [)][ is undefined, which we do not concern.]


19


and we can simply let _α_ _e_ _[m]_ [= 0] [. Therefore, we assume that] _[ Z >]_ [ 0] [, then both] _[ m]_ [ and] _[ mY]_ [ +] _[ Z]_ [ are]

�
positive. Hence, _F_ 1 _R_ _e_ _[m]_ _≥_ _F_ 1 ( _R_ _e_ _[m]_ [)] [ if and only if] [ 2] _[f]_ [(] _[e, T]_ [0] _[, p]_ [0] _[, m]_ [)] _[/m][ ≥]_ _[F]_ [1] [(] _[R]_ _e_ _[m]_ [)] [. Equality is]
� �
achieved when and only when all equalities hold.


The above result indicates that, in order to increase _F_ 1 ( _R_ _e_ _[m]_ [)] [, for any segment satisfying] _[ R]_ _e_ _[m]_ [(] _[T, p]_ [) = 0]
and _f_ ( _e, T, p, m_ ) _≥_ ( _m/_ 2) _· F_ 1 ( _R_ _e_ _[m]_ [)] [, we should change the routing decision to] _[ R]_ _e_ _[m]_ [(] _[T, p]_ [) = 1] [§] [, and]
for any segment satisfying _R_ _e_ _[m]_ [(] _[T, p]_ [) = 1] [ and] _[ f]_ [(] _[e, T, p, m]_ [)] _[ <]_ [ (] _[m/]_ [2)] _[ ·][ F]_ [1] [(] _[R]_ _e_ _[m]_ [)] [, we should change]
the routing decision to _R_ _e_ _[m]_ [(] _[T, p]_ [) = 0] [. Under the case where the number of possible inputs is finite]
(which is the case for most LLMs due to their limited context windows), this will eventually result in
a _R_ [�] _e_ _[m]_ [that activates and only activates all segments with] _[ f]_ [(] _[e, T, p, m]_ [)] _[ ≥]_ [(] _[m/]_ [2)] _[·]_ _[F]_ [1] _R_ � _e_ _[m]_, whose _F_ 1
� �

cannot increase further. Such _R_ [�] _e_ _[m]_ [must be unique and maximizing] _[ F]_ [1] [(] _[R]_ _e_ _[m]_ [)] [: Otherwise, if there exists]
another _R_ [�] _e_ _[m]_ _′_ with _F_ 1 _R_ � _e_ _[m]_ _′_ [�] _> F_ 1 _R_ � _e_ _[m]_, then the only segments where _R_ [�] _e_ _[m]_ [and] [ �] _R_ _e_ _[m]_ _′_ disagree are
� � �

� � _′_ [�]
the ones satisfying ( _m/_ 2) _· F_ 1 _R_ _e_ _[m]_ _≤_ _f_ ( _e, T, p, m_ ) _<_ ( _m/_ 2) _· F_ 1 _R_ _e_ _[m]_, where _R_ [�] _e_ _[m]_ [(] _[T, p]_ [) = 1]
� � �

and _R_ [�] _e_ _[m]_ _′_ ( _T, p_ ) = 0 ; however, changing � _R_ _e_ _[m]_ [on these segments to] [ 0] [ should not increase] _[ F]_ [1] _R_ � _e_ _[m]_,
� �

� _′_ [�] � �
thus _F_ 1 _R_ _e_ _[m]_ _≤_ _F_ 1 _R_ _e_ _[m]_, a contradiction. Therefore, we can let _α_ _e,m_ = _F_ 1 _R_ _e_ _[m]_, which
� � � � � ��
yields Equation 4. _2_


**D** **Experiment setup details**


**D.1** **Model architecture list**


Table 4 lists the detailed architecture and configuration of all models where we conduct our experi
ments.


Table 4: Model architecture and configuration, sorted by model size. Experts: T: total; A: active; S:
shared (not included in total).


# Params (B) # Experts
Model # Layers MoE Layer

Total Active T A S


PowerMoE-3B (Shen et al., 2024c) 3.30 0.88 32 all 40 8 0
LLaMA-MoE-v1-3.5B (Zhu et al., 2024) 6.74 3.50 32 all 16 4 0
OLMoE-1B-7B-0125 6.92 1.28 16 all 64 8 0
(Muennighoff et al., 2025)

SwitchTransformers-Base-128 7.42 0.22 24 every 2 128 1 0
(Fedus et al., 2022)

LLaMA-MoE-v2-3.8B (Qu et al., 2024) 8.03 3.80 32 all 8 2 0
JetMoE-8B (Shen et al., 2024b) 8.52 2.33 24 all 8 2 0
OpenMoE-8B (Xue et al., 2024a) 11.86 3.80 24 every 6 32 2 1
MiniCPM-MoE-8x2B (Hu et al., 2024) 13.87 4.32 40 all 8 2 0
Qwen1.5-MoE-A2.7B (Qwen Team, 2024) 14.32 2.69 24 all 60 4 4
DeepSeek-V2-Lite 15.71 2.66 27 after 1st 64 6 2
(DeepSeek-AI et al., 2024a)

DeepSeekMoE (Dai et al., 2024) 16.38 2.83 28 after 1st 64 6 2
XVERSE-MoE-A4.2B 25.78 4.23 28 all 64 6 2
(XVERSE Technology Inc., 2024)

Qwen3-30B-A3B (Yang et al., 2025) 30.53 3.35 48 all 128 8 0
Yuan2.0-M32 (Wu et al., 2024) 39.94 3.70 24 all 32 2 0
Phi-3.5-MoE (Abdin et al., 2024) 41.87 6.64 32 all 16 2 0
GRIN-MoE (Liu et al., 2024b) 41.87 6.64 32 all 16 2 0
Mixtral-8x7B-v0.1 (Jiang et al., 2024) 46.70 12.88 32 all 8 2 0
Jamba-Mini-1.6 (Lenz et al., 2025) 51.57 12.11 32 every 2 16 2 0
NLLB-MoE-54B (NLLB Team et al., 2022) 54.50 3.75 48 every 4 128 2 0
Qwen2-57B-A14B (Yang et al., 2024a) 57.41 14.25 28 all 64 8 8


§ When _f_ ( _e, T, p, m_ ) = ( _m/_ 2) _· F_ 1 ( _R_ _em_ [)][, changing] _[ R]_ _e_ _[m]_ [(] _[T, p]_ [)][ does not affect] _[ F]_ 1 [(] _[R]_ _e_ _[m]_ [)][.]


20


A few notes:


 - SwitchTransformers-Base-128 and NLLB-MoE-54B are encoder-decoder models that use the
T5 architecture. SwitchTransformers-Base-128 has 12 encoder layers and 12 decoder layers.
NLLB-MoE-54B has 24 encoder layers and 24 decoder layers.

 - JetMoE-8B employs mixture-of-attention(Shen et al., 2024a), which we keep intact in our experi
ments.

 - GRIN-MoE shares the same architecture with Phi-3.5-MoE, but is trained using different methods.

 - Jamba-Mini-1.6 employs a hybrid SSM-Transformer structure, yet the MoE part is identical to
vanilla transformer-based MoE models.


**D.2** **Data processing and input generation**


We first extract samples from RedPajama and downstream application datasets in plain text format.
For RedPajama, this is already done. For LMArena, each of the original instances consists of
two human-LLM conversations and a preference vote. We keep the instances where one of the
conversations is preferred and concatenate all rounds from the preferred conversation (each round
with its role and content) into one document. For OpenMath, OpenCode, and OpenScience, we
simply concatenate the input and output of each instance.


After collecting samples from each RedPajama category and the downstream application dataset, we
concatenate the samples within the domain, cutting them into input sequences of 512 tokens (the
context window size of SwitchTransformers). We sample 2,048 input sequences for each domain,
resulting in 22,528 input samples in total.


For SwitchTransformers, since the model is trained for masked language modeling, we randomly
select 64 tokens from each input sequence, masking them in the original sequence as the encoder
input and constructing the corresponding label sequence as the decoder input. For NLLB-MoE, as the
model is trained for machine translation, we use the same sequence (with the English language token
prepended) as both the encoder input and the decoder input. All other models do not need further
data preprocessing, as they are decoder-only and trained for next token prediction.


**E** **Additional results**


**E.1** **Base vs. post-trained**


We selected three models—LLaMA-MoE-v1, OLMoE, and JetMoE—that have both base and posttrained versions released, and calculated SRP( _E, m_ ) and _ρ_ ( _E, m_ ) of each version. Table 5 lists
the results, from which we can see that the differences of both SRP( _E, m_ ) and _ρ_ ( _E, m_ ) between
models before and after post-training are not significant enough to change the degree of local routing
consistency, regardless of what type of post-training (SFT, DPO, etc.) is applied. Another related
fact is that Phi-MoE-3.5 and GRIN-MoE, which share the same model architecture but are trained
differently, have similar local routing consistency. Both indicate that the training method may be less
important than the model architecture concerning local routing consistency.


Table 5: SRP( _E, m_ ) between models before and after post-training.


_m_ = 4 _m_ = 16 _m_ = 64 _m_ = 256
Model

SRP _ρ_ ( _E, m_ ) SRP _ρ_ ( _E, m_ ) SRP _ρ_ ( _E, m_ ) SRP _ρ_ ( _E, m_ )


LLaMA-MoE-v1 55.78 1.03 45.29 2.39 41.61 2.92 40.62 3.52

+SFT +0.01 -0.00 -0.01 -0.00 -0.01 +0.00 -0.00 -0.00


OLMoE 64.69 1.00 50.91 1.06 45.53 1.21 42.64 1.19

+SFT +0.40 +0.00 +0.47 +0.01 +0.50 +0.02 +0.60 -0.02

+DPO +0.37 +0.00 +0.43 +0.01 +0.47 +0.02 +0.57 -0.02

+Instruct +0.45 +0.00 +0.56 +0.01 +0.62 +0.02 +0.74 -0.02


JetMoE 60.22 1.09 47.45 2.26 42.78 2.69 41.09 3.15

+SFT -0.20 -0.00 -0.14 +0.01 -0.12 +0.02 -0.09 +0.03

+Chat -0.20 -0.00 -0.15 +0.01 -0.13 +0.02 -0.10 +0.03


21


**E.2** **SRP and corpus perplexity**


Figure 6 compares each model’s segment routing best performance with its mean log perplexity on
_S_ . Most models have corpus perplexity close to each other, and we do not find a significant relation
between SRP and corpus perplexity.


4


3.5


OP OP OP OP



3


2.5


2


1.5



~~LL2~~ ~~LL2~~ ~~LL2~~ ~~LL2~~


JB JB JB JB





LL1 OL PWQW3 JT OL PWQW3 LL1 OL QW3PW LL1 OL



~~MC~~ ~~Y2~~ QW1 LL1 ~~MC~~ ~~Y2~~ QW1 ~~MC~~ ~~Y2~~ QW1 ~~MC~~



QW3 ~~Y2~~ QW1 LL1 ~~MC~~ QW3 ~~Y2~~ QW1 LL1 ~~MC~~ QW3 ~~Y2~~ QW1 LL1 ~~MC~~ QW3 ~~Y2~~









~~GR~~ PH ~~GR~~ PH ~~GR~~ PH ~~GR~~ PH







PWQW3 JT OL PWQW3 LL1 OL QW3PW LL1 OL QW3PW



DS1 DS1 DS1













XV MX XV MX XV MX XV MX


|Col1|OOOOOPPPPP|Col3|Col4|Col5|
|---|---|---|---|---|
||||||
||||~~LL2~~<br>~~LL2~~<br><br>||
||||~~LL2~~<br><br><br>~~LL2~~<br>~~LL2~~|~~LL2~~<br><br><br>~~LL2~~<br>~~LL2~~|
||JB<br>JB<br>JB<br>JB<br>JB<br>QW1<br>QW1<br>QW1<br>QW1<br>QW1<br>LL1<br>LL1<br>LL1<br>LL1<br>LL1|QW3<br>QW3<br>QW3<br>QW3<br>QW3<br>~~MC~~<br>~~MC~~<br>~~MC~~<br>~~MC~~<br>~~MC~~<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>|~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~|~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~|
||QW2<br>~~QW2~~<br>~~QW2~~<br>QW2<br>QW2<br>~~G~~<br>~~G~~<br>~~G~~<br>~~G~~<br>~~G~~<br><br><br><br><br><br>DS1<br>DS1<br>DS1<br>DS1<br>DS1<br>DS2<br>DS2<br>DS2<br>DS2<br>DS2<br>JJ<br>JJ<br>J<br><br><br>|MX<br>MX<br>MX<br>MX<br>MX<br>~~R~~<br>~~R~~<br>~~R~~<br>~~R~~<br>~~R~~<br>~~PH~~<br>PH<br>PH<br>~~PH~~<br>PH<br>TT<br>TT<br>T<br>OL<br>OL<br>OL<br>OL<br>OL<br><br><br><br>PW<br>PW<br>PW<br>PW<br>PW|||


|OOOOOPPPPP|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|O<br>O<br>O<br>O<br>O|||||
||||~~LL2~~<br>~~LL2~~<br><br>||
||||~~LL2~~<br><br><br>~~LL2~~<br>~~LL2~~|~~LL2~~<br><br><br>~~LL2~~<br>~~LL2~~|
||JB<br>JB<br>JB<br>JB<br>JB<br>1<br>1<br>1<br>1<br>1<br><br><br><br><br><br>LL1<br>LL1<br>LL1<br>LL1<br>LL1|QW3<br>QW3<br>QW3<br>QW3<br>QW3<br>~~MC~~<br>~~MC~~<br>~~MC~~<br>~~MC~~<br>~~MC~~<br><br><br><br><br><br><br><br><br><br>|~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~|~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~|
|D<br>D<br>D<br>D<br>D|QW2<br>QW2<br>QW2<br>QW2<br>QW2<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~GR~~<br><br><br><br><br><br>S1<br>S1<br>S1<br>S1<br>S1<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>JTJT<br>JTJT<br>JT<br><br><br>|MX<br>MX<br>MX<br>MX<br>MX<br>~~PH~~<br>PH<br>PH<br>~~PH~~<br>PH<br>OL<br>OL<br>OL<br>OL<br>OL<br>PW<br>PW<br>PW<br>PW<br>PW|||



1 0.2 0.4 0.6 0.8


|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
|||OP<br>OP<br>OP<br>OP<br>OP|||
|||||~~LL2~~<br>~~LL2~~<br><br>|
|||||~~LL2~~<br><br><br>~~LL2~~<br>~~LL2~~|
|||JB<br>JB<br>JB<br>JB<br>JB<br>DS1<br>DS1<br>DS1<br>DS1<br>DS1<br>W1<br>W1<br>W1<br>W1<br>W1<br>LL<br>LL<br>LL<br>LL<br>LL|~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>QW3<br>QW3<br>QW3<br>QW3<br>QW3<br>~~MC~~<br>~~MC~~<br>~~MC~~<br>~~MC~~<br>~~MC~~<br><br><br><br><br><br>1<br>1<br>1<br>1<br>1<br><br><br><br><br>||
|||QW2<br>QW2<br>QW2<br>QW2<br>QW2<br>~~GR~~<br>~~G~~<br>~~GR~~<br>~~G~~<br>~~G~~<br>XV<br>XV<br>XV<br>XV<br>XV<br><br><br><br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br>~~DS2~~<br><br><br><br><br><br>JTJT<br>JTJT<br>JT<br><br><br>|MX<br>MX<br>MX<br>MX<br>MX<br><br>~~R~~<br><br>~~R~~<br>~~R~~<br>~~PH~~<br>PH<br>PH<br>~~PH~~<br>PH<br>OL<br>OL<br>OL<br>OL<br>OL<br><br><br><br>PW<br>PW<br>PW<br>PW<br>PW||


|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
||OP<br>OP<br>OP<br>OP<br>OP|||||
|||||~~LL~~<br>~~LL2~~<br><br>|~~LL~~<br>~~LL2~~<br><br>|
|||||~~LL2~~<br><br><br>~~LL~~<br>~~LL~~|~~LL2~~<br><br><br>~~LL~~<br>~~LL~~|
||JB<br>JB<br>JB<br>JB<br>JB<br>QW1<br>QW1<br>QW1<br>QW1<br>QW1|QW<br>Q<br>QW<br>Q<br>QW<br>~~MC~~<br>~~MC~~<br>~~MC~~<br>~~MC~~<br>~~MC~~<br>JTJT<br>JTJT<br>JT<br><br><br><br><br><br>LL1<br>LL1<br>LL1<br>LL1<br>LL1<br><br><br><br><br>|~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>~~Y2~~<br>3<br>W3<br>3<br>W3<br>3<br><br><br><br><br>|||
||QW2<br>~~QW2~~<br>~~QW2~~<br>QW2<br>QW2<br><br><br><br><br><br>DS1<br>DS1<br>DS1<br>DS1<br>DS1<br><br><br><br><br>|MX<br>MX<br>MX<br>MX<br>MX<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~PH~~<br>PH<br>PH<br>~~PH~~<br>PH<br>DS2<br>DS2<br>DS2<br>DS2<br>DS2<br><br><br><br>OL<br>OL<br>OL<br>OL<br>OL<br>PW<br>PW<br>PW<br>PW<br>PW||||
||QW2<br>~~QW2~~<br>~~QW2~~<br>QW2<br>QW2<br><br><br><br><br><br>DS1<br>DS1<br>DS1<br>DS1<br>DS1<br><br><br><br><br>|MX<br>MX<br>MX<br>MX<br>MX<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~GR~~<br>~~PH~~<br>PH<br>PH<br>~~PH~~<br>PH<br>DS2<br>DS2<br>DS2<br>DS2<br>DS2<br><br><br><br>OL<br>OL<br>OL<br>OL<br>OL<br>PW<br>PW<br>PW<br>PW<br>PW||||



0.2 0.4 0.6 0.8



0.2 0.4 0.6 0.8



0.2 0.4 0.6 0.8



SRP(E,4) SRP(E,16) SRP(E,64) SRP(E,256)


PowerMoE LLaMA-MoE-v1 OLMoE LLaMA-MoE-v2 JetMoE OpenMoE MiniCPM-MoE Qwen1.5-MoE DeepSeek-V2-Lite DeepSeekMoE XVERSE-MoE


Qwen3 Yuan2.0 Phi-3.5-MoE GRIN-MoE Mixtral-8x7B Jamba-Mini Qwen2


Figure 6: SRP( _E, m_ ) of each model on _S_, compared with the mean log perplexity on _S_ . Marker
size represents model size.


**E.3** **SRP and model architecture**


Table 6 compares each model’s segment routing best performance with several architecture parameters
listed in Table 4 but not in Table 1. On these parameters, we do not observe significant patterns
related to SRP.


Table 6: SRP( _E,_ 16) of each model on _S_, compared with architecture parameters listed in Table 4
but not in Table 1.



# Params (B) Active Param # Experts
Model SRP # Layers
Ratio (%)

Total Active T A



LLaMA-MoE-v2 78.16 8.03 3.80 47.36 32 8 2

Yuan2.0 63.48 39.94 3.70 9.27 24 32 2

PowerMoE 55.17 3.30 0.88 26.76 32 40 8
Qwen3 54.14 30.53 3.35 10.98 48 128 8
Phi-3.5-MoE 51.98 41.87 6.64 15.86 32 16 2

OLMoE 50.91 6.92 1.28 18.53 16 64 8

GRIN-MoE 50.39 41.87 6.64 15.86 32 16 2


Mixtral-8x7B 49.36 46.70 12.88 27.58 32 8 2

MiniCPM-MoE 48.85 13.87 4.32 31.13 40 8 2

JetMoE 47.45 8.52 2.33 27.36 24 8 2

LLaMA-MoE-v1 45.29 6.74 3.50 51.85 32 16 4


XVERSE-MoE 38.58 25.78 4.23 16.39 28 64 6

Jamba-Mini 38.08 51.57 12.11 23.48 32 16 2
DeepSeek-V2-Lite 37.92 15.71 2.66 16.94 27 64 6
DeepSeekMoE 36.94 16.38 2.83 17.27 28 64 6
Qwen2 36.74 57.41 14.25 24.82 28 64 8


NLLB-MoE (en) 25.24 27.25 1.88 6.88 24 128 2
(de) 31.35 27.25 1.88 6.88 24 128 2
Qwen1.5-MoE 30.71 14.32 2.69 18.78 24 60 4
OpenMoE 28.77 11.86 3.80 32.07 24 32 2
SwitchTF (en) 19.33 3.71 0.11 3.02 12 128 1
(de) 19.27 3.71 0.11 3.02 12 128 1


**E.4** **SRP per segment position**


To determine whether the segment position _p_ can affect the segment routing best performance, we
calculate _SRP_ ( _E, m_ ) on each segment position by summarizing statistics of all segments that share


22


the same position. Figure 7 illustrates this position-wise SRP( _E, m_ ) at each possible segment
position. Most models have nearly constant SRP( _E, m_ ) at every position except _p_ = 0, where many
models activate specialized experts to handle the beginning of the input sequence. This stability
of local routing consistency across input positions allows us to use segments from all positions to
calculate SRP( _E, m_ ), and apply conclusions based on SRP( _E, m_ ) to any segment of the input
(except the very first one).


LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE


0.8


0.6


0.4


0.2



200 400



200 400 200 400 200 400 200 400 200 400 200 400 200 400 200 400 200 400



LLaMA-MoE-v1 XVERSE-MoE Jamba-Mini DeepSeek-V2-Lite DeepSeekMoE Qwen2 NLLB-MoE Qwen1.5-MoE OpenMoE SwitchTransformers



0.8


0.6


0.4


0.2



200 400



200 400 200 400 200 400 200 400 200 400 200 400 200 400 200 400 200 400



Position Position Position Position Position Position Position Position Position Position

SRP(E,4) SRP(E,16) SRP(E,64) SRP(E,256)


Figure 7: Position-wise SRP of each model on _S_ . For encoder-decoder models, dotted lines show
the encoder SRP( _E, m_ ) and solid lines show the decoder ones.


**E.5** **SRP across domains**


To verify whether local routing consistency is transitive across different domains, we calculate the
correlation of expert segment routing best performance between pair-wise domains and demonstrate
it in Figure 8. We also compute the correlation of expert activation frequency between pair-wise
domains, results illustrated in Figure 9. By comparing corresponding heapmaps, we can see that local
routing consistency is nearly always positively correlated, even between distant domains on which the
experts’ activation frequencies are negatively correlated. This means that local routing consistency
is transitive; domain-specialized experts with high local routing consistency in one domain tend to
exhibit it in any other domain. We also found that some models (e.g., LLaMA-MoE-v2 and Qwen2)
do not show a significant difference between domains, which is aligned with the results in Section 4.2.



OMWKGHOCOSLMCCAXBKC4SE

OMWKGHOCOSLMCCAXBKSE



LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE 1


0.5



LLaMA-MoE-v1 XVERSE-MoE Jamba-Mini DeepSeek-V2-Lite DeepSeekMoE Qwen2 NLLB-MoE Qwen1.5-MoE OpenMoE SwitchTransformers



0


−0.5


−1



C4 C4 CC BK WK AX SE GH LMOMOC OS



C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS



Figure 8: Correlation between domain-wise expert SRP of each model. C4: C4; CC: CommonCrawl;
BK: Books; WK: Wikipedia; AX: ArXiv; SE: StackExchange; GH: GitHub; LM: LMArena; OM:
OpenMath; OC: OpenCode; OS: OpenScience.



OMWKGHOCOSLMCCAXBKC4SE

OMWKGHOCOSLMCCAXBKSE



LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE 1


0.5



LLaMA-MoE-v1 XVERSE-MoE Jamba-Mini DeepSeek-V2-Lite DeepSeekMoE Qwen2 NLLB-MoE Qwen1.5-MoE OpenMoE SwitchTransformers



0


−0.5


−1



C4 C4 CC BK WK AX SE GH LMOMOC OS



C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS C4 CC BK WK AX SE GH LMOMOC OS



Figure 9: Correlation between the domain-wise expert activation frequency of each model. C4: C4;
CC: CommonCrawl; BK: Books; WK: Wikipedia; AX: ArXiv; SE: StackExchange; GH: GitHub;
LM: LMArena; OM: OpenMath; OC: OpenCode; OS: OpenScience.


23


**E.6** **SRP vs. SCH**


To clarify the relation between SRP( _E, m_ ) and SCH( _E, m, ρ_ ), Table 7 lists the correlation between
them across all models. SRP( _E, m_ ) and SCH( _E, m, ρ_ ) are always highly positively correlated
regardless of the values of _m_ and _ρ_ . This ensures that SCH shares the same property of SRP under
reasonable segment length and cache size. Furthermore, when _ρ_ is around 1.5, the two metrics are
most closely related, nearly perfectly linear, aligned with Figure 2 where most models have _ρ_ ( _E, m_ )
between 1–3 when _m ≥_ 16, as well as our previous claim that _ρ_ = 2 balances cache effectiveness
and efficiency.


Table 7: Correlation between SRP( _E, m_ ) and SCH( _E, m, ρ_ ) across all models. Bold font indicates
the highest correlation across _ρ_ for each _m_ .


_m_ _ρ_ = 0 _._ 5 _ρ_ = 1 _._ 0 _ρ_ = 1 _._ 5 _ρ_ = 2 _._ 0 _ρ_ = 2 _._ 5 _ρ_ = 3 _._ 0


4 96.58 97.98 **98.21** 96.04 89.07 75.05

16 97.87 99.52 **99.76** 98.49 95.70 92.33

64 96.75 99.01 **99.78** 99.02 96.81 93.60

256 95.41 98.32 **99.58** 99.20 97.11 93.70


**E.7** **Statistical significance**


Due to the very high correlation between SRP and SCH, we choose SCH to represent local routing
consistency, and report the 95% confidence intervals when _ρ_ = 2 in Table 8. The confidence intervals
are obtained by bootstrapping 1,000 times with samples from _S_ .


Table 8: 95% confidence interval of SCH( _E, m,_ 2) of each model. The decoder of SwitchTransformer does not have valid data when _m_ = 256.


Model _m_ = 4 _m_ = 16 _m_ = 64 _m_ = 256


LLaMA-MoE-v2 (99 _._ 93 _,_ 99 _._ 94) (98 _._ 51 _,_ 98 _._ 56) (97 _._ 36 _,_ 97 _._ 45) (96 _._ 69 _,_ 96 _._ 80)
Yuan2.0 (94 _._ 99 _,_ 95 _._ 10) (82 _._ 39 _,_ 82 _._ 57) (78 _._ 44 _,_ 78 _._ 64) (76 _._ 57 _,_ 76 _._ 81)
PowerMoE (92 _._ 85 _,_ 92 _._ 95) (80 _._ 13 _,_ 80 _._ 30) (74 _._ 53 _,_ 74 _._ 75) (71 _._ 92 _,_ 72 _._ 18)
Qwen3 (91 _._ 58 _,_ 91 _._ 74) (75 _._ 48 _,_ 75 _._ 75) (67 _._ 03 _,_ 67 _._ 40) (61 _._ 62 _,_ 62 _._ 09)
Phi-3.5-MoE (89 _._ 48 _,_ 89 _._ 70) (74 _._ 25 _,_ 74 _._ 62) (67 _._ 10 _,_ 67 _._ 57) (63 _._ 26 _,_ 63 _._ 84)
OLMoE (89 _._ 23 _,_ 89 _._ 44) (72 _._ 69 _,_ 73 _._ 04) (65 _._ 09 _,_ 65 _._ 52) (61 _._ 04 _,_ 61 _._ 54)
GRIN-MoE (88 _._ 18 _,_ 88 _._ 40) (72 _._ 47 _,_ 72 _._ 83) (65 _._ 07 _,_ 65 _._ 54) (61 _._ 07 _,_ 61 _._ 63)


Mixtral-8x7B (88 _._ 20 _,_ 88 _._ 28) (73 _._ 89 _,_ 74 _._ 00) (66 _._ 25 _,_ 66 _._ 41) (62 _._ 20 _,_ 62 _._ 40)
MiniCPM-MoE (88 _._ 11 _,_ 88 _._ 19) (73 _._ 09 _,_ 73 _._ 19) (64 _._ 95 _,_ 65 _._ 07) (60 _._ 73 _,_ 60 _._ 87)
JetMoE (85 _._ 64 _,_ 85 _._ 72) (70 _._ 79 _,_ 70 _._ 88) (63 _._ 04 _,_ 63 _._ 16) (59 _._ 05 _,_ 59 _._ 20)
LLaMA-MoE-v1 (80 _._ 80 _,_ 80 _._ 89) (66 _._ 96 _,_ 67 _._ 04) (60 _._ 25 _,_ 60 _._ 35) (57 _._ 07 _,_ 57 _._ 18)


XVERSE-MoE (78 _._ 17 _,_ 78 _._ 31) (57 _._ 34 _,_ 57 _._ 54) (46 _._ 39 _,_ 46 _._ 61) (41 _._ 00 _,_ 41 _._ 25)
Jamba-Mini-1.6 (77 _._ 82 _,_ 77 _._ 95) (56 _._ 87 _,_ 57 _._ 05) (46 _._ 43 _,_ 46 _._ 68) (41 _._ 10 _,_ 41 _._ 41)
DeepSeek-V2-Lite (77 _._ 86 _,_ 78 _._ 01) (56 _._ 62 _,_ 56 _._ 82) (45 _._ 76 _,_ 46 _._ 00) (40 _._ 15 _,_ 40 _._ 43)
DeepSeekMoE (76 _._ 99 _,_ 77 _._ 14) (55 _._ 21 _,_ 55 _._ 42) (44 _._ 07 _,_ 44 _._ 32) (38 _._ 37 _,_ 38 _._ 65)
Qwen2 (75 _._ 18 _,_ 75 _._ 26) (54 _._ 86 _,_ 54 _._ 92) (45 _._ 26 _,_ 45 _._ 32) (40 _._ 96 _,_ 41 _._ 03)


NLLB-MoE (en) (62 _._ 31 _,_ 62 _._ 44) (37 _._ 60 _,_ 37 _._ 84) (28 _._ 56 _,_ 28 _._ 86) (24 _._ 06 _,_ 24 _._ 37)
(de) (65 _._ 38 _,_ 65 _._ 59) (44 _._ 93 _,_ 45 _._ 24) (37 _._ 69 _,_ 38 _._ 03) (31 _._ 76 _,_ 32 _._ 12)
Qwen1.5-MoE (69 _._ 07 _,_ 69 _._ 20) (45 _._ 31 _,_ 45 _._ 48) (33 _._ 37 _,_ 33 _._ 58) (27 _._ 49 _,_ 27 _._ 72)
OpenMoE (65 _._ 03 _,_ 65 _._ 24) (42 _._ 07 _,_ 42 _._ 39) (32 _._ 22 _,_ 32 _._ 60) (27 _._ 65 _,_ 28 _._ 09)
SwitchTF (en) (54 _._ 81 _,_ 54 _._ 95) (26 _._ 80 _,_ 27 _._ 04) (17 _._ 44 _,_ 17 _._ 72) (13 _._ 66 _,_ 13 _._ 97)
(de) (55 _._ 39 _,_ 55 _._ 56) (26 _._ 76 _,_ 27 _._ 06) (16 _._ 64 _,_ 16 _._ 94)


**E.8** **Layer level results**


Figure 10 illustrates each model’s layer-wise SRP. Most models have peak SRPs among middle
layers, while some (e.g., Yuan2.0 and MiniCPM) have another peak at the last layer. We conjecture
that middle layers are less tied to input/output tokens and thus more sensitive to the general topic, and


24


the final layers process highly abstract information that is also more related to the overall topic. Both
encourage routers to select similar experts within a local segment that share the same topic across
tokens. PowerMoE and Qwen2 have another peak on layer 2 due to expert imbalance. Appendix E.9
gives a clear view on this.


LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE



1


0.8


0.6


0.4


0.2



5


4


3


2


1



1 LLaMA-MoE-v1 16 32 1 XVERSE-MoE 12 24 1 Jamba-Mini 16 32 1 DeepSeek-V2-Lite 24 48 1 DeepSeekMoE 16 32 1 Qwen2 8 16 1 NLLB-MoE 16 32 1 Qwen1.5-MoE 16 32 1 OpenMoE 20 40 1 SwitchTransformers 12 24



1


0.8


0.6


0.4


0.2



5


4


3


2


1



1 16 32 1 14 28 1 16 32 1 13 27 1 14 28 1 14 28 1 24 48 1 12 24 1 12 24 1 12 24



Layer Layer Layer Layer Layer Layer Layer Layer Layer Layer
SRP(E,4) ρ(E,4) SRP(E,16) ρ(E,16) SRP(E,64) ρ(E,64) SRP(E,256) ρ(E,256)


Figure 10: Layer-wise SRP on _S_ of each model. Solid lines show SRP( _E, m_ ) while dotted lines
show corresponding _ρ_ ( _E, m_ ).


We also calculated layer-wise SCH, results demonstrated in Figure 11. The patterns are the same as
SRP, indicating a high correlation between the two metrics.


LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE

1


0.8


0.6


0.4


0.2



1 LLaMA-MoE-v1 16 32 1 XVERSE-MoE 12 24 1 Jamba-Mini 16 32 DeepSeek-V2-Lite 1 24 48 1 DeepSeekMoE 16 32 1 Qwen2 8 16 1 NLLB-MoE 16 32 1 Qwen1.5-MoE 16 32 1 OpenMoE 20 40 SwitchTransformers 1 12 24



1


0.8


0.6


0.4


0.2



1 16 32 1 14 28 1 16 32 1 13 27 1 14 28 1 14 28 1 24 48 1 12 24 1 12 24 1 12 24



Layer Layer Layer Layer Layer Layer Layer Layer Layer Layer
SCH(E,4,1) SCH(E,4,2) SCH(E,16,1) SCH(E,16,2) SCH(E,64,1) SCH(E,64,2) SCH(E,256,1) SCH(E,256,2)


Figure 11: Layer-wise SCH on _S_ of each model. Solid lines show SCH( _E, m,_ 1) while dotted lines
show corresponding SCH( _E, m,_ 2).


**E.9** **Expert level results**


We demonstrate expert-wise segment routing best performance against activation frequency in
Figure 12. LLaMA-MoE-v2, Yuan2.0, and PowerMoE have experts with very high activation
frequency. These experts naturally have very high local routing consistency and contribute to these
models’ high model-level local routing consistency. The imbalanced experts of PowerMoE mainly
belong to layer 2, which also explains the observation in Section E.8.


LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE



Ly. 24


12



Ly. 32


16



Ly. 48


24



Ly. 16


8



Ly. 32


16





Ly. 40


20



Ly. 24


12



1


0.5



Ly. 32


16



0


1



1


Ly. 32



1


Ly. 28



1


Ly. 32



1


Ly. 27



Ly. 32


16


1



1


Ly. 48





1


Ly. 24



1

|Col1|Col2|Col3|Col4|Ly|
|---|---|---|---|---|
||||||



Ly. 24


|Col1|Col2|Ly.<br>3<br>1<br>1|2|Col5|
|---|---|---|---|---|
||||6||



LLaMA-MoE-v1 XVERSE-MoE Jamba-Mini DeepSeek-V2-Lite DeepSeekMoE Qwen2 NLLB-MoE Qwen1.5-MoE OpenMoE SwitchTransformers



1


Ly. 28



14


1



0.5


0



16


1





14


1



13


1



16


1



24


1



12


1



12


1



Ly. 28


14


1


|Col1|Col2|Ly.|Col4|Col5|
|---|---|---|---|---|
|||1<br>2<br>Ly.|4||
||||2||


|Col1|Col2|Col3|Col4|Ly|
|---|---|---|---|---|
|||||L|
||||||



Act. Freq. Act. Freq. Act. Freq. Act. Freq. Act. Freq. Act. Freq. Act. Freq. Act. Freq. Act. Freq. Act. Freq.


Figure 12: Per-expert activate frequency vs. SRP. The x-axis is stretched to show experts with very
low or high activation frequency. Gray dashed lines indicate the theoretical lower bound of SRP
at different activation frequencies. Green dashed lines show the expected activation frequency of
experts from each model.


Furthermore, Figures 13, 14, 15 and 16 compares SRP with domain and vocabulary specialzations.
The plots are aligned with the conclusion of Section 4.2 that when the model exhibits domain


25


LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE



Ly. 24


12



Ly. 32


16



Ly. 48


24



Ly. 16


8



Ly. 32


16



Ly. 32


16



Ly. 40


20



Ly. 24


12



1


0.8


0.6


0.4


0.2



Ly. 32


16



1

|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



Ly. 28



1

|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



Ly. 32



1

|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



Ly. 27



Ly. 32


16


1



1

|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



Ly. 48



1

|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



Ly. 24



1

|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



Ly. 24



1

|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



Ly. 24


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



LLaMA-MoE-v1 XVERSE-MoE Jamba-Mini DeepSeek-V2-Lite DeepSeekMoE Qwen2 NLLB-MoE Qwen1.5-MoE OpenMoE SwitchTransformers



1


Ly. 28



14


1



1


0.8


0.6


0.4


0.2

|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



0 1 2 3



1


Ly. 32


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||


|Col1|Col2|Col3|L|
|---|---|---|---|
|||||
|||||
|||||
|||||



0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3



12


1



16


1



14


1



13


1



16


1



24


1



12


1



Ly. 28


14


1



12


1


Ly. 24


12


1



Domain Spec. Domain Spec. Domain Spec. Domain Spec. Domain Spec. Domain Spec. Domain Spec. Domain Spec. Domain Spec. Domain Spec.


Figure 13: Per-expert domain specialization vs. SRP.


LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE



Ly. 24


12



Ly. 32


16



Ly. 48


24



Ly. 16


8



Ly. 32


16



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 24



Ly. 40


20



1


0.8


0.6


0.4


0.2



Ly. 32


16



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 28



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 32



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 27



Ly. 32


16


1



Ly. 32


16


1



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 24


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



LLaMA-MoE-v1 XVERSE-MoE Jamba-Mini DeepSeek-V2-Lite DeepSeekMoE Qwen2 NLLB-MoE Qwen1.5-MoE OpenMoE SwitchTransformers



1


Ly. 28



14


1



1


0.8


0.6


0.4


0.2



1


Ly. 32



16


1



14


1



13


1



16


1



12


1



12


1



Ly. 28


14


1


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



0.5 1



0.5 1 0.5 1 0.5 1 0.5 1 0.5 1 0.5 1 0.5 1



In. Vocab. Spec. In. Vocab. Spec. In. Vocab. Spec. In. Vocab. Spec. In. Vocab. Spec. In. Vocab. Spec. In. Vocab. Spec. In. Vocab. Spec.


Figure 14: Per-expert input vocabulary specialization vs. SRP. Encoder-decoder models are not
involved due to different input formats from other decoder-only models.


LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE



Ly. 24


12



Ly. 32


16



Ly. 48


24



Ly. 16


8



Ly. 32


16



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 24



Ly. 40


20



1


0.8


0.6


0.4


0.2



Ly. 32


16



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 28



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 32



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 27



Ly. 32


16


1



Ly. 32


16


1



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 24



Ly. 24


12


1


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



LLaMA-MoE-v1 XVERSE-MoE Jamba-Mini DeepSeek-V2-Lite DeepSeekMoE Qwen2 NLLB-MoE Qwen1.5-MoE OpenMoE SwitchTransformers



1


Ly. 28



14


1



1


0.8


0.6


0.4


0.2

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



0 0.5 1



1


Ly. 32


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



0 0.5 1 0 0.5 1 0 0.5 1 0 0.5 1 0 0.5 1 0 0.5 1 0 0.5 1



16


1



14


1



13


1



16


1



12


1



12


1



Ly. 28


14


1



P. O. Vocab. Spec. P. O. Vocab. Spec. P. O. Vocab. Spec. P. O. Vocab. Spec. P. O. Vocab. Spec. P. O. Vocab. Spec. P. O. Vocab. Spec. P. O. Vocab. Spec.


Figure 15: Per-expert predicted output vocabulary specialization vs. SRP. Encoder-decoder models
are not involved due to different input formats from other decoder-only models.


LLaMA-MoE-v2 Yuan2.0 PowerMoE Qwen3 Phi-3.5-MoE OLMoE GRIN-MoE Mixtral-8x7B MiniCPM-MoE JetMoE



Ly. 24


12



Ly. 32


16



Ly. 48


24



Ly. 16


8



Ly. 32


16



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 24



Ly. 40


20



1


0.8


0.6


0.4


0.2



Ly. 32


16



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 28



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 32



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 27



Ly. 32


16


1



Ly. 32


16


1



1

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



Ly. 24



Ly. 24


12


1


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



LLaMA-MoE-v1 XVERSE-MoE Jamba-Mini DeepSeek-V2-Lite DeepSeekMoE Qwen2 NLLB-MoE Qwen1.5-MoE OpenMoE SwitchTransformers



1


Ly. 28



14


1



1


0.8


0.6


0.4


0.2

|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



0 0.5 1



1


Ly. 32


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||


|Col1|Col2|L|
|---|---|---|
||||
||||
||||
||||



0 0.5 1 0 0.5 1 0 0.5 1 0 0.5 1 0 0.5 1 0 0.5 1 0 0.5 1



16


1



14


1



13


1



16


1



12


1



12


1



Ly. 28


14


1



G. T. O. Vocab. Spec. G. T. O. Vocab. Spec. G. T. O. Vocab. Spec. G. T. O. Vocab. Spec. G. T. O. Vocab. Spec. G. T. O. Vocab. Spec. G. T. O. Vocab. Spec. G. T. O. Vocab. Spec.


Figure 16: Per-expert ground-truth output vocabulary specialization vs. SRP. Encoder-decoder
models are not involved due to different input formats from other decoder-only models.


26


specialization, domain-specialized experts contribute more to overall local routing consistency than
vocabulary-specialized experts.


27


