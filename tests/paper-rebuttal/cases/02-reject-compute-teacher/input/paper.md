**Policy** **Reference Estimation**



**Verification**

























**Reward** policy answers by comparing to

synthesized answers



**Explore** with
parallel rollouts



**Synthesize** exploration

into better answers



**Figure 1 Compute as Teacher (CaT) pipeline. Exploration** : During each GRPO step, the current policy produces _G_ parallel
rollouts for a prompt. **Synthesis** : A frozen _anchor_, the initial policy, conditions only on the set of rollouts and synthesizes
an _estimated reference_ . We convert this supervision into **rewards** : (a) _verifiable_ domains use a programmatic equivalence
check on final answers; (b) _non-verifiable_ domains use _self-proposed rubrics_ whose yes/no criteria are marked by an
LLM judge, with reward given by the proportion satisfied. CaT can be applied at test time for inference-time gains or
inside RL ( _CaT-RL_ ) to improve the policy.


1


### **1 Introduction**

Post-training large language models (LLMs) for specialized skills typically relies on supervised fine-tuning with
labeled references (Ouyang et al., 2022; Wei et al., 2022), or verifiable rewards from programmatic checkers
(Lambert et al., 2024; Shao et al., 2024). Many valuable tasks lack both. In non-verifiable settings, such as
clinical or lifestyle guidance (Arora et al., 2025), freeform dialogue (Roller et al., 2020), and creative writing
(Paech, 2023), there may be multiple valid answers; experts can disagree, and deterministic rule-checking is
impractical. As a result, practitioners often fall back on (i) annotation pipelines that are hard to scale, or (ii)
judge-only feedback where another LLM assigns coarse scores to freeform outputs, despite known issues with
inconsistency, verbosity bias, and reward hacking.


This paper asks a simple question:


_Can inference compute substitute for missing supervision?_


**Compute as Teacher (CaT).** We answer _yes_ . Our method, Compute as Teacher (CaT), converts the model’s
own exploration into reference-free supervision. For each prompt, the current policy generates a set of parallel
rollouts. A frozen anchor—the initial policy used only as an estimator—conditions _on the rollout set_ and
_synthesizes_ a single estimated reference by reconciling omissions, contradictions, and partial solutions. This
separation keeps roles independent: the current policy explores while a stable estimator turns extra inference
compute into a teacher signal derived entirely from the model’s behavior. Practically, CaT reuses the group
rollout compute budget already common in RL (e.g., GRPO), adding little overhead beyond the compute
already spent to sample the group. _(see Figure 1)_


**Reference-free signals for both regimes.** CaT turns the estimated reference into learning signals in two
complementary settings:


  - **Verifiable domains (e.g., math).** We programmatically reward agreement of the response with the estimated
reference, e.g., by checking whether answer strings match.


  - **Non-verifiable domains.** The model _self-proposes rubrics_ —binary criteria that characterize the estimated
reference. An independent judge marks each criterion yes/no, and the reward is the proportion satisfied.
Rubrics decompose coarse judgments into parts, reducing instability and surface-form bias relative to
direct judging (Arora et al., 2025).


**Synthesis, notselection.** A natural alternative is to select a single rollout using confidence heuristics, perplexity,
majority vote, or an LLM judge. CaT is different: the anchor _constructs_ a new answer that can (i) rightfully
disagree with the majority and (ii) be correct even when all rollouts are wrong. Empirically, we observe both
behaviors, disagreement with majority on 14% of questions, and disagreement with all rollouts on almost 1%,
indicating structured reconciliation rather than selection. Moreover, performance scales with the number of
rollouts _G_, yielding a practical FLOPs-for-supervision trade-off.


**Why it works (intuition).** Parallel rollouts diversify generations, surfacing different sub-facts or solution steps.
Conditioning the anchor on the _set_ of rollouts enables ensemble-like error correction within the model’s
generative space: complementary evidence is integrated; idiosyncratic errors are suppressed. In non-verifiable
domains, rubric rewards transform “match the teacher” into discrete, auditable criteria, providing shaped
feedback to RL that is less sensitive to verbosity and formatting. We keep the anchor question-blind to
prevent it from acting as just another rollout and to encourage genuine cross-rollout reasoning.


**Practicality.** CaT is drop-in: it requires no human labels and no domain-specific verifiers beyond simple
answer-equivalence for math. It can be used (i) at test time to boost accuracy by spending extra inference
compute, and (ii) for training ( _CaT-RL_ ) by turning the estimated reference (or rubric satisfaction) into
rewards inside an RL loop. In practice, we find that CaT improves three distinct 4–8B-scale model families
(Gemma 3 4B, Qwen 3 4B, Llama 3.1 8B) on MATH-500 and HealthBench at test time, and CaT-RL delivers
additional gains, with the trained policy usually exceeding the initial teacher.


2


**CaT bridges several lines of work.** Like self-training (Schmidhuber, 2003, 2013; Silver et al., 2016, 2018) and
knowledge distillation (Hinton et al., 2015), it learns from model-generated supervision, but it derives the
target by reconciling multiple samples rather than trusting a single self-label. Unlike best-of- _N_ (Ouyang et al.,
2022) or majority vote (Wang et al., 2023a), it constructs a new answer that can depart from consensus.
Compared to LLM-as-a-judge (Zheng et al., 2023), rubric-based scoring yields decomposed, specific criteria
that mitigate instability and bias (Gunjal et al., 2025). Finally, CaT complements programmatic verification
(Lambert et al., 2024) by extending learning to non-verifiable domains where formal checkers are unavailable.


**Contributions:**


1. **ComputeasTeacher(CaT).** A simple procedure that turns inference compute into supervision by estimating
a reference from parallel rollouts using a stable anchor policy.


2. **Self-proposed rubric rewards.** A practical, auditable signal for non-verifiable tasks that avoids human
references and reduces reliance on brittle judge-only scores.


3. **Comprehensive empirical study.** Test-time and RL gains across MATH-500 and HealthBench and three
model families, plus analyses showing non-majority reconciliation, correcting when all rollouts are wrong,
and improvements scaling with rollout count.


**Organization.** Section 2 contextualizes CaT among related work. Section 3 formalizes CaT and the rubric
mechanism. Section 4 details experimental setup. Section 4.1 presents results, ablations, and further analyses.
Section 5 discusses limitations, future work, and concludes.

### **2 Related Work**


**Reference-Free Fine-Tuning.** Reference-free training has been a long-standing direction in statistical learning (Pearson, 1901). In LLM finetuning, Bai et al. (2022) proposed Constitutional AI for training harmless AI
with self-revised generations. Wang et al. (2023b) proposed Self-Instruct for training instruction following
through self-generated and filtered data, while Zelikman et al. (2024) proposed Quiet-STaR for learning to
produce useful thought tokens without reference reasoning or external feedback. These methods either focus
on specific tasks, or specific skills like producing thought tokens, while our approach can holistically improve
outputs for arbitrary specialized tasks.


