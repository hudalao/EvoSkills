## **FantasyPortrait: Enhancing Multi-Character Portrait Animation with** **Expression-Augmented Diffusion Transformers**

**Qiang Wang** [1*] **, Mengchao Wang** [1*] **, Fan Jiang** [1†] **, Yaqi Fan** [2] **, Yonggang Qi** [2‡] **, Mu Xu** [1] **,**

1 AMAP, Alibaba Group
yijing.wq,wangmengchao.wmc,frank.jf,xumu.xm@alibaba-inc.com
2 Beijing University of Posts and Telecommunications
yqfan,qiyg@bupt.edu.cn



**Abstract**


Producing expressive facial animations from static images is
a challenging task. Prior methods relying on explicit geometric priors (e.g., facial landmarks or 3DMM) often suffer from
artifacts in cross reenactment and struggle to capture subtle
emotions. Furthermore, existing approaches lack support for
multi-character animation, as driving features from different
individuals frequently interfere with one another, complicating the task. To address these challenges, we propose FantasyPortrait, a diffusion transformer based framework capable
of generating high-fidelity and emotion-rich animations for
both single- and multi-character scenarios. Our method introduces an expression-augmented learning strategy that utilizes
implicit representations to capture identity-agnostic facial dynamics, enhancing the model’s ability to render fine-grained
emotions. For multi-character control, we design a masked
cross-attention mechanism that ensures independent yet coordinated expression generation, effectively preventing feature
interference. To advance research in this area, we propose the
Multi-Expr dataset and ExprBench, which are specifically designed datasets and benchmarks for training and evaluating
multi-character portrait animations. Extensive experiments
demonstrate that FantasyPortrait significantly outperforms
state-of-the-art methods in both quantitative metrics and qualitative evaluations, excelling particularly in challenging cross
reenactment and multi-character contexts. Our project page is
https://fantasy-amap.github.io/fantasy-portrait/.


**1** **Introduction**


Portrait animation aims to generate dynamic facial video sequences from static images, enabling rich and natural expressions with broad applications in film production (Gu
et al. 2024), virtual communication (Khmel 2021), and gaming (Li et al. 2024). Existing approaches typically rely on
driving video inputs and employ generative models (e.g.,
GANs (Zeng et al. 2023; Drobyshev et al. 2022; Wang et al.
2023a; Deng et al. 2024; Guo et al. 2024), NeRF (Yu et al.
2023; Ye et al. 2024), and Diffusion Models (Ma et al. 2024;
Xie et al. 2024; Qiu et al. 2025)) to manipulate facial expressions through geometric priors like facial landmarks (Lu

  - These authors contributed equally.

  - Project leader.

  - Corresponding author.



garesi et al. 2019) or 3D Morphable Models (3DMM) (Egger et al. 2020).
However, these geometry-based methods face two fundamental limitations. First, they struggle with cross reenactment when significant facial geometry differences exist between the source image and the driving video (e.g., across
ethnicities, ages, or genders), often leading to facial artifacts, motion distortions, and background flickering. Second, explicit geometric representations are insufficient to
capture subtle expression variations and complex emotional
nuances, as they require precise alignment between source
and target faces. These issues severely hinder performance
in cross-identity scenarios.
Moreover, prior research primarily focuses on singlecharacter portrait animation, shedding little light on multicharacter collaborative animation. In such a setting, features from different individuals can interfere with each other,
causing expression leakage, where facial attributes of one
character inadvertently transfer to others. This makes it challenging to maintain both expression independence and harmony among characters. The absence of publicly available
datasets and standardized evaluation benchmarks for multicharacter portrait animation further impedes progress in this

area.

In this work, we propose FantasyPortrait, a Diffusion
Transformer (DiT)-based framework for generating precisely aligned, emotionally expressive multi-character portrait animations. Specifically, we extract implicit expression
representations from the driven videos to capture identityagnostic facial dynamics and enhance the model’s ability to
express fine-grained affective nuances through expressionaugmented learning. To enable coordinated yet independent control of multi-character expressions, we introduce
a masked cross-attention mechanism for avoiding intercharacter interference. To advance the training and evaluation of multi-character portrait animation, we present ExprBench, a novel benchmark that captures a wide range
of expressions, emotions, and head movements across both
single- and multi-character settings. Extensive experiments
on ExprBench demonstrate that FantasyPortrait consistently
outperforms existing methods in both quantitative metrics
and qualitative evaluations, particularly in cross-identity
reenactment scenarios. In summary, our key contributions
are as follows:


Figure 1: Given a portrait image and a reference motion video, FantasyPortrait generates vivid animated portraits during crossreenactment. It achieves high-fidelity facial dynamics and natural head movements for both single-character and multi-character.




 - We propose an expression-augmented implicit facial expression control method that enhances subtle expression
dynamics and complex emotions through decomposed
implicit representations and an expression-aware learning module.

 - We design a masked attention mechanism that enables
synchronized multi-character animation while maintaining rigorous identity separation, effectively preventing
cross-character feature interference.

 - We construct ExprBench, a specialized evaluation benchmark for expression-driven animation, along with a
multi-character expression Multi-Expr dataset. Extensive
experiments demonstrate our method superior performance in both fine-grained controllability and expressive
quality.


**2** **Related Work**

**2.1** **Diffusion-Based Video Generation**


Early research on video generation (Chu et al. 2020; Wang
et al. 2020; Clark, Donahue, and Simonyan 2019; Balaji et al. 2019)primarily relied on Generative Adversarial
Networks (GANs) (Goodfellow et al. 2020). Recently, the
groundbreaking progress of diffusion models (Ho, Jain, and
Abbeel 2020) in image generation (Dhariwal and Nichol
2021; Rombach et al. 2022; Podell et al. 2023) has directly catalyzed a surge of interest in video generation. This
field has recently undergone a significant paradigm shift,
transitioning from conventional U-Net architectures (Ronneberger, Fischer, and Brox 2015) to DiTs (Peebles and Xie
2023). U-Net-based approaches (Blattmann et al. 2023; Guo
et al. 2023; Wang et al. 2023b) typically extend pre-trained



