## Graph Representational Learning: When Does More Expressivity Hurt Generalization?

Sohir Maskey [∗][,][1][,][2] Raffaele Paolino [1][,][2] Fabian Jogl [3]

Gitta Kutyniok [1][,][2][,][4][,][5] Johannes F. Lutzeyer [6]

1 Department of Mathematics, LMU Munich
2 Munich Center for Machine Learning (MCML)
3 Machine Learning Research Unit, CAIML, TU Wien
4 Institute for Robotics and Mechatronics, DLR-German Aerospace Center
5 Department of Physics and Technology, University of Tromsø
6 LIX, ´Ecole Polytechnique, IP Paris, France


Abstract


Graph Neural Networks (GNNs) are powerful tools for learning on structured data,
yet the relationship between their expressivity and predictive performance remains
unclear. We introduce a family of pseudometrics that capture different degrees
of structural similarity between graphs and relate these similarities to generalization, and consequently, the performance of expressive GNNs. By considering a
setting where graph labels are correlated with structural features, we derive generalization bounds that depend on the distance between training and test graphs,
model complexity, and training set size. These bounds reveal that more expressive
GNNs may generalize worse unless their increased complexity is balanced by a
sufficiently large training set or reduced distance between training and test graphs.
Our findings relate expressivity and generalization, offering theoretical insights
[supported by empirical results. Our code is available on GitHub.](https://github.com/RPaolino/GenVsExp)


1 Introduction


Graph Neural Networks (GNNs) (Scarselli et al., 2009; Bronstein et al., 2017) have become a central tool for learning representations of structured data. A major line of research has focused
on improving their expressivity, that is, their capacity to distinguish non-isomorphic graphs, often evaluated with respect to the Weisfeiler-Lehman (WL) hierarchy of graph isomorphism tests
(Weisfeiler & Lehman, 1968; Xu et al., 2019; Morris et al., 2020b, 2023b).


The relationship between expressivity and performance of GNNs remains poorly understood.
While more expressive models are theoretically capable of distinguishing a broader range of nonisomorphic graphs, their practical effectiveness in real-world tasks is not always apparent. On
the one hand, more expressive models have been shown to outperform standard architectures
(Maron et al., 2019a; Bodnar et al., 2021; Bouritsas et al., 2023), even when their additional expressive power does not result in separating more non-isomorphic graphs in the benchmarks at hand
(Zopf, 2022). For instance, the 1-WL test, and by extension simple message-passing neural networks (MPNNs) such as GIN (Xu et al., 2019), can separate all graphs in widely used datasets (Zopf,
2022; Kriege et al., 2020) and almost all random graphs (Babai et al., 1980), but performance is still
far from saturated. On the other hand, less expressive models can outperform their more expressive
counterparts. For example, Bechler-Speicher et al. (2024) show that models which completely discard the graph structure (hence, less-expressive than 1-WL) can outperform sophisticated GNNs in
certain tasks.


Preprint. Under review.
∗ [Corresponding author: maskey@math.lmu.de](mailto:maskey@math.lmu.de)


Test error vs. noise


0.5


0.4


0.3


0.2

0 0.5 1

|Col1|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
||||||||
||||||||
|||||||Mutagenicity<br>BZR<br>NCI109|
||||||||



Noise p



GNN error on cycle task


LF-G

L-G

Sub-G

F 4 -MPNN
F 3 -MPNN

MPNN

|Col1|Train Tes|Col3|
|---|---|---|
|||t|
||||



0 5 10 15


Error (%)



Training loss (M UTAGENICITY )



0.6


0.4


0.2


0

|Col1|Label noise<br>0.0<br>0.2<br>0.5<br>0.8|Col3|
|---|---|---|
||||
|||1.0|

0 50 100


Epoch







Figure 1: Left: Train–test errors for several GNN variants on a synthetic cycle-counting task; moderately expressive models such as F 4 -MPNN (Barcel´o et al., 2021), i.e., MPNNs augmented with
cycle counts, generalize best, while more expressive ones tend to overfit. Center: Training-loss
curves of a MPNN on M UTAGENICITY under increasing label noise p. Right: Corresponding test
errors on BZR, M UTAGENICITY, and NCI109 rises sharply as label-structure correlation is essential for generalization (mean ± standard deviation across five seeds). See Appendix I.1 for more
details.


These contrasting observations suggest a complex and nuanced relationship between expressivity
and performance, raising two critical questions:


1. When does increased expressivity in GNNs help, and when does it hurt performance?


2. If a more expressive GNN performs better on a given task, is it due to its improved expressivity in terms of graph separability?


To explore these questions, we begin with a synthetic graph-classification task in which the labels are
designed to depend on a known structural feature, namely the number of cycles. We train a sequence
of models whose expressive power increases from a plain MPNN to an LF-GNN (Zhang et al., 2024).
As Figure 1 (left) shows, moderately expressive models achieve the lowest test error, while the
most expressive ones overfit, and performance deteriorates on unseen graphs. The result echoes
a well-documented phenomenon in Euclidean deep learning: large neural networks can memorize
arbitrary labels, yet they generalize only when there is genuine correlation between data and labels. Classical complexity measures such as the VC dimension or Rademacher complexity cannot
account for this behavior in over-parametrized regimes (Zhang et al., 2017). A more plausible explanation is that generalization requires a balance between the model’s inductive bias (in our case,
its expressivity) and the structure–label correlation present in the data.


We further test this hypothesis on three real-world graph datasets: BZR, M UTAGENICITY, and
NCI109 (Morris et al., 2020a). We follow the setup from Zhang et al. (2017) by progressively resampling the labels uniformly at random, i.e., introducing label noise, while leaving the graphs
untouched. Figure 1 (center and right) shows that training loss still converges to zero, confirming
the network’s ability to memorize, yet the test error rises sharply as soon as the correlation between
the graphs and labels is destroyed. Together, these experiments indicate that expressivity by itself
is neither strictly harmful nor helpful; model performance ultimately is determined by the model’s
ability to measure similarity in a way that reflects the task-relevant relation between graphs and
labels. In this work, we set out to better understand this phenomenon.


1.1 Our Contribution


We formalize the empirical insight that generalization heavily depends on structure–label correlation
as follows. We introduce a family of pseudometrics, called ζ-Tree Mover Distances (ζ-TMDs), each
parameterized by a graph invariant (e.g., degree distributions or k-WL colors), which measure a
specific level of expressivity. We then consider a graph classification setting where labels correlate
with a fixed ζ-TMD: two graphs are likely to share the same label if they are similar under the chosen
pseudometric. This captures structure–label alignment, a property we empirically validate across
several real-world graph learning tasks, where generalization depends critically on such alignment.


2


Within this framework, we derive data-dependent generalization bounds for models with fixed encoders (e.g., random GNN features) and expressive, end-to-end trainable GNNs (e.g., GIN, GAT,
k-GNNs). Our bound (Theorem 4.1, Equation (4)) decomposes the generalization gap into two
terms: a capacity term, depending on model width, weight norms, and maximum node degree, and
a structural similarity term, which measures the distance between training and test graphs under the
chosen ζ-TMD. This decomposition highlights that generalization improves when the model maps
structurally similar graphs (with respect to the ζ-TMD that correlates with the labels) to similar
representations while keeping model capacity in check.


This perspective not only explains existing empirical observations but also guides model design.
Deeper or more expressive GNNs can improve performance—but only if they enhance the structural
similarity between train and test graphs. Otherwise, increased complexity may fail to improve label
alignment, thereby degrading both generalization and computational efficiency. This trade-off is
especially relevant since higher-order methods often introduce significant computational overhead.
In Section 5, we formalize this phenomenon and show that, in a concrete setting, the optimal GNN
is precisely as expressive as required to capture the relevant structure-label correlation—no more,
no less.


1.2 Related Work


Expressivity in GNNs. A common benchmark for GNN expressivity is the Weisfeiler-Leman (kWL) hierarchy, which measures the ability to distinguish non-isomorphic graphs. Standard MPNNs
are provably limited by 1-WL expressivity (Xu et al., 2019; Morris et al., 2019), while higher-order
k-GNNs (Morris et al., 2020b) and subgraph-based models (Frasca et al., 2022) extend this by incorporating higher-order structural interactions. Structural and positional encodings (Vignac et al.,
2020; Barcel´o et al., 2021) enhance expressivity by injecting global features into node representations. Jogl et al. (2024) offer a unifying view by showing that many expressive architectures can be
simulated via input transformations followed by standard message passing.


However, expressivity often comes at a computational cost: while MPNNs scale linearly with
edges (O(|E|)), subgraph-based and higher-order models scale super-linearly (e.g., O(|V ||E|) or
O(|V | [k] )), making them less viable for large-scale graphs.


Generalization in GNNs. Generalization theory for GNNs has traditionally relied on classical complexity measures such as VC-dimension (Scarselli et al., 2018), Rademacher complexity (Garg et al.,
2020), and PAC-Bayes bounds (Liao et al., 2021). Graphon-based frameworks (Levie, 2024) establish bounds using covering numbers in continuous function spaces. Similarly, Maskey et al. (2022a,
2024) establish tighter bounds using graphon models, but under stronger assumptions on the data
distribution and their analysis does not directly handle expressive GNNs.


Recent works increasingly focus on the interplay between expressivity and generalization.
Morris et al. (2023a) relate 1-WL to VC-dimension in MPNNs. Li et al. (2024) analyze a tradeoff between intra-class concentration and inter-class separation, but only for fixed graph encoders.
Wang et al. (2024) study graphs sampled from manifolds, and Ma et al. (2021) model label–feature
correlations in node classification, but neither framework extends to graph-level tasks or expressive
GNNs.


Most recently, Vasileiou et al. (2024) derive tighter generalization bounds by combining covering
number arguments with the robustness framework of Xu & Mannor (2012), using the fact that
MPNNs are Lipschitz with respect to Tree and Forest distances. Their analysis does not model
structure–label correlation and is limited to standard MPNNs. We refer to Appendix A for further
discussion.


Comparison with Prior Work. While existing approaches have deepened our understanding of
GNN generalization, many rely on idealized assumptions—such as known graphon distributions or
fixed feature maps—that limit applicability to real-world graph learning. The work most closely
related to ours is Ma et al. (2021), which models label-feature alignment but does not support graphlevel tasks or trainable GNNs. In contrast, our framework explicitly models structure-label correlation using task-aligned pseudometrics and supports expressive, end-to-end trainable GNNs.This
enables a fine-grained analysis of how architectural expressivity and task alignment interact. Our
generalization bounds identify when increased expressivity may improve performance—and when
it leads to overfitting—addressing a key open question posed by Morris et al. (2024).


3


2 Preliminaries


Let G denote the set of all simple, undirected graphs, and let G = (V, E) ∈G, where V, or V (G), is
the set of nodes and E is the set of edges. For any node v ∈ V, the neighborhood of v is defined as:
N (v) := {u ∈ V | {v, u} ∈ E}.


Definition 2.1 (Graph Invariant and CRA). A graph invariant is a function ζ : G →C that assigns
a value to each graph such that for any isomorphic graphs G and H, it holds that ζ(G) = ζ(H).


A color refinement algorithm (CRA) ζ (·) is a mapping that assigns to each graph G a function ζ G :
V (G) → P such that for any graph H isomorphic to G, and any isomorphism h : V (H) → V (G),
the CRA satisfies ζ G (v) = ζ H (h(v)) for all v ∈ V (G).


We note that every CRA ζ (·) induces a graph invariant ζ by aggregating the vertex labels into a
multiset. Specifically, the induced graph invariant is defined as ζ(G) := {{ζ G (v)}} v∈V (G), where
{{·}} denotes a multiset. Throughout this work, we use the terms “graph invariant” and “CRA”
interchangeably when the context allows.


Graph invariants vary in their ability to distinguish between graphs. We say that a graph invariant
ζ is more expressive than another graph invariant θ if ζ(G) = ζ(H) implies θ(G) = θ(H) for all
G, H ∈G.


Definition 2.2 (Message Passing Neural Networks (MPNNs)). For a graph G = (V, E) with node
features x ∈ R [|][V][ |×][F], an MPNN updates node v ∈ V at layer t as:


x [(] v [t][+1)] = f [(][t][+1)] [ �] x [(] v [t][)] [,][ □] [u][∈N] [(][v][)] g [(][t][+1)] [ �] x [(] u [t][)],
�� ����


where f [(][t][+1)] and g [(][t][+1)] are MLPs, and □ denotes a permutation-invariant aggregation function.


We focus on sum aggregation, but our framework naturally extends to mean or weighted sum aggregation. After the final message passing layer, node features are typically aggregated into a graphlevel representation, followed by a final MLP.


Similar to MPNNs, the 1-Weisfeiler-Lehman (1-WL) Test updates the node features of input graphs
through local neighborhood aggregation. However, a key distinction is that in 1-WL, both the message and update functions are necessarily injective. 1-WL provides a tight upper bound on the
expressivity of MPNNs (Xu et al., 2019; Morris et al., 2020b).


To quantify similarity between graphs, we use the notion of pseudometrics. In particular, every
graph invariant naturally induces a pseudometric d ζ (G, H) with d ζ (G, H) = 0 if ζ(G) = ζ(H)
and d ζ (G, H) = 1 otherwise. However, such pseudometrics only indicate whether two graphs are
distinguishable by ζ (distance 0 or 1). To capture finer structural similarities, general pseudometrics
are often employed. Conversely, any pseudometric d can induce a graph invariant ζ d by anchoring
comparisons to a fixed graph A ∈G with ζ d,A (G) := d(G, A). Thus, pseudometrics can be seen as
generalizations of graph invariants, offering richer measures of graph similarity.


The Tree Mover’s Distance (TMD) (Chuang & Jegelka, 2022) is a pseudometric that quantifies the
dissimilarity between two graphs. Formally, for graphs G and H, and a depth t, the TMD is defined
as the Wasserstein distance between their distributions of rooted trees up to depth t:


TMD [t] (G, H) = Wasserstein �T [t] (G), T [t] (H)�,


where T [t] (G) and T [t] (H) are the multisets of rooted trees of depth t generated by the 1-WL test for
G and H, respectively. For further details, we refer to Appendix C.


3 Generalized Tree Mover’s Distance for Strongly Simulatable Colorings


We now extend the concept of the TMD to a broader class of CRAs that can be strongly simulated
by the 1-WL test. For detailed proofs of the results presented in this section, refer to Appendix C.2.


A CRA ζ is said to be strongly simulatable if, for any graph G, running t iterations of the CRA on
G can be simulated by running t iterations of the 1-WL test on a suitably transformed graph R [ζ] (G).
This transformation, called the strong simulation under ζ, ensures that the colorings at each 1-WL


4


iteration on R [ζ] (G) are at least as expressive as those of ζ (Jogl et al., 2024) on G. See Appendix B
for more details and examples of CRAs and their corresponding transformed graphs.


For any strongly simulatable CRA ζ, we define a generalized pseudometric as the TMD between the
strong simulations of the graphs under ζ.

Definition 3.1. Let ζ be a strongly simulatable CRA. For any depth t > 0, the ζ-TMD is defined as:


ζ-TMD [t] (G, H) := TMD [t] (R [ζ] (G), R [ζ] (H)), (1)


where R [ζ] (G) and R [ζ] (H) are the strong simulations of G and H under ζ, respectively.
Proposition 3.2. Let ζ be a strongly simulatable CRA. For every t > 0, ζ-TMD [t] is a pseudometric.


Similar to the standard TMD, ζ-TMD [t] (G, H) can be zero even if G ̸= H, as it is a pseudometric.
Nonetheless, it can distinguish graphs that are differentiable by the color refinement algorithm ζ
within T iterations.

Proposition 3.3. Let ζ be a strongly simulatable CRA. If two graphs G and H are distinguished by
ζ after T iterations, then ζ-TMD [T][ +1] (G, H) > 0.


                                                            Another immediate consequence is that MPNNs corresponding to the CRA ζ, referred to as ζ
MPNNs, are Lipschitz continuous with respect to the ζ-TMD. Specifically, we have the following
result:

Theorem 3.4. Let ζ be a strongly simulatable CRA, and let h : G → R [K] be a ζ-MPNN with T
layers, where the message and update functions are Lipschitz continuous with Lipschitz constants
bounded by L g (t) and L f (t), respectively. Suppose h includes a global sum pooling layer followed
by a Lipschitz continuous classifier c with Lipschitz constant L c . Then, for any graphs G and H,


∥h(G) − h(H)∥≤ L · ζ-TMD [T][ +1] (G, H),


where L = L c 2 [T] [ �] [T] t=1 [L] [f] [ (][t][)] [L] [g] [(][t][)] [ and][ ∥· ∥] [denotes the Euclidean vector norm.]


The Lipschitz property established in Theorem 3.4 plays a key role in deriving the generalization
bounds for ζ-MPNNs presented in Section 4. Next, we illustrate the Lipschitz continuity using the
example of F -MPNNs.


3.1 Example: F -MPNNs


The F -Weisfeiler-Leman (F -WL) test generalizes the 1-WL test by incorporating features derived
from a finite family of graphs, F ⊂G. These features, often referred to as motifs or patterns, are
used to enhance node representations.


Specifically, for each node v in a graph G, the feature vector of v is augmented with counts of
patterns in F that include v. Formally, the augmented feature vector is defined as:


x˜ v = �x v, cnt(P 1, G; v), . . ., cnt(P |F|, G; v)�,


where cnt(P, G; v) represents the number of occurrences of the pattern P in G such that v is part
of the pattern. These counts can for example be (injective) homomorphism counts (Bouritsas et al.,
2023) or cycle basis counts (Yan et al., 2024).


If F ⊂ F [˜], then F [˜] -WL is more expressive than F -WL (Barcel´o et al., 2021; Bouritsas et al., 2023).


Correspondingly, F -MPNNs incorporate these motif counts into their message-passing scheme.
Clearly, F -WL can be strongly simulated via a transformed graph R [F] (G) that includes the motif
counts as node features.

Corollary 3.5. Let h be an F -MPNN with T layers. Then, there exists a constant L such that for
any graphs G and H,


∥h(G) − h(H)∥≤ L · F -TMD [T][ +1] (G, H). (2)


We emphasize that this is just one example; analogous definitions of ζ-TMDs and corresponding
versions of Corollary 3.5 can be derived for other GNN architectures, such as k-GNNs (Morris et al.,
2019), see Appendix C.3.


5


4 Generalization Bounds With Respect to Tree Mover’s Distance


In this section, we establish generalization bounds for GNNs using our generalized TMD framework.


4.1 Problem Setup and Assumptions


We consider a classification task where each data point is a graph equipped with node features.
Formally, let G tr and G te denote the fixed sets of training and test graphs, respectively. We assume
that there exists a constant B > 0 such that the norm of each node feature is bounded, i.e.,


∥x(G) i ∥ 2 ≤ B ∀G ∈G tr ∪G te, ∀i ∈ V (G).


Each graph G is assigned a label y G ∈{1, . . ., K}. We assume that, for each class k, there exists a
Lipschitz continuous function η k : G → [0, 1] with respect to some pseudometric pm such that


Pr(y G = k | G) = η k (G),


and set C := max k∈{1,...,K} Lip(η k ). If the labels are sampled according to such functions η k, we
say that the labels y are strongly correlated with pm and write y ∼ pm.


Furthermore, we define ξ pm as the distance between the training set and the test set:


ξ pm = pm (G te, G tr ) := max (3)
G∈G te H [min] ∈G tr [pm(][G, H][)][.]


Given the set of labeled graphs G tr the task of graph-level supervised learning is to learn a classifier
h : G → R [K] from a function family H. Given a classifier h ∈H, the classification for a graph G is
obtained by
y˜ G = argmax h(G)[k],
k∈{1,...,K}


where h(G)[k] refers to the k-th entry of h(G).


For the observed graph labels (y G ) G∈G tr, the empirical margin loss of h on G tr for a margin γ ≥ 0
is defined as
� 1
L [γ] tr [(][h][) :=] N tr � 1 [h(G)[y G ] ≤ (γ + max k≠ y G [h][(][G][)[][k][])]][.]



�

̸



̸

G∈G tr



1 [h(G)[y G ] ≤ (γ + max
k≠ y G [h][(][G][)[][k][])]][.]



̸


Here, 1 is the indicator function. The empirical margin loss of h on G te is defined equivalently. The

�
expected margin loss is defined as follows, L [γ] te [(][h][) :=][ E] y G ∼Pr(y G |G),G∈G te �L [γ] te [(][h][)] � .


4.2 Main Results


In this section, we derive generalization bounds for GNNs, where we focus on the standard approach
involving end-to-end trainable GNNs.


We consider the GNN to be the composition of two functions. Specifically, let e : G → R [b] denote
the graph embedding network, which maps a graph G ∈G into a b-dimensional latent space, and
let c : R [b] → R [K] denote the classifier, which maps embeddings to class scores. Consequently, the
hypothesis space for these models can be written as:


H = C ◦E,


where E represents the space of graph embedding networks and C represents the class of MLP
classifiers. For end-to-end learnable GNNs, both E and C are trainable. In contrast, for models with
fixed encoders, only C is trainable, while E remains fixed.


4.2.1 End-to-End Learnable GNNs


Let ζ represent a CRA that can be strongly simulated by 1-WL. In this context, we consider the
hypothesis space H ζ = C ◦E ζ, where E ζ is the set of all ζ-MPNNs of depth T, where each layer
consists of a message function g [(][t][)] and an update function f [(][t][)] . Both g [(][t][)] and f [(][t][)] are MLPs with
a maximum hidden dimension of b and may contain an arbitrary number of layers. The weight
matrices across all message and update functions are denoted by {W i } [P] i=1 [.]


6


Let C denote the set of MLP classifiers with L layers and a maximum hidden dimension of b. The
weight matrices in the MLP classifier are denoted by {W [˜] l } [L] l=1 [.]


We now present the generalization bound for end-to-end learnable GNNs.
Theorem 4.1. Suppose that y ∼ ζ-TMD [T][ +1] . Under mild assumptions (see Appendix D), for any
γ > 0 and 0 < α < [1] 4 [, with probability at least][ 1][ −] [δ][ over the sample of training labels][ y] [tr] [, we have]

for any h [˜] ∈H ζ



b i [∥][W] [i] [∥] 2 [2] [+][ �] l [∥][W][˜] [l] [∥] 2 [2]
�� �
� N tr [2][α] [(][γ/][8)] [2][/D]



L [0] te [(˜][h][)][ ≤] [L][�] [γ] tr [(˜][h][) +][ O]



N [W] tr [2][i][α] [∥][(] 2 [γ/][+][8)][ �] [2][/D] l [∥][W] [l] [∥] 2 ξ ζ [2][/D] + [b] [2] [ ln] �2NbDC tr [2][α] [γ] [1] (2 [/D] dB [δ] ) [1][/D] [�]



+ CKξ ζ
N tr [2][α] [γ] [1][/D] [δ]



,

�



where ξ ζ := ζ-TMD [T][ +1] (G te, G tr ) is defined in Equation (3), D represents the total number of
learnable weight matrices, b denotes the maximum hidden dimension, d is the maximum degree
of the graphs, and C serves as an upper bound on the spectral norm of all weight matrices.


Theorem 4.1 highlights key factors influencing generalization in learnable graph classifiers, which
are the structural similarity ξ ζ under ζ-TMD, model complexity D, b, {∥W i ∥ 2 } i, {∥W [˜] l ∥ 2 } l,
� �
graph properties such as maximum degree d, and training set size N tr . The structural similarity term
ξ ζ emphasizes the importance of diverse training data. This agrees with empirical observations by
Southern et al. (2025), who demonstrated that augmenting graph representation to maximize TMD
dissimilarity improves predictive performance and generalization. These findings underscore the significance of diverse training data (via task-specific augmentations) and balancing model complexity
to achieve robust graph-based learning.


The proof of Theorem 4.1, given in Appendix E, follows a standard PAC-Bayesian approach
(Neyshabur et al., 2018) and extends it to the correlated setting, following the approach of (Ma et al.,
2021). It leverages the Lipschitz continuity of ζ-MPNNs, established in Theorem 3.4, to derive the
generalization bound. Throughout the remainder of this paper, we use the following simplified version of the bound from Theorem 4.1:



L [0] te [(˜][h][)] ≤ L� [γ] tr [(˜][h][) +][ O] � NMC( tr [2][α] γC◦E [1][/D] ζ )δ
� �� �
complexity term



+ C ξ ζ . (4)
���� �
structural
similarity term



Here, MC(C◦E ζ ) captures the model complexity, i.e., spectral norms of all learnable weight matrices,
hidden dimensions, and maximal graph degree. Notably, the model complexity may increase if
the graph transformation R [ζ] enlarges the size, maximum degree, or node feature dimension of the
original input graphs.


The structural similarity term, ξ ζ, depends on the alignment between training and test graphs under
ζ-TMD. Whether ξ ζ increases or decreases with more expressive networks depends on the task.


The same PAC-Bayes machinery yields analogous bounds when the graph encoder is frozen and
only the MLP head is trained. We relegate the formal statement and proof to Appendix F to keep the
main exposition focused on the end-to-end learnable case.


5 When Does More Expressivity Hurt?


In this section, we explore two scenarios within our framework: first, we identify conditions under which augmenting expressivity beyond task-specific requirements can negatively impact generalization. Second, we highlight conditions where increasing expressivity to accurately capture
task-specific features does not degrade the bound in Theorem 4.1. This gives a possible explanation
of why such graph classifiers achieve an optimal balance between expressivity and generalization,
resulting in superior performance.


To formalize this, consider a classification task where the labels y G are strongly correlated with
the pseudometric F -TMD [T][ +1] for a specific set of substructures F ⊂G. Assume that all MPNNs
considered in this section have T layers. Let F [′] ⊊ F ⊊ F ⊂G [˜] be finite sets of graphs, where
F [′] -MPNNs are less expressive than F -MPNNs, which in turn are less expressive than F [˜] -MPNNs.
Denote the corresponding hypothesis spaces as H F ′, H F, and H F ˜ [.]


7


Our analysis shows that increasing expressivity to the level required to capture task-relevant features (e.g., transitioning from F [′] -MPNNs to F -MPNNs) generally preserves generalization. However, further increasing expressivity beyond this necessary level (e.g., to F [˜] -MPNNs) can degrade
generalization significantly.
Theorem 5.1. Consider the setting above. Then, for any γ > 0 and α < [1] 4 [, with probability at least]

1 − δ over the sample of training labels y tr,


i) the test loss of any F [′] -MPNN classifier h [′], satisfies