**Reference-Free RL.** Recently, there have been a series of impressive preprints on reference-free LLM training
via RL. Zuo et al. (2025) proposed Test-Time RL (TTRL), which uses self-consistent majority consensus
answers (Wang et al., 2023a) as label estimates for RL fine-tuning in math. In Absolute Zero, Zhao et al.
(2025a) improve LLMs via self-play on math and coding tasks, solving increasingly difficult problems posed by
the model itself. While these methods propose useful reference-free RL strategies, they are only applicable in
verifiable domains. Other recent work has proposed minimizing entropy or maximizing self-certainty (Zhao
et al., 2025c; Agarwal et al., 2025; Prabhudesai et al., 2025; Gao et al., 2025; Li et al., 2025). Similarly,
Wen et al. (2025) propose a scoring function for multiple choice questions based on mutual predictability.
In contrast, our approach is generative, able to construct and synthesize answers outside of the explored
distribution, and extends beyond verifiable to non-verifiable domains.


**Non-Verifiable RL.** In non-verifiable domains, where rule-based answer checking is infeasible, a few methods
have established ways to score outputs against references. VeriFree (Zhou et al., 2025), JEPO (Tang et al.,
2025), and RLPR (Yu et al., 2025) compute the probability of the reference given a generated reasoning chain
under the initial policy model to provide a verifier-free reward function. In contrast, Gunjal et al. (2025)
propose Rubrics as Rewards (RaR), a more general approach that constructs rubrics from reference answers,
which are then judged via an LLM to compute a score. Unlike all of these methods, our approach does not
require any reference answer.


3


### **3 Compute as Teacher (CaT)**

**Notation.** We use _q_ for the prompt, _o_ for a rollout, _o_ 1: _G_ for the rollout set, _s_ for the synthesized reference, _r_
for a criterion from a rubric _R_, _v_ for a binary yes/no verdict from an LLM judge _π_ _J_, _π_ _t_ for the current policy,
and _π_ 0 for the (frozen) anchor. We introduce the GRPO reward symbol _R_ ( _·_ ) in Section 3.1 and replace it
with task-appropriate definitions in Section 3.3.


**3.1** **Preliminaries**


**Group Relative Policy Optimization (GRPO).** GRPO (Shao et al., 2024) is a memory-efficient variant of PPO
(Schulman et al., 2017) that avoids a value network by using a group baseline. For each _q_, we draw _G_ rollouts
_o_ 1: _G_ from the policy _π_ _θ_ old and optimize



_|o_ _i_ _|_
� _L_ _t_ ( _θ_ ) _−_ _β_ D KL � _π_ _θ_ _∥_ _π_ ref �

_t_ =1 �



_J_ GRPO ( _θ_ ) = E _q, {o_ _i_ _}_


with the clipped surrogate



1

_G_
�



_G_
�


_i_ =1



1

_|o_ _i_ _|_



_,_ (1)



_L_ _t_ ( _θ_ ) = min� _r_ _t_ ( _θ_ ) _A_ [ˆ] _i,t_ _,_ clip� _r_ _t_ ( _θ_ ) _,_ 1 _−_ _ε,_ 1 + _ε_ � _A_ ˆ _i,t_ � _,_ (2)


where the importance weighting token-level ratio and the group-normalized advantage are


_r_ _t_ ( _θ_ ) = _π_ _θ_ ( _o_ _i,t_ _|_ _q, o_ _i,<t_ ) _A_ ˆ _i,t_ = _[R]_ [(] _[q,][ o]_ _[i]_ [)] _[ −]_ _[R]_ [¯] _[G]_ _._ (3)
_π_ _θ_ old ( _o_ _i,t_ _| q, o_ _i,<t_ ) _[,]_ _σ_ _G_


Here _R_ [¯] _G_ = _G_ [1] � _Gj_ =1 _[R]_ [(] _[q, o]_ _[j]_ [)][ is the group mean reward and] _[ σ]_ _[G]_ [ its standard deviation; the KL term discourages]

large policy drift from the reference _π_ ref (typically the initial policy _π_ 0 ).


**3.2** **CaT: Estimating a reference by synthesizing rollouts**



We turn extra inference compute into a
supervision signal. For each prompt _q_,
the current policy _π_ _t_, at GRPO timestep
_t_, produces a set of _G_ rollouts _o_ 1: _G_ . A
frozen anchor _π_ 0 then synthesizes a single reference response _s_ by reconciling
omissions and contradictions across _o_ 1: _G_ .
We convert this estimated reference into
rewards in two regimes: (i) _verifiable_
tasks (e.g., math) use a lightweight
programmatic checker; and (ii) _non-_
_verifiable_ tasks (e.g., freeform dialogue)
use self-proposed rubrics whose binary
criteria are judged by an LLM, yielding
a fine-grained verifiable reward. [1]



Question


Policy
model





**Figure 2 Estimating a reference via CaT.** At each GRPO step, the current

To estimate a reference response, we

policy _π_ _t_ samples _G_ rollouts _o_ 1: _G_ for a prompt _q_ (exploration). A frozen

introduce a synthesis step, where we anchor _π_ 0 receives only the rollouts (not _q_ ) together with a synthesis
ask the anchor policy to reconcile the prompt _p_ syn and produces a synthesized reference _s_ that reconciles
model’s _exploration_, the parallel rollouts omissions and contradictions across _o_ 1: _G_ . This keeps estimation stable
during GRPO, into a single, improved while _π_ _t_ explores.
answer. Formally, for a question _q_ and
policy _π_ _t_ we draw _G_ rollouts
_o_ _i_ _∼_ _π_ _t_ ( _· | q_ ) _,_ _i_ = 1 _, . . ., G._ (4)


1 Rubric rewards are introduced in Section 3.3 and build on the GRPO setup from Section 3.1.


4


Using a prompt _p_ syn and only the set of rollouts, the anchor produces a synthesized reference
_(see Appendix C for prompts)_


_s ∼_ _π_ 0 ( _· | p_ syn _, o_ 1: _G_ ) _._ (5)


We omit _q_ in Eq. 5 to discourage trivially generating a new rollout and to force the anchor to operate
purely on model exploration [2], integrating complementary evidence and resolving disagreements among _o_ 1: _G_ .
Keeping _π_ 0 fixed decouples exploration (by _π_ _t_ ) from estimation (by _π_ 0 ), improving stability and preventing
role interference since the initial policy and the current policy play different roles as estimator and rollout
generator. We optimize only the current policy. _(cf. Figure 2)_