image generation models by incorporating temporal attention layers, thereby equipping them with sequential modeling capabilities for video generation. Although these models
have demonstrated remarkable video synthesis performance,
the latest DiT architectures (e.g., Wan (Wan et al. 2025) and
Hunyuan Video (Kong et al. 2024)) have achieved substantial quality improvements. This is accomplished through the
integration of 3D VAEs (Kingma, Welling et al. 2013) as
encoder-decoders, while combining the sequential modeling advantages of Transformer architectures with advanced
techniques such as rectified flows (Esser et al. 2024; Lipman et al. 2022). Moreover, DiT-based models have been
successfully applied to diverse scenarios like camera control (Cao et al. 2025; Zheng et al. 2024), identity-preserving
(Yuan et al. 2025; Zhang et al. 2025; Liu et al. 2025), and
audio-driven (Wang et al. 2025; Kong et al. 2025; Cui et al.
2025a), demonstrating strong application potential and generalization capabilities.


**2.2** **Human Portrait Animation**


Portrait animation generation aims to drive static human portraits into dynamic video sequences by leveraging reference
conditions such as video and facial expressions. Early approaches (Guo et al. 2024; Zeng et al. 2023; Drobyshev
et al. 2022; Wang et al. 2023a) primarily employed GANs
to learned motion dynamics, while more recent methods
based on diffusion models (Xu et al. 2025; Ma et al. 2024;
Xie et al. 2024; Qiu et al. 2025) have demonstrated significantly stronger generative capabilities. However, most existing approaches rely on explicit intermediate representations as driving signals. For instance, Follow-Your-Emoji
(Ma et al. 2024) utilizes facial keypoints, and Skyreels-A1


(Qiu et al. 2025) employs the 3DMM (Retsinas et al. 2024).
These methods exhibit two main limitations. Firstly, due to
significant variations in facial features among individuals,
methods relying on explicit intermediate representations often struggle to achieve precise alignment when there are substantial differences in facial structure between the reference
image and the target portrait, leading to degraded generation
quality. Secondly, these methods typically require portraitspecific keypoint adaptation, making them difficult to generalize to multi-character portrait animation scenarios. In this
study, we propose a novel DiT-based model architecture that
implements implicit feature-driven multiple portrait animation, surpassing previous methods in generation quality and
generalization capability.


**3** **Method**

The overall architecture of FantasyPortrait is illustrated in
Figure 2. Given a reference portrait image and a driving
video clip containing facial movements, we extract implicit facial expression features from the video sequence
and transfer and fuse them into the target portrait to generate the final video output. We propose a novel expressionaugmented implicit control method, which is designed to
learn fine-grained expression features from implicit facial
representations while significantly enhancing the modeling
of challenging facial dynamics, particularly in mouth movements and emotional expressions. Furthermore, we propose a multi-portrait Masked Cross-Attention mechanism to
achieve precise and coordinated control of facial expressions
across multiple characters.


**3.1** **Preliminary**

**Latent Diffusion Model.** Our framework is built upon
the Latent Diffusion Model (LDM) (Rombach et al. 2022),
which operates in latent space rather than pixel space to
enable efficient and stable training. The model employs a
pre-trained VAE to establish bidirectional mapping between
pixel space and latent space. Specifically, the VAE encoder
_E_ transforms input video data _x_ into latent representations
_z_ = _E_ ( _x_ ), and the decoder _D_ reconstructs the latent tokens
back into video space. During training, Gaussian noise _ϵ_ is
incrementally added to _z_ through a forward process, producing noised latents _z_ _t_ = (1 _−_ _t_ ) _z_ + _tϵ_, where _t ∈_ [0 _,_ 1] is sampled from the logit-normal distribution. Furthermore, we incorporate flow matching (Lipman et al. 2022) to simplify the
transformation between complex and tractable probability
distributions, facilitating sample generation through learned
inverse transformations. The LDM’s training objective minimizes the discrepancy between the velocity _v_ _t_ and the noise
predicted by the denoising network _v_ _θ_ using the following
loss function:


_L_ = E _z_ _t_ _,v_ _t_ _,t,c_ � _∥v_ _θ_ ( _z_ _t_ _, t, c_ ) _−_ _v_ _t_ _∥_ 2 [2] � (1)


where _c_ denotes the conditions, _z_ 1 denote the latent embedding of the training sample, and _z_ 0 represents the initialized noise sampled from the gaussian distribution. The velocity term _v_ _t_ = _dz_ _t_ _/dt_ = _z_ 1 _−_ _z_ 0 serves as the regression
target for the model’s prediction task.



**Video Diffusion Transformer.** Diffusion transformer is
an advanced class of diffusion models that employ a multilayer transformer architecture as the denoising network _u_ _θ_,
demonstrating exceptional generative capabilities in video
synthesis tasks (Seawead et al. 2025; Wan et al. 2025; Kong
et al. 2024; Yang et al. 2024). Specifically, we adopt the Wan
(Wan et al. 2025) as the foundational architecture, which
consists of 40 transformer layers. The model utilizes a causal
3D VAE to compress videos both temporally and spatially,
while incorporating umT5 (Chung et al. 2023) as a multilingual text encoder to effectively integrate textual features via cross-attention mechanisms. Furthermore, Wan enhances conditional generation by integrating a CLIP (Radford et al. 2021) image encoder along with a masked training strategy for initial frames, enabling more effective conditioning on image inputs.


**3.2** **Expression-Augmented Implicit Control**


**Implicit** **Expression** **Representations.** We derive
identity-agnostic expression representations from the driving video through an implicit feature extraction pipeline.
In contrast to conventional portrait animation methods that
depend on explicit facial landmarks, our approach leverages
implicit encoding to better disentangle expression-related
features from confounding factors such as camera motion
and subject-specific attributes, thereby achieving more
natural and adaptable animation results. Specifically, we
detect (Huang et al. 2020) and align the facial region in
each frame. Subsequently, we employ a pretrained implicit
expression extractor _E_ _e_ (Wang et al. 2023a) to encode the
driving video into expressive latent features. These features
include lip motion _e_ _lip_, eye gaze and blink _e_ _eye_, head pose
_e_ _head_, and emotional expression _e_ _emo_ .


