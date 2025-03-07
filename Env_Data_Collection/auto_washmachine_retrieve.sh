#!/bin/bash


random_flag=False   # define whether to use random stir (random pick random place) or random pick model place
model_path=Env_Config/Model/wm_retrieve_model_finetuned.pth   # if random pick model place, define the model path
rgb_flag=False    # define whether to collect rgb image
gif_flag=False    # define whether to collect gif image

collect_epoch=500  # define the number of epochs to collect data


TARGET_DIR="Data/WashMachine/Retrieve"


if [ ! -d "$TARGET_DIR" ]; then
    echo "目标文件夹不存在，正在创建..."
    mkdir -p "$TARGET_DIR/point_cloud"
    mkdir -p "$TARGET_DIR/rgb"
    mkdir -p "$TARGET_DIR/gif"
    touch "$TARGET_DIR/Record.txt"
    echo "创建完成：$TARGET_DIR 及其子文件夹"
fi

for ((i=0; i<collect_epoch; i++))
do
    ~/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh Env_Data_Collection/washmachine_retrieve.py $random_flag $model_path $rgb_flag $gif_flag

    sleep 5
done