Since we can estimate reference responses, CaT can be used as an inference-time method to produce stronger
answers if we let the policy _π_ _t_ = _π_ 0 . Instead, in the next section, we show how to train the policy _π_ _t_ by
turning the reference estimate into a reward signal for RL (CaT-RL).


**3.3** **CaT-RL: Turning estimated references into rewards**


Given an estimated reference _s_, we define _R_ ( _q, o_ ) used by GRPO in two regimes and plug it into the advantage
in Eq. 3. _(see Section 3.1 for GRPO)_


**Verifiable tasks (math).** Let _v_ ( _o, s_ ) _∈{_ 0 _,_ 1 _}_ be a programmatic verifier (e.g., final-answer equivalence via a
simple string match or programmatic execution). We set


_R_ ver ( _o_ ; _s_ ) = _v_ ( _o, s_ ) _._ (6)


For math, _v_ extracts the final boxed expression from _o_ and _s_ and checks if they match.


**Non-verifiable tasks (freeform dialogue).** The anchor converts _s_ into a response-specific rubric _R_ = _{r_ _i_ _}_ _[n]_ _i_ =1
using a rubric prompt _p_ rub : _(see Appendix C for prompts)_


_R ∼_ _π_ 0 ( _· | p_ rub _, s_ ) _,_ _r_ _i_ : binary, checkable criterion describing an important property of _s._ (7)


An independent judge LLM _π_ _J_ evaluates whether rollout _o_ satisfies each criterion _r_ _i_ . We score _o_ by the
normalized proportion of satisfied criteria, _(cf. Figure 3)_



_R_ rub ( _o_ ; _R_ ) = [1]

_n_



_n_
� **1** � _π_ _J_ ( _p_ _J_ ; _o, r_ _i_ ) = “yes”� _._ (8)

_i_ =1



**GRPO with CaT rewards.** We use


_R_ ( _q, o_ ) =



_R_ ver ( _o_ ; _s_ ) _,_ if _q_ is verifiable _,_

(9)

� _R_ rub ( _o_ ; _R_ ) _,_ otherwise _,_



in the GRPO objective (Eq. 1–3 in Section 3.1), which computes group-relative advantages with the group
mean as baseline. _(plug into Eq. 3)_


**Remarks.** (i) When _G_ = 1, synthesis offers limited improvement; benefits grow with _G_ due to complementary
information. The reference estimator _π_ 0 resolves disagreements, which highlight points of uncertainty between
multiple responses, in synthesizing the estimated reference. If more of the model’s responses disagree on a
point, then this is something that the model is more uncertain about. We rely on the anchor to use each
response to determine or construct the closest estimate of the truth. (ii) Using the initial policy as the
anchor stabilizes reference estimation while _π_ _t_ explores and improves. (iii) Rubric rewards decompose holistic
judgment into auditable checks, mitigating verbosity and form bias where overall judgments might favor
properties like answer length and style that do not reflect genuinely good answers. _(see Section 4.1)_


2 See Appendix F for commentary on the performance difference of omitting _q_ .


5


**Figure 3 Rubric-based rewards for non-verifiable tasks (CaT-RL).** From the synthesized reference _s_, the anchor _π_ 0 generates
a response-specific rubric _R_ = _{r_ _i_ _}_ _i_ _[n]_ =1 [. A judge model] _[ π]_ _[J]_ [evaluates whether a rollout] _[ o]_ [ satisfies each criterion, yielding]
yes/no verdicts _{v_ _i_ _}_ . We map verdicts to scores and use the normalized proportion satisfied, _n_ [1] � _i_ **[1]** [[] _[v]_ _[i]_ [ =] [ yes] []][, as the]

reward (optionally scaled). For verifiable tasks, we instead apply a programmatic checker against _s_ .


**Algorithm 1** CaT-RL with GRPO (one question)


**Inputs:** Anchor _π_ 0 (frozen), policy _π_ _t_, prompts _p_ syn _, p_ rub _, p_ _J_, question _q_

1: Sample _o_ 1: _G_ _∼_ _π_ _t_ ( _· | q_ ) _▷_ exploration
2: _s ←_ _π_ 0 ( _· | p_ syn _, o_ 1: _G_ ) _▷_ synthesis
3: **for** _i_ in _{_ 1 _, . . ., G}_ **do**
4: **if** _q_ is verifiable **then**

5: _R_ _i_ _←_ _v_ ( _o_ _i_ _, s_ ) _▷_ verifiable rewards
6: **else**
7: _R ←_ _π_ 0 ( _· | p_ rub _, s_ )
1
8: _R_ _i_ _←_ _|R|_ � _r∈R_ **[1]** [[] _[π]_ _[J]_ [(] _[p]_ _[J]_ [;] _[ o]_ _[i]_ _[, r]_ [) =][ “yes”][]] _▷_ non-verifiable rewards

9: Update _π_ _t_ with GRPO using all computed rewards _R_ ( _q, o_ _i_ )

### **4 Experiments**


**Setup summary.** We evaluate Compute as Teacher in two modes— **CaT** (inference-time synthesis only) and
**CaT-RL** (training with CaT-derived rewards)—across three model families, Gemma 3 4B (Kamath et al., 2025),
Qwen 3 4B (Yang et al., 2025), and Llama 3.1 8B (Grattafiori et al., 2024). Our evaluation spans verifiable
domains with MATH-500 (Hendrycks et al., 2021), a set of 500 questions for measuring LLM progress in
mathematics, and non-verifiable domains with HealthBench (Arora et al., 2025), a dataset of 5000 freeform
healthcare chats with physicians and users. For MATH-500, we train and test on the same 500 questions,
crucially without using any reference labels in training, following the test-time training setup in TTRL (Zuo
et al., 2025). For HealthBench, we hold-out 500 questions with physician-designed evaluation rubrics, reporting
rubric scores with GPT-4o (Hurst et al., 2024) as judge. The remaining questions are used for reference-free
training and validation. Unless otherwise specified, CaT conditions the anchor on _G_ = 8 rollouts; and when
evaluating CaT at inference-time, _π_ _t_ = _π_ 0 (no weight updates). Further details are in Appendices E and F.


**Research questions.** Core Performance Validation: **RQ1.** _Does CaT-RL outperform the initial policy and can_
_it improve over the teacher signal (CaT)?_ We contrast CaT-RL with the initial policy baseline and CaT at
inference. **RQ3.** _Does CaT-RL outperform SFT?_ We contrast CaT-RL with CaT-SFT (offline fine-tuning on
synthesized references). **RQ5.** _How does performance scale with the number of rollouts_ _G_ _?_ We sweep _G_ to
study the FLOPs _→_ supervision trade-off.


Reward Signal Validation: **RQ2.** _Are self-proposed rubrics effective rewards in non-verifiable domains?_ We


