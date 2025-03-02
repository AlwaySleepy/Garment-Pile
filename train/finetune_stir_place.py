import glob
import os
import torch
import random
import numpy as np
import open3d
from plyfile import PlyData, PlyElement
from Model.pointnet2_Place_Model import Place_Model, Place_Model_Loss
from tqdm import tqdm
from torchnet import meter
import shutil

def write_ply(points, filename, text=True):
    """ input: Nx3, write points to filename as PLY format. """
    points = [(points[i,0], points[i,1], points[i,2]) for i in range(points.shape[0])]
    vertex = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'),('z', 'f4')])
    el =PlyElement.describe(vertex, 'vertex', comments=['vertices'])
    PlyData([el], text=text).write(filename)
    print(f"write to {filename}")

def get_unique_filename(base_filename, extension=".png"):
    counter = 0
    filename = f"{base_filename}_{counter}{extension}"
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_filename}_{counter}{extension}"
        
    # if counter==0:
    #     filename=f"{base_filename}_0{extension}"
       
    return filename


# stir_train is for all the training stir data, stir is for new online finetune data
def sample_origin_data(
        sample_pc_dir="data/stir_train", 
        put_data_dir="data/stir", 
    ):
 
    sample_num = len(os.listdir(put_data_dir))

    npz_path = [os.path.join(sample_pc_dir, npz) for npz in os.listdir(sample_pc_dir)] 

    npz = sorted(npz_path, key = lambda x : int(x.split(".")[-2].split("_")[-1]))

    # record = np.loadtxt(sample_record_address).astype(np.float32)
    
    random_num = random.sample(range(len(npz)), sample_num)

    print(len(random_num), random_num)

    for i in random_num:


        file_name = get_unique_filename(put_data_dir + "/data", ".npz")

        print(file_name)


        shutil.copy(npz[i], file_name)



