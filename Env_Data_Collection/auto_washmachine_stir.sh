#!/bin/bash


random_flag=True  # define whether to use random stir (random pick random place) or random pick model place
model_path=None    # if random pick model place, define the model path
rgb_flag=False      # define whether to collect rgb image

collect_epoch=5  # define the number of epochs to collect data


if [ "$random_flag" = "True" ]; then
    TARGET_DIR="Data/WashMachine/Stir_Random"
else
    TARGET_DIR="Data/WashMachine/Stir_Model"
fi


if [ ! -d "$TARGET_DIR" ]; then
    echo "目标文件夹不存在，正在创建..."
    mkdir -p "$TARGET_DIR/point_cloud"
    mkdir -p "$TARGET_DIR/rgb"
    mkdir -p "$TARGET_DIR/point_cloud_after_stir"
    mkdir -p "$TARGET_DIR/rgb_after_stir"
    touch "$TARGET_DIR/Record.txt"
    echo "创建完成：$TARGET_DIR 及其子文件夹"
fi

for ((i=0; i<collect_epoch; i++))
do
    ~/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh Env_Data_Collection/washmachine_stir.py $random_flag $model_path $rgb_flag
    sleep 5
done