�



L [0] te [(][h] [′] [)][ ≤L] [γ] tr [(][h] [′] [) +][ O]



MC(H F ′ )ξ F [1][/D] + Cξ F
N tr [2][α] [γ] [1][/D] [δ]
�



.



where C is described in Theorem 4.1 and ξ F = F -TMD [T][ +1] (G tr, G te ).


ii) the test loss of any F -MPNN classifier h, satisfies



L [0] te [(][h][)][ ≤L] [γ] tr [(][h][) +][ O]



MC(H F )ξ F [1][/D] + Cξ F
N tr [2][α] [γ] [1][/D] [δ]
�



iii) the test loss of any F [˜] -MPNN classifier [˜] h, satisfies



�


�



.


.



L [0] te [(˜][h][)][ ≤L] tr [γ] [(˜][h][) +][ O]


where ξ F ˜ [= ˜][F] [-TMD] [T][ +1] [(][G] [tr] [,][ G] [te] [)][.]



MC(N tr [2] H [α] [γ] F ˜ [1] [)] [/D] [ξ] F [1] ˜ [δ] [/D] + Cξ F ˜
�



Theorem 5.1 highlights the critical role of structural alignment between training and test graphs in
determining generalization performance. In cases i) and ii), the same F -TMD governs the similarity
between training and test graphs, ensuring that the bound remains controlled. However, in case iii),
introducing a more expressive GNN that captures features beyond those captured by F -TMD (with
which the labels are strongly correlated) leads to a higher structural discrepancy ξ F ˜ [≥] [ξ] [F] [, see]
Lemma G.1. These findings underscore the importance of aligning model expressivity with the
structural requirements of the task, as excessive expressivity can increase our generalization bound
in Theorem 4.1.


6 Experiments


In this section, we evaluate GNNs on both synthetic and real-world graph datasets. We introduce
two tasks to evaluate how structural similarity between training and test graphs, as well as taskrelevant expressivity, impact classification performance and generalization. All experiments use
10-fold cross-validation, and we report the mean accuracy or error. Additional experiments and
tasks, details and extended results are provided in Appendix I.



Task 1: Median-Based Labeling with Cycle Counts.
We generate 3,000 random graphs from Erd˝os–R´enyi,
Barab´asi–Albert, and Stochastic Block Model distributions. The sum of 3-cycle and 4-cycle counts is computed
for each graph, and graphs with counts below the dataset’s
median receive label 0, while those above receive label
1. We evaluate multiple GNN variants, including standard MPNNs, F l -MPNNs where F l contains cycles up to
length l, Subgraph GNNs (Sub-G), Local 2-GNNs (L-G),
and Local Folklore 2-GNNs (LF-G). Model expressivity
increases strictly in this order. We report training and test
accuracies at both the final and the epoch with the best
validation performance. Results can be found in Table 1,
and more details and experiments in Appendix I.



Table 1: Test accuracy on Erd˝os–R´enyi
graphs for Task 1. All GNNs achieve a
train accuracy greater than 0.99. More
results in Table 4 in Appendix I.


Model Test Accuracy


LF-G 0.8450 ± 0.0135

L-G 0.8543 ± 0.0063

Sub-G 0.8623 ± 0.0058
F 7 -MPNN 0.9660 ± 0.0065
F 4 -MPNN 0.9793 ± 0.0068
F 3 -MPNN 0.8657 ± 0.0085
MPNN 0.8490 ± 0.0045



Task 2: Real-World Datasets We evaluate our framework on six graph classification datasets from
the TUDataset (Morris et al., 2020a). Results on BZR, M UTAGENICITY, and NCI109 include:


8


BZR







1


0.9



0.9


0.8







0.9


0.85


0.8





0.7

|NCI109|Col2|Col3|
|---|---|---|
|#layers<br>1<br>3<br>5|#layers<br>1<br>3<br>5|#layers<br>1<br>3<br>5|
|#layers<br>1<br>3<br>5|#layers<br>1<br>3<br>5|#layers<br>1<br>3<br>5|
|#la|#la|#la|
|#la|#la||

10 [1] 10 [2] 10 [3] 10 [4]


TMD to training set



0.8

|Col1|Col2|yers<br>1<br>3<br>5|
|---|---|---|
|#l|#l|#l|

10 [1] 10 [2] 10 [3] 10 [4]


TMD to training set



0.75

|Mutagenicity|Col2|Col3|
|---|---|---|
||#layers<br>1<br>3<br>5|#layers<br>1<br>3<br>5|
|#la|#la|#la|
|#la|#la||

10 [1] 10 [2] 10 [3] 10 [4]


TMD to training set



Figure 2: Accuracy of a GIN with 1, 3, and 5 layers versus TMD (log scale) to the training dataset.




- 10 [4]



NCI109




- 10 [4]



Mutagenicity



1.4


1.2


1


0.8
0 200 400 600 800


TMD to training dataset



0.1


5 · 10 [−][2]



2


1.5


1

0 500 1,000


TMD to training dataset



0.2


0.15


0.1


5 · 10 [−][2]



Figure 3: Error-bound curves for Mutagenicity, and NCI109. Each plot shows our theoretical bound
(blue, left axis) and the empirical generalization error (red, right axis) as a function of TMD to the
training set. Shaded areas indicate ±1 standard deviation across 10 random splits.


Figure 2, which plots test accuracy versus ζ-TMD distance, and Figure 3, which compares our
bound to the observed generalization gap. Additional results on PROTEINS, AIDS, COX2, and
experiments on fixed encoders via molecular fingerprints (Gainza et al., 2019) appear in Appendix I.


Results and Discussion. In Task 1, GNNs that explicitly incorporate task-relevant cycle information, in particular F 4 -MPNNs, outperform MPNNs and expressive GNNs like Local Folklore
2-GNNs. Since the labels in Task 1 strongly correlated with F 4 -TMD, these results align with our
theoretical findings in Section 5: GNNs that effectively leverage features strongly correlated with
the task generalize better than more expressive models. On real-world datasets, we observe that
classification accuracy declines as test graphs become more distant from the training set, in line
with our theoretical insights in Theorem 4.1. Importantly, our bound closely aligns with the observed generalization gap across these datasets. By explicitly capturing structure–label correlation,
our framework yields significantly tighter generalization bounds compared to standard PAC-Bayes
bounds (Liao et al., 2021), which are often orders of magnitude larger (e.g., on the order of 10 [16]
compared to our 10 [4] ).


7 Conclusion


We introduced a framework for analyzing GNN generalization in settings where graph labels correlate with different pseudometrics. Our analysis provided generalization bounds that emphasize the
role of structural similarity between training and test data. We show that increasing expressivity
does not necessarily degrade generalization if it aligns with the task. However, both theoretical and
empirical results show that excessive expressivity can worsen generalization and predictive perfor
mance.


Empirical results confirm that GNNs whose embeddings align with task-relevant structures, i.e.,
those that are proven to be Lipschitz continuous with respect to pseudometrics strongly correlated
with the labels, achieve better generalization. We show that performance degrades for test graphs that
are structurally distant from the training set, supporting our theoretical findings. Additionally, we


9


identify cases where increased expressivity can either improve or hinder generalization, depending
on task alignment, providing insights for GNN design.


Limitations. While our framework enables comparisons between F -MPNNs, in general the dependence of our bound in Theorem 4.1 on different TMDs makes direct model comparisons challenging.
These bounds serve as qualitative guidelines rather than precise estimates, as they are not tight and
may not reflect practical performance. Moreover, the relevant pseudometric is often unknown and
possibly expensive to compute, limiting direct applicability and leaving the identification of suitable
metrics an open problem.


Future Work. Our generalization bounds improve with increased structural similarity between test
and train graphs. Future work could explore augmentation techniques that generate synthetic graphs
to improve this similarity, thereby boosting generalization. Additionally, developing strategies to
adapt model expressivity to input data could enhance performance while maintaining flexibility.


Acknowledgements


S. Maskey is funded by the NSF-Simons Research Collaboration on the Mathematical and Scientific
Foundations of Deep Learning (MoDL) (NSF DMS 2031985).


R. Paolino is funded by the Munich Center for Machine Learning (MCML).


F. Jogl is funded by the Center for Artificial Intelligence and Machine Learning (CAIML) at TU
Wien.


G. Kutyniok acknowledges support by the DAAD programme Konrad Zuse Schools of Excellence in
Artificial Intelligence, sponsored by the Federal Ministry of Education and Research. G. Kutyniok
acknowledges support by the project ”Genius Robot” (01IS24083), funded by the Federal Ministry
of Education and Research (BMBF). G. Kutyniok acknowledges support by the gAIn project, which
is funded by the Bavarian Ministry of Science and the Arts (StMWK Bayern) and the Saxon Ministry
for Science, Culture and Tourism (SMWK Sachsen). G. Kutyniok acknowledges partial support by
the Munich Center for Machine Learning (MCML), as well as the German Research Foundation
under Grants DFG-SPP-2298, KU 1446/31-1 and KU 1446/32-1. Furthermore, G. Kutyniok is
supported by LMUexcellent, funded by the Federal Ministry of Education and Research (BMBF)
and the Free State of Bavaria under the Excellence Strategy of the Federal Government and the
L¨ander as well as by the Hightech Agenda Bavaria.


J. Lutzeyer is supported by the French National Research Agency (ANR) via the “GraspGNNs”
JCJC grant (ANR-24-CE23-3888).


References


Abboud, R., Ceylan, I. I., Grohe, M., and Lukasiewicz, T. The Surprising Power of Graph Neural Networks with Random Node Initialization. In International Joint Conference on Artificial
Intelligence (IJCAI), pp. 2112–2118, 2021. doi: 10.24963/ijcai.2021/291.


Abboud, R., Dimitrov, R., and Ceylan, I. I. Shortest Path Networks for Graph Property Prediction.
In Learning on Graphs Conference (LoG), pp. 5:1–5:25, 2022.