**Expression-Augmented** **Learning.** Facial expression
generation involves a complex multi-level system, encompassing both relatively simple rigid motion features (e.g.,
head rotation and eye movements) and highly dynamic
non-rigid deformations (e.g., emotion-related muscle activity and lip movements). Simple motions, due to their more
regular patterns and well-defined physical constraints, can
be relatively easily modeled. In contrast, complex motions
involve richer semantic information and subtle muscle
synergies, exhibiting stronger nonlinear characteristics.
This significant disparity in feature complexity poses a
considerable challenge for simultaneous learning of both
motion types.
To address this, we propose an expression-augmented
encoder _E_ _a_ to enhance the learning of subtle and challenging features. Specifically, for _e_ _emo_ and _e_ _lip_, we employ learnable tokens to perform fine-grained decomposition
and enhancement, where each sub-feature corresponds to
more granular muscle groups or emotional dimensions. Each
fine-grained sub-feature then interacts with semantically
aligned video tokens via multi-head cross-attention, effectively capturing region-specific semantic relationships. Subsequently, we concatenate the expression-augmented features with _e_ _head_ and _e_ _eye_ to obtain the motion embedding
_e_ _m_, as follows:


**Multi-Portrait Masked Cross-Attention**



**Expression-Augmented Encoder**































Figure 2: **Overview of FantasyPortrait.**



_e_ _m_ = _Concat_ ( _E_ _a_ ( _e_ _emo_ ) _, E_ _a_ ( _e_ _lip_ ) _, e_ _head_ _, e_ _eye_ ) (2)


**3.3** **Multi-Portrait Animations**

**Multi-Portrait Embeddings.** Using implicit expressionaugmented representations, we derive fine-grained portrait
motion embeddings for individual characters. For multiportrait animations, we detect and crop facial regions using the face recognition model (Huang et al. 2020), then extract identity-specific motion embeddings _e_ _m_ _∈_ R _[f]_ _[×][l][×][c]_ for
each character, where _f_ is the number of frames, _c_ denotes
the number of channel, and _l_ represents the spatial embedding length. The final multi-portrait motion feature ˆ _e_ _m_ is obtained by concatenating all _N_ individual embeddings along
the length axis:


_e_ ˆ _m_ = _{e_ [1] _m_ _[, e]_ [2] _m_ _[, . . ., e]_ _m_ _[N]_ _[} ∈]_ [R] _[f]_ _[×]_ [(] _[N]_ _[×][l]_ [)] _[×][c]_ (3)


**Masked Cross-Attention.** To prevent identity confusion
and cross-interference between expression-driven signals
from different individuals, we design a masked crossattention mechanism to weight the multi-portrait embeddings in all cross-attention layers. We extract the face
mask from the video and then apply trilinear interpolation
to map it to the latent space, obtaining the latent mask
_M_ . The multi-portrait motion embedding _e_ _m_ interact with
each block of the pre-trained DiT through dedicated crossattention layers. The hidden state _Z_ _i_ of each DiT block is
re-expressed as:



_Z_ _i_ _[′]_ [=] _[ Z]_ _[i]_ [+] _[ softmax]_ � _M ⊙_ ~~_√_~~ _dQ_ _Ki_ _K_ _i⊤_



_V_ _i_ (4)
�



_Q_ _i_ represents the query matrices, _K_ _i_ = ˆ _e_ _m_ _W_ _i_ _[k]_ [, and] _[ V]_ _[i]_ [ =]
_e_ ˆ _m_ _W_ _i_ _[v]_ [. Here,] _[ W]_ _[ k]_ _i_ [and] _[ W]_ _[ v]_ _i_ [are trainable projection weights]
for keys and values.


**4** **Experiment**


**4.1** **Multi-Expr Datasets**


To address the current scarcity of multi-portrait facial expression video datasets, we introduce Multi-Expr, a novel
dataset specifically designed for this purpose. The dataset
is curated from OpenVid-1M (Nan et al. 2024) and OpenHumanVid (Li et al. 2025), and we design a comprehensive
data processing pipeline—including multi-portrait filtering,
quality control, and facial expression selection—to ensure
the quality and suitability of the video datasets. First, we
employ YOLOv8 (Reis et al. 2023) to detect the number
of individuals present in each video clip, and retain only
those containing two or more portrait. Next, we filter out
low-quality, blurry, or artifact-ridden clips using aesthetic
scoring (Yeh et al. 2013) and dathe Laplacian operator. Finally, leveraging facial landmarks detected by MediaPipe
(Lugaresi et al. 2019), we compute the angular and motion
variations of key facial points to select clips exhibiting clear
and expressive facial movements. The dataset comprises approximately 30,000 high-quality video clips, each annotated
with descriptive captions generated by CogVLM2 (Hong
et al. 2024).


**4.2** **ExprBench**


Due to the lack of publicly available evaluation benchmarks
in the field of multiple expression-driven video generation,
we introduce ExprBench to objectively compare the performance of different methods in generating facial animations



where _⊙_ denotes element-wise multiplication, _i_ ndexes
the attention block layers, _d_ _K_ denotes the dimension of keys,


Figure 3: **Examples of ExprBench.**


with rich expressions. ExprBench comprises ExprBenchsingle for single-portrait evaluation and ExprBench-multi
for multi-portrait scenarios. Specifically, we meticulously
collected 200 single portraits and 100 driving videos from
copyright-free sources on Pexels [1] to construct ExprBenchSingle. Each driving video was trimmed to 5-second clips
containing approximately 125 frames. The portrait images
encompass realistic human styles, various anthropomorphic
styles (e.g., animals, cartoon characters), and a wide range of
scenarios (e.g., recording studios, performance stages, live
streaming rooms). The driving videos contain diverse facial
expressions (e.g., drooping eyelids, eyebrow twitches), emotions (e.g., happiness, sadness, anger), and head movements.
To further evaluate the performance of multi-portrait
expression-driven generation, we also collected 100 portrait
images and 50 driving videos to construct ExprBench-Multi,
a multi-centric benchmark. ExprBench-Multi is designed to
test and compare the performance of different methods in
handling video generation tasks involving multiple characters’ expressions and movements. Figure 3 showcases examples of portrait images and driving videos from ExprBench.


