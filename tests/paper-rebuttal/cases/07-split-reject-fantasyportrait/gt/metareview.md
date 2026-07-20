Meta Review of Submission8319 by Area Chair Msk3 (decision: Reject; scores 8,6,4,2)

Summary: Initial scores show inconsistencies. After reviewing all rebuttals and discussions, the AC remains concerned about the novelty of EAL and masked cross-attention, unfair comparisons, misleading bold numbers, and missing content in the supplementary material. The authors' excessive embellishment of certain existing modules undermines the perceived innovation.

Reviewer Concerns:
- G4db (conf 4, score 2, likely maintain): "no improvement over APD/MAE" assertion in review was unfounded (EAL applies only to e_lip/e_emo), BUT the AC still finds the limited-novelty rebuttal unconvincing — "difficulty-aware decomposition and selective enhancement" reads as over-the-top description of "two separate refiners of PD-FGC features"; masked attention reweighting ≈ 2D region isolation.
- YcGk (conf 4, score 4, likely maintain): technical concerns (softmax, 3D VAE, occlusion, token dims) partially addressed; detection-confidence approach lacks robustness under severe occlusion; novelty reply unconvincing. Backbone disparity: Skyreels-A1=CogVideoX-5B, HunyuanPortrait=SVD~5B, FantasyPortrait=Wan2.1-I2V-14B. Table 1 bold = "Ours", not SOTA — on HDTF, Skyreels-A1 beats FantasyPortrait on Self-Reenactment (FID,SSIM) and Cross (APD); AC can't tell if typo or intentional.
- coGC (conf 4, score 4→likely LOWER): many "we will update in revision" but no updates in supplementary: no pretrained-backbone ablations, no zoomed-in crops/per-region comparisons, Mediapipe visualization misalignment unfixed, no sample frames/statistics.
- uYNe (conf 5, score 8, likely maintain): shares EAL novelty concern; said rebuttal addressed majority of their concerns.

(Authors' rebuttal summary, 02 Dec 2025: clarified EAL novelty as "selective enhancement of challenging non-rigid components"; elaborated MCA mechanism; only uYNe replied positively, others silent.)
