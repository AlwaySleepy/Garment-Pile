<h2 align="center">
  <b><tt>GarmentPile</tt>: <br>
  Point-Level Visual Affordance Guided Retrieval and Adaptation for Cluttered Garments Manipulation</b>
</h2>

<div align="center" margin-bottom="6em">
<b>CVPR 2025</b>
</div>

<br>

<div align="center">
    <a href="" target="_blank">
    <img src="https://img.shields.io/badge/Paper-arXiv-green" alt="Paper arXiv"></a>
    <a href="https://garmentpile.github.io/" target="_blank">
    <img src="https://img.shields.io/badge/Page-GarmentPile-red" alt="Project Page"/></a>
    <a href="https://github.com/AlwaySleepy/Garment-Pile" target="_blank">
    <img src="https://img.shields.io/badge/Code-Github-blue" alt="Github Code"/></a>
</div>

<br>

![teaser](Repo_Image/Teaser.jpg)

## Get Started

### 1. Install Isaac Sim 2023.1.1
   Our Project is built upon Isaac Sim 2023.1.1. Please refer to the [official guideline](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/download.html) to download it.

   After Download, please move the file into path '/home/XXX/.local/share/ov/pkg/' to adapt the path configuration of the repo.

   There are some modification need to be done in Isaac Sim's meta-file. Please refer to this [document]().

### 2. Repo Preparation

- Clone the repo frist.

```
git clone https://github.com/AlwaySleepy/Garment-Pile.git
```

- Download *Garment* Assets

Here we use *Garment* Assets from GarmentLab. Please refer to [Google_Drive_link](https://drive.google.com/drive/folders/1EWH9zYQfBa96Z4JyimvUSBYOyW615JSg) to download **Garment** folder and unzip it to 'Assets/'.

### 3. Environment Preparation

- **Isaac Sim Env** Preparation

For convenience, we recommend to provide an alias for the python.sh file in Isaac Sim 2023.1.1.
```bash
# 1. open .bashrc file
sudo vim ~/.bashrc

# 2. add following part to the end of the file
alias isaac_pile=/home/XXX[need change]/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh

# 3. save file and exit.

# 4. refresh for file configuration to take effect.
source ~/.bashrc
```

Install necessary packages into Isaac Sim Env.

```bash
isaac_pile -m pip install -e requirements_isaacsim.txt
```

- **Model Training Env** Preparation

create new conda environment

``` bash
conda create -n garmentpile python=3.10
```

Install necessary packages into Model Training Env.

``` bash
conda activate garmentpile

pip install -e requirements_model.txt
```

### 4. Repo Structure Explanation

    📂 ProjectRoot
        # VS Code Configuration Files
    ├── 📁 .vscode
        # Assets used in Isaac Sim
    ├── 📁 Assets
        # Isaac Sim Env Configuration, including Camera, Robot, Garment, etc.
    ├── 📁 Env_Config
        # Used for train_data collection
    ├── 📁 Env_Data_Collection
        # standlone environment with pre-trained model
    ├── 📁 Env_Eval
        # Used for fintuning model
    ├── 📁 Env_Finetune
        # Model training code
    ├── 📁 Model_Train
        # repo images
    ├── 📁 Repo_Image

## StandAlone Env

In our project, we provide three garment-pile scenes: **washingmachine**, **sofa**, **basket**.

You can directly run the three environment based on the file in *'Env_Eval'* folder.

The retrieve, pick, place procedure all rely on pre_trained model.

```bash
# washmachine
isaac_pile Env_Eval/washmachine.py

# sofa
isaac_pile Env_Eval/sofa.py

# basket
isaac_pile Env_Eval/basket.py
```

## Data Collection

Run the following command to generate retrieval data:

```bash
# washmachine
bash Env_Data_Collection/auto_washmachine_retrieve.sh

# sofa
bash Env_Data_Collection/auto_sofa_retrieve.sh

# basket
bash Env_Data_Collection/auto_basket_retrieve.sh
```

Run the following command to generate stir data:

```bash
# washmachine
bash Env_Data_Collection/auto_washmachine_stir.sh

# sofa
bash Env_Data_Collection/auto_sofa_stir.sh

# basket
bash Env_Data_Collection/auto_basket_stir.sh
```

There are some flags you can define manually in .sh file. Please check .sh file for more information. (such as, rgb_flag, random_flag, etc.)

## Model Training

Training Data are all collected in 'Data' file.

```bash
# activate conda env
conda activate garmentpile

# run any .py file in 'Model_Train' folder. remember to login in wandb
# e.g.
python WM_Model_train.py
```

## Finetune

We provide washmachine place model finetune code as example in 'Env_Finetune' folder.

you can run the .sh file directly to see finetune procedure.

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