**4.3** **Implementation Details**

We employ Wan2.1-I2V-14B (Wan et al. 2025) as the pretrained model. We train on the single-portrait-centric Hallo3
Dataset (Cui et al. 2025b) and the multi-portrait-centric
Multi-Expr Dataset as proposed in Sec. 4.1. The entire training process runs on 24 A100 GPUs for approximately 3
days, with a learning rate set to 1e-4. To enhance the variability of video generation, we apply independent dropout to
the reference image, expression features and prompts, each
with a probability of 0.2. We adopt 30 sampling steps during the inference stage. We set the classifier-free guidance
scale (Ho and Salimans 2022) for expressions to 4.5 while
keeping text prompts empty.


**4.4** **Comparison with Baselines**

**Baselines and Metrics.** We select several publicly available portrait animation methods for comparative evaluation
in the single-portrait setting, including LivePortrait (Guo
et al. 2024), Skyreels-A1 (Qiu et al. 2025), HunyuanPortrait
(Xu et al. 2025), X-Portrait (Xie et al. 2024), and FollowYE
(Ma et al. 2024). We employ the multiple faces version of
LivePortrait as the multi-portrait baseline.


1 https://www.pexels.com/



We evaluate all methods on ExprBench. For selfreenactment evaluation, we use the first frame as the source
input image and the driving video as ground truth. To assess the generalization quality and motion accuracy of the
generated portrait animations, we employ the Fr´echet Inception Distance ( **FID** ) (Heusel et al. 2017), the Fr´echet Video
Distance ( **FVD** ) (Unterthiner et al. 2019), Peak Signalto-Noise Ratio ( **PSNR** ), and Structural Similarity Index
( **SSIM** ) (Wang et al. 2004). Additionally, to measure expression motion accuracy, we use Landmark Mean Distance
( **LMD** ) (Lugaresi et al. 2019), while Mean Angular Error
( **MAE** ) (Han et al. 2024) is adopted to evaluate eye movement accuracy. For cross-reenactment evaluation, we utilize
Average Expression Distance ( **AED** ) (Siarohin et al. 2019),
Average Pose Distance ( **APD** ) (Siarohin et al. 2019), and
MAE. AED and APD are used to assess the accuracy of expression and head pose movements respectively.


**Quantitative Results.** The quantitative comparison results are presented in Table 1. The warping-based approach
employed by LivePortrait demonstrates limited accuracy in
controlling global head movements, resulting in the lowest
APD score among the compared methods. Approaches including FollowYE, and Skyreels-A1 utilize explicit facial
landmark to control head or facial movements. However, this
methodology inevitably introduces identity leakage in crossreenactment scenarios, consequently degrading performance
across AED, APD, and MAE evaluation metrics. HunyuanPortrait utilizes implicit signals for facial expression generation, while employing explicit DWPose (Yang et al. 2023)
condition to drive head movements, which still exhibits
limited performance. The GAN-based method LivePortrait
along with UNet-based architectures including HunyuanPortrait, X-Portrait, and FollowYE exhibit inferior FID and
FVD scores, indicating their limitations in generated video
quality, especially in preserving fine facial details, compared
to advanced DiT-based models including Skyreels-A1 and
FantasyPortrait. Our method achieves state-of-the-art performance on expression and head movement similarity metrics including LMD, MAE, AED and APD, demonstrating particularly significant improvements in cross-identity
reenactment. These results validate that our fine-grained implicit expression representation combined with expressionaugmented learning effectively captures nuanced facial expressions and emotional dynamics while maintaining superior cross-identity transfer capabilities. In multi-portrait experiments, our approach also yields the best quantitative results, confirming that the masked cross-attention mechanism
enables robust and precise control over multiple portraits.


**Qualitative Results.** Figure 4 presents the qualitative results, demonstrating that our method achieves more accurate
facial motion transfer and more visually compelling results.
In the single-character case, despite significant interference
from camera movement and body pose variations in the driving video, our method still outperforms all baselines in terms
of visual quality, while the baselines exhibit artifacts and incorrect expressions under such disturbances. This advantage
stems from our expression-enhanced implicit facial control
approach, which enables more robust and nuanced expres

**Self Reenactment** **Cross Reenactment**

**Dataset** **Method**

**FID** _↓_ **FVD** _↓_ **PSNR** _↑_ **SSIM** _↑_ **LMD** _↓_ **MAE** _↓_ **AED** _↓_ **APD** _↓_ **MAE** _↓_



Single



LivePortrait 79.32 438.27 23.38 0.789 6.90 9.29 45.13 39.79 17.09
Skyreels-A1 66.84 373.98 24.58 0.812 4.21 7.59 36.91 24.27 16.41
HunyuanPortrait 74.86 409.14 24.54 0.783 5.73 8.35 40.41 26.12 16.65
X-Portrait 83.28 445.25 22.51 0.739 7.26 9.15 49.26 29.15 18.89

FollowYE 103.75 489.93 21.47 0.692 9.15 12.63 54.11 32.19 21.58
FantasyPortrait **64.66** **358.08** **25.76** **0.818** **5.08** **6.97** **33.45** **23.08** **14.55**



LivePortrait 120.43 416.39 21.98 0.7370 7.36 10.57 59.09 36.14 21.52
Multi
FantasyPortrait **84.09** **391.12** **24.29** **0.7652** **5.34** **7.42** **34.63** **30.64** **16.26**


Table 1: **Quantitative Results on ExprBench.** LMD multiplied by 10 _[−]_ [3], AED multiplied by 10 _[−]_ [2] and APD multiplied by
10 _[−]_ [3] . _↑_ indicates higher is better. _↓_ indicates lower is better. The best results are in bold.


Figure 4: **Qualitative Results.**



**Dataset** **Method** **VQ** **ES** **MN** **ER**



