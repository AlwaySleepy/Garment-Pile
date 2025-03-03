"""
Use Point_Cloud_Camera to generate pointcloud graph

pointcloud graph will be used to get which point to catch
"""

import numpy as np
import torch
from Model.pointnet2_seg_ssg import get_model
from omni.isaac.sensor import Camera
from omni.isaac.core.utils.rotations import euler_angles_to_quat
from Utils_Project.utils import get_unique_filename, record_success_failure, write_ply
import omni.replicator.core as rep
import random


import matplotlib.pyplot as plt
from point_sample import furthest_point_sampling


class Point_Cloud_Camera:
    def __init__(
        self,
        camera_position,
        camera_orientation,
        frequency=20,
        resolution=(512, 512),
        prim_path="/World/point_cloud_camera",
        garment_num: int = 1,
    ):
        # define camera parameters
        self.camera_position = camera_position
        self.camera_orientation = camera_orientation
        self.frequency = frequency
        self.resolution = resolution
        self.camera_prim_path = prim_path
        self.garment_num = garment_num
        # define camera
        self.camera = Camera(
            prim_path=self.camera_prim_path,
            position=self.camera_position,
            orientation=euler_angles_to_quat(self.camera_orientation, degrees=True),
            frequency=self.frequency,
            resolution=self.resolution,
        )
        # self.initialize(garment_num)

    def initialize(self, garment_num: int):
        """
        add semantic objects to camera and add corresponding attribute to camera
        In this way, camera will generate cloud_point of semantic objects.
        """
        # define semantic objects
        for i in range(garment_num):
            semantic_type = "class"
            semantic_label = (
                f"garment_{i}"  # The label you would like to assign to your object
            )
            prim_path = f"/World/Garment/garment_{i}"  # the path to your prim object
            rep.modify.semantics([(semantic_type, semantic_label)], prim_path)

        # rep.modify.semantics([("class_wm","wash_machine")], "/World/Wash_Machine")

        # add corresponding attribute to camera
        self.camera.initialize()
        self.camera.add_semantic_segmentation_to_frame()
        self.camera.add_distance_to_image_plane_to_frame()
        self.camera.add_pointcloud_to_frame(include_unlabelled=False)
        # get pointcloud annotator and attach it to camera
        self.render_product = rep.create.render_product(
            self.camera_prim_path, [512, 512]
        )
        self.annotator = rep.AnnotatorRegistry.get_annotator("pointcloud")
        self.annotator_semantic = rep.AnnotatorRegistry.get_annotator(
            "semantic_segmentation"
        )
        self.annotator_bbox = rep.AnnotatorRegistry.get_annotator("bounding_box_3d")
        self.annotator_rgb = rep.AnnotatorRegistry.get_annotator(
            "pointcloud", init_params={"includeUnlabelled": True}
        )

        self.annotator.attach(self.render_product)
        self.annotator_semantic.attach(self.render_product)
        self.annotator_bbox.attach(self.render_product)
        self.annotator_rgb.attach(self.render_product)

        # load model
        self.model = get_model(normal_channel=False).cuda()
        self.model.load_state_dict(torch.load("Model/finetune_model_5.pth"))
        self.model.eval()

    def get_point_cloud_data(self, sample=True):
        """
        get point_cloud's data and color of each point
        """
        # get point_cloud data
        self.data = self.annotator.get_data()
        self.point_cloud = self.data["data"]
        self.semantic_data = self.data["info"]["pointSemantic"]
        # print(self.semantic_data)
        pointRgb = self.data["info"]["pointRgb"]

        self.semantic_data = self.semantic_data.astype(np.int32)
        pointRgb = pointRgb.reshape((-1, 4))

        if sample:
            self.point_cloud, colors, self.semantic = furthest_point_sampling(
                self.point_cloud, pointRgb, self.semantic_data, 4096
            )
            self.colors = colors / 255.0
        else:
            self.colors = pointRgb / 255.0
        return self.point_cloud, self.colors
        # print(self.data)
        # print(self.point_cloud)
        # get the color of each point
        # pointRgb=data["info"]['pointRgb']
        # pointRgb_reshaped = pointRgb.reshape((-1, 4))
        # self.colors = pointRgb_reshaped / 255.0

        # if len(self.point_cloud)==0:
        #     record_success_failure(flag=False,file_path="data/Record.txt",str="cannot get pointcloud")

        # write_ply(points=self.point_cloud,filename=get_unique_filename(base_filename="data/pointcloud_1/pointcloud",extension=".ply"))

    def get_pointcloud_with_washing_machine(self):
        data = self.annotator_rgb.get_data()
        points = self.data["data"]
        rgb = self.data["info"]["pointRgb"]
        rgb = rgb.reshape((-1, 4))
        rgb = rgb / 255.0
        return points, rgb

    def draw_point_cloud(self, sample=False):

        from PIL import Image

        rgb_data = self.camera.get_rgb()
        # print(rgb_data)
        image = Image.fromarray(rgb_data)
        filename = get_unique_filename("data/camera/camera_image")  # 你想要保存的文件名
        image.save(filename)

        with open("data/Record.txt", "a") as file:
            # file.write(f"{self.cur}"+'\n')

            file.write(f"{filename}" + "\n")
        # get point_cloud data
        points, rgb = self.get_point_cloud_data(sample=sample)
        # --draw the picture and save it-- #
        # import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        fig = plt.figure(figsize=(8, 8))  # create figure
        ax = fig.add_subplot(111, projection="3d")  # create 3d plot in figure
        # extract x y z from point_cloud data
        # print(self.point_cloud)
        x = points[:, 0]
        y = points[:, 1]
        z = points[:, 2]
        # draw
        ax.scatter(x, y, z, c=rgb, s=5)
        ax.view_init(elev=12, azim=180)

        ax.axis("off")  # 关闭坐标轴
        ax.grid(False)  # 关闭网格
        # get suitable file name
        filename = get_unique_filename("data/sample/pointcloud")
        # save file
        plt.savefig(filename, dpi=300)

    def get_random_point(self):
        """
        get random points from point_cloud graph to pick
        return pick_point
        """
        point_nums = self.point_cloud.shape[0]
        self.pick_num = random.sample(range(point_nums), 1)
        pick_points = self.point_cloud[self.pick_num]
        self.id = self.semantic[self.pick_num[0]]
        return pick_points

    def get_model_point(self):
        # print(self.point_cloud.shape)
        # input=self.point_cloud.reshape(1, -1, 3)
        # print(input.shape)
        # print("ready to put data into model")
        # self.output=self.model.forward(input)
        # # print(output)
        # # max_values = np.max(output, axis=1)

        # # # 沿着第 1 维获取最大值的索引
        # # indices = np.argmax(output, axis=1)
        # max_value,indices = torch.max(self.output, dim=1, keepdim=False)
        # # print(max_value)
        # self.pick_num=indices
        # # print(self.point_cloud[indices])

        # # point,self.pick_num=self.select_point()
        # # print(self.pick_num)
        # # print("get point from model")
        # # return point.cpu().numpy(),max_value
        # return self.point_cloud[indices],max_value

        # print(self.point_cloud.shape)
        self.seg = self.annotator_semantic.get_data()["info"]["idToLabels"]
        # print(self.semantic_id)
        # print(self.seg)

        input = self.point_cloud.reshape(1, -1, 3)
        # print(input.shape)
        print("ready to put data into model")
        output = self.model(input)
        # self.analyze_statistics(output)
        output = output.detach()
        # self.analyze_statistics(output)

        max_value = 0
        distance = 1.0
        occlusion = 1.0
        flag = False
        count = 0
        while True:
            if occlusion == 0.0:
                break
            count += 1
            max_value, indices = torch.max(output, dim=1, keepdim=False)
            self.pick_num = indices.squeeze().item()
            self.id = self.semantic[indices]
            # print(self.id)
            cur_cloth = self.seg.get(str(int(self.id)))["class"]
            garment_cur_index = int(cur_cloth[8:])
            occlusion = self.get_occlusion(garment_cur_index)
            output[torch.arange(output.size(0)), indices] = 0
            pick_point = torch.Tensor(input[0, indices].squeeze()).cuda()
            # point_compare = torch.Tensor([0.1, 0.0, 0.59]).cuda()
            # distance = torch.sqrt(torch.sum((pick_point - point_compare) ** 2)).item()
            # print("pick_point:", pick_point)
            print("max_value:", max_value)
            print("distance between pick_point and center:", distance)
            print("occlusion:", occlusion)
            # if distance<0.33 and occlusion<0.6:
            if occlusion < 1.0:  # 0.6
                break
            if count == 300:
                break
            if flag is False:
                filename, ply_counter = get_unique_filename(
                    base_filename=f"data/pointcloud/pointcloud", extension=".ply"
                )
                write_ply(points=self.point_cloud, filename=filename)
                with open("data/Record.txt", "a") as file:
                    # file.write(f"{self.cur}"+'\n')
                    file.write(
                        f"{pick_point[0]} {pick_point[1]} {pick_point[2]} {ply_counter} 0 occlusion not good"
                        + "\n"
                    )
                if count == 3:
                    flag = True

        pick_point = pick_point.cpu().numpy()
        print("get point from model, the point is:", pick_point)
        return pick_point, max_value, output

    def get_cloth_picking(self):
        # self.semantic_data=self.data["info"]['pointSemantic']
        # self.semantic_id=self.semantic_data[self.pick_num]
        self.seg = self.annotator_semantic.get_data()["info"]["idToLabels"]
        # print(self.semantic_id)
        # print(self.seg)
        # print(self.id)
        # print(self.seg.get(str(int(self.id))))
        return self.seg.get(str(int(self.id)))["class"]

    def get_rgb_depth(self):
        rgb = self.camera.get_rgb()
        depth = self.camera.get_depth()
        return rgb, depth

    def draw_point_cloud(self, file_name):
        from PIL import Image

        rgb_data = self.camera.get_rgb()
        image = Image.fromarray(rgb_data)
        image.save(file_name)

    def select_point(self):

        # 选择最大的三个值及其索引
        topk_values, topk_indices = torch.topk(self.output, 3, dim=1)

        # 从 pointcloud 中选择相应的三个点
        if not isinstance(self.point_cloud, torch.Tensor):
            pointcloud = torch.tensor(self.point_cloud).to("cuda:0")
        # print(topk_indices)
        # print(topk_indices.device)
        # print(pointcloud.device)
        topk_points = pointcloud[topk_indices.squeeze(0)]

        position = torch.tensor([-0.115, 0.0, 0.85]).to("cuda:0")
        # 计算这些点到 position 的距离
        distances = torch.norm(topk_points - position, dim=2)

        # 选择距离最小的点
        min_distance_index = torch.argmin(distances)
        selected_point = topk_points[min_distance_index]
        print(selected_point)
        pick_num = topk_indices.squeeze(0)[min_distance_index][0].item()
        print(pick_num)
        return selected_point, pick_num

    def get_occlusion(self, id):
        data = self.annotator_bbox.get_data()
        # print(id)
        occlusion_ratios = data["data"]["occlusionRatio"]
        elements = data["info"]["primPaths"]
        print(data["info"])
        # print(data['data']["semanticId"])
        # print(data["info"]["idToLabels"])
        print(occlusion_ratios)
        indices = [int(el[-1]) for el in elements]
        occlusion_ratios_re = [-1] * self.garment_num

        # 根据索引重新排列 occlusion
        for i, index in enumerate(indices, start=0):
            occlusion_ratios_re[index] = occlusion_ratios[i]
        print(occlusion_ratios_re)
        # occlusion_ratios_re = [x for x in occlusion_ratios_re if x != -1]

        # print(occlusion_ratios_re)
        return occlusion_ratios_re[int(id)]

    def analyze_statistics(self, output):

        # 将 Tensor 数组展平为 1D 数组

        output = output.cpu().numpy()
        data = output.flatten()
        print(data)
        # 计算直方图
        counts, bins = np.histogram(
            data, bins=30, density=True
        )  # density=True 表示计算概率密度

        # 计算每个区间的中心值
        bin_centers = 0.5 * (bins[1:] + bins[:-1])  # 中心值

        # 绘制直方图
        plt.bar(bin_centers, counts, width=bins[1] - bins[0], alpha=0.7, color="blue")
        plt.xlabel("value")
        plt.ylabel("portion")
        plt.title("histogram")
        plt.xlim(0, 1)  # 设置 x 轴范围
        plt.ylim(0, max(counts) * 1.1)  # 设置 y 轴范围

        filename = get_unique_filename("data/statistics/picture")

        plt.savefig(
            filename, dpi=300, bbox_inches="tight"
        )  # 保存为 PNG 格式，设置分辨率和边距

        # 关闭当前图像（可选）
        plt.close()
