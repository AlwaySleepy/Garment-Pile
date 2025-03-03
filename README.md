# Point-Level Visual Affordance Guided Retrieval and Adaptation for Cluttered Garments Manipulation
[[Project page]](https://garmentpile.github.io/)
<!-- | [[Paper]](https://arxiv.org/pdf/2501.00879) | [[Video]](https://www.youtube.com/watch?v=IiOBj3ww-qA) -->

[Ruihai Wu*](https://warshallrho.github.io/), [Ziyu Zhu*](https://alwaysleepy.github.io/), Yuran Wang*, [Yue Chen](https://github.com/Cold114514), Jiarui Wang, [Hao Dong](https://zsdonghao.github.io/)

Peking University

*CVPR 2025*

<img src="Repo_Image/Teaser.jpg" alt="teaser" width="80%"/>

## Structure of the Repository
```
# training and evaluation
/data_collection         # The data collection pipeline
/train                   # The code for training affordance
/eval                    # The code for evaluation in different scenarios
/Model                   # The code for model implementation and checkpoints

# garment pile simulation (Isaac Sim)
/Camera                  # Implementation for camera
/Garment                 # Implementation for garments
/Robot                   # Implementation for robot
/Room                    # Implementation for room
/Wash_Machine            # Implementation for washing machine
```

## Developer Guidance

For developers, please install pre-commit hooks:

```shell
pip install pre-commit
pre-commit install
```

And do install the [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) vscode extension.

The .vscode/settings.json is configured aligning with the pre-commit hooks. Whenever you save the file, it will be formatted automatically.

## Installation

To reproduce our simulation results, install our conda environment on a Linux machine with Nvidia GPU.

1. Install Isaac Sim

   Download Isaac Sim 2023.1.1. You can refer to the [official guideline](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html) and [Isaac Sim Forum](https://docs.omniverse.nvidia.com/isaacsim/latest/overview.html) to download it.

2. Clone this repo

    ```
    git clone https://github.com/AlwaySleepy/Garment-Pile.git
    ```

3. Download 'Garment' Assets

    Please refer to [Google_Drive_link](https://drive.google.com/drive/folders/1EWH9zYQfBa96Z4JyimvUSBYOyW615JSg) to download **Garment** folder and unzip it to 'Assets/'.

4. Install environment for PointNet++: (to do)

## Data Collection
Run the following command to generate retrieval data:
```
data_collection/retrieve_collect.sh
```
Run the following command to generate stir data:
```
data_collection/stir_collect.sh
```
Change the path of Isaac Sim to your own local path in all the shell files. <br>
Data will be stored in /data/retrieval or /data/stir in .npz form.


## Training
### Offline Training

### Finetune




## Evaluation
Run the following command to evaluate provided model.
```
/home/user/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh eval/washmachine.py
```
Change the path of Isaac Sim to your own local path.





## Citation and Reference

If you find this paper useful, please consider staring 🌟 this repo and citing 📑 our paper:

```
@InProceedings{Wu_2025_CVPR,
      author    = {Wu, Ruihai and Zhu, Ziyu and Wang, Yuran and Chen, Yue and Wang, Jiarui and Dong, Hao},
      title     = {Point-Level Visual Affordance Guided Retrieval and Adaptation for Cluttered Garments Manipulation},
      booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
      year      = {2025},
  }
```