Single



LivePortrait 7.01 6.23 7.59 7.69
Skyreels-A1 7.93 6.68 8.25 7.84
HunyuanPortrait 7.88 6.81 8.13 7.58
X-Portrait 6.66 4.74 6.09 6.57

FollowYE 5.87 4.29 5.77 6.34
FantasyPortrait **8.16** **7.66** **9.03** **8.21**



LivePortrait 4.72 5.96 6.29 6.88
Multi
FantasyPortrait **7.46** **7.17** **8.75** **8.12**


Table 2: **User Study Results.**


sion manipulation. For multi-character scenarios, LivePortrait exhibits noticeable discontinuities between the driven
regions and static background areas, as it relies on segmenting and re-compositing the facial regions in the pixel space.



In contrast, our method employs a masked cross-attention
mechanism that allows for thorough integration of expression features from different identities in the latent space,
without mutual interference or leakage between individuals’
expressions, thereby producing more natural results.


**User Studies.** Considering that the cross-reenactment
evaluation lacks ground truth, we conduct a subjective study
to comprehensively assess the generation quality. Specifically, 32 participants are invited to rate each sample on a
scale from 0 to 10 across four key dimensions: Video Quality ( **VQ** ), Expression Similarity ( **ES** ), Motion Naturalness
( **MN** ), and Expression Richness ( **ER** ). As shown in Table
2, FantasyPortrait outperforms all baselines across all evaluated dimensions. Notably, our method achieves significant
improvements in expression similarity and expressiveness,
demonstrating that our implicit conditional control mechanism and Expression-Augmented Learning framework en

able the model to better capture and transfer fine-grained facial expressions across different identities, which highlight
the strong generalization capability of our approach.


**More Visualization Results.** Our supplementary materials include extended videos showcasing additional visual results, such as diverse portrait styles (e.g., animals and anime
characters), outcomes in various complex real-world scenarios (e.g., glasses occlusion, head accessories, and facial obstructions), identity swapping animation, and multi-portrait
animation generated by combining multiple single-portrait
video inputs.


**4.5** **Ablation Study and Discussion**


**Dataset** **Method** **AED** _↓_ **APD** _↓_ **MAE** _↓_



Single


Multi



Ours 33.45 23.08 **14.55**
Ours(w/o EAL) 42.88 23.10 14.57
Ours(all EAL) **33.38** **23.05** 14.61
Ours(w/o MCA) 33.41 23.06 14.57
Ours(w/o MED) 34.02 23.15 14.63


Ours 34.63 **30.64** **16.26**
Ours(w/o EAL) 43.63 30.75 16.25
Ours(all EAL) **34.45** 30.69 16.29
Ours(w/o MCA) 73.18 46.22 24.37
Ours(w/o MED) 40.92 37.99 22.75



Table 3: **Ablation Studies in Cross Reenactment.**


Figure 5: **Qualitative Ablation Results.**


**Ablation on Expression-Augmented Learning (EAL).**
To validate the effectiveness of our proposed EAL module, we conducted comprehensive comparisons between
three configurations: (1) direct concatenation of all implicit features without EAL ( **Ours(w/o EAL)** ), (2) applying expression-augmented learning to all implicit features
( **Ours(all EAL)** ), and (3) our selective approach focusing
only on lip _e_ _lip_ and emotional _e_ _emo_ features. As demonstrated in Figure 5 and Table 3, the absence of EAL leads to
significantly reduced AED scores, indicating impaired finegrained expression learning capability. Interestingly, both
APD and MAE metrics remain relatively stable across all
configurations, suggesting that head pose and eye movements follow more rigid, easily-learned motion patterns, and



the benefits of augmented learning are inherently limited for
these rigid motions. However, for complex non-rigid motions like lip articulation and emotional dynamics, the performance degradation without EAL becomes pronounced.
These findings validate our design rationale for selectively
applying emotion augmentation to _e_ _lip_ and _e_ _emo_ features,
as full augmentation provides negligible benefits for rigid
motions while unnecessarily increasing computational complexity.


**Ablation on Masked Cross-Attention (MCA).** The results in Table 3 and Figure 5 underscore the critical importance of MCA in multi-portrait applications. Without MCA,
the facial driving features of multiple individuals interfere
with each other, leading to significant degradation across all
evaluation metrics. As illustrated in Figure 5, the absence
of MCA results in mutual interference between characters’
facial expressions, generating conflicting outputs that nearly
eliminate the model’s ability to follow the driving video. In
contrast, our designed masked cross-attention mechanism
effectively empowers the model to independently control
different individuals.


**Ablation on Multi-Expr Dataset (MED).** Our experimental results demonstrate the critical role of multiexpression datasets in portrait animation tasks. As shown in
Table 3 and Figure 5, training exclusively on single-portrait
datasets maintains comparable performance for single portrait animation, but leads to substantial performance degradation and even visual artifacts in multi-portrait scenarios. These findings demonstrate that while multi-expression
datasets may be less essential for single-portrait animation,
they are indispensable for achieving high-quality results in
complex multi-portrait animation tasks, which facilitates the
model’s capacity to acquire nuanced facial expression representations across multiple individuals.


**Limitations and Future Works.** While our method
demonstrates significant advancements, particularly in
cross-identity reenactment portrait animation, two key limitations and future works warrant discussion. First, the iterative sampling process required by diffusion models leads
to relatively slow generation speeds, which may hinder realtime applications. Future research would explore acceleration strategies to improve computational efficiency for timesensitive scenarios. Second, the high-fidelity nature of our
portrait animations raises potential misuse concerns. We
advocate for development of robust detection and defense
mechanisms to mitigate possible ethical risks associated
with this technology.


**5** **Conclusion**

In this work, we present FantasyPortrait, a novel DiT-based
framework for generating expressive and well-aligned multicharacter portrait animations. Our method leverages implicit facial expression representations to achieve identityagnostic motion transfer while preserving fine-grained affective details. Additionally, we introduce a masked crossattention mechanism to enable synchronized yet independent control of multiple characters, effectively soluting ex

