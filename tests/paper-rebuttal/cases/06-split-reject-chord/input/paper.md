### **CHOrD: Generation of Collision-Free, House-Scale, and Organized Digital** **Twins for 3D Indoor Scenes with Controllable Floor Plans and Optimal Layouts**

Chong Su _[†][,]_ [1] Yingbin Fu _[†][,]_ [1] Zheyuan Hu [2] Jing Yang [2] Param Hanji [2]

Shaojun Wang [1] Xuan Zhao [1] Cengiz Oztireli [¨] [2] Fangcheng Zhong [2]

1 KE Holdings Inc. 2 Department of Computer Science and Technology, University of Cambridge

_†_ indicates equal contribution.



Floor-plan guidance



The area of the

house is 75 square
meters. The house

has 1 living room...


**Ⅲ.** Multi-modal floor planning



**Ⅰ.** Spatially coherent 3D digital twin generation Multi-level layout **IV.** Photo-realistic rendering



Figure 1. _I)_ CHOrD synthesizes realistic and well-structured digital twins for 3D indoor scenes. _II)_ CHOrD can be conditioned on complex
floor plan structures to generate realistic **house-wide** layouts while ensuring **physically plausible**, **spatially coherent**, and **collision-free**
arrangements. It further introduces a **hierarchical** data structure that organizes objects not only at the room level but also at finer scales,
such as desks and coffee tables. _III, IV)_ CHOrD supports controllable floor plans via multimodal inputs, as well as photorealistic, 3Dconsistent rendering. These capabilities equip CHOrD with considerable versatility, enabling a broad range of downstream applications.



**Abstract**


_We introduce CHOrD, a novel framework for scalable_
_synthesis of 3D indoor scenes, designed to create_ _**house-**_
_**scale**_ _,_ _**collision-free**_ _, and_ _**hierarchically structured**_ _indoor_
_digital twins. In contrast to existing methods that directly_
_synthesize the scene layout as a scene graph or object list,_
_CHOrD incorporates a 2D image-based intermediate lay-_
_out representation, enabling effective_ _**prevention of col-**_
_**lision artifacts**_ _by successfully capturing them as out-of-_
_distribution (OOD) scenarios during generation. Further-_
_more, unlike existing methods, CHOrD is capable of gener-_
_ating scene layouts that_ _**adhere to complex floor plans**_ _with_
_multi-modal controls, enabling the creation of coherent,_
_house-wide layouts robust to both geometric and semantic_
_variations in room structures. Additionally, we propose a_
_**novel dataset**_ _with expanded coverage of household items_
_and room configurations, as well as significantly improved_
_data quality. CHOrD demonstrates_ _**state-of-the-art**_ _perfor-_
_mance on both the 3D-FRONT and our proposed datasets,_
_delivering photorealistic, spatially coherent indoor scene_
_synthesis adaptable to arbitrary floor plan variations._


**1. Introduction**


Generative 3D indoor scene synthesis and digital twin creation [7, 12, 15, 16, 18, 20, 22–24, 27, 32, 34–36, 40, 43,



44, 46] play increasingly vital roles not only in _creative_
_and technical workflows_ such as interior design, architectural planning, and virtual or augmented reality, but also
in _advancing embodied AI_ by providing scalable simulated
environments for training and testing. This approach facilitates rapid prototyping, reduces manual labor, lowers deployment costs, and accelerates iteration. Despite recent advances in neural volumetric representations [14, 21], classic
mesh-based assets remain the predominant 3D digital twin
representation in these domains due to superior rendering
quality, direct interactivity, and explicit spatial structures.
Consequently, existing pipelines [16, 18, 23, 27, 32, 35, 46]
primarily follow a procedural generation paradigm, constructing a _scene graph_ or _object list_ for the scene layout,
with each node containing detailed specifications for individual objects. These objects can then be retrieved from a
CAD asset dataset and interacted with or rendered by various graphics and physics engines. Therefore, synthesizing
diverse and logical scene layouts has been a core aspect of
creating high-quality indoor digital twins.
However, a fundamental limitation of existing methods
that construct scene graphs or object lists—either directly
by a tabular generative model [16, 18, 23, 27, 32, 35, 46] or
by an LLM writing configuration files [37, 41]—is their _in-_
_ability_ to prevent physically implausible collisions or overlaps between objects, such as a bed intersecting with cabi


1


nets, during the generation process. While collision detection can be performed as a post-processing step, it is computationally expensive and lacks scalability. Moreover, effectively resolving detected collisions during post-processing
remains nontrivial. Prior work has also attempted to prevent collisions using manually defined rules [5, 41], but this
approach lacks generalizability to arbitrary scenes and cannot be used to learn desirable layout distributions from data.
Another critical yet frequently overlooked limitation of existing methods is their _restriction_ to single-room layout generation [16, 18, 23, 27, 32, 35, 46], which fails to account
for the overall floor plan structure of a house. Since room
shapes, sizes, and the arrangement of various room types
collectively influence the logical organization of the household layout, existing approaches neglect key spatial relationships that are essential for coherent multi-room designs.
The occurrence of these limitations is not coincidental —

neither tabular generative models nor LLMs have the granular spatial understanding needed to distinguish adjacent objects from intersecting ones or to properly incorporate the
floor plan geometries into the generation process.


In this paper, we propose CHOrD, a framework designed
to comprehensively enhance the spatial coherence of digital twin generation for 3D indoor scenes, as highlighted
in Figure 1. In particular, CHOrD _i) prohibits collision_
_artifacts_ during the generation process without relying on
post-processing, collision detection, or pre-defined rules; _ii)_
enables _house-scale layout generation_ that adapts to complex geometric and semantic floor plan structures, which are
controllable via multi-modal input; and _iii)_ supports a _hier-_
_archically structured_ scene graph representation that seamlessly integrates into existing pipelines. Central to our approach is the synthesis of a _2D image-based_ layout representation as an intermediate step in the procedural workflow, which can be subsequently converted into a _hierarchi-_
_cal scene graph_, rather than constructing the graph in a single step. Our key insight is that, compared to the graph representation, which is inherently _tabular_, introducing an intermediate 2D layout representation greatly strengthens the
spatial perception and reasoning of the generative model.
For example, humans can readily spot collisions by examining the top-down view of a layout, whereas simply reviewing a table of bounding boxes does not enable such direct assessment. Designers routinely rely on top-down floor
plan views to create spatially orderly layouts. In a similar vein, CHOrD successfully captures collision artifacts as
_out-of-distribution_ (OOD) scenarios, facilitating the empirical elimination of physically implausible collisions during
the generation process. The 2D layout of CHOrD also enables the adaptation of complex floor plan structures via
various modalities, a feature rarely available in existing approaches. We advocate that all graph-based methods for
digital twin generation incorporate an intermediate 2D lay


out for collision avoidance and house-scale organization.
We additionally introduce a novel dataset, referred to
as the CHOrD dataset, comprising 9,706 scenes with floor
plans and scene layouts, approximately 1.4 times larger than
3D-FRONT [8]. Compared to 3D-FRONT, the CHOrD
dataset expands household item coverage to 26 supercategories, including items from kitchens, bathrooms, and
balconies, addressing gaps in 3D-FRONT, which lacks furnishings in these areas and occasionally leaves living rooms
or bedrooms unfurnished. It also resolves common issues

found in 3D-FRONT, such as misclassified objects, unrealistic placements, and collisions, providing clean layouts
without requiring extensive data cleaning.
Our contributions are summarized as: _i)_ **Framework** [1]