Babai, L., Erd¨os, P., and Selkow, S. M. Random graph isomorphism. SIAM J. Comput., 9:628–635,
[1980. URL https://api.semanticscholar.org/CorpusID:9371805.](https://api.semanticscholar.org/CorpusID:9371805)


Barcel´o, P., Geerts, F., Reutter, J., and Ryschkov, M. Graph neural networks with local graph
parameters. In Advances in Neural Information Processing Systems (NeurIPS), pp. 25280–25293,
2021.


Barcel´o, P., Geerts, F., Reutter, J., and Ryschkov, M. Graph neural networks
with local graph parameters. In Ranzato, M., Beygelzimer, A., Dauphin, Y.,
Liang, P., and Vaughan, J. W. (eds.), Advances in Neural Information Processing Systems, volume 34, pp. 25280–25293. Curran Associates, Inc., 2021. URL
[https://proceedings.neurips.cc/paper_files/paper/2021/file/d4d8d1ac7e00e9105775a6b660dd3cbb-Pap](https://proceedings.neurips.cc/paper_files/paper/2021/file/d4d8d1ac7e00e9105775a6b660dd3cbb-Paper.pdf)


10


Bause, F., Jogl, F., Indri, P., Drucks, T., Penz, D., Kriege, N., G¨artner, T., Welke, P., and Thiessen, M.
Maximally expressive gnns for outerplanar graphs. In NeurIPS 2023 Workshop: New Frontiers
in Graph Learning, 2023.


Bechler-Speicher, M., Amos, I., Gilad-Bachrach, R., and Globerson, A. Graph neural networks use
[graphs when they shouldn’t, 2024. URL https://arxiv.org/abs/2309.04332.](https://arxiv.org/abs/2309.04332)


Bevilacqua, B., Frasca, F., Lim, D., Srinivasan, B., Cai, C., Balamurugan, G., Bronstein, M. M.,
and Maron, H. Equivariant Subgraph Aggregation Networks. In International Conference on
Learning Representations (ICLR), 2021.


Bodnar, C., Frasca, F., Otter, N., Wang, Y. G., Li`o, P., Montufar, G., and Bronstein, M. M. Weisfeiler and lehman go cellular: CW networks. In Beygelzimer, A., Dauphin, Y., Liang, P.,
and Vaughan, J. W. (eds.), Advances in Neural Information Processing Systems, 2021. URL
[https://openreview.net/forum?id=uVPZCMVtsSG.](https://openreview.net/forum?id=uVPZCMVtsSG)


Bouritsas, G., Frasca, F., Zafeiriou, S., and Bronstein, M. M. Improving graph neural network
expressivity via subgraph isomorphism counting. IEEE Transactions on Pattern Analysis and
Machine Intelligence, 45(1):657–668, January 2023. ISSN 1939-3539. doi: 10.1109/tpami.2022.
[3154319. URL http://dx.doi.org/10.1109/TPAMI.2022.3154319.](http://dx.doi.org/10.1109/TPAMI.2022.3154319)


Bronstein, M. M., Bruna, J., LeCun, Y., Szlam, A., and Vandergheynst, P. Geometric Deep Learning:
Going beyond Euclidean data. IEEE Signal Processing Magazine, 34(4):18–42, 2017. ISSN 15580792. doi: 10.1109/MSP.2017.2693418.


Buitinck, L., Louppe, G., Blondel, M., Pedregosa, F., Mueller, A., Grisel, O., Niculae, V., Prettenhofer, P., Gramfort, A., Grobler, J., Layton, R., VanderPlas, J., Joly, A., Holt, B., and Varoquaux,
G. API design for machine learning software: experiences from the scikit-learn project. In ECML
PKDD Workshop: Languages for Data Mining and Machine Learning, pp. 108–122, 2013.


Chen, Z., Villar, S., Chen, L., and Bruna, J. On the equivalence between graph isomorphism testing
and function approximation with gnns. In Advances in Neural Information Processing Systems
(NeurIPS), pp. 15868–15876, 2019.


Chuang, C.-Y. and Jegelka, S. Tree mover’s distance: Bridging graph metrics and stability of graph neural networks. In Oh, A. H., Agarwal, A., Belgrave, D., and
Cho, K. (eds.), Advances in Neural Information Processing Systems, 2022. URL
[https://openreview.net/forum?id=Qh89hwiP5ZR.](https://openreview.net/forum?id=Qh89hwiP5ZR)


Cybenko, G. Approximation by superpositions of a sigmoidal function. Mathematics of control,
signals and systems, 2(4):303–314, 1989.


Dasoulas, G., Santos, L. D., Scaman, K., and Virmaux, A. Coloring graph neural networks for
node disambiguation. In International Joint Conference on Artificial Intelligence (IJCAI), pp.
2126–2132, 2020. ISBN 978-0-9992411-6-5.


Davidson, Y. and Dym, N. On the h¨older stability of multiset and graph neural networks, 2024. URL
[https://arxiv.org/abs/2406.06984.](https://arxiv.org/abs/2406.06984)


Dell, H., Grohe, M., and Rattan, G. Lov´asz meets Weisfeiler and Leman. In International Colloquium on Automata, Languages, and Programming (ICALP), volume
107 of LIPIcs, pp. 40:1–40:14, 2018. doi: 10.4230/LIPICS.ICALP.2018.40. URL
[https://doi.org/10.4230/LIPIcs.ICALP.2018.40.](https://doi.org/10.4230/LIPIcs.ICALP.2018.40)


Dimitrov, R., Zhao, Z., Abboud, R., and Ceylan, I. I. Plane: Representation learning over planar graphs. In Advances in Neural Information Processing Systems (NeurIPS), 2023. URL
[https://openreview.net/forum?id=u2RJ0I3o3j.](https://openreview.net/forum?id=u2RJ0I3o3j)


Du, S. S., Hou, K., P´oczos, B., Salakhutdinov, R., Wang, R., and Xu, K. Graph
neural tangent kernel: Fusing graph neural networks with graph kernels, 2019. URL
[https://arxiv.org/abs/1905.13192.](https://arxiv.org/abs/1905.13192)


Fey, M. and Lenssen, J. E. Fast graph representation learning with PyTorch Geometric. In ICLR
Workshop on Representation Learning on Graphs and Manifolds, 2019.


11


Franks, B. J., Morris, C., Velingker, A., and Geerts, F. Weisfeiler-leman at the margin: When more
expressivity matters. In Forty-first International Conference on Machine Learning, 2024.


Frasca, F., Bevilacqua, B., Bronstein, M., and Maron, H. Understanding and Extending Subgraph
GNNs by Rethinking Their Symmetries. In Advances in Neural Information Processing Systems
(NeurIPS), pp. 31376–31390, 2022.


Gainza, P., Sverrisson, F., Monti, F., Rodol`a, E., Boscaini, D., Bronstein, M. M.,
and Correia, B. E. Deciphering interaction fingerprints from protein molecular surfaces using geometric deep learning. Nature Methods, 17:184 – 192, 2019. URL
[https://api.semanticscholar.org/CorpusID:209167696.](https://api.semanticscholar.org/CorpusID:209167696)


Garg, V., Jegelka, S., and Jaakkola, T. Generalization and representational limits of graph neural
networks. Proceedings of the 37th International Conference on Machine Learning, 119:3419–
[3430, 13–18 Jul 2020. URL https://proceedings.mlr.press/v119/garg20c.html.](https://proceedings.mlr.press/v119/garg20c.html)


Geerts, F. and Reutter, J. L. Expressiveness and approximation properties of graph neural
networks. In International Conference on Learning Representations (ICLR), 2022. URL
[https://openreview.net/forum?id=wIzUeM3TAU.](https://openreview.net/forum?id=wIzUeM3TAU)


Gilmer, J., Schoenholz, S. S., Riley, P. F., Vinyals, O., and Dahl, G. E. Neural message passing
for quantum chemistry. In International conference on machine learning, pp. 1263–1272. PMLR,
2017.


Graziani, C., Drucks, T., Jogl, F., Bianchini, M., franco scarselli, and G¨artner, T. The expressive
power of path-based graph neural networks. In Forty-first International Conference on Machine
[Learning, 2024. URL https://openreview.net/forum?id=io1XSRtcO8.](https://openreview.net/forum?id=io1XSRtcO8)


Hagberg, A., Swart, P., and S Chult, D. Exploring network structure, dynamics, and function using
networkx. Technical report, Los Alamos National Lab.(LANL), Los Alamos, NM (United States),
2008.


Hornik, K., Stinchcombe, M., and White, H. Multilayer feedforward networks are universal approximators. Neural networks, 2(5):359–366, 1989.


Huang, Y., Peng, X., Ma, J., and Zhang, M. Boosting the cycle counting power of graph neural
networks with I [2] -GNNs. In International Conference on Learning Representations (ICLR), 2022.


Jin, E., Bronstein, M., Ceylan, I. I., and Lanzinger, M. Homomorphism counts for graph neural
networks: All about that basis. In International Conference on Machine Learning (ICML), 2024.


Jogl, F., Thiessen, M., and G¨artner, T. Expressivity-preserving gnn simulation. Advances in Neural
Information Processing Systems, 36, 2024.


Keriven, N. and Peyr´e, G. Universal invariant and equivariant graph neural networks. In Advances
in Neural Information Processing Systems (NeurIPS), pp. 7090–7099, 2019.


Kingma, D. P. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980, 2014.


Kriege, N. M., Johansson, F. D., and Morris, C. A survey on graph kernels. Applied Network
Science, 5:1–42, 2020.


Kruskal, J. B. Nonmetric multidimensional scaling: A numerical method. Psychometrika, 29(2):
115–129, 1964.


Levie, R. A graphon-signal analysis of graph neural networks. Advances in Neural Information
Processing Systems, 36, 2024.


Li, S., Geerts, F., Kim, D., and Wang, Q. Towards bridging generalization and expressivity of graph
[neural networks, 2024. URL https://arxiv.org/abs/2410.10051.](https://arxiv.org/abs/2410.10051)


Liao, R., Urtasun, R., and Zemel, R. A pac-bayesian approach to generalization bounds for
graph neural networks. In International Conference on Learning Representations, 2021. URL
[https://openreview.net/forum?id=TR-Nj6nFx42.](https://openreview.net/forum?id=TR-Nj6nFx42)


12


Lim, D., Robinson, J. D., Zhao, L., Smidt, T., Sra, S., Maron, H., and Jegelka, S. Sign and basis
invariant networks for spectral graph representation learning. In International Conference on
Learning Representations (ICLR), 2022.


Lov´asz, L. M. Operations with structures. Acta Mathematica Academiae Scientiarum Hungarica,
[18:321–328, 1967. URL https://api.semanticscholar.org/CorpusID:121512807.](https://api.semanticscholar.org/CorpusID:121512807)


Ma, J., Deng, J., and Mei, Q. Subgroup generalization and fairness of graph neural networks. In
Beygelzimer, A., Dauphin, Y., Liang, P., and Vaughan, J. W. (eds.), Advances in Neural Informa[tion Processing Systems, 2021. URL https://openreview.net/forum?id=68B1ezcffDc.](https://openreview.net/forum?id=68B1ezcffDc)


Maron, H., Ben-Hamu, H., Shamir, N., and Lipman, Y. Invariant and equivariant graph networks.
In International Conference on Learning Representations (ICLR), 2018.


Maron, H., Ben-Hamu, H., Serviansky, H., and Lipman, Y. Provably Powerful Graph Networks. In
Advances in Neural Information Processing Systems (NeurIPS), pp. 2153–2164, 2019a.


Maron, H., Fetaya, E., Segol, N., and Lipman, Y. On the universality of invariant networks.
In International Conference on Machine Learning (ICML), pp. 4363–4371, 2019b. URL
[https://proceedings.mlr.press/v97/maron19a.html.](https://proceedings.mlr.press/v97/maron19a.html)


Maskey, S., Levie, R., Lee, Y., and Kutyniok, G. Generalization analysis of message passing neural networks on large random graphs. Advances in Neural Information Processing Systems, 35,
2022a.


Maskey, S., Parviz, A., Thiessen, M., St¨ark, H., Sadikaj, Y., and Maron, H. Generalized laplacian
positional encoding for graph representation learning. In NeurIPS 2022 Workshop on Symmetry
and Geometry in Neural Representations, 2022b.


Maskey, S., Kutyniok, G., and Levie, R. Generalization bounds for message passing networks on
mixture of graphons. arXiv preprint arXiv:2404.03473, 2024.


Michel, G., Nikolentzos, G., Lutzeyer, J. F., and Vazirgiannis, M. Path Neural Networks: Expressive
and Accurate Graph Neural Networks. In International Conference on Machine Learning (ICML),
pp. 24737–24755, 2023.


Morris, C., Ritzert, M., Fey, M., Hamilton, W. L., Lenssen, J. E., Rattan, G., and Grohe, M. Weisfeiler and Leman Go Neural: Higher-Order Graph Neural Networks. In AAAI Conference on
Artificial Intelligence (AAAI), pp. 4602–4609, 2019. doi: 10.1609/aaai.v33i01.33014602.


Morris, C., Kriege, N. M., Bause, F., Kersting, K., Mutzel, P., and Neumann, M. Tudataset: A collection of benchmark datasets for learning with graphs, 2020a. URL
[https://arxiv.org/abs/2007.08663.](https://arxiv.org/abs/2007.08663)


Morris, C., Rattan, G., and Mutzel, P. Weisfeiler and leman go sparse: Towards scalable higherorder graph embeddings. In Advances in Neural Information Processing Systems (NeurIPS), pp.
21824–21840, 2020b.


Morris, C., Rattan, G., Kiefer, S., and Ravanbakhsh, S. Speqnets: Sparsity-aware permutationequivariant graph networks. In International Conference on Machine Learning (ICML), pp.
16017–16042. PMLR, 2022.


Morris, C., Geerts, F., T¨onshoff, J., and Grohe, M. WL meet VC. In Krause, A.,
Brunskill, E., Cho, K., Engelhardt, B., Sabato, S., and Scarlett, J. (eds.), Proceedings of the 40th International Conference on Machine Learning, volume 202 of Proceedings of Machine Learning Research, pp. 25275–25302. PMLR, 23–29 Jul 2023a. URL
[https://proceedings.mlr.press/v202/morris23a.html.](https://proceedings.mlr.press/v202/morris23a.html)


Morris, C., Lipman, Y., Maron, H., Rieck, B., Kriege, N. M., Grohe, M., Fey, M., and Borgwardt,
K. Weisfeiler and Leman go Machine Learning: The Story so far. Journal of Machine Learning
[Research, 24:333:1–333:59, 2023b. URL http://jmlr.org/papers/v24/22-0240.html.](http://jmlr.org/papers/v24/22-0240.html)


Morris, C., Frasca, F., Dym, N., Maron, H., Ismail [˙] [˙] Ilkan Ceylan, Levie, R., Lim, D., Bronstein,
M., Grohe, M., and Jegelka, S. Future directions in the theory of graph machine learning. In
International Conference on Machine Learning (ICML), 2024.


13


Neyshabur, B., Bhojanapalli, S., and Srebro, N. A PAC-bayesian approach to spectrally-normalized
margin bounds for neural networks. In International Conference on Learning Representations,
[2018. URL https://openreview.net/forum?id=Skz_WfbCZ.](https://openreview.net/forum?id=Skz_WfbCZ)


Nguyen, H. and Maehara, T. Graph homomorphism convolution. In International Conference on Machine Learning (ICML), pp. 7306–7316, 2020. URL
[https://proceedings.mlr.press/v119/nguyen20c.html.](https://proceedings.mlr.press/v119/nguyen20c.html)


Paolino, R., Maskey, S., Welke, P., and Kutyniok, G. Weisfeiler and leman go loopy: A new hierarchy for graph representational learning. In The Thirty-eighth Annual Conference on Neural Infor[mation Processing Systems, 2024. URL https://openreview.net/forum?id=9O2sVnEHor.](https://openreview.net/forum?id=9O2sVnEHor)


Papp, P. A. and Wattenhofer, R. A theoretical comparison of graph neural network extensions. In
International Conference on Machine Learning, pp. 17323–17345. PMLR, 2022.


Qian, C., Rattan, G., Geerts, F., Niepert, M., and Morris, C. Ordered subgraph aggregation networks.
Advances in Neural Information Processing Systems (NeurIPS), pp. 21030–21045, 2022.


Sato, R., Yamada, M., and Kashima, H. Approximation ratios of graph neural networks for combinatorial problems. Advances in Neural Information Processing Systems, 32, 2019.


Sato, R., Yamada, M., and Kashima, H. Random features strengthen graph neural networks. In
SIAM International Conference on Data Mining (SDM), pp. 333–341, 2021. doi: 10.1137/1.
[9781611976700.38. URL https://doi.org/10.1137/1.9781611976700.38.](https://doi.org/10.1137/1.9781611976700.38)


Scarselli, F., Gori, M., Tsoi, A. C., Hagenbuchner, M., and Monfardini, G. The Graph Neural
Network Model. IEEE Transactions on Neural Networks, 20(1):61–80, 2009. doi: 10.1109/TNN.
2008.2005605.


Scarselli, F., Tsoi, A. C., and Hagenbuchner, M. The vapnik–chervonenkis dimension of graph and
recursive neural networks. Neural Networks, 108:248–259, 2018.


Southern, J., Eitan, Y., Bar-Shalom, G., Bronstein, M., Maron, H., and Frasca, F. Balancing efficiency and expressiveness: Subgraph gnns with walk-based centrality, 2025. URL
[https://arxiv.org/abs/2501.03113.](https://arxiv.org/abs/2501.03113)


Tinhofer, G. Graph isomorphism and theorems of birkhoff type. Computing, 36:285–300, 1986.
[URL https://api.semanticscholar.org/CorpusID:23977711.](https://api.semanticscholar.org/CorpusID:23977711)


Tinhofer, G. A note on compact graphs. Discrete Applied Mathematics, 30:253–264, 1991. URL
[https://api.semanticscholar.org/CorpusID:7530138.](https://api.semanticscholar.org/CorpusID:7530138)


Tropp, J. A. An introduction to matrix concentration inequalities. Found. Trends Mach.
Learn., 8(1–2):1–230, may 2015. ISSN 1935-8237. doi: 10.1561/2200000048. URL
[https://doi.org/10.1561/2200000048.](https://doi.org/10.1561/2200000048)


T¨onshoff, J., Ritzert, M., Wolf, H., and Grohe, M. Walking out of the weisfeiler leman hierarchy:
[Graph learning beyond message passing, 2023. URL https://arxiv.org/abs/2102.08786.](https://arxiv.org/abs/2102.08786)


Vasileiou, A., Finkelshtein, B., Geerts, F., Levie, R., and Morris, C. Covered forest: Fine-grained generalization analysis of graph neural networks, 2024. URL
[https://arxiv.org/abs/2412.07106.](https://arxiv.org/abs/2412.07106)


Vignac, C., Loukas, A., and Frossard, P. Building powerful and equivariant graph neural networks with structural message-passing. In Advances in Neural Information Processing Systems
(NeurIPS), pp. 14143–14155, 2020.


Wang, Z., Cervino, J., and Ribeiro, A. A manifold perspective on the statistical generalization of
graph neural networks. arXiv preprint arXiv:2406.05225, 2024.


Weisfeiler, B. and Lehman, A. A. A Reduction of a Graph to a Canonical Form and an Algebra
Arising During This Reduction. Nauchno-Technicheskaya Informatsia, Ser. 2(N9):12–16, 1968.


14


Welke, P., Thiessen, M., Jogl, F., and G¨artner, T. Expectation-complete graph representations with
homomorphisms. In International Conference on Machine Learning (ICML), pp. 36910–36925,
[2023. URL https://proceedings.mlr.press/v202/welke23a.html.](https://proceedings.mlr.press/v202/welke23a.html)


Wijesinghe, A. and Wang, Q. A new perspective on ”how graph neural networks go beyond
weisfeiler-lehman?”. In International Conference on Learning Representations, 2022. URL
[https://openreview.net/forum?id=uxgg9o7bI_3.](https://openreview.net/forum?id=uxgg9o7bI_3)


Xu, H. and Mannor, S. Robustness and generalization. Machine Learning, 86(3):391–423, 2012.
doi: 10.1007/s10994-011-5268-1.


Xu, K., Hu, W., Leskovec, J., and Jegelka, S. How powerful are graph neural networks? In
International Conference on Learning Representations (ICLR), 2019.


Yan, Z., Ma, T., Gao, L., Tang, Z., Chen, C., and Wang, Y. Cycle invariant positional encoding for
graph representation learning. In Learning on Graphs Conference, pp. 4–1. PMLR, 2024.


You, J., Gomes-Selman, J. M., Ying, R., and Leskovec, J. Identity-aware Graph Neural Networks.
AAAI Conference on Artificial Intelligence (AAAI), pp. 10737–10745, 2021. ISSN 2374-3468.
doi: 10.1609/aaai.v35i12.17283.


Zhang, B., Luo, S., Wang, L., and He, D. Rethinking the expressive power of GNNs via graph
biconnectivity. In The Eleventh International Conference on Learning Representations, 2023.
[URL https://openreview.net/forum?id=r9hNv76KoT3.](https://openreview.net/forum?id=r9hNv76KoT3)


Zhang, B., Gai, J., Du, Y., Ye, Q., He, D., and Wang, L. Beyond Weisfeiler-Lehman: A quantitative
framework for GNN expressiveness. In International Conference on Learning Representations
(ICLR), 2024.


Zhang, C., Bengio, S., Hardt, M., Recht, B., and Vinyals, O. Understanding deep learning requires
rethinking generalization. In International Conference on Learning Representations, 2017. URL
[https://openreview.net/forum?id=Sy8gdB9xx.](https://openreview.net/forum?id=Sy8gdB9xx)


Zopf, M. 1-wl expressiveness is (almost) all you need, 2022. URL
[https://arxiv.org/abs/2202.10156.](https://arxiv.org/abs/2202.10156)


15


Notation



c (MLP) classifier
G A graph G = (V, E)
G The set of all graphs
N (v) Neighborhood of vertex v in graph G
x v Feature of node v
∥· ∥ 2 Frobenius norm
∥· ∥ Spectral norm
TD w Tree Distance weighted by function w
TMD [T] w Tree Mover’s Distance at depth T with weight

w
T G [T] Multiset of depth-T computation trees for
graph G
P Prior distribution in PAC-Bayes framework
Q Posterior distribution in PAC-Bayes framework
LLˆ [γ][γ] Expected margin loss with marginEmpirical margin loss with margin γ γ
h Classifier function (e.g., a MPNN + MLP)
H Hypothesis space
E Graph embedding networks (e.g., a MPNN)
C Final classifer (e.g., a MLP)

   Pr( ) Probability function
G tr Training graphs
G te Test graphs
TMD [L] w [(][G] [tr] [,][ G] [te] [)] Distance between G tr and G te
N tr Number of training graphs
N te Number of test graphs
b Maximal hidden dimension of classifier function
B Maximum L [2] -norm of input node features
d Maximum degree of all graphs in training or

test set
d(f ) Depth of MLP f
T Number of MPNN layers
C Maximum Frobenius norm of any learnable
weight matrix
D Number of learnable weight matrices in hypothesis space
g [(][t][)] Message function in layer t
f [(][t][)] Update function in layer t


16


A Detailed Related Work


A.1 Expressivity of GNNs


Expressivity in standard neural networks is often associated with their ability to approximate functions within a specific function class. For example, early works showed that MLPs can approximate
any continuous function (Cybenko, 1989; Hornik et al., 1989). In the context of GNNs, however, expressivity is more commonly measured by the ability to distinguish between non-isomorphic graphs.
This focus stems from computational challenges associated with achieving universality in GNNs
and is further supported by the Stone-Weierstrass theorem: a GNN that can distinguish all graphs is
also capable of approximating any continuous function on graphs (Chen et al., 2019; Dasoulas et al.,
2020). Consequently, practical research often centers on characterizing the distinguishing power of
specific GNN architectures (Xu et al., 2019; Morris et al., 2023b).


Xu et al. (2019); Morris et al. (2019) established that the expressive power of standard MPNNs is
limited by the 1-WL test. To overcome this limitation, later works introduced higher-order GNNs
based on k-WL and its local variants (Maron et al., 2018; Morris et al., 2020b; Geerts & Reutter,
2022). These models are theoretically universal (Maron et al., 2019b; Keriven & Peyr´e, 2019),
meaning they can distinguish any non-isomorphic graphs and approximate continuous functions
on graphs. However, their expressivity comes at the cost of exponential time and space complexity
with respect to k, making them impractical for large-scale applications. To reduce this complexity,
Morris et al. (2020b); Zhang et al. (2024) proposed local k-WL variants, while Abboud et al. (2022)
introduced k-hop GNNs, which expand the receptive field to k-hop neighborhoods. Despite these
improvements, the computational complexity of these approaches remains exponential in k.


Subgraph-based models further enhance expressivity by decomposing graphs into subgraphs and
aggregating their information (Papp & Wattenhofer, 2022; Bevilacqua et al., 2021; You et al., 2021;
Frasca et al., 2022; Huang et al., 2022). Although these models are more expressive than 1-WL, their
power is bounded by 3-WL (Frasca et al., 2022). Moreover, subgraph GNNs increase computational
complexity significantly, often scaling quadratically or cubically with the number of nodes N, which
worsens the computational complexity of standard MPNNs by a factor of N .


Most subgraph-based GNNs associate a family of subgraphs with specific nodes or edges by either
deleting or marking nodes. However, other strategies for subgraph representation have also been explored. For instance, Michel et al. (2023); Graziani et al. (2024); Paolino et al. (2024) focus on paths
to enhance expressivity, while T¨onshoff et al. (2023) leverage random walks for similar purposes.


Positional encodings (PEs) and structural encodings (SEs) have emerged as effective strategies to
enhance the expressivity of MPNNs. PEs augment node representations with additional information, such as unique node identifiers (Vignac et al., 2020), random features (Abboud et al., 2021;
Sato et al., 2021), or spectral features like eigenvectors (Lim et al., 2022; Maskey et al., 2022b). In
contrast, SEs enrich MPNNs by embedding structural information about the graph. Examples of SEs
include subgraph counts (Bouritsas et al., 2023) and homomorphism counts (Nguyen & Maehara,
2020; Barcel´o et al., 2021; Welke et al., 2023; Jin et al., 2024).


While PEs and SEs enhance the expressivity of MPNNs by modifying the initial node features,
another line of research focuses on using computational graphs that differ from the input graph. For
instance, Dimitrov et al. (2023) and Bause et al. (2023) propose graph transformations that enable
MPNNs to achieve universality for specific classes of graphs, such as (outer-)planar graphs. More
broadly, Jogl et al. (2024) demonstrate that many expressive GNN variants, including k-GNNs and
subgraph GNNs, can be simulated by applying suitable graph transformations followed by standard
message passing.


While incorporating SEs does not increase the forward-pass complexity of MPNNs, it introduces
significant preprocessing overhead. For instance, computing homomorphism counts for graphs with
treewidth k requires O(N [k] ) operations, where N is the number of nodes. This preprocessing complexity becomes exponential in k, making it computationally prohibitive for achieving expressivity
beyond k-WL.


Most prior work evaluates GNN expressivity using the k-WL hierarchy, which provides a qualitative
measure of distinguishing power but does not quantify the specific substructures a GNN can encode.
To address this gap, Zhang et al. (2024) proposed homomorphism counts as a quantitative measure
of expressivity. Building on the work of Lov´asz (1967), they demonstrated that homomorphism


17


counts are a complete graph invariant, meaning that two graphs are isomorphic if and only if their
homomorphism counts are identical. Tinhofer (1986, 1991) showed that 1-WL is equivalent to
counting homomorphisms from graphs with treewidth one, while Dell et al. (2018) extended this to
prove that k-WL corresponds to counting homomorphisms from graphs with treewidth k.


Recent studies have further explored the relationship between homomorphism counts and GNN expressivity. For example, Barcel´o et al. (2021) showed that MPNNs augmented with homomorphism
counts as initial node features can count homomorphisms of trees augmented with the included
patterns. Similarly, Paolino et al. (2024) demonstrated that MPNNs enriched with specific path information can count homomorphisms of cactus graphs.


A.2 Generalization Bounds for GNNs


The generalization capabilities of Graph Neural Networks (GNNs) have been studied from various
theoretical perspectives. Scarselli et al. (2018) provided an early understanding of GNN capacity by
deriving generalization bounds for implicitly defined GNNs based on their VC-dimension. Building
on this, Du et al. (2019) analyzed the generalization behavior of GNNs in the infinite-width limit
using the Graph Neural Tangent Kernel (GNTK), offering insights into their asymptotic performance
as network width grows unbounded.


Focusing on data-dependent approaches, Garg et al. (2020) and Liao et al. (2021) investigated the
generalization properties of specific MPNNs with sum aggregation. By employing Rademacher
complexity and PAC-Bayes methods, they established bounds that depend on the observed training
data, shedding light on how factors like data distribution and architectural choices influence generalization.


Levie (2024) introduced the graphon-signal cut distance, a metric for measuring similarity between
graph-signal distributions, and demonstrated that MPNNs are Lipschitz-continuous with respect to
this distance. This insight enabled the derivation of generalization bounds for MPNNs in the context
of arbitrary graph-signal distributions. However, these bounds exhibit a slow convergence rate of
O(1/ log log( [√] m)), where m is the number of training graphs. This slow rate arises from the
generality of their assumptions, which accommodate highly flexible graph-signal distributions.


The connection between GNN expressivity and generalization was further explored by Morris et al.
(2023a), who showed that the number of graphs distinguishable by the 1-WL test is directly linked
to the VC-dimension of GNNs. This result highlights the role of the Weisfeiler-Lehman hierarchy
in understanding both the combinatorial expressivity and theoretical capacity of GNNs. In the restricted setting of linear separability, margin-based bounds have been proposed to partially bridge
theory and practice (Franks et al., 2024), yet our broader understanding of how expressivity influences generalization remains incomplete.


Li et al. (2024) provide a novel perspective on the generalization behavior of graph neural networks
by decoupling the representation learning component from the classification step. Their framework
considers fixed graph encoders—such as MPNNs, k-WL, or homomorphism-based models—which
map graphs into an embedding space. A separate, typically parametric, classifier (e.g., a softmaxbased MLP) is then applied to these embeddings. This setting allows for a focused study of the
generalization ability of classifiers conditioned on precomputed graph representations, shifting attention away from the learning dynamics of the GNN and toward the geometry and concentration
properties of the induced embedding distributions.


Their analysis formalizes how generalization depends on two key factors: intra-class concentration,
i.e., how tightly embeddings from the same class cluster, and inter-class separation, i.e., how well
embeddings of different classes are separated. These are quantified using the 1-Wasserstein distance between class-conditional embedding distributions. The main theoretical result establishes a
generalization bound on the classifier’s margin loss, showing it can be upper-bounded in terms of
these geometric quantities. Importantly, the bound incorporates the expressivity of the graph encoder through a Lipschitz constant that quantifies how much the embedding distribution of a more
expressive encoder (bounding in distinguishing power) can distort the geometry of a less expressive
one (that is used for calculating the graph embeddings). This captures how changes in expressivity
influence intra-class concentration and inter-class separation, and thus directly affect generalization.


18


Although the results elegantly characterize the trade-off between expressivity and generalization, a
central limitation is that the graph encoders are fixed. They are fixed feature extractors, often derived from CRAs or fixed GNN architectures. As such, the framework does not directly reflect the
behavior of trainable GNNs in practical deep learning pipelines, where representation learning and
classifier fitting are tightly coupled. Additionally, in contrast to our correlation-based analysis, the
generalization bounds in Li et al. (2024) require the existence of a fixed positive margin, which is a
strong assumption that may not hold in practice. Our framework is more general, as it does not rely
on margin separability and can quantify generalization even in the presence of label noise or overlapping classes. Nonetheless, the insights are valuable: they reveal conditions under which more expressive encoders can improve generalization—specifically, when expressivity increases intra-class
concentration without excessively harming inter-class separation. In this way, the paper offers a principled theoretical basis for interpreting empirical phenomena observed in GNN performance across
datasets and model classes.


Related to our work, Maskey et al. (2022a, 2024) analyzed scenarios where graph labels are correlated with random graph models, based on graphons. They demonstrated that MPNNs generalize
better as the size of the sampled graphs increases, since the statistical properties of larger graphs
more closely approximate those of the underlying random graph models.


The approach by Maskey et al. (2022a, 2024) is limited because it assumes labels are linked to
random graph models, where many specific assumptions are made about the underlying graphon
governing the data. These assumptions may not hold in practical scenarios, making their results less
general and potentially less applicable to real-world tasks. In contrast, our framework accommodates
arbitrary correlations between graph labels and structural features, as long as they can be described
by a Lipschitz-continuous distribution. This broader scope makes our method suitable for analyzing
a wide variety of graph datasets, including those where the graph generation process is not well
understood or where random graph model assumptions are too restrictive.


The work most closely related to ours is (Ma et al., 2021), which studies generalization in a semisupervised node classification setting. Their analysis considers a scenario where node labels are
correlated with features derived from the node’s local neighborhood and its attributes. Using a PACBayes approach that heavily inspired our work, they show that generalization improves when the
extracted features are similar between the training and test sets. However, their framework is limited
by the assumption of a fixed, non-learnable graph encoder, and their results do not generalize to
multi-graph settings or models with learnable parameters.


In contrast, our approach provides a general framework to analyze GNN generalization in settings
where graph labels are correlated with structural features. This is achieved by introducing a pseudometric, such as the Tree Mover’s Distance, which captures structural differences between graphs.
Unlike prior works, our framework does not rely on restrictive assumptions about the underlying
graph distribution. Instead, we assume only that the labels are generated by a Lipschitz-continuous
probability distribution with respect to the pseudometric. This allows us to analyze a broad range
of tasks where the graph structure plays a critical role in determining labels. By explicitly connecting generalization bounds to structural alignment between training and test graphs, our framework
offers a flexible and robust method to study GNN performance in diverse applications.


Our framework overcomes these limitations by supporting learnable GNN architectures and extending naturally to multi-graph settings. This allows for a broader analysis of generalization, including
GNNs beyond 1-WL expressivity. Moreover, our approach bridges the gap between theory and practice by providing insights into how the interplay between model capacity, structural similarity, and
feature alignment affects performance.


B Simulatable Color Refine Algorithms


It is possible to represent many different GNNs as MPNNs without loss in expressivity. For this,
Jogl et al. (2024) developed the concept of simulation. Intuitively, a GNN with t > 0 layers can
be simulated if we can map its input domain to the set of graphs and achieve the same expressivity
with a t-layer MPNN on this adapted set of graphs. To generalize to different types of GNNs, one
represents GNNs φ as color refinement functions that iteratively refine a coloring on some relational
structure X.


19


Definition B.1. Let φ be a color update function. Let R be a mapping from the domain of φ to the set
of graphs. [1] We consider two arbitrary relational structures from the domain of φ, say X and X [′] . We
say φ can be strongly simulated under R if for every t ≥ 0 it holds that WL [t] (R(X)) = WL [t] (R(X [′] ))
implies that φ [t] (X) = φ [t] (X [′] ).


As an example, consider 3-WL from Section C.3. It can be seen as a color update function c that operates on a set of labeled 3-tuples, i.e. in iteration t > 0 it refines the coloring of tuple (v 1, v 2, v 3 ) ∈ V [3]

by utilizing the coloring c [(][t][−][1)] :


c [t] (v 1,v 2,v 3 ) [=][ HASH] �c [t] ( [−] v 1 [1],v 2,v 3 ) [,] �C 1 [t] [((][v] [1] [, v] [2] [, v] [3] [))][, . . ., C] 3 [t] [((][v] [1] [, v] [2] [, v] [3] [))] � [�]


where
C 1 [t] [((][v] [1] [, v] [2] [, v] [3] [)) =][ HASH] �{{c [t] ( [−] w,v [1] 2,v 3 ) [|][ w][ ∈] [V][ }}] �,

C 2 [t] [((][v] [1] [, v] [2] [, v] [3] [)) =][ HASH] �{{c [t] ( [−] v 1 [1],w,v 3 ) [|][ w][ ∈] [V][ }}] �,

C 3 [t] [((][v] [1] [, v] [2] [, v] [3] [)) =][ HASH] �{{c [t] ( [−] v 1 [1],v 2,w) [|][ w][ ∈] [V][ }}] � .

Instead of using 3-WL, we can create the graph G [⊗][3] with vertices (v 1, v 2, v 3 ) ∈ V [3] and three types
of edges
E 1 = ∪ v 1,v 2,v 3 ∈V {{(v 1, v 2, v 3 ), (w, v 2, v 3 )} | w ∈ V },


E 2 = ∪ v 1,v 2,v 3 ∈V {{(v 1, v 2, v 3 ), (v 1, w, v 3 )} | w ∈ V },


E 3 = ∪ v 1,v 2,v 3 ∈V {{(v 1, v 2, v 3 ), (v 1, v 2, w)} | w ∈ V }.


Observe, that for a tuple (v 1, v 2, v 3 ) the neighborhood E j contains exactly those tuples as aggregated in the definition of C j . We can merge these three edge sets E 1, E 2, E 3 into a single edge
set E by using edge features that encode from which of the three sets the edge originates. Such a
transformation R it allows for the strong simulation of 3-WL.


B.1 Other Strongly-Simulatable Architectures


A GNN/WL variant is strongly simulated when there exists a structure-to-graph encoding R such
that applying R to the input and running a depth–t MPNN reproduces—layer by layer—the colours
(or hidden states) produced by the original depth–t model (Definition B.1). Table 3 summarises
some architectures that admit such a simulation and sketches the key transformation behind R; full
proofs are in (Jogl et al., 2024).


C Tree Mover’s Distance


We summarize some important results from Chuang & Jegelka (2022) and Davidson & Dym (2024).
We first start with the definition of the tree mover’s distance which provides us with a tool to compare
two graphs based on their computational trees quantitatively.


C.1 Tree Mover’s Distance


The definition and notations in this section largely follow (Chuang & Jegelka, 2022).

Definition C.1. Let G = (V, E) be a graph. We define the depth-T computational tree T v [T] [of node]
v recursively by connecting the neighbors of the leaf nodes of T v [T][ −][1] to the tree. We set T v [1] [:=][ v][ as]
the single node tree without any edges. The multiset of depth-T computation trees defined by G is
denoted by T G [T] [:=][ {{][T] [ T] v [}}] [v][∈][V] [. Additionally, for a tree][ T][ with root][ r][, we denote by][ T] [r] [the multiset]
of subtrees that root at the descendants of r.


In other words, the depth-T computational tree T v [T] [of node][ v][ is the 1-WL computational tree of]
node v after T − 1 iterations. To compare two multisets of computational tree we need to augments

trees.


1 Jogl et al. (2024) introduces some additional restrictions on R that we omit for the sake of simplicity.


20


Model / Algorithm Graph transformation R(G)


VVC-GNN (Sato et al., 2019) For a given port ordering, write on each edge direction the port of the source and target node.


k-WL / k-GNN (Morris et al., Compute all k-tuples of nodes. Create a node for each k-tuple and encode the isomorphism
2019) class of each tuple as a node feature. Connect tuples differing in one position encoding this
postion as an edge feature.
δ-k-(L)WL / GNN (Morris et al., Similar as the k-tuple graph above: when connecting tuples add a local/global flag encoding
2020b) whether the nodes that differ in the tuple form an edge in the original graph. For δ-k-LWL,
only connect tuples when these nodes do form an edge.
(k, s)-LWL / SpeqNet Similar as δ-k-WL above: keep only tuple-vertices whose induced subgraph has ≤ s com(Morris et al., 2022) ponents.
GSN-e / GSN-v (Bouritsas et al., For pre-computed subgraph pattern counts, augment original node and edge features with
2023) these counts.
DS-WL / DS-GNN For a given policy π to generate subgraphs, create a graph by taking the disjoint union of all
(Bevilacqua et al., 2021) extracted subgraphs π(G).
k-OSWL / OSAN (Qian et al., For each k tuple of vertices in the graph (“k-ordered subgraphs”), create a copy of all ver2022) tices in the original graph and use node features to encode the atomic type of that node in
this ordered subgraph. In each subgraph, either link all vertices or only neighbors in the
original graph.
Mk-GNN (Papp & Wattenhofer, For a given set of marked nodes, on each edge encode whether the target node is marked or
2022) unmarked.
GMP (Wijesinghe & Wang, 2022) Attach structural coefficients as node or edge features.


Shortest-Path Nets (Abboud et al., For i ∈ 1, . . ., k add an edge between every pair of nodes with shortest path distance i
2022) and encode i as a feature on that edge.
Generalised-Distance WL For a given distance metric d and graph G, add an edge between every pair of nodes u, v
(Zhang et al., 2023) and encode the metric d G (u, v) as a feature on this edge.


Table 3: GNN families whose per-layer updates can be exactly reproduced by a 1-WL–equivalent
MPNN on the transformed graph R(G).


Definition C.2. A blank tree T ∅ is defined as a tree graph that contains a single node and no edge,
where the node feature is the zero vector 0 p ∈ R [p] . We define T ∅ [n] [as the multiset of][ n][ blank trees.]
Definition C.3. Let T v, T u be two multisets of trees. We define ρ as function that augments a pair
of trees with blank trees as follows:

ρ : (T v, T u ) �→ �T v ∪ T ∅ [max(][|T] [u] [|−|T] [v] [|][,][0)], T u ∪ T ∅ [max(][|T] [v] [|−|T] [u] [|][,][0)] � . (5)

Definition C.4. Let w : N → R [+] be a depth-dependent weighting function. For two trees T a, T b,
we define the tree distance TD w (T a, T b ) between T a and T b recursively as

TD w (T a, T b ) := ∥x a − x b ∥ + w(T ) · OT TD w (ρ(T a, T b )) if T > 1 (6)
�∥x a − x b ∥ otherwise,


where T = max(Depth(T a ), Depth(T b )) and


We note that the optimal transport OT with respect to some metric d between two multisets x =
{{x 1, . . ., x n }} and y = {{y 1, . . ., y n }} of the same size n is defined via



OT d (x, y) = min
σ



� d �x i, y σ(i) � . (7)


i



Definition C.5. Let G, H ∈G, w : N → R [+], and T ≥ 0. The tree mover’s distance between G and
H is defined as
TMD [T] w [(][G, H][) =][ OT] [TD] w �ρ(T G [T] [,][ T] H [ T] [)] �, (8)
where T G [T] [and][ T] H [ T] [are multisets of the depth-][T][ computation trees of graphs][ G][ and][ H][, respectively.]


We note that, for simplicity, we omit the weighting function w the corresponding subscript in the
definition of TMD [T] w [and simply write TMD] [T] w [in the main part of this manuscript.]


C.2 Proofs in Section 3


Proof of Proposition 3.2. By (Chuang & Jegelka, 2022, Theorem 6), TMD [t] w [is a pseudometric. It is]
easy to see that ζ-TMD [t] w [is also a pseudometric. For example, given][ G, H][ ∈G][, we have]

ζ-TMD(G, H) = TMD(R [ζ] (G), R [ζ] (H))



= TMD(R [ζ] (H), R [ζ] (G))
= ζ-TMD(H, G),


21



(9)


showing the symmetry of ζ-TMD [t] w [.]


Proof of Proposition 3.3. By (Chuang & Jegelka, 2022, Theorem 7), if two graphs G [′] and H [′] are
determined to be non-isomorphic in WL iteration T and w(t) > 0 for all 0 < t ≤ T + 1, then
TMD [T] w [ +1] (G [′], H [′] ) > 0.


If ζ distinguishes G and H after T iterations, then WL determines R [ζ] (G) and R [ζ] (H) to be nonisomorphic, i.e., TMD [T] w [ +1] (R [ζ] (G), R [ζ] (H)) > 0. Then,

ζ-TMD [T] w [ +1] (G, H) > 0.


We reformulate and prove a more general version of Theorem 3.4, where we consider general
message functions on multisets that are Lipschitz continuous on the multiset domain, and update
function that are Lipschitz on the standard Euclidean latent space. This follows the approach in
(Davidson & Dym, 2024), where a similar version was proved in Theorem F.2. in their manuscript.
However, in contrast, we calculate the explicit constant of the Lipschitz constant which we will need
for later proofs.


Theorem 3.4 then follows as a corollary as permutations-invariant aggregation functions composed
of a MLP followed by sum aggregation are Lipschitz continuous on multisets.
Lemma C.6. Consider a MPNN of the form

x [(] v [t][)] = f [(][t][)] [ �] x v [(][t][−][1)], g [(][t][)] [ �] {{x u [(][t][−][1)], }} u∈N (v) �� (10)

with message and update functions �g [(][t][)], f [(][t][)] [�] [T] t=1 [. Consider also a global readout function][ e][ of the]
form
h(G) = c �{{x [(] v [T][ )] }} v∈V (G) � .

Suppose that for all t = 1, . . ., T, the message and update functions are Lipschitz continuous with
Lipschitz constants bounded by L g (t) and L f (t), respectively. Suppose that the readout function is
Lipschitz continuous with Lipschitz constants bounded by L c . Then, for all layers t = 0, 1, . . ., T
and for all pairs of graphs G, H ∈G and all pairs of nodes u ∈ V (G) and v ∈ V (H), we have


t

���x (ut) [−] [x] [(] v [t][)] ��� ≤ � L g (t [′] ) L f (t [′] ) 2 [t] TD �T u [(][t][+1)], T v [(][t][+1)] � . (11)

� �



t
�
� t [′] =1



� L g (t [′] ) L f (t [′] )


t [′] =1



�



2 [t] TD T u [(][t][+1)], T v [(][t][+1)] . (11)
� �



For the global output, we have


∥h(G) − h(H)∥≤ L c



T
� L g (t) L f (t)
� t=1



T
�
� t=1



�



2 [T] TMD [T][ +1] (G, H) . (12)



Proof. Without loss of generality, suppose that L f (t), L g (t) ≥ 1. We show Equation (11) by induction. For t = 0 Equation (11) holds trivially.


Step 1: Bound the difference between message function outputs.
���g (t) �{{x s [(][t][−][1)] }} s∈N (u) � − g [(][t][)] [ �] {{x s [(][t] [′] [−][1)] }} s ′ ∈N (u) ����

≤ L g (t) WD ∥·∥ �{{x s [(][t][−][1)] }} s∈N (v), {{x s [(][t] [′] [−][1)] }} s ′ ∈N (u) �



���x s(t−1) − x τ [(][t] ( [−] s) [1)] ���



= L g (t) min τ ∈S n



�


u



≤ L g (t) �


s



���x s(t−1) − x τ [(][t] [∗] [−] (s [1)] ) ���



(13)



2 [t][−][1] [ �] TD �T s [(][t][)] [, T] [ (] τ [t] [∗] [)] (s) �


s


2 [t][−][1] WD TD {{T s [(][t][)] [}}] [s][∈N] [(][v][)] [,][ {{][T] [ (] s [′] [t] [ }}] [)] [s] [′] [∈N] [(][u][)],
� �


22



= L g (t)


= L g (t)



t−1
� L g (t [′] ) L f (t [′] )
� t [′] =1



t−1
� L g (t [′] ) L f (t [′] )
� t [′] =1



�

�


where τ [∗] is the optimal permutation in the definition of WD TD �{{T s [(][t][)] [}}] s∈N (v) [,][ {{][T] [ (] s [′] [t] [ }}] [)] [s] [′] [∈N] [(][u][)] �.


Step 2: Bound the difference between update function outputs.

x (ut) [−] [x] [(] v [t][)]
��� ���

= ���f (t) �x s [(][t][−][1)], g [(][t][)] [ �] {{x s [(][t][−][1)] }} s∈N (u) �� − f [(][t][)] [ �] x v [(][t][−][1)], g [(][t][)] [ �] {{x s [(][t] [′] [−][1)] }} s ′ ∈N (v) �����

≤ L f (t) ����x u(t−1) − x v [(][t][−][1)] ��� + ���g (t) �{{x s [(][t][−][1)] }} s∈N (u) � − g [(][t][)] [ �] {{x s [(][t] [′] [−][1)] }} s ′ ∈N (v) �����



�



2 [t][−][1] WD TD �{{T s [(][t][)] [}}] s∈N (v) [,][ {{][T] [ (] s [′] [t] [ }}] [)] [s] [′] [∈N] [(][u][)] � [�]



x u(t−1) − x v [(][t][−][1)] ��� + L g (t)
����



t−1
� L g (t [′] ) L f (t [′] )
� t [′] =1



≤ L f (t)


≤ L f (t)


+ L g (t)



t−1
� L g (t [′] ) L f (t [′] )
�� t [′] =1



�



2 [t][−][1] TD T u [(][t][)] [, T] [ (] v [t][)]
� �



t−1
� L g (t [′] ) L f (t [′] )
� t [′] =1



�



2 [t][−][1] WD TD {{T s [(][t][)] [}}] [s][∈N] [(][v][)] [,][ {{][T] [ (] s [′] [t] [ }}] [)] [s] [′] [∈N] [(][u][)]
� � [�]



�



≤



t
� L g (t [′] ) L f (t [′] )
� t [′] =1



2 [t] TD T v [(][t][+1)], T u [(][t][+1)] .
� �



(14)


This finishes the proof of the first claim.


Step 3: Bound the different between global outputs. The second claim follows by calculating,

∥h(G) − h(H)∥ = ���c �{{x [(] u [T][ )] [}}] [u][∈][V][ (][G][)] � − c �{{x [(] v [T][ )] }} v∈V (G) ����

≤ L c WD ∥·∥ ({{x [(] u [T][ )] [}}] [u][∈][V][ (][G][)] [,][ {{][x] [(] v [T][ )] }} v∈V (G) )



= L c min
τ



� ∥x [(] s [T][ )] − x [(] τ [T] (s [ )] ) [∥]


s



(15)



≤ L c


= L c



T
� L g (t [′] ) L f (t [′] )
� t [′] =1



T
� L g (t [′] ) L f (t [′] )
� t [′] =1



�

�



2 [T] [ �] TD �T s [(][T][ +1)], T τ [(][T] [∗] ( [ +1)] s) �


s


2 [T] TMD [T][ +1] (G, H),



where τ [∗] is the optimal permutation in the definition of TMD [T][ +1] (G, H).


We now consider the case where Lipschitz continuous functions on multisets are implemented via
sum aggregation, followed by Lipschitz continuous functions on the Euclidean domain. This includes scenarios where the message, update, and readout functions are MLPs with Lipschitz continuous activation functions, such as ReLU.

Corollary C.7. Consider a MPNN of the form



� g [(][t][+1)] [ �] x [(] u [t][)] �

u∈N (v) 



,



x [(] v [t][+1)] = f [(][t][+1)]







x [(] v [t][)] [,] �
 u∈N (



with message and update functions �g [(][t][)], f [(][t][)] [�] [T] t=1 [. Consider also a global readout function][ e][ of the]
form



 .



h(G) = e







 v∈ [�] V (



x [(] v [T][ )]
v∈ [�] V (G)



Suppose that for all t = 1, . . ., T, the message and update functions are Lipschitz continuous with
Lipschitz constants bounded by L g (t) and L f (t), respectively. Suppose that the readout function is


23


Lipschitz continuous with Lipschitz constants bounded by L c . Then, for all layers t = 0, 1, . . ., T
and for all pairs of graphs G, H ∈G and all pairs of nodes u ∈ V (G) and v ∈ V (H), we have



�



x (ut) [−] [x] [(] v [t][)] ≤
��� ���


For the global output, we have



t
� L g (t [′] ) L f (t [′] )
� t [′] =1



2 [t] TD T u [(][t][+1)], T v [(][t][+1)] . (16)
� �



�



∥h(G) − h(G)∥≤ L c



T
� L g (t) L f (t)
� t=1



2 [T] TMD [T][ +1] (G, H) .



Proof. This follows directly from Lemma C.6, since for any Lipschitz continuous function f with
Lipschitz constant L f, the induced multiset function f [˜] : X �→ [�] x∈X [f] [(][x][)][ remains Lipschitz]
continuous with a Lipschitz constant bounded by L f .


Theorem C.8. Let ζ be a strongly simulatable CRA, and let h : G → R [K] be a ζ-MPNN with T
layers, where the message and update functions are Lipschitz continuous with Lipschitz constants
bounded by L g (t) and L f (t), respectively. Suppose h includes a global sum pooling layer followed
by a Lipschitz continuous classifier c with Lipschitz constant L c . Then, for any graphs G and H,


∥h(G) − h(H)∥≤ L · ζ-TMD [T][ +1] (G, H),

where L = L c 2 [T] [ �] [T] t=1 [L] f [ (][t][)] [L] g [(][t][)] [.]


Proof. Let h [′] be the underlying MPNN of h. The proof of theorem follows from Corollary C.7 by


∥h(G) − h(G)∥ = ��h ′ �R [ζ] (G)� − h [′] [ �] R [ζ] (H)���



�

�



≤ L c


= L c



T
� L g (t) L f (t)
� t=1


T
� L g (t) L f (t)
� t=1



2 [T] TMD [T][ +1] [ �] R [ζ] (G), R [ζ] (H)�


2 [T] ζ-TMD [T][ +1] (G, H) .



C.3 Example II: k-GNNs


The k-Weisfeiler-Leman (k-WL) test enhances the expressive power of the 1-WL test by considering
interactions between k-tuples of nodes. To strongly simulate k-WL, a product graph G [⊗][k] is constructed, where each node represents a k-tuple of nodes from the original graph G, and edges are
defined based on the adjacency relationships in G.


Similarly, k-MPNNs operate directly on the product graph G [⊗][k], achieving the same level of expressivity as the k-WL.

Corollary C.9. Let h be an k-MPNN with T layers. Then, there exists a constant L such that for
any graphs G and H,
∥h(G) − h(H)∥≤ L · k-TMD [T][ +1] (G, H). (17)


D Graph Classification Setting


We consider a classification problem with K classes over a fixed set of training graphs G tr and test
graphs G te . Each graph G is equipped with node features x, and we assume there exists a constant
D > 0 such that ∥x i ∥≤ D for every node i ∈ V (G) and every G ∈G tr ∪G te . Let N tr = |G tr |
and N te = |G te |. Each graph G has a label y sampled from an unknown distribution p. Moreover,
we assume that graphs closer in a given pseudometric pm are more likely to share the same label.
Concretely, for each class k ∈{1, . . ., K}, there is a Lipschitz continuous function η k (with respect
to some pseudometric pm) such that

Pr�y = k �� G� = η k (G),


24


and we denote by C := max k Lip(η k ) the maximum Lipschitz constant among all {η k }. Let ξ be
an upper bound on the distance (with respect to pm) between any training graph in G tr and any test
graph in G te .


We now introduce a PAC-Bayes framework to derive a generalization bound for classifiers under
this setting. We consider two different setups for learning on graphs:


1. ζ-MPNNs: Let ζ be a strongly simulatable color-refinement algorithm (see Definition B.1).
A ζ-MPNN has a fixed depth T and a final MLP e as the classifier. Each layer t ∈
{1, . . ., T } has message and update functions denoted by g [(][t][)] and f [(][t][)], each with fixed
depths d(g [(][t][)] ) and d(f [(][t][)] ), respectively. The corresponding weight matrices are written

as {w(g [(][t][)], s)} [d] s=1 [(][g] [(][t][)] [)] and {w(f [(][t][)], s)} [d] s=1 [(][f] [ (][t][)] [)] . The final MLP classifier e has parameters
{w(e, s)} [d] s=1 [(][e][)] [. Define][ b][ to be the maximum hidden dimension across these modules, and]
let H ζ be the class of all such ζ-MPNN classifiers.

2. MLPs on non-learnable graph embeddings: Here, the final MLP classifier c has the same
notations for its parameters as above, and we denote the hypothesis set by H latent .


We assume that every non-linearities in the MLPs are Lipschitz continuous and homogeneous.


Finally, we adapt the following assumption from Ma et al. (2021).

Assumption D.1 (Assumption on Concentrated Expected Loss Difference.). Let P be a distribution
over H obtained by sampling the (vectorized) trainable weight matrices from N (0, σ [2] I), with



σ [2] ≤



2
�γ/(8ξ)� /D
2 b�λ N tr [−][α] + ln(2 b D)� .



For any classifier h ∈H with model parameters {w j } j, define T h := max j ��w j �� 2 [.][ Assume there]
exists an 0 < α < [1]

4 [such that]

Pr h∼P �L [γ/] te [4] [(][h][)][ −L] [γ/] tr [2] [(][h][)][ > N] [ −] tr [α] + c K ξ �� T Dh [ξ >] γ8 � ≤ e [−][N] [ 2] tr [α] .


This assumption posits that when the model parameters h sampled from P do not exceed a certain
norm threshold (i.e., T h [D] [ξ][ ≤] [γ] 8 [) and the number of training samples][ N] [tr] [ is sufficiently large, then the]

expected margin loss on the test set will not exceed that on the training set by more than N tr [−][α] [+][cKξ][.]
Informally, once the training set grows large enough (and model weights are not too large), the test
performance cannot deviate significantly from the training performance. This property becomes
trivially true if all samples in G tr and G te are i.i.d. since L [γ/] te [2] −L [γ/] tr [2] ≤ 0 in that case.


E Proofs of the Results Section 4


In this section, we provide detailed proofs of the theoretical results presented in the Section 4.


We note that the proof of Theorem 4.1 follows the proof of Theorem 3 in (Ma et al., 2021), carefully
adapted for graph classification tasks and learnable graph encoders.


Specifically, the proof leverages the PAC-Bayes framework, properties of the chosen pseudometric,
and structural constraints on the hypothesis space. For clarity, we decompose it into a series of steps,
each contributing to the final result.


In Appendix E.1, we present intermediate results that are independent of the choice of pseudometric
and hypothesis space. To emphasize this generality, we denote the pseudometric by pm and the
hypothesis space by H. This ensures that the results in Appendix E.1 apply regardless of whether
the pseudometric is defined in the graph space or latent space, and whether the classifier is an endto-end learnable GNN or a deterministic graph encoder followed by a learnable MLP classifier. This
approach allows us to establish in Appendix E.2 the generalization bound for end-to-end learnable
GNNs, and in the following subsection, the bound for graph classifiers with fixed encoders–both
derived from the results in Appendix E.1.


We note that if pm is defined on G, the corresponding classifier h : G →{1, . . ., K} is assumed to
be Lipschitz with respect to pm. If instead pm is defined on R [b], the classifier h : R [b] →{1, . . ., K},


25


typically an MLP, is assumed to be Lipschitz with respect to pm. In the latter case, classification is
performed via h ◦ e(G), where e : G → R [b] is a deterministic graph embedding network.


E.1 Preliminaries for the Proofs in Section 4


Step 1: Deterministic Bound via PAC-Bayes We begin by establishing a deterministic bound
on the test loss in terms of the training loss and the Kullback-Leibler (KL) divergence between the
posterior and prior distributions over the hypothesis space H.

Lemma E.1. Let h [˜] ∈H be any classifier and let P be a prior distribution on H independent of the
training data. For any λ > 0 and γ ≥ 0, with probability at least 1 − δ over the training sample y tr,
for any posterior distribution Q on H satisfying


̸


̸


̸


̸


̸

̸



≥ [1]
� 2 [,]


̸


̸


̸


̸


̸

̸



P h∼Q


the following bound holds:


̸


̸


̸


̸


̸

̸



max
� G∈G tr ∪G te [∥][h][(][G][)][ −] [h][˜][(][G][)][∥] [∞] [< γ] 8


̸


̸


̸


̸


̸

̸



2 (D KL (Q∥P ) + 1) + ln [1]
� δ


̸


̸


̸


̸


̸

̸



λ [2]

4N tr + D te [γ/], [2] tr [(][P] [;][ λ][)] �, (18)


̸


̸


̸


̸


̸

̸



L [0] te [(˜][h][)][ ≤L] [γ] tr [(˜][h][) + 1]

λ


̸


̸


̸


̸


̸

̸



L [0] te [(˜][h][)][ ≤L] [γ] tr [(˜][h][) + 1]


̸


̸


̸


̸


̸

̸




[1] λ [2]

δ [+] 4N


̸


̸


̸


̸


̸

̸



where D te [γ/], [2] tr [(][P] [;][ λ][) = ln][ E] [h][∼][P] [exp] �λ �L [γ/] te [2] [(][h][)][ −L] [γ] tr [(][h][)] ��.


Proof of Lemma E.1. The proof adapts Theorem 2 from Ma et al. (2021) from the node to the graph
classification setting. We present the proof for completeness.


First, define a subset H h˜ ⊂H as:


̸


̸


̸


̸


̸

̸



H h˜ = h ∈H | max
� G∈G tr ∪G te [∥][h][(][G][)][ −] [h][˜][(][G][)][∥] [∞] [≤] [γ] 8


Using this subset H h˜, define the modified distribution Q [′] over H h˜ as:


̸


̸


̸


̸


̸

̸



. (19)
�


̸


̸


̸


̸


̸

̸



Q [′] (h) =


̸


̸


̸


̸


̸

̸



1
P h∼Q ( h∈H h˜ ) [Q][(][h][)][,][ if][ h][ ∈H] [h][˜] [,] (20)
�0, otherwise


̸


̸


̸


̸


̸

̸



We aim to show L [0] te [(˜][h][)][ ≤L] [γ/] te [4] [(][h][)] and Lˆ [γ/] tr [2] [(][h][)][ ≤] [L][ˆ] [γ] tr [(˜][h][)][.] (21)


The first inequality holds since

L [0] te [(˜][h][)][ −L] [γ/] te [4] [(][h][)]


� �
= E y i ∼Pr(y|G i ),G i ∈G te �L [γ] te [(˜][h][)] � − E y i ∼Pr(y|g i ),G i ∈G te �L [γ/] t [4] (h)�


̸


̸


̸


̸


̸

̸



1

= E y i ∼Pr(y|G i ),G i ∈G te

N te ̸
�


1

− E y i ∼Pr(y|G i ),G i ∈G te

N te ̸
�


1

= E y i ∼Pr(y|G i ),G i ∈G te

N te ̸
�


̸


̸

̸



�

̸

G i ∈G te


�

̸

G i ∈G te


�

̸

G i ∈G te


̸


̸

̸



1 ˜h(G i )[y i ] ≤ 0 + max h(G i )[k]
� � k≠ y Gi �� [�]


1 h(G i )[y i ] ≤ γ/4 + max h(G i )[k]
� � k≠ y Gi �� [�]


1 ˜h(G i )[y i ] ≤ 0 + max h˜(G i )[k]
� � k≠ y Gi ��


̸


̸

̸



̸


̸


̸


− 1 h(G i )[y i ] ≤ γ/4 + max h(G i )[k]
� � k≠ y Gi �� [�]


̸

̸



̸


̸


̸


̸,


̸

̸



̸


̸


̸


̸


i.e., it remains to show that if h [˜] (G i )[y i ] ≤ �0 + max k≠ y Gi h(G i )[k]� holds, then also h(G i )[y i ] ≤
�γ/4 + max k≠ y Gi h(G i )[k]�. This is clear by Equation (19),


h(G i )[y i ] ≤ γ/8 + h [˜] (G i )[y i ]


26


≤ γ/8 + max h˜(G i )[k]
k≠ y Gi


≤ γ/4 + max h(G i )[k].
k≠ y Gi


Similarly, one can prove the second inequality in Equation (21).


Therefore, with probability at least 1 − δ over the samples y tr, we get


L [te] 0 [≤] [E] [h][∼][Q] [′] [L] [γ/] te [4] [(][h][)]


̸



̸


̸


λ [2]

4N tr + D te [γ/], [2] tr [(][P] [;][ λ][)] �


̸



̸


̸


≤ E h∼Q ′ L [ˆ] [γ/] tr [2] [(][h][) + 1]

λ


̸



̸


̸


D KL (Q [′] ||P ) + ln [1]
� δ


̸



̸


̸


[1] λ [2]

δ [+] 4N


̸



̸


̸


λ [2]

4N tr + D te [γ/], [2] tr [(][P] [;][ λ][)] � .


̸



̸


̸


≤ L [ˆ] [γ] tr [(˜][h][) + 1]

λ


̸



̸


̸


D KL (Q [′] ||P ) + ln [1]
� δ


̸



̸


̸


[1] λ [2]

δ [+] 4N


̸



̸


̸


The second inequality applies Theorem 1 from Ma et al. (2021), while the first and last inequalities

˜
follow directly from (21) and the definitions of H h and Q [′] . The remaining steps align with the proof
of Theorem 2 from Ma et al. (2021).


tion (18) in Lemma E.1, which captures the difference in expected losses between the test andStep 2: Bounding the Discrepancy Term Next, we bound the term D te [γ/], [2] tr [(][P] [;][ λ][)][ from Equa-]
training distributions under the prior P . We begin by bounding L [γ/] te [2] [(][h][)][ −L] [γ] tr [(][h][)][ in this step.]


Lemma E.2. Let h ∈H be any classifier with Lipschitz constant L with respect to the pseudometric
pm. For any γ ≥ 0, if Lξ ≤ [γ] 4 [, then]


L [γ/] te [2] [(][h][)][ −L] [γ] tr [(][h][)][ ≤] [CKξ,]


where K is the number of classes and C is the maximum Lipschitz constant of the functions η k .


Proof of Lemma E.2. We set


L [γ] (G, y) := 1 h(G)[y] ≤ γ + max,
� k≠ y [h][(][G][)[][k][]] �


where h(G)[k] denotes the output score for class k.


27


Then, we can write

L [γ/] te [2] [(][h][)][ −L] [γ] tr [(][h][)]







= E te
y


1

=
N te


1

=
N te







 G [�] j ∈G



1

N tr



�� G i ∈G tr



1
L [γ] (G i, y i )
N tr

�



G j ∈G te



1
L [γ/][2] (G j, y j )
N te



− E tr
 y



�

G i ∈G tr



�

G j ∈G te



K

1

� η k (G j )L [γ/][2] (G j, k) − N tr

k=1



K
� η k (G i )L [γ] (G i, k)


k=1



1

N te



�

G i ∈G tr


�



�

G j ∈G te



�

G j ∈G te



�

G i ∈G tr



�



K

1

� η k (G j )L [γ/][2] (G j, k) − N tr

k=1



K
�



K
� η k (G i )L [γ] (G i, k)


k=1



1

=
N te N tr


1

=
N te N tr



G i ∈G tr


�

G i ∈G tr



K
�


k=1


K
�


k=1



G j ∈G te


�

G j ∈G te



η k (G j )L [γ/][2] (G j, k) − η k (G i )L [γ] (G i, k)
� �


η k (G j )L [γ/][2] (G j, k) − η k (G j )L [γ] (G i, k)
� �



+ (η k (G j )L [γ] (G i, k) − η k (G i )L [γ] (G i, k))



1

=
N te N tr


1
≤
N te N tr



�

G i ∈G tr


�

G i ∈G tr



K
�


k=1



�

G j ∈G te


�

G j ∈G te



K
� η k (G j ) �L [γ/][2] (G j, k) −L [γ] (G i, k)� + L [γ] (G i, k) (η k (G j ) − η k (G i ))

k=1



L [γ/][2] (G j, k) −L [γ] (G i, k) + (η k (G j ) − η k (G i )) .
� �



(22)
The last inequality holds since L [γ] and η k are bounded by 1. We have, by assumption on the probability distribution,
η k (G j ) − η k (G i ) ≤ C · pm (G j, G i ) ≤ Cξ. (23)


Furthermore, by assumption,

∥h(G i ) − h(G j )∥ ∞ ≤ L · pm (G j, G i ) ≤ Lξ ≤ [γ] (24)

4 [.]

Then, for any k = 1, . . ., K,

L [γ/][2] (h(G j ), k) ≤ L [γ] (h(G i ), k) . (25)

This is true since both L [γ/][2] (h(G j ), k) and L [γ] (h(G i ), k) are 0-1-valued. If L [γ/][2] (h(G j ), k) = 1,
we have by Equation (24),
h(G i )[k] ≤ γ/4 + h(G i )[k]
≤ γ/4 + γ/2 + max
l=1,...,K [h][(][G] [j] [)[][l][]]


≤ γ/4 + γ/2 + γ/4 + max
l=1,...,K [h][(][G] [i] [)[][l][]]


= γ + max
l=1,...,K [h][(][G] [i] [)[][l][]][,]


i.e., L [γ] (h(G i ), k) = 1 as well.


Finally, we continue with the calculation in Equation (22),



1
L [γ/] te [2] [(][h][)][ −L] [γ] tr [(][h][)][ ≤]
N te N tr



�

G j ∈G te



�

G i ∈G tr



K
�


k=1



L [γ/][2] (G j, k) −L [γ] (G i, k) + (η k (G j ) − η k (G i ))
� �



�

G j ∈G te



1
≤
N tr G � i ∈G tr



1

N te



K
� (0 + Cξ)


k=1



=
CKξ,
(26)


28


where the second inequality holds by Equation (23) and Equation (25).


Step 3: Bounding the Discrepancy Term D tr [γ/],te [2] [(][P] [;][ λ][)][.]


Lemma E.3. Let α > 0. For any 0 < λ ≤ N [2][α] and γ ≥ 0, assume the “prior” P on H is defined by
(γ/8m) [2][/D]
sampling the vectorized trainable weight matrices from N (0, σ [2] I) for some σ [2] ≤ 2b(λN tr [−][α] +ln 2bD) [.]

We have

D tr [γ/],te [2] [(][P] [;][ λ][)][ ≤] [ln 3 +][ λCKξ,] (27)


where D te [γ/], [2] tr [(][P] [;][ λ][) = ln][ E] [h][∼][P] [ e] λ�L te [γ/][2] (h)−L [γ] tr [(][h][)] � .


Proof. First, set T h := max j=1,...,D ∥w j ∥ 2 . We prove this lemma by partitioning H into two events:
one with high probability, where the spectral norms of the model parameters satisfy the conditions
in Lemma E.2, and its complement. For the latter event, we use Assumption D.1.


For any j = 1, . . ., D, we have, by (Tropp, 2015), for any t > 0,


t [2]
Pr (∥w j ∥ 2 ≥ t) ≤ 2be [−] 2bσ [2],


1/D
where b is the maximum width of all hidden layers of the considered classifier. We set t = � 8γξ � .
Applying a union bound leads to



� 1/D [�]



�



γ
T h � 8ξ



≤ 2bDe [−] [(][γ/] 2 [8] bσ [ε][)2][2][/D] ≤ e [−][λN] [ −] tr, [α] (28)



Pr T h [D] [ξ > γ]
� 8



= Pr
�



(γ/8ξ) [2][/D]
where the last inequality uses the condition σ [2] ≤ 2b ( λN tr [−][α] +ln 2bD ) [.]



For any h satisfying T h [D] [ξ][ ≤] [γ] 8 [, by Lemma E.2, we have][ e] λ�L [γ/] te [4] (h)−L [γ/] tr [2] (h)� ≤ e [λCKξ] .


The complement event, i.e., T h [D] [ξ >] γ8 [occurs with probability at most][ e] [−][λN] [ −] tr . We decompose [α]
D tr [γ/],te [2] [(][P] [;][ λ][)][ as follows,]


D tr [γ/],te [2] [(][P] [;][ λ][) = ln][ E] [h][∼][P] [e] λ�L [γ/] te [4] (h)−L [γ/] tr [2] (h)�



≤ ln Pr T h [D] [ξ][ ≤] [γ]
� � 8



e [λCKξ] + Pr T h [D] [ξ > γ]
� � 8



� E h∼P | T h D [ξ>] [ γ] 8 [e] [λ] �L [γ/] te [4] (h)−L [γ/] tr [2] (h)� �



≤ ln e [λCKξ] + e [−][λN] [ −] tr E [α] h∼P | T h D [ξ>] [ γ] 8 [e] λ�L [γ/] te [4] (h)−L [γ/] tr [2] (h)�
� �

≤ ln e [λCKξ] + e [−][λN] [ −] tr [α] e [−][N] [ 2] tr [α] - e [λ] + 1 − e [−][N] [ 2] tr [α] - e [λN] [ −] tr [α] +λCKξ [��]
� � � �

= ln e [λCKξ] + e [λ][−][N] [ 2] tr [α] + e [−][λN] [ −] tr [α] 1 − e [−][N] [ 2][α] [�] - e [λN] [ −] tr [α] +λCKξ [��]
� ��

= ln e [λCKξ] + e [λ][−][N] [ 2] tr [α] + 1 − e [−][N] [ 2] tr [α] - e [λCKξ] [��]
� �� �

≤ ln �2e [λCKξ] + 1�



≤ ln 3 + λCKξ.
(29)
The first inequality holds by decomposing the domain over the expectation/integral into the event
in which T h [D] [ξ][ ≤] [γ] 8 [holds and its complement. The second inequality holds by][ Pr] �T h [D] [ξ][ ≤] [γ] 8 � ≤ 1



in which T h [D] [ξ][ ≤] [γ] 8 [holds and its complement. The second inequality holds by][ Pr] �T h [D] [ξ][ ≤] [γ] 8 � ≤ 1

and Equation (28). The third inequality holds by Assumption D.1. The second-to-last inequality
holds by the assumption 0 < λ ≤ N [2][α] . The remaining equations and inequalities are algebraic
reformulations.




[γ] 8 [holds and its complement. The second inequality holds by][ Pr] �T h [D] [ξ][ ≤] [γ] 8



29


E.2 Proof of Theorem 4.1


We first present auxiliary results for the proof of Theorem 4.1, focusing on MPNNs, which may be
end-to-end learnable. At the end of this chapter, we provide the full proof of Theorem 4.1, building
on the results from this and the previous section. For simplicity, we derive the results for MPNNs;
the corresponding results for ζ-MPNNs applied to a graph G follow by applying the derived results
for standard MPNNs to the strong simulation ζ. Let us denote the hypothesis space of MPNNs by
H mpnn, where the parameters follow the assumptions in Theorem 4.1.


Step 4: MPNNs are stable under weight pertubations. We proceed by proving the following
result that shows that MPNNs are stable under small pertubations of their weights.

Lemma E.4. Let h [˜] be any classifier in H mpnn with learnable weight matrices w =
{w(f [(][t][)], s)} [d] s=1 [(][f] [ (][t][)] [)], {w(g [(][t][)], s)} [d] s=1 [(][g] [(][t][)] [)], {w(c, s)} [d] s=1 [(][c][)] and β > [˜] 0. Let G B,d be the set of graphs
� �
with maximum degree d and input node features in a ball of radius B. Then,


max
G∈G B,d [|][h][˜] [w][+][u] [(][G][)][ −] [h][˜] [w] [(][G][)][|]



B



 


�



1 + d� [d][(][g] � [(][k][+1)] [)]













d(f [(][k][+1)] )
� ∥w(f [(][k][+1)], s)∥


s



d(f [(][k][+1)] )
�




[)]

∥w(g [(][k][+1)], s)∥
� [��]

s









T −1
�
� k=0



≤ e









d(c)
�



� ∥w(c, s)∥ 2


s=1



�� s



�



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥




 


T −1
�


t=0



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s



(30)


Proof. We denote by x [(] v [t][)] the representation of node v after t layers of the MPNN h [˜] w with standard
weights w and ˜x [(] v [t][)] is the representation of node v after t + 1 layers of the MPNN h [˜] w+u with
perturbed weights w + u. We similarly define the message terms m [(] v [t][)] and ˜m [(] v [t][)] [. We further define]



δ t+1 := max
v



x˜ (vt+1) − x [(] v [t][+1)] .
��� ���



We calculate



δ t+1 = max
v


= max

v



x˜ (vt+1) − x [(] v [t][+1)]
��� ���

f (wt++1)u [(˜][x] v [(][t][)] [,][ ˜][m] [(] v [t][+1)] ) − f w [(][t][+1)] (x [(] v [t][)] [, m] [(] v [t][+1)] )
��� ���



≤ f (wt++1)u [(˜][x] [(] v [t] [∗] [)] [,][ ˜][m] [(] v [t] [∗] [+1)] ) − f w [(][t] + [+1)] u [(][x] [(] v [t] [∗] [)] [, m] [(] v [t] [∗] [+1)] )
��� ���

+ f (wt++1)u [(][x] [(] v [t] [∗] [)] [, m] [(] v [t] [∗] [+1)] ) − f w [(][t][+1)] (x [(] v [t] [∗] [)] [, m] [(] v [t] [∗] [+1)] )
��� ���

= (A) + (B),


where v [∗] is the node where the maximum is taken.


Bound (A). We begin by bounding the first term (A). It holds


(A) ≤ L(f w [(][t] + [+1)] u [)] ∥x˜ [(] v [t][)] [−] [x] [(] v [t][)] [∥] [+][ ∥][m][˜] [(] v [t][)] [−] [m] [(] v [t][)] [∥]
� �



(31)



������



� g w [(][t] + [+1)] u [(˜][x] [(] u˜ [t][)] [)][ −] [g] w [(][t][+1)] (x [(] u˜ [t][)] [)]

u˜∈N (v)



�









≤ L(f w [(][t] + [+1)] u [)]



δ t +







������



(t+1)

≤ L(f w [(][t] + [+1)] u [)] δ t + d max g w+u [(˜][x] [(] u [t] [∗] [)] [)][ −] [g] w [(][t][+1)] (x [(] u [t] [∗] [)] [)]
� u [∗] ∈N (v) ��� ����


(t+1)

≤ L(f w [(][t] + [+1)] u [)] δ t + d max g w+u [(˜][x] [(] u [t] [∗] [)] [)][ −] [g] w [(][t][+1)] (x [(] u [t] [∗] [)] [)]
� u [∗] ∈N (v) ��� ����


30


We calculate,


∥g w [(][t] + [+1)] u [(˜][x] [(] u [t] [∗] [)] [)][ −] [g] w [(][t][+1)] (x [(] u [t] [∗] [)] [)][∥]

≤∥g w [(][t] + [+1)] u [(˜][x] u [(][t] [∗] [)] [)][ −] [g] w [(][t] + [+1)] u [(][x] u [(][t] [∗] [)] [)][∥] [+][ ∥][g] w [(][t] + [+1)] u [(][x] u [(][t] [∗] [)] [)][ −] [g] w [(][t][+1)] (x [(] u [t] [∗] [)] [)][∥]



d(g [(][t][+1)] ) [�]
� ∥w(g [(][t][+1)], s)∥
� s



≤ 1 + [1]
� D



≤ 1 + [1]
� D



�



u [∗] max ∈N (v) [∥][x] u [(][t] [∗] [)] [∥] � s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥



(32)



+ L(g w [(][t] + [+1)] u [)] max u [∗] [−] [x] u [(][t] [∗] [)] [∥]
u [∗] ∈N (v) [∥][x][˜] [(][t][)]



Hence,



(A) ≤ L(f w [(][t] + [+1)] u [)]

�



�



δ t + d �1 + D [1]



δ t + d �1 + D [1]



d(g [(][t][+1)] ) [�]
� ∥w(g [(][t][+1)], s)∥
� s �



∥x [(][t][)] ∥ �


s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥


(33)



+ L(g w [(][t] + [+1)] u [)][δ] [t]

�



Bound (B). We continue by bounding the first term (B). It holds



d(f [(][t][+1)] ) [�]

(B) ≤ �1 + D [1] � � s ∥w(f [(][t][+1)], s)∥



∥x [(] v [t] [∗] [)] [∥] [+][ ∥][m] [(] v [t] [∗] [+1)] ∥
��
�� s



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥ [.]



�



Together, we have



∥x [(][t][)] ∥ �

� s



(34)


∥u(g [(][t][+1)], s)∥
w+u [)][δ] [t]
∥w(g [(][t][+1)], s)∥ [+][ L][(][g] [(][t][+1)]



δ t+1 ≤ L(f w [(][t] + [+1)] u [)] �δ t + d �1 + D [1]



d(g [(][t][+1)] ) [�]
� ∥w(g [(][t][+1)], s)∥
� s



∥x [(] v [t] [∗] [)] [∥] [+][ ∥][m] [(] v [t] [∗] [+1)] ∥
��
�� s



+ 1 + [1]
� D



d(f [(][t][+1)] ) [�]
� ∥w(f [(][t][+1)], s)∥
� s



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



= L(f w [(][t] + [+1)] u [)]

�


+ L(f w [(][t] + [+1)] u [)]

�



�

�



(1 + L(g w [(][t] + [+1)] u [))]

�



�



δ t



�



�



d 1 + [1]
� D



d 1 + [1]
� D



d(g [(][t][+1)] ) [�]
� ∥w(g [(][t][+1)], s)∥
� s



∥x [(][t][)] ∥ �


s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥



∥x [(] v [t] [∗] [)] [∥] [+][ ∥][m] [(] v [t] [∗] [+1)] ∥
��
�� s



+ 1 + [1]
� D



d(f [(][t][+1)] ) [�]
� ∥w(f [(][t][+1)], s)∥
� s



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥ [.]



(35)



We solve this recurrence relation to get


δ T ≤


where



T −1
�
� k=t



T −1
�


t=0



� A k

k=t+1



�



B t,



A t = L(f w [(][t] + [+1)] u [)] �1 + L�g w [(][t] + [+1)] u � [�], (36)


31












B t = L(f w [(][t] + [+1)] u [)]

�



d(g [(][t][+1)] )

[1] 

D
�



d 1 + D [1]
�







d(g [(][t][+1)] )
� ∥w�g [(][t][+1)], s�∥


s



d(g [(][t][+1)] )
�



(37)



�



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥







t
� L(f w [(][k][)] [)] �1 + dL(g w [(][k][)] [)] � [�]
� k=1



t
�
� k=1



B �


s



d(f [(][t][+1)] )

[1] 

D
�









+ 1 + D [1]
�







d(f [(][t][+1)] )
�



∥w�f [(][t][+1)], s�∥

s




- (1 + dL(g w [(][t][+1)] ))
�



t
� L(f w [(][k][)] [)] �1 + dL(g w [(][k][)] [)] � [�]
� k=1



∥u(f [(][t][+1)], s)∥

B
�� s ∥w(f [(][t][+1)], s)∥ [,]



where


and the product



T −1
�





, (38)







L(f w [(][t] + [+1)] u [) =]


L(g w [(][t] + [+1)] u [) =]



















d(f [(][t][+1)] )
� ∥w(f [(][t][)], s) + u(f [(][t][)], s)∥


s=1



d(f [(][t][+1)] )
�



d(g [(][t][+1)] )
�



� ∥w(g [(][t][)], s) + u(g [(][t][)], s)∥


s=1





, (39)







T −1
� A k is taken to be 1 when t = T (empty product).

k=t+1



Final Step As a final step we need to incorporate the MLP classifier after the T message passing
layers. For this we calculate,



1

− f w

N
�



N
� x [(] v [T][ )]


v=1



N
�



������



δ T +1 =


≤


+



1

f w+u N
����� �


1

f w+u N
����� �


1

f w+u N
����� �



N
� x˜ [(] v [T][ )]


v=1



N
�



N
� x [(] v [T][ )]


i=1



N
�



N
� x˜ [(] v [T][ )]


v=1



N
�



�

�

�



1

− f w+u N

�



N
� x [(] v [T][ )]


v=1



N
�



������



1

− f w

N
�



N
� x [(] v [T][ )]


v=1



N
�



������



d(f )
�


i=1



∥u(f, s)∥ 2
∥w(c, s)∥ 2







δ T + 1 + [1]
� D




D



 x (T )

��� ��� 2








≤ 1 + [1]
� D


≤ 1 + [1]
� D



≤ 1 + [1]
� D



d(f )

�





d(f )
� ∥w(c, s)∥ 2


s=1



d(f )
�



d(f )

�





d(f )
� ∥w(c, s)∥ 2


s=1



d(f )
�



T −1
�
� k=t+1



B t







T −1



�


t=0





t=0



�



≤ 1 + [1]
� D



d(f )

�




d(f )

�





d(f )
� ∥w(c, s)∥ 2


s=1



d(f )
�



� A k

k=t+1



T
� L(f w [(][t][)] [)] �1 + dL(g w [(][t][)] [)] � [�]
� t=1



B













+ 1 + [1]
� D



d(f )

�




d(f )

�





d(f )

�



d(f )
� ∥w(c, s)∥ 2


s=1



d(f )
�



d(f )

∥u(f, s)∥ 2

� i=1 ∥w(c, s)∥ 2



= (C) + (D)
(40)


32


For the term (C), we calculate



T −1
�
� k=t



B t







T −1



�


t=0





t=0



�



1 + [1]
� D



1 + [1]
� D



d(c)

�





d(c)
� ∥w(c, s)∥ 2


s=1



d(c)
�



� A k

k=t+1



d(c)

�





d(c)

�



T −1
�
� k=t



B t







T −1



�


t=0





t=0



�



≤ 1 + [1]
� D



≤ 1 + [1]
� D



d(c)
� ∥w(c, s)∥ 2


s=1



d(c)
�



� L(f w [(][k] + [+1)] u [)] �1 + L�g w [(][k] + [+1)] u � [�],

k=t+1



d(c)

�





d(c)

�



T −1
�
� k=t







T −1



�


t=0





t=0



= 1 + [1]
� D



= 1 + [1]
� D



d(c)
� ∥w(c, s)∥ 2


s=1



d(c)
�



d(f [(][k][+1)] )

�







d(f [(][k][+1)] )
�









∥w(f [(][k][+1)], s)∥

s



k=t+1



1 + [1]
� D



1 + [1]
� D







�



1 + 1 + [1]
� D



D



d(g [(][k][+1)] ) d(g [(][k][+1)] )
� � � s ∥w(g [(][k][+1)], s)∥� [��]




 - B t



(41)
For B t, we calculate













B t = L(f w [(][t] + [+1)] u [)]

�



d(g [(][t][+1)] )

[1] 

D
�



d 1 + D [1]
�







d(g [(][t][+1)] )
� ∥w�g [(][t][+1)], s�∥


s



d(g [(][t][+1)] )
�



t
� L(f w [(][k][)] [)] �1 + dL(g w [(][k][)] [)] � [�]
� k=1



t
�
� k=1



�







D �


s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥



d(f [(][t][+1)] )

[1] 

D
�



+ 1 + D [1]
�







d(f [(][t][+1)] )
�









∥w�f [(][t][+1)], s�∥

s




- (1 + dL(g w [(][t][+1)] ))
�



t
� L(f w [(][k][)] [)] �1 + dL(g w [(][k][)] [)] � [�]
� k=1



∥u(f [(][t][+1)], s)∥

D
�� s ∥w(f [(][t][+1)], s)∥



d(f [(][t][+1)] )

[1] 

D
�



B













t
� L(f w [(][k][)] [)] �1 + dL(g w [(][k][)] [)] � [�]
� k=1



t
�
� k=1



= 1 + D [1]
�







d(f [(][t][+1)] )
� ∥w�f [(][t][+1)], s�∥


s



d(f [(][t][+1)] )
�







d(g [(][t][+1)] )

[1] 

D
�







s

 [�]



s



d 1 + D [1]
�








∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥







d(g [(][t][+1)] )
� ∥w�g [(][t][+1)], s�∥


s



d(g [(][t][+1)] )
�













d(f [(][t][+1)] )
� ∥w�f [(][t][+1)], s�∥


s



d(f [(][t][+1)] )
�

















s

 [�]



s









∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



+



1 + d









d(f [(][t][+1)] )

[1] 

D
�









t
� L(f w [(][k][)] [)] �1 + dL(g w [(][k][)] [)] � [�]
� k=1



t
�
� k=1



≤ 1 + D [1]
�







d(f [(][t][+1)] )
� ∥w�f [(][t][+1)], s�∥


s



d(f [(][t][+1)] )
�



d(g [(][t][+1)] )

[1] 

D
�







 


�� s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s













�



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



d(g [(][t][+1)] )
�




- B







1 + d 1 + D [1]
�




� ∥w�g [(][t][+1)], s�∥


s



d(f [(][t][+1)] )+d(g [(][t][+1)] ) t+1

[1]

D � �
� k=1



�� s



�



≤ 1 + D [1]
�



t+1
� L(f w [(][k][)] [)] �1 + dL(g w [(][k][)] [)] � [�]

k=1



B ·



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] �



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



,



(42)
since L(g w [(][t][+1)] ) = [�] [d] s [(][g] [(][t][+1)] [)] ∥w�g [(][t][+1)], s�∥ and L(f w [(][t][+1)] ) = [�] [d] s [(][f] [ (][t][+1)] [)] ∥w�f [(][t][+1)], s�∥, respectively.


33


Together, we get



T −1
�
� k=t



�



1 + � [d][(][g] � [(][k][+1)] [)] ∥w(g [(][k][+1)], s)∥� [��]


s



1 + � [d][(][g] � [(][k][+1)] [)]



 










T −1



�


t=0





d(f [(][k][+1)] )
�



(C) ≤ 1 + [1]
� D



(C) ≤ 1 + [1]
� D



D

�







d(c)
�



� ∥w(c, s)∥ 2


s=1



t=0



k=t+1









∥w(f [(][k][+1)], s)∥

s



d(f [(][t][+1)] )+d(g [(][t][+1)] ) t+1

[1]

D � �
� k=1



�




- 1 + D [1]
�



t+1
� L(f w [(][k][)] [)] �1 + dL(g w [(][k][)] [)] � [�]

k=1



B ·



�� s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



T −1
�
� k=0



∥w(f [(][k][+1)], s)∥

s



B



 


















d(f [(][k][+1)] )
�



≤ 1 + [1]
� D



≤ 1 + [1]
� D



D

�







d(c)
�



� ∥w(c, s)∥ 2


s=1



�



1 + d� [d][(][g] � [(][k][+1)] [)] ∥w(g [(][k][+1)], s)∥� [��]


s



1 + d� [d][(][g] � [(][k][+1)] [)]



�







T −1
�


t=0



�� s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] �



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥













�



1 + d� [d][(][g] � [(][k][+1)] [)]



B



 










T −1



�
 � k=0



d(f [(][k][+1)] )
� ∥w(f [(][k][+1)], s)∥


s



d(f [(][k][+1)] )
�




[)]
� ∥w(g [(][k][+1)], s)∥� [��]


s



k=0



≤ e



d(c)
�



� ∥w(c, s)∥ 2


s=1









�







T −1
�


t=0



�� s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] �



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



(43)
where D = d(f ) + [�] [T] k=1 �d �f [(][k][)] [�] + d �g [(][k][)] [��] . Hence,

δ T +1 ≤ (C) + (D)



�



B









d(f [(][k][+1)] )
�



1 + d� [d][(][g] � [(][k][+1)] [)] ∥w(g [(][k][+1)], s)∥� [��]


s



 












T −1
�
� k=0



∥w(f [(][k][+1)], s)∥

s



e


 








T −1
�

t=0 �� s



d(c)
�



� ∥w(c, s)∥ 2


s=1



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s



�



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



T
� L(f w [(][t][)] [)] �1 + dL(g w [(][t][)] [)] � [�]

t=1



B







T



�
 � t=1



+ 1 + [1]
� D



d(f )

�





d(f )

�



d(f )
� ∥w(c, s)∥ 2


s=1



d(f )
�



d(f )
�


i=1



∥u(f, s)∥ 2
∥w(c, s)∥ 2









�



1 + d� [d][(][g] � [(][k][+1)] [)]



B



 










T −1



�
 � k=0







d(f [(][k][+1)] )
�




[)]

∥w(g [(][k][+1)], s)∥
� [��]

s



k=0



≤ e



d(c)
�



� ∥w(c, s)∥ 2


s=1









d(f [(][k][+1)] )
� ∥w(f [(][k][+1)], s)∥


s



+



�



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



 .



d(f )
�


i=1



∥u(f, s)∥ 2
∥w(c, s)∥ 2




 






T −1



�


t=0





t=0



�� s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s



(44)


Step 5: Derive sufficient conditions for Lemma E.1 We proceed with the following lemma that
gives sufficient conditions under which the conditions of Lemma E.1 are satisfied. The following
lemma is the first result that is specific to the hypothesis space H mpnn .

Lemma E.5. Let h [˜] be any classifier in H mpnn with learnable weight matrices w =
{w(f [(][t][)], s)} [d] s=1 [(][f] [ (][t][)] [)], {w(g [(][t][)], s)} [d] s=1 [(][g] [(][t][)] [)], {w(c, s)} [d] s=1 [(][c][)] and β > [˜] 0. Consider random perturbations
� �

to w given by u = {u(f [(][t][)], s)} [d] s=1 [(][f] [ (][t][)] [)], {u(g [(][t][)], s)} [d] s=1 [(][g] [(][t][)] [)], {u(c, s)} [d] s=1 [(][c][)], where each perturbation
� �

follows an independent Gaussian distribution N (0, σ [2] I). Suppose the following conditions hold:


    - The variance of the perturbation satisfies



γ
σ ≤ ˜



. (45)
2h ln(4Dh)



e [2] B �β˜ D−(� Tk=1 [d][(][g] [(][k][)] [))][−][1] + d [T][ −][1] [ ˜] β [D][−][1] [��]



34


    - All weights w ∈ w satisfy ∥w∥ 2 = β, with |β [˜] − β| ≤ Dβ˜ [.]


Then, with respect to the random draw of u,


Pr max
� G∈G tr ∪G te [∥][h][˜] [w] [(][G][)][ −] [h][˜] [w][+][u] [(][G][)][∥] [∞] [< γ] 8


Proof. By |β − β [˜] | ≤ D [1] [β][˜][, we get]



≥ [1]
� 2 [.]



1
e [β] [D][−][1] [ ≤] [β][˜] [D][−][1] [ ≤] [eβ] [D][−][1] [.]


We can bound the spectral norm of each perturbation matrix u ∈ u, by Tropp (2015), as follows:



Pr (∥u∥ 2 - t) ≤ 2b exp − [t] [2]
� 2bσ [2]



,
�



where b represents the hidden dimension. Applying a union bound over all layers, we obtain that
with probability at least 1/2, the spectral norm of each perturbation u ∈ u is bounded by



σ�



2b ln (4Db).


35


Substituting this spectral norm bound into Lemma E.4, we have with probability at least 1/2,


max
G∈G tr ∪G te [|][h][˜] [w][+][u] [(][G][)][ −] [h][˜] [w] [(][G][)][|]









1 + d

�



�



B



 






�







T −1



�


k=0





d(g [(][k][+1)] )
� ∥w(g [(][k][+1)], s)∥


s



d(g [(][k][+1)] )
�







d(f [(][k][+1)] )
�



k=0



≤ e



d(c)
�



� ∥w(c, s)∥ 2


s=1









d(f [(][k][+1)] )
� ∥w(f [(][k][+1)], s)∥


s



+



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



�









d(f )
�


i=1



∥u(f, s)∥ 2
∥w(c, s)∥ 2




 






T −1



�


t=0





t=0

 d


s





�� s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s



d(g [(][k][+1)] )
� ∥w(g [(][k][+1)], s)∥B


s



 - d













T −1



�


k=0









d(f [(][k][+1)] )
�



k=0



≤ e



d(c)
�



� ∥w(c, s)∥ 2


s=1









d(f [(][k][+1)] )
� ∥w(f [(][k][+1)], s)∥


s



+



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



�














d(f )
�


i=1




 






T −1



�


t=0





t=0



�� s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s













d(c)
� ∥w(c, s)∥ 2


s=1



d(c)
�



 B













T −1



�


k=0





k=0







d(f [(][k][+1)] )
�



+ e









d(f [(][k][+1)] )
� ∥w(f [(][k][+1)], s)∥


s



+



∥u(f, s)∥ 2
∥w(c, s)∥ 2


∥u(f, s)∥ 2
∥w(c, s)∥ 2



∥u(f [(][t][+1)], s)∥
∥w(f [(][t][+1)], s)∥



�



d(f )
�


i=1




 






T −1



�


t=0





t=0



�� s



∥u(g [(][t][+1)], s)∥
∥w(g [(][t][+1)], s)∥ [+] � s



+



�



= eβ [D][−][1] d [T][ −][1] B ·







T −1



�


t=0





d(f )
� ∥u(f, s)∥


s=1













t=0



�� s



∥u(g [(][t][+1)], s)∥ + �

s s



∥u(f [(][t][+1)], s)∥

s



+



+ eβ [D][−][(][�] k [T] =1 [d][(][g] [(][k][)] [))][−][1] B ·







T −1



�


t=0





�



d � (f ) ∥u(f, s)∥


s=1





t=0



�� s



∥u(g [(][t][+1)], s)∥ + �

s s



∥u(f [(][t][+1)], s)∥

s



+









�



≤ e [2] [ ˜] β [D][−][1] d [T][ −][1] B ·







T −1



�


t=0





d(f )
� ∥u(f, s)∥


s=1



t=0



�� s



∥u(g [(][t][+1)], s)∥ + �

s s



∥u(f [(][t][+1)], s)∥

s



+









+ e [2] [ ˜] β [D][−][(][�] k [T] =1 [d][(][g] [(][k][)] [))][−][1] B ·







T −1



�


t=0





�



d(f )
� ∥u(f, s)∥


s=1



d(f )
�



t=0



�� s



∥u(g [(][t][+1)], s)∥ + �

s s



∥u(f [(][t][+1)], s)∥

s



+









˜ ˜
= e [2] [ �] β [D][−][(][�] k [T] =1 [d][(][g] [(][k][)] [))][−][1] + d [T][ −][1] β [D][−][1] [�] B ·







T −1



�


t=0





�



d(f )
� ∥u(f, s)∥


s=1



t=0



�� s



∥u(g [(][t][+1)], s)∥ + �

s s



∥u(f [(][t][+1)], s)∥

s



˜ ˜
≤ e [2] [ �] β [D][−][(][�] k [T] =1 [d][(][g] [(][k][)] [))][−][1] + d [T][ −][1] β [D][−][1] [�] Bσ�2b ln (4Db)



≤ [γ]

4 [,]



where for the last inequality we used Equation (45).


Step 6: Putting everything together We finish this section by reformulating and proving Theorem 4.1.

Theorem E.6. Let [˜] h be any classifier in H mpnn with parameters {w i } [D] i=1 [. For any][ γ][ ≥] [0][,][ α][ ≥] [1][/][4]
and large enough N tr, with probability at least 1 − δ over the sample of y tr, we have



L [0] te [(˜][h][)][ −] [L][ˆ] [γ] tr [(˜][h][)][ ≤O]



b [�] i [∥][w] [i] [∥] F [2] 1 h [2] ln 2h [DC][ (2][dB][)] [1][/D] + 1 + CKξ
� N tr [2][α] [(][γ/][8)] [2][/D] [ ξ] [2][/D] [ +] N tr [2][α] γ [1][/D] δ N tr [1][−][2][α] �



.



(46)



36


Proof. The proof follows the proof of Theorem 1 in (Neyshabur et al., 2018) Theorem 6 in (Ma et al.,
2021).


There are two main steps in the proof. In the first step, for a given constant β > 0, we first define
the ”prior” P and the ”posterior” Q on H in a way complying with conditions in Lemma E.1,
Lemma E.3, and Lemma E.5. Without loss of generality (due to the homogeneity of the activation
function), we can assume that β˜ ∥w i [(][j][)] [∥] [2] [ =][ β][ for some][ β][ ≥] [0][. Then, for all classifiers with parameters]
satisfying |β − β [˜] | ≤ D [and][ ˜][β][ being some value on a predefined grid in the parameters space, we]
can derive a generalization bound by applying Lemma E.1, Lemma E.3, and Lemma E.5.


In the second step, we investigate the number of β [˜] we need to cover all possible relevant classifier
parameters and apply a union bound to get the final bound. The two steps are essentially the same
as Neyshabur et al. (2018) with the first step differing by the need for incorporating Lemma E.1.


Step 1. We first show the first step. Given a choice of β [˜] independent of the training data, let



γ
2b �λN tr [−][α] + ln 2bD� [,] e [2] B �β˜ D−(� Tk=1 [d][(][g] [(][k][)] [))][−][1] +



σ = min







 (γ/8ξ) [1][/D]

 �2b �λN tr [−][α]



e [2] B �β˜ D−(� Tk=1 [d][(][g] [(][k][)] [))][−][1] + d [T][ −][1] [ ˜] β [D][−][1] [��]



2h ln(4Dh)



 .



(47)
Assume the ”prior” P on H is defined by sampling the vectorized MLP parameters from N (0, σ [2] I).
The ”posterior” Q on H is defined by first sampling a set of random perturbations {u i } [D] i=1 [and then]
adding them to {w i } [D] i=1 [. By Lemma E.5, we have]



Pr max
� G∈G tr ∪G te [∥][h][˜] [w] [(][G][)][ −] [h][˜] [w][+][u] [(][G][)][∥] [∞] [< γ] 8



≥ [1] (48)
� 2 [.]



Therefore, by applying Lemma E.1, we get with probability at least 1 − δ,



λ [2]

+ (ln 3 + λCKξ)
4N tr �



L [0] te [(˜][h][)][ −] [L][ˆ] [γ] tr [(˜][h][)][ ≤] [1]

λ



λ [2]

4N tr + D te [γ/], [2] tr [(][P] [;][ λ][)] �



≤ [1]

λ



2 (D KL (Q||P ) + 1) + ln [1]
� δ

2 (D KL (Q||P ) + 1) + ln [1]
� δ




[1] λ [2]

δ [+] 4N

[1] λ [2]

δ [+] 4N



(49)




[1] 1 + [2 + ln 3]

δ [+] 4N tr [1][−][2][α] N tr [2][α]



2 1
≤ D KL (Q||P ) + ln [1]
N tr [2][α] N tr [2][α] δ



+ CKξ.
N tr [2][α]



where we chose λ = N tr [2][α] [.]


Moreover, since both P and Q are normal distributions, we know that



D KL (Q||P ) ≤ �


i



∥w i ∥ [2] 2 (50)
2σ [2] [ .]



Per assumption, both B and D are constant with respect to N tr . Hence, for large enough N tr,



(γ/8ξ) [1][/D]
�2b �λN tr [−][α]



γ
2b �λN tr [−][α] + ln 2bD� [<] 4(e [2] + 1)e [2] d [J] B β [D][−][1] [�]



2h ln (4Dh), (51)



which implies,


and hence



(γ/8ξ) [1][/D]
σ = (52)
�2b �λN tr [−][α] + ln 2bD�



tr [+ ln 2][bD][)][ �] i [∥][w] [i] [∥] 2 [2]
D KL (Q||P ) ≤ [b][ (][N] [ α] ξ [2][/D] . (53)
(γ/8) [2][/D]

Therefore, with probability at least 1 − δ,




[1] 1 + [2 + ln 3]

δ [+] 4N tr [1][−][2][α] N tr [2][α]



2 1
L [0] te [(˜][h][)][ −L] tr [γ] [(˜][h][)][ ≤] D KL (Q||P ) + ln [1]
N tr [2][α] N tr [2][α] δ



+ CKξ
N tr [2][α]



(54)

.



�



≤O



b [�] i [∥][w] [i] [∥] 2 [2] 1 ln [1] 1 + CKξ
� N tr [α] [(][γ/][8)] [2][/D] [ ξ] [2][/D] [ +] N tr [2][α] δ [+] N tr [1][−][2][α]



b [�] i [∥][w] [i] [∥] 2 [2] 1 ln [1]
� N tr [α] [(][γ/][8)] [2][/D] [ ξ] [2][/D] [ +] N tr [2][α] δ



37


Step 2. Then we show the second step, i.e., finding out the number of β [˜] we need to cover all possible
relevant classifier parameters. Similarly as Neyshabur et al. (2018), we will show that we only need
to consider � 2γB � 1/D ≤ β ≤ C (recall that the spectral norm of all weight matrices is bounded by



2γB � 1/D, then for any graph G ∈G tr ∪G te, we get ∥h˜(G)∥ ∞ ≤ γ2



C). If β < � 2γ



C). If β < � 2γB �, then for any graph G ∈G tr ∪G te, we get ∥h(G)∥ ∞ ≤ γ2 [, which implies]

that the bound trivially holds. Since we only consider β in the above range, a sufficient condition to
make |β − β [˜] | ≤ D [β] [hold would be][ |][β][ −] [β][˜][| ≤] D1 � 2γB � 1/D . Therefore, it suffices to find a covering



2γB � 1/D . Therefore, it suffices to find a covering



D [β] [hold would be][ |][β][ −] [β][˜][| ≤] D1 � 2γ



for all possible weight matrices with radius [1]



γ 1/D for a ball in R b×b of radius C. This can be

2B �




[1] γ

D � 2



b [2]

satisfied by 2 [DCb][(2][B][)] [1][/D] balls. Taking a union bound, we get, with probability at least 1 − δ,
� γ [1][/D] �



�



L [0] te [(˜][h][)][ −L] [γ] tr [(˜][h][)][ ≤O]



b [�] j � i [∥][w] [i] [∥] 2 [2] 1 b [2] ln 2b [DC][ (2][B][)] [1][/D] + 1 + CKξ
� N tr [2][α] [(][γ/][8)] [2][/D] [ ξ] [2][/D] [ +] N tr [2][α] γ [1][/D] δ N tr [1][−][2][α]



b [�] j � i [∥][w] [i] [∥] 2 [2] 1 b [2] ln 2b [DC][ (2][B][)] [1][/D]
� N tr [2][α] [(][γ/][8)] [2][/D] [ ξ] [2][/D] [ +] N tr [2][α] γ [1][/D] δ



.



(55)


F Fixed Graph Encoders


Next, we apply our analysis to GNNs with fixed encoders. Here, the embedding function e : G → R [b]
is fixed, and only the classifier c : R [b] → R [K] is trainable. Let H = C ◦E, where E now represents a
fixed graph embedding network. The generalization bound in this setting simplifies to the following.

Corollary F.1. Let lat be any pseudometric in the latent space R [d] . Under mild assumptions (see
Appendix D), for any γ > 0 and 0 < α < 4 [1] [, with probability at least][ 1][ −] [δ][ over the sample of]

training labels y tr, the test loss of any classifier h [˜] ∈H



� MC(C)
L [0] te [(˜][h][)] ≤ L [γ] tr [(˜][h][) +][ O] � N tr [2][α] γ [1][/D] δ
� �� �
complexity term



+ C ξ lat, (56)
���� �
structural
similarity term



where ξ lat = max G∈G te min H∈G tr lat (g(G), g(H)) and the other constants are defined in Theorem 4.1.


Proof. The proof follows the same steps as in the proof of Theorem E.6. For example, Lemma E.4
can be shown for MLPs by simply assuming that there are no MPNN layers in Lemma E.4. Theorem E.6 can then be proved for the hypothesis space H by defining the variance as



γ
2b �λN tr [−][α] + ln 2bD� [,] e [2] B β [˜] [D][−][1] [�]



σ = min







 (γ/8ξ) [1][/D]

 �2b �λN tr [−][α]



e [2] B β [˜] [D][−][1] [�]



2b ln(4Db)



 .



In this case, the complexity of the graph embedding model no longer contributes to the bound, and
only the complexity of the MLP classifier affects generalization. This reduced complexity underscores promise of fixed graph encoders.


G Proof of Lemma on Comparison of TMD and F -TMD


Lemma G.1. For any G, H ∈G and any non-empty family of features F [′] ⊂F ⊂G, we have


F [′] -TMD(G, H) ≤F -TMD(G, H).


Proof. Starting from the definitions, we have:



n
�



σ [H] (j [F′] ) �,



TD T [G] [F′]

� � j

j=1



F [′] -TMD(G, H) = min
σ∈S n



j [G] [F′], T σ [H] (j [F′] )



38


F -TMD(G, H) = min
σ∈S n



n
� TD �T j [G] [F], T σ [H] (j [F] ) �,

j=1



where S n is the set of all permutations of the node set {1, 2, . . ., n}, and T j [G] [F] denotes the subtree
of G [F] (the graph G augmented with additional features F ) at node j.


Let σ [′] be the optimal assignment for F -TMD(G, H), i.e.,



F -TMD(G, H) =



n
� TD �T j [G] [F], T σ [H] [′] ( [F] j) � .

j=1



Since F [′] -TMD(G, H) optimizes over all assignments, it follows that



σ [H] [′] ( [F′] j) � . (57)



F [′] -TMD(G, H) ≤


Our goal is to show that for every j:



n
�



TD T [G] [F′]

� � j

j=1



j [G] [F′], T σ [H] [′] ( [F′] j)



j [G] [F′], T σ [H] [′] ( [F′] j)



TD T [G] [F′]
� j



σ [H] [′] ( [F′] j) � ≤ TD �T j [G] [F], T σ [H] [′] ( [F] j) � . (58)



Together, Equation (57) and Equation (58), lead to



σ [H] [′] ( [F′] j) �



F [′] -TMD(G, H) ≤


≤



n
�



TD T [G] [F′]

� � j

j=1



n
� TD �T j [G] [F], T σ [H] [′] ( [F] j) �

j=1



j [G] [F′], T σ [H] [′] ( [F′] j



= F -TMD(G, H).


We proceed to prove Equation (58) via induction. In fact, we show a more general version: for every
assignment ρ between nodes of G and H and any node j, we have



j [G] [F′], T ρ [H] (j [F′] )



TD T [G] [F′]
� j



ρ [H] (j [F′] ) � ≤ TD �T j [G] [F], T ρ [H] (j [F] ) � .



Base Case (t = 0)


At depth 0, the trees consist only of root nodes. The tree distance is the difference between node
features, i.e.,



j [G] [F′], T ρ [H] (j [F′] )



TD T [G] [F′]
� j



ρ [H] (j [F′] ) � = ∥x [′] j [−] [x] [′] ρ(j) [∥]



≤∥x˜ j − x˜ ρ(j) ∥

= TD �T j [G] [F], T ρ [H] (j [F] ) �,


where x [′] j [= (][x] [j] [, c] [j] [(][F] [1] [)][, . . ., c] [j] [(][F] [|F] [ ′] [|] [))][ and][ ˜][x] [j] [ = (][x] [j] [, c] [j] [(][F] [1] [)][, . . ., c] [j] [(][F] [|F|] [))][ include the additional]
features.


Induction Step (t − 1 �→ t)


Assume that for every tree of depth t − 1, we have, for every assignment ρ and every j = 1, . . ., n,



j [G] [F′], T ρ [H] (j [F′] )



TD T [G] [F′]
� j



ρ [H] (j [F′] ) � ≤ TD �T j [G] [F], T ρ [H] (j [F] ) � .



Let σ [′] be any assignment of trees and let τ be the optimal assignment in W TD �T j [F] [,][ T] σ [ F] [′] (j) �.


39


Then, for any j = 1, . . ., n



τ [H] [′] ( [F′] j) �



j [G] [F′], T σ [H] [′] ( [F′] j



TD T [G] [F′]
� j



σ [H] [′] ( [F′] j) � = ∥x [′] j [−] [x] [′] σ [′] (j) [∥] [+ min] τ [′] ∈S n



n
�



TD T [G] [F′]

� � j

j=1



j [G] [F′], T τ [H] [′] ( [F′] j



τ [H] (j [F′] ) �



≤∥x [′] j [−] [x] [′] σ [′] (j) [∥] [+]


≤∥x [′] j [−] [x] [′] σ [′] (j) [∥] [+]



n
�



TD T [G] [F′]

� � j

j=1



n
� TD �T j [G] [F], T τ [H] (j [F] ) �

j=1



j [G] [F′], T τ [H] (j [F′] )



(59)



= ∥x [′] j [−] [x] [′] σ [′] (j) [∥] [+][ W] [TD] �ρ �T j [F] [,][ T] σ [ F] [′] (j) ��


˜ ˜
≤∥x j − x σ ′ (j) ∥ + W TD �ρ �T j [F] [,][ T] σ [ F] [′] (j) ��

= TD �T j [G] [F], T σ [H] [′] ( [F] j) � .



The second inequality follows by the induction hypothesis as the considered trees are of depth t − 1.
Hence, by induction, the inequality TD �T j [G] [F′], T σ [H] [′] ( [F′] j) � ≤ TD �T j [G] [F], T ρ [H] (j [F] ) � holds, completing the



Hence, by induction, the inequality TD �T j [G] [F′], T σ [H] [′] ( [F′] j) � ≤ TD �T j [G] [F], T ρ [H] (j [F] ) � holds, completing the

proof.



j [G] [F′], T σ [H] [′] ( [F′] j



Proof of Theorem 6.1. Assume that y ∼F -TMD.


1. Since any F -GIN classifier h is Lipschitz continuous with respect to F -TMD and h is
stable with respect to weight perturbations, by Theorem 4.1, we have



L [0] te [(˜][h][)][ ≤L] [γ] tr [(˜][h][) +][ O]



b [�] j � i [∥][W] i [ (][j][)] ∥ [2] F 1
ξ [2][/D] + [h] [2] [ ln(2][h][)][DC][(2][dB][)] [1][/D] + + CKξ
� N tr [2][α] [(][γ/][8)] [2][/D] N tr [2][α] [γ] [1][/D] [δ] N tr [1][−][2][α]



,

�



,



with ξ := max G tr ∈G tr,G te ∈G te F -TMD [L] w [+1] (G tr, G te ) and B = max G ∥X(R [F] (G))[i, :]∥ 2 .


2. By Lemma G.1, every F [′] -GIN classifier h [′] is Lipschitz continuous with respect to F -TMD,

as
∥h [′] (G) − h [′] (H)∥≤ L [′] F [′] -TMD(G, H) ≤ L [′] F -TMD(G, H). (60)
Hence, applying Theorem 4.1, we have



L [0] te [(˜][h][)][ ≤L] [γ] tr [(˜][h][) +][ O]



b [�] j � i [∥][W] i [ (][j][)] ∥ [2] F 1
ξ [2][/D] + [h] [2] [ ln(2][h][)][DC][(2][dB] [′] [)] [1][/D] + + CKξ
� N tr [2][α] [(][γ/][8)] [2][/D] N tr [2][α] [γ] [1][/D] [δ] N tr [1][−][2][α]



,

�



,



where B [′] = max G ∥X(R [F] [ ′] (G))[i, :]∥ 2 . Note that B [′] is the only difference compared to
the previous bound.


3. Assume y ∼F -TMD, but apply a F [˜] -GIN classifier h [˜] . Since h [˜] is not necessarily Lipschitz
continuous with respect to F -TMD, we cannot directly apply Theorem 4.1.


However, if y ∼F -TMD, then y ∼ F [˜] -TMD as well. Specifically, if y ∼F -TMD, there
exists for every class k some η k such that η k (G) = Pr(y G = k | G), and η k is Lipschitz
continuous with constant L η k . Then, by Lemma G.1,

|η k (G) − η k (H)| ≤ L η k        - F -TMD(G, H) ≤ L η k        - F [˜] -TMD(G, H). (61)


Consequently, we can now apply Theorem 4.1 to obtain



,

�




[h][)][DC][(2][d][B][)] 1

+ + CKξ [˜]
N tr [2][α] [γ] [1][/D] [δ] N tr [1][−][2][α]



L [0] te [(˜][h][)][ ≤L] [γ] tr [(˜][h][) +][ O]



b [�]


N

�




[�] j � i [∥][W] i [ (][j][)] ∥ [2] F ˜

ξ [2][/D] + [h] [2] [ ln(2][h][)][DC][(2][d][B][ ˜][)] [1][/D]
N tr [2][α] [(][γ/][8)] [2][/D] N tr [2][α] [γ] [1][/D] [δ]



j �



,



where ξ [˜] := max G tr ∈G tr,G te ∈G te F [˜] -TMD [L] w [+1] (G tr, G te ) and B [˜] = max G ∥X(R F [˜] (G))[i, :
]∥ 2 . Note that B [˜] and ξ [˜] are now different compared to the previous bounds in Item 1 and 2.


40


0.6


0.4


0.2


0

|Training loss|Col2|Col3|
|---|---|---|
||Label noise<br>0.0<br>0.2<br>0.5<br>0.8<br>1.0|Label noise<br>0.0<br>0.2<br>0.5<br>0.8<br>1.0|
||||
||||

0 50 100


Epoch



Time to Overfit vs Noise


100


50


0
0 0.5 1


Noise p





Test error vs. noise


0.5


0.4


0.3


0.2

0 0.5 1


Noise p



Figure 4: Left: Training-loss trajectories of a GIN on M UTAGENICITY under increasing label
noise p. Center: Corresponding test errors on M UTAGENICITY rises sharply as label–structure correlation is essential for generalization (mean ± standard deviation across five seeds). Right: Number
of epochs to overfit, i.e., reach 99% training accuracy under increasing label noise p.


H Other Results


The following lemmata are easy to prove.

Lemma H.1. Given a MPNN with t layers such that the message and update functions g [(][k][)] and
f [(][k][)] are Lipschitz continuos with Lipschitz constant L(f [(][k][)] ) and L(g [(][k][)] ), respectively. Then for any
graph G with maximum node degree v, we have



max v [∥≤]
v∈V (G) [∥][x] [(][t][)]



t
� L(f [(][k][)] ) �1 + dL(g [(][k][)] )� [�]
� k=1



B, (62)



where x [(] v [t][)] denotes the output of the MPNN after t layers at node v.
Lemma H.2. Given a MPNN with t + 1 layers such that the message and update functions g [(][k][)] and
f [(][k][)] are Lipschitz continuos with Lipschitz constant L(f [(][k][)] and L(g [(][k][)] ), respectively. Then for any
graph G with maximum node degree v, we have



max v ∥m [(] v [t][+1)] ∥≤ dL g (t+1)



t
� L(f w [(][k][)] [)] �1 + dL(g w [(][k][)] [)] � [�] B, (63)
� k=1



where m [(] v [t][)] denotes the message of the MPNN at the (t + 1)’th layer at node v.

Lemma H.3 (Lemma 2 in (Neyshabur et al., 2018)). let f w : R [n] → R [k] be a neural network
with Lipschitz continuous and homogenous activations and d(f ) layers For any D, Then for any w,
x ∈X B,n, and any perturbation u = vec({U i } [d] i=1 [)][ such that][ ∥][U] [i] [∥] [2] [ ≤] d [1] [∥][W] [i] [∥] [2] [, the change in the]

output of the network can be bounded as follows:



d
�
� i=1



∥f w+u (x) − f w (x)∥ 2 ≤ eB



d
� ∥W i ∥ 2
� i=1



∥U i ∥ 2
∥W i ∥ 2 .



I Additional Experimental Results and Details


This appendix provides a comprehensive overview of our experimental setup, including dataset generation, model architectures, training procedures, evaluation metrics, and additional analyses. All
experiments were run on an internal cluster with Intel Xeon CPUs (28 cores, 192GB RAM) and
GeForce RTX 3090 Ti GPUs (4 units, 24GB memory each), as well as Intel Xeon CPUs (32 cores,
192GB RAM) and NVIDIA RTX A6000 GPUs (3 units, 48GB memory each). Each subsection
corresponds to one of the three experimental tasks.


I.1 Label Noise Experiments


To investigate how MPNNs behave under noisy supervision, we conducted controlled label corruption experiments on three benchmark molecular graph classification datasets from the TUDataset


41


Time to Overfit vs Noise


20


10


0
0 0.5 1


Noise p



Test error vs. noise


0.5


0.4


0.3


0.2

0 0.5 1

|Col1|Col2|Col3|Col4|Col5|
|---|---|---|---|---|
||||||
||||||
||||||
||||||
||||||



Noise p



0.8


0.6


0.4


0.2





0

|Training loss|Col2|Col3|
|---|---|---|
||Label noise<br>0.0<br>0.2<br>0.5<br>0.8<br>1.0|Label noise<br>0.0<br>0.2<br>0.5<br>0.8<br>1.0|
||||
||||

0 10 20 30


Epoch



Figure 5: Left: Training-loss trajectories of a GIN on BZR under increasing label noise p. Center:
Corresponding test errors on BZRrises sharply as label–structure correlation is essential for generalization (mean ± standard deviation across five seeds). Right: Number of epochs to overfit, i.e.,
reach 99% training accuracy under increasing label noise p.





Time to Overfit vs Noise


200


100


0
0 0.5 1


Noise p



Test error vs. noise


0.5


0.4


0.3


0.2

0 0.5 1


Noise p



0.6


0.4


0.2





0

|Training loss|Col2|Col3|
|---|---|---|
||Label noise<br>0.0<br>0.2<br>0.5<br>0.8<br>1.0|Label noise<br>0.0<br>0.2<br>0.5<br>0.8<br>1.0|
||||
||||

0 200 400


Epoch



Figure 6: Left: Training-loss trajectories of a GIN on NCI109 under increasing label noise p. Center: Corresponding test errors on NCI109 rises sharply as label–structure correlation is essential for
generalization (mean ± standard deviation across five seeds). Right: Number of epochs to overfit,
i.e., reach 99% training accuracy under increasing label noise p.


collection (Morris et al., 2020a): M UTAGENICITY, NCI109, and BZR. For each dataset, we randomly corrupted a fixed proportion of the training labels by replacing them with uniformly sampled
class labels.


We employed a MPNN with four layers, ReLU activations, GraphNorm, and a two-layer MLP
head. Each message and update function in the MPNN is given by a MLP with two layers. The
models were trained for up to 5000 epochs with early stopping once 99% training accuracy was
achieved. Label noise levels were varied in 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, and results were averaged
over five random seeds per setting.


We track the per-epoch training and test accuracy/loss, the number of epochs until memorization,
and total training time. This setup closely follows the protocol of Zhang et al. (2017), adapted to
the graph setting, and enables us to study not only final generalization but also how memorization
unfolds over time under increasing label noise.


Figure 4, 5, and 6 visualize the results on M UTAGENICITY, BZR, and NCI109, respectively. Each
figure presents from left to right: (left) the full training curves, (middle) final test accuracy versus noise level, and (right) the number of epochs required to reach 99% training accuracy. These
plots collectively illustrate the sharp transition from generalization to memorization and the datasetspecific sensitivity of MPNNs to label corruption.


As the label noise increases, the time required to reach 99% training accuracy increases moderately—suggesting that fitting corrupted labels is harder, but still feasible. However, all models
eventually reach near-perfect training accuracy across all noise levels, even for fully randomized
labels (p = 1.0), underscoring the high memorization capacity of GNNs. In stark contrast, the test
accuracy consistently deteriorates with increasing noise and converges to chance level at p = 1.0,


42


where labels are entirely uninformative. This gap between training and test performance confirms
that GNNs can overfit to pure noise and emphasizes the need for principled regularization and early
stopping to preserve generalization.


I.2 Task 1: Median-Based Labeling with Cycle Counts


To investigate the role of local structural patterns in graph classification, we generate 3,000 random graphs using three common models: Erd˝os–R´enyi (ER), Barab´asi–Albert (BA), and Stochastic
Block Model (SBM). Each graph’s label is related to the sum of its 3-cycle and 4-cycle counts,
which are computed using NetworkX (Hagberg et al., 2008). The total cycle count is then used to
assign labels: graphs with counts below the dataset median are labeled 0, while those above receive
label 1.


For all synthetic graphs, we sample the number of nodes randomly between 35 and 55. For each
random graph model, we chose the following parameters.


    - Erd˝os–R´enyi (ER) Graphs: We generate an ER graph with edge probability p = 0.1.

   - Barab´asi–Albert (BA) Graphs: Each new node is connected to m = 2 existing nodes
following the BA preferential attachment process.

   - Stochastic Block Model (SBM) Graphs: We randomly select between 3 and 6 blocks, ensuring each block has at least 3 nodes. The probability of an edge within the same block is
sampled uniformly between [0.1, 0.3], while inter-block connections have a probability in
the range [0.001, 0.02].


We evaluate multiple GNN variants to assess the impact of different levels of expressivity:


    - MPNN: A standard Message Passing Neural Network (Gilmer et al., 2017).

   - F l -MPNN: MPNNs enriched with cycle counts of cycles up to length l (Bouritsas et al.,
2023; Barcel´o et al., 2021).

    - Subgraph GNN: Incorporates subgraph structures (Frasca et al., 2022).

    - Local 2-GNN: A local variant of 2-GNN (Morris et al., 2019).

    - Local Folklore 2-GNN: A local variant of 2-Folklore-GNN (Zhang et al., 2024).


Each model is implemented in PyTorch Geometric (Fey & Lenssen, 2019), using the implementation
details of Zhang et al. (2024). We trained the models using the Adam optimizer (Kingma, 2014) with
a learning rate of 10 [−][3] for 100 epochs and cosine scheduler. We fix the test set, and we perform
10-fold cross-validation, reporting mean accuracy (ACC) and standard deviation. Performance is
measured at both the final epoch and the best validation epoch.


We present additional experimental results in Table 4–6 in this appendix. To further illustrate the
strong correlation between labels and F 4 -TMD, we provide a qualitative visualization of the dataset
structure (see Figure 7). Specifically, we select 50 graphs of the ER dataset and project them into a
two-dimensional space using Multidimensional Scaling (MDS), with distances computed based on
standard TMD, F 3 -TMD, F 4 -TMD, and F 12 -TMD. Among these, the projection using F 4 -TMD
exhibits the clearest class separation, visually reinforcing its alignment with the classification task.


I.3 Task 2: Real-World Datasets


We evaluate our generalization framework on six real-world datasets from the TU Dataset collection
(Morris et al., 2020a), spanning both biological and chemical graph classification tasks:


    - Mutagenicity: 4,337 molecular graphs labeled as mutagenic or non-mutagenic.

    - PROTEINS: 1,113 protein graphs classified by their enzymatic function.

    - BZR: 405 graphs representing benzodiazepine receptor ligands labeled for activity.

    - COX2: 467 graphs labeled based on activity against the COX2 enzyme.

    - NCI109: 4,127 graphs representing chemical compounds screened for anti-cancer activity.

    - AIDS: 2,000 graphs with binary activity labels relevant to AIDS antiviral screening.


43


Figure 7: Low-dimensional embeddings via MDS for Task 1 in Section 6. MDS projects the graphs
into R [2] while preserving the pairwise F l -TMDs between graphs in the dataset. From left to right:
TMD, F 3 -TMD, F 4 -TMD, and F 12 -TMD. Visually, F 4 -TMD achieves the best class separation,
highlighting that the labels strongly correlate with F 4 -TMD. As a result, F 4 -MPNNs provide the
best generalization and predictive performance.


To assess whether generalization in MPNNs and MLPs with fixed feature extractors depends on the
structural similarity between test and training graphs, as predicted by our generalization bound in
Theorem 4.1, we conduct two complementary evaluations:


(i) GIN with TMD: We train GINs (Xu et al., 2019) and measure distances between graphs
using the TMD.


(ii) Fixed encoder with Hamming distance: We compute molecular fingerprints
(Gainza et al., 2019) for each graph, apply an MLP classifier, and measure distances in
the resulting feature space via Hamming distance.


We analyze two key properties:


Error vs. TMD Distance To quantify the relationship between structural proximity and model
performance, we report cumulative accuracy. Test graphs are ordered by increasing distance to the
training set, and we compute the cumulative average accuracy. Specifically, given the ordered test
set G 1, . . ., G N te, we define


̸



y˜ i = [1]

i ̸



i
�

̸

j=1



1 h(G i )[y G i ] ≤ max h(G)[k],
� k≠ y Gi �



̸


where ˜y i represents the average accuracy over the first i graphs. For end-to-end trained GIN models,
Figure 2 and Figure 8 illustrate that test accuracy consistently decreases as the structural distance
from the training distribution increases. A similar trend is observed for MLP+fingerprint models
in Figure 9. These empirical results align with our theoretical insights presented in Theorem 4.1,
which predict this performance degradation.


Theoretical vs. Empirical Generalization Bound We further examine how well our bound from
Theorem 4.1 predicts the actual generalization behavior. For each dataset and model, we compute
the theoretical bound using the empirical training loss and the graph distances to the training set
as prescribed by Theorem 4.1 We compare this bound to the observed test error across all datasets.
Results are presented in Figure 3 and in the appendix (Figure 10). While our bound is not tight,
it does track the empirical error trends well across datasets, substantiating our claim that structural
similarity with respect to the right pseudometric governs generalization in graph learning.


I.4 Task 3: MDS-Based Labeling via F 5 -TMD Distances


For the second synthetic task, we construct 500 random graphs and compute pairwise distances
using the F 5 -TMD pseudometric, where F 5 includes cycles up to length 5. Labels are assigned
using a clustering algorithm, ensuring that graphs closer in F 5 -TMD likely share the same label. We
test different GNNs and summarize the results in Figure 11.


Details For the second synthetic task, we generate 500 random graphs between 15 and 35 nodes
using ER graphs with edge probability p = 0.1. We use the F 5 -TMD pseudometric, where F 5
consists of cycles up to length 5. We compute pairwise graph distances with respect to F 5 -TMD
and embed the graphs into a two-dimensional space via Multidimensional Scaling (MDS) (Kruskal,


44


Table 4: Train and test accuracy, Erd˝os–R´enyi graphs. The task is to predict if the count of cycles of
length at most 4 in the cycle basis of each graph is above or below the median of the whole dataset.
The node features are augmented with (hom N ) homomorphism-counts of cycles up to length N,
(sub N ) subgraph-counts of cycles up to length N, and (bas N ) number of cycle graphs up to length
N in the cycle basis.



(a) w/ early stopping.


Num. layers


Model 1 3 5


0.9180 ± 0.0179 0.9216 ± 0.0379 0.9226 ± 0.0318
L-G
0.8707 ± 0.0105 0.8707 ± 0.0110 0.8637 ± 0.0106


0.9162 ± 0.0165 0.9148 ± 0.0409 0.9226 ± 0.0391
LF-G
0.8647 ± 0.0095 0.8683 ± 0.0086 0.8623 ± 0.0112


0.9050 ± 0.0094 0.9135 ± 0.0256 0.9255 ± 0.0403
MP
0.8737 ± 0.0091 0.8694 ± 0.0165 0.8597 ± 0.0126


0.8993 ± 0.0122 0.9115 ± 0.0316 0.9335 ± 0.0462
MP+hom 3 0.8783 ± 0.0105 0.8710 ± 0.0116 0.8750 ± 0.0098


0.8993 ± 0.0121 0.8998 ± 0.0120 0.9185 ± 0.0408
MP+hom 4 0.8783 ± 0.0089 0.8767 ± 0.0063 0.8710 ± 0.0125


0.8913 ± 0.0117 0.9002 ± 0.0198 0.8915 ± 0.0286
MP+hom 7 0.8740 ± 0.0065 0.8693 ± 0.0178 0.8700 ± 0.0097


0.9210 ± 0.0201 0.9465 ± 0.0376 0.9436 ± 0.0393
MP+bas 3 0.8717 ± 0.0173 0.8773 ± 0.0168 0.8783 ± 0.0096


0.9754 ± 0.0061 0.9761 ± 0.0066 0.9841 ± 0.0081
MP+bas 4 0.9870 ± 0.0046 0.9700 ± 0.0154 0.9603 ± 0.0048


0.9782 ± 0.0087 0.9804 ± 0.0051 0.9850 ± 0.0155
MP+bas 7 0.9720 ± 0.0111 0.9573 ± 0.0077 0.9490 ± 0.0093


0.8979 ± 0.0174 0.9340 ± 0.0473 0.9166 ± 0.0320
MP+sub 3 0.8827 ± 0.0123 0.8697 ± .0135 0.8747 ± 0.0144


0.8976 ± 0.0111 0.9090 ± 0.0270 0.9233 ± 0.0287
MP+sub 4 0.8780 ± 0.0031 0.8717 ± 0.0098 0.8733 ± 0.0109


0.8963 ± 0.0059 0.9140 ± 0.0174 0.9312 ± 0.0304
MP+sub 7 0.8790 ± 0.0067 0.8760 ± 0.0092 0.8657 ± 0.0075


0.9194 ± 0.0238 0.9060 ± 0.0338 0.9561 ± 0.0411
Sub-G
0.8710 ± 0.0088 0.8663 ± 0.0074 0.8640 ± 0.0099







(b) w/o early stopping.


Num. layers


1 3 5


0.9904 ± 0.0041 0.9998 ± 0.0004 1.0000 ± 0.0001
0.8543 ± 0.0063 0.8520 ± 0.0073 0.8553 ± 0.0102


0.9868 ± 0.0051 0.9999 ± 0.0003 1.0000 ± 0.0001
0.8450 ± 0.0135 0.8540 ± 0.0121 0.8543 ± 0.0116


0.9906 ± 0.0033 1.0000 ± 0.0001 0.9998 ± 0.0005
0.8490 ± 0.0045 0.8567 ± 0.0087 0.8637 ± 0.0138


0.9886 ± 0.0039 0.9999 ± 0.0002 1.0000 ± 0.0000
0.8480 ± 0.0108 0.8537 ± 0.0107 0.8673 ± 0.0141


0.9302 ± 0.0039 0.9978 ± 0.0018 0.9990 ± 0.0011
0.8720 ± 0.0088 0.8520 ± 0.0138 0.8540 ± 0.0102


0.9091 ± 0.0081 0.9795 ± 0.0040 0.9897 ± 0.0058
0.8693 ± 0.0099 0.8450 ± 0.0123 0.8390 ± 0.0145


0.9956 ± 0.0028 0.9999 ± 0.0002 1.0000 ± 0.0000
0.8657 ± 0.0085 0.8670 ± 0.0097 0.8723 ± 0.0049


0.9904 ± 0.0034 0.9985 ± 0.0021 0.9997 ± 0.0004
0.9793 ± 0.0068 0.9587 ± 0.0072 0.9523 ± 0.0102


0.9958 ± 0.0026 0.9999 ± 0.0003 0.9998 ± 0.0005

0.9660 ± 0.0065 0.9550 ± 0.0062 0.9537 ± 0.0072


0.9933 ± 0.0029 1.0000 ± 0.0001 1.0000 ± 0.0000
0.8510 ± 0.0078 0.8547 ± 0.0075 0.8683 ± 0.0080


0.9853 ± 0.0034 0.9995 ± 0.0009 0.9998 ± 0.0004
0.8487 ± 0.0155 0.8613 ± 0.0127 0.8623 ± 0.0130


0.9018 ± 0.0035 0.9670 ± 0.0070 0.9815 ± 0.0090
0.8803 ± 0.0070 0.8680 ± 0.0121 0.8553 ± 0.0135


0.9887 ± 0.0048 1.0000 ± 0.0001 1.0000 ± 0.0000
0.8623 ± 0.0058 0.8533 ± 0.0088 0.8680 ± 0.0100



1


0.98

|AIDS|Col2|
|---|---|
|||
|#laye|#laye|
|#laye||

10 [1] 10 [2] 10 [3]


TMD to training set





0.9


0.8


0.7





1


0.9


0.8






|COX2|Col2|
|---|---|
|||
|#laye|#laye|
|#laye||


|PROTEINS|Col2|Col3|
|---|---|---|
||#layers<br>1<br>3<br>5|#layers<br>1<br>3<br>5|
|#laye<br><br><br>|#laye<br><br><br>|#laye<br><br><br>|
|#laye<br><br><br>|#laye<br><br><br>||



10 [1] 10 [3] 10 [5]


TMD to training set



10 [1] 10 [2] 10 [3]


TMD to training set



Figure 8: Accuracy of a GIN with 1, 3, and 5 layers versus Tree Mover’s Distance (log scale) to the
training dataset.


1964). MDS embeds the graphs into a two-dimensional space while preserving the initial F 5 -Tree
Mover’s Distances from the raw graph space, i.e., one can formulate it as the optimization problem
given by



arg x 1,...,x min n ∈R [2] � (∥x i − x j ∥− ζ-TMD(G i, G j )) [2] .

i<j



Labels are assigned using 2-means clustering, ensuring that structurally similar graphs remain in the
same class. MDS and 2-means clustering are implemented via scikit-learn (Buitinck et al., 2013).


45


Table 5: Train and test accuracy, Barabasi-Albert graphs. The task is to predict if the count of
cycles of length at most 4 in the cycle basis of each graph is above or below the median of the
whole dataset. The node features are augmented with (hom N ) homomorphism-counts of cycles up
to length N, (sub N ) subgraph-counts of cycles up to length N, and (bas N ) number of cycle graphs
up to length N in the cycle basis.



(a) w/ early stopping.


Num. layers


Model 1 2 5


0.819 ± 0.013 0.794 ± 0.017 0.793 ± 0.019
L-G
0.767 ± 0.014 0.751 ± 0.013 0.747 ± 0.010


0.818 ± 0.018 0.807 ± 0.021 0.822 ± 0.051
LF-G
0.775 ± 0.008 0.770 ± 0.012 0.747 ± 0.015


0.811 ± 0.015 0.802 ± 0.013 0.798 ± 0.022
MP
0.771 ± 0.015 0.767 ± 0.011 0.757 ± 0.009


0.777 ± 0.010 0.750 ± 0.010 0.789 ± 0.019
MP+hom 4 0.774 ± 0.019 0.749 ± 0.021 0.772 ± 0.01


0.840 ± 0.010 0.847 ± 0.017 0.863 ± 0.039
MP+bas 3 0.809 ± 0.020 0.804 ± 0.021 0.798 ± 0.016


0.963 ± 0.012 0.970 ± 0.005 0.963 ± 0.008
MP+bas 4 0.995 ± 0.003 0.994 ± 0.005 0.980 ± 0.008


0.978 ± 0.008 0.978 ± 0.014 0.981 ± 0.016
MP+bas 8 0.989 ± 0.005 0.977 ± 0.007 0.953 ± 0.006


0.795 ± 0.013 0.814 ± 0.030 0.821 ± 0.060
Sub-G
0.760 ± 0.015 0.730 ± 0.015 0.733 ± 0.016



(b) w/o early stopping.


Num. layers


1 2 5


0.928 ± 0.009 0.827 ± 0.006 0.993 ± 0.003
0.747 ± 0.007 0.757 ± 0.014 0.719 ± 0.011


0.846 ± 0.008 0.902 ± 0.006 0.978 ± 0.006
0.773 ± 0.013 0.745 ± 0.010 0.730 ± 0.018


0.849 ± 0.004 0.909 ± 0.011 1.000 ± 0.000
0.762 ± 0.009 0.740 ± 0.011 0.751 ± 0.025


0.787 ± 0.004 0.760 ± 0.005 0.908 ± 0.012
0.778 ± 0.006 0.759 ± 0.011 0.737 ± 0.015


0.962 ± 0.003 0.982 ± 0.005 0.998 ± 0.001
0.809 ± 0.016 0.807 ± 0.015 0.807 ± 0.008


0.972 ± 0.005 0.977 ± 0.007 0.992 ± 0.005
0.994 ± 0.004 0.991 ± 0.006 0.973 ± 0.003


0.982 ± 0.004 0.994 ± 0.003 0.998 ± 0.001
0.989 ± 0.007 0.971 ± 0.009 0.954 ± 0.004


0.918 ± 0.004 0.878 ± 0.011 0.992 ± 0.004
0.755 ± 0.015 0.728 ± 0.011 0.712 ± 0.025



Table 6: Train and test accuracy, Stochastic Block Model graphs. The task is to predict if the count
of cycles of length at most 4 in the cycle basis of each graph is above or below the median of the
whole dataset. The node features are augmented with (hom N ) homomorphism-counts of cycles up
to length N, (sub N ) subgraph-counts of cycles up to length N, and (bas N ) number of cycle graphs
up to length N in the cycle basis.



(a) w/ early stopping.


Num. layers


Model 1 2 5


0.961 ± 0.007 0.972 ± 0.009 0.960 ± 0.011
L-G
0.961 ± 0.003 0.949 ± 0.003 0.943 ± 0.010


0.965 ± 0.005 0.959 ± 0.020 0.962 ± 0.020
LF-G
0.948 ± 0.005 0.942 ± 0.004 0.953 ± 0.011


0.967 ± 0.006 0.973 ± 0.004 0.967 ± 0.004
MP
0.955 ± 0.006 0.962 ± 0.007 0.955 ± 0.006


0.947 ± 0.005 0.950 ± 0.007 0.963 ± 0.013
MP+hom 4 0.953 ± 0.006 0.946 ± 0.006 0.953 ± 0.004


0.966 ± 0.007 0.958 ± 0.007 0.973 ± 0.012
MP+bas 3 0.958 ± 0.012 0.960 ± 0.005 0.959 ± 0.007


0.957 ± 0.011 0.959 ± 0.007 0.979 ± 0.012
MP+bas 4 0.981 ± 0.005 0.977 ± 0.011 0.975 ± 0.005


0.964 ± 0.006 0.959 ± 0.010 0.955 ± 0.005
MP+bas 8 0.982 ± 0.007 0.973 ± 0.004 0.975 ± 0.008


0.957 ± 0.006 0.959 ± 0.010 0.977 ± 0.006
Sub-G
0.951 ± 0.012 0.943 ± 0.006 0.934 ± 0.008



(b) w/o early stopping.


Num. layers


1 2 5


0.968 ± 0.003 0.981 ± 0.002 0.998 ± 0.001
0.961 ± 0.005 0.948 ± 0.005 0.923 ± 0.004


0.968 ± 0.003 0.979 ± 0.005 0.999 ± 0.001
0.957 ± 0.002 0.941 ± 0.006 0.937 ± 0.005


0.973 ± 0.006 0.975 ± 0.003 0.991 ± 0.002
0.951 ± 0.005 0.963 ± 0.005 0.955 ± 0.007


0.958 ± 0.003 0.963 ± 0.002 0.973 ± 0.006

0.953 ± 0.008 0.939 ± 0.008 0.953 ± 0.006


0.979 ± 0.003 0.991 ± 0.001 0.994 ± 0.003
0.960 ± 0.005 0.962 ± 0.007 0.959 ± 0.007


0.980 ± 0.001 0.989 ± 0.003 0.995 ± 0.002
0.989 ± 0.003 0.984 ± 0.003 0.971 ± 0.010


0.982 ± 0.004 0.995 ± 0.001 0.999 ± 0.001
0.978 ± 0.003 0.967 ± 0.003 0.966 ± 0.006


0.970 ± 0.006 0.975 ± 0.002 0.994 ± 0.003
0.954 ± 0.004 0.948 ± 0.009 0.931 ± 0.009



The experimental setup is identical to Task 1, with models trained and evaluated under the same
protocol: We perform 10-fold cross validation with a training/validation/test set with 80/10/10 splits.
We report the test accuracy at the epoch with the highest validation accuracy. This task tests the
ability of different GNN architectures to generalize. The task is generated such that labels strongly
correlate with F 5 -TMD. We present classification performance, showing that F 5 -MPNNs perform
better than MPNNs and more expressive GNN variants.


46


Mutagenicity



0.86


0.85


0.84


0.83


0.82


0.81





0 1 2 3 4 5 6 7



FPD




- 10 [−][2]



Figure 9: Cumulative test accuracy of MLP vs. Fingerprint Distance (FPD).


47


BZR

- 10 [4]
0.1




- 10 [4]



COX2



3


2.8


2.6


2.4

0 200 400


TMD to training dataset



0.1


0


−0.1



0


−0.1



2.6


2.4


2.2
0 100 200


TMD to training dataset



6


4


2




- 10 [4]



PROTEINS



1.5


1.4


1.3


1.2



AIDS

- 10 [4] - 10 [−][2]

1


0


−1



5 · 10 [−][2]


0


−5 · 10 [−][2]


−0.1



1.1

0 200 400


TMD to training dataset


LF-G


Sub-G


F 5 -MPNN


MPNN



0 1 2 3


TMD to training dataset·10 [4]



Figure 10: Caption







|Col1|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
||||11.01|15.6||
||||12.1<br>|17||
||||10.37<br>13.|||
||||11.36|16.8||


0 5 10 15 20


Error (%)


Figure 11: Performance of different GNNs for y ∼F 5 -TMD [3], where F 5 includes cycles up to
length 5. F 5 -MPNN achieves the best performance, supporting our claim that incorporating taskrelevant features outperforms excessive expressivity.


48