pression leakage. To support research in this field, we contribute ExprBench, a comprehensive evaluation benchmark,
along with a multi-character facial expression Multi-Expr
dataset. Extensive experiments demonstrate that FantasyPortrait outperforms existing methods in both single- and
multi-character animation scenarios, particularly in handling
cross-identity reenactment and complex emotional expressions.


**References**


Balaji, Y.; Min, M. R.; Bai, B.; Chellappa, R.; and Graf, H. P.
2019. Conditional GAN with Discriminative Filter Generation for Text-to-Video Synthesis. In _IJCAI_, volume 1, 2.

Blattmann, A.; Dockhorn, T.; Kulal, S.; Mendelevitch, D.;
Kilian, M.; Lorenz, D.; Levi, Y.; English, Z.; Voleti, V.;
Letts, A.; et al. 2023. Stable video diffusion: Scaling latent video diffusion models to large datasets. _arXiv preprint_
_arXiv:2311.15127_ .

Cao, C.; Zhou, J.; Li, S.; Liang, J.; Yu, C.; Wang, F.; Xue, X.;
and Fu, Y. 2025. Uni3C: Unifying Precisely 3D-Enhanced
Camera and Human Motion Controls for Video Generation.
_arXiv preprint arXiv:2504.14899_ .

Chu, M.; Xie, Y.; Mayer, J.; Leal-Taix´e, L.; and Thuerey, N.
2020. Learning temporal coherence via self-supervision for
GAN-based video generation. _ACM Transactions on Graph-_
_ics (TOG)_, 39(4): 75–1.

Chung, H. W.; Constant, N.; Garcia, X.; Roberts, A.; Tay,
Y.; Narang, S.; and Firat, O. 2023. Unimax: Fairer and more
effective language sampling for large-scale multilingual pretraining. _arXiv preprint arXiv:2304.09151_ .

Clark, A.; Donahue, J.; and Simonyan, K. 2019. Adversarial video generation on complex datasets. _arXiv preprint_
_arXiv:1907.06571_ .

Cui, J.; Chen, Y.; Xu, M.; Shang, H.; Chen, Y.; Zhan, Y.;
Dong, Z.; Yao, Y.; Wang, J.; and Zhu, S. 2025a. Hallo4:
High-Fidelity Dynamic Portrait Animation via Direct Preference Optimization and Temporal Motion Modulation.
_arXiv preprint arXiv:2505.23525_ .

Cui, J.; Li, H.; Zhan, Y.; Shang, H.; Cheng, K.; Ma, Y.; Mu,
S.; Zhou, H.; Wang, J.; and Zhu, S. 2025b. Hallo3: Highly
dynamic and realistic portrait image animation with video
diffusion transformer. In _Proceedings of the Computer Vi-_
_sion and Pattern Recognition Conference_, 21086–21095.

Deng, Y.; Wang, D.; Ren, X.; Chen, X.; and Wang, B. 2024.
Portrait4d: Learning one-shot 4d head avatar synthesis using
synthetic data. In _Proceedings of the IEEE/CVF Conference_
_on Computer Vision and Pattern Recognition_, 7119–7130.

Dhariwal, P.; and Nichol, A. 2021. Diffusion models beat
gans on image synthesis. _Advances in neural information_
_processing systems_, 34: 8780–8794.

Drobyshev, N.; Chelishev, J.; Khakhulin, T.; Ivakhnenko, A.;
Lempitsky, V.; and Zakharov, E. 2022. Megaportraits: Oneshot megapixel neural head avatars. In _Proceedings of the_
_30th ACM International Conference on Multimedia_, 2663–
2671.



Egger, B.; Smith, W. A.; Tewari, A.; Wuhrer, S.; Zollhoefer, M.; Beeler, T.; Bernard, F.; Bolkart, T.; Kortylewski, A.;
Romdhani, S.; et al. 2020. 3d morphable face models—past,
present, and future. _ACM Transactions on Graphics (ToG)_,
39(5): 1–38.

Esser, P.; Kulal, S.; Blattmann, A.; Entezari, R.; M¨uller, J.;
Saini, H.; Levi, Y.; Lorenz, D.; Sauer, A.; Boesel, F.; et al.
2024. Scaling rectified flow transformers for high-resolution
image synthesis. In _Forty-first international conference on_
_machine learning_ .

Goodfellow, I.; Pouget-Abadie, J.; Mirza, M.; Xu, B.;
Warde-Farley, D.; Ozair, S.; Courville, A.; and Bengio, Y.
2020. Generative adversarial networks. _Communications of_
_the ACM_, 63(11): 139–144.

Gu, Y.; Xu, H.; Xie, Y.; Song, G.; Shi, Y.; Chang, D.; Yang,
J.; and Luo, L. 2024. Diffportrait3d: Controllable diffusion for zero-shot portrait view synthesis. In _Proceedings_
_of the IEEE/CVF Conference on Computer Vision and Pat-_
_tern Recognition_, 10456–10465.

Guo, J.; Zhang, D.; Liu, X.; Zhong, Z.; Zhang, Y.; Wan, P.;
and Zhang, D. 2024. Liveportrait: Efficient portrait animation with stitching and retargeting control. _arXiv preprint_
_arXiv:2407.03168_ .

Guo, Y.; Yang, C.; Rao, A.; Liang, Z.; Wang, Y.; Qiao, Y.;
Agrawala, M.; Lin, D.; and Dai, B. 2023. Animatediff: Animate your personalized text-to-image diffusion models without specific tuning. _arXiv preprint arXiv:2307.04725_ .

Han, Y.; Zhu, J.; He, K.; Chen, X.; Ge, Y.; Li, W.; Li, X.;
Zhang, J.; Wang, C.; and Liu, Y. 2024. Face-Adapter for
Pre-trained Diffusion Models with Fine-Grained ID and Attribute Control. In _European Conference on Computer Vi-_
_sion_, 20–36. Springer.

Heusel, M.; Ramsauer, H.; Unterthiner, T.; Nessler, B.; and
Hochreiter, S. 2017. Gans trained by a two time-scale update rule converge to a local nash equilibrium. _Advances in_
_neural information processing systems_, 30.