6


|Col1|Col2|Col3|2 8|Col5|Col6|Col7|Col8|1|Col10|Col11|Col12|Col13|Col14|Col15|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|+8%|+8%|+8%|+<br>+|+<br>+|+<br>+|+<br>+|+<br>+|+<br>|+<br>|+<br>|+<br>|12%<br>+29%|12%<br>+29%|12%<br>+29%|
|||||||||||||+|+|+|
||||||||||||||||
||||||||||||||||
||||||||||||||||


|Col1|Col2|Col3|% 3|Col5|Col6|Col7|Col8|3 %|Col10|Col11|Col12|Col13|Col14|Col15|Col16|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|+11%|+11%|+11%|+17%<br>+1|+17%<br>+1|+17%<br>+1|+17%<br>+1|+17%<br>+1|+9<br>|+9<br>|+9<br>|+9<br>|+9<br>|%|%|%|
|||||||||||+26%|+26%|+26%|+33|+33|+33|
|||||||||||||||||
|||||||||||||||||
|||||||||||||||||



**Figure 4 CaT and CaT-RL improve models by up to** _∼_ **30% relative to the initial policy.** Initial describes the initial policy
model’s performance. Error bars are standard error.


compare rubric rewards to (i) model-as-judge semantic equivalence to the reference and (ii) expert (physician)
rubrics on HealthBench. **RQ4.** _Does CaT improve over single-sample and selection baselines?_ We compare
against several alternatives at inference-time to compare teacher signals.


Mechanism Analysis: **RQ6.** _Does CaT act as a new rollout or leverage the reasoning of rollouts in context?_
We compare CaT with a single rollout in context vs eight to see if it uses information across rollouts. **RQ7.**
_Does CaT reconcile rather than select?_ We analyse disagreement with majority vote and cases where CaT is
correct despite all rollouts being wrong.


**4.1** **Results**


**Result 1: CaT-RL improves over the initial policy and outperforms inference-time CaT (Figure 4).** Thus, CaT
provides an effective teacher signal to go beyond the initial policy’s performance and CaT-RL leverages it in
both verifiable and non-verifiable domains. Except for Qwen 3 4B on math, CaT-RL even improves over the
initial teacher signal given by the reference estimates from CaT. Therefore, CaT-RL leads to a virtuous cycle
of improving the policy, which improves the estimated reference, which further improves the policy.


Nevertheless, improving beyond the initial estimated reference does not imply arbitrary improvement is
possible. After some time, the estimated reference is no longer a significant improvement over policy rollouts
(Appendix B). At this point, the _useful diversity_ among rollouts is insufficient to synthesize a better estimated
reference. This is a known phenomena in RL post-training where generation entropy reduces as the model
improves (Yue et al., 2025; Song et al., 2025b; Wu et al., 2025; Zhao et al., 2025b). Since CaT resolves
disagreements and omissions to produce better estimated references, it can no longer improve over the
individual rollouts if they tend to agree too much.


**Result 2: Self-proposed rubrics are effective rewards in non-verifiable domains.** Figure 5 (left) shows that selfproposed rubrics outperform model-as-judge and compete with human expert annotations. In model-as-judge,
instead of checking individual rubric criteria, _π_ _J_ checks whether an output is semantically equivalent to
the estimated reference response to provide a binary reward. The physician-annotated rubrics come from
the HealthBench dataset. Our approach consistently outperforms model-as-judge, supporting the view that
rubrics provide fine-grained assessment criteria that are easier to verify, and therefore are better reward signals
than course model judgments. Finally, our approach is competitive with even the human annotation baseline,
outperforming it on Gemma 3 4B and achieving comparable performance on Qwen 3 4B and Llama 3.1 8B.


**Result 3: RL with self-proposed rubrics (CaT-RL) is better than SFT.** Although SFT is the _de facto_ method
for fine-tuning with non-verifiable outputs, in Figure 5 (right), we show that RL is better when rewards
are derived from self-proposed rubrics. CaT-SFT describes fine-tuning the model with estimated reference


7


|Col1|Col2|Col3|Col4|%|Col6|Col7|Col8|Col9|Col10|Col11|
|---|---|---|---|---|---|---|---|---|---|---|
|||||1%|1%|1%|1%|1%|%|%|
||-10%<br>-10%<br>|-10%<br>-10%<br>|-10%<br>-10%<br>|-5%<br>+|-5%<br>+|-5%<br>+|-5%<br>+|-5%<br>+|+7|+7|
||||||||||||
|||||||||-53%|||
||||||||||||
||||||||||||
||||||||||||


|Col1|Col2|CaT-RL|Col4|Col5|CaT-SFT|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||||||
|||-15%|-15%|-15%|-9%|-9%|-9%|||
|||||||||-25%|-25%|
|||||||||||
|||||||||||
|||||||||||
|||||||||||



**Figure 5 Left: CaT-RL’s self-proposed rubrics compete with expert human rubrics.** We compare reward mechanisms for
non-verifiable domains: self-proposed rubrics (CaT-RL), physician-annotated rubrics, and an LLM-as-judge that checks
if the rollout is semantically equivalent to the estimated reference response. **Right: RL with rubrics is better than SFT.**
CaT-SFT fine-tunes a model using CaT estimated reference responses generated over the training dataset offline.


responses generated through CaT. CaT-RL always leads to better results. This is consistent with Gunjal
et al. (2025), who also find rubric rewards perform better than SFT on HealthBench. However, our insight is
that these rubrics can be self-proposed from our own estimated reference responses and that RL with these
rewards is still better than SFT.


**Result 4: CaT produces better reference estimates than single-sample and selection baselines.** In Figure 6, we
compare to alternatives at inference-time and show that CaT produces the strongest reference estimates and
is most versatile. _Single_ is a single-sample baseline representing one rollout response. Among alternatives,
self-selected best-of- _N_ _(Self-BoN)_, is a self-proposed baseline in which the model selects its own best response.
In _min(PPL)_, we select the response with the lowest trajectory perplexity under the model. This reflects
prior work on trajectory-level confidence maximization and entropy minimization, e.g., Agarwal et al. (2025)
and Li et al. (2025). In mutual predictability _(MP)_ (Wen et al., 2025), we select the rollout with the highest
probability when the model is conditioned on all other responses. Finally, _Majority_ represents the most
common answer (Wang et al., 2023a; Zuo et al., 2025) and is only well-defined in verifiable tasks. CaT











|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||


**Figure 6 CaT at inference outperforms alternatives.** CaT improves 12.5% on HealthBench and 27% on MATH-500. We
compare CaT against alternative methods of leveraging eight rollouts which are described in detail in Section 4.1.
Percentage improvement is relative to one sample (Single).


8