if __name__ == "__main__":
    #---------------------check file---------------------#





        print("\033[33m" + 
"""
________  _______   ________  ___  ________           ________ ___  ________   ___  ___  _________  ___  ___  ________   _______          
|\   __  \|\  ___ \ |\   ____\|\  \|\   ___  \        |\  _____\\  \|\   ___  \|\  \|\  \|\___   ___\\  \|\  \|\   ___  \|\  ___ \         
\ \  \|\ /\ \   __/|\ \  \___|\ \  \ \  \\ \  \       \ \  \__/\ \  \ \  \\ \  \ \  \\\  \|___ \  \_\ \  \\\  \ \  \\ \  \ \   __/|        
\ \   __  \ \  \_|/_\ \  \  __\ \  \ \  \\ \  \       \ \   __\\ \  \ \  \\ \  \ \  \\\  \   \ \  \ \ \  \\\  \ \  \\ \  \ \  \_|/__      
\ \  \|\  \ \  \_|\ \ \  \|\  \ \  \ \  \\ \  \       \ \  \_| \ \  \ \  \\ \  \ \  \\\  \   \ \  \ \ \  \\\  \ \  \\ \  \ \  \_|\ \     
\ \_______\ \_______\ \_______\ \__\ \__\\ \__\       \ \__\   \ \__\ \__\\ \__\ \_______\   \ \__\ \ \_______\ \__\\ \__\ \_______\       
                                                                                                                                        
                                                                                                                                        
                                                                                                                                        
""" 
        + "\033[0m")
        print("place model begin to finetune\n")


        # ----------------------------- save original data -----------------------------
        dir = get_unique_filename("data/store_finetune_data/data", "")

        os.makedirs(dir, exist_ok=True)

        shutil.copytree("data/stir", dir + "/pointcloud")

        # shutil.copy2("data/stir.txt", dir)

        # ----------------------------- process data -----------------------------

        # 读取原始文件
        # output_file = 'data/stir.txt'  # 输入文件路径
        # output_file = 'data/Record_process.txt'  # 输出文件路径

        # with open(input_file, 'r') as file:
        #     lines = file.readlines()

        # # 处理每一行数据，去除第四列
        # with open(output_file, 'w') as file:
        #     for line in lines:
        #         columns = line.split()
        #         # 保留第1到第3列和第5列
        #         new_line = f"{columns[0]} {columns[1]} {columns[2]} {columns[4]}\n"
        #         file.write(new_line)

        # print(f"处理后的数据已保存到 {output_file}")

        # # ----------------------------- calculate accuracy -----------------------------

        stir_folder = "data/stir"

        # 获取所有 .npz 文件路径
        npz_files = glob.glob(os.path.join(stir_folder, "*.npz"))

        success_count = 0
        total_count = 0

        for file in npz_files:
            data = np.load(file)  # 加载 .npz 文件

            if "flag" in data:  # 确保文件中有 flag
                flag = data["flag"]

                success_count += (flag == 1)  # 单个值情况
                total_count += 1

        # 计算成功率
        accuracy = success_count / total_count if total_count > 0 else 0


        with open('data/Record_Model_Accuracy.txt', 'a') as file:
                
                new_line = f"Success: {success_count} Total: {total_count} Pick Model Accuracy: {accuracy}\n"
    
                file.write(new_line)

        # ----------------------------- sample data -----------------------------

        sample_origin_data()

        # ----------------------------- load data -----------------------------

        point_cloud_dir = "data/stir"

        record_dir = "data/stir.txt"

        ply_path = [os.path.join(point_cloud_dir, ply) for ply in os.listdir(point_cloud_dir)] 

        ply = sorted(ply_path, key = lambda x : int(x.split(".")[-2].split("_")[-1]))


        data_arrays_pick = []

        data_arrays_place=[]

        label_arrays = []

        for i in range(len(ply)):

            data=np.load(ply[i])
            pc_np_pick=data["point_cloud"]
            if not isinstance(pc_np_pick, np.ndarray):
                pc_np_pick = np.array(pc_np_pick)


            pc_np_pick[0] = data["pick"]

            data_arrays_pick.append(pc_np_pick)

            pc_np_place=data["point_cloud"]
            if not isinstance(pc_np_place, np.ndarray):
                pc_np_place = np.array(pc_np_place)

            pc_np_place[0] = data["place"]

            data_arrays_place.append(pc_np_place)

            label_arrays.append(data["flag"])
        
        data_pick = np.stack(data_arrays_pick, axis=0)

        data_place = np.stack(data_arrays_place, axis=0)


        label = np.stack(label_arrays, axis=0)

        print(data_pick.shape, label.shape)

        # ----------------------------- train data -----------------------------

        model = Place_Model(normal_channel=False).cuda()
        model.load_state_dict(torch.load("Model/finetune_model_place.pth"))
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        model.train()
        criterion = Place_Model_Loss().cuda()
        optimizer = torch.optim.Adam(
            model.parameters(), 
            lr=0.0008,
            betas=(0.9, 0.999),
            eps=1e-08,
            weight_decay=1e-4
        )
        for epoch in range(5):
            if isinstance(data_pick, np.ndarray):
                data_pick = torch.tensor(data_pick, dtype=torch.float32)
            else:
                data_pick = data_pick.clone().detach().float()
            if isinstance(data_place, np.ndarray):
                data_place = torch.tensor(data_place, dtype=torch.float32)
            else:
                data_place = data_place.clone().detach().float()
            if isinstance(label, np.ndarray):
                label = torch.tensor(label, dtype=torch.float32)
            else:
                label = label.clone().detach().float()

            data_pick,data_place, label = data_pick.to(device),data_place.to(device), label.to(device)
            model.zero_grad()
            output = model(data_pick.transpose(2,1),data_place.transpose(2,1))
            loss = criterion(output, label)
            loss.backward()
            optimizer.step()

            stir_output = output[:, 0, :]
            prediction = (stir_output >= 0.5).float()
            correct = (prediction==label).sum().item()
            total = label.size(0)
            accuracy = correct / total

            print(f"epoch: {epoch}, loss: {loss.item()}, accuracy: {accuracy}")

            with open('data/Record_Model_Accuracy.txt', 'a') as file:
                    
                    new_line = f"epoch: {epoch}, loss: {loss.item()}, accuracy: {accuracy}\n"        
                    file.write(new_line)


        torch.save(model.state_dict(), "Model/finetune_model_place.pth")
        if not os.path.exists("Model/saved_place_model_pth"):
            os.makedirs("Model/saved_place_model_pth")
        torch.save(model.state_dict(), get_unique_filename("Model/saved_place_model_pth/finetune_model", ".pth"))

        with open('data/Record_Model_Accuracy.txt', 'a') as file:
                new_line = f"\n"        
                file.write(new_line)

        # # ----------------------------- reset data -----------------------------

        # # filename=get_unique_filename(base_filename="data/stir_past",extension="")
        # # shutil.move("data/stir", filename)
        # shutil.rmtree("data/stir")

        # os.makedirs("data/stir", exist_ok=True) 


#     else:

#         print("\033[31m" + 
# """
#  ________  ________  ________   _________  ___  ________   ___  ___  _______      
# |\   ____\|\   __  \|\   ___  \|\___   ___\\  \|\   ___  \|\  \|\  \|\  ___ \     
# \ \  \___|\ \  \|\  \ \  \\ \  \|___ \  \_\ \  \ \  \\ \  \ \  \\\  \ \   __/|    
#  \ \  \    \ \  \\\  \ \  \\ \  \   \ \  \ \ \  \ \  \\ \  \ \  \\\  \ \  \_|/__  
#   \ \  \____\ \  \\\  \ \  \\ \  \   \ \  \ \ \  \ \  \\ \  \ \  \\\  \ \  \_|\ \ 
#    \ \_______\ \_______\ \__\\ \__\   \ \__\ \ \__\ \__\\ \__\ \_______\ \_______\                                                                              
                                                                                
# """ 
#               + "\033[0m")


