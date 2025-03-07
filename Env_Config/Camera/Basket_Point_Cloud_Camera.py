"""
Use Point_Cloud_Camera to generate pointcloud graph

pointcloud graph will be used to get which point to catch
"""

import sys

sys.path.append("Env_Config/")

import numpy as np
import torch
from termcolor import cprint
from Model.pointnet2_Retrieve_Model import Retrieve_Model as Aff_Model
from Model.pointnet2_Place_Model import Place_Model
from Model.pointnet2_Pick_Model import Pick_Model
from omni.isaac.sensor import Camera
from omni.isaac.core.utils.rotations import euler_angles_to_quat
from Utils_Project.utils import (
    get_unique_filename,
    record_success_failure,
    write_ply,
    furthest_point_sampling,
    write_ply_with_colors,
    write_rgb_image,
)
import omni.replicator.core as rep
import random


class Point_Cloud_Camera:
    def __init__(
        self,
        camera_position,
        camera_orientation,
        frequency=20,
        resolution=(640, 480),
        prim_path="/World/point_cloud_camera",
        garment_num: int = 1,
        retrieve_model_path=None,
        place_model_path=None,
        pick_model_path=None,
    ):
        # define camera parameters
        self.camera_position = camera_position
        self.camera_orientation = camera_orientation
        self.frequency = frequency
        self.resolution = resolution
        self.camera_prim_path = prim_path
        # define camera
        self.camera = Camera(
            prim_path=self.camera_prim_path,
            position=self.camera_position,
            orientation=euler_angles_to_quat(self.camera_orientation, degrees=True),
            frequency=self.frequency,
            resolution=self.resolution,
        )
        # self.initialize(garment_num)
        self.retrieve_model_path = retrieve_model_path
        self.place_model_path = place_model_path
        self.pick_model_path = pick_model_path

    def initialize(self, garment_num: int):
        """
        add semantic objects to camera and add corresponding attribute to camera
        In this way, camera will generate cloud_point of semantic objects.
        """
        # print(self.camera.get_focal_length())

        self.camera.set_focal_length(4.25)

        # define semantic objects
        for i in range(garment_num):
            semantic_type = "class"
            semantic_label = (
                f"garment_{i}"  # The label you would like to assign to your object
            )
            prim_path = f"/World/Garment/garment_{i}"  # the path to your prim object
            rep.modify.semantics([(semantic_type, semantic_label)], prim_path)

        # add corresponding attribute to camera
        self.camera.initialize()

        # get pointcloud annotator and attach it to camera
        self.render_product = rep.create.render_product(
            self.camera_prim_path, [640, 480]
        )
        self.annotator = rep.AnnotatorRegistry.get_annotator("pointcloud")
        self.annotator_semantic = rep.AnnotatorRegistry.get_annotator(
            "semantic_segmentation"
        )
        self.annotator_bbox = rep.AnnotatorRegistry.get_annotator("bounding_box_3d")

        self.annotator.attach(self.render_product)
        self.annotator_semantic.attach(self.render_product)
        self.annotator_bbox.attach(self.render_product)

        # load model
        self.model = Aff_Model(normal_channel=False).cuda()
        if self.retrieve_model_path is None:
            self.model.load_state_dict(
                torch.load("Env_Config/Model/basket_retrieve_model_finetuned.pth")
            )
        else:
            self.model.load_state_dict(torch.load(self.retrieve_model_path))
        self.model.eval()

        # load place model
        self.place_model = Place_Model(normal_channel=False).cuda()
        if self.place_model_path is None:
            self.place_model.load_state_dict(
                torch.load("Env_Config/Model/basket_place_model_finetuned.pth")
            )
        else:
            self.place_model.load_state_dict(torch.load(self.place_model_path))
        self.place_model.eval()

        self.pick_model = Pick_Model(normal_channel=False).cuda()
        if self.pick_model_path is None:
            self.pick_model.load_state_dict(
                torch.load("Env_Config/Model/basket_pick_model_finetuned.pth")
            )
        else:
            self.pick_model.load_state_dict(torch.load(self.pick_model_path))
        self.pick_model.eval()

    def get_point_cloud_data(self, sample_flag: bool = False, sample_num: int = 1024):
        """
        get point_cloud's data and color of each point
        """
        # get point_cloud data
        self.data = self.annotator.get_data()
        self.point_cloud = self.data["data"]
        if len(self.point_cloud) == 0:
            cprint("No point cloud data", "red")
            return None, None
        self.colors = self.data["info"]["pointRgb"].reshape((-1, 4))
        self.semantic_data = self.data["info"]["pointSemantic"]
        # if sample_flag is True, sample the point_cloud
        if sample_flag:
            self.point_cloud, self.colors, self.semantic_data = furthest_point_sampling(
                points=self.point_cloud,
                colors=self.colors,
                semantics=self.semantic_data,
                n_samples=sample_num,
            )

        return self.point_cloud, self.colors

    def save_point_cloud(
        self,
        sample_flag=True,
        sample_num=4096,
        save_flag=False,
        save_path="data/pointcloud/pointcloud",
    ):
        # get point_cloud data
        self.get_point_cloud_data(sample_flag=sample_flag, sample_num=sample_num)
        # save point_cloud data to .ply file

        file_name, count = get_unique_filename(save_path, extension=".ply")
        if save_flag:
            write_ply_with_colors(
                points=self.point_cloud, colors=self.colors, filename=file_name
            )

        return file_name, count

    def get_rgb_graph(self, save_path="data/rgb/rgb", count=None):
        # get rgb data
        rgb_data = self.camera.get_rgb()
        # save it to .png file
        # import open3d as o3d
        # image = o3d.geometry.Image(np.ascontiguousarray(rgb_data))
        # o3d.io.write_image(get_unique_filename("data/rgb/rgb", ".png"), image)
        if count is None:
            file_name = get_unique_filename(save_path, ".png")
        else:
            file_name = f"{save_path}_{count}.png"
        write_rgb_image(rgb_data, file_name)

        return file_name

    def save_pc(
        self, pointcloud, colors, save_path="data/pointcloud/pointcloud", count=None
    ):
        if count is None:
            file_name, count = get_unique_filename(save_path, extension=".ply")
        else:
            file_name = f"{save_path}_{count}.ply"
        write_ply_with_colors(points=pointcloud, colors=colors, filename=file_name)

        return file_name, count

    def get_random_point(self):
        """
        get random points from point_cloud graph to pick
        return pick_point
        """
        point_nums = self.point_cloud.shape[0]
        self.pick_num = random.sample(range(point_nums), 1)
        pick_points = self.point_cloud[self.pick_num]
        return pick_points

    def get_model_point(self):
        print(self.point_cloud.shape)
        input = self.point_cloud.reshape(1, -1, 3)
        print(input.shape)
        print("ready to put data into model")
        input = torch.from_numpy(input).float().cuda()
        output = self.model(input)
        # print(output)
        # max_values = np.max(output, axis=1)

        # # 沿着第 1 维获取最大值的索引
        # indices = np.argmax(output, axis=1)
        self.max_value, indices = torch.max(output, dim=1, keepdim=False)
        print(self.max_value)
        self.pick_num = indices
        print(self.point_cloud[indices])
        print("get point from model")
        self.pick_num = self.pick_num.cpu().numpy()
        print(self.pick_num, type(self.pick_num))
        return self.point_cloud[indices]

    def get_pc_ratio(self):
        """
        get ratio of point cloud that is greater than 0.70
        """
        input = self.point_cloud.reshape(1, -1, 3)
        input = torch.from_numpy(input).float().cuda()
        output = self.model(input)
        count_greater_than_0_70 = (output > 0.70).sum().item()
        ratio_greater_than_0_70 = count_greater_than_0_70 / output.numel()
        return ratio_greater_than_0_70

    def get_cloth_picking(self):
        # self.semantic_data=self.data["info"]['pointSemantic']
        self.semantic_id = self.semantic_data[self.pick_num]
        self.seg = self.annotator_semantic.get_data()["info"]["idToLabels"]
        # print(self.semantic_id)
        # print(self.seg)
        # print(self.seg.get(str(int(self.semantic_id[0]))))
        return self.seg.get(str(int(self.semantic_id[0])))["class"]

    def get_occlusion(self):
        data = self.annotator_bbox.get_data()
        semanticid = data["data"]["semanticId"]
        occlusion_ratios = data["data"]["occlusionRatio"]
        print(occlusion_ratios)
        print(semanticid)

    def get_place_point(self, pc, pick_point):
        """
        get place point from place model
        """
        input_pick_pc = pc
        input_pick_pc[0] = pick_point
        input_pick_pc = torch.from_numpy(input_pick_pc).float().cuda().unsqueeze(0)
        input_place_pc = torch.from_numpy(pc).float().cuda().unsqueeze(0)
        output = self.place_model(
            input_pick_pc.transpose(2, 1), input_place_pc.transpose(2, 1)
        )
        max_value, indices = torch.max(output, dim=1, keepdim=False)
        print(max_value)
        print(indices)
        print("get place point from model")
        return pc[indices]

    def get_pick_point(self, pc):
        """
        get pick point from pick model
        """
        input_pc = torch.from_numpy(pc).float().cuda().unsqueeze(0)
        output = self.pick_model(input_pc.transpose(2, 1))
        max_value, indices = torch.max(output, dim=1, keepdim=False)
        print(max_value)
        print(indices)
        print("get pick point from model")
        return pc[indices]