|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|
|---|---|---|---|---|---|---|---|---|
||||||||||
|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|
|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|~~0.85~~|||
||||||||||
|0.80<br>~~0.81~~|0.80<br>~~0.81~~|0.80<br>~~0.81~~|0.80<br>~~0.81~~|0.80<br>~~0.81~~|0.80<br>~~0.81~~|0.80<br>~~0.81~~|||
|0.80<br>~~0.81~~|0.80<br>~~0.81~~|0.80<br>~~0.81~~|0.80<br>~~0.81~~|0.80<br>~~0.81~~|||||
|~~0.79~~|~~0.79~~|~~0.79~~|||||||
|~~0.79~~|||||||||
||||||||||
||||||||||



**Figure 7 Left: CaT scales with the number of rollouts in context. Right: CaT reconciles rollouts rather than acting as a new**
**rollout.** Results generated with Gemma 3 4B and Qwen 3 4B respectively. For the right figure, brackets indicate the
number of rollouts in context.


is superior to all baselines, thus providing the strongest teacher signal, and works across verifiable and
non-verifiable domains.


**Result 5: CaT scales with the number of rollouts** _G_ **.** Figure 7 (left) shows that on MATH-500, scaling is
monotonic, while on HealthBench, CaT plateaus after around 4 rollouts. This plateau could be explained by
the increasing difficulty of extracting further useful omissions across more freeform rollouts. Since CaT can
scale with rollouts, if GRPO uses a large _G_, then CaT-RL can leverage the improved estimated reference for
_free_ from these rollouts and needs only to encode the additional rollout tokens.


**Result 6: CaT reasons about prior rollouts rather than acting as another rollout.** In Figure 7 (right), we show
that CaT improves results as it meaningfully uses past exploration. CaT with a single rollout in context
performs only mildly better than the single rollout itself. This suggests that the additional generation step of
synthesizing is not acting only as a new rollout that self-conditions with its past context. Instead, because CaT
(a) improves only slightly on a single generation with a single rollout in context and (b) with multiple rollouts
it outperforms majority voting, it must be resolving omissions, disagreements, and reconciling reasoning
patterns in the rollouts that it uses. It is not improving by simply generating another rollout.


**Result 7: CaT reconciles rather than selects to disagree with consensus.** We show that CaT can disagree with
majority consensus and even disagree with all rollouts. Analyzing MATH-500 results for simplicity, although
CaT uses all rollouts in context, it does not always select the consensus answer, disagreeing with majority
voting on 14% of questions. This allows CaT to exceed the performance of majority voting. Rather remarkably,
we observed that CaT occasionally produces correct answers that disagree with all of the rollouts it was
conditioned on, occurring for around 1% of questions. This kind of self-correction, outside of the distribution
of rollout answers, is impossible with a selection method like best-of- _N_ or majority voting.
_(see Appendix A for an example)_

### **5 Discussion**


**Limitations & Future Work.** CaT depends on the initial policy to meaningfully estimate reference answers; for
weak base models or completely unknown domains, synthesis may fail to produce improvements. We observe
a dynamic where improvement plateaus as the policy converges and rollout diversity decreases; since CaT
relies on resolving disagreements between rollouts, increasingly similar outputs lessen improvement from the
estimated reference, and therefore weaken the teacher signal in CaT-RL. An opportunity for future work is to
generate more diverse rollouts through sampling or exploration rewards, e.g., Song et al. (2025a), to enable


9


CaT-RL to improve for longer. While our approach learns without references, it uses existing datasets for
questions. Self-proposed questions, e.g., AbsoluteZero (Zhao et al., 2025a), or automated question extraction,
e.g., Source2Synth (Lupidi et al., 2024), could eliminate human constructed or curated data. CaT may be
naturally extended to synthesize over thinking and reasoning traces rather than only question responses and
chain of thought. Finally, synthesis is just one way of estimating a reference answer; CaT-RL opens the door
to reference-free training with task-specific reference estimation strategies.


**Conclusion.** We present Compute as Teacher (CaT), a method that turns inference compute into supervision
by using an anchor policy to synthesize parallel LLM policy rollouts into estimated reference answers. We
then convert the estimated references into rewards: using programmatic checkers for verifiable tasks, and
the model’s self-proposed rubrics for non-verifiable ones. With training, CaT-RL delivers up to 33% relative
improvement on MATH-500 and 30% on HealthBench with Llama 3.1 8B, and large gains across two other
model families without human annotations. CaT outperforms single sample and selection baselines like
majority voting. We also show using self-proposed rubric rewards works better than SFT in non-verifiable
domains. CaT-RL demonstrates virtuous circle dynamics where better policies generate better rollouts, which
enables better reference estimates, improving the policy further until the supervision signal from the reference
estimates no longer exceeds the performance of the policy rollouts.


We conclude that inference compute can generate meaningful supervision. As annotation becomes the
bottleneck for specialized model development, Compute as Teacher provides a solution for both verifiable and
non-verifiable domains where reference answers are scarce, expensive, contested, or even unknown. By going
beyond human reference texts, using compute to generate supervision may suggest a path toward superhuman
capabilities beyond the limits of human data.


10


### **Acknowledgements**

In alphabetical order, we would like to thank the following people: Joseph Brennan for assistance with rubric
data, Lovish Madaan for various technical assistance, Nicola Cancedda for feedback on institutional approval
processes, Stéphane Collot for guidance on rubric generation, Yonatan Gideoni for comments on a draft of
this work, and Yunzhen Feng for general technical advice.


DJ was an intern at Meta at the time of this work and is supported by an AWS Studentship from the EPSRC
Centre for Doctoral Training in Autonomous Intelligent Machines and Systems (AIMS) (EP/S024050/1).

### **References**


Shivam Agarwal, Zimin Zhang, Lifan Yuan, Jiawei Han, and Hao Peng. The unreasonable effectiveness of entropy
minimization in LLM reasoning. _arXiv preprint arXiv:2505.15134_, 2025.


Rahul K Arora, Jason Wei, Rebecca Soskin Hicks, Preston Bowman, Joaquin Quiñonero-Candela, Foivos Tsimpourlas,
Michael Sharman, Meghan Shah, Andrea Vallone, Alex Beutel, et al. HealthBench: Evaluating large language
models towards improved human health. _arXiv preprint arXiv:2505.08775_, 2025.


Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna
Goldie, Azalia Mirhoseini, Cameron McKinnon, et al. Constitutional AI: Harmlessness from AI feedback. _arXiv_
_preprint arXiv:2212.08073_, 2022.


Zitian Gao, Lynx Chen, Joey Zhou, and Bryan Dai. One-shot entropy minimization. _arXiv preprint arXiv:2505.20282_,

2025.


Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha
Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al. The Llama 3 herd of models. _arXiv preprint_
_arXiv:2407.21783_, 2024.


