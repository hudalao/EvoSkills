Preprint

## M AGIC M IRROR : A L ARGE -S CALE D ATASET AND - B ENCHMARK FOR F INE -G RAINED A RTIFACTS A S - SESSMENT IN T EXT TO -I MAGE G ENERATION


**Jia Wang** [1] _[,]_ [2] **Jie Hu** [2] _[∗]_ **Xiaoqi Ma** [2] **Hanghang Ma** [2] **Yanbing Zeng** [2] **Xiaoming Wei** [2]

1 University of Chinese Academy of Sciences 2 Meituan
_{_ wangj.infinite, hujiemr _}_ @gmail.com


A BSTRACT


Text-to-image (T2I) generation has achieved remarkable progress in instruction
following and aesthetics. However, a persistent challenge is the prevalence of
physical artifacts, such as anatomical and structural flaws, which severely degrade
perceptual quality and limit application. Given the diversity and complexity of
these artifacts, a systematic and fine-grained evaluation framework is required,
which is lacking in current benchmarks. To fill this gap, we introduce **MagicMir-**
**ror**, a comprehensive framework for artifacts assessment. We first establish a detailed taxonomy of generated image artifacts. Guided by this taxonomy, we manually annotate **MagicData340K**, the first human-annotated large-scale dataset of
340K generated images with fine-grained artifact labels. Building on this dataset,
we train **MagicAssessor**, a Vision-Language Model (VLM) that provides detailed
assessments and corresponding labels. To overcome challenges like class imbalance and reward hacking, we design a novel data sampling strategy and a multilevel reward system for Group Relative Policy Optimization (GRPO). Finally, we
leverage MagicAssessor to construct **MagicBench**, an automated benchmark for
evaluating the image artifacts of current T2I models. Our evaluation with MagicBench reveals that despite their widespread adoption, even top-tier models like
GPT-image-1 are consistently plagued by significant artifacts, highlighting artifact reduction as a critical frontier for future T2I development. Project page:
[https://wj-inf.github.io/MagicMirror-page/.](https://wj-inf.github.io/MagicMirror-page/)


1 I NTRODUCTION


Diffusion-based text-to-image (T2I) models (Saharia et al., 2022; Rombach et al., 2022; Podell et al.,
2023; Labs, 2024) have achieved remarkable advancements in image quality, instruction following,
and aesthetics. These capabilities have unlocked practical applications in specialized domains, from
photorealistic portraiture (midjourney team, 2024) to graphic design (Gao et al., 2025a; Hu et al.,
2025). Yet, this progress is often challenged by a persistent and fundamental problem: the generation
of physical artifacts (Xu et al., 2023; Liang et al., 2024). From incorrect limb counts (Zhu et al.,
2024) to distorted shapes, these artifacts represent a fundamental challenge to the models’ reliability.
They lower the output’s visual quality, require repeated manual correction, and ultimately limit the
models’ widespread use in real-world situations.


The persistence of these artifacts can be attributed to the historical focus of T2I evaluation, which
traditionally prioritized two main areas: image quality (measured by text-agnostic metrics like
IS (Salimans et al., 2016) and FID (Heusel et al., 2017)), and semantic alignment (assessed with
instruction-following benchmarks (Ghosh et al., 2023; Huang et al., 2023; Hu et al., 2024)). More
recently, aligning with human preferences is gradually taken into consideration (Kirstain et al., 2023;
Xu et al., 2023; Wu et al., 2023b;a), with a significant emphasis on aesthetics (Zhou et al., 2024;
Liao et al., 2025). However, while human preference evaluations implicitly consider artifacts, this
aspect is not a primary focus and is typically captured only indirectly through an annotator’s overall

score.


_∗_ Corresponding author.


1


Preprint


Lables: L2: Abnormal Object Morphology
T2I_prompt: BMW isetta in dark souls



Model output: <think>
Upon examining the image, the primary subject is a BMW Isetta, which is a classic car known for its unique and compact
design. The setting appears to be a forested area, which aligns with the “Dark Souls” theme, a game known for its atmospheric
and often eerie environments. The lighting in the image is consistent with the sun filtering through the trees, creating a warm
and inviting atmosphere.
The car itself is depicted with a realistic texture and color, matching the expected appearance of a BMW Isetta. However,
upon closer inspection, there is a noticeable issue with the car's rearview mirror. It appears to be missing or not properly
attached, which is an abnormality in the object's morphology. This kind of deformity falls under the category of “Abnormal
Object Morphology”, as the car's structure does not conform to the expected design.
No other elements in the image, such as the trees, lighting, or road, appear to have any abnormalities. The proportions and
interactions between elements seem reasonable, and there are no human or animal figures present to consider for anatomical
abnormalities. Therefore, the primary concern is the car's mirror, which is not functioning as it should.
Given this analysis, the image is not entirely reasonable due to the deformity in the car's rearview mirror.</think>
\boxed{{“Whether Normal”: false, “Type of Deformity”: {“L2: Abnormal Object Morphology”: true}}}


Figure 1: An output example of MagicAssessor-7B.



In response to this gap, several recent studies have begun to concentrate more specifically on the
task of identifying artifacts. For instance, while RichHF (Liang et al., 2024) introduces plausibility
scores, its approach to artifacts is coarse-grained, labeling all defects with undifferentiated dots.
This makes it impossible to distinguish between different error types. Furthermore, its dataset’s
limited scale (RichHF-18K) and reliance on older T2I models (before the original text-image pairs
dataset Pick-a-Pic (Kirstain et al., 2023)) result in a scarcity of positive examples for challenging
subjects, such as anatomically correct hands, hindering effective learning. On the other hand, while
subsequent works like HEIE (Yang et al., 2025) and FakeVLM (Wen et al., 2025) have explored
generating textual explanations for defects, their reliance on standard Supervised Fine-Tuning (SFT)
is inherently limited by token-level supervision, which can restrict the flexibility and quality of the
model’s reasoning. Taken together, these limitations highlight a clear need for a more granular,
scalable, and robustly trained evaluation framework.


To address this gap, we introduce **MagicMirror**, a complete framework for systematically evaluating image artifacts. The foundation of our work is a novel, fine-grained taxonomy that categorizes artifacts into three primary groups: _object anatomy_, _attribute_, and _interaction_ . Guided by
this taxonomy, we construct **MagicData340K**, the first human-annotated large-scale dataset with
fine-grained labels in this field. This involves collecting diverse prompts (Kirstain et al., 2023), generating approximately 340K images from various advanced T2I models (Esser et al., 2024; Labs,
2024; midjourney team, 2024), and undertaking a massive human annotation effort to apply our
detailed artifact labels to each image.


Building upon this data foundation, we introduce **MagicAssessor**, a specialized Vision-Language
Model (VLM) trained specifically for artifact assessment, based on Qwen2.5-VL-7B (Bai et al.,
2025). To enhance its performance, we employ Group Relative Policy Optimization (GRPO) (Shao
et al., 2024), which we uniquely adapt to our task through two key innovations: a targeted data
sampling strategy and a multi-level reward system. First, to address the issue of data imbalance, our
data sampling strategy oversamples challenging positive cases, such as anatomically correct hands.
Then, we propose a multi-level reward system, which guides the model from coarse to fine-grained
detection and introduce a novel consistency reward to align the model’s reasoning with its final
output to prevent reward hacking. We show an output example of MagicAssessor in Fig. 1, where
the artifact of the car’s rearview mirror is accurately identified. Finally, we use this powerful assessor
to build **MagicBench**, our automated benchmark. With MagicBench, we can now fairly compare
the image artifacts against various T2I models. Our main contributions are summarized as follows:


1. We develop a comprehensive taxonomy for image artifacts and, guided by it, construct
**MagicData340K**, the first large-scale dataset with fine-grained, human-annotated artifact
labels.


2. We propose **MagicAssessor**, a fine-grained artifact evaluator, along with a novel training
strategy that adapts GRPO with custom data sampling and reward system to overcome
challenges like data imbalance and reward hacking.


3. We build and release **MagicBench**, the first automated benchmark special for evaluating
image artifacts. We leverage it to conduct a systematic analysis of leading T2I models,
providing actionable guidance for future work on artifact reduction.


2


Preprint


Figure 2: The hierarchical taxonomy of image artifacts. Our classification begins by distinguishing
between artifacts of **the subject itself** and **interactions between subjects** . These are further divided
into fine-grained Level 2 (L2) and Level 3 (L3) categories.



(a) L2: Irrational Element

Interaction



(b) L2: Abnormal Human

Anatomy



(e) L2: Irrational Element

Attributes



(c) L2: Abnormal Animal

Anatomy



(d) L2: Abnormal Object

Morphology



Figure 3: Visual examples of artifacts corresponding to our taxonomy.


2 D ATASET


The construction of our dataset follows three main stages. We first establish a fine-grained taxonomy
for image artifacts. Guided by this taxonomy, we manually annotate a large collection of textimage pairs generated from diverse and advanced models. Finally, to enable a cold start for our
model’s step-by-step reasoning, we further annotate a representative subset with localized artifacts
and synthesize detailed textual rationales.


2.1 C LASSIFICATION OF A RTIFACTS


Existing evaluation methods for generated images lack the necessary granularity. They typically fall
into two types: single, coarse-grained scores for metrics like aesthetics or alignment, which offer
limited rationale, or undifferentiated spatial annotations like “artifact region” (Liang et al., 2024),
which fail to distinguish between different types of artifacts. To enable a truly granular assessment,
we propose a multi-label taxonomy that provides a detailed artifact profile for each image.


Our taxonomy is organized hierarchically, as illustrated in Figure 2. We define Normal/Artifact as
Level 1 (L1). At the highest level, we distinguish between artifacts concerning the subject itself and
those involving interactions between subjects. Subject-level issues are further divided into Anatomy
(including human, animal, and object structure) and Attributes (including color and proportion).
These main categories constitute our Level 2 (L2) labels. For critical areas, we define more specific
Level 3 (L3) labels, such as _Hand Structure Deformity_ . Figure 3 provides visual examples of several
L2 artifacts.


2.2 D ATA C OLLECTION


Fig. 4 illustrates the data curation for MagicData340K. The process begins with curating prompts
from diverse sources and generating corresponding images with a suite of T2I models. A comprehensive annotation taxonomy for artifacts is then developed through iterative tests and applied to the
resulting text-image pairs. Finally, a representative subset is selected for fine-grained annotation,
where detailed descriptions for each label are written by humans and used to synthesize Chain-ofThought (CoT) rationales with GPT-4o.


3


Preprint


Text-Image Pairs Collection Human Annotation CoT Data Construction











































Figure 4: Data curation for MagicData340K. The process is divided into three main stages: prompt
collection and image generation, human annotation with multi-labels, and detailed CoT rationale
synthesis for a cold start.


**Collecting Text-Image Pairs.** To construct a diverse dataset, we begin by compiling a large-scale
database of entities, artistic styles, and human attributes from a wide range of sources. We then
curate a set of 50,000 prompts from three primary sources: (1) 23,000 user prompts sampled from
Pick-a-Pic (Kirstain et al., 2023); (2) 23,000 prompts generated by GPT combining entities and artistic styles from our database; and (3) 4,000 prompts specifically targeting human subjects, also composed by GPT using attributes from this resource. We then use this prompt set to generate images
with a diverse suite of T2I models, including FLUX.1-dev/schnell (Labs, 2024), Kolors1.0 (Team,
2024b), SD3.5 (Stability AI, 2024), SD3 (Esser et al., 2024), Midjourney-v6.1 (midjourney team,
2024), and an internal model.


**Human Annotation with Multi-Labels.** After collecting numerous text-image pairs, we start a
multi-stage annotation process. We begin by developing a detailed set of annotation guidelines and
an intuitive interface, which are refined through a pilot study with expert annotators and several cycles of feedback. The final guidelines provide clear definitions and visual examples for each artifact
label, specify the required level of detail, and outline how to handle ambiguous cases (see Appendix A.2 for details). With these robust guidelines, our annotators begin the large-scale labeling
process. To ensure high quality and consistency, experts continuously follow the annotation work
to ensure all rules are followed. Finally, we filter out inappropriate content, resulting in 343,269
annotated text-image pairs. Note that our annotation scheme is designed to assess complex images
that may contain multiple artifacts. While the L1 label is a simple binary choice (Normal vs. Artifact), annotators can assign multiple L2 and L3 labels to a single image to describe all co-occurring
artifacts.


**Chain-of-Thought Data Construction.** To train a model capable of not just detecting but also
explaining image artifacts, we curate a high-quality subset from our annotated data for more detailed
annotation. For each sample in this subset, human annotators provide detailed textual descriptions
for every applied artifact label, specifying the location and nature of the issue. After gathering this
granular information, we feed all data points for a single sample: the original prompt, the generated
image, the artifact labels, and their detailed descriptions into GPT-4o. The model is then prompted
to synthesize this information into a high-quality, step-by-step CoT rationale. Crucially, during this
process, any samples where the initial labels are inaccurate or ambiguous were discarded. This
process ensures the detailed subset maintains high quality, making it suitable for fine-tuning models
on detailed reasoning tasks.


To acquire high-quality CoT data from GPT-4o, we engineer our prompt using two key strategies.
We first prompt the model to follow a structured, four-step reasoning process: _T2I prompt review_, _im-_
_age description_, _element examination_, and _conclusion_ as shown in Fig. 4. Additionally, we employ
an in-context learning (ICL) approach by including a curated example directly within the prompt to
demonstrate the desired output format and reasoning style.


4


Preprint


Percent of labels







Artifact



Normal

Artifact


Normal

50.75%


|L2 labels|Percent of labels|
|---|---|
|L2: Irrational Element Interaction|36.45%|
|L2: Abnormal Human Anatomy|61.53%|
|L2: Abnormal Animal Anatomy|13.84%|
|L2: Abnormal Object Morphology|13.84%|
|L2: Irrational Element Attributes|0.51%|
|L2: Other Irrationalities|0.01%|


|Model|Artifact rate|
|---|---|
|FLUX.1-dev|37.0%|
|Midjourney-v6|42.1%|
|FLUX.1-schnell|42.7%|
|Kolors1.0|51.5%|
|SD3.5|58.5%|
|SD3|60.4%|



(a) Percent of L1 labels (b) Percent of L2 labels (c) Artifact rate of different model


Figure 5: Data statistics of MagicData340K. Note that multiple L2 labels can coexist for a single
image, leading the sum of percentages in (b) is over 100%.


2.3 D ATA S TATISTICS OF M AGIC D ATA 340K


Our statistical analysis of the annotated data is presented in Fig. 5, which shows a nearly even
split between normal images and those containing artifacts. Among the different types of artifacts,
_L2: Abnormal Human Anatomy_ is the most frequent, caused by the complexity of the human body.
Current T2I models often generate images with missing fingers, distorted faces, and unnatural limbs,
which are even more common in multi-person scenarios. Another common issue is _L2: Irrational_
_Element Interaction_, where the most frequent sub-type is _L3: Abnormal Element Overlap_ . These
models struggle to generate clear boundaries between objects, leading to blended or improperly
merged images. As for individual model performance, FLUX.1-dev has a relatively low artifact
rate, with its outputs showing a notably higher success rate in rendering anatomically correct hands.
More details of MagicData340K are shown in Appendix A.2.


3 M ETHODS


3.1 M ODEL T RAINING


The training of our model follows a two-stage pipeline. We begin with a cold start based on our
CoT data to teach our model the expected reasoning process and output format. Then, we enhance
its detection capabilities using GRPO. To optimize the second stage, we introduce the _Multi-Buckets_
_Data Sampling_ strategy to handle class imbalance and the _Multi-level Reward System_ to guide the
model’s learning and mitigate reward hacking.


**Supervised Fine-Tuning with CoT Data.** The experiment results in Table. 1 reveal that existing
open-source VLMs exhibit poor zero-shot abilities on the artifact detection task. This weakness
makes the direct usage of GRPO ineffective: the algorithm works by refining a model’s existing
reasoning, but naive open-source VLMs struggle to locate obvious artifacts in an image. To solve
this, we resort to a cold start strategy (Guo et al., 2025), which is front-loaded by first performing
SFT on the VLM with minimal iterations using our pre-constructed CoT data. Through this process,
the model learns how to generate responses that include a CoT analysis, how to follow our predefined
output format and label taxonomy and, crucially, acquire the fundamental ability to assess artifacts
on generated images.


**Artifacts Recognition Enhancement via GRPO.** Following cold-start, we transition from tokenlevel supervision to sequence-level optimization to enhance the model’s reasoning and detection
accuracy. For this, we employ GRPO, whose objective is to refine the policy model _π_ _θ_ by rewarding
entire generated sequences that are superior to the average quality within a sampled group. For each
question _q_, the optimization objective is formulated as:


_J_ _GRP O_ ( _θ_ ) = E[ _q∼P_ ( _Q_ ) _,{o_ _i_ _}_ _Gi_ =1 _[∼][π]_ _[θ]_ _old_ [(] _[O][|][q]_ [)] []]
_G_ 1 � _Gi_ =1 �min � _π_ _θold_ _π_ _θ_ ( _o_ ( _i_ _o|_ _i_ _q|_ ) _q_ ) _[A]_ _[i]_ _[,]_ [ clip] � _π_ _θold_ _π_ _θ_ ( _o_ ( _o_ _i_ _|_ _i_ _q|q_ )) ~~_[′]_~~ _[,]_ [ 1] _[ −]_ _[ε,]_ [ 1 +] _[ ε]_ � _A_ _i_ � _−_ _β_ D _KL_ ( _π_ _θ_ _||π_ _ref_ )� _,_ (1)


where _G_, _ε_ and _β_ are hyper-parameters, _o_ _i_ is the output from _π_ _θ_ _old_, _π_ _θ_ is the policy model to be optimized, and _A_ _i_ is the advantage, computed using a group of rewards _{R_ 1 _, R_ 2 _, ..., R_ _G_ _}_ corresponding


5


Preprint



Data Sampling Strategy



Reward System


Consistency Reward





Batch VLLM


Figure 6: Data sampling strategy and reward system in model training.



GRPO Loss



to the outputs within each group:


_A_ _i_ = _[R]_ _[i]_ _[ −]_ _[mean]_ [(] _[{][R]_ [1] _[,][ R]_ [2] _[,][ ...][,][ R]_ _[G]_ _[}]_ [)] _._ (2)

_std_ ( _{R_ 1 _, R_ 2 _, ..., R_ _G_ _}_ )


To adapt GRPO for artifacts detection, we design a multi-level reward system to compute _R_ _i_ and a
data sampling strategy, which are detailed below.


**Multi-level Reward System.** A simple reward for outcome correctness is insufficient for our complex, hierarchical task. To provide progressive guidance for our model, we design a multi-level
reward system. Our design is guided by three core principles: enforcing a structured, hierarchical
output format, prioritizing the accuracy of high-level labels over more granular ones, and emphasizing high recall to ensure the model effectively identifies as many artifacts as possible.


Based on these principles, our system computes the final reward _R_, which combines several components. These include a format reward _r_ 0, hierarchical rewards for the L1, L2, and L3 labels
( _r_ 1 _, r_ 2 _, r_ 3 ), and a crucial consistency reward _r_ _c_ that penalizes mismatches between the model’s reasoning and its final output to mitigate reward hacking. For the final reward, higher weights are
given to more fundamental aspects like format and high-level accuracy. The detailed formulation
for each component and the reward calculation are provided in Appendix A.4. The final reward R is
a weighted sum:



_R_ = _r_ _c_ _·_


where _r_ _c_ _, r_ 0 _, r_ 1 _∈{_ 0 _,_ 1 _}_ and _r_ 2 _, r_ 3 _∈_ [0 _,_ 1].



_n_
� 2 _[n][−][l]_ _r_ _l_ _, n_ = 3 _,_ (3)


_l_ =0



**Data Sampling Strategy.** While cold start provides a promising starting point, the resulting VLM
still struggles with the significant class imbalance present in our dataset. A naive application of
GRPO would cause the model to overfit to the most frequent artifact categories such as _L2: Ab-_
_normal Human Anatomy_, leading to poor recall on rarer types. To address this, we introduce a
Multi-Bucket Sampling strategy. For each training batch, we construct a balanced sample by drawing from five distinct buckets: normal images and images corresponding to our four main L2 artifact
labels. These are sampled in a 4:1:1:1:1 ratio in a batch, ensuring less frequent but still important
artifact types are consistently represented during training. For simplicity, the data of the remaining
two L2 labels are omitted from this strategy, which collectively account for less than 1% of the
dataset.


A related challenge is the lack of hard positive samples like anatomically correct human hands,
which models typically struggle to generate properly. Without seeing enough of these correct examples, the model may also fall into reward hacking. It could learn a simple but incorrect rule that _any_
_image containing hands is always artifact_ . To prevent this, we upsample images with these challenging and anatomically correct objects to better teach the model to distinguish between artifact
subjects and correctly formed ones.


6


Preprint


Table 1: Overall performance comparison with other models.

L2 Labels Macro Average L2 Labels Micro Average Artifacts


Precision Recall F1 Precision Recall F1 Precision Recall F1

Qwen2.5-VL-7B 0.3395 0.0995 0.1490 0.3263 0.1130 0.1678 0.5674 0.3597 0.4403

Qwen2.5-VL-32B 0.3808 0.0289 0.0529 0.3256 0.0301 0.0552 0.5511 0.1320 0.2130

InternVL3-8B 0.3528 0.0958 0.1396 0.3043 0.1054 0.1566 0.5345 0.3617 0.4314

InternVL3-38B 0.3662 0.0313 0.0564 0.3433 0.0282 0.0521 0.5483 0.1034 0.1740

GPT-4o 0.4348 0.1410 0.2117 0.4923 0.1623 0.2442 0.6222 0.3189 0.4217

Gemini2.5-flash 0.4356 0.2753 0.3230 0.4440 0.3068 0.3629 0.5734 0.6682 0.6172
Gemini2.5-pro 0.4294 0.3572 0.3638 0.3868 0.3816 0.3842 0.5577 **0.7962** 0.6560
**MagicAssessor-7B** **0.5446** **0.5244** **0.5261** **0.5744** **0.5425** **0.5580** **0.7756** 0.6381 **0.7001**


Table 2: Detailed performance on L2 labels comparison with other models.


L2: Irrational Element Interaction L2: Abnormal Human Anatomy L2: Abnormal Animal Anatomy L2: Abnormal Object Morphology


Precision Recall F1 Precision Recall F1 Precision Recall F1 Precision Recall F1

Qwen2.5-VL-7B 0.2008 0.1180 0.1486 0.6182 0.1358 0.2227 0.4361 0.1005 0.1634 0.1028 0.0436 0.0612

Qwen2.5-VL-32B 0.2372 0.0296 0.0527 0.6167 0.0331 0.0629 0.5641 0.0337 0.0635 0.1054 0.0193 0.0326

InternVL3-8B 0.2032 0.1509 0.1732 0.6272 0.1065 0.1821 0.4545 0.0798 0.1357 0.1263 0.0459 0.0673

InternVL3-38B 0.2268 0.0383 0.0655 0.5702 0.0230 0.0443 0.5282 0.0566 0.1023 0.1398 0.0071 0.0134

GPT-4o 0.2612 0.1148 0.1595 0.7193 0.2215 0.3387 0.5563 0.1836 0.2761 0.2025 0.0440 0.0724

Gemini2.5-flash 0.2784 0.1288 0.1761 0.7257 0.4235 0.5349 0.5513 0.2608 0.3541 0.1871 0.2881 0.2269
Gemini2.5-pro 0.2574 0.2206 0.2375 0.7523 0.4707 0.5791 0.5475 0.3241 0.4072 0.1606 **0.4134** 0.2313
**MagicAssessor-7B** **0.3665** **0.4621** **0.4088** **0.8957** **0.6177** **0.7312** **0.5805** **0.6563** **0.6161** **0.3359** 0.3616 **0.3482**


3.2 A SSESSMENT B ENCHMARK


To objectively evaluate and quantify the artifact rates of current T2I models, we introduce MagicBench, a standardized evaluation framework powered by our trained MagicAssessor model.


**Prompt Construction.** We first construct 800 prompts including single/double/multiple human,
single/multiple animals, and single/multiple/complex object (100 for each). Notice that _L2: Irra-_
_tional Element Interaction_ does not have a specific prompt, as it could be present in the generated
image containing the entity. To ensure diversity, we use an LLM to generate prompts with different
subjects, scenes, photographic styles, and photographic angles, with detail construction process in
Appendix A.7. We also specify in the prompts that the generated image must contain the specified
subject. Each model under evaluation is used to generate one image per prompt.


**Subject Verification.** When testing, we found that some models tend to hide the difficult parts of
the generated subject (e.g., human hands), or even not include any part of the subject. To address
this problem, we highlight it at the end of each prompt and use a general-purpose VLM to perform
automated subject verification, confirming that the main subject specified in the prompt is present in
the image.


**Artifacts Assessment.** For all images that successfully pass subject verification, we apply our
MagicAssessor for a fine-grained artifact analysis. Our scoring process consists of three steps.
Images that do not contain the corresponding subject are considered corresponding artifacts and
excluded from the subsequent artifacts analysis. After that, we label each generated image with our
model. Finally, we give the score according to the model’s performance on our test set. The score is
calculated by:

_N_ _label_
_Score_ _label_ = 100 _·_ (1 _−_ ) _,_ (4)
_N_ _label_ ~~_s_~~ _et_

where the _N_ _label_ is the image numbers with each L2 label or _Artifacts_, _N_ _label_ ~~_s_~~ _et_ is 300 for _Human_,
200 for _Animal_, 300 for _Object_, and 800 for _Interaction_ and _Artifacts_ . Notice that Overall Score in
Table. 3 is the same as _Score_ _artifacts_, representing the performance about whether the generated
images are _Normal_ .


4 E XPERIMENTS


4.1 E XPERIMENTAL SETUP


We develop MagicAssessor by fine-tuning Qwen2.5-VL-7B. Our two-stage training process consists
of an initial SFT on the CoT sub-dataset, followed by GRPO on the resampled MagicData340K
dataset. We evaluate model performance using Precision, Recall, and F1-Score, calculated for both
the overall artifact detection task and for each of our primary L2 categories. All experiments are


7


Preprint


Table 3: Evaluation score ( _↑_ ) on different labels of different models in MagicBench.

Interaction Score Human Score Animal Score Object Score Overall Score
FLUX.1-dev **84.71** **46.00** **44.50** 89.60 **62.16**

Seedream3.0 78.37 41.00 43.00 **90.56** 59.54
Qwen-image 79.01 44.15 40.70 87.85 59.41
Hidream-l1 80.30 39.33 39.50 90.07 58.08

FLUX.1-schnell 79.90 37.67 39.00 86.49 56.03

SD3.5 79.06 39.33 37.50 82.64 54.82

Kolors1.0 82.56 39.46 40.50 75.44 52.82

SD3 73.89 27.00 39.50 80.35 50.06

SDXL 76.02 32.33 39.00 74.30 49.36
GPT-image-1 81.54 45.00 **49.00** **91.41** **63.08**
Bagel **85.96** 41.00 48.00 87.92 60.53
Blip3-o 79.57 **46.33** 43.00 81.27 57.98
Janus-pro 74.14 22.07 32.66 80.84 45.35
Show-o 74.49 23.33 30.50 76.41 44.77


conducted on 32 NVIDIA H800 GPUs. Comprehensive details regarding our dataset and training
hyperparameters are provided in Appendix A.5. In all result tables presented following, we indicate
the best-performing value for each metric in **bold** and the second-best value with underline.


4.2 P ERFORMANCE A NALYSIS


We perform a comprehensive comparison of MagicAssessor-7B against several baseline models,
including Qwen2.5-VL-7B/32B (Bai et al., 2025), InternVL3-8B/38B (Zhu et al., 2025), GPT4o (Achiam et al., 2023), and Gemini2.5-flash/pro (Gemini Team and Google DeepMind, 2024).
The overall and class-specific performance metrics are detailed in Table 1 and Table 2, respectively.
We present a case of the model’s output in Fig. 1 and more cases in Appendix A.6.


**Performance of MagicAssessor.** On the binary classification task, our model achieves a precision
of 0.77 and an F1-score of approximately 0.7, indicating its strong potential for use as a reward
signal. Breaking down the performance across the four L2 categories, the model excels at identifying
human and animal anatomy artifacts but is less effective with interaction and object morphology
issues. These latter categories present distinct challenges: for interaction, the model struggles to
distinguish between element overlap and image areas with low quality. For object morphology, the
sheer diversity and vast number of object types make assessment fundamentally difficult.


**Comparison with Other Models.** Our model significantly outperforms all competitors across the
main evaluation metrics, establishing a large performance gap. The general-purpose open-source
models, like the Qwen-VL and InternVL series, are not very sensitive to artifacts and have very low
recall. An unexpected phenomenon is that the larger versions of these models often perform worse.
We suggest that larger models are more conservative and tend to regard the images as normal. The
commercial models, such as GPT-4o and the Gemini family, perform better but show a clear tradeoff. GPT-4o is more precise but tends to be too cautious and misses many actual artifacts. In contrast,
the Gemini series is better at finding artifacts but also makes more mistakes, flagging labels that are
not real artifacts. In contrast, our model overcomes this trade-off, achieving an excellent balance
between finding real issues and not making false claims, which leads to its much better overall
performance.


4.3 M AGIC B ENCH R ESULTS


To evaluate the performance of existing models with respect to image artifacts, we establish a
baseline using our MagicBench benchmark. This involves a comprehensive evaluation of leading
text-to-image models, with results presented in Table 3. We select a variety of models, including
Qwen-image (Wu et al., 2025), Seedream3.0 (Gao et al., 2025b), Hidream-l1 (Cai et al., 2025),
FLUX.1-dev/schell (Labs, 2024), Kolors1.0 (Team, 2024b), SD3.5 (Stability AI, 2024), SD3 (Esser
et al., 2024), SDXL (Podell et al., 2023), GPT-image-1 (OpenAI, 2025), Bagel (Deng et al., 2025),
Blip3-o (Chen et al., 2025a), Show-o (Xie et al., 2024), and Janus-pro (Chen et al., 2025b). These
models are divided into two categories for comparison: diffusion-based architectures (e.g., SDXL,
FLUX.1-dev) and unified generation-understanding models (e.g., GPT-image-1, Janus-pro).


8


Preprint


GRPO



Table 4: Overall performance of ablation study.

L2 Labels Macro Average L2 Labels Micro Average Artifacts


Precision Recall F1 Precision Recall F1 Precision Recall F1


MagicAssessor-7B 0.5446 0.5244 **0.5261** **0.5744** 0.5425 **0.5580** **0.7756** 0.6381 0.7001
w/o Multi-Bucket Sampling 0.3936 **0.5839** 0.4177 0.4497 **0.6135** 0.5190 0.5337 **0.9652** 0.6874
w/o Positive Data Resampling **0.5462** 0.5098 0.5153 0.5569 0.5196 0.5376 0.7725 0.5937 0.6714

w/o Consistent Reward 0.5292 0.5331 0.5120 0.5153 0.5346 0.5248 0.7448 0.6026 0.6662

SFT 0.4538 0.4340 0.4306 0.5238 0.5330 0.5284 0.7205 0.6936 **0.7068**



Among all models, GPT-image-1 and FLUX.1-dev exhibit the highest overall scores. These models demonstrate a strong ability to produce logically sound and anatomically correct images. Conversely, models like Janus-pro and Show-o struggle the most with image artifacts, indicating ongoing
difficulties in generating consistently accurate and detailed images.


The result indicates that advanced unified models outperform advanced diffusion-based models on
MagicBench. Unified models secure the top position in every evaluation category. Specifically,
GPT-image-1 performances best in both Animal Score and Object Score, in addition to achieving
the highest Overall Score. Meanwhile, Bagel excels with the best Interaction Score, and Blip3-o
leads in Human Score. While the top diffusion-based models like FLUX.1-dev and Seedream3.0 are
highly competitive, they typically rank just behind the leading unified models in most categories.
For instance, FLUX.1-dev achieves the highest Overall Score among all diffusion models and performs strongly across the board, but does not secure the top rank in any single category. Similarly,
Seedream3.0 is a very close runner-up for the top Object Score. This suggests that the integration
of generation and understanding capabilities within a unified architecture may offer an advantage in
mitigating the creation of image artifacts.


Consistent with public benchmarks, newer models generally perform better on our benchmark,
though FLUX.1-dev notably outperforms the more recent Seedream3.0 and Qwen-image. We attribute this to FLUX.1-dev’s tendency to generate subjects in more stable, common poses. In contrast, Seedream3.0 produces more aesthetic and content-rich images, but this complexity increases
the likelihood of artifacts. Our findings suggest that for practical application, future model development must balance the pursuit of aesthetics with the critical need for artifact reduction.


4.4 A BLATION S TUDY


We conduct ablation studies to validate our two-stage training pipeline and key design choices, with
results in Table 4. Detailed per-class performance metrics are provided in the Appendix (Table 6).
The results show that although MagicAssessor-7B is slightly lower than SFT in the F1 score on the
binary classification, it performs significantly better on the four categories of labels. In addition, our
model outputs an inspection process, increasing the confidence level of the inspection results.


Our data sampling strategies are crucial for achieving both balanced and precise results. Without
**Multi-Bucket Sampling**, the model overfits to the most frequent artifact type, _L2: Abnormal Human_
_Anatomy_, causing recall on minority classes like _L2: Irrational Element Interaction_ to collapse to
near zero, as shown in Table 6 in the Appendix. Furthermore, removing **Positive Data Resampling**
degrades the model’s ability to distinguish between correctly formed and artifact hands, leading to
lower precision on _L2: Abnormal Human Anatomy_ . Besides, the design of our reward system is vital
for guiding the model effectively and mitigating reward hacking. Removing **Consistency Reward**
leads to a general drop in metrics and more disorganized textual explanations.


5 C ONCLUSIONS AND F UTURE W ORK


This work introduces MagicMirror, a comprehensive framework to systematically evaluate physical
artifacts in visual generation models. It comprises the first human-annotated large-scale dataset in
this field (MagicData340K), a specialized assessor (MagicAssessor), and an automated benchmark
(MagicBench). Collectively, these tools enable the community to transition from merely acknowledging generation artifacts to actively diagnosing and addressing them.


9


Preprint


While our current framework is designed for post-hoc assessment, a key future direction is to integrate it directly into the model training lifecycle. This can be pursued in two primary ways. First, for
static monitoring, it can be used during the pre-training stage to evaluate model checkpoints. In this
capacity, it would serve as a diagnostic tool to track convergence with respect to artifact reduction,
offering insights into the training process itself. Second, for active optimization, MagicAssessor can
be employed as a reward model in a post-training phase, enabling the fine-tuning of T2I models via
RLHF or ReFL to directly reduce artifact generation.


R EFERENCES


Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical
report. _arXiv preprint arXiv:2303.08774_, 2023.


Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Sibo Song, Kai Dang, Peng Wang,
Shijie Wang, Jun Tang, et al. Qwen2. 5-vl technical report. _arXiv preprint arXiv:2502.13923_,
2025.


Qi Cai, Jingwen Chen, Yang Chen, Yehao Li, Fuchen Long, Yingwei Pan, Zhaofan Qiu, Yiheng
Zhang, Fengbin Gao, Peihan Xu, et al. Hidream-i1: A high-efficient image generative foundation
model with sparse diffusion transformer. _arXiv preprint arXiv:2505.22705_, 2025.


Huiwen Chang, Han Zhang, Lu Jiang, Ce Liu, and William T Freeman. Maskgit: Masked generative
image transformer. In _Proceedings of the IEEE/CVF conference on computer vision and pattern_
_recognition_, pp. 11315–11325, 2022.


Jiuhai Chen, Zhiyang Xu, Xichen Pan, Yushi Hu, Can Qin, Tom Goldstein, Lifu Huang, Tianyi
Zhou, Saining Xie, Silvio Savarese, et al. Blip3-o: A family of fully open unified multimodal
models-architecture, training and dataset. _arXiv preprint arXiv:2505.09568_, 2025a.


Xiaokang Chen, Zhiyu Wu, Xingchao Liu, Zizheng Pan, Wen Liu, Zhenda Xie, Xingkai Yu, and
Chong Ruan. Janus-pro: Unified multimodal understanding and generation with data and model
scaling. _arXiv preprint arXiv:2501.17811_, 2025b.


Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou, Feng Li, Zeyu Wang, Shu Zhong, Weihao
Yu, Xiaonan Nie, Ziang Song, et al. Emerging properties in unified multimodal pretraining. _arXiv_
_preprint arXiv:2505.14683_, 2025.


Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim Entezari, Jonas M¨uller, Harry Saini, Yam
Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling rectified flow transformers
for high-resolution image synthesis. In _Forty-first international conference on machine learning_,
2024.


Yifan Gao, Zihang Lin, Chuanbin Liu, Min Zhou, Tiezheng Ge, Bo Zheng, and Hongtao Xie. Postermaker: Towards high-quality product poster generation with accurate text rendering. In _Proceed-_
_ings of the Computer Vision and Pattern Recognition Conference_, pp. 8083–8093, 2025a.


Yu Gao, Lixue Gong, Qiushan Guo, Xiaoxia Hou, Zhichao Lai, Fanshi Li, Liang Li, Xiaochen Lian,
Chao Liao, Liyang Liu, et al. Seedream 3.0 technical report. _arXiv preprint arXiv:2504.11346_,
2025b.


Gemini Team and Google DeepMind. Gemini 2.5: The next generation of our most capable model.
[Technical report, Google DeepMind, August 2024. URL https://storage.googleapis.](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf)
[com/deepmind-media/gemini/gemini_v2_5_report.pdf.](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf)


Dhruba Ghosh, Hannaneh Hajishirzi, and Ludwig Schmidt. Geneval: An object-focused framework
for evaluating text-to-image alignment. _Advances in Neural Information Processing Systems_, 36:
52132–52152, 2023.


Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu,
Shirong Ma, Peiyi Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms
via reinforcement learning. _arXiv preprint arXiv:2501.12948_, 2025.


10


Preprint


Jack Hessel, Ari Holtzman, Maxwell Forbes, Ronan Le Bras, and Yejin Choi. Clipscore: A
reference-free evaluation metric for image captioning. _arXiv preprint arXiv:2104.08718_, 2021.


Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp Hochreiter.
Gans trained by a two time-scale update rule converge to a local nash equilibrium. _Advances in_
_neural information processing systems_, 30, 2017.


Xiwei Hu, Rui Wang, Yixiao Fang, Bin Fu, Pei Cheng, and Gang Yu. Ella: Equip diffusion models
with llm for enhanced semantic alignment. _arXiv preprint arXiv:2403.05135_, 2024.


Xiwei Hu, Haokun Chen, Zhongqi Qi, Hui Zhang, Dexiang Hong, Jie Shao, and Xinglong Wu.
Dreamposter: A unified framework for image-conditioned generative poster design. _arXiv_
_preprint arXiv:2507.04218_, 2025.


Kaiyi Huang, Kaiyue Sun, Enze Xie, Zhenguo Li, and Xihui Liu. T2i-compbench: A comprehensive benchmark for open-world compositional text-to-image generation. _Advances in Neural_
_Information Processing Systems_, 36:78723–78747, 2023.


Yuval Kirstain, Adam Polyak, Uriel Singer, Shahbuland Matiana, Joe Penna, and Omer Levy. Picka-pic: An open dataset of user preferences for text-to-image generation. _Advances in neural_
_information processing systems_, 36:36652–36663, 2023.


[Black Forest Labs. Flux: Official inference repository for flux.1 models, 2024. URL https:](https://github.com/black-forest-labs/flux)
[//github.com/black-forest-labs/flux.](https://github.com/black-forest-labs/flux)


Youwei Liang, Junfeng He, Gang Li, Peizhao Li, Arseniy Klimovskiy, Nicholas Carolan, Jiao Sun,
Jordi Pont-Tuset, Sarah Young, Feng Yang, et al. Rich human feedback for text-to-image generation. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_,
pp. 19401–19411, 2024.


Zhichao Liao, Xiaokun Liu, Wenyu Qin, Qingyu Li, Qiulin Wang, Pengfei Wan, Di Zhang, Long
Zeng, and Pingfa Feng. Humanaesexpert: Advancing a multi-modality foundation model for
human image aesthetic assessment. _arXiv preprint arXiv:2503.23907_, 2025.


Jie Liu, Gongye Liu, Jiajun Liang, Yangguang Li, Jiaheng Liu, Xintao Wang, Pengfei Wan,
Di Zhang, and Wanli Ouyang. Flow-grpo: Training flow matching models via online rl. _arXiv_
_preprint arXiv:2505.05470_, 2025.


midjourney team. midjourney-v6.1 official website, 2024. [URL https://updates.](https://updates.midjourney.com/version-6-1/)
[midjourney.com/version-6-1/.](https://updates.midjourney.com/version-6-1/)


Alex Nichol, Prafulla Dhariwal, Aditya Ramesh, Pranav Shyam, Pamela Mishkin, Bob McGrew,
Ilya Sutskever, and Mark Chen. Glide: Towards photorealistic image generation and editing with
text-guided diffusion models. _arXiv preprint arXiv:2112.10741_, 2021.


OpenAI. Gpt-image-1, 2025. URL [https://openai.com/index/](https://openai.com/index/introducing-4o-image-generation/)
[introducing-4o-image-generation/. Accessed: 2025-09-01.](https://openai.com/index/introducing-4o-image-generation/)


Dustin Podell, Zion English, Kyle Lacey, Andreas Blattmann, Tim Dockhorn, Jonas M¨uller, Joe
Penna, and Robin Rombach. Sdxl: Improving latent diffusion models for high-resolution image
synthesis. _arXiv preprint arXiv:2307.01952_, 2023.


Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea
Finn. Direct preference optimization: Your language model is secretly a reward model. _Advances_
_in neural information processing systems_, 36:53728–53741, 2023.


Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen,
and Ilya Sutskever. Zero-shot text-to-image generation. In _International conference on machine_
_learning_, pp. 8821–8831. Pmlr, 2021.


Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen. Hierarchical textconditional image generation with clip latents. _arXiv preprint arXiv:2204.06125_, 1(2):3, 2022.


11


Preprint


Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Bj¨orn Ommer. Highresolution image synthesis with latent diffusion models. In _Proceedings of the IEEE/CVF confer-_
_ence on computer vision and pattern recognition_, pp. 10684–10695, 2022.


Chitwan Saharia, William Chan, Saurabh Saxena, Lala Li, Jay Whang, Emily L Denton, Kamyar
Ghasemipour, Raphael Gontijo Lopes, Burcu Karagol Ayan, Tim Salimans, et al. Photorealistic
text-to-image diffusion models with deep language understanding. _Advances in neural informa-_
_tion processing systems_, 35:36479–36494, 2022.


Tim Salimans, Ian Goodfellow, Wojciech Zaremba, Vicki Cheung, Alec Radford, and Xi Chen.
Improved techniques for training gans. _Advances in neural information processing systems_, 29,
2016.


John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy
optimization algorithms. _arXiv preprint arXiv:1707.06347_, 2017.


Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
Mingchuan Zhang, YK Li, Yang Wu, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_, 2024.


Haozhan Shen, Peng Liu, Jingcheng Li, Chunxin Fang, Yibo Ma, Jiajia Liao, Qiaoli Shen, Zilun
Zhang, Kangjia Zhao, Qianqian Zhang, Ruochen Xu, and Tiancheng Zhao. Vlm-r1: A stable and
generalizable r1-style large vision-language model. _arXiv preprint arXiv:2504.07615_, 2025.


Stability AI. Stable Diffusion 3.5 Large. [https://huggingface.co/stabilityai/](https://huggingface.co/stabilityai/stable-diffusion-3.5-large)
[stable-diffusion-3.5-large, 2024. Accessed: 2025-09-01.](https://huggingface.co/stabilityai/stable-diffusion-3.5-large)


Chameleon Team. Chameleon: Mixed-modal early-fusion foundation models. _arXiv preprint_
_arXiv:2405.09818_, 2024a.


Kolors Team. Kolors: Effective training of diffusion model for photorealistic text-to-image synthesis. _arXiv preprint_, 2024b.


Keyu Tian, Yi Jiang, Zehuan Yuan, Bingyue Peng, and Liwei Wang. Visual autoregressive modeling:
Scalable image generation via next-scale prediction. _Advances in neural information processing_
_systems_, 37:84839–84865, 2024.


Bram Wallace, Meihua Dang, Rafael Rafailov, Linqi Zhou, Aaron Lou, Senthil Purushwalkam,
Stefano Ermon, Caiming Xiong, Shafiq Joty, and Nikhil Naik. Diffusion model alignment using
direct preference optimization. In _Proceedings of the IEEE/CVF Conference on Computer Vision_
_and Pattern Recognition_, pp. 8228–8238, 2024.


Xiaodong Wang and Peixi Peng. Open-r1-video. [https://github.com/](https://github.com/Wang-Xiaodong1899/Open-R1-Video)
[Wang-Xiaodong1899/Open-R1-Video, 2025.](https://github.com/Wang-Xiaodong1899/Open-R1-Video)


Siwei Wen, Junyan Ye, Peilin Feng, Hengrui Kang, Zichen Wen, Yize Chen, Jiang Wu, Wenjun
Wu, Conghui He, and Weijia Li. Spot the fake: Large multimodal model-based synthetic image
detection with artifact explanation. _arXiv preprint arXiv:2503.14905_, 2025.


Chenfei Wu, Jiahao Li, Jingren Zhou, Junyang Lin, Kaiyuan Gao, Kun Yan, Sheng-ming Yin, Shuai
Bai, Xiao Xu, Yilei Chen, et al. Qwen-image technical report. _arXiv preprint arXiv:2508.02324_,
2025.


Xiaoshi Wu, Yiming Hao, Keqiang Sun, Yixiong Chen, Feng Zhu, Rui Zhao, and Hongsheng Li.
Human preference score v2: A solid benchmark for evaluating human preferences of text-toimage synthesis. _arXiv preprint arXiv:2306.09341_, 2023a.


Xiaoshi Wu, Keqiang Sun, Feng Zhu, Rui Zhao, and Hongsheng Li. Human preference score:
Better aligning text-to-image models with human preference. In _Proceedings of the IEEE/CVF_
_International Conference on Computer Vision_, pp. 2096–2105, 2023b.


Jinheng Xie, Weijia Mao, Zechen Bai, David Junhao Zhang, Weihao Wang, Kevin Qinghong Lin,
Yuchao Gu, Zhijie Chen, Zhenheng Yang, and Mike Zheng Shou. Show-o: One single transformer
to unify multimodal understanding and generation. _arXiv preprint arXiv:2408.12528_, 2024.


12


Preprint


Jiazheng Xu, Xiao Liu, Yuchen Wu, Yuxuan Tong, Qinkai Li, Ming Ding, Jie Tang, and Yuxiao
Dong. Imagereward: Learning and evaluating human preferences for text-to-image generation.
_Advances in Neural Information Processing Systems_, 36:15903–15935, 2023.


Zeyue Xue, Jie Wu, Yu Gao, Fangyuan Kong, Lingting Zhu, Mengzhao Chen, Zhiheng Liu, Wei
Liu, Qiushan Guo, Weilin Huang, et al. Dancegrpo: Unleashing grpo on visual generation. _arXiv_
_preprint arXiv:2505.07818_, 2025.


Fan Yang, Ru Zhen, Jianing Wang, Yanhao Zhang, Haoxiang Chen, Haonan Lu, Sicheng Zhao, and
Guiguang Ding. Heie: Mllm-based hierarchical explainable aigc image implausibility evaluator.
In _Proceedings of the Computer Vision and Pattern Recognition Conference_, pp. 3856–3866,
2025.


Yaowei Zheng, Junting Lu, Shenzhi Wang, Zhangchi Feng, Dongdong Kuang, and Yuwen Xiong.
[Easyr1: An efficient, scalable, multi-modality rl training framework. https://github.com/](https://github.com/hiyouga/EasyR1)
[hiyouga/EasyR1, 2025.](https://github.com/hiyouga/EasyR1)


Zhaokun Zhou, Qiulin Wang, Bin Lin, Yiwei Su, Rui Chen, Xin Tao, Amin Zheng, Li Yuan, Pengfei
Wan, and Di Zhang. Uniaa: A unified multi-modal image aesthetic assessment baseline and
benchmark. _arXiv preprint arXiv:2404.09619_, 2024.


Jie Zhu, Yixiong Chen, Mingyu Ding, Ping Luo, Leye Wang, and Jingdong Wang. Mole: Enhancing human-centric text-to-image diffusion via mixture of low-rank experts. _Advances in Neural_
_Information Processing Systems_, 37:29354–29386, 2024.


Jinguo Zhu, Weiyun Wang, Zhe Chen, Zhaoyang Liu, Shenglong Ye, Lixin Gu, Hao Tian, Yuchen
Duan, Weijie Su, Jie Shao, et al. Internvl3: Exploring advanced training and test-time recipes for
open-source multimodal models. _arXiv preprint arXiv:2504.10479_, 2025.


13


Preprint


A A PPENDIX


This supplementary material is structured into several sections to provide additional details and
analysis for our work. Specifically, it covers the following topics:


    - In Appendix A.1, we provide a review of related works in the fields of text-to-image generation and evaluation.


   - In Appendix A.2, we offer a detailed overview of our MagicData340K dataset, including
the annotation process and complete label taxonomy.


    - In Appendix A.3, we describe the prompt engineering used to elicit detailed reasoning from
our models.


    - In Appendix A.4, we elaborate on the design and implementation of the multi-level reward
system.


    - In Appendix A.5, we present the full experimental setup, including training configurations
and evaluation metric definitions.


    - In Appendix A.6, we showcase qualitative examples of responses from different assessor
models on the artifact detection task.


   - In Appendix A.7, we present the detail prompt construction process of MagicBench and
more detail evaluation result.


A.1 R ELATED W ORKS


**Text-to-Image Generation.** The emergence of diffusion-based text-to-image (T2I) models (Nichol
et al., 2021; Saharia et al., 2022; Ramesh et al., 2022; Rombach et al., 2022) marks a significant leap
in text-to-image quality, attracting widespread attention. This paradigm has been further advanced
by subsequent works (Podell et al., 2023; Esser et al., 2024; Labs, 2024), which elevated generation
quality to new heights by refining model architectures and expanding parameter capacity.


On the other hand, autoregressive T2I models (Ramesh et al., 2021; Chang et al., 2022; Tian et al.,
2024) have also been developing rapidly. Some works (Team, 2024a; Xie et al., 2024; Chen et al.,
2025b; Deng et al., 2025) attempt to unify generation and understanding into a single model, thereby
enabling the text-to-image process to better leverage vast world knowledge. As instruction following, aesthetics, and resolution have progressively improved, higher demands have been placed on
generation quality, and the presence of artifacts in images has gradually become one of the main
bottlenecks for improving image quality.


**Text-to-Image Evaluation.** The evaluation of T2I models is critical for guiding their development
and has evolved in tandem with their capabilities. Early metrics like Inception Score (IS)(Salimans
et al., 2016) and Fr´echet Inception Distance (FID)(Heusel et al., 2017) assessed general image quality, independent of text prompts. As models’ instruction-following abilities improved, evaluation
branched into two major directions: semantic and aesthetic alignment.


On the semantic front, metrics like CLIP Score (Hessel et al., 2021) were introduced to measure
text-image consistency. This was followed by specialized benchmarks targeting specific abilities,
such as object-level alignment in Geneval (Ghosh et al., 2023), compositional accuracy in T2ICompBench (Huang et al., 2023), and adherence to dense prompts in DPG-Bench (Hu et al., 2024).
In parallel, the aesthetic front focused on aligning models with human preferences. This led to
influential reward models trained on large-scale human feedback, including ImageReward (Xu et al.,
2023), the Human Preference Score (HPS) series (Wu et al., 2023b;a), and Pick-a-Pic (Kirstain et al.,
2023), which have become standards for judging visual appeal.


More recently, research has shifted towards evaluating higher-level attributes like plausibility and
realism. For instance, RichHF (Liang et al., 2024) focuses on human feedback for plausibility, while
HEIE (Yang et al., 2025) and FakeVLM (Wen et al., 2025) attempt to not only detect but also explain
unrealistic or ”fake” elements in images. Despite these advancements, existing evaluation methods
lack a granular assessment of common image artifacts and artifacts. This gap highlights the need for
a comprehensive benchmark dedicated to the multi-dimensional evaluation of such artifacts, which
remains a key barrier to achieving true photorealism and reliability.


14


Preprint


Figure 7: The annotation interface designed for the MagicData340K dataset.


**GRPO in Vision Language Model.** With advancements in reinforcement learningSchulman et al.
(2017); Rafailov et al. (2023); Wallace et al. (2024), the Group Relative Policy Optimization
(GRPO) (Shao et al., 2024) algorithm has effectively enhanced the reasoning capabilities of models,
showing significant potential. Consequently, recent work has begun to extend GRPO to VisionLanguage Models (VLMs) (Zheng et al., 2025; Shen et al., 2025; Wang & Peng, 2025), demonstrating considerable performance gains in multimodal tasks. A notable application involves leveraging
scores from evaluation benchmarks (Liu et al., 2025; Xue et al., 2025), such as Geneval, as reward
signals to fine-tune text-to-image models (Liu et al., 2025), leading to significant improvements on
those specific metrics. To better identify artifacts in generated images, we introduce GRPO to the
task of artifacts detection.


A.2 D ATASET A NNOTATION AND L ABEL T AXONOMY


This section provides a comprehensive overview of the MagicData340K dataset, detailing the data
statistics, the established labeling methodology, and the complete taxonomy of our classification
labels.


Our dataset contains a total of 343,269 images, which are partitioned into a training set (325,238),
a test set (17,366), and a Chain-of-Thought (CoT) set (1,294). The data is broadly categorized
into “Normal” images (173,768) and “Artifacts” images (169,501), which contain various types
of anomalies. A detailed statistical breakdown is presented in Table 5. The analysis reveals that
“Abnormal Human Anatomy” is the most prevalent category of artifacts, accounting for 61.53% of
all anomalous samples. This is followed by “Irrational Element Interaction” (36.6%) and “Abnormal
Object Morphology” (21.88%), highlighting the most common failure modes in image generation.


To ensure consistency and quality in annotation, we develop a specific labeling user interface (UI),
as shown in Fig. 7, and establish a set of core guidelines for our annotators. These guidelines are as
follows:


1. **Handling Multiple Issues:** When judging, if an image corresponds to multiple issues, only
the two most obvious issues need to be marked. However, there are two exceptions: if the
number of people in the image is _≥_ 3 and the number of abnormal issues is _≥_ 3, you can


15


Preprint


Normal



L3: Limb Structure Deformity L3: Trunk Structure Deformity L3: Hand Structure Deformity



L3: Foot Structure Deformity L3: Facial Structure Deformity L3: Abnormal and Uncoordinated Posture L3: Abnormal Human Anatomy


L3: Abnormal Material Texture L3: Abnormal Detail Drawing L3: Abnormal Element Proportion L3: Abnormal Color Combination



L3: Abnormal Limb Structure L3: Abnormal Posture Presentation L3: Abnormal Head Structure


L3: Abnormal Light and Shadow Effect L3: Abnormal Element Overlap L3: Abnormal Spatial Position



L2: Abnormal Object Morphology


L2: Other Irrationalities



Figure 8: Visual examples of labeled artifacts categories.


simply label it as “L3: Abnormal Human Anatomy”; if a single person has more than 3
abnormal issues, you can directly label it as “L3: Abnormal Human Anatomy”.

2. **Standard for Abnormality:** During the annotation process, only more obvious abnormalities need to be noted. If an issue cannot be identified within 3 seconds (e.g., it may be a
blurred background entity or a small-sized object), or if a reasonable explanation exists, or
it belongs to an imaginable special case, it is not considered abnormal; you can label it as
“Whether Normal: True”.

3. **Distinguishing Style from Structure:** Instantly fake or heavily AI-generated feeling belongs to image style issues, not structural abnormalities; therefore, you can label it as
“Whether Normal: True”.


16


Preprint


Table 5: Detailed statistics of the MagicData340K dataset.

|Labels|Col2|Col3|Col4|Train|Test|CoT|
|---|---|---|---|---|---|---|
|Total|Total|Total|**(343269)**|**325238**|**17366**|**1835**|
|Normal|Normal|Normal|**(173768)**|**165078**|**8690**|**642**|
|Artifacts|Artifacts|Artifacts|**(169501)**|**160160**|**8676**|**1193**|
||L2: Irrational Element Attributes|L2: Irrational Element Attributes|**(881 / 169501) (0.52%)**|**561**|**247**|**256**|
|||L3: Abnormal Material Texture|(54) (0.03%)|37|19|37|
|||L3: Abnormal Detail Drawing|(192) (0.11%)|133|59|101|
|||L3: Abnormal Element Proportion|(612) (0.36%)|374|163|101|
|||L3: Abnormal Color Combination|(23) (0.01%)|17|9|17|
||L2: Irrational Element Interaction|L2: Irrational Element Interaction|**(61994 / 169501) (36.6%)**|**56262**|**3004**|**299**|
|||L3: Abnormal Light and Shadow Effect|(258) (0.15%)|176|77|101|
|||L3: Abnormal Element Overlap|(45857) (27.0%)|42387|2232|111|
|||L3: Abnormal Spatial Position|(15879) (9.3%)|15128|798|101|
||L2: Abnormal Human Anatomy|L2: Abnormal Human Anatomy|**(104289 / 169501) (61.53%)**|**97882**|**5645**|**639**|
|||L3: Limb Structure Deformity|(3638) (2.1%)|3246|362|101|
|||L3: Trunk Structure Deformity|(723) (0.1%)|497|215|101|
|||L3: Hand Structure Deformity|(54114) (31.9%)|50959|2684|269|
|||L3: Foot Structure Deformity|(4604) (2.7%)|4113|459|101|
|||L3: Facial Structure Deformity|(8581) (5.0%)|7661|853|101|
|||L3: Abnormal Human Anatomy|(42327) (24.9%)|40015|2108|104|
|||L3: Abnormal and Uncoordinated Posture|(300) (0.1%)|207|91|101|
||L2: Abnormal Animal Anatomy|L2: Abnormal Animal Anatomy|**(23464/169501) (13.84%)**|**21968**|**1324**|**235**|
|||L3: Abnormal Limb Structure|(20932) (12.3%)|19760|1041|130|
|||L3: Abnormal Posture Presentation|(234) (0.1%)|162|72|101|
|||L3: Abnormal Head Structure|(5433) (3.2%)|4833|539|101|
||L2: Abnormal Object Morphology|L2: Abnormal Object Morphology|**(37085 / 169501) (21.88%)**|**34972**|**1842**|**101**|
||L2: Other Irrationalities|L2: Other Irrationalities|**(20) (0.01%)**|**18**|**10**|**18**|



4. **Ignoring Textual Content:** If there is a text error in the image, do not judge it as unreasonable based on the text content.

5. **Considering User Prompts:** When some images initially appear to violate physical laws,
refer to the user’s prompt and style requirements to assist judgment. If the image conforms
to the special conditions specified in the prompt, you can label it as “Whether Normal:
True”.


The artifacts were categorized into a hierarchical taxonomy with five high-level (L2) categories,
each containing more specific (L3) sub-categories. Fig. 8 provides visual examples for many of
these labels. The complete definitions are as follows:


L2: Irrational Element Attributes: “The visual attributes of elements in the image do not conform to
physical laws.”


    - L3: Abnormal Material Texture: “The material texture does not match the actual properties
of the object, such as metallic texture displaying a wooden pattern.”

   - L3: Abnormal Detail Drawing: “Abnormal background elements in the image.”

   - L3: Abnormal Element Proportion: “The relative sizes of elements in the image do not
conform to real proportions or expected scales, such as a mosquito larger than a hand.”

    - L3: Abnormal Color Combination: “Color combination violates visual color theory, leading to a visual appearance that does not conform to the real world.”


L2: Irrational Element Interaction: “The spatial and logical interactions between elements in the
image are unreasonable.”


   - L3: Abnormal Light and Shadow Effect: “The position of the light source and shadow
direction are inconsistent, causing unnatural light and shadow projection. The light and
shadow effect does not match the light source position, intensity, and objective factors.”


17


Preprint


    - L3: Abnormal Element Overlap: “Overlap relationships between different elements do not
conform to physical laws, such as a solid object partially penetrating another object.”


    - L3: Abnormal Spatial Position: “The distribution and logical arrangement of elements in
space are inconsistent, causing chaotic overall layout, such as floating, mismatch between
inside and outside state in a mirror.”


L2: Abnormal Human Anatomy: “The structure of the human body in the image does not conform
to normal physiological and anatomical standards”


   - L3: Limb Structure Deformity: “Limb structure does not conform to conventional human
form.”


    - L3: Trunk Structure Deformity: “The spine shows unnatural curvature or twisting.”


    - L3: Hand Structure Deformity: “Abnormal number of fingers or unreasonable joint angles.”


    - L3: Foot Structure Deformity: “Disorganized toe arrangement or abnormal arch shape.”


    - L3: Facial Structure Deformity: “Imbalance in facial features or lack of facial symmetry.”


   - L3: Abnormal Human Anatomy: “Multiple human abnormalities.”


   - L3: Abnormal and Uncoordinated Posture: “Whole body posture does not conform to
gravitational direction or movements are inconsistent with ergonomics.”


L2: Abnormal Animal Anatomy: “The structure of animals in the image does not conform to normal
physiological and anatomical standards”


   - L3: Abnormal Limb Structure: “Imbalance in animal limb proportions or shape does not
conform to common sense.”


    - L3: Abnormal Posture Presentation: “Animal movement posture does not match its biological characteristics.”


    - L3: Abnormal Head Structure: “Abnormal position or imbalance in the proportion of eyes
or ears.”


L2: Abnormal Object Morphology: “Geometric shape is abnormal, the object outline or geometric
proportions do not match actual characteristics; or the construction is unreasonable, the connection
method of object parts does not conform to logic or actual structure.”


L2: Other Irrationalities: “Other irrationalities.”


A.3 C HATTING T EMPLATE


To effectively guide the model in identifying and classifying anomalies in generated images, we
designed a comprehensive prompt structured with the following key components:


1. **Task Description:** The core objective is then clearly defined: “You need to determine
whether this image is reasonable (or whether there is any deformity), and if it is not reasonable, provide the corresponding type of deformity. If the provided type of deformity has
sub-tags, additionally provide the corresponding sub-tag categories.”


2. **Labels and Definitions:** To ensure standardized classification, a complete taxonomy
of deformities is provided: “All types of deformities and their sub-tags are: “ +
str(type ~~d~~ efinition) + ”. Note that the primary label is Whether Normal, L2 represents
second-level tags, and L3 represents third-level tags.”


3. **Illustrative Answer Formats:** To clarify the expected output, the prompt provides a few
example answer formats. These examples demonstrate the required structure for different
scenarios, such as


      - the format for a normal image ( _{_ “Whether Normal”: True _}_ )

      - an image with an abnormality but no sub-tags ( _{_ “Whether Normal”: False, “Type of
Abnormality”: _{_ “L2: Abnormal Object Morphology”: True _}}_ )


18


Preprint


      - an image with an abnormality that includes sub-tags ( _{_ “Whether Normal”: False,
“Type of Abnormality”: _{_ “L2: Abnormal Human Anatomy”: [“L3: Abnormal Human
Anatomy”] _}}_ )

      - an image with two distinct types of abnormalities ( _{_ “Whether Normal”: False, “Type
of Abnormality”: _{_ “L2: Abnormal Object Morphology”: True, “L2: Abnormal Human Anatomy”: [“L3: Abnormal Human Anatomy”] _}}_ ).

4. **Answering Process:** The prompt outlines the required cognitive steps for the model: “You
need to first understand all the given labels and rules, then think about possible issues
according to the text prompt and the subject of the prompt, and then observe the image to
analyze every detail in the image to determine whether there is any deformity.”

5. **Content Requirements:** The model is instructed on how to articulate its reasoning process: “Give a continuous thinking process using natural language. The response should
flow seamlessly as a narrative or story, examining the image as a whole rather than in separate points. Please describe the reasoning process without using bullet points or distinct
sections.”

6. **Formatting Requirements:** Finally, the required output structure is specified: “Ensure
that the answer matches the format of the given example. The output format should be
_< think > ... < /think > ... boxed{answer}_ .”


A.4 M ULTI -R EWARD D ESIGN


Consistency Reward ( _r_ _c_ ): To prevent reward hacking, where the model might produce a correct final
answer without a valid reasoning process, we use a smaller, pre-trained LLM to judge the logical
consistency between the generated Chain-of-Thought and the final labeled output. The result is a
binary reward, _r_ _c_ _∈{_ 0 _,_ 1 _}_, where 1 indicates consistency. This entire reward is nullified if the
reasoning is flawed.


Hierarchical Rewards ( _r_ 1 _, r_ 2 _, r_ 3 _, r_ 4 ): The system categorizes rewards into four hierarchical levels:


1. _r_ 0 (Format and Parsability Reward): This is a binary reward, _r_ 0 _∈{_ 0 _,_ 1 _}_ . It assesses
whether the output adheres to the required _< think >_ and dictionary format and can
be successfully parsed by our evaluation script. This includes checking for hierarchical
dependencies (e.g., an L3 label only appears under its parent L2 label).

2. _r_ 1 (L1-level Label Reward): This is a binary reward, _r_ 1 _∈{_ 0 _,_ 1 _}_, evaluating the accuracy
of the highest-level binary classification (i.e., whether the image is correctly identified as
”Normal” or ”Artifact”).

3. _r_ 2 _, r_ 3 (L2, L3-level Label Rewards): Since a single sample can have multiple L2 and L3
labels, these rewards are calculated based on the number of correct ( _n_ _correct_ ), missed
( _n_ _miss_ ), and extra ( _n_ _extra_ ) predictions. The score is 1 if all ground-truth labels are correctly predicted and there are no extra predictions, and 0 if no labels are predicted at all.
Otherwise, the score is calculated using the following formula, which rewards precision
and penalizes recall errors:


_r_ 2 _,_ 3 = clamp(0 _._ 6 _· n_ _correct_ _−_ 0 _._ 3 _·_ ( _n_ _miss_ + _n_ _extra_ ) _,_ min = 0 _,_ max = 1) _._ (5)


A.5 E XPERIMENTAL D ETAILS


We provide supplementary information for our experiments. Section A.5 details the experimental
setup and the formulas used to calculate our evaluation metrics. Furthermore, Table 6 presents the
detailed per-class results of the ablation study discussed in the main text.


A.5.1 E XPERIMENTAL S ETUP


All of our experiments are built upon the **Qwen2.5-VL-7B** as the foundational model. Our training
methodology follows a two-stage process designed to progressively enhance the model’s capabilities. The initial cold start phase consists of Supervised Fine-Tuning (SFT) using our curated **CoT**
**dataset**, which contains 1,294 high-quality examples with detailed reasoning. This stage was conducted for 40 steps with a batch size of 32, a learning rate of 2.0e-5, and a LoRA rank of 32.


19


Preprint



GRPO



Table 6: Four class performance of ablation study.


L2: Irrational Element Interaction L2: Abnormal Human Anatomy L2: Abnormal Animal Anatomy L2: Abnormal Object Morphology


Precision Recall F1 Precision Recall F1 Precision Recall F1 Precision Recall F1


MagicAssessor-7B **0.3665** 0.4621 0.4088 0.8957 0.6177 0.7312 0.5805 0.6563 0.6161 **0.3359** 0.3616 **0.3482**
w/o Multi-Bucket Sampling 0.2248 0.0097 0.0185 0.7407 **0.8955** **0.8107** 0.4621 **0.9071** 0.6123 0.1468 **0.5233** 0.2293
w/o Positive Data Resampling 0.3575 0.4917 **0.4140** **0.9010** 0.5624 0.6926 **0.5949** 0.6322 0.6130 0.3315 0.3529 0.3418

w/o Consistent Reward 0.3258 **0.5523** 0.4098 0.8980 0.5488 0.6813 0.5834 0.6579 **0.6184** 0.3096 0.3735 0.3386

SFT 0.2879 0.4567 0.3532 0.7640 0.7382 0.7509 0.5509 0.4615 0.5023 0.2124 0.0798 0.1160



Following this, the model undergoes Group Relative Policy Optimization (GRPO) for 300 steps on
our main **GRPO dataset**, which is partitioned into 325,238 training and 17,366 test samples. For
the GRPO stage, we used the AdamW optimizer with a learning rate of 1.0e-6 and a global batch
size of 128. To benchmark the effectiveness of this two-stage approach, we also trained an SFT-only
baseline model on the full dataset for 300 steps.


A.5.2 E VALUATION M ETRICS


To quantitatively assess model performance, we employ the standard metrics of Precision, Recall,
and F1-Score. Precision measures the accuracy of positive predictions, while Recall measures the
model’s ability to identify all relevant instances. The F1-Score provides a balanced measure as the
harmonic mean of Precision and Recall. The formulas are as follows:


TP
Precision = (6)
TP + FP


TP
Recall = (7)
TP + FN



F1-Score = 2 _·_ [Precision] _[ ·]_ [ Recall] (8)

Precision + Recall


where:


    - **TP (True Positives):** The number of images correctly identified as having a specific artifacts (model predicted the label, and it was correct).


    - **FP (False Positives):** The number of images incorrectly identified as having a specific
artifacts when they do not (model **over-predicted** the label).


    - **FN (False Negatives):** The number of images that have a specific artifacts but were not
identified by the model (model **under-predicted** the label).


Our evaluation is conducted in two settings: a top-level binary detection of “Normal” vs. “Artifact”
images, and a fine-grained, multi-label classification across our four primary L2 artifacts categories.
For the multi-label task, we report both macro and micro averages to provide a complete performance picture. The **Macro Average** computes the metric independently for each class and then
takes the average, treating all classes equally. The **Micro Average** aggregates the contributions
of all classes to compute the metric globally, giving more weight to more populous classes. The
formulas for a set of C classes are:



Macro Average = [1]

_C_



_C_
� Metric _i_ (9)


_i_ =1



_C_ _C_
� _i_ =1 [TP] _[i]_ � _i_ =1 [TP] _[i]_
Micro Average Precision = ~~�~~ _Ci_ =1 [(][TP] _[i]_ [ +][ FP] _[i]_ [)] _,_ Micro Average Recall = ~~�~~ _Ci_ =1 [(][TP] _[i]_ [ +][ FN] _[i]_ [)]
(10)


20


Preprint


Table 7: Evaluation score ( _↑_ ) on different labels of different models in MagicBench.

Human Animal Object


Single Double Multiple Single Multi Single Multiple Compose
FLUX.1-dev 80.00 43.00 16.00 85.00 11.00 97.00 86.87 84.85

Seedream3.0 93.00 26.00 4.00 89.00 5.00 98.99 83.70 88.42
Qwen-image 91.00 34.00 8.08 83.00 7.07 98.00 82.98 81.91
Hidream-l1 77.00 33.00 8.00 87.00 4.00 100.00 81.91 87.88

FLUX.1-schnell 78.00 35.00 3.00 77.00 6.00 98.99 79.38 81.00

SD3.5 78.00 34.00 8.00 74.00 10.00 93.94 80.85 72.63

Kolors1.0 66.00 34.00 19.19 76.00 13.00 84.21 75.00 67.02

SD3 66.00 15.00 1.00 83.00 7.00 97.98 77.17 64.89

SDXL 69.00 21.00 8.00 83.00 6.00 92.71 70.21 59.57
GPT-image-1 84.00 44.00 9.00 96.00 9.00 99.00 85.26 89.58
Bagel 72.00 36.00 15.00 85.00 20.00 91.00 83.00 89.80
Blip3-o 83.00 48.00 9.00 83.00 9.00 95.83 78.72 68.82
Janus-pro 55.00 10.00 1.01 73.00 3.03 98.99 72.92 69.57
Show-o 51.00 14.00 7.00 71.00 3.00 95.92 70.21 61.96


A.6 R ESPONSE OF D IFFERENT M ODELS


We selected two representative cases to showcase the distinct answering styles and behavioral patterns of the various models, as shown in Fig. 9, Fig. 10, Fig. 11 and Fig. 12.


    - MagicAssessor-7B demonstrates a highly focused and efficient response style. In all four
examples—from animal anatomy and human figures to object interaction and morphology—its reasoning process was concise and directly targeted the specific visual flaw. It
consistently avoided irrelevant descriptions, instead moving straight to identifying and correctly classifying the error. This pattern highlights its reliable and accurate analytical approach.


    - Gemini-2.5-pro is characterized by its thorough and highly accurate analytical process. It
correctly identified the abnormalities in all cases, providing detailed, step-by-step reasoning
that demonstrates a deep contextual understanding. For instance, in the billiard table scene,
it not only spotted the error but also explained why it was illogical according to the rules of
the game. Its extensive reasoning serves to strengthen its conclusions, rather than leading
it to incorrect classifications.


   - GPT-4o shows inconsistent performance. While it can identify more obvious anatomical
deformities, such as the incorrect limb structure on the dinosaur and the artifact hands in the
nightclub scene, it fails on more subtle or logical errors. In the billiard table and barber tool
examples, it overlooked clear flaws in object arrangement and shape, incorrectly judging
the images to be normal. Its tendency to provide a general description can prevent it from
noticing critical details, making it unreliable.


   - Qwen2.5-VL-7B and InternVL3-8B exhibited significant weaknesses in their analytical
capabilities. They consistently failed to identify the actual deformities in the images. A
common issue was misinterpreting the creative intent of a prompt as a flaw (e.g., labeling
the concept of a dinosaur with a lightsaber as an error). Furthermore, they often made
subjective judgments about the scene’s content rather than performing an objective analysis
of the generated image. Both models also frequently failed to follow the required output
format.


A.7 P ROMPT C ONSTRUCTION OF M AGIC B ENCH


To ensure the diversity and comprehensiveness of our evaluation, we devise a structured approach
for prompt construction centered on three core entity types: Human, Animal, and Object. For each
entity, we design prompts of increasing complexity to systematically test model capabilities. These
are classified into eight distinct sub-categories: human ~~s~~ ingle, human ~~d~~ ouble, human ~~m~~ ultiple, animal ~~s~~ ingle, animal ~~m~~ ultiple, object ~~s~~ ingle, object ~~m~~ ultiple, and object ~~c~~ ompose. To generate a
rich and varied set of prompts, we first curate an extensive entity library extracted from large-scale
datasets. Subsequently, we utilize Gemini-2.5-pro (Gemini Team and Google DeepMind, 2024) to


21


Preprint


systematically combine these entities with a wide range of contexts, actions, and stylistic elements
(e.g., scenes, camera shots). The detailed design for each entity type is outlined below.


   - For the human ~~s~~ ingle sub-category, prompts focus on the detailed description of individuals, specifying their profession, actions, and emotional state. The human ~~d~~ ouble subcategory assesses the capacity to represent interactions between two people, such as collaboration or conversation, testing the model’s grasp of body language and composition.
Finally, human ~~m~~ ultiple challenges the ability to render complex group scenes, such as
team sports or crowded markets, to evaluate performance in managing busy compositions
and generating a specific group atmosphere.


   - The animal ~~s~~ ingle prompts are centered on capturing the distinctive features and characteristic actions of a single animal, often styled after wildlife photography to test for anatomical
accuracy and environmental realism. The animal ~~m~~ ultiple sub-category evaluates the capacity to depict collective animal behaviors, such as migration or herding. These prompts
often employ wide-angle or aerial perspectives to test the model’s ability to generate largescale scenes while maintaining the integrity of individual animals.


   - The object ~~s~~ ingle prompts concentrate on the careful depiction of a single object, aiming
to cover different material properties, such as the transparency of glass or the aged surface
of metal, under specific lighting. Object ~~m~~ ulti assesses performance in generating patterns
and textures from many identical objects, testing the ability to handle repetition and convey
a sense of scale. Lastly, object ~~c~~ ompose includes rendering the logical and spatial relationships between different but thematically linked objects, testing its ability to create a
coherent and well-composed scene.


After obtaining these initial prompts, we extract the corresponding subject (e.g., little boy) from
each one and annotate it with its class (e.g., human) and detailed sub-category (e.g., human ~~s~~ ingle).
Finally, we append the instruction, “The image must include the complete ‘subject’.” to the end of
each prompt to form the final test instance, where ‘subject’ refers to the extracted subject. The scores
of different models for each category are presented in Table 7. Note that due to some generation
failures, the denominator for some categories is 99 or 98, instead of 100.


22


Preprint


Lables:

{“Whether Normal”: false,
“Type of Deformity”: {
“L2: Abnormal Human Anatomy”: [
“L3: Abnormal Human Anatomy”]}}


T2I_prompt:
Bruce wayne at a night club surrounded by women having a cocktail and laughing.


**MagicAssessor-7B:**
<think>\nUpon examining the image, it depicts a scene consistent with the prompt: Bruce Wayne at a night club surrounded by women, with everyone
appearing to be enjoying cocktails and laughter. However, upon closer inspection, there are several anatomical abnormalities present in the image. The
woman on the left side of the image has a hand that appears to be missing a finger, and the woman on the right side of the image also has a hand that
seems to be missing a finger. Additionally, the man in the center of the image has a hand that appears to be missing a finger as well. These hand
deformities are consistent with the 'Hand Structure Deformity' sub-tag under 'Abnormal Human Anatomy'. Furthermore, the woman on the far right has a
hand that appears to be missing a finger, and the man in the center has a hand that appears to be missing a finger. These abnormalities indicate multiple
human anatomical abnormalities in the image. Therefore, the image is not reasonable due to these deformities.\n</think>\n\\boxed{{\"Whether Normal\":
false, \"Type of Deformity\": {\"L2: Abnormal Human Anatomy\": [\"L3: Abnormal Human Anatomy\"]}}


**Gemini-2.5-pro:**
<think>The user wants me to analyze an image based on the prompt \"bruce wayne at a night club surrounded by women having a cocktail and laughing\"
and determine if it's normal or has deformities according to a specific classification system.\n\nFirst, I'll examine the image's overall adherence to the
prompt. The image does show a man who could be interpreted as Bruce Wayne, characterized by his confident, playboy persona. He is in a nightclub
setting, surrounded by women, and they are all laughing and holding cocktails. The comic book art style is a specific interpretation, but it fits the subject
matter, as Bruce Wayne is a comic book character. So, the content matches the prompt.\n\nNext, I'll analyze the image for potential deformities, going
through the provided categories.\n\n**L2: Irrational Element Attributes:** The colors are dramatic and fitting for a nightclub scene. The textures are
consistent with a comic book illustration style. The proportions between people and objects (like cocktail glasses) seem reasonable. There are no issues in
this category.\n\n**L2: Irrational Element Interaction:** The lighting is stylized with strong highlights and deep shadows, which is a common technique
in this art style to create drama. The light source appears to be from the front and slightly above, and the highlights and shadows on the figures are
consistent with this. The way the characters are crowded together and overlapping is natural for a busy club scene. There are no spatial or logical
inconsistencies.\n\n**L2: Abnormal Human Anatomy:** This is where I need to look closely. Comic book art often exaggerates anatomy for stylistic
effect, but there's a line between style and error.\n- The central figure, Bruce Wayne, has a highly muscular and defined torso, which is characteristic of
the character. His laughing expression is extreme but anatomically plausible.\n- Let's examine the other figures, particularly their hands, as these are often
problematic in generated images.\n- The woman in the foreground on the left is holding a cocktail. Her left forearm appears unusually long and her hand is
quite large and sinewy, with very pronounced tendons. The structure looks more masculine and skeletal than is typical, creating a slight incongruity. This
could be considered a `L3: Limb Structure Deformity`.\n- The woman in the foreground on the right is also holding a cocktail. Her fingers, especially the
pinky, appear unnaturally long and thin. This points towards a `L3: Hand Structure Deformity`.\n- The woman standing behind Bruce Wayne has her hand
on his shoulder. This hand appears reasonably well-drawn.\n- The man in the background (top right) is holding a glass, but his hand is poorly defined and
looks somewhat malformed, almost like a clump. This is another instance of a hand deformity.\n\nGiven these observations, there are multiple instances of
anatomical abnormalities in the image. The arm and hand of the woman on the left are disproportionate and strangely textured. The fingers of the woman
on the right are unnaturally long. The hand of the man in the background is malformed. Since there are several distinct anatomical problems across
different characters, this qualifies as a deformity.\n\nThe appropriate category is `L2: Abnormal Human Anatomy`. Within this category, we have issues
that could fall under `L3: Limb Structure Deformity` and `L3: Hand Structure Deformity`. Since the definition for the sub-tag `L3: Abnormal Human
Anatomy` is \"Multiple human abnormalities,\" it is the most suitable choice to encompass the various issues found with the limbs and hands of several
characters in the image.\n\nTherefore, the image is not reasonable due to multiple anatomical deformities. The final classification will reflect this.
```json\n{\n  \"Whether Normal\": false,\n  \"Type of Abnormality\": {\n    \"L2: Abnormal Human Anatomy\": [\n      \"L3: Abnormal Human
Anatomy\"\n    ]\n  }\n}\n```


**GPT-4o:**
<think>The image depicts Bruce Wayne at a nightclub, surrounded by women, holding a cocktail, and laughing. Considering the prompt, I need to
evaluate whether the visual representation exhibits any deformities. First, I'll focus on the anatomy of the characters to identify if there is any abnormality
in their physiology. Regarding their hands, which are quite central in this image due to the cocktails, there appear to be irregularities. Upon close
inspection, the hand structures shown do not have anatomically correct arrangements. The number of fingers is inconsistent or disproportionate, and some
joint angles appear abnormal. This qualifies as a \"Hand Structure Deformity\" under \"Abnormal Human Anatomy.\" Additionally, looking at the
interaction between elements, all other features seem plausible in terms of proportion, spatial arrangement, and coherence of interactions (e.g., lighting
appears consistent, background elements align well with the nightclub setting). Thus, there's no concern in the broader setup—only localized deformities
are apparent in the anatomical accuracy of human hands.</think>\n\n\\boxed{ {'Whether Normal': False, 'Type of Abnormality': {'L2: Abnormal Human
Anatomy': ['L3: Hand Structure Deformity']}}


**Qwen2.5-VL-7B:**
The image depicts a scene with Bruce Wayne at a night club surrounded by women, each holding a cocktail and laughing. The overall composition and
elements in the image appear to be reasonable and align with the described scenario. However, upon closer inspection, there are some visual
inconsistencies that suggest potential deformities.\n\n1. **L2: Irrational Element Interaction**\n  - **L3: Abnormal Light and Shadow Effect**: The
lighting in the image is somewhat inconsistent. The light sources seem to be coming from multiple directions, creating a mix of highlights and shadows
that don't seem to follow a single light source. This could be interpreted as an irrational light and shadow effect.\n\n2. **L2: Abnormal Human
Anatomy**\n  - **L3: Abnormal Human Anatomy**: The figures in the image, particularly the women, have exaggerated and unrealistic proportions.
Their limbs and body structures appear to be elongated or distorted, which is not typical in real-life human anatomy. This could be categorized as an
abnormal human anatomy.\n\nGiven these observations, the image contains some deformities that do not align with real-world
expectations.\n\n\\boxed{False, Type of Abnormality: {'L2: Irrational Element Interaction': ['L3: Abnormal Light and Shadow Effect'], 'L2: Abnormal
Human Anatomy': ['L3: Abnormal Human Anatomy']}}


**InternVL3-8B:**
<think>\nThe image depicts a scene where Bruce Wayne is at a nightclub surrounded by women, holding cocktails and laughing. The first thing to note is
the overall setting and the characters' appearances. The lighting and shadows seem consistent, with no obvious inconsistencies in light direction or
intensity. The characters are drawn with realistic proportions and anatomical features, and their interactions appear logical.\n\nHowever, there are some
elements that might be considered irrational. The women are dressed in revealing outfits, which is somewhat unusual for a character like Bruce Wayne,
who is typically portrayed as more reserved. This could be seen as an irrational element attribute, specifically an abnormal element interaction, as it
doesn't align with typical character behavior.\n\nAdditionally, the presence of multiple women surrounding Bruce Wayne in such a manner might be
considered an irrational element interaction, as it doesn't align with his usual demeanor. The attire and behavior of the women could also be seen as an
abnormal element attribute, as it doesn't conform to typical social norms for such a setting.\n\nThere are no obvious deformities in the human anatomy or
object morphology, and the spatial arrangement seems logical. Therefore, the primary issues are related to the interaction and attributes of the elements
rather than their physical properties or proportions.\n\nConsidering these points, the image has some irrationalities related to the interaction and attributes
of the elements.\n</think>\n\n\\boxed{\n{'Whether Normal': False, 'Type of Abnormality': {'L2: Irrational Element Interaction': True, 'L2: Irrational
Element Attributes': True}}


Figure 9: Model outputs for label “L2: Abnormal Human Anatomy”.


23


Preprint


Lables:

{“Whether Normal”: false,
“Type of Deformity”: {
“L2: Abnormal Animal Anatomy”: [
“L3: Abnormal Limb Structure”]}}


T2I_prompt:
A painting of a velociraptor wielding a lightsaber in his hand, artstation, 8k, high res,
ultra detailed HD. Realistic style.


MagicAssessor-7B:
<think>\nUpon examining the image, the primary subject is a velociraptor holding a lightsaber, which is a fantastical combination given the velociraptor's prehistoric nature and the
lightsaber's science fiction origin. The velociraptor is depicted in a realistic style, with detailed textures and high-resolution features, as specified in the prompt. The velociraptor's
anatomy, excluding the lightsaber, appears consistent with typical depictions of velociraptors in art, with no apparent anatomical deformities. However, the velociraptor's hand
holding the lightsaber is where the potential abnormality lies. The hand structure does not conform to the typical anatomy of a velociraptor, which usually has three fingers on each
hand. Instead, the velociraptor's hand appears to have an extra finger, indicating an abnormal limb structure. This falls under the category of 'Abnormal Animal Anatomy,'
specifically 'Abnormal Limb Structure.' The rest of the image, including the background and the overall composition, seems consistent with the prompt's description and does not
exhibit any other deformities or irrationalities.\n</think>\n\\boxed{{\"Whether Normal\": false, \"Type of Deformity\": {\"L2: Abnormal Animal Anatomy\": [\"L3: Abnormal Limb
Structure\"]}}}


Gemini-2.5-pro:
<think>\nThe user wants me to analyze an image of a dinosaur with a lightsaber and determine if it has any deformities.\n\n1. **Analyze the prompt:** The prompt asks for \"a
painting of a velociraptor wielding a lightsaber in his hand... Realistic style.\"\n2. **Analyze the image:**\n  *  **Subject:** The image depicts a large, bipedal, theropod-like
dinosaur holding a red lightsaber. There is fire and smoke in the background.\n  *  **Realism vs. Fantasy:** The concept itself is fantasy (dinosaur + lightsaber). The style aims
for realism in terms of texture, lighting, and form. The task is to evaluate if the *depiction* is reasonable within its own fantastical context, or if there are clear anatomical or
physical errors in how it's drawn.\n  *  **Anatomy Check:** The prompt specifies a \"velociraptor\". Real velociraptors were much smaller (turkey-sized) and are now widely
believed to have been covered in feathers. The creature in the image is large, scaly, and has a head shape more akin to a Tyrannosaurus Rex or Allosaurus. This is a common popculture misrepresentation, but the key issue for deformity analysis is the structure of the body itself.\n  *  **Limb Structure:** Let's focus on the arms and hands, as the prompt
mentions \"wielding a lightsaber in his hand\". Theropod dinosaurs, including velociraptors, had forelimbs with wrists that could not pronate (turn palm-down) like a human's. They
had a permanent \"clapping\" orientation. The creature in the image is holding the lightsaber with a fully pronated, human-like grip. Furthermore, the arms are incredibly muscular
and proportioned like human bodybuilder arms, rather than the more slender forelimbs of a theropod. This fusion of a dinosaur torso and head with anthropomorphic arms is a
significant anatomical abnormality. It doesn't conform to the normal physiological and anatomical standards of an animal, even a stylized one.\n  *  **Interaction Check:** The
way the creature holds the lightsaber is the primary interaction. Because the arm and hand structure is anatomically incorrect for a dinosaur, the way it interacts with the object
(wielding it) is also presented in an anatomically impossible way for the animal it's supposed to be.\n  *  **Lighting Check:** The lightsaber casts a red glow on the creature's
right side, which is consistent. There appears to be another light source from the top-left. The shadows seem generally plausible. No major issues with light and shadow.\n  *
**Object Morphology Check:** The lightsaber itself looks fine. It's a recognizable hilt with a glowing blade.\n\n3. **Conclusion on Deformity:** The most prominent issue is the
animal's anatomy. The forelimbs are not structured like a dinosaur's. They are human-like in their musculature and in the wrist's ability to pronate to hold the weapon. This falls
directly under the category `L2: Abnormal Animal Anatomy` and the sub-tag `L3: Abnormal Limb Structure`. The posture of holding the weapon is a consequence of this abnormal
limb structure, so `L3: Abnormal Posture Presentation` could also be argued, but the structural deformity of the limb itself is the root cause.\n\n4. **Final Formatting:** The image
is not normal. The type of abnormality is `L2: Abnormal Animal Anatomy`, and the specific sub-tag is `L3: Abnormal Limb Structure`. The final answer should be in the specified
JSON format. The image depicts a dinosaur-like creature, which the prompt identifies as a velociraptor, wielding a lightsaber. While the concept is fantastical, I must assess the
anatomical and physical coherence of the depiction. The creature's overall body plan resembles a large theropod dinosaur, but there is a significant and jarring abnormality in its
forelimbs. Instead of the slender arms and non-pronated wrists characteristic of a theropod, this animal has been given highly muscular, anthropomorphic arms, very similar in
structure and proportion to those of a human bodybuilder. This allows it to hold the lightsaber with a human-like grip, something a real dinosaur's skeletal structure would not permi
This blending of human and dinosaur anatomy results in a creature whose limbs do not conform to the physiological standards of the animal it is meant to represent. Therefore, the
image contains a clear anatomical deformity.\n\n<boxed>\n{'Whether Normal': False, 'Type of Abnormality': {'L2: Abnormal Animal Anatomy': ['L3: Abnormal Limb
Structure']}}\n</boxed>


GPT-4o:

<think>The image depicts a velociraptor, a prehistoric creature, holding a lightsaber in its hand, and this concept inherently introduces a fictional and fantastical element into the
scenario. Since velociraptors do not have hands or a natural anatomical ability to wield objects, the representation of the hands must be examined carefully. The portrayal of the
velociraptor's hands appears anatomically misleading, featuring humanoid muscular arms, which is incongruent with the normal physiology of such an animal. From an anatomical
perspective, the depiction shows an unnatural and distorted limb structure.\n\nAdditionally, the inclusion of a lightsaber raises questions of potential irrationalities in material textur
and lighting interaction. The lightsaber itself emits a glowing, high-energy plasma-like light, but the interaction of this light source with its immediate surrounding does not show
consistent reflections or lighting effects, such as corresponding highlights or colored illumination on the velociraptor’s body. This introduces an abnormality in terms of light and
shadow effects relative to the depicted scene.\n\nThe overall dimensions of the velociraptor’s body are quite robust and appear exaggerated, with proportions that do not align with
most artistic or paleontological portrayals of velociraptors. Specifically, the body muscles, particularly the arms and torso, are overly anthropomorphized, giving the creature an
unrealistic, humanlike physical build that does not align with its animal characteristics. This suggests an exaggeration in proportions.\n\nFocusing on the setting, the background
features smoke and fire, likely to add drama to the scene. However, upon inspection, these effects do not show any meaningful influence on the velociraptor’s lighting, which should
be affected by the intense light of nearby flames. This further illustrates unrealistic light interactions in the environment. Furthermore, considering the tail area where the fire is
located, there is a spatial disconnect, as the fire and velociraptor do not appear physically interconnected or their spatial relationship lacks logical consistency.\n\nThus, there are
anomalies to be highlighted: the abnormal limb structure of the velociraptor as part of animal anatomy deformity, light and shadow inconsistencies introduced by the lightsaber and
fire, and unnatural proportional exaggeration of the velociraptor’s muscular form.</think>\n\n\\boxed{'Whether Normal': False, 'Type of Abnormality': {'L2: Abnormal Animal
Anatomy': ['L3: Abnormal Limb Structure'], 'L2: Irrational Element Interaction': ['L3: Abnormal Light and Shadow Effect'], 'L2: Irrational Element Attributes': ['L3: Abnormal
Element Proportion']}}


Qwen2.5-VL-7B:
The image depicts a velociraptor wielding a lightsaber, which is a combination of a prehistoric creature and a fictional weapon from the Star Wars universe. The velociraptor is
rendered in a highly detailed and realistic style, with vibrant colors and dynamic lighting. The background features a dramatic scene with smoke and fire, adding to the intensity of
the image.\n\nUpon examining the image, the following observations can be made:\n1. The velociraptor is depicted with a lightsaber, which is an element from the Star Wars
universe. This is an irrational element interaction, as velociraptors are not known to wield lightsabers in reality.\n2. The velociraptor's posture and limb structure appear to be
consistent with its biological characteristics, but the presence of a lightsaber introduces an irrational element.\n3. The velociraptor's head structure, including its eyes and ears,
appears normal and consistent with its biological characteristics.\n4. The overall composition and lighting are well-executed, with no apparent abnormalities in the spatial position o
light and shadow effects.\n\nGiven these observations, the image contains an irrational element interaction due to the presence of a lightsaber, which is not a natural attribute of a
velociraptor. The velociraptor's limb structure and head structure appear normal, and there are no other apparent deformities.\n\nTherefore, the answer is:\n\\boxed{'Whether
Normal': False, 'Type of Abnormality': {'L2: Irrational Element Interaction': True}}


InternVL3-8B:

<think>\nThe image depicts a velociraptor wielding a lightsaber, which is an imaginative and fantastical combination. First, I'll assess the overall composition and elements. The
velociraptor is anthropomorphized with a muscular human-like torso, which is an unusual feature for a dinosaur. This anthropomorphization could be considered an irrational
element interaction, as it mixes human and dinosaur characteristics in an unrealistic way.\n\nNext, the lightsaber itself is a sci-fi element, which is not present in the natural world.
This introduces an irrational element attribute, specifically an abnormal material texture, as the lightsaber's material does not match the dinosaur's skin texture. Additionally, the
velociraptor's posture and limb structure appear human-like, which is another abnormal element interaction.\n\nThe background includes flames and smoke, which are not directly
related to the velociraptor, potentially causing an abnormal element interaction. The light and shadow effects seem consistent, so there's no issue there. The velociraptor's head and
limb proportions are exaggerated, which could be seen as abnormal element attributes.\n\nConsidering these points, the image has multiple issues: the combination of a dinosaur
with human-like features, the presence of a sci-fi weapon, and the exaggerated proportions. These issues fall under the categories of irrational element attributes and
interactions.\n</think>\n\n\\boxed{\n \"Whether Normal\": False,\n \"Type of Abnormality\": {\n  \"L2: Irrational Element Attributes\": True,\n  \"L2: Irrational Element
Interaction\": True\n }\n}


Figure 10: Model outputs for label “L2: Abnormal Animal Anatomy”.


24


Preprint


Lables:

{“Whether Normal”: false,
“Type of Deformity”: {
“L2: Abnormal Object Morphology”: true}}


T2I_prompt:
A beautifully arranged flat lay of vintage barbering equipment, including a classic straight razor, a
pair of ornate scissors, and a wooden comb, all set against a rustic wooden table. Soft, natural light
filters in from a nearby window, casting gentle shadows that enhance the textures of the tools. The
background features a blurred out barbershop interior, with leather chairs and a mirror reflecting
the warm ambiance of the space. HD. Realistic style.
MagicAssessor-7B:
<think>\nUpon examining the image, the focus is on the vintage barbering equipment laid out on a rustic wooden table. The elements include a classic
straight razor, ornate scissors, and a wooden comb. The lighting is soft and natural, consistent with the description of gentle shadows enhancing the
textures of the tools. The background features a blurred barbershop interior with leather chairs and a mirror, contributing to the warm ambiance.
\n\nHowever, upon closer inspection, there is an abnormality in the morphology of the scissors. The scissors appear to have an unusual shape, with the
handles and blades not conforming to typical design standards. This suggests a deviation from normal object morphology, as the scissors do not match the
expected geometric shape or construction. \n\nThe rest of the elements, such as the wooden table, the comb, and the barbershop background, seem to be
depicted realistically without any apparent deformities. The light and shadow effects also appear consistent with the described natural lighting.
\n\nTherefore, the primary abnormality in the image is the abnormal morphology of the scissors, which does not align with standard design
expectations.\n</think>\n\\boxed{{\"Whether Normal\": false, \"Type of Deformity\": {\"L2: Abnormal Object Morphology\": true}}}


Gemini-2.5-pro:
\\boxed{{'Whether Normal': False, 'Type of Abnormality': {'L2: Abnormal Object Morphology': True}}}


GPT-4o:

<think>To determine whether this image is normal and free from deformities, I begin by analyzing its adherence to the details mentioned in the prompt.
The image is a flat lay of vintage barbering equipment, showcasing a straight razor, ornate scissors, and a wooden comb, all arranged on a rustic wooden
table. The lighting, described as soft natural light, is consistent with the prompt as it creates gentle shadows that enhance the texture of the tools and the
table. \n\nThe razor, comb, and scissors are realistic in design and scale, showing no deformities in their geometry or proportions. The material texture of
the objects, such as the metal of the razor and scissors or the wood of the comb handles, matches their expected physical properties and qualities. The light
and shadow play appear harmonious and consistent with the direction and intensity of the natural light source, as suggested by the reflections and smooth
gradients created on the table surface.\n\nThe background, featuring a blurred barbershop interior with leather chairs and a mirror, provides an ambient and
warm atmosphere, just as described. There is no evidence of any abnormal interaction between the elements, such as logical inconsistencies in overlap or
spatial positioning. The background elements—even though blurred—are coherent with the barbershop theme and maintain appropriate shapes, textures,
and arrangements.\n\nIn summary, the image conforms to real-world physical laws, proportionality, and visual expectations. There are no irrational
element attributes nor any abnormalities in element interactions. The objects are logically placed, and their attributes, as well as the overall scene
composition, appear perfectly reasonable upon detailed observation. \n\nHence, this image is deemed normal with no deformities.</think>
\n\\boxed{{'Whether Normal': True}}


Qwen2.5-VL-7B:
The image depicts a beautifully arranged flat lay of vintage barbering equipment, including a classic straight razor, a pair of ornate scissors, and a wooden
comb, all set against a rustic wooden table. The background features a blurred out barbershop interior, with leather chairs and a mirror reflecting the warm
ambiance of the space. The lighting is soft and natural, casting gentle shadows that enhance the textures of the tools.\n\nUpon examining the image, the
following observations are made:\n1. The straight razor, scissors, and comb appear to be in proportion to each other and to the table, which is consistent
with real-world expectations.\n2. The materials and textures of the tools (metal, wood, and plastic) are realistic and align with the expected properties of
these items.\n3. The background elements, such as the leather chairs and the mirror, are consistent with a barbershop setting and do not appear to be out of
place.\n4. The lighting and shadows are natural and do not exhibit any inconsistencies that would suggest an unnatural light source or shadow direction.\n5.
There are no elements in the image that appear to be overlapping in an unrealistic manner.\n6. The spatial arrangement of the tools on the table is logical
and does not cause any chaotic layout issues.\n\nGiven these observations, the image appears to be a reasonable representation of the described scene
without any deformities. Therefore, the answer is:\n\n\\boxed{{'Whether Normal': True}}


InternVL3-8B:

<think>\nThe image depicts a flat lay of vintage barbering equipment, including a classic straight razor, a pair of ornate scissors, and a wooden comb, set
against a rustic wooden table. The background shows a blurred barbershop interior with leather chairs and a mirror. The prompt describes a scene with soft,
natural light filtering in from a nearby window, casting gentle shadows that enhance the textures of the tools. \n\nFirst, I'll examine the objects in the image.
The straight razor, scissors, and comb appear to be realistically rendered with appropriate textures and proportions. The wooden table and the leather chairs
in the background also seem consistent with the described setting. The light and shadow effects seem natural, with the light source likely coming from the
window, creating shadows that align with the objects' positions.\n\nNext, I'll consider the background. The blurred barbershop interior with leather chairs
and a mirror reflects the warm ambiance, which fits the prompt's description. The mirror's reflection is consistent with the barbershop setting, and the
leather chairs are appropriately placed.\n\nNow, I'll check for any irrational elements or interactions. The objects are arranged logically on the table, and
their sizes and proportions seem realistic. There are no elements that appear out of place or physically anomalous. The light and shadow effects are
consistent with the light source, and there are no unnatural overlaps or spatial inconsistencies.\n\nConsidering all these factors, the image appears to be
reasonable and aligns with the provided text prompt. There are no deformities or irrationalities in the image.\n</think>\n\n\\boxed{answer: {'Whether
Normal': True}}


Figure 11: Model outputs for label “L2: Abnormal Object Morphology”.


25


Preprint


Lables:

{“Whether Normal”: false, “Type of Deformity”: {“L2: Irrational Element Interaction”:

[“L3: Abnormal Element Overlap”, “L3: Abnormal Spatial Position”]}}


T2I_prompt:
A hyper-realistic depiction of a polished wooden pool cue resting on a green felt billiard table.
The scene captures the intricate details of the cue's grain and finish, with soft lighting reflecting
off its surface. In the background, a set of colorful billiard balls is arranged in a triangle, with a
cue ball positioned at the front, ready for the break. The atmosphere is warm and inviting, with
shadows playing across the table, enhancing the realism of the scene.


MagicAssessor-7B:
<think>\nUpon examining the image, the primary focus is on the polished wooden pool cue resting on the green felt billiard table. The prompt describes a
hyper-realistic depiction with intricate details of the cue's grain and finish, and soft lighting reflecting off its surface. The background features a set of
colorful billiard balls arranged in a triangle, with a cue ball positioned at the front. The atmosphere is described as warm and inviting, with shadows
playing across the table, enhancing the realism of the scene.\n\nUpon close inspection, the pool cue appears to be resting naturally on the table, and the
grain and finish are depicted with high detail, consistent with the prompt. However, there is a noticeable issue with the cue ball. The cue ball is positioned
in a way that suggests it is resting on the tip of the pool cue, which is not a typical or logical position for a cue ball in a billiard setup. In a standard
arrangement, the cue ball is positioned at the front of the triangle of balls, ready for the break, but here it appears to be in an unusual position that does not
conform to the expected setup.\n\nThis abnormal positioning of the cue ball leads to a conclusion that there is an irrational element interaction, specifically
an abnormal spatial position, as the cue ball's placement does not align with the typical setup of a billiard table. This suggests a deformity in the spatial
arrangement of the elements within the image.\n\nTherefore, the image contains an abnormality related to the spatial positioning of the elements,
particularly the cue ball's position on the pool cue, which does not conform to the expected physical laws and setup of a billiard
table.\n</think>\n\\boxed{{\"Whether Normal\": false, \"Type of Deformity\": {\"L2: Irrational Element Interaction\": [\"L3: Abnormal Spatial
Position\"]}}}


Gemini-2.5-pro:
I am examining the image provided, which is supposed to be a hyper-realistic depiction of a billiard table set up for a game. The prompt specifies a
polished wooden cue, a green felt table, and a rack of colorful billiard balls with a cue ball ready for the break.\n\nAt first glance, the image is visually
impressive. The texture of the green felt is detailed, the wooden grain on the pool cue is well-defined, and the reflections from the polished surfaces of both
the cue and the balls are rendered realistically. The soft lighting and shadows create the warm, inviting atmosphere described in the prompt. The individual
objects, such as the cue and the balls, appear morphologically correct.\n\nHowever, upon closer inspection of the scene's overall logic, a significant
irrationality becomes apparent. The scene is described as \"ready for the break.\" In any game of pool, this setup requires a cue ball (typically white) to be
placed separately from the racked object balls. The player then uses the cue stick to strike the cue ball, which in turn hits the rack. In the generated image,
the cue ball is conspicuously absent. Instead, the pool cue itself is lying on the table with its tip resting directly against the front ball of the triangular rack.
This arrangement is fundamentally incorrect and nonsensical in the context of the game. One does not initiate a break by touching the racked balls directly
with the cue. This represents a misunderstanding of the spatial and logical relationships between the elements in a game of pool.\n\nThis error falls under
the category of 'L2: Irrational Element Interaction', as the interaction and arrangement between the cue and the racked balls defy the rules and logic of the
activity being depicted. More specifically, it aligns with the sub-tag 'L3: Abnormal Spatial Position', because the logical arrangement of the elements in
space is inconsistent with the described situation. The cue is in a position it would never occupy for a break shot, and the crucial element of the cue ball is
missing, making the entire spatial layout of the game setup illogical.\n\n\\boxed{\n \"Whether Normal\": false,\n \"Type of Abnormality\": {\n  \"L2:
Irrational Element Interaction\": [\n   \"L3: Abnormal Spatial Position\"\n  ]\n }\n}


GPT-4o:
<think>The image depicts a wooden pool cue resting on a green billiard table, accompanied by a triangular arrangement of colorful billiard balls and a cue
ball positioned at the front. To determine whether the image is reasonable and free of any deformities, I first examine the pool cue itself. Its polished
wooden surface appears hyper-realistic, with accurate wood grain texture and a reflective finish consistent with the description provided. The cue adheres
to realistic proportions, without any distortions in its shape.\n\nNext, I assess the green felt of the billiard table. The texture and lighting are consistent with
expectations, showing realistic shadows cast by the pool cue and surrounding elements. The triangular arrangement of balls is correctly formed, with no
physical irregularities or violations of spatial laws. The cue ball does not exhibit any deformities, appearing properly shaped and
positioned.\n\nAdditionally, the interplay of light and shadow enhances realism without presenting any inconsistencies. The reflections and shadows align
with the lighting direction, maintaining logical physics. The background details, including portions of the table and the environment visible in the scene,
are coherently depicted without unexpected anomalies.\n\nAs I continue examining the image for potential deformities across all categories, including
object morphology, irrational element attributes, light and shadow effects, and spatial positioning, everything conforms to physical laws and expected
realism. There are no abnormalities in proportions, textures, or interactions between elements. The image maintains fidelity to its hyper-realistic intent,
matching the corresponding text prompt perfectly.\n\nAfter thorough scrutiny, I find no signs of deformity or irrationality, indicating the scene is entirely
plausible and visually accurate.</think>\n\n\\boxed{{'Whether Normal': True}}"


Qwen2.5-VL-7B:
The image depicts a polished wooden pool cue resting on a green felt billiard table. The cue's grain and finish are intricately detailed, and the soft lighting
reflects off its surface, creating a warm and inviting atmosphere. In the background, a set of colorful billiard balls is arranged in a triangle, with a cue ball
positioned at the front, ready for the break. Shadows play across the table, enhancing the realism of the scene.\n\nUpon examining the image, there are no
apparent deformities in the visual attributes of the elements. The material texture of the pool cue matches the actual properties of wood, and the
background elements, such as the billiard balls and the table, are arranged in a logical and realistic manner. The spatial and logical interactions between the
elements are consistent with the expected behavior of a billiard table and its accessories. The light and shadow effects are natural and do not appear
inconsistent with the light source position and intensity.\n\nTherefore, the image is reasonable and does not exhibit any deformities.\n\n\\boxed{answer}


InternVL3-8B:
<think>\nThe image depicts a polished wooden pool cue resting on a green felt billiard table. The scene is hyper-realistic, with detailed textures and soft
lighting. The pool balls are arranged in a triangle, and the cue ball is positioned at the front, ready for the break. The lighting and shadows are consistent,
creating a warm and inviting atmosphere. \n\nFirst, I'll check for any irrational element attributes. The pool cue's grain and finish look realistic, and the
material texture matches the actual properties of wood. The colors of the billiard balls are vibrant and natural, adhering to real-world color theory. The
proportions of the objects seem correct, with no elements being disproportionately large or small. \n\nNext, I'll examine the interaction between elements.
The light and shadow effects are consistent, with the shadows cast in a logical direction relative to the light source. The arrangement of the pool balls and
the cue on the table is realistic and follows expected spatial relationships. There are no overlaps or spatial inconsistencies that defy physical laws.
\n\nConsidering the overall layout, the scene is well-organized, with no chaotic or unrealistic positioning of objects. The image does not contain any
human or animal elements, so I can disregard those categories. \n\nAfter evaluating all aspects, the image appears to be reasonable without any
deformities.\n</think>\n\n\\boxed{answer: {'Whether Normal': True}}


Figure 12: Model outputs for label “L2: Irrational Element Interaction”.


26