- A novel framework for _house-scale_, _collision-free_, and
_hierarchically structured_ indoor digital twin creation with
multi-modal controllable floor plans; _ii)_ **Dataset** - A novel
dataset of 9,706 scenes with floor plans and scene layouts,
1.4 times larger than 3D-FRONT, with improved item coverage and data quality; and _iii)_ **Performance** - CHOrD’s
state-of-the-art performance on both the 3D-FRONT and
proposed datasets, evaluated both qualitatively and quantitatively, particularly in the near-elimination of unreasonable
object collisions, a prevalent issue in existing methods.


**2. Related Work**


Early work employed a rule-based constraint satisfaction
formulation to generate 3D room layouts for pre-specified
sets of objects [5, 40]. While allowing for moderate diversity, rule-based methods cannot learn desirable layout distributions from data. Other approaches optimized cost functions based on interior design principles [20] and objectobject statistical relationships [44]. The earliest data-driven
approach modeled object co-occurrences using a Bayesian
network and Gaussian mixtures to capture pairwise spatial
relations extracted from 3D scenes [7]. With the availability of large datasets of 3D environments, such as SUNCG

[31], 3D-FRONT [8], SUN3D [39], Matterport3D [4], InteriorNet [17], Structured3D [47], and 3D-FURNITURE [9],
learning-based approaches have gained popularity. Various
methods for indoor scene synthesis have been proposed, including: human-centric probabilistic grammars [24], Generative Adversarial Networks (GANs) trained on matrix
representations of scene objects [46], recursive neural networks for sampling 3D scene hierarchies [16], convolutional neural networks (CNNs) trained on top-down room
images [27, 46], spatial prior graph neural networks trained
on labeled 3D spatial relationships [35, 43], and Variational
Autoencoder (VAE) models trained on top-down functional
furniture group images [22]. Additionally, floor plan synthesis approaches have been proposed using graph neural


1 Our codebase and dataset are available in the Supplementary Materials, and will be publicly released upon acceptance.



2


Inference only **"height": 99,**





Scene layout


|Training only<br>Inference only<br>Floor plan|Col2|
|---|---|
|Floor plan<br>Inference only<br>Training only||



Figure 2. Overview of CHOrD. First, we generate the scene layout using a conditional diffusion model, conditioned on a floor plan image.
Next, we apply object detection to identify individual household items and use a structured scene graph to hierarchically organize the
spatial relationships between rooms and objects, along with their attributes. Finally, the scene is rendered into photorealistic images.



networks [12]. With the development of transformer models

[34], transformer-based approaches have become increasingly popular. These include floor plan-conditioned furniture synthesis and text-conditioned furniture synthesis using transformer autoregressive models [23, 36], as well as
methods integrating expert knowledge in the form of differentiable scalar functions to guide the generation of more
ergonomic layouts [15]. Recently, diffusion models [11]
have demonstrated impressive visual quality in generative
tasks, including indoor furniture synthesis [18, 32]. However, these methods primarily synthesize layouts for individual rooms rather than house-scale scenes that consider

the overall floor plan structure. Additionally, unlike recent works [18, 32, 42], which directly synthesize the scene
graph using a 1D-Unet, our approach employs a 2D-Unet.
This enables a better understanding of the spatial relationships between doors, windows, and furniture, thereby more
effectively preventing collisions, doorway blockages, and
other artifacts. Such artifacts are also present in widely used
indoor scene datasets, such as 3D-FRONT [8, 9], requiring
substantial effort for data cleaning.


**3. CHOrD Pipeline**


We propose a novel pipeline for 3D-aware indoor scene synthesis and digital twin creation, as depicted in Figure 2. The
pipeline starts with a floor plan description—provided as
an RGB image—and use a conditional diffusion model to
generate a corresponding 2D scene layout. The use of this
2D representation enables us to leverage efficient image encoders for layout generation while effectively distinguishing _natural_ and _implausible_ object overlaps. Next, we employ automatic object detectors and segmentation maps to
identify individual household items and extract a structured
scene graph that hierarchically organizes _multi-level_ spatial
relationships and object attributes. Finally, the 3D scene
objects are retrieved accordingly and rendered to produce
photorealistic 3D-consistent images, which can also be deployed in a physics engine for simulation.



**3.1. Diffusion-based scene layout generation**


We leverage the recent success of image-based diffusion
models [2, 28, 29] and frame the problem of generating diverse, realistic indoor scene layouts as a conditional imageto-image translation task, as illustrated in Figure 2 (left).
Unlike complex scene graphs or tabular formats, natural
RGB images serve as a convenient intermediate representation for the layout, easily processed by existing vision tools.
Crucially, since RGB images are easy-to-interpret by an appropriate encoder, we can construct a highly effective conditional generative model that accurately captures the data
distribution. In 2D images, implausible object collisions are
instantly visible and flagged as OOD samples, enabling the
model to generate coherent, realistic layouts.
Specifically, given an image of an empty floor plan _**y**_, we
train a diffusion model _ϵ_ _θ_ ( _**x**_ ; _**y**_ _, t_ ) to model the conditional
distribution of the corresponding layouts _p_ ( _**x**_ _|_ _**y**_ ), where
_ϵ_ _θ_ is structured as a 2D U-Net, following [11], with 3 input channels (random noise) and 3 output channels (the predicted layout image). To incorporate floor plan image conditioning, we expand the U-Net input from 3 to 6 channels.
During training, a predetermined noise schedule realizes a
Markov chain, yielding the diffused sample _**x**_ _**t**_ ( _**x**_ _,_ _**y**_ _, t, ϵ_ ),
where _ϵ ∼N_ ( **0** _,_ _**I**_ ) and _t ∼U_ (0 _,_ 1). The loss function is
given by the denoising score matching objective [11]:


E ( _**x**_ _,_ _**y**_ ) _∼p_ data _,ϵ∼N_ ( **0** _,_ _**I**_ ) _,t∼U_ (0 _,_ 1) � _∥ϵ_ _θ_ ( _**x**_ ; _**y**_ _, t_ ) _−_ _ϵ∥_ [2] [�] _._ (1)


**3.2. Hierarchical scene graph extraction and object**
**retrieval**


To generate a scene graph from the candidate layout _**x**_ _∼_
_p_ ( _**x**_ _|_ _**y**_ ), we follow the automatic framework proposed
by [19]. As depicted in Figure 3, we start by fine-tuning
YOLOv8 [13] to detect the locations and attributes of all
objects present in _**x**_ . The color of each object uniquely
identifies its category from a set of 28 household item categories and 3 floor plan item categories. Detailed color



3


schemes are listed in Supplementary Table 2. The other
relevant attributes are then populated to produce an object
list _O_ = ( _**o**_ **1** _,_ _**o**_ **2** _, . . .,_ _**o**_ _**n**_ ), with each node containing object properties such as category, position, orientation, and
size. We employ YOLOv8 to simultaneously obtain the segmentation maps for each room type, including living rooms,
bedrooms, kitchens, bathrooms, and balconies.

Given the dimensions and category of each object, we
deterministically retrieve an example from a categoryspecific textured mesh database _D_ [2] such that it has the
smallest size difference:


