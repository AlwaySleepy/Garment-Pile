random_flag=True  # define whether to use random stir (random pick random place) or random pick model place
model_path=None    # if random pick model place, define the model path
rgb_flag=False      # define whether to collect rgb image

for i in {0..1000}
do

    ~/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh data_collection/washmachine_stir.py $random_flag $model_path $rgb_flag
    file_count=$(find "Data/WashMachine/Stir_Random/point_cloud" -maxdepth 1 -type f | wc -l)

    # when the number of files in the folder reaches 32, start finetuning

    if [ "$file_count" -ge 32 ]; then

        DISPLAY=: ~/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh train/finetune_stir_place.py
        flag=true

    fi

    sleep 5

done
~
