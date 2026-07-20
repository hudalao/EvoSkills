## **mCLM: A Function-Infused and Synthesis-Friendly** **Modular Chemical Language Model**

**Carl Edwards** [1] _[∗]_ **Chi Han** [1] _[∗]_ **Gawon Lee** [2] **Thao Nguyen** [1] **Bowen Jin** [1]


**Chetan Kumar Prasad** [2] **Sara Szymku´c** [4] **Bartosz A. Grzybowski** [5] _[,]_ [6] **Ying Diao** [3]


**Jiawei Han** [1] **Ge Liu** [1] **Hao Peng** [1] **Martin D. Burke** [2] **Heng Ji** [1]


**Abstract**


Despite their ability to understand chemical knowledge and accurately generate
sequential representations, large language models (LLMs) remain limited in their
capacity to propose novel molecules with drug-like properties. In addition, the
molecules that LLMs propose can often be challenging to make in the lab. To more
effectively enable the discovery of functional small molecules, LLMs need to learn
a molecular language. However, LLMs are currently limited by encoding molecules
from atoms. In this paper, we argue that just like tokenizing texts into (sub-)word
tokens instead of characters, molecules should be decomposed and reassembled at
the level of functional building blocks, i.e., parts of molecules that bring unique
functions and serve as effective building blocks for real-world automated laboratory
synthesis. This motivates us to propose mCLM, a modular Chemical-Language
Model tokenizing molecules into building blocks and learning a bilingual language
model of both natural language descriptions of functions and molecule building
blocks. By reasoning on such functional building blocks, mCLM guarantees to
generate efficiently synthesizable molecules thanks to recent progress in blockbased chemistry, while also improving the functions of molecules in a principled
manner. In experiments on 430 FDA-approved drugs, we find mCLM capable
of significantly improving 5 out of 6 chemical functions critical to determining
drug potentials. More importantly, mCLM can reason on multiple functions and
improve the FDA-rejected drugs (“fallen angels”) over multiple iterations to greatly
improve their shortcomings. [†]


**1** **Introduction**


Small molecules—the class of chemical matter primarily built from carbon atoms bonded together—can perform a wide range of important functions in human society. These include essentials
like promoting health by acting as medicines [ 125, 20, 81, 90, 110 ], converting energy by functioning
as key components in solar cells [ 69, 65, 48, 49, 79 ], and achieving sustainability by serving as
inherently recyclable products. These functions also include many nice-to-haves that drive substantial
economic growth, including acting as colorants, flavorings, perfumes, cosmetics, lotions, sunscreens,
coatings, quantum dots, molecular computers, chemical biology probes, insect repellants, etc.


_∗_ Equal contribution. 1 Siebel School of Computing and Data Science, University of Illinois UrbanaChampaign, [2] Department of Chemistry, University of Illinois Urbana-Champaign, [3] Department of Chemical
and Biomolecular Engineering, University of Illinois Urbana-Champaign, [4] Allchemy Inc., [5] Ulsan National Institute of Science and Technology, [6] Institute of Organic Chemistry, Polish Academy of Sciences. Correspondence:
`cne2@illinois.edu`, `chihan3@illinois.edu`, `hengji@illinois.edu`, `mdburke@illinois.edu`

   - All codes, data, and models will be released publicly upon publication.


Preprint.


Figure 1: mCLM adopts a modular chemical vocabulary, which uses molecular _modules_ as tokens
together with natural language tokens. Note that we also refer to these modules as “building blocks”.
Compared with using natural language names, SMILES strings, or holistic embeddings for whole
molecules, this level of tokenization aligns better with molecular function groups. It allows more
efficient molecular structure modification and synthesis.


A major challenge with small molecules, however, is that the traditional approach for small molecule
synthesis is highly artisanal, slow, and expensive. It considers all possible arrangements of atoms
and centers on creating for each targeted molecule a unique process for its assembly that leverages
a menu of thousands of different reactions each run under thousands of possible conditions and
using millions of possible starting materials. This approach imposes several limitations: (1) It is
unfriendly to automation – machines are not good at doing thousands of different things thousands of
different ways from a million different starting points. (2) It leads to an undemocratized landscape in
drug discovery. With development costs averaging around $1.3 billion per drug, only economically
advanced countries can afford to invest in such high-risk research [ 41 ]. Moreover, participation in
the process of molecular innovation currently requires access to highly trained experts in chemical
synthesis. (3) Most importantly, there are many instances of known commercial drugs or materials
that have well-documented limitations that have remained unaddressed. For example, Imatinib is an
important anticancer drug that works well in most parts of the body, but it only poorly penetrates the
blood-brain barrier [ 87, 77, 14, 36 ]. This means it may effectively treat cancer at its primary site, yet
fail to prevent fatal brain metastasis. In such cases, more blood-brain-barrier penetrant molecules that
retain all of the other favorable properties of the current drug are desired, but making such selective
modifications in functional properties can be very challenging. As another example in the materials
domain, organic photovoltaic (OPV) molecules are expected to be more economical and environmentfriendly alternatives to current solar cells. However, current commercialized OPV devices either
achieve less than 10% energy conversion efficiency—significantly lower than traditional silicon solar
cells—or have stability far short of 10 years [ 82 ]. Overcoming these types of drawbacks of current
molecules remains a challenging problem in the domain.


An alternative block-based chemistry approach for small molecule synthesis has recently emerged [ 28,
107, 50, 45, 92, 8, 4, 100, 84 ], and we recognized that this approach provides an opportunity to
reimagine the intersection of AI and small molecule science. Block-based chemistry is chemistry
that machines can do. It iteratively assembles small molecules from prefabricated building blocks
using chemistry that is simple and general and thus readily automated. Akin to automated DNA,
RNA, and peptide synthesis platforms, a major strength of this block-based approach is that it can
access billions of novel small molecules with high degrees of functional potential using only a few
automation-friendly reactions and a bounded set of pre-fabricated function-infused building blocks.


We specifically recognized that this block-based approach provided an opportunity to create a new
modular language for chemistry. The idea that molecules and their synthesis may be best understood
from the perspective of a “chemical language” dates back to 2014 [ 11 ], where structural fragments
and functional groups play the roles of “chemical words”. This view is supported by multiple
observations aligned with natural language: (1) they can be decomposed and reassembled, (2) they


2


exhibit ambiguity—the same building block can perform vastly different functions depending on the
chemical context, and (3) they possess significant diversity, as many different structures can lead
to the same function. This linguistic parallel suggests the potential to train a large language model
specifically for molecules by linearizing their structures into modular sequences.


A common representation for such an approach is the Simplified Molecular Input Line Entry System
(SMILES) [ 104 ], where atoms are denoted by one- or two-character symbols (e.g., C for carbon, Br
for bromine, and F for fluorine), rings are represented with numbers, and branches are indicated using
parentheses. However, such atom-level tokenization strategies (e.g., SMILES [ 104 ] or SELFIES

[ 43 ]) resemble character-level natural language models, which struggle to generalize effectively.
Unlike proteins, which have a fixed vocabulary of 20 amino acids, small molecules exhibit an open
vocabulary when each atom is treated as a token, as illustrated in Figure 1. It also causes severe
restrictions in practicality because many of the new structures proposed by LLMs based on atom-level
tokenization are not practically synthesizable in the laboratory. This approach has created a major
gap between what is now possible in silico and what is possible in the physical world.


Furthermore, the SMILES representation can obscure critical structure information: two atoms that
are direct neighbors in the molecular graph may be distantly separated in the SMILES string. Even
with recent efforts to align SMILEs and natural language description [ 17, 73, 2 ], integrate chemical
properties and functional groups [ 71 ] into SMILES, incorporate 3D geometric information [ 25, 54 ],
and employ graph neural networks to capture molecular graphs and chemical reaction contexts [ 97 ],
these representations still fail to encapsulate functional knowledge that is often described only in
natural language literature because the inherent properties and functions of molecules are hidden in
their structure, composition, and interaction.


Against this backdrop, we argue that there is a correctable fundamental mismatch between the way
LLMs work and the way chemists traditionally synthesize and study small molecules. Increasing
the “tokenization granularity” down to the corresponding letters is not helpful, and in fact makes
the extraction of meaning much more complex and causes generative AI to hallucinate words that
don’t exist. To bridge this gap, in this paper, we aim to teach computers to speak two complementary
languages: one that represents molecular building blocks (i.e., subgraph structures) indicative of
specific functions and compatible with automated modular assembly, and another that describes these
functions in natural language (Figure 2). Unlike existing approaches that add such knowledge as a post
hoc step, we developed a function- and synthesis-aware modular chemical language model (mCLM).
Inspired by bilingual speakers who frequently “code-switch” (naturally and often switch between
their two languages within the same message), we propose a novel neural encoder that integrates
molecular structure and natural language. mCLM incorporates both function- and synthesis-related
knowledge into the small molecule tokenization process a priori.


First, we tokenize small molecules at the level of building blocks (graph substructures) that are better
able to predict function and are, by design, fully compatible with automated modular small molecule
synthesis. We use graph neural networks to encode each building block. We then extract natural
language sentences from the literature that describe the molecule’s functions and chemical reactions
and synthesis constraints of various molecules, and seamlessly insert the encoded building blocks
alongside the corresponding entity names, as illustrated in Figure 2. During the inference stage,
mCLM enables these functional modules to be predictably and automatically assembled into new
molecules with desired functions.


mCLM has multiple potential advantages of encoding and generating molecules at a modular level:


1. **Synthesis efficiency** : synthesis can be faster and more broadly accessible because the
process is, by design, simple, iterative, general, and machine-friendly. This can enable rapid
iterative drug and material development and even automated lab experiments.


2. **Alignment with language models** : resembling the mechanism of natural language tokenization, molecular modularization provides a more natural interface to align with word
representations.


3. **Reasoning** : leveraging LLMs’ instruction following capability and wide-scale pretraining,
mCLM is able to iteratively refine molecules based on knowledge of molecular functions.


3


**2** **The Modular Chemical Language Model**


**2.1** **Overview**





























Small molecules pose unique challenges to tokenize and encode due to their perceived open-ended
structural diversity. This has caused the field to consider them differently from natural language
where well-defined vocabularies exist. In natural language modeling, tokenization identifies common
substrings (such as words and subwords), which carry richer semantic information than sequences of
characters. We note that most small molecules that occur in nature are similarly composed primarily
of connected _building blocks_ [ 45, 92 ]. There is likewise a high degree of inherent modularity in many
medicines and materials [ 23, 22, 3, 5, 45, 92, 95 ]. We propose mCLM, a multimodal model that
jointly encodes and understands natural language and molecules based on synthesis-friendly building
blocks instead of atoms. In Section 2.2, we introduce the concept of molecular building blocks as
a chemical “vocabulary” in addition to the natural language vocabulary we use. Section 2.3 then
describes the tokenization process to obtain the library of building blocks. Then in Section 2.4 we
describe how the mCLM trains and runs on the token sequences. Finally, we introduce the reasoning
mechanism of mCLM which refines molecule design over multiple iterations in Section 2.5.


4


**2.2** **A Function-Infused and Synthesis-Friendly Vocabulary**


