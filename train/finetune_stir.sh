flag=true


for i in {0..1000}
do

    /home/user/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh data_collection/washingmachine_stir.py
    file_count=$(find "data/stir" -maxdepth 1 -type f | wc -l)

    # 检查文件数量是否大于等于 32
    
    if [ "$file_count" -ge 32 ]; then
     
                if [ "$flag" = false ]; then
                    DISPLAY=: /home/user/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh train/finetune_stir_place.py
                    flag=true
                else
                    DISPLAY=: /home/user/.local/share/ov/pkg/isaac-sim-2023.1.1/python.sh train/finetune_stir_pick.py
                    flag=false
            
        fi
    fi

    sleep 5

done
~       