Ho, J.; Jain, A.; and Abbeel, P. 2020. Denoising diffusion
probabilistic models. _Advances in neural information pro-_
_cessing systems_, 33: 6840–6851.

Ho, J.; and Salimans, T. 2022. Classifier-free diffusion guidance. _arXiv preprint arXiv:2207.12598_ .

Hong, W.; Wang, W.; Ding, M.; Yu, W.; Lv, Q.; Wang, Y.;
Cheng, Y.; Huang, S.; Ji, J.; Xue, Z.; et al. 2024. Cogvlm2:
Visual language models for image and video understanding.
_arXiv preprint arXiv:2408.16500_ .

Huang, Y.; Wang, Y.; Tai, Y.; Liu, X.; Shen, P.; Li, S.; Li,
J.; and Huang, F. 2020. Curricularface: adaptive curriculum
learning loss for deep face recognition. In _proceedings of_
_the IEEE/CVF conference on computer vision and pattern_
_recognition_, 5901–5910.

Khmel, I. 2021. Humanization of Virtual Communication:
from Digit to Image. _Philosophy and Cosmology_, 27(27):
126–134.

Kingma, D. P.; Welling, M.; et al. 2013. Auto-encoding variational bayes.


Kong, W.; Tian, Q.; Zhang, Z.; Min, R.; Dai, Z.; Zhou, J.;
Xiong, J.; Li, X.; Wu, B.; Zhang, J.; et al. 2024. Hunyuanvideo: A systematic framework for large video generative
models. _arXiv preprint arXiv:2412.03603_ .

Kong, Z.; Gao, F.; Zhang, Y.; Kang, Z.; Wei, X.; Cai, X.;
Chen, G.; and Luo, W. 2025. Let Them Talk: Audio-Driven
Multi-Person Conversational Video Generation. _arXiv_
_preprint arXiv:2505.22647_ .

Li, H.; Xu, M.; Zhan, Y.; Mu, S.; Li, J.; Cheng, K.; Chen,
Y.; Chen, T.; Ye, M.; Wang, J.; et al. 2025. Openhumanvid: A large-scale high-quality dataset for enhancing humancentric video generation. In _Proceedings of the Computer_
_Vision and Pattern Recognition Conference_, 7752–7762.

Li, R.; Zhang, H.; Zhang, Y.; Zhang, Y.; Zhang, Y.; Guo, J.;
Zhang, Y.; Li, X.; and Liu, Y. 2024. Lodge++: High-quality
and long dance generation with vivid choreography patterns.
_arXiv preprint arXiv:2410.20389_ .

Lipman, Y.; Chen, R. T.; Ben-Hamu, H.; Nickel, M.; and
Le, M. 2022. Flow matching for generative modeling. _arXiv_
_preprint arXiv:2210.02747_ .

Liu, L.; Ma, T.; Li, B.; Chen, Z.; Liu, J.; Li, G.; Zhou,
S.; He, Q.; and Wu, X. 2025. Phantom: Subject-consistent
video generation via cross-modal alignment. _arXiv preprint_
_arXiv:2502.11079_ .

Lugaresi, C.; Tang, J.; Nash, H.; McClanahan, C.; Uboweja,
E.; Hays, M.; Zhang, F.; Chang, C.-L.; Yong, M. G.; Lee, J.;
et al. 2019. Mediapipe: A framework for building perception
pipelines. _arXiv preprint arXiv:1906.08172_ .

Ma, Y.; Liu, H.; Wang, H.; Pan, H.; He, Y.; Yuan, J.; Zeng,
A.; Cai, C.; Shum, H.-Y.; Liu, W.; et al. 2024. Follow-youremoji: Fine-controllable and expressive freestyle portrait animation. In _SIGGRAPH Asia 2024 Conference Papers_, 1–12.

Nan, K.; Xie, R.; Zhou, P.; Fan, T.; Yang, Z.; Chen, Z.;
Li, X.; Yang, J.; and Tai, Y. 2024. Openvid-1m: A largescale high-quality dataset for text-to-video generation. _arXiv_
_preprint arXiv:2407.02371_ .

Peebles, W.; and Xie, S. 2023. Scalable diffusion models
with transformers. In _Proceedings of the IEEE/CVF inter-_
_national conference on computer vision_, 4195–4205.

Podell, D.; English, Z.; Lacey, K.; Blattmann, A.; Dockhorn,
T.; M¨uller, J.; Penna, J.; and Rombach, R. 2023. Sdxl: Improving latent diffusion models for high-resolution image
synthesis. _arXiv preprint arXiv:2307.01952_ .

Qiu, D.; Fei, Z.; Wang, R.; Bai, J.; Yu, C.; Fan, M.; Chen,
G.; and Wen, X. 2025. Skyreels-a1: Expressive portrait
animation in video diffusion transformers. _arXiv preprint_
_arXiv:2502.10841_ .

Radford, A.; Kim, J. W.; Hallacy, C.; Ramesh, A.; Goh, G.;
Agarwal, S.; Sastry, G.; Askell, A.; Mishkin, P.; Clark, J.;
et al. 2021. Learning transferable visual models from natural language supervision. In _International conference on_
_machine learning_, 8748–8763. PmLR.

Reis, D.; Kupec, J.; Hong, J.; and Daoudi, A. 2023. Realtime flying object detection with YOLOv8. _arXiv preprint_
_arXiv:2305.09972_ .



Retsinas, G.; Filntisis, P. P.; Danecek, R.; Abrevaya, V. F.;
Roussos, A.; Bolkart, T.; and Maragos, P. 2024. 3D facial
expressions through analysis-by-neural-synthesis. In _Pro-_
_ceedings of the IEEE/CVF Conference on Computer Vision_
_and Pattern Recognition_, 2490–2501.

Rombach, R.; Blattmann, A.; Lorenz, D.; Esser, P.; and Ommer, B. 2022. High-resolution image synthesis with latent
diffusion models. In _Proceedings of the IEEE/CVF confer-_
_ence on computer vision and pattern recognition_, 10684–
10695.