Anisha Gunjal, Anthony Wang, Elaine Lau, Vaskar Nath, Bing Liu, and Sean Hendryx. Rubrics as Rewards:
Reinforcement learning beyond verifiable domains. _arXiv preprint arXiv:2507.17746_, 2025.


Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset. In _Proceedings of the_
_Neural Information Processing Systems Track on Datasets and Benchmarks 1, NeurIPS Datasets and Bench-_
_marks 2021, December 2021, virtual_, 2021. [https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/be83ab3ecd0db773eb2dc1b0a17836a1-Abstract-round2.html)

[be83ab3ecd0db773eb2dc1b0a17836a1-Abstract-round2.html.](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/be83ab3ecd0db773eb2dc1b0a17836a1-Abstract-round2.html)


Geoffrey Hinton, Oriol Vinyals, and Jeff Dean. Distilling the knowledge in a neural network. _arXiv preprint_
_arXiv:1503.02531_, 2015.


Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu
Chen. LoRA: Low-rank adaptation of large language models. In _The Tenth International Conference on Learning_
_Representations, ICLR 2022, Virtual Event, April 25-29, 2022_ . OpenReview.net, 2022. [https://openreview.net/](https://openreview.net/forum?id=nZeVKeeFYf9)

[forum?id=nZeVKeeFYf9.](https://openreview.net/forum?id=nZeVKeeFYf9)


Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila
Welihinda, Alan Hayes, Alec Radford, et al. GPT-4o system card. _arXiv preprint arXiv:2410.21276_, 2024.


Aishwarya Kamath, Johan Ferret, Shreya Pathak, Nino Vieillard, Ramona Merhej, Sarah Perrin, Tatiana Matejovicova,
Alexandre Ramé, Morgane Rivière, et al. Gemma 3 technical report. _arXiv preprint arXiv:2503.19786_, 2025.


Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brahman, Lester James V
Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, et al. Tulu 3: Pushing frontiers in open language model post-training.
_arXiv preprint arXiv:2411.15124_, 2024.


Pengyi Li, Matvey Skripkin, Alexander Zubrey, Andrey Kuznetsov, and Ivan Oseledets. Confidence Is All You Need:
Few-shot rl fine-tuning of language models. _arXiv preprint arXiv:2506.06395_, 2025.


Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. In _7th International Conference on_
_Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ . OpenReview.net, 2019. [https:](https://openreview.net/forum?id=Bkg6RiCqY7)
[//openreview.net/forum?id=Bkg6RiCqY7.](https://openreview.net/forum?id=Bkg6RiCqY7)


11


Alisia Lupidi, Carlos Gemmell, Nicola Cancedda, Jane Dwivedi-Yu, Jason Weston, Jakob Foerster, Roberta Raileanu,
and Maria Lomeli. Source2Synth: Synthetic data generation and curation grounded in real data sources. _arXiv_
_preprint arXiv:2409.08239_, 2024.


Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang,
Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F. Christiano, Jan Leike, and Ryan Lowe. Training language models to follow instructions with human feedback. In _Advances in Neural Information Processing_
_Systems 35:_ _Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Or-_
_leans, LA, USA, November 28 - December 9, 2022_, 2022. [http://papers.nips.cc/paper_files/paper/2022/hash/](http://papers.nips.cc/paper_files/paper/2022/hash/b1efde53be364a73914f58805a001731-Abstract-Conference.html)

[b1efde53be364a73914f58805a001731-Abstract-Conference.html.](http://papers.nips.cc/paper_files/paper/2022/hash/b1efde53be364a73914f58805a001731-Abstract-Conference.html)


Samuel J Paech. EQ-Bench: An emotional intelligence benchmark for large language models. _arXiv preprint_
_arXiv:2312.06281_, 2023.


Karl Pearson. LIII. On lines and planes of closest fit to systems of points in space. _The London, Edinburgh, and Dublin_
_philosophical magazine and journal of science_, 2(11):559–572, 1901.


Mihir Prabhudesai, Lili Chen, Alex Ippoliti, Katerina Fragkiadaki, Hao Liu, and Deepak Pathak. Maximizing confidence
alone improves reasoning. _arXiv preprint arXiv:2505.22660_, 2025.


Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He. ZeRO: memory optimizations toward training
trillion parameter models. In _Proceedings of the International Conference for High Performance Computing,_
_Networking, Storage and Analysis, SC 2020, Virtual Event / Atlanta, Georgia, USA, November 9-19, 2020_, page 20.
[IEEE/ACM, 2020. doi: 10.1109/SC41405.2020.00024. https://doi.org/10.1109/SC41405.2020.00024.](https://doi.org/10.1109/SC41405.2020.00024)


Stephen Roller, Y-Lan Boureau, Jason Weston, Antoine Bordes, Emily Dinan, Angela Fan, David Gunning, Da Ju,
Margaret Li, Spencer Poff, et al. Open-domain conversational agents: Current progress, open problems, and future
directions. _arXiv preprint arXiv:2006.12442_, 2020.


Jürgen Schmidhuber. Exploring the predictable. In _Advances in evolutionary computing: theory and applications_,
pages 579–612. Springer, 2003.


Jürgen Schmidhuber. PowerPlay: Training an increasingly general problem solver by continually searching for the
simplest still unsolvable problem. _Frontiers in psychology_, 4:313, 2013.


John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization
algorithms. _arXiv preprint arXiv:1707.06347_, 2017.


Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li,
Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv_
_preprint arXiv:2402.03300_, 2024.


Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and
Chuan Wu. HybridFlow: A flexible and efficient RLHF framework. _arXiv preprint arXiv: 2409.19256_, 2024.


David Silver, Aja Huang, Chris J Maddison, Arthur Guez, Laurent Sifre, George Van Den Driessche, Julian Schrittwieser,
Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, et al. Mastering the game of Go with deep neural
networks and tree search. _Nature_, 529(7587):484–489, 2016.


David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur Guez, Marc Lanctot,
Laurent Sifre, Dharshan Kumaran, Thore Graepel, et al. A general reinforcement learning algorithm that masters
chess, shogi, and Go through self-play. _Science_, 362(6419):1140–1144, 2018.


Yuda Song, Julia Kempe, and Remi Munos. Outcome-based exploration for LLM reasoning. _arXiv preprint_
_arXiv:2509.06941_, 2025a.


Yuda Song, Hanlin Zhang, Carson Eisenach, Sham M. Kakade, Dean P. Foster, and Udaya Ghai. Mind the Gap:
Examining the self-improvement capabilities of large language models. In _The Thirteenth International Conference on_
_Learning Representations, ICLR 2025, Singapore, April 24-28, 2025_ . OpenReview.net, 2025b. [https://openreview.](https://openreview.net/forum?id=mtJSMcF3ek)
[net/forum?id=mtJSMcF3ek.](https://openreview.net/forum?id=mtJSMcF3ek)


Yunhao Tang, Sid Wang, Lovish Madaan, and Rémi Munos. Beyond Verifiable Rewards: Scaling reinforcement learning
for language models to unverifiable data. _arXiv preprint arXiv:2503.19618_, 2025.


Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, and
Denny Zhou. Self-consistency improves chain of thought reasoning in language models. In _The Eleventh International_


12


_Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023_ . OpenReview.net, 2023a.

[https://openreview.net/forum?id=1PL1NIMMrw.](https://openreview.net/forum?id=1PL1NIMMrw)


Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A. Smith, Daniel Khashabi, and Hannaneh Hajishirzi.
Self-instruct: Aligning language models with self-generated instructions. In _Proceedings of the 61st Annual Meeting_
_of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2023, Toronto, Canada, July 9-14,_
_2023_, pages 13484–13508. Association for Computational Linguistics, 2023b. doi: 10.18653/V1/2023.ACL-LONG.754.

[https://doi.org/10.18653/v1/2023.acl-long.754.](https://doi.org/10.18653/v1/2023.acl-long.754)


Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M. Dai, and
Quoc V. Le. Finetuned language models are zero-shot learners. In _The Tenth International Conference on Learning_
_Representations, ICLR 2022, Virtual Event, April 25-29, 2022_ . OpenReview.net, 2022. [https://openreview.net/](https://openreview.net/forum?id=gEZrGCozdqR)
[forum?id=gEZrGCozdqR.](https://openreview.net/forum?id=gEZrGCozdqR)


Jiaxin Wen, Zachary Ankner, Arushi Somani, Peter Hase, Samuel Marks, Jacob Goldman-Wetzler, Linda Petrini, Henry
Sleight, Collin Burns, He He, et al. Unsupervised elicitation of language models. _arXiv preprint arXiv:2506.10139_,

2025.


Fang Wu, Weihao Xuan, Ximing Lu, Zaid Harchaoui, and Yejin Choi. The invisible leash: Why RLVR may not escape
its origin. _arXiv preprint arXiv:2507.14843_, 2025.


An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chengen Huang,
Chenxu Lv, et al. Qwen3 technical report. _arXiv preprint arXiv:2505.09388_, 2025.


Tianyu Yu, Bo Ji, Shouli Wang, Shu Yao, Zefan Wang, Ganqu Cui, Lifan Yuan, Ning Ding, Yuan Yao, Zhiyuan Liu,
et al. RLPR: Extrapolating RLVR to general domains without verifiers. _arXiv preprint arXiv:2506.18254_, 2025.


Yang Yue, Zhiqi Chen, Rui Lu, Andrew Zhao, Zhaokai Wang, Shiji Song, and Gao Huang. Does reinforcement learning
really incentivize reasoning capacity in LLMs beyond the base model? _arXiv preprint arXiv:2504.13837_, 2025.


Eric Zelikman, Georges Harik, Yijia Shao, Varuna Jayasiri, Nick Haber, and Noah D Goodman. Quiet-STaR: Language
models can teach themselves to think before speaking. _arXiv preprint arXiv:2403.09629_, 2024.


Andrew Zhao, Yiran Wu, Yang Yue, Tong Wu, Quentin Xu, Matthieu Lin, Shenzhi Wang, Qingyun Wu, Zilong Zheng,
and Gao Huang. Absolute Zero: Reinforced self-play reasoning with zero data. _arXiv preprint arXiv:2505.03335_,

2025a.


Rosie Zhao, Alexandru Meterez, Sham M. Kakade, Cengiz Pehlevan, Samy Jelassi, and Eran Malach. Echo chamber:
RL post-training amplifies behaviors learned in pretraining. In _Second Conference on Language Modeling_, 2025b.
[https://openreview.net/forum?id=dp4KWuSDzj.](https://openreview.net/forum?id=dp4KWuSDzj)


Xuandong Zhao, Zhewei Kang, Aosong Feng, Sergey Levine, and Dawn Song. Learning to reason without external
rewards. _arXiv preprint arXiv:2505.19590_, 2025c.


Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin,
Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. In _Advances in Neural Information Process-_
_ing Systems 36:_ _Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New_
_Orleans, LA, USA, December 10 - 16, 2023_, 2023. [http://papers.nips.cc/paper_files/paper/2023/hash/](http://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)

[91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html.](http://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html)


Xiangxin Zhou, Zichen Liu, Anya Sims, Haonan Wang, Tianyu Pang, Chongxuan Li, Liang Wang, Min Lin, and Chao
Du. Reinforcing general reasoning without verifiers. _arXiv preprint arXiv:2505.21493_, 2025.


Yuxin Zuo, Kaiyan Zhang, Li Sheng, Shang Qu, Ganqu Cui, Xuekai Zhu, Haozhan Li, Yuchen Zhang, Xinwei Long,
Ermo Hua, et al. TTRL: Test-time reinforcement learning. _arXiv preprint arXiv:2504.16084_, 2025.


13


## **Appendix**

### **A Example: CaT Disagrees With All Rollouts**

Disagreement with all rollouts occurs across all models. The following is one among a few examples discovered
with Gemma 3 4B on the MATH-500 dataset.





All rollouts failed to provide the correct answer, exhibiting calculation errors. The following is an example
from the second rollout which did not compute a division correctly:



















In another example, the sixth rollout made several calculation errors, inexplicably multiplying and dividing
by 137 and 1 around the same place as the second rollout:













Despite this, the synthesized response identified these errors, used the correct reasoning and provided the
right final response. Since the individual rollouts failed to find the correct answer, finding the right method
would not be easy for the model without observing these attempts.

### **B When Does CaT-RL Stop Learning?**









|78%|Col2|82%<br>78%|Col4|Col5|83%|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|||||||56%|56%|58%|58%|
|||||||||||
|||||||||||
|||||||||||


**Figure 8 The trained model’s teacher signal is not much stronger than the policy.** CaT-RL is the trained model and CaT-RL
+ CaT denotes applying synthesis with the trained model (i.e., the teacher signal at the end of training). Error bars
are standard error.


In Figure 8, we compare the trained policy to if we apply CaT at inference-time to the trained policy. The
latter is the final teacher signal in CaT-RL. At this point, we note that the teacher signal is very close to the
trained policy’s performance. Therefore, the model is unable to continue improving as the teacher provides
no, or very little, delta to improve.


14


Since CaT’s synthesis step improves upon the group rollouts by resolving contradictions, synthesizing partial
solutions, and inserting omissions, if it does not improve, then this indicates that the group rollouts are
generally in agreement. Here, we note that the model has gone from generating diverse solutions when it
was less capable to generating less diverse, but more likely solutions when it has been trained to be more
capable at solving the task. This is a commonly observed issue in RL fine-tuning (Yue et al., 2025; Song et al.,
2025b; Wu et al., 2025; Zhao et al., 2025b). Its presence here places a bound on the potential reference-free
improvement that can be achieved via CaT-RL.

### **C Prompts**


We provide two prompts for exploration synthesis. We use the Freeform Synthesis Prompt for HealthBench
questions, and the COT/Reasoning Synthesis Prompt for math questions.





15


16


17


18


### **D Example Rubrics**

All examples in this section were generated from Qwen 3 4B on the HealthBench dataset.







19


### **E Hyperparameters**

We provide RL training parameters in Table 1, SFT training parameters in Table 2, and model sampling
parameters in Table 3. We use the verl library (Sheng et al., 2024) for both RL and SFT. We also note that
we apply a length penalty of _−_ 1 to responses longer than 750 tokens when training with HealthBench to
discourage length-based reward hacking.


Parameter Value


Algorithm GRPO (Shao et al., 2024)
Rollouts per prompt 8
Learning rate 5 _×_ 10 _[−]_ [7]

Learning rate schedule Constant with no warmup
Global batch size 256
Reward-level KL coefficient 1 _×_ 10 _[−]_ [3]

Max. training steps 1000
Max. gen. tokens (HealthBench) 1024
Max. gen. tokens (MATH-500) 1536
Training GPUs 8 _×_ NVIDIA H100s
_π_ _J_ GPT-4o (Hurst et al., 2024)
Optimiser AdamW (Loshchilov and Hutter, 2019)
Parallelism Strategy FSDP (Rajbhandari et al., 2020)


**Table 1** Shared RL training hyperparameters. Note that we use the PyTorch FSDP implementation as provided in verl.
[See https://docs.pytorch.org/docs/stable/fsdp.html.](https://docs.pytorch.org/docs/stable/fsdp.html)


Parameter Value


Batch size 32

CaT rollouts in context 8
Learning rate 5 _×_ 10 _[−]_ [5]

Learning rate schedule Cosine with warmup
LoRA (Hu et al., 2022) Rank 32
Optimizer AdamW (Loshchilov and Hutter, 2019)


**Table 2** Shared SFT training hyperparameters.


20


Model Parameter Value


Gemma 3 4B Temperature 1 _._ 0
Top- _k_ 64
Top- _p_ 0 _._ 95


Qwen 3 4B Temperature 0 _._ 7
Top- _k_ 20
Top- _p_ 0 _._ 8


Llama 3.1 8B Temperature 0 _._ 7
Top- _k_ 50
Top- _p_ 0 _._ 9


**Table 3** Model sampling parameters. Where available, we use the standard model sampling parameters recommended
by the model authors. We disable thinking mode in Qwen 3 4B by prefixing all prompts with /no_think.

### **F Experimental Details**


**Computing perplexity.** To compute the perplexity of the output tokens in response to a question, we calculate



�



�



Perplexity( _w_ 1 _, w_ 2 _, . . ., w_ _n_ ) = exp



_−_ [1]



_n_



(10)



_n_
�



� log _p_ ( _w_ _i_ _|w_ 1 _, . . ., w_ _i−_ 1 )


_i_ =1



where _w_ 1 _, w_ 2 _, . . ., w_ _n_ are the output tokens generated by the model. When selecting the best response for
min(PPL), in practice we do not compute the exponential as minimizing entropy is the same as minimizing
perplexity.


**Computing mutual predictability.** For _G_ = 8 rollouts we construct eight prompts, where we pick each rollout
answer in turn to include last in the prompt and randomly order the other answers in the prompt before it.
Then, we encode the prompt with the model and compute the token-level perplexity of the tokens in the final

answer:







(11)




PPL( _a_ _j_ ) = exp







_−_ [1]
 _|a_



_|a_ _j_ _|_



_|a_ _j_ _|_
�



� log _p_ ( _w_ _t_ [(] _[j]_ [)] _[|]_ [context] _[, a]_ _[−][j]_ _[, w]_ 1 [(] _[j]_ [)] _[, . . ., w]_ _t_ [(] _−_ _[j]_ [)] 1 [)]


_t_ =1



where _a_ _j_ is the _j_ -th answer, _|a_ _j_ _|_ is its length in tokens, _w_ _t_ [(] _[j]_ [)] is the _t_ -th token of answer _j_, and _a_ _−j_ represents
the other answers included in the context. We pick the answer with the lowest perplexity as the best response:


_a_ _[∗]_ = arg min (12)
_j∈{_ 1 _,...,G}_ [PPL][(] _[a]_ _[j]_ [)]


**Supervised fine-tuning.** For our SFT experiments, we generate _G_ = 8 rollouts with the initial policy _π_ 0
over our HealthBench training and validation splits. Then, we use the same initial policy to synthesize the
rollouts per question into a synthesized estimated reference response _s_ . We then fine-tune the model with the
estimated reference responses as targets by minimizing the cross-entropy loss







(13)




_L_ SFT = _−_ E ( _q,s_ ) _∼D_







 _|_ [1] _s|_



_|s|_



_|s|_
�



� log _π_ _θ_ ( _s_ _t_ _|q, s_ _<t_ )


_t_ =1



where _q_ is the input question, _s_ is the estimated reference response, _s_ _t_ is the _t_ -th token of the reference
response, and _D_ is the training dataset. We use early stopping, using the checkpoint with the lowest validation
loss to evaluate the model on the held-out 500-question HealthBench test set. We also note that we train
with LoRA (Hu et al., 2022) due to fast overfitting and worse results with full parameter fine-tuning.


21


**RL fine-tuning.** Much of the detail for RL fine-tuning is described in the main body and other appendices.
Here, we note that for math data, we extract a verifiable final answer from boxed text, e.g., boxed{...}, using
regular expressions and string matching where we have instructed the model to give its final answer in this
form. To extract rubric judgments and rubric generations, we instruct the model to output its answer in XML
format [3] and use a standard XML tree parser to extract the result. When RL fine-tuning with HealthBench,
we use early stopping, evaluating the test set with the checkpoint that yielded the best validation score. For
math, since we use the test-time reinforcement learning setting (Zuo et al., 2025), we train for a fixed number
of steps.


**Synthesis.** We note that in the synthesis step, we do not include the task prompt or question in the estimator’s
prompt because it did not make a difference in preliminary inference-time experiments with Gemma 3 4B on
MATH-500 (+0 _._ 004). Excluding the task prompt simplifies the setup and makes no meaningful difference to
performance.


3 [See the prompts in Appendix C and https://www.w3.org/TR/xml/.](https://www.w3.org/TR/xml/)


22