In this work, we propose to leverage a chemical vocabulary of synthesis-friendly building blocks. This
approach guarantees capacity for automated iterative assembly [ 51 ]. The blocks can be chemically
connected using predefined synthesis rules in a short period. In particular, we propose a chemically
meaningful vocabulary, _V_ . Briefly, akin to language models developed for peptides/proteins, small
molecules can be assembled automatically from accessible building blocks. These building blocks
are often highly associated with chemical functions, such as binding to protein targets, modulating
enzyme activity, or affecting involved metabolic processes. This will enable rapid and iterative
proposal of new small molecules, automated synthesis of those small molecules, and generation of
the corresponding functional data on demand. Notably, in contrast to SMILES strings which break
molecule structure during graph linearization (e.g., separating physically adjacent subgraphs such as
the two carbons in molecule C(N)C), our representation is linear in the physical world.


**2.3** **Tokenization**


Figure 3: An overview of the tokenization process. A functional molecule is first processed by
the synthesis-guaranteed tokenizer to produce a set of building blocks compatible with automated
modular synthesis. These blocks are then evaluated via a structure coverage check to determine
whether they fully reconstruct the original molecule. If coverage is complete, the blocks are used
directly for pretraining. Otherwise, the molecule is reprocessed using a rule-based tokenizer to ensure
full representation for training purposes.


To generate molecules that are not only valid but also automatically synthesizable, we tokenize
molecular inputs into molecular “building blocks” (i.e., subgraphs) that align with known chemical
synthesis procedures. During training, we combine two tokenization strategies to balance coverage
and synthetic feasibility: a synthesis-guaranteed tokenizer and a rule-based tokenizer (Figure 3).
The synthesis-guaranteed tokenizer disconnects the molecule only at bonds that can be formed by a
predetermined small set of reactions that can be performed in an automated manner. Specifically,
it only permits bond disconnections that correspond to reactions compatible with state-of-the-art
automated synthesis platforms. These three bonds are: amide coupling, Suzuki-Miyaura coupling, and
Buchwald-Hartwig coupling (see Figure 3 tokenization rules) [ 93 ] . Unlike traditional retrosynthesis
tools that prioritize maximum coverage or human-designed heuristics, this tokenizer is guided by
the operational constraints of block-based chemistry. It also ensures that resulting blocks are free
from functional group conflicts that would interfere with downstream synthesis. Please see Appendix
D.1 for more information. This conservative approach leads to a set of molecular tokens that are
guaranteed to work under defined synthesis protocols, enabling seamless transition from modelgenerated output to real-world synthesis. When the synthesis-guaranteed tokenizer cannot fully cover
a molecule—due to chemical incompatibilities or reaction constraints—we fall back on a rule-based
tokenizer to ensure coverage of a larger variety of molecules. The rule-based tokenizer also breaks
molecules along the same automated machine-friendly bonds as the above tokenizer. However, no
other rules are applied beyond specifying a minimum size for blocks. This rule-based tokenizer


5


is used only during training to support learning on diverse molecular structures while maintaining
consistency with synthesis logic.


**2.4** **Chemical-Language Modeling**


Figure 2 illustrates the architecture of mCLM. The model is a sequential generative model that
processes molecule and text sequences in a unified manner. It adopts a Transformer architecture,
which is well-suited for handling sequential data and allows for using pre-trained language models
as a backbone. After tokenizing the molecules as mentioned in the last section, we encode each
building block using graph neural networks (GNNs) [ 19, 83, 26 ]. These representations are then
concatenated with natural language embeddings at positions where molecule entity names appear.
This results in a form of “code-switched” language which blends molecular structures with natural
language descriptions. The feature sequence is then fed into a Transformer decoder-only architecture,
which predicts the next token based on previous tokens. This allows for pre-training the model on a
large corpus of multi-modal data, enabling it to learn and “talk about” the relationships between the
different modalities and their respective representations.


We train this model—mCLM—on top of open-source large language models pretrained on generaldomain corpora, allowing us to leverage their linguistic capabilities without incurring the computational cost of training from scratch. As the training objective, we adopt a unified categorical
cross-entropy (CCE) loss applied to both natural language and molecular tokens:


_⊤_
**c** **e** _v_ _, v ∈V_ natural language
_L_ = _H_ ( _P_ ( **X** ) _, P_ _θ_ ( **X** )) _,_ logit( _P_ _θ_ ( _v |_ **X** 1 _···i−_ 1 )) =
� **c** _[⊤]_ _f_ _θ_ (GNN _θ_ ( _v_ )) _, v ∈V_ molecular building block


Specifically, the loss is computed between the ground truth distribution _P_ ( **X** ) and the model-predicted
distribution _P_ _θ_ ( **X** ) over the combined vocabulary of natural language and molecular building blocks.
The model generates logits for the next token _v_ by computing the dot product between the contextual
representation **c** with token embeddings. **c** is produced by the Transformer given the previous tokens
**X** 1 _···i−_ 1 = [ _X_ 1 _, · · ·, X_ _i−_ 1 ]) . For natural language tokens, the embedding **e** _v_ is directly taken from
the pretrained natural language model. The embedding for molecular building blocks is computed by
passing the building block’s graph through a GNN, followed by a linear adapter function _f_ _θ_ to project
it into the same embedding space. This formulation enables joint training over both modalities using
a single loss function. More detailed training procedure is described in Appendix C.


**2.5** **Critical Chemical Reasoning**


Chemical reasoning over molecules often involves optimization of multiple functions, such as
toxicity, bioactivity, binding affinity, etc. Therefore, it is not a straightforward task to propose an
ideal molecule structure, especially with only a single attempt. In nature, organisms evolved over
billions of years to produce complex molecules that are optimal for their use. Additionally, many
functions positively or negatively correlate with each other. Optimizing one function may lead to
trade-offs in others. For example, many drugs with higher potency were rejected due to increased
toxicity to patients. To address this, we propose a reasoning process that allows the model to refine
its own generated molecules and iteratively improve their desired functions. At each step, mCLM
proposes a modification of the molecule for improvement by considering one or more functions and
self-evaluates the effect of the proposed modification. Then in the next iteration, mCLM identifies
those functional building blocks that still have room for improvement. This process is repeated
until a maximum number of iterations is reached, or if mCLM fails to find additional reasonable
modifications. As illustrated in Figure 2, this process can be summarized in the following algorithm:


**3** **Experimental Evaluation**


**3.1** **Creating Oracle Models for Evaluation**


To evaluate the performance of our generated molecules, we construct oracle models focused on
Absorption, Distribution, Metabolism, Excretion, Toxicity (ADMET) property prediction. We select
6 tasks from the Therapeutics Data Commons (TDC) benchmark [ 33 ]: **AMES** (mutagenicity), **BBBP**
(blood-brain barrier permeability), **CYP3A4** inhibition (metabolism), **DILI** (drug-induced liver
injury), **HIA** (human intestinal absorption), and **PGP** (P-glycoprotein substrate classification).


6


**Algorithm 1** Critical Chemical Reasoning for Molecule Design in mCLM


1: **Input:** Initial molecule _M_ 0
2: **Output:** Refined molecule _M_ _[∗]_

3: Initialize _M ←_ _M_ 0
4: **while** True **do**
5: Enumerate over functions to improve in _M_ (e.g., metabolism, drug-induced organ injury,
blood-brain barrier penetration)
6: **if** No clear objective remains for improvement **then**
7: **return** _M_

8: **end if**
9: mCLM generates a candidate modification _M_ _[′]_ by replacing, adding, or removing building
blocks in _M_
10: mCLM evaluates _M_ _[′]_ with respect to desired functions
11: **end while**


Models are trained using predefined scaffold-based data splits with an 8:1:1 ratio for train, validation,
and test sets. The detailed training procedure is described in Appendix B.2.3. We opt to use robust
foundation models—FARM [ 71 ], ChemBERTA-2 [ 2 ], and a GNN [ 19 ]—for ensemble learning. To
build the ensemble, we use each model as a feature extractor. The extracted features are concatenated
and passed through a fully connected layer for final prediction.


**3.2** **Improving FDA-Approved Drugs with Out-of-Vocabulary Blocks**



As a large-scale test, we apply the
mCLM to improve all FDA-approved
drugs consisting of at least 3 blocks.
This amounts to 430 molecular struc
tures and 796 unseen blocks. Since most
of these molecules (426/430) contain
blocks that were not present in the 1,000
blocks used for training, this presents an
opportunity to find how the mCLM performs out-of-distribution. Results in Table 1 show that improvement is achieved
for 5/6 properties, even though the model
has not seen almost half of the blocks in
its vocabulary during training.



**Property** **FDA Drug** **Modified**


AMES Mut. ( _↓_ ) 59.5 **54.0**
CYP3A4 Inhib. ( _↓_ ) 2.0 **1.2**
BBBP ( _↑_ ) 37.6 **41.4**
HIA ( _↑_ ) 93.2 **97.6**
DILI ( _↓_ ) 66.2 **55.5**
PGP ( _↓_ ) **66.0** 68.0


Table 1: Average pharmacokinetic and toxicity properties of FDA drugs with 3 or more blocks and their
proposed modifications. ( _↓_ : lower is better, _↑_ : higher is
better; p < 0.05 by Wilcoxon Test [105, 74].)



**3.3** **Case Study: Multi-step Critical Reasoning to Resurrect the “Fallen Angels”**


In a similar vein, there are many new drug candidates that almost make it to FDA approval but fall
short for various reasons when being tested in clinical trials. For example, Evobrutinib is a Bruton’s
tyrosine kinsase (BTK) inhibitor that went through clinical trial as a drug for relapsing Multiple
Sclerosis. However, the FDA placed a partial clinical hold on Phase III trials in April 2023 after
two patients showed signs of drug-induced liver injury [ 67 ]. TNG348 is a USP1 inhibitor designed
for treating BRCA1/2-mutant and HRD cancers, but it failed in phase 1/2 clinical trials due to liver
abnormalities [ 35, 80 ]. These “fallen angels” represent tremendous opportunities for impactful
engagement of the AI/chemistry interface, because much is known about the strengths of each of
these small molecules, and it is also known why they fell short. Fixing such fallen angels is a high
leverage opportunity for the function-infused and synthesis-friendly mCLM to contribute. Herein we
demonstrate this potential with some real-world examples of fallen angels that can be optimized with
mCLM. Importantly, and uniquely, all of the new compounds proposed by mCLM are, by design,
well-suited for rapid automated assembly using robots.


Figure 4 shows an application of the mCLM to these two molecules. For both, the inital step is to
optimize DILI, the reason the drugs failed in clinical trials. Following that, the mCLM is applied to fix
other properties which were made worse in the previous attempt (PGP for Evobrutinib and BBBP for
TNG248). For good measure, another property of each molecule is then improved. Notably, at each


7


Decrease DILI Decrease PGP



Decrease AMES



**Drug:**

- Evobrutinib

**Target:**

- BTK

**Reason for**

**Failure:**

- Liver

Toxicity


**Drug:**

 - TNG348

**Target:**

 - USP1

**Reason for**

**Failure:**

 - Liver

Toxicity



















Decrease DILI Increase BBBP



Decrease CYP3a4



Figure 4: Examples of fallen angel property modification.


step, the mCLM only makes minor modifications to each drug of roughly 1 building block. While
the mCLM shows promising results for repairing these drugs, it is worth noting that drug discovery
is a many-objective optimization problem. While we are able to generate proposed molecules with
improved toxicity relative to Evobrutinib and TNG348, as well as other properties, yet other important
properties may still have been compromised. Future work may want to investigate longer reasoning
chains across a wider variety of properties.


**3.4** **Library Design: Identifying Functionally-Important Blocks**



