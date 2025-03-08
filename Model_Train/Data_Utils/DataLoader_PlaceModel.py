import os
import numpy as np
import sys

sys.path.append("Model_Train")

import open3d
from torch.utils.data import Dataset
from Data_Utils.utils import read_ply, furthest_point_sampling


class DataLoader_PlaceModel(Dataset):
    def __init__(self, mode=None, data_dir: str = "Data/WashMachine/Stir_Random"):

        assert mode in ["train", "test", "val"]
        self.mode = mode

        if self.mode == "train":
            # load dir name
            self.point_cloud_dir = data_dir + "/point_cloud"
            self.record_dir = data_dir + "/Record.txt"
        else:
            # load dir name
            self.point_cloud_dir = data_dir + "/point_cloud"
            self.record_dir = data_dir + "/Record.txt"

        # get ply_filepath
        ply_path = [
            os.path.join(self.point_cloud_dir, ply)
            for ply in os.listdir(self.point_cloud_dir)
        ]
        # sort plt file and get final result
        self.ply = sorted(ply_path, key=lambda x: int(x.split(".")[-2].split("_")[-1]))
        # get ply_file_nums
        self.ply_nums = len(self.ply)
        # get record file content(including pick_point and label)
        self.record = np.loadtxt(self.record_dir, usecols=range(7))
        self.record = self.record.astype(np.float32)
        # get pick_points and labels from record
        self.pick_points = self.record[:, :3]
        self.place_points = self.record[:, 3:6]
        self.labels = self.record[:, 6:7]

    def __getitem__(self, index):
        """
        return:
            - point_cloud_data: sampled (4096)
            - label: 1/0(Success/Failure)
        """
        # get index ply_path
        ply_path = self.ply[index]
        # read np_data from ply
        pc = open3d.io.read_point_cloud(ply_path)
        pick_data = np.asarray(pc.points, dtype=np.float32)
        place_data = np.asarray(pc.points, dtype=np.float32)
        # print(pick_data)
        # push pick_point_position to data
        pick_data[0] = self.pick_points[index]
        place_data[0] = self.place_points[index]
        # get label
        label = self.labels[index]

        return pick_data, place_data, label

    def __len__(self):
        """
        return:
            - the num of point_clouds
        """
        return self.ply_nums