_**e**_ _**i**_ = arg min _i_ _[−]_ _[e]_ _[x]_ _i_ _[∥]_ [2] [+] _[∥][o]_ _[y]_ _i_ _[−]_ _[e]_ _[y]_ _[∥]_ [2] [) :] _[ o]_ _i_ _[c]_ [=] _[ e]_ _[c]_ _[,][ ∀]_ _**[o]**_ _**[i]**_ _[∈O][.]_
_**e**_ _∈D_ [(] _[∥][o]_ _[x]_

(2)
The set of retrieved examples _{_ _**e**_ **1** _,_ _**e**_ **2** _, . . .,_ _**e**_ _**n**_ _}_ constitutes the leaf nodes of the scene graph, as shown in Figure 3.
To position the objects in each room and construct the hierarchal scene graph, we utilize the semantic detection and
segmentation outputs of household items and rooms from
YOLOv8. We straighten the edges of the room polygons,
similar to [19], to reduce uneven lines, and attach doors and
windows to these edges, ensuring corrected wall positions
that enclose the room.

Note that this approach enables CHOrD to generate
granular, hierarchical spatial layouts in a multi-level _au-_
_toregressive_ manner. Specifically, we can iteratively apply
the conditional diffusion model to generate fine-grained layouts, such as placing objects on a coffee table, as illustrated
in Figure 3 (bottom). When generating fine-grained layouts, the conditional input for the diffusion model becomes
the top-down views of the upper level ( _e.g._, the boundaries
of the table) instead of floor plan images.
The advantages of a hierarchical layout data structure are
threefold. First, this structure allows CHOrD to be seamlessly integrated into widely adopted graph-based pipelines
to enhance spatial coherence, which we strongly advocate.
Second, it facilitates a wide range of downstream tasks,
such as intricate robotic spatial understanding and navigation [38]. Finally, this multi-level layout enables CHOrD to
also accommodate natural vertical object overlaps, such as
placing objects on a desk or coffee table.


**3.3. Multi-modal floor planning**


Apart from the main pipeline, the 2D layout of CHOrD
enables additional multimodal controls for the floor plan.
Specifically, we provide two types of controls:


**Text-conditioned floor planning** An alternative and convenient way to specify the floor plan is through natural


2 Note that the selection of this database and its retrieval rules can

be flexibly user-specified, enabling custom functionality by incorporating advanced features into the graph nodes, as explored in many prior
works [42, 45]. CHOrD can be seamlessly integrated into these pipelines.


4





**Rooms**



**Floor plan**


Hierarchical scene graph

|s|Col2|
|---|---|
|||



**Living Room** **Bedroom** **Kitchen** **Bathroom**


























|Tab|Double Door Cabinet ble Washbas|Col3|Col4|
|---|---|---|---|
|||||
|||||











Figure 3. Scene graph extraction and object retrieval.


language, especially when floor plan images are not accessible or incompatible with the format accepted by our
model. Given the success of text-to-image diffusion models [26, 30], text descriptions provide a viable alternative for
floor plan specification, as shown in Figure 7 (left).


**Open-plan-conditioned floor planning** CHOrD also
supports synthesizing floor plans conditioned on an openplan layout, as shown in Figure 7 (right). Specifically, given
a 2D image of an open-plan layout without room arrangements, CHOrD generates complete floor plans with optimal
room separations. This is particularly useful for users looking to modify floor plan structures or synthesize digital twin
environments with greater variety.
These controls are considered extended features of

CHOrD—the main pipeline functions perfectly without
them—but they are made possible largely due to our adoption of a multi-level 2D layout. We anticipate various new
features enabled by this approach. Further technical details
are provided in Supplementary Section A.


**3.4. Rendering**


Finally, we convert the structured scene graph into a 3D
mesh. The wall and floor materials for each _**e**_ _**i**_ are procedurally sampled, while being aware of the rooms to which


they belong. To maintain uniform lighting and shadow consistency across the scene, an appropriately sized area light
is placed at the center of each room. The UE engine [6] is
subsequently utilized to generate photorealistic renderings.
The key advantage of the multi-stage pipeline of
CHOrD—which first generates a 2D layout rather than directly synthesizing an object scene graph using a tabular
generative model [18, 32] or LLMs [37, 41]—lies in its enhanced granular spatial understanding, adapting to various
floor plan structures and object placements. By leveraging
an intermediate 2D layout, CHOrD ensures that the hierarchical spatial relationships between household items are
preserved, avoiding common issues such as object overlap,
collision, or inconsistencies between object placement and
room shapes, as validated in Section 5.


**4. CHOrD Dataset**


We collected a new large-scale dataset, which we refer to as
the CHOrD dataset, of indoor scenes with floor plans and
scene layouts, comprising a total of 9,706 design schemes,
approximately 1.4 times larger than the 3D-FRONT dataset

[8]. This dataset was meticulously created by professional
interior designers, stored in JSON format with vectorized
data, as exampled in Appendix List 1, including wall lines,
doors, windows, and household items such as furniture, fixtures, and appliances. The data description is as follows:

- **Rooms** : Represented as enclosed loops of interior wall
lines, defined by 2D coordinates.

- **Doors, windows, and household items** : Represented as
2D bounding boxes, defined by category, 3D coordinates,
orientation, and dimensions (length, width, height).

It is important to note that CHOrD dataset is a 3D _layout_
dataset rather than a 3D _asset_ dataset. The layout primarily focuses on the geometric characteristics ( _e.g._, bounding
boxes) and categorical distinctions among objects. While
CHOrD dataset is currently linked to a small pool of CAD
asset models, users are free to retrieve assets from any large
public dataset [1, 9] to introduce _stylistic variations_ of objects if needed. Similarly, 3D-FRONT has been associated
with the 3D-FUTURE dataset [9] for this purpose. CHOrD
dataset offers several clear advantages over 3D-FRONT:


**Expanded coverage of household items and room cate-**
**gories** While 3D-FRONT provides instance semantic labels for 34 categories and 10 super-categories of household
items, its dataset primarily includes objects placed in living
rooms, bedrooms, and dining rooms, with no objects for
kitchens, bathrooms, or balconies. Consequently, the layouts in 3D-FRONT are consistently devoid of furnishings
in these areas, as seen in Figure 4. Our CHOrD dataset fills
this gap by offering 26 super-categories of household items,
including furniture, fixtures, and appliances, that comprehensively cover living rooms, bedrooms, dining rooms,



Empty rooms


Object exceeding room boundaries


Object overlaps


Figure 4. Erroneous scenes in 3D-FRONT.


kitchens, bathrooms, and balconies. Our CHOrD dataset
not only contains more valid living rooms and bedrooms
(each with at least one household item in place), but also
includes outfitted kitchens and bathrooms. A comprehensive statistic of the CHOrD dataset in comparison with 3DFRONT is detailed in Supplementary Table 5 and Figure 11.


**Improved data quality** As frequently reported [18, 23,
27, 32, 46], the 3D-FRONT dataset contains erroneous layouts such as empty rooms, unnatural object sizes, misclassified items, and unrealistic object placements ( _e.g._, furniture
outside room boundaries, lamps on the floor, blockage of
doorways, and overlapping objects), as seen in Figure 4.
Consequently, previous work [18, 23, 27, 32, 46] using 3DFRONT invested considerable effort in data cleaning, removing numerous layouts with artifacts, which greatly reduced the amount of valid data. In contrast, our dataset is
ready to use without these artifacts. Supplementary Table 6
and 7 provide additional details.


**5. Experiments**


We conducted several experiments to assess the performance of CHOrD on structured layout synthesis and compare it with prior work. We particularly evaluate the effectiveness of CHOrD in eliminating collision artifacts by
assessing its ability to capture these scenarios as out-ofdistribution samples. Next, we demonstrate the versatility
of CHOrD in several extended tasks, including fine-grained
layout synthesis, multi-model floor planning, and photorealistic rendering.


**5.1. Floor plan-conditioned synthesis**


**Implementation** We trained CHOrD on four RTX 8000
GPUs with a batch size of 4 for 400 epochs. The initial
learning rate was set to 1e-4, with a decay factor of 0.1 every 100 epochs. For the diffusion process, we followed the
default configuration of DDPM [11], where noise intensity
gradually increases from 0 to 1 over 1000 time steps. For



5


DiffuScene


InstructScene


PhyScene


CHOrD


3D-FRONT CHOrD dataset


Figure 5. Visualization of synthesized layouts by CHOrD, DiffuScene [32], InstructScene [18], and PhyScene [42]. All results were
randomly selected from an arbitrary batch _without any cherry-picking_ . It is evident that only CHOrD produces clean, collision-free layouts,
whereas other methods exhibit significant artifacts such as implausible overlapping items, inconsistent orientations, or missing objects.

|Dataset|Bedroom|Living Room|Entire House|
|---|---|---|---|
|Dataset|FID_↓_<br>KID_↓_<br>POR_↓_<br>PIoU_↓_|FID_↓_<br>KID_↓_<br>POR_↓_<br>PIoU_↓_|FID_↓_<br>KID_↓_<br>POR_↓_<br>PIoU_↓_|
|DiffuScene<br>3D-FRONT<br>InstructScene<br>3D-FRONT<br>PhyScene<br>3D-FRONT<br>CHOrD (ours)<br>3D-FRONT|15.91<br>0.04<br>0.1632<br>0.0152<br>22.35<br>0.02<br>0.2039<br>0.0088<br>-<br>-<br>-<br>-<br>**14.78**<br>**0.008**<br>**0.0766**<br>**0.0013**|45.89<br>0.034<br>0.05<br>0.012<br>-<br>-<br>-<br>-<br>117.29<br>0.119<br>0.389<br>0.0134<br>**24.15**<br>**0.018**<br>**0.0207**<br>**0.0015**|-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>11.51<br>0.01<br>0.0130<br>0.0005|
|DiffuScene<br>CHOrD dataset<br>InstructScene<br>CHOrD dataset<br>CHOrD (ours)<br>CHOrD dataset|37.16<br>0.03<br>0.1922<br>0.0038<br>48.59<br>0.05<br>0.3010<br>0.0092<br>**21.86**<br>**0.02**<br>**0.1049**<br>**0.0025**|29.97<br>0.02<br>0.0707<br>0.0028<br>46.05<br>0.04<br>0.0908<br>0.0037<br>**26.69**<br>**0.02**<br>**0.0485**<br>**0.0021**|-<br>-<br>-<br>-<br>-<br>-<br>-<br>-<br>29.97<br>0.039<br>0.0125<br>0.0007|



Table 1. Quantitative evaluation of CHOrD against prior approaches, demonstrating superior performance across all metrics and datasets.



the object detection process, we followed the default configuration of YOLOv8 [13]. Further implementation details
can be found in Supplementary Section A.


**Datasets** We compare CHOrD with baseline methods on
both the 3D-FRONT dataset [8] and the proposed CHOrD
dataset. The 3D-FRONT dataset consists of 6,813 scenes,
of which 4,847 were retained after a cleaning process that
excluded layouts lacking furniture, containing objects extending beyond room boundaries, or exhibiting collisions.



Prior works [18, 23, 27, 32, 46] have applied similar data
filtering to remove erroneous scenes from 3D-FRONT due
to various artifacts, as discussed in Section 4. The CHOrD
dataset comprises 9,706 scenes and is ready for use without
the need for data cleaning or preprocessing. We use 80% of
the dataset for training and 20% for testing.


**Baselines** We compare CHOrD with the latest work DiffuScene [32], InstructScene [18], and PhyScene [42], all
aiming to synthesize 3D indoor scenes with optimized lay


6


outs. Note that DiffuScene, InstructScene, and PhyScene
are all _unable_ to synthesize house-scale layouts but individual categories of rooms.
For evaluation on the 3D-FRONT dataset, we used the
official pre-trained checkpoints of these methods to ensure
their optimal performance. Specifically, we used the checkpoint from the DiffuScene unconditional model to generate top-down views of object arrangements in bedrooms
and living rooms at a resolution of 256 _×_ 256, matching
the image size generated by our diffusion model. For InstructScene, we similarly used the checkpoint from the unconditional model to generate bedroom views at the same
resolution. InstructScene did not release unconditional

model checkpoints for living rooms. For PhyScene, we
used their checkpoint from the floorplan-conditioned model
to generate living room layouts. PhyScene did not release
model checkpoints for bedrooms. To ensure fairness in the
comparison, the object categories generated by DiffuScene,
InstructScene, and PhyScene were remapped to our categorization, as detailed in Supplementary Table 4. For evaluation on the CHOrD dataset, we re-trained the unconditional
models of DiffuScene and InstructScene on living rooms
and bedrooms using their default training configurations.
PhyScene did not release its training code.


**Results** We present the qualitative evaluation of all methods in Figure 5, with all results randomly selected without cherry-picking. CHOrD effectively synthesizes diverse,
spatially coherent, and collision-free layouts, while other
methods produce significant artifacts, including physically
implausible object collisions, inconsistent object orientations, and missing objects, greatly limiting their practical
applicability. Moreover, unlike CHOrD, these methods cannot generate house-scale layouts covering all rooms. Figure 8 illustrates house-scale layouts synthesized by CHOrD,
as well as photorealistic renderings. Additional results are
available in Supplementary Materials. Notably, CHOrD can
generate diverse 2D layouts from the same floor plan, despite CHOrD dataset containing only one layout per plan.
We present the quantitative evaluation of all methods in
Table 1. Following previous work [18, 32, 42], we use
Frechet Inception Distance (FID) [10] and Kernel Inception
Distance (KID) [3] to assess the quality and diversity of synthesized layout images. Additionally, we compute two metrics to evaluate 2D bounding box collisions in synthesized
layouts: Pairwise Overlap Ratio (POR), which quantifies
the proportion of intersecting object pairs relative to the total number of pairs, and Pairwise Intersection over Union
(PIoU), which measures the ratio of the intersecting area
between two objects to the combined area of their union.
The average values for these metrics are obtained by first
computing per-scene values, followed by applying the arithmetic mean. CHOrD consistently achieves state-of-the-art
performance across all metrics and datasets.



Figure 6. Fine-grained coffee table and desk layouts that accommodate natural vertical object overlaps. The computer setup in the
right column, consisting of a monitor, keyboard, and mouse, was
modeled as a single object placed on the mat.


**Collision as OOD samples** In diffusion models, the training loss is computed as the reconstruction error of the data
given the noise, serving as an approximation of the negative
log-likelihood (NLL). After adequate training, if a sample
has a high training loss and, consequently, a high NLL, it
is most likely an out-of-distribution (OOD) sample within
the learned distribution that is _improbable_ to be generated
during sampling. To validate the effectiveness of CHOrD
in preventing implausible collision artifacts by recognizing
them as OOD samples during inference, we computed the
training loss for clean 3D-FRONT layout samples devoid
of collisions and for a set of 400 3D-FRONT samples with
the largest PIoU values. The loss was calculated by adding
noise to the samples at timesteps ranging from 900 to 1000,
measuring the mean squared error between the true and predicted noise, and averaging the results over 100 iterations.
The results indicate an average loss of 5 _._ 37 _×_ 10 _[−]_ [5] for the
clean samples and 7 _._ 10 _×_ 10 _[−]_ [5] for the samples with collisions, a significant 32.22% difference explaining the efficacy of CHOrD in identifying and prohibiting unnatural
object collisions as OODs.


**5.2. Fine-grained layout synthesis**


As discussed in Section 3.2, the multi-level graph structure
enables CHOrD to synthesize fine-grained layouts such as
placing objects on a coffee table. This can be achieved by
iteratively applying the conditional diffusion model, except
that the floor plan image conditioning is replaced by an image indicating the boundaries of upper-level items.


**Dataset and implementation** Since neither the 3DFRONT nor CHOrD datasets contain fine-grained layouts
for this task, we additionally collected a small dataset of object placements on common household items such as dining
tables, coffee tables, and desks. We recorded the object categories, positions, orientations, and sizes, as well as their
bounding boxes, and generated top-view images of their
layouts. Object categorization and their color schemes are
detailed in Supplementary Table 3. The objects were drawn
proportionally to their absolute sizes, with the maximum
drawing area fixed at 2-meter squares. We adhered to the
same training procedures as detailed in Section 5.1.



7


The area of the

house is 95 square
meters. The house

has 1 living room 3
bedroom 1 kitchen 1

bathroom.



The area of the

house is 130 square
meters. The house

has 1 living room 3
bedroom 1 kitchen 2

bathroom.



Figure 7. Multi-modal floor planning.


**Results** We present exemplar results in Figure 6. CHOrD
enables two mechanisms that simultaneously prevent implausible object collisions while allowing natural vertical
overlaps. First, as discussed in Section 3.2, the iterative
multi-level layout generation allows fine-grained objects to
be placed on upper levels, such as a computer on a desk.
Second, some vertical overlaps do not exhibit clear hierarchical relationships, such as an object partially resting on a
desk mat. In this scenario, we directly train the diffusion
model with RGB images containing vertical overlaps, enabling it to generate plausible layouts with natural vertical
overlaps while preventing unreasonable ones. The unique
color assigned to each object guides the 2D diffusion model
in distinguishing permissible overlaps from invalid ones.
Due to the limited availability of naturally occurring partially overlapped objects, we demonstrate this feature only
at the fine-grained level. Figure 6 illustrates both scenarios.


**5.3. Multi-modal floor planning**


**Text-conditioned floor planning** For text conditioning,
we parse the JSON file of each scene in the CHOrD dataset
to extract the total area, room count, and categories to generate the corresponding textual description.


**Open-plan-conditioned floor planning** We use the
CHOrD dataset to generate open-plan layouts and floor
plans with proper room arrangements as grayscale images,
with different colors representing room types.
Both experiments followed the same training procedures
as detailed in Section 5.1. We present exemplar results in
Figure 7 and more in Supplementary Figure 13, 14.


**6. Discussions and Summary**


In this paper, we propose a novel framework that employs
a 2D image-based intermediate layout representation to ensure house-scale, spatially coherent, collision-free, and hierarchically structured digital twins for indoor 3D scenes.



Living room Bedroom


Figure 8. **Top** - Visualization of three diverse layouts (columns)
synthesized by CHOrD for each of the three floor plans (rows).
CHOrD is robust to irregular and slanted room shapes. **Bottom** Photorealistic rendering of living rooms and bedrooms with identical camera positions and floor plans, highlighting layout diversity.
The correspondence between the layout on the top and the rendering on the bottom is indicated by matching colored frames.


The success of CHOrD hinges on its comprehensively enhanced spatial understanding compared to existing solutions, such as tabular generative models or LLMs, which
struggle to meet these objectives. Notably, CHOrD prevents
implausible object collisions while allowing natural vertical
overlaps, demonstrating considerable robustness. CHOrD
can seamlessly integrate into existing graph-based pipelines
for digital twin creation, enabling photorealistic rendering
and physics simulation for various downstream tasks.


**Limitations** CHOrD did not explore stylistic control of
individual objects or text-guided object placement, as has
been explored by prior works [18, 32]. However, as CHOrD
can be integrated into these pipelines, we leave these features for future work. In extremely rare cases, YOLOv8
failed to detect precise bounding boxes, leading to misoriented objects or minor collisions despite the layout images
being axis-aligned and collision-free. This can be readily addressed with more training data, thanks to the strong
scalability of CHOrD, as evidenced in Supplementary Section C. With the same amount of training data, CHOrD outperforms prior work by a significant margin.



8


**References**


[1] 3D66. 3d model website, 2013. 5

[2] Tomer Amit, Tal Shaharbany, Eliya Nachmani, and Lior
Wolf. Segdiff: Image segmentation with diffusion probabilistic models. _arXiv preprint arXiv:2112.00390_, 2021. 3

[3] Mikołaj Bi´nkowski, Danica J Sutherland, Michael Arbel, and
Arthur Gretton. Demystifying mmd gans. _arXiv preprint_
_arXiv:1801.01401_, 2018. 7

[4] Angel Chang, Angela Dai, Thomas Funkhouser, Maciej
Halber, Matthias Niessner, Manolis Savva, Shuran Song,
Andy Zeng, and Yinda Zhang. Matterport3d: Learning
from rgb-d data in indoor environments. _arXiv preprint_
_arXiv:1709.06158_, 2017. 2

[5] Matt Deitke, Eli VanderBilt, Alvaro Herrasti, Luca Weihs,
Jordi Salvador, Kiana Ehsani, Winson Han, Eric Kolve,
Ali Farhadi, Aniruddha Kembhavi, and Roozbeh Mottaghi.
Procthor: Large-scale embodied ai using procedural generation, 2022. 2

[6] Epic Games. Unreal engine. 5

[7] Matthew Fisher, Daniel Ritchie, Manolis Savva, Thomas
Funkhouser, and Pat Hanrahan. Example-based synthesis
of 3d object arrangements. In _International Conference on_
_Computer Graphics and Interactive Techniques_, 2012. 1, 2

[8] Huan Fu, Rongfei Jia, Lin Gao, Mingming Gong, Binqiang
Zhao, Steve Maybank, and Dacheng Tao. 3d-future: 3d furniture shape with texture. _International Journal of Computer_
_Vision_, pages 1–25, 2021. 2, 3, 5, 6

[9] Huan Fu, Rongfei Jia, Lin Gao, Mingming Gong, Binqiang
Zhao, Steve Maybank, and Dacheng Tao. 3d-future: 3d furniture shape with texture. _International Journal of Computer_
_Vision_, pages 1–25, 2021. 2, 3, 5

[10] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner,
Bernhard Nessler, and Sepp Hochreiter. Gans trained by a
two time-scale update rule converge to a local nash equilibrium. _Advances in neural information processing systems_,
30, 2017. 7

[11] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. 2020. 3, 5

[12] Ruizhen Hu, Zeyu Huang, Yuhan Tang, Oliver Van Kaick,
Hao Zhang, and Hui Huang. Graph2plan: Learning floorplan generation from layout graphs. _ACM Transactions on_
_Graphics_, 39(4), 2020. 1, 3

[13] Glenn Jocher, Ayush Chaurasia, and Jing Qiu. Ultralytics
YOLO, 2023. 3, 6

[14] Bernhard Kerbl, Georgios Kopanas, Thomas Leimk¨uhler,
and George Drettakis. 3d gaussian splatting for real-time
radiance field rendering. _ACM Trans. Graph._, 42(4):139–1,
2023. 1

[15] Kurt Leimer, Paul Guerrero, Tomer Weiss, and Przemyslaw
Musialski. Layoutenhancer: Generating good indoor layouts
from imperfect data. 2022. 1, 3

[16] Manyi Li, Akshay Gadi Patil, Kai Xu, Siddhartha Chaudhuri,
Owais Khan, Ariel Shamir, Changhe Tu, Baoquan Chen,
Daniel Cohen-Or, and Hao Zhang. Grains: Generative recursive autoencoders for indoor scenes. 2018. 1, 2

[17] Wenbin Li, Sajad Saeedi, John McCormac, Ronald Clark,
Dimos Tzoumanikas, Qing Ye, Yuzhong Huang, Rui Tang,



and Stefan Leutenegger. Interiornet: Mega-scale multisensor photo-realistic indoor scenes dataset. _arXiv preprint_
_arXiv:1809.00716_, 2018. 2

[18] Chenguo Lin and Yadong Mu. Instructscene: Instructiondriven 3d indoor scene synthesis with semantic graph prior.
_arXiv preprint arXiv:2402.04717_, 2024. 1, 2, 3, 5, 6, 7, 8

[19] Xiaolei Lv, Shengchu Zhao, Xinyang Yu, and Binqiang
Zhao. Residential floor plan recognition and reconstruction.
In _Proceedings of the IEEE/CVF conference on computer vi-_
_sion and pattern recognition_, pages 16717–16726, 2021. 3,
4

[20] Paul C. Merrell, Eric Schkufza, Zeyang Li, Maneesh
Agrawala, and V. Koltun. Interactive furniture layout using
interior design guidelines. _ACM SIGGRAPH 2011 papers_,
2011. 1, 2

[21] B Mildenhall, PP Srinivasan, M Tancik, JT Barron, R Ramamoorthi, and R Ng. Nerf: Representing scenes as neural
radiance fields for view synthesis. In _European conference_
_on computer vision_, 2020. 1

[22] Wenjie Min, Wenming Wu, Gaofeng Zhang, and Liping
Zheng. Funcscene: Function-centric indoor scene synthesis
via a variational autoencoder framework. _Computer Aided_
_Geometric Design_, 111, 2024. 1, 2

[23] Despoina Paschalidou, Amlan Kar, Maria Shugrina, Karsten
Kreis, Andreas Geiger, and Sanja Fidler. Atiss: Autoregressive transformers for indoor scene synthesis. 2021. 1, 2, 3,
5, 6

[24] Siyuan Qi, Yixin Zhu, Siyuan Huang, Chenfanfu Jiang, and
Song Chun Zhu. Human-centric indoor scene synthesis using stochastic grammar. In _2018 IEEE/CVF Conference on_
_Computer Vision and Pattern Recognition_, 2018. 1, 2

[25] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya
Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry,
Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning
transferable visual models from natural language supervision. In _International conference on machine learning_, pages
8748–8763. PMLR, 2021. 11

[26] Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu,
and Mark Chen. Hierarchical text-conditional image generation with clip latents. _arXiv preprint arXiv:2204.06125_, 1
(2):3, 2022. 4

[27] Daniel Ritchie, Kai Wang, and Yu An Lin. Fast and flexible indoor scene synthesis via deep convolutional generative
models. _IEEE_, 2019. 1, 2, 5, 6

[28] Robin Rombach, Andreas Blattmann, Dominik Lorenz,
Patrick Esser, and Bj¨orn Ommer. High-resolution image
synthesis with latent diffusion models. In _Proceedings of_
_the IEEE/CVF conference on computer vision and pattern_
_recognition_, pages 10684–10695, 2022. 3

[29] Chitwan Saharia, William Chan, Huiwen Chang, Chris Lee,
Jonathan Ho, Tim Salimans, David Fleet, and Mohammad
Norouzi. Palette: Image-to-image diffusion models. In
_ACM SIGGRAPH 2022 conference proceedings_, pages 1–10,
2022. 3

[30] Chitwan Saharia, William Chan, Saurabh Saxena,
Lala Li, Jay Whang, Emily Denton, Seyed Kamyar
Seyed Ghasemipour, Burcu Karagol Ayan, S. Sara Mahdavi,



9


Raphael Gontijo Lopes, Tim Salimans, Jonathan Ho, David
Fleet, and Mohammad Norouzi. Imagen: Text-to-image
diffusion models. _arXiv preprint arXiv:2205.11487_, 2022. 4

[31] Shuran Song, Fisher Yu, Andy Zeng, Angel X. Chang, and
Thomas Funkhouser. Semantic scene completion from a single depth image. In _2017 IEEE Conference on Computer_
_Vision and Pattern Recognition (CVPR)_, 2017. 2

[32] Jiapeng Tang, Yinyu Nie, Lev Markhasin, Angela Dai, Justus
Thies, and Matthias Nießner. Diffuscene: Denoising diffusion models for generative indoor scene synthesis. In _Pro-_
_ceedings of the IEEE/CVF conference on computer vision_
_and pattern recognition_, pages 20507–20518, 2024. 1, 2, 3,
5, 6, 7, 8

[33] A Vaswani. Attention is all you need. _Advances in Neural_
_Information Processing Systems_, 2017. 11

[34] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Lukasz Kaiser, and Illia
Polosukhin. Attention is all you need. _arXiv_, 2017. 1, 3

[35] Kai Wang, Yu An Lin, Ben Weissmann, Manolis Savva, and
Daniel Ritchie. Planit: planning and instantiating indoor
scenes with relation graph and spatial prior networks. _ACM_
_Transactions on Graphics_, 38(4):1–15, 2019. 1, 2

[36] Xinpeng Wang, Chandan Yeshwanth, and Matthias Niener.
Sceneformer: Indoor scene generation with transformers.
2020. 1, 3

[37] Yufei Wang, Zhou Xian, Feng Chen, Tsun-Hsuan Wang,
Yian Wang, Katerina Fragkiadaki, Zackory Erickson, David
Held, and Chuang Gan. Robogen: Towards unleashing infinite data for automated robot learning via generative simulation, 2023. 1, 5

[38] Abdelrhman Werby, Chenguang Huang, Martin B¨uchner,
Abhinav Valada, and Wolfram Burgard. Hierarchical OpenVocabulary 3D Scene Graphs for Language-Grounded Robot
Navigation. In _Proceedings of Robotics: Science and Sys-_
_tems_, Delft, Netherlands, 2024. 4

[39] Jianxiong Xiao, Andrew Owens, and Antonio Torralba.
Sun3d: A database of big spaces reconstructed using sfm
and object labels. In _Proceedings of the IEEE international_
_conference on computer vision_, pages 1625–1632, 2013. 2

[40] Ken Xu, James Stewart, and Eugene Fiume. Constraintbased automatic placement for scene composition. _Proceed-_
_ings - Graphics Interface_, pages 25–34, 2002. 1, 2

[41] Yue Yang, Fan-Yun Sun, Luca Weihs, Eli VanderBilt, Alvaro Herrasti, Winson Han, Jiajun Wu, Nick Haber, Ranjay
Krishna, Lingjie Liu, Chris Callison-Burch, Mark Yatskar,
Aniruddha Kembhavi, and Christopher Clark. Holodeck:
Language guided generation of 3d embodied ai environments. _arXiv preprint arXiv:2312.09067_, 2023. 1, 2, 5

[42] Yandan Yang, Baoxiong Jia, Peiyuan Zhi, and Siyuan
Huang. Physcene: Physically interactable 3d scene synthesis for embodied ai. In _Proceedings of the IEEE/CVF Con-_
_ference on Computer Vision and Pattern Recognition_, pages
16262–16272, 2024. 3, 4, 6, 7

[43] Zhihan Yao, Yuhang Chen, Jiahao Cui, Shoulong Zhang,
Shuai Li, and Aimin Hao. Conditional room layout generation based on graph neural networks. _Computers & Graph-_
_ics_, page 103971, 2024. 1, 2




[44] Lap Fai Yu, Sai Kit Yeung, Chi Keung Tang, Demetri Terzopoulos, Tony F. Chan, and Stanley J. Osher. Make it home:
automatic optimization of furniture arrangement. In _Inter-_
_national Conference on Computer Graphics and Interactive_
_Techniques_, 2011. 1, 2

[45] Guangyao Zhai, Evin Pinar ¨Ornek, Shun-Cheng Wu,
Yan Di, Federico Tombari, Nassir Navab, and Benjamin
Busam. Commonscenes: Generating commonsense 3d indoor scenes with scene graph diffusion. _arXiv preprint_
_arXiv:2305.16283_, 2023. 4

[46] Zaiwei Zhang, Zhenpei Yang, Chongyang Ma, Linjie Luo,
and Qixing Huang. Deep generative modeling for scene synthesis via hybrid representations. 2018. 1, 2, 5, 6

[47] Jia Zheng, Junfei Zhang, Jing Li, Rui Tang, Shenghua Gao,
and Zihan Zhou. Structured3d: A large photo-realistic
dataset for structured 3d modeling. In _Computer Vision–_
_ECCV 2020: 16th European Conference, Glasgow, UK, Au-_
_gust 23–28, 2020, Proceedings, Part IX 16_, pages 519–535.
Springer, 2020. 2



10


### **CHOrD: Generation of Collision-Free, House-Scale, and Organized Digital** **Twins for 3D Indoor Scenes with Controllable Floor Plans and Optimal Layouts** Supplementary Materials



**A. Additional CHOrD Technical Details**


**A.1. CHOrD Inference Efficiency**


On a single RTX 8000 GPU, the diffusion model inference
takes approximately 18 seconds (this can be potentially reduced with advanced diffusion solvers); YOLO object detection takes around 40 milliseconds; 3D model matching
and scene construction take about 100 milliseconds; and
rendering, performed using the UE engine, takes approximately 30 seconds for a 2K image and around 120 seconds for a 4K image. While rendering is the most timeconsuming module, it is an independent component that
can be flexibly replaced with any real-time rasterizationbased renderer when efficiency is a priority. We chose a
ray-tracing-based renderer for photorealistic quality.


**A.2. Text-conditioned floor planning**


As discussed in Section 3.3, text conditioning serves as a
viable alternative for layout generation when floor plans images are not available. We use a text-conditioned diffusion
model for this purpose, as illustrated in Figure 9. We generate a fixed-size conditioning vector _**y**_ _**c**_ by passing the text
input through a CLIP encoder [25]. Semi-structured text is
particularly effective for this task ( _e.g._, “This is a 40-squaremeter flat with 0 living rooms, 1 bedroom, 0 kitchens, and
1 bathroom.”). The resulting CLIP embedding serves as
the conditional variable for the diffusion model, guiding the
generation of scene layouts based on high-level semantic
information encoded in the text description. This allows for
more intuitive control over the layout generation by leveraging natural language as an additional input modality. The
text-based model is trained using the same loss as Equation 1, with the conditioning variable being the CLIP embedding _**y**_ _**c**_ instead of the floor plan image _**y**_ . Conditioning
is introduced through a cross-attention layer [33] near the
UNet bottleneck.


**A.3. Open-plan-conditioned floor planning**


As illustrated in Figure 10, the open-plan-conditioned diffusion model shares the same architecture as the floor planconditioned diffusion model detailed in Section 3.1, except
that this model takes an open-plan figure as input and generates a structured floor plan with optimal room arrangements. The generated floor plan can then serve as input to
the floor plan-conditioned diffusion model. In other words,
open-plan-conditioned floor planning functions as an optional preprocessing step before the CHOrD main pipeline.



|Category|Color|Category|Color|
|---|---|---|---|
|Bed|FF0000|Cabinet|FFFF00|
|Bed Background|FF3333|Bedside Table|F08080|
|Table|A52A2A|Leisure Sofa|666600|
|Sofa|FF9933|TV Cabinet|FFCC99|
|Sofa Background|99004C|Coffea Table|CCFF99|
|Dining Cabinet|FF9999|Shoe Cabinet|006633|
|Single Sofa|CC6600|Dining Table|FF6666|
|Side Coffea Table|99FFCC|Single Door Floor Cabinet|9999FF|
|Double Door Floor Cabinet|6666FF|Cooker Cabinet|000099|
|Sink Cabinet|0000CC|Electrical FLoor Cabinet|3333FF|
|Refrigerator|006666|Shower|33FF99|
|Toilet|660033|Washbasin|CC0066|
|Washing Machine|FFCCE5|Washing Set|FF66B2|
|Wall|000000|Door|139C5A|
|Window|0000FF|||


Table 2. Scene layout items and corresponding color schemes,
with the opacity level set to 0.3.



Figure 10. Open-plan-conditioned diffusion model.


**B. Additional CHOrD Dataset Details**


An example CHOrD data stored in JSON format is shown
in List 1. A comprehensive statistic of the CHOrD dataset
in comparison with 3D-FRONT is detailed in Table 5, 6, 7,
and Figure 11.


Listing 1. Example JSON data format


_{_



Input



Text conditioned diffusion







Input



Figure 9. Text-conditioned diffusion model.


Load-bearing walls conditioned diffusion


Diffusion









11


|Category|Color|Category|Color|
|---|---|---|---|
|Bedside Table|F08080|Table|A52A2A|
|Coffea Table|CCFF99|Side Coffea Table|99FFCC|
|Dining Table|FF6666|Lying Book|0000FF|
|Standing Book|FFFFAA|Magazine|7FFFAA|
|All-in-one Computer|00FFAA|Laptop|FF7FAA|
|Big Mouse Pad|7F7FAA|Table Lamp|007FAA|
|Small Ornament|FF00AA|Pen Holder|7F00AA|
|Big Plant|0000AA|Small Plant|FFFF55|
|Coffee Cup|7FFF55|Electronic|FF0000|
|Photo Frame|FF7F55|Food|7F7F55|
|Dinner Set|FFFF00|Drinks|7F7F00|


Table 3. Fine-grained items and corresponding color schemes.


” rooms ” : [
_{_
” roomId ” : ”D5F19A0446724E ”,
”roomName ” : ” l i v i n g ”, # i n n e r room
”roomType ” : 1,
” w a l l P o i n t s ” : [

[171.65, 2 4 1 . 5 ],

[651.66, 2 4 1 . 5 ],
. . . ] # 2d coords
_}_,
_{_
” roomId ” : ”D5F19A044672 ”,
”roomName ” : ” out room ”,
”roomType ” : 0,
” w a l l P o i n t s ” : [

[171.65, 2 4 1 . 5 ],

[651.66, 2 4 1 . 5 ],
. . . ] # 2d coords
_}_ ],
” windowsDoors ” : [
_{_
” type ” : ” door ”,
” pos ” : [717.32, 737.0, 0],
# box c e n t e r p o s i t i o n x, y ;
# h e i g h t to f l o o r z
” l e n g t h ” : 95,
” width ” : 12,
” h e i g h t ” : 210,
” r o t a t e ” : 100

# r o a t e angle in degree
_}_,
_{_
” type ” : ”window ”,
” pos ” : [657.66, 945.12, 90],
” l e n g t h ” : 153.75,
” width ” : 12,
” h e i g h t ” : 110,
” r o t a t e ” : 90.0


12



_}_
],
” f u r n i t u r e ” : [
# 3d bounding box data,
# same with windows and doors
_{_
” type ” : ” c o f f e e t a b l e ”,
” pos ” : [569.91, 1844.75, 0],
” l e n g t h ” : 76.0,
” width ” : 94.0,
” h e i g h t ” : 99,
” r o t a t e ” : 180.0
_}_,
_{_
” type ” : ” sofa ”,
” pos ” : [411.66, 169.45, 0],
” l e n g t h ” : 185.3,
” width ” : 120.1,
” h e i g h t ” : 99,
” r o t a t e ” : 0.0
_}_
]
_}_


**C. Additional Results**


We present additional qualitative results for fine-grained
layout synthesis in Figure 12, text-conditioned floor planning in Figure 13, open-plan-conditioned floor planning
in Figure 14, and photorealistic rendering of floor planconditioned layout synthesis in Figure 17.
In rare instances, YOLOv8 struggled to detect accurate
bounding boxes, resulting in misaligned objects or minor
collisions, even though the layout images were axis-aligned
and collision-free, as shown in Figure 15. We demonstrated
that this can be straightforwardly addressed with more training data. Specifically, we trained CHOrD on a privately
collected dataset of over 100,000 indoor scenes, achieving significantly better results ( **FID** 17.76, **KID** 0.02, **POR**
0.005, **PIoU** 4 _._ 399 _×_ 10 _[−]_ [5] ) with substantially fewer failure cases compared to the results obtained from training on
the CHOrD dataset (9,706 scenes) and reported in Table 1.
CHOrD also performs considerably better when trained on
CHOrD dataset compared to 3D-FRONT, as illustrated in
Figure 16. These results evidence the strong scalability of
CHOrD.


|Item|Category|
|---|---|
|Nightstand|bedside table|
|Wardrobe|cabinet|
|Three-Seat / Multi-seat Sofa|sofa|
|Dining Table|dining table|
|Coffee Table|coffee table|
|Loveseat Sofa|sofa|
|Children Cabinet|cabinet|
|Drawer Chest / Corner cabinet|cabinet|
|King-size Bed|bed|
|TV Stand|tv cabinet|
|Sideboard / Side Cabinet / Console|dining cabinet|
|Lazy Sofa|leisure~~ s~~ofa|
|Dressing Table|table|
|Wine Cabinet|dining cabinet|
|L-shaped Sofa|sofa|
|Corner/Side Table|side coffee table|
|Bookcase / jewelry Armoire|cabinet|
|Kids Bed|bed|
|Sideboard / Side Cabinet / Console Table|table|
|Bed Frame|bed|
|Shoe Cabinet|shoe cabinet|
|Three-Seat / Multi-person sofa|sofa|
|Double Bed|bed|
|Bunk Bed|bed|
|Desk|table|
|Two-seat Sofa|sofa|
|Tea Table|coffee table|
|Couch Bed<br>|bed<br>|
|Single bed<br>Chaise Longue Sofa|bed<br>sofa|
|U-shaped Sofa|sofa|


Table 4. 3D-FRONT furniture items and remapped categories.


|Col1|Col2|Col3|ONT<br>dataset|
|---|---|---|---|
|||||
|||||
|||||
|||||
|||||
|||||
|||||
||3D-FR<br>CHOrD|3D-FR<br>CHOrD|ONT<br>dataset|
|||||


|Col1|Col2|Col3|Col4|Col5|Col6|-FRONT<br>rD dataset|
|---|---|---|---|---|---|---|
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||||
||||||3D<br>CHO|3D<br>CHO|
||||||||
||||||||
||||||||
||||||||



0 200 400 600 800 1 _,_ 000 1 _,_ 200


Occurence


(b) Distribution of room counts per house, with an average of 9.78 and
a total of 94,964 counts.


Figure 11. Statistics of the CHOrD dataset in comparison with
3D-FRONT.



Bed

Cabinet
Bed Background


Bedside Table


Table

Leisure Sofa


Sofa

TV Cabinet
Sofa Background


Coffee Table
Dining Cabinet


Shoe Cabinet

Single Sofa
Dining Table

Side Coffee Table
Single Door Cabinet

Double Door Cabinet


Cooker Cabinet


Sink Cabinet

Electrical FLoor Cabinet

Refrigerator


Shower


Toilet

Washbasin
Washing Machine

Washing Set





28


23


21


19


17


15


13


11


9


7


5


3


1



0 10 _,_ 000 20 _,_ 000


Occurence


(a) Distribution of household item occurrences per
super-category.



13


Room Furniture 3D-FRONT CHOrD dataset (ours)


Bedroom Bed 10620 24354

Cabinet 17649 19365
Bed Background 0 16619
Bedside Table 14333 10439

Table 8318 9359


Living Room Leisure Sofa 237 8953
Sofa 6564 8430

TV Cabinet 6821 7935
Sofa Background 0 7019
Coffee Table 6565 7005
Dining Cabinet 1169 5368
Shoe Cabinet 0 4817
Single Sofa 0 3939
Dining Table 5822 3444
Side Coffee Table 6300 4195


Kitchen Single Door Cabinet 0 15889
Double Door Cabinet 0 14156

Cooker Cabinet 0 6904

Sink Cabinet 0 6773

Electrical Cabinet 0 2081
Refrigerator 0 1307


Bathroom Shower 0 15174

Toilet 0 15026

Washbasin 0 12517
Washing Machine 0 970


Balcony Washing Machine Cabinet 0 4153


Table 5. Comparison of furniture occurrences between 3DFRONT and CHOrD dataset.


Empty Room Rate POR PIoU


3D-FRONT 0.5906 0.0361 0.2547

CHOrD dataset (ours) 0.2902 0.0044 0.0018


Table 6. Comparison of data quality statistics between 3D-FRONT
and CHOrD dataset.



Figure 12. Fine-grained layout synthesis.



The area of the house is 75

square meters. The house has
1 living room 3 bedroom 1
kitchen 1 bathroom.



The area of the house is 105

square meters. The house has
1 living room 3 bedroom 1
kitchen 1 bathroom.



The area of the house is 160

square meters. The house has
1 living room 3 bedroom 1
kitchen 2 bathroom.



The area of the house is 160

square meters. The house has
1 living room 4 bedroom 1
kitchen 2 bathroom.



Living Bedroom Kitchen Bathroom Balcony


3D-FRONT 1813 4041 0 0 0

CHOrD dataset (ours) 15115 40983 8262 16351 8262


Table 7. Comparison of non-empty room statistics between 3DFRONT and CHOrD dataset.


14



Figure 13. Visualization of text-to-layout generation by CHOrD
trained on our CHOrD dataset. Floor plans of different room sizes
all fill the entire canvas, with the wall thickness set to 24 cm for all
scenes. Hence, the room size can be inferred from the thickness of
the gray walls, which is consistent with the raw training data.


Condition Real Prediction Prediction


Figure 14. Open-plan-conditioned floor planning.


Unet output Unet output Unet output



3D-FRONT


CHOrD dataset


Figure 16. Performance of CHOrD on 3D-FRONT and CHOrD
dataset, where results obtained from training on 3D-FRONT exhibit implausible unfurnished rooms due to artifacts in the original
database.



Kitchen cabinet detec
tion errors



Bed and table detec
tion errors



Kitchen cabinet detec
tion errors



Figure 15. Sporadic failure cases due to YOLO detection errors
when trained with insufficient data.



15


Figure 17. Additional photorealistic rendering of diverse synthesized layouts by CHOrD conditioned on floor plans.



16