One notable thing about the architecture of the
mCLM is the ability to identify blocks which are
preferred for certain functions. This can help
inform virtual screening campaign design (e.g.,
which 10 blocks should we use to get the best
chemical space for BBBP?), and it can also be
useful for stimulating scientific inquiry. As an
example, Figure 5 shows the most frequent modifications preferred by the mCLM for improving
DILI in FDA drugs. Interestingly, these modification tend to be small changes from the original
molecule block.


**4** **Related Work**


**4.1** **Applying LLMs**
**to Chemical Representation and Discovery**



**mCLM**
**Before** **After**



Following their success in general natural language processing tasks [ 123 ], large language models (LLMs) have been increasingly adopted for
solving a wide range of problems in computational chemistry [ 116, 119 ]. Existing efforts can Figure 5: Four of the most frequent mCLMbe broadly categorized into two groups based proposed modifications to improve DILI in FDAon molecular representation: (1) SMILES-based approved drugs.
modeling [ 24, 61, 72, 124 ], and (2) graph-based
modeling [ 59 ]. For SMILES-based approaches, MolT5[ 18 ] introduces a multimodal language model


8


that jointly understands and generates textual and SMILES representations. GIMLET[ 122 ] unifies
graph and textual information using a distance-aware graph-text Transformer. LlaSMol[ 115 ] is
instruction-tuned for property prediction and molecular description. DrugAssist [ 114 ] explores
interactive molecule optimization by enabling LLMs to perform goal-driven modifications through
human-in-the-loop dialogue. Graph-based approaches aim to capture molecular structure more
explicitly. MolCA [ 59 ] integrates graph encoders with Galactica [ 89 ] using a cross-modal projector.
3D-MoLM[ 53 ] extends this paradigm to 3D molecular structures by incorporating a 3D molecular
encoder. Llamole[ 55 ] further advances this direction by enabling interleaved generation of text and
molecular graphs, supporting applications such as retrosynthetic planning and molecular inverse design. However, most molecule language models tokenize at the level of atoms [ 99, 2, 126, 109 ] and/or
they do not infuse synthesis considerations up front, which precludes matching tokens with desired
functions and/or leads to AI- generated new molecular targets that are not readily synthesizable.


**4.2** **Functional Groups/Fragments**


Functional groups/fragments are core structural motifs that govern molecular reactivity, biological
activity, and physicochemical properties, forming the basis of chemical understanding [ 23, 75, 39 ].
Their study has propelled advances in medicinal chemistry, natural product research, and material
science by guiding synthesis and performance optimization [23, 22, 3, 5].


Given their interpretability and functional relevance, functional groups/fragments are also increasingly being incorporated into machine learning models for molecular representation [ 46, 70, 29, 38,
68, 102, 118, 120 ]. Some approaches employ a masking strategy for masked atom prediction by
simultaneously masking all atoms within a functional group, applied to both molecular graph and
SMILES representations [ 103, 46 ]. Other approaches include augmenting SMILES strings with functional group annotations [ 68 ], building functional group-level graphs [ 68 ], or leveraging hierarchical
architectures that model both atomic-level and functional module-level representations [29, 70].


Our work goes beyond mere chemical representation by attempting to encode molecules at the
building-block level within natural language LLMs, paving the way for chemical reasoning. These
methods also often overlook the synthesizability of molecules. They tend to break molecules at
bonds that are difficult to form through chemical reactions, resulting in generated molecules that
are challenging—or even impossible—to synthesize using standard reaction pathways. This gap
limits the practical applicability of the learned representations, especially for tasks such as molecular
generation or optimization.


**4.3** **Multimodality, Multilinguality and Code-Switching in LMs**


This work is also inspired by exploration in enabling LLMs to understand multiple languages [ 34, 10,
117, 15, 91 ] or data modalities such as vision and audio [ 52, 1, 57, 64, 98, 96, 113, 13, 101, 12, 88,
111 ]. [ 32 ] fed genome sequences to LLMs and found them capable of suggesting common functions
for gene sets while also providing interpretable rationales. Explorations on proteins [ 60, 78 ] show
success in protein-to-text and text-to-protein generation in applications including antibody design
and protein understanding. This work is also related to other recent studies that have explored the
integration of graph neural networks (GNNs) as feature vectors into LMs capture both textual and
structural information [59, 122, 37].


**5** **Conclusions and Future Work**


In this work, we propose the modular Chemical-Language Model, which is the first attempt to jointly
model natural language sequences with modular chemical language. mCLM is capable of conducting
critical chemical reasoning by iteratively refining molecule designs over diverse objectives and
chemical knowledge. Future work could incorporate richer information such as 3D structures of
molecules and physical constraints into mCLM representation. Other modalities such as protein and
nucleic acid sequences will further enable mCLM to reason on biological activity, protein docking
knowledge, and individuals’ genetic profiles. Future efforts could also extend chemical reasoning to
additional aspects such as collecting and leveraging results from physical simulation tools, including
protein interaction dynamics, retrieval from chemical and reaction knowledge bases, etc. Another
important direction is to introduce multi-agent interactions with other AI agents, human scientists,
and automatic laboratories, where proposed molecules can be efficiently synthesized using modular
chemistry technologies. There is also great potential in including alternative scientific hypothesis


9


generation and plausibility prediction. In the long-term, we envision a landscape where mCLMs can
be included in a more comprehensive chemical research workflow consisting of fully automated and
never-ending reasoning - proposal - synthesis - physical testing - feedback - reasoning loops. mCLM
can serve as a preliminary step in bridging AI and physical world experiments, shattering the barriers
that currently preclude non-specialists in organic synthesis from meaningfully participating in small
molecule innovation.


**Acknowledgments and Disclosure of Funding**


We would like to thank Kyunghyun Cho, Anna Hart, Hyeonjeong Ha, Gabriele Scalia, Yanru Qu,
and Jeonghwan Kim for helpful discussion. This research is based upon work supported by the
Molecule Maker Lab Institute: an AI research institute program supported by NSF under award
No. 2019897, and IBM-Illinois Discovery Accelerator Institute (IIDAI) Center. The core idea of
decomposing-and-reassembling functional parts into novel concepts is inspired by research supported
by the U.S. DARPA ECOLE Program No. HR00112390060. Any opinions, findings, conclusions, or
recommendations expressed in this material are those of the authors and do not necessarily reflect
those of the National Science Foundation.


10


**References**