Ronneberger, O.; Fischer, P.; and Brox, T. 2015. U-net:
Convolutional networks for biomedical image segmentation. In _Medical image computing and computer-assisted_
_intervention–MICCAI 2015: 18th international conference,_
_Munich, Germany, October 5-9, 2015, proceedings, part III_
_18_, 234–241. Springer.

Seawead, T.; Yang, C.; Lin, Z.; Zhao, Y.; Lin, S.; Ma, Z.;
Guo, H.; Chen, H.; Qi, L.; Wang, S.; et al. 2025. Seaweed7b: Cost-effective training of video generation foundation
model. _arXiv preprint arXiv:2504.08685_ .

Siarohin, A.; Lathuili`ere, S.; Tulyakov, S.; Ricci, E.; and
Sebe, N. 2019. First order motion model for image animation. _Advances in neural information processing systems_,
32.

Unterthiner, T.; Van Steenkiste, S.; Kurach, K.; Marinier, R.;
Michalski, M.; and Gelly, S. 2019. FVD: A new metric for
video generation.

Wan, T.; Wang, A.; Ai, B.; Wen, B.; Mao, C.; Xie, C.-W.;
Chen, D.; Yu, F.; Zhao, H.; Yang, J.; et al. 2025. Wan: Open
and advanced large-scale video generative models. _arXiv_
_preprint arXiv:2503.20314_ .

Wang, D.; Deng, Y.; Yin, Z.; Shum, H.-Y.; and Wang, B.
2023a. Progressive disentangled representation learning for
fine-grained controllable talking head synthesis. In _Proceed-_
_ings of the IEEE/CVF Conference on Computer Vision and_
_Pattern Recognition_, 17979–17989.

Wang, J.; Yuan, H.; Chen, D.; Zhang, Y.; Wang, X.; and
Zhang, S. 2023b. Modelscope text-to-video technical report.
_arXiv preprint arXiv:2308.06571_ .

Wang, M.; Wang, Q.; Jiang, F.; Fan, Y.; Zhang, Y.; Qi, Y.;
Zhao, K.; and Xu, M. 2025. Fantasytalking: Realistic talking portrait generation via coherent motion synthesis. _arXiv_
_preprint arXiv:2504.04842_ .

Wang, Y.; Bilinski, P.; Bremond, F.; and Dantcheva, A. 2020.
Imaginator: Conditional spatio-temporal gan for video generation. In _Proceedings of the IEEE/CVF winter conference_
_on applications of computer vision_, 1160–1169.

Wang, Z.; Bovik, A. C.; Sheikh, H. R.; and Simoncelli, E. P.
2004. Image quality assessment: from error visibility to
structural similarity. _IEEE transactions on image process-_
_ing_, 13(4): 600–612.

Xie, Y.; Xu, H.; Song, G.; Wang, C.; Shi, Y.; and Luo, L.
2024. X-portrait: Expressive portrait animation with hierarchical motion attention. In _ACM SIGGRAPH 2024 Confer-_
_ence Papers_, 1–11.


Xu, Z.; Yu, Z.; Zhou, Z.; Zhou, J.; Jin, X.; Hong, F.-T.; Ji,
X.; Zhu, J.; Cai, C.; Tang, S.; et al. 2025. Hunyuanportrait:
Implicit condition control for enhanced portrait animation.
In _Proceedings of the Computer Vision and Pattern Recog-_
_nition Conference_, 15909–15919.

Yang, Z.; Teng, J.; Zheng, W.; Ding, M.; Huang, S.; Xu,
J.; Yang, Y.; Hong, W.; Zhang, X.; Feng, G.; et al. 2024.
Cogvideox: Text-to-video diffusion models with an expert
transformer. _arXiv preprint arXiv:2408.06072_ .

Yang, Z.; Zeng, A.; Yuan, C.; and Li, Y. 2023. Effective
whole-body pose estimation with two-stages distillation. In
_Proceedings of the IEEE/CVF International Conference on_
_Computer Vision_, 4210–4220.

Ye, Z.; Zhong, T.; Ren, Y.; Yang, J.; Li, W.; Huang, J.;
Jiang, Z.; He, J.; Huang, R.; Liu, J.; et al. 2024. Real3dportrait: One-shot realistic 3d talking portrait synthesis.
_arXiv preprint arXiv:2401.08503_ .

Yeh, H.-H.; Yang, C.-Y.; Lee, M.-S.; and Chen, C.-S. 2013.
Video aesthetic quality assessment by temporal integration
of photo-and motion-based features. _IEEE transactions on_
_multimedia_, 15(8): 1944–1957.

Yu, W.; Fan, Y.; Zhang, Y.; Wang, X.; Yin, F.; Bai, Y.; Cao,
Y.-P.; Shan, Y.; Wu, Y.; Sun, Z.; et al. 2023. Nofa: Nerfbased one-shot facial avatar reconstruction. In _ACM SIG-_
_GRAPH 2023 conference proceedings_, 1–12.

Yuan, S.; Huang, J.; He, X.; Ge, Y.; Shi, Y.; Chen, L.; Luo,
J.; and Yuan, L. 2025. Identity-preserving text-to-video
generation by frequency decomposition. In _Proceedings of_
_the Computer Vision and Pattern Recognition Conference_,
12978–12988.

Zeng, B.; Liu, X.; Gao, S.; Liu, B.; Li, H.; Liu, J.; and Zhang,
B. 2023. Face animation with an attribute-guided diffusion
model. In _Proceedings of the IEEE/CVF Conference on_
_Computer Vision and Pattern Recognition_, 628–637.

Zhang, Y.; Wang, Q.; Jiang, F.; Fan, Y.; Xu, M.; and Qi, Y.
2025. Fantasyid: Face knowledge enhanced id-preserving
video generation. _arXiv preprint arXiv:2502.13995_ .
Zheng, G.; Li, T.; Jiang, R.; Lu, Y.; Wu, T.; and Li, X.
2024. Cami2v: Camera-controlled image-to-video diffusion
model. _arXiv preprint arXiv:2410.15957_ .


