Meta Review of Submission5573 by Area Chair CU1Z
Copy URL of note tv6qukeqbS
Meta Reviewby Area Chair CU1Z03 Jan 2026, 09:04 (modified: 08 Feb 2026, 22:37)EveryoneRevisions
Summary:

The paper addresses a fundamental question in Graph Representation Learning: the trade-off between model expressivity and generalization. It introduces a family of pseudometrics, 
𝜁
-Tree Mover Distances (
𝜁
-TMDs), to quantify the structural similarity between training and test graphs relative to a specific task. The authors derive PAC-Bayes generalization bounds decomposing the error into model capacity and structural alignment terms. Theoretical and empirical results suggest that increased expressivity only improves performance if it aligns with the task's structural requirements (reducing the 
𝜁
-TMD between train and test); otherwise, it may degrade generalization.

The reviewers generally appreciated the novelty of the theoretical framework and the intuition that "more expressivity is not always better." However, significant concerns were raised regarding:

Practicality: The difficulty of selecting the correct pseudometric 
𝜁
 without prior domain knowledge (effectively the model selection problem).
Baselines & Context: The distinction from prior work (specifically Ma et al., 2021) and the relevance of orthogonal GNN issues (oversmoothing, heterophily).
Bounds: The looseness of the derived bounds and the reliance on comparing upper bounds to infer performance degradation.
Experiments: The reliance on synthetic and small-scale TUDatasets.

Given the theoretical insights and the plausible (albeit unilateral) defenses provided by the authors against generic critiques, I recommend accepting the paper.

Reviewer Concerns:

Due to the interruption of the rebuttal process, I have evaluated the author's responses as independent arguments.

Concerns Adequately Addressed:

Differentiation from Prior Work: The authors convincingly distinguished their work from Ma et al. (2021) by clarifying that their framework supports end-to-end trainable GNNs and graph-space metrics, whereas Ma et al. rely on fixed encoders and Euclidean distances.
Orthogonal GNN Issues: Critiques regarding oversmoothing and heterophily (raised by Reviewer wMWG) were effectively argued as orthogonal to the graph-level classification focus of this work.
Computational Feasibility: Concerns about the cost of computing 
𝜁
-TMD were addressed with new runtime tables and approximation strategies (e.g., subsampling).
Bound Validity: While acknowledging the bounds are loose, the authors provided strong rank correlation data (Spearman/Kendall) to demonstrate that the metric meaningfully tracks empirical error.

Outstanding Concerns:

Selection of 
𝜁
: The practical challenge of selecting the correct pseudometric without prior domain knowledge remains a "model selection" bottleneck, as noted by multiple reviewers.
Upper Bound Logic: The theoretical limitation noted by Reviewer uzRa remains: proving a looser upper bound for expressive models does not strictly prove that performance must degrade, only that it may.
Reviewer Scores:
Reviewer cYcW: Remains 6. While the author's response on correlations was strong, the reviewer's initial concerns about the practicality of selecting 
𝜁
 likely prevent a move to a higher score band.
Reviewer uzRa: Remains 4. The authors addressed the novelty concern regarding Ma et al., but this reviewer expressed fundamental skepticism about the "upper bound" logic (arguing that a looser upper bound doesn't prove performance degradation). This theoretical disagreement likely keeps the score at 4.
Reviewer wMWG: Remains 4. Although the authors refuted the relevance of heterophily/oversmoothing, the reviewer felt the paper lacked "actionable guidance" for practitioners. This practical gap likely keeps the score at 4.
Reviewer iyDd: Remains 6. This reviewer was positive about the theoretical depth but felt the results needed significant contextualization. While the authors promised this in the revision, the score likely holds at 6.
Add:
Public Comment
−
＝
≡
Final Summary Comment
Copy URL of note EEN2YU9KTz
Official Commentby Authors03 Dec 2025, 07:53Everyone
Comment:

Dear Area Chair,

Thank you very much for handling our paper! In this comment, we summarize the main weaknesses raised by the reviewers and how we have addressed them.

Access to 
𝜂
: Multiple reviewers (cYcW, uzRa, wMWG) have raised the point that finding the right pseudo-metric 
𝜂
 can be hard. Indeed, selecting the perfect 
𝜂
 is equivalent to solving graph ML model selection. However, our work does not require us to find the perfect 
𝜂
. In contrast, our results suggest a principled way of selecting a strong 
𝜂
 (or finding a strong GNN): One should start with a low-expressivity model and slowly increase expressivity until increasing expressivity reduces performances. More fundamentally, our work serves as a theoretical justification for a common empirical observation in the associ