[1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman,
Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _ArXiv_
_preprint_, abs/2303.08774, 2023. URL `[https://arxiv.org/abs/2303.08774](https://arxiv.org/abs/2303.08774)` .


[2] Walid Ahmad, Elana Simon, Seyone Chithrananda, Gabriel Grand, and Bharath Ramsundar. Chemberta-2:
Towards chemical foundation models. _arXiv preprint arXiv:2209.01712_, 2022.


[3] PR Andrews, DJ Craik, and JL Martin. Functional group contributions to drug-receptor interactions.
_Journal of medicinal chemistry_, 27(12):1648–1657, 1984.


[4] Nicholas H. Angello, Vandana Rathore, Wiktor Beker, Agnieszka Wołos, Edward R. Jira, Rafał Roszak,
Tony C. Wu, Charles M. Schroeder, Alán Aspuru-Guzik, Bartosz A. Grzybowski, and et al. Closed-loop
optimization of general reaction conditions for heteroaryl suzuki-miyaura coupling. _Science_, 378(6618):
399–405, Oct 2022. doi: 10.1126/science.adc8743.


[5] Emre Arkan, Eyup Yalcin, Muhittin Unal, M Zeliha Yigit Arkan, Mustafa Can, Cem Tozlu, and Serafettin
Demic. Effect of functional groups of self assembled monolayer molecules on the performance of inverted
perovskite solar cell. _Materials Chemistry and Physics_, 254:123435, 2020.


[6] Dávid Bajusz, Anita Rácz, and Károly Héberger. Why is tanimoto index an appropriate choice for
fingerprint-based similarity calculations? _Journal of cheminformatics_, 7:1–13, 2015.


[7] Guy W Bemis and Mark A Murcko. The properties of known drugs. 1. molecular frameworks. _Journal of_
_medicinal chemistry_, 39(15):2887–2893, 1996.


[8] Daniel J. Blair, Sriyankari Chitti, Melanie Trobe, David M. Kostyra, Hannah M. Haley, Richard L. Hansen,
Steve G. Ballmer, Toby J. Woods, Wesley Wang, Vikram Mubayi, and et al. Automated iterative csp3–c
bond formation. _Nature_, 604(7904):92–97, Feb 2022. doi: 10.1038/s41586-022-04491-w.


[9] Fabio Broccatelli, Richard Trager, Michael Reutlinger, George Karypis, and Mufei Li. Benchmarking
accuracy and generalizability of four graph neural networks using large in vitro adme datasets from
different chemical spaces. _Molecular Informatics_, 41(8):2100321, 2022.


[10] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal,
Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel HerbertVoss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu,
Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin
Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario
Amodei. Language models are few-shot learners. In Hugo Larochelle, Marc’Aurelio Ranzato, Raia
Hadsell, Maria-Florina Balcan, and Hsuan-Tien Lin, editors, _Advances in Neural Information Process-_
_ing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020,_
_December 6-12, 2020, virtual_, 2020. URL `[https://proceedings.neurips.cc/paper/2020/hash/](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html)`
`[1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html](https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html)` .


[11] Andrea Cadeddu, Elizabeth K. Wylie, Janusz Jurczak, Matthew Wampler-Doty, and Bartosz A. Grzybowski. Organic chemistry as a language and the implications of chemical linguistics for structural
and retrosynthetic analyses. _Angewandte Chemie International Edition_, 53(31):8108–8112, 2014. doi:
https://doi.org/10.1002/anie.201403708. URL `[https://onlinelibrary.wiley.com/doi/abs/10.](https://onlinelibrary.wiley.com/doi/abs/10.1002/anie.201403708)`
`[1002/anie.201403708](https://onlinelibrary.wiley.com/doi/abs/10.1002/anie.201403708)` .


[12] Xiaokang Chen, Zhiyu Wu, Xingchao Liu, Zizheng Pan, Wen Liu, Zhenda Xie, Xingkai Yu, and Chong
Ruan. Janus-pro: Unified multimodal understanding and generation with data and model scaling. _arXiv_
_preprint arXiv:2501.17811_, 2025.


[13] Yangyi Chen, Xingyao Wang, Hao Peng, and Heng Ji. Solo: A single transformer for scalable visionlanguage modeling. In _Transactions on Machine Learning Research_, 2024.


[14] Philipp le Coutre, Karl-Anton Kreuzer, Stefan Pursche, Malte von Bonin, T Leopold, Gökben Baskaynak,
Bernd Dörken, Gerhard Ehninger, Oliver G. Ottmann, Andreas Jenke, Martin Bornhäuser, and Eberhard
Schleyer. Pharmacokinetics and cellular uptake of imatinib and its main metabolite cgp74588. _Cancer_
_Chemotherapy and Pharmacology_, 2004. doi: 10.1007/s00280-003-0741-6.


[15] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha
Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. The llama 3 herd of models. _ArXiv_
_preprint_, abs/2407.21783, 2024. URL `[https://arxiv.org/abs/2407.21783](https://arxiv.org/abs/2407.21783)` .


11


[16] Carl Edwards, ChengXiang Zhai, and Heng Ji. Text2Mol: Cross-modal molecule retrieval with
natural language queries. In _Proceedings of the 2021 Conference on Empirical Methods in Nat-_
_ural Language Processing_, pages 595–607, Online and Punta Cana, Dominican Republic, 2021.
Association for Computational Linguistics. doi: 10.18653/v1/2021.emnlp-main.47. URL `[https:](https://aclanthology.org/2021.emnlp-main.47)`
`[//aclanthology.org/2021.emnlp-main.47](https://aclanthology.org/2021.emnlp-main.47)` .


[17] Carl Edwards, Tuan Lai, Kevin Ros, Garrett Honke, Kyunghyun Cho, and Heng Ji. Translation between
molecules and natural language. In _Proc. The 2022 Conference on Empirical Methods in Natural_
_Language Processing (EMNLP2022)_, 2022.


[18] Carl Edwards, Tuan Lai, Kevin Ros, Garrett Honke, Kyunghyun Cho, and Heng Ji. Translation between
molecules and natural language. In _Proceedings of the 2022 Conference on Empirical Methods in_
_Natural Language Processing_, pages 375–413, Abu Dhabi, United Arab Emirates, 2022. Association for
Computational Linguistics. URL `[https://aclanthology.org/2022.emnlp-main.26](https://aclanthology.org/2022.emnlp-main.26)` .


[19] Carl Edwards, Ziqing Lu, Ehsan Hajiramezanali, Tommaso Biancalani, Heng Ji, and Gabriele Scalia.
Molcap-arena: A comprehensive captioning benchmark on language-enhanced molecular property
prediction. _arXiv preprint arXiv:2411.00737_, 2024.


[20] Carl Edwards, Aakanksha Naik, Tushar Khot, Martin Burke, Heng Ji, and Tom Hope. Synergpt: Incontext learning for personalized drug synergy prediction and drug design. In _Proc. 1st Conference on_
_Language Modeling (COLM2024)_, 2024.


[21] Carl Edwards, Qingyun Wang, Lawrence Zhao, and Heng Ji. L+M-24: Building a dataset for Language+Molecules @ ACL 2024. In Carl Edwards, Qingyun Wang, Manling Li, Lawrence Zhao, Tom Hope,
and Heng Ji, editors, _Proceedings of the 1st Workshop on Language + Molecules (L+M 2024)_, pages 1–9,
Bangkok, Thailand, 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.langmol-1.1.
URL `[https://aclanthology.org/2024.langmol-1.1](https://aclanthology.org/2024.langmol-1.1)` .


[22] Peter Ertl and Tim Schuhmann. A systematic cheminformatics analysis of functional groups occurring in
natural products. _Journal of natural products_, 82(5):1258–1263, 2019.


[23] Peter Ertl, Eva Altmann, and Jeffrey M McKenna. The most common functional groups in bioactive
molecules and how their popularity has evolved over time. _Journal of medicinal chemistry_, 63(15):
8408–8418, 2020.


[24] Yin Fang, Xiaozhuan Liang, Ningyu Zhang, Kangwei Liu, Rui Huang, Zhuo Chen, Xiaohui Fan, and
Huajun Chen. Mol-instructions: A large-scale biomolecular instruction dataset for large language models.
_ArXiv preprint_, abs/2306.08018, 2023. URL `[https://arxiv.org/abs/2306.08018](https://arxiv.org/abs/2306.08018)` .


[25] Cong Fu, Xiner Li, Blake Olson, Heng Ji, and Shuiwang Ji. Fragment and geometry aware tokenization of
molecules for structure-based drug design using language models. In _Proc. The Thirteenth International_
_Conference on Learning Representations (ICLR2025)_, 2025.


[26] Johannes Gasteiger, Florian Becker, and Stephan Günnemann. Gemnet: Universal directional graph
neural networks for molecules. _Advances in Neural Information Processing Systems_, 34:6790–6802,
2021.


[27] Anna Gaulton, Louisa J Bellis, A Patricia Bento, Jon Chambers, Mark Davies, Anne Hersey, Yvonne
Light, Shaun McGlinchey, David Michalovich, Bissan Al-Lazikani, et al. Chembl: a large-scale bioactivity
database for drug discovery. _Nucleic acids research_, 40(D1):D1100–D1107, 2012.


[28] Eric P Gillis and Martin D Burke. A simple and modular strategy for small molecule synthesis: Iterative
suzuki _−_ miyaura coupling of b-protected haloboronic acid building blocks. _Journal of the American_
_Chemical Society._, 129(21), 2007. ISSN 0002-7863.


[29] Shen Han, Haitao Fu, Yuyang Wu, Ganglan Zhao, Zhenyu Song, Feng Huang, Zhongfei Zhang, Shichao
Liu, and Wen Zhang. Himgnn: a novel hierarchical molecular graph representation learning framework
for property prediction. _Briefings in Bioinformatics_, 24(5):bbad305, 2023.


[30] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Delving deep into rectifiers: Surpassing
human-level performance on imagenet classification. In _Proceedings of the IEEE international conference_
_on computer vision_, pages 1026–1034, 2015.


[31] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and
Weizhu Chen. Lora: Low-rank adaptation of large language models. _arXiv preprint arXiv:2106.09685_,
2021.


12


[32] Mengzhou Hu, Sahar Alkhairy, Ingoo Lee, Rudolf T Pillich, Dylan Fong, Kevin Smith, Robin Bachelder,
Trey Ideker, and Dexter Pratt. Evaluation of large language models for discovery of gene set function.
_Nature methods_, 22(1):82–91, 2025.


[33] Kexin Huang, Tianfan Fu, Wenhao Gao, Yue Zhao, Yusuf Roohani, Jure Leskovec, Connor W Coley, Cao
Xiao, Jimeng Sun, and Marinka Zitnik. Therapeutics data commons: Machine learning datasets and tasks
for drug discovery and development. _arXiv preprint arXiv:2102.09548_, 2021.


[34] Lifu Huang, Kyunghyun Cho, Boliang Zhang, Heng Ji, and Kevin Knight. Multi-lingual common
semantic space construction via cluster-consistent word embedding. In _Proc. 2018 Conference on_
_Empirical Methods in Natural Language Processing (EMNLP2018)_, 2018.


[35] Tango Therapeutics Inc. Tango therapeutics announces discontinuation of tng348 program, May 2024. URL `[https://ir.tangotx.com/news-releases/news-release-details/](https://ir.tangotx.com/news-releases/news-release-details/tango-therapeutics-announces-discontinuation-tng348-program)`
`[tango-therapeutics-announces-discontinuation-tng348-program](https://ir.tangotx.com/news-releases/news-release-details/tango-therapeutics-announces-discontinuation-tng348-program)` .


[36] Y. Isobe, K. Sugimoto, A. Masuda, Y. Hamano, and K. Oshimi. Central nervous system is a sanctuary
site for chronic myelogenous leukaemia treated with imatinib mesylate. _Internal medicine journal_, 2009.
doi: 10.1111/j.1445-5994.2009.01947.x.


[37] Bowen Jin, Gang Liu, Chi Han, Meng Jiang, Heng Ji, and Jiawei Han. Large language models on graphs:
A comprehensive survey. In _IEEE Transactions on Knowledge and Data Engineering_, 2023.


[38] Bowen Jin, Gang Liu, Chi Han, Meng Jiang, Heng Ji, and Jiawei Han. Large language models on graphs:
A comprehensive survey. _IEEE Transactions on Knowledge and Data Engineering_, 2024.


[39] Shao Jinsong, Jia Qifeng, Chao Xing, Yusheng Hao, and Li Wang. Molecular fragmentation as a crucial
step in the ai-based drug development pathway. _Communications Chemistry_, 2024. doi: 10.1038/
s42004-024-01109-2.


[40] Sunghwan Kim, Jie Chen, Tiejun Cheng, Asta Gindulyte, Jia He, Siqian He, Qingliang Li, Benjamin A
Shoemaker, Paul A Thiessen, Bo Yu, et al. Pubchem 2023 update. _Nucleic Acids Research_, 51(D1):
D1373–D1380, 2023.


[41] R. Kneller. The importance of new companies for drug discovery: origins of a decade of new drugs. In
_Nat Rev Drug Discov 9, 867–882 (2010)_, 2010.


[42] Clayton W Kosonocky, Claus O Wilke, Edward M Marcotte, and Andrew D Ellington. Mining patents
with large language models demonstrates congruence of functional labels and chemical structures. _arXiv_
_preprint arXiv:2309.08765_, 2023.


[43] Mario Krenn, Florian Häse, AkshatKumar Nigam, Pascal Friederich, and Alan Aspuru-Guzik. Selfreferencing embedded strings (selfies): A 100% robust molecular string representation. _Machine Learning:_
_Science and Technology_, 1(4):045024, 2020.


[44] Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brahman,
Lester James V Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, et al. T _\_ " ulu 3: Pushing frontiers in open
language model post-training. _arXiv preprint arXiv:2411.15124_, 2024.


[45] Jonathan W. Lehmann, Daniel J. Blair, and Martin D. Burke. Towards the generalized iterative synthesis
of small molecules. _Nature Reviews Chemistry_, 2(2), Feb 2018. doi: 10.1038/s41570-018-0115.


[46] Biaoshun Li, Mujie Lin, Tiegen Chen, and Ling Wang. Fg-bert: a generalized and self-supervised
functional group-based molecular representation learning framework for properties prediction. _Briefings_
_in Bioinformatics_, 24(6):bbad398, 2023.


[47] Bo Li, Hao Zhang, Kaichen Zhang, Dong Guo, Yuanhan Zhang, Renrui Zhang, Feng Li, Ziwei Liu, and
Chunyuan Li. Llava-next: What else influences visual instruction tuning beyond data?, May 2024. URL
`[https://llava-vl.github.io/blog/2024-05-25-llava-next-ablations/](https://llava-vl.github.io/blog/2024-05-25-llava-next-ablations/)` .


[48] Jin Li, Naiteng Wu, Jian Zhang, Honghui Wu, Kunming Pan, Yingxue Wang, Guilong Liu, Xianming Liu,
Zhenpeng Yao, and Qiaobao Zhang. Machine learning-assisted low-dimensional electrocatalysts design
for hydrogen evolution reaction. _Nano-Micro Letters_, 2023. doi: 10.1007/s40820-023-01192-5.


[49] Jin Li, Meisa Zhou, Honghui Wu, Lifei Wang, Jian Zhang, Naiteng Wu, Kunming Pan, Guilong Liu,
Yinggan Zhang, Jiajia Han, Xianming Liu, Xiang Chen, Jiayu Wan, and Qiaobao Zhang. Machine
learning-assisted property prediction of solid-state electrolyte. _Advanced Energy Materials_, 2024. doi:
10.1002/aenm.202304480.


13


[50] Junqi Li, Steven G Ballmer, Eric P Gillis, Seiko Fujii, Michael J Schmidt, Andrea M E Palazzolo,
Jonathan W Lehmann, Greg F Morehouse, and Martin D Burke. Synthesis of many different types of
organic small molecules using one automated process. _Science._, 347(6227), 2015. ISSN 0036-8075.


[51] Junqi Li, Steven G Ballmer, Eric P Gillis, Seiko Fujii, Michael J Schmidt, Andrea ME Palazzolo,
Jonathan W Lehmann, Greg F Morehouse, and Martin D Burke. Synthesis of many different types of
organic small molecules using one automated process. _Science_, 347(6227):1221–1226, 2015.


[52] Manling Li, Ruochen Xu, Shuohang Wang, Luowei Zhou, Xudong Lin, Chenguang Zhu, Michael Zeng,
Heng Ji, and Shih-Fu Chang. Clip-event: Connecting text and images with event structures. In _Proc._
_Conference on Computer Vision and Pattern Recognition (CVPR2022)_, 2022.


[53] Sihang Li, Zhiyuan Liu, Yanchen Luo, Xiang Wang, Xiangnan He, Kenji Kawaguchi, Tat-Seng Chua, and
Qi Tian. Towards 3d molecule-text interpretation in language models. _ArXiv preprint_, abs/2401.13923,
2024. URL `[https://arxiv.org/abs/2401.13923](https://arxiv.org/abs/2401.13923)` .


[54] Xiner Li, Limei Wang, Youzhi Luo, Carl Edwards, Shurui Gui, Yuchao Lin, Heng Ji, and Shuiwang Ji.
Learning to generate 3d molecules via language models with geometry-aware tokenization. In _Proc. 2025_
_International Conference on Machine Learning (ICML2025)_, 2025.


[55] Gang Liu, Michael Sun, Wojciech Matusik, Meng Jiang, and Jie Chen. Multimodal large language models
for inverse molecular design with retrosynthetic planning. _arXiv preprint arXiv:2410.04223_, 2024.


[56] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. Visual instruction tuning, 2023.


[57] Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. Improved baselines with visual instruction
tuning. In _Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition_, pages
26296–26306, 2024.


[58] Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, and Yong Jae Lee. Llava-next:
Improved reasoning, ocr, and world knowledge, January 2024. URL `[https://llava-vl.github.io/](https://llava-vl.github.io/blog/2024-01-30-llava-next/)`
`[blog/2024-01-30-llava-next/](https://llava-vl.github.io/blog/2024-01-30-llava-next/)` .


[59] Zhiyuan Liu, Sihang Li, Yanchen Luo, Hao Fei, Yixin Cao, Kenji Kawaguchi, Xiang Wang, and Tat-Seng
Chua. Molca: Molecular graph-language modeling with cross-modal projector and uni-modal adapter.
_arXiv preprint arXiv:2310.12798_, 2023.


[60] Zhiyuan Liu, An Zhang, Hao Fei, Enzhi Zhang, Xiang Wang, Kenji Kawaguchi, and Tat-Seng Chua.
Prott3: Protein-to-text generation for text-based protein understanding. In _Proceedings of the 62nd Annual_
_Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_, pages 5949–5966,
2024.


[61] Micha Livne, Zulfat Miftahutdinov, Elena Tutubalina, Maksim Kuznetsov, Daniil Polykovskiy, Annika Brundyn, Aastha Jhunjhunwala, Anthony Costa, Alex Aliper, Alán Aspuru-Guzik, et al. nach0:
multimodal natural and chemical languages foundation model. _Chemical Science_, 15(22):8380–8389,
2024.


[62] Steven A Lopez, Edward O Pyzer-Knapp, Gregor N Simm, Trevor Lutzow, Kewei Li, Laszlo R Seress,
Johannes Hachmann, and Alán Aspuru-Guzik. The harvard organic photovoltaic dataset. _Scientific data_,
3(1):1–7, 2016.


[63] Ilya Loshchilov and Frank Hutter. Decoupled weight decay regularization. _arXiv preprint_
_arXiv:1711.05101_, 2017.


[64] Haoyu Lu, Wen Liu, Bo Zhang, Bingxuan Wang, Kai Dong, Bo Liu, Jingxiang Sun, Tongzheng Ren,
Zhuoshu Li, Hao Yang, et al. Deepseek-vl: towards real-world vision-language understanding. _arXiv_
_preprint arXiv:2403.05525_, 2024.


[65] Chade Lv, Xin Zhou, Lixiang Zhong, Chunshuang Yan, M. Srinivasan, Z. Seh, Chuntai Liu, Hongge
Pan, Shuzhou Li, Yonggang Wen, and Qingyu Yan. Machine learning: An advanced platform for
materials development and state prediction in lithium-ion batteries. _Advances in Materials_, 2021. doi:
10.1002/adma.202101474.


[66] Rishikesh Magar, Yuyang Wang, Cooper Lorsung, Chen Liang, Hariharan Ramasubramanian, Peiyuan Li,
and Amir Barati Farimani. Auglichem: data augmentation library of chemical structures for machine
learning. _Machine Learning: Science and Technology_, 3(4):045015, nov 2022. doi: 10.1088/2632-2153/
ac9c84. URL `[https://dx.doi.org/10.1088/2632-2153/ac9c84](https://dx.doi.org/10.1088/2632-2153/ac9c84)` .


14


[67] Xavier Montalban, Karolina Piasecka-Stryczynska, Jens Kuhle, Pascal Benkert, Douglas L Arnold,
Martin S Weber, Andrea Seitzinger, Hans Guehring, Jamie Shaw, Davorka Tomic, Yann Hyvert, Danielle E
Harlow, Martin Dyroff, and Jerry S Wolinsky. Efficacy and safety results after >3.5 years of treatment
with the bruton’s tyrosine kinase inhibitor evobrutinib in relapsing multiple sclerosis: Long-term followup of a phase ii randomised clinical trial with a cerebrospinal fluid sub-study. _Multiple Sclerosis_
_Journal_, 30(4-5):558–570, 2024. doi: 10.1177/13524585241234783. URL `[https://doi.org/10.](https://doi.org/10.1177/13524585241234783)`
`[1177/13524585241234783](https://doi.org/10.1177/13524585241234783)` . PMID: 38436271.


[68] Thao Nguyen, Kuan-Hao Huang, Ge Liu, Martin D Burke, Ying Diao, and Heng Ji. Farm: Functional
group-aware representations for small molecules. _arXiv preprint arXiv:2410.02082_, 2024.


[69] Thao Nguyen, Tiara Torres-Flores, Changhyun Hwang, Carl Edwards, Ying Diao, and Heng Ji. Glad:
Synergizing molecular graphs and language descriptors for enhanced power conversion efficiency prediction in organic photovoltaic devices. In _Proc. 33rd ACM International Conference on Information and_
_Knowledge Management (CIKM 2024)_, 2024.


[70] Thao Nguyen, Tiara Torres-Flores, Changhyun Hwang, Carl Edwards, Ying Diao, and Heng Ji. Glad:
Synergizing molecular graphs and language descriptors for enhanced power conversion efficiency prediction in organic photovoltaic devices. In _Proceedings of the 33rd ACM International Conference on_
_Information and Knowledge Management_, pages 4777–4785, 2024.


[71] Thao Nguyen, Kuan-Hao Huang, Ge Liu, Martin D. Burke, Ying Diao, and Heng Ji. Farm: Functional
group-aware representations for small molecules. In _Proc. NAACL2025 Workshop on AI and Scientific_
_Discovery: Directions and Opportunities_, 2025.


[72] Qizhi Pei, Wei Zhang, Jinhua Zhu, Kehan Wu, Kaiyuan Gao, Lijun Wu, Yingce Xia, and Rui Yan. Biot5:
Enriching cross-modal integration in biology with chemical knowledge and natural language associations.
_arXiv preprint arXiv:2310.07276_, 2023.


[73] Qizhi Pei, Lijun Wu, Kaiyuan Gao, Xiaozhuan Liang, Yin Fang, Jinhua Zhu, Shufang Xie, Tao Qin, and
Rui Yan. Biot5+: Towards generalized biological understanding with iupac integration and multi-task
tuning. _ArXiv preprint_, abs/2402.17810, 2024. URL `[https://arxiv.org/abs/2402.17810](https://arxiv.org/abs/2402.17810)` .


[74] John W Pratt. Remarks on zeros and ties in the wilcoxon signed rank procedures. _Journal of the American_
_Statistical Association_, 54(287):655–667, 1959.


[75] S. Rotstein and M. Murcko. Groupbuild: a fragment-based method for de novo drug design. _Journal of_
_medicinal chemistry_, 1993. doi: 10.1021/jm00064a003.


[76] Benjamin Sanchez-Lengeling, Jennifer N Wei, Brian K Lee, Richard C Gerkin, Al’an Aspuru-Guzik, and
Alexander B Wiltschko. Machine learning for scent: Learning generalizable perceptual representations of
small molecules. _arXiv preprint arXiv:1910.10685_, 2019.


[77] K. Senior. Gleevec does not cross blood-brain barrier. _The Lancet. Oncology_, 2003. doi: 10.1016/
s1470-2045(03)01050-7.


[78] Richard W Shuai, Jeffrey A Ruffolo, and Jeffrey J Gray. Iglm: Infilling language modeling for antibody
sequence design. _Cell Systems_, 14(11):979–989, 2023.


[79] Zhan Si, Deguang Liu, Wan Nie, Jingjing Hu, Wei Wang, Tingting Jiang, Haizhu Yu, and Yao Fu. Databased prediction of redox potentials via introducing chemical features into the transformer architecture.
_Journal of Chemical Information and Modeling_, 2024. doi: 10.1021/acs.jcim.4c01299.


[80] Antoine Simoneau, Charlotte B Pratt, Hsin-Jung Wu, Shreya S Rajeswaran, Charlotte Grace Comer,
Sirimas Sudsakorn, Wenhai Zhang, Shangtao Liu, Samuel R Meier, Ashley H Choi, et al. Characterization
of tng348: a selective, allosteric usp1 inhibitor that synergizes with parp inhibitors in tumors with
homologous recombination deficiency. _Molecular Cancer Therapeutics_, 2025.


[81] Karan Singhal, Shekoofeh Azizi, Tao Tu, S Sara Mahdavi, Jason Wei, Hyung Won Chung, Nathan
Scales, Ajay Tanwani, Heather Cole-Lewis, Stephen Pfohl, et al. Large language models encode clinical
knowledge. _Nature_, 620(7972):172–180, 2023.


[82] E. Solak and E. Irmak. Advances in organic photovoltaic cells: a comprehensive review of materials,
technologies, and performance. _RSC Advances_, 2023. doi: 10.1039/d3ra01454a.


[83] Henry W Sprueill, Carl Edwards, Khushbu Agarwal, Mariefel V Olarte, Udishnu Sanyal, Conrad Johnston,
Hongbin Liu, Heng Ji, and Sutanay Choudhury. Chemreasoner: Heuristic search over a large language
model’s knowledge space using quantum-chemical feedback. _ArXiv preprint_, abs/2402.10980, 2024.
URL `[https://arxiv.org/abs/2402.10980](https://arxiv.org/abs/2402.10980)` .


15


[84] Felix Strieth-Kalthoff, Han Hao, Vandana Rathore, Joshua Derasp, Théophile Gaudin, Nicholas H
Angello, Martin Seifrid, Ekaterina Trushina, Mason Guy, Junliang Liu, Xun Tang, Masashi Mamada,
Wesley Wang, Tuul Tsagaantsooj, Cyrille Lavigne, Robert Pollice, Tony C Wu, Kazuhiro Hotta, Leticia
Bodo, Shangyu Li, Mohammad Haddadnia, Agnieszka Wołos, Rafał Roszak, Cher Tian Ser, Carlota
Bozal-Ginesta, Riley J Hickman, Jenya Vestfrid, Andrés Aguilar-Granda, Elena L Klimareva, Ralph C
Sigerson, Wenduan Hou, Daniel Gahler, Slawomir Lach, Adrian Warzybok, Oleg Borodin, Simon
Rohrbach, Benjamin Sanchez-Lengeling, Chihaya Adachi, Bartosz A Grzybowski, Leroy Cronin, Jason E
Hein, Martin D Burke, and Alán Aspuru-Guzik. Delocalized, asynchronous, closed-loop discovery of
organic laser emitters. _Science_, 384(6697):eadk9227, May 2024.


[85] Dagmar Stumpfe, Huabin Hu, and Jurgen Bajorath. Evolving concept of activity cliffs. _ACS omega_, 4
(11):14360–14368, 2019.


[86] Xiaoyu Sun, Nathaniel J. Krakauer, Alexander Politowicz, Wei-Ting Chen, Qiying Li, Zuoyi Li, Xianjia
Shao, Alfred Sunaryo, Mingren Shen, James Wang, and Dane Morgan. Assessing graph-based deep
learning models for predicting flash point. _Mol. Inf._, 39(6):1900101, feb 2020. doi: 10.1002/minf.
201900101. URL `[https://doi.org/10.1002%2Fminf.201900101](https://doi.org/10.1002%2Fminf.201900101)` .


[87] N. Takayama, N. Sato, S. O’Brien, Y. Ikeda, and S. Okamoto. Imatinib mesylate has limited activity
against the central nervous system involvement of philadelphia chromosome-positive acute lymphoblastic
leukaemia due to poor penetration into cerebrospinal fluid. _British journal of haematology_, 2002. doi:
10.1046/j.1365-2141.2002.03881.x.


[88] Zineng Tang, Ziyi Yang, Chenguang Zhu, Michael Zeng, and Mohit Bansal. Any-to-any generation via
composable diffusion. _Advances in Neural Information Processing Systems_, 36:16083–16099, 2023.


[89] Ross Taylor, Marcin Kardas, Guillem Cucurull, Thomas Scialom, Anthony Hartshorn, Elvis Saravia,
Andrew Poulton, Viktor Kerkez, and Robert Stojnic. Galactica: A large language model for science.
_arXiv preprint arXiv:2211.09085_, 2022.


[90] A. Thirunavukarasu, D. Ting, Kabilan Elangovan, Laura Gutierrez, Ting Fang Tan, and D. Ting. Large
language models in medicine. _Nature Network Boston_, 2023. doi: 10.1038/s41591-023-02448-8.


[91] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix,
Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard
Grave, and Guillaume Lample. Llama: Open and efficient foundation language models. _arXiv Preprint_,
2023.


[92] Melanie Trobe and Martin D. Burke. The molecular industrial revolution: Automated synthesis of small
molecules. _Angewandte Chemie International Edition_, 57(16):4192–4214, Mar 2018. doi: 10.1002/anie.
201710482.


[93] Theodore Tyrikos-Ergas, Sevasti Agiakloglou, Antonio J Laporte, Wesley Wang, Chieh-Kai Chan, Clare E
Wells, Christopher K Rakowski, Rachel I Hammond, Jia Qiu, Jonathan D Raymond, et al. Automated
iterative nc and cc bond formation. _ChemRxiv_, 2025.


[94] Derek Van Tilborg, Alisa Alenicheva, and Francesca Grisoni. Exposing the limitations of molecular
machine learning with activity cliffs. _Journal of chemical information and modeling_, 62(23):5938–5951,
2022.


[95] Edon Vitaku, David T. Smith, and Jon T. Njardarson. Analysis of the structural diversity, substitution
patterns, and frequency of nitrogen heterocycles among u.s. fda approved pharmaceuticals. _Journal of_
_Medicinal Chemistry_, 2014. doi: 10.1021/jm501100b.


[96] Chengyi Wang, Sanyuan Chen, Yu Wu, Ziqiang Zhang, Long Zhou, Shujie Liu, Zhuo Chen, Yanqing Liu,
Huaming Wang, Jinyu Li, et al. Neural codec language models are zero-shot text to speech synthesizers.
_arXiv preprint arXiv:2301.02111_, 2023.


[97] Hongwei Wang, Weijiang Li, Xiaomeng Jin, Kyunghyun Cho, Heng Ji, Jiawei Han, and Martin Burke.
Chemical-reaction-aware molecule representation learning. In _Proc. The International Conference on_
_Learning Representations (ICLR2022)_, 2022.


[98] Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin
Wang, Wenbin Ge, et al. Qwen2-vl: Enhancing vision-language model’s perception of the world at any
resolution. _arXiv preprint arXiv:2409.12191_, 2024.


[99] Sheng Wang, Yuzhi Guo, Yuhong Wang, Hongmao Sun, and Junzhou Huang. Smiles-bert: large scale
unsupervised pre-training for molecular property prediction. In _Proceedings of the 10th ACM international_
_conference on bioinformatics, computational biology and health informatics_, pages 429–436, 2019.


16


[100] Wesley Wang, Nicholas H Angello, Daniel J Blair, Theodore Tyrikos-Ergas, William H Krueger, Kameron
N S Medine, Antonio J LaPorte, Joshua M Berger, and Martin D Burke. Rapid automated iterative
small-molecule synthesis. _Nat. Synth._, 3(8):1031–1038, May 2024.


[101] Xinlong Wang, Xiaosong Zhang, Zhengxiong Luo, Quan Sun, Yufeng Cui, Jinsheng Wang, Fan Zhang,
Yueze Wang, Zhen Li, Qiying Yu, et al. Emu3: Next-token prediction is all you need. _arXiv preprint_
_arXiv:2409.18869_, 2024.


[102] Yifei Wang, Shiyang Chen, Guobin Chen, Ethan Shurberg, Hang Liu, and Pengyu Hong. Motif-based
graph representation learning with application to chemical molecules. In _Informatics_, volume 10, page 8.
MDPI, 2023.


[103] Yuyang Wang, Jianren Wang, Zhonglin Cao, and Amir Barati Farimani. Molecular contrastive learning of
representations via graph neural networks. _Nature Machine Intelligence_, 4(3):279–287, 2022.


[104] David Weininger. Smiles, a chemical language and information system. 1. introduction to methodology
and encoding rules. _Journal of chemical information and computer sciences_, 28(1):31–36, 1988.


[105] Frank Wilcoxon. Individual comparisons by ranking methods. _Biometrics Bulletin_, 1(6):80–83, 1945.


[106] David S Wishart, Sagan Girod, Harrison Peters, Eponine Oler, Juan Jovel, Zachary Budinski, Ralph
Milford, Vicki W Lui, Zinat Sayeeda, Robert Mah, et al. Chemfont: the chemical functional ontology
resource. _Nucleic Acids Research_, 51(D1):D1220–D1229, 2023.


[107] Eric M Woerly, Jahnabi Roy, and Martin D Burke. Synthesis of most polyene natural product motifs
using just 12 building blocks and one coupling reaction. _Nature Chemistry._, 6, 2014. ISSN 1755-4349.


[108] Zhenqin Wu, Bharath Ramsundar, Evan N. Feinberg, Joseph Gomes, Caleb Geniesse, Aneesh S. Pappu,
Karl Leswing, and Vijay Pande. Moleculenet: a benchmark for molecular machine learning. _Chemical_
_science_, 9(2):513–530, 2018.


[109] Jun Xia, Chengshuai Zhao, Bozhen Hu, Zhangyang Gao, Cheng Tan, Yue Liu, Siyuan Li, and Stan Z Li.
Mole-bert: Rethinking pre-training graph neural networks for molecules. In _The Eleventh International_
_Conference on Learning Representations_, 2023.


[110] Hanguang Xiao, Feizhong Zhou, Xingyue Liu, Tianqi Liu, Zhipeng Li, Xin Liu, and Xiaoxuan Huang.
A comprehensive survey of large language models and multimodal large language models in medicine.
_Information Fusion_, page 102888, 2024.


[111] Le Xue, Mingfei Gao, Chen Xing, Roberto Martín-Martín, Jiajun Wu, Caiming Xiong, Ran Xu, Juan Carlos Niebles, and Silvio Savarese. Ulip: Learning a unified representation of language, images, and point
clouds for 3d understanding. In _Proceedings of the IEEE/CVF conference on computer vision and pattern_
_recognition_, pages 1179–1189, 2023.


[112] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng
Liu, Fei Huang, Haoran Wei, et al. Qwen2. 5 technical report. _arXiv preprint arXiv:2412.15115_, 2024.


[113] Dongchao Yang, Jinchuan Tian, Xu Tan, Rongjie Huang, Songxiang Liu, Haohan Guo, Xuankai Chang,
Jiatong Shi, Sheng Zhao, Jiang Bian, et al. Uniaudio: Towards universal audio generation with large
language models. In _International Conference on Machine Learning_, pages 56422–56447. PMLR, 2024.


[114] Geyan Ye, Xibao Cai, Houtim Lai, Xing Wang, Junhong Huang, Longyue Wang, Wei Liu, and Xiangxiang
Zeng. Drugassist: A large language model for molecule optimization. _Briefings in Bioinformatics_, 26(1):
bbae693, 2025.


[115] Botao Yu, Frazier N Baker, Ziqi Chen, Xia Ning, and Huan Sun. Llasmol: Advancing large language
models for chemistry with a large-scale, comprehensive, high-quality instruction tuning dataset. _arXiv_
_preprint arXiv:2402.09391_, 2024.


[116] Di Zhang, Wei Liu, Qian Tan, Jingdan Chen, Hang Yan, Yuliang Yan, Jiatong Li, Weiran Huang, Xiangyu
Yue, Dongzhan Zhou, et al. Chemllm: A chemical large language model. _arXiv preprint arXiv:2402.06852_,
2024.


[117] Ruochen Zhang, Samuel Cahyawijaya, Jan Christian Blaise Cruz, Genta Indra Winata, and Alham Fikri
Aji. Multilingual large language models are not (yet) code-switchers. In _The 2023 Conference on_
_Empirical Methods in Natural Language Processing_, 2023.


[118] Shichang Zhang, Ziniu Hu, Arjun Subramonian, and Yizhou Sun. Motif-driven contrastive learning of
graph representations. _arXiv preprint arXiv:2012.12533_, 2020.


17


[119] Yu Zhang, Xiusi Chen, Bowen Jin, Sheng Wang, Shuiwang Ji, Wei Wang, and Jiawei Han. A comprehensive survey of scientific large language models and their applications in scientific discovery. _arXiv_
_preprint arXiv:2406.10833_, 2024.


[120] Zaixi Zhang, Qi Liu, Hao Wang, Chengqiang Lu, and Chee-Kong Lee. Motif-based graph self-supervised
learning for molecular property prediction. _Advances in Neural Information Processing Systems_, 34:
15870–15882, 2021.


[121] Ziqiao Zhang, Bangyi Zhao, Ailin Xie, Yatao Bian, and Shuigeng Zhou. Activity cliff prediction: Dataset
and benchmark. _arXiv preprint arXiv:2302.07541_, 2023.


[122] Haiteng Zhao, Shengchao Liu, Ma Chang, Hannan Xu, Jie Fu, Zhihong Deng, Lingpeng Kong, and
Qi Liu. Gimlet: A unified graph-text model for instruction-based molecule zero-shot learning. _Advances_
_in neural information processing systems_, 36:5850–5887, 2023.


[123] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, et al. A survey of large language models. _arXiv preprint_
_arXiv:2303.18223_, 1(2), 2023.


[124] Zihan Zhao, Da Ma, Lu Chen, Liangtai Sun, Zihao Li, Hongshen Xu, Zichen Zhu, Su Zhu, Shuai
Fan, Guodong Shen, et al. Chemdfm: Dialogue foundation model for chemistry. _arXiv preprint_
_arXiv:2401.14818_, 2024.


[125] Yizhen Zheng, Huan Yee Koh, Maddie Yang, Li Li, Lauren T. May, Geoffrey I. Webb, Shirui Pan, and
George Church. Large language models in drug discovery and development: From disease mechanisms
to clinical trials, 2024. URL `[https://arxiv.org/abs/2409.04481](https://arxiv.org/abs/2409.04481)` .


[126] Gengmo Zhou, Zhifeng Gao, Qiankun Ding, Hang Zheng, Hongteng Xu, Zhewei Wei, Linfeng Zhang,
and Guolin Ke. Uni-mol: A universal 3d molecular representation learning framework. In _The Eleventh_
_International Conference on Learning Representations_, 2023.


[127] George Kingsley Zipf. _The psycho-biology of language: An introduction to dynamic philology_ . Routledge,
1936.


18


**A** **Pretraining Data Mixture**


To train the model, our goal is to cover a wide variety of different molecular functions and classes of molecules.
To do so, we consider a wide variety of data sources. We use three existing instruction datasets: SMolInstruct

[ 115 ], Tulu-3 [ 44 ], and the Biomolecular text portion of Mol-Instructions [ 24 ]. SMolInstruct is used to cover the
standard set of chemistry LLM tasks. We supplement this with the non-overlapping portion of Mol-Instructions.
Finally, we include Tulu-3 to preserve general reasoning capability.


**A.1** **Property-Based Synthetic Instruction Data Generation for Contrastive Learning**


Additionally, we augment this data mixture with a significant amount of synthetic data created using realworld property datasets. Given our datasets, we create additional question datapoints for both regression and
classification tasks, such as “Is this molecule <SMILES> ... </SMILES> blood brain barrier permeable?
Yes”. We also consider the opposite direction: property to molecule and multiple properties to molecule, and
unconditional molecule generation. The templates used for constructing this data were created using GPT-4o; 50
were originally generated and then bad templates were removed by hand. Further, we augmented each data point
with a description of the property, also written by GPT-4o.


In addition to these tasks, we also consider the molecule optimization task as described in DrugAssist [ 114 ] (e.g.,
given molecule A, improve property X). However, their approach has fundamental limitations due to the reliance
on oracle models. These models may be out-of-distribution for molecules within our dataset, and low-quality
models may propagate errors into our training data. To address this issue, we consider “activity cliffs” [ 85, 121 ]
within existing property datasets to train the model for molecule optimization. Activity cliffs are two molecules
which are structurally similar but have large differences in a given property. We opt to base our definition of
activity cliff on Murcko scaffolds [ 7 ]. This methodology, which is widely used in medicinal chemistry, extracts
the core subgraph, or scaffold, of a molecule. We found that this approach was much more computationally
feasible on large-scale molecule datasets than approaches like fingerprint similarity [6].


Given nominal data (e.g., toxic, kinase inhibitor, banana smell), we look for a pair of molecules that have the
same scaffold but only one molecule has the desired property. Given numerical data (e.g., solubility, power































Figure 6: Overview of Data Creation.


19








conversion efficiency, HOMO-LUMO gap), we instead look for molecules which have a property difference of 1
standard deviation. This forms the positive-negative same-scaffold portion of our data. We also consider pairs of
molecules that have different scaffolds but the same property. Here, our goal is to teach the model to consider
function over structure. As an example, we may ask “Propose a molecule with a different structure than [MOL]
... [/MOL] that still demonstrates anticoagulant properties. [MOL] ... [/MOL]”. For a select number of property
types, we use oracle models instead of ground truth data. Please see Appendix B.2.3 for more information.


**A.2** **Data Filtering**


Due to the large size of our dataset, we filter our data to only keep the most frequent 100k (50k end blocks and
50k mid blocks), 10k (5k and 5k), and 1000 blocks (500 and 500) for experiments. This is because there are far
fewer molecule tokens compared to text (each training sample only has up to about 10). Due to Zipf’s law [ 127 ],
in the full dataset, a single molecule token may only appear in one example in the entire training corpus. Without
considerably scaling the compute budget, understanding this additional block is difficult. Overall, this filtering
enables us to learn more efficiently and requires less memory resources for training the model, and allows us to
better test the model architecture. Please see the section on training details for more information in Appendix C
and see Appendix E for source property datasets.

|Data Type|Full Data|Only Blocks|Top 100k|Top 10k|Top 1000|
|---|---|---|---|---|---|
|**All**|36,641,170|20,910,431|14,823,280|6,195,903|1,054,124|
|**Existing Data Sources**|3,117,841|1,208,365|1,049,473|537,674|149,994|
|SMolInstruct<br>Tulu-3<br>Mol-Instructions Biomol. Text|2,124,738<br>939,343<br>53,760|215,262<br>939,343<br>53,760|56,370<br>939,343<br>53,760|14,242<br>469,672<br>53,760|2,300<br>93,934<br>53,760|
|**Synthetic Real Data**|21,290,353|9,294,434|7,711,548|3,960,633|705,210|
|Classifcation<br>Molecule Generation<br>Positive Negative Same Scaffold<br>Positive Positive Different Scaffold<br>Property to Molecule<br>Multi-Property to Molecule<br>Scaffold+Property to Molecule<br>Regression|5,612,215<br>535,317<br>3,795,820<br>660,925<br>6,676,957<br>572,505<br>705,833<br>2,730,781|3,771,038<br>316,630<br>113,390<br>477,976<br>3,125,097<br>556,107<br>405,497<br>528,699|3,192,583<br>245,034<br>65,566<br>256,435<br>2,878,012<br>533,647<br>226,696<br>313,575|1,337,619<br>150,001<br>16,286<br>191,720<br>1,639,322<br>423,089<br>80,448<br>122,148|223,341<br>27,393<br>2,007<br>33,579<br>307,780<br>78,793<br>13,078<br>19,239|
|**Synthetic Oracle Data**|12,232,976|10,407,632|6,062,259|1,697,596|198,920|
|Classifcation<br>Positive Negative Same Scaffold<br>Scaffold+Property to Molecule<br>Property to Molecule<br>Regression|2,077,327<br>72,763<br>1,169,407<br>13,257<br>8,900,222|1,778,874<br>58,645<br>925,055<br>13,254<br>7,631,804|1,058,754<br>25,035<br>453,087<br>8,841<br>4,516,542|299,444<br>4,935<br>113,049<br>906<br>1,279,262|35,168<br>469<br>13,642<br>2<br>149,639|



Table 2: Dataset categories and their respective sample counts.





|Subset|Source|Molecules<br>Total Tokenized Untokenized Scaffolds|Col4|Col5|Col6|Molecule Tokens<br>Cap Mid Total Synthesis-Aware|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|Full Data|SMolInstruct<br>Our data<br>Total|1,951,205<br>6,160,565<br>7,994,305|1,566,030<br>5,270,982<br>6,787,879|385,175<br>864,212<br>1,178,957|510,464<br>1,109,562<br>1,537,424|||||
|Only Blocks|SMolInstruct<br>Ours<br>Total|459,910<br>3,830,543<br>4,220,604|459,910<br>3,830,543<br>4,220,604|0<br>0<br>0|145,614<br>705,641<br>799,267|157,204<br>531,472<br>598,470|59,681<br>175,903<br>203,810|216,885<br>707,375<br>802,280|50,788<br>189,770<br>214,431|
|Top 100k|SMolInstruct<br>Ours<br>Total|146,079<br>2,345,519<br>2,458,034|146,079<br>2,345,519<br>2,458,034|0<br>0<br>0|49,743<br>429,960<br>457,032|22,871<br>49,941<br>50,000|14,809<br>49,780<br>50,000|37,680<br>99,721<br>100,000|10,930<br>27,823<br>28,220|
|Top 10k|SMolInstruct<br>Ours<br>Total|37,686<br>821,238<br>848,674|37,686<br>821,238<br>848,674|0<br>0<br>0|12,373<br>147,524<br>153,144|4,130<br>5,000<br>5,000|2,534<br>4,998<br>5,000|6,664<br>9,998<br>10,000|2,618<br>3,468<br>3,487|
|Top 1000|SMolInstruct<br>Ours<br>Total|4,867<br>109,554<br>112,657|4,867<br>109,554<br>112,657|0<br>0<br>0|1391<br>19,639<br>20,101|477<br>500<br>500|359<br>500<br>500|836<br>1,000<br>1,000|420<br>432<br>432|


Table 3: Breakdown of molecule data.


20


**B** **Synthetic Data Generation**


**B.1** **Task Formulation for Molecular Design**


To train our modular chemical language model (mCLM), we generate synthetic data that reflect realistic scenarios
encountered in molecular design. These include tasks relevant to drug discovery and organic photovoltaic (OPV)
materials design. Our goal is to equip the model with the ability to understand and reason over molecular
representations and natural language prompts across a diverse set of tasks.


_**Drug Discovery Tasks:**_ In the context of drug discovery, chemists often engage in iterative and multi-objective
optimization processes, where molecules are evaluated, modified, or generated based on various physicochemical
and pharmacological properties. These tasks typically involve querying for specific properties, modifying
structures to meet certain design criteria, or generating novel candidates that satisfy given constraints. We
consider the following tasks that a chemist may perform:


     - **Text-to-Molecule Generation:** Generate a molecule from a textual description of its structure or
properties.


     - **Property Prediction:** Given a molecule and a property of interest, predict whether the molecule
possesses the property (binary classification) or the quantitative value of the property (regression).


     - **Molecular Optimization:** Modify a given molecule to satisfy or improve a specific property.


     - **Scaffold-Constrained Generation:** Given a scaffold and a target property, generate a molecule that
satisfies both the structural constraint and the property constraint.


_**OPV Material Design Tasks:**_ To support broader applications of mCLM beyond drug discovery, we also
incorporate tasks relevant to organic photovoltaic (OPV) material design. OPVs are an emerging class of
lightweight, flexible materials used for solar energy harvesting, where the power conversion efficiency (PCE)
is the primary performance metric. A typical OPV device is composed of a donor molecule and an acceptor
molecule. The donor is responsible for absorbing sunlight and generating excitons (electron-hole pairs), while
the acceptor facilitates charge separation and electron transport. The chemical compatibility and electronic
alignment between the donor and acceptor molecules critically influence the resulting PCE. To enable learning
in this domain, we define the following OPV-specific tasks


     - **PCE Prediction** : Predict the PCE of a given donor–acceptor pair.


     - **Donor/Acceptor Completion** : Given a donor (or acceptor) and a target PCE, generate the complementary component (acceptor or donor) that achieves the desired performance.


     - **Constrained Completion with Scaffold** : Generate donor or acceptor molecules that match a given
scaffold and achieve a target PCE.


**B.2** **Instruction Tuning Data Generation**


**B.2.1** **Prompt-Answer Templates**


To generate instructional data, we construct a pool of question and answer templates for each task. These
templates include multiple paraphrased variants to introduce linguistic diversity and improve the model’s
generalization capability. During data generation, a question template is randomly sampled from the question set
and populated with sample-specific content. Likewise, a corresponding answer template is sampled from the
answer set to form a complete prompt–response pair. For example:


     - **Question Template:** _“Given [a molecule] and [a property of interest], modify the molecule to achieve_

_[desired property value].”_


     - **Answer Template:** _“The [property] of [molecule] is [value].”_


This templating strategy allows us to produce a large number of diverse, semantically equivalent training
instances that support instruction tuning across multiple molecular design tasks.


**B.2.2** **Label Sources for Instruction Tuning Data**


To enable diverse and meaningful pretraining for mCLM, we incorporate both experimentally derived and
model-generated labels, covering a broad spectrum of molecular properties critical to chemistry, pharmacology,
and materials science. This dual-labeling strategy allows the model to learn from abundant low-level molecular
descriptors while also reasoning over high-level functional and biological endpoints.


_**Low-Level Molecular Properties from ChEMBL:**_ For foundational chemical descriptors, we leverage the
ChEMBL25 database—a comprehensive bioactivity resource containing approximately 2 million compounds


21


with rich structural and physicochemical annotations. ChEMBL25 serves as an abundant and reliable source of
labels for low-level properties that are widely used in cheminformatics pipelines. From this corpus, we select
a core set of descriptors that are most informative for molecular design: Hydrogen bond acceptors (HBA),
Hydrogen bond donors (HBD), LogP (octanol–water partition coefficient), Molecular weight (MolWt), Number
of aromatic rings, Number of rotatable bonds, Topological polar surface area (TPSA). These descriptors are
inexpensive to compute and provide critical insights into molecular solubility, permeability, and synthetic
feasibility—making them essential for early-stage screening and property-based filtering.


_**High-Level Molecular Properties via Oracle Labeling:**_ In addition to low-level properties, we aim to expose the
model to high-level functional endpoints that capture complex biological phenomena. Such endpoints are central
to pharmacokinetics, drug safety, and efficacy, but they are rarely available in large quantities due to the high
cost of experimental validation. Consequently, labeled datasets for these tasks are limited in size and diversity.
To address this challenge, we employ the oracle ensemble models to generate synthetic labels for a curated set of
ADMET tasks.


**B.2.3** **Ensemble Oracle Model:**


To generate high-quality synthetic labels for downstream tasks, we construct oracle models focused on ADMET
property prediction. We select tasks from the Therapeutics Data Commons (TDC) benchmark [‡] using the
following criteria:


     - **Relevance to Drug Discovery:** The task must reflect a critical aspect of drug efficacy or toxicity.


     - **Predictability:** The task must be reliably predictable using existing models. Specifically, we evaluate
all 22 ADMET-related classification tasks in TDC and retain only those where standard models achieve
an area under the ROC curve (AUC) greater than 0.80. This ensures the synthetic labels are sufficiently
accurate for training purposes.


Based on these criteria, we select six tasks:


     - **AMES** (mutagenicity),


     - **BBBP** (blood-brain barrier permeability),


     - **CYP3A4** inhibition (metabolism),


     - **DILI** (drug-induced liver injury),


     - **HIA** (human intestinal absorption),


     - **PGP** (P-glycoprotein substrate classification).


TDC provides predefined scaffold-based data splits with an 8:1:1 ratio for train, validation, and test sets. This
splitting strategy ensures that structurally dissimilar compounds are separated across subsets, encouraging
generalization to novel scaffolds.


Although TDC provides leaderboards for these tasks, many top-performing entries lack reproducible code
or working implementations. For instance, the authors of one of the top submissions explicitly acknowledge
on GitHub that their code is not runnable. [§] Therefore, we opt to use robust foundation models—FARM,
ChemBERTA-2, and a GNN—for ensemble learning.


     - **FARM** [68]: A SMILES-based BERT model trained with functional group-aware tokenization.


     - **ChemBERTA-2** [ 2 ]: A large-scale transformer model trained on millions of canonical SMILES

sequences.


     - **GNN** [19]: A graph neural network trained on molecular graphs with atom- and bond-level features.


To build the ensemble, we use each model as a feature extractor. The extracted features are concatenated and
passed through a fully connected layer for final prediction. This ensemble approach is stacking, where multiple
base learners feed into a meta-learner. For each task, we select a threshold that maximizes the F1 score on the
validation set. This threshold is then used to binarize the predicted logits into class labels. The performance of
our ensemble model across the selected tasks is summarized in Table 4.


   - `[https://tdcommons.ai/benchmark/admet_group/overview/](https://tdcommons.ai/benchmark/admet_group/overview/)`
§ `[https://github.com/maplightrx/MapLight-TDC](https://github.com/maplightrx/MapLight-TDC)`


22


Table 4: Performance (AUC) of individual models and the ensemble across six selected ADMET
tasks.


**Model** **AMES** **Pgp** **DILI** **BBBP** **CYP3A4** **HIA**


FARM [68] 0.88 0.89 0.79 **0.94** 0.88 0.92
GNN [19] 0.75 0.78 **0.86** 0.79 0.80 0.81
ChemBERTa-2 [2] 0.86 0.89 0.81 0.93 0.86 **0.99**
**Ensemble** **0.89** **0.91** 0.84 0.93 **0.89** **0.99**


23


**C** **Training Procedure**


We employed Qwen2.5-3B [ 112 ] as the starting LLM for building the mCLM. Generally, we followed the
training procedure from LLaVa [ 56, 58, 47 ]. We used a two-layer MLP with PReLU activation [ 30 ] as an adapter
into the LLM input/output from the GNN. We selected an initial learning rate of 1e-5 for the full model and 1e-6
for the adaptor and LM heads. Further, we used a cosine annealing schedule with a minimum of 1e-6 and 2000
linear warmup steps; AdamW [ 63 ] optimizer was employed. The model was trained on 4 A100 80GB GPUs in
bfloat16 precision.


We found that the model learned the molecule tokens much slower than the text (there is usually a 10x difference
in loss value). Molecule tokens are rarer and show up less in the training data. Because of this, we decided
to separate the molecule classifier head and the language classifier head. We used a standard autoregressive
language modeling loss for both, and we averaged these two losses for the final loss value. The main part of our
training experiments focused on minimizing the molecule loss, since the text loss was easy to optimize. Further,
we found PEFT [ 31 ] was not sufficient to adapt to molecules, so full finetuning was required. Roughly 10-50
examples from each synthetic (data source, task) pair were put into a validation set.


To initialize the GNN weights, we employed the MolCLR [ 103 ] unsupervised contrastive learning technique. We
used AugliChem [ 66 ] for the augmentations: random atom masking, random bond deletion, and motif removal.
One of these augmentation was selected uniformly at random for each data point. The GNN was initialized
using a batch size of 128 and lr of 1e-4 with a cosine schedule. The model was trained on all 800k blocks in the
full data until convergence on a validation set. Please see Appendix **??** for vocabulary examples and their nearest
neighbor embeddings. We tested embedding dimensions between 16 and 4,096 and found 128 dimensions to be
sufficient while minimizing total memory cost. This was necessary because we stored the entire embedding
matrix in GPU memory, which was much faster, but consumed about 20GB VRAM. Doing so allowed us to train
without the GNN during our pretraining process, which is considerably more efficient. We note the GNN can
then be finetuned along with the rest of the mCLM during finetuning to new types of molecules or specific tasks.
While we did consider a sampled softmax to train the mCLM, we found this to limit the learning of the model.


For training the mCLM, we used two stages for pretraining. First, we trained for 1 epoch with everything frozen
except the adaptor, to allow the adaptor to adjust to the LLM representation space. For the second stage, we
trained for 5 epochs with only the GNN embeddings frozen. As discussed in the training data mixture section A,
we used the most frequent 1000 building blocks as our vocabulary.


After pretraining, we finetune the mCLM to standardize it’s outputs for our experiments. During pretraining,
we train for robustness by using a wide variety of responses (e.g., for BBBP prediction we might respond “It is
restricted from entering the central nervous system” instead of ‘No’). For finetuning, we train with standardized
responses for our desired tasks (e.g., “Generate a molecule that has higher blood brain barrier permeability
than [MOL] ... [/MOL].”, “[MOL] ... [/MOL]”. Due to our downstream tasks, we finetuned exclusively on
the molecule optimization task for 5 epochs over 100k examples for each property. We trained using the same
procedure as the pretraining stage, but we selected the best model using validation loss.


**D** **Tokenizer Details**


**D.1** **Synthetic Tokenizer Details**


The synthesis-guaranteed tokenizer disconnects the molecule only at bonds that can be formed by a predetermined small set of reactions, preferably only those that can be performed in an automated manner. For
instance, if amide bond formation is defined as available, the tokenizer will be able to disconnect amide bonds in
the molecule of interest. Up to this point, the protocol is synonymous with classical computational retrosynthesis
but there is a fundamental difference. Namely, the sets of reactions suitable for automated synthesis is very
limited – in fact, state-of-the-art synthesis machines utilize only three types of disconnections (amide bond
formation, as well as Suzuki and Buchwald-Hartwig couplings). This places very stringent requirements on the
groups that can be present in the disconnected blocks – for instance, when the disconnection (say, BuchwaldHartwig coupling) yields an amine functionality on one of the blocks, this block cannot contain any groups that
during the anticipated uses of this block would present a synthetic incompatibility. In the most trivial case, the
block cannot contain another unprotected amine because after the Buchwald-Hartwig disconnection, the block
would feature two amines which, in turn, would present competing reactive sites (in the Buchwald-Hartwig
synthesis but also in the formation of amide bonds). Therefore, the tokenizer performs retrosynthetic operations
while simultaneously checking if they do not lead to blocks with functional groups presenting competing
reactivities. Only disconnections avoiding such problems are allowed. This then guarantees that when the
corresponding blocks are used to make other molecules, they give only the selective synthesis outcomes.


24


**E** **Source Datasets and Databases**


    - Leffingwell odors [76]


   - BACE [108]


    - Flashpoint [86]


   - MUV [108]


    - Tox21 [108]


   - AMES [33]


    - Bioavailability [33]


    - Caco2 [33]


    - Carcinogens [33]


    - cav3_t [33]


    - choline_transporter [33]


    - clearance hepatocyte [33]


   - CYP1A2 [33]


   - CYP2C9 [33]


   - CYP2D6 [33]


   - CYP3A4 [33]


    - DILI (drug induced liver toxicity) [33]


    - Half_life [33]


   - hERG [33]


    - HIA (human intestinal absorption) [33]


    - Hydration free energy [33]


    - kcnq2 [33]


    - LD50 [33]


    - Lipophilicity [108]


    - m1_muscarinic [33]


    - OPV data [69, 62]


    - orexin_receptor [33]


   - PAMPA_NCATS [33]


    - Broccatelli [9]


    - potassium_ion_channel [33]


    - PPBR (Plasma Protein Binding Rate) [33]


    - Pubchem logP [40]


   - SARSCoV2_3CL [33]


   - SARSCoV2_vitro [33]


    - serine_threonine_kinase_33 [33]


    - Skin Reaction [33]


    - Solubility_AqSolDB [33]


    - tyrosyl-dna_phosphodiesterase [33]


    - VDss (volume of distribution at steady state) [33]


    - Molecule Property Cliff Datasets (30+ datasets) [94]


    - Chemical Function (CheF) [42]


    - ChemFOnt: the chemical functional ontology resource [106]


    - Pubchem properties [40]


    - FreeSolv [108]


   - QM8 [108]


25


- QM9 [108]


- Thermosol [108]


- ESOL (Estimated SOLubility) [108]


- Lipo [108]


- BBBP [27]


- ClinTox [108]


- HIV [108]


- SIDER [108]


- Forward synthesis (USPTO) [115]


- Retrosynthesis [115]


- CheBI-20 [16]


- L+M-24 [21]


- HBA [27]


- HBD [27]


- MolWt [27]


- NumAromaticRings [27]


- rotatable_bonds [27]


- TPSA (topological polar surface area) [27]



26


