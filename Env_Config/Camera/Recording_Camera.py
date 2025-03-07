"""
Use Recording Camera to generate gif
"""

import os
import sys

sys.path.append("Env_Config/")

import numpy as np
import torch
from omni.isaac.sensor import Camera
from omni.isaac.core.utils.rotations import euler_angles_to_quat
from Utils_Project.utils import (
    get_unique_filename,
    record_success_failure,
    furthest_point_sampling,
)
import omni.replicator.core as rep
import random
import imageio
import time


class Recording_Camera:
    def __init__(
        self,
        camera_position,
        camera_orientation,
        frequency=20,
        resolution=(512, 512),
        prim_path="/World/recording_camera",
    ):
        # define camera parameters
        self.camera_position = camera_position
        self.camera_orientation = camera_orientation
        self.frequency = frequency
        self.resolution = resolution
        self.camera_prim_path = prim_path
        # define capture photo flag
        self.capture = True
        # define contact ground flag
        self.contact = False
        # define record_camera Judge flag
        self.judge = True

        # define camera
        self.camera = Camera(
            prim_path=self.camera_prim_path,
            position=self.camera_position,
            orientation=euler_angles_to_quat(self.camera_orientation, degrees=True),
            frequency=self.frequency,
            resolution=self.resolution,
        )
        # self.initialize()

    def initialize(self):
        self.video_frame = []
        self.camera.initialize()
        self.camera.add_semantic_segmentation_to_frame()
        self.camera.add_distance_to_image_plane_to_frame()
        self.camera.add_pointcloud_to_frame(include_unlabelled=False)
        # get pointcloud annotator and attach it to camera
        self.render_product = rep.create.render_product(
            self.camera_prim_path, [512, 512]
        )
        self.annotator = rep.AnnotatorRegistry.get_annotator("pointcloud")
        self.annotator.attach(self.render_product)

    def get_rgb_graph(self):
        """
        take RGB graph from recording_camera and collect them
        """
        # when capture flag is True, make camera capture photos
        while self.capture:
            data = self.camera.get_rgb()
            if len(data):
                self.video_frame.append(data)

            # take rgb photo every 500 ms
            time.sleep(0.5)
            # print("get rgb successfully")
        print("stop get rgb")

    def create_gif(self, save_path: str = None):
        """
        create gif according to video frame list
        """
        self.capture = False
        output_filename = save_path
        with imageio.get_writer(output_filename, mode="I", duration=0.1) as writer:
            for frame in self.video_frame:
                # write each video frame into gif
                writer.append_data(frame)

        print(f"GIF has been save into {output_filename}")

        self.video_frame.clear()

    def judge_contact_with_ground(
        self, save_path: str = "Env_Eval/washmachine_record.txt"
    ):
        """
        Judge whether the fetched garment has contact with ground
        """
        while self.judge:
            # self.draw_point_cloud()
            self.data = self.annotator.get_data()
            if self.data is None:
                continue
            self.point_cloud = self.data["data"]

            # print(self.point_cloud)
            if len(self.point_cloud) == 0:
                continue
            if self.point_cloud.ndim < 2:
                print(self.data)
                continue
            if self.point_cloud.shape[1] < 3:
                print(self.data)
                continue

            z_values = self.point_cloud[:, 2]

            # 计算 z 坐标小于 0.01 的点的数量
            count_z = np.sum(z_values < 0.05).item()
            # print(count_z)
            if count_z >= 50:
                # self.draw_point_cloud()
                record_success_failure(
                    flag=False,
                    file_path=save_path,
                    str="contact with floor",
                )
                self.contact = True
                # print("garment contact with ground")

    def judge_final_pose(self):
        """
        Judge whether final pose is correct,
        which means the fetched gatment isn't stuck in the washing machine.
        """
        data = self.annotator.get_data()
        self.point_cloud = data["data"]
        if len(self.point_cloud) == 0:
            return
        if self.point_cloud.ndim < 2:

            return
        if self.point_cloud.shape[1] < 3:

            return
        z_values = self.point_cloud[:, 2]
        max_z_value = np.max(z_values).item()
        if not self.contact:
            if max_z_value > 0.35:
                record_success_failure(
                    flag=False,
                    file_path="Env_Eval/washmachine_record.txt",
                    str="did not fall onto the floor properly",
                )
            else:
                record_success_failure(
                    flag=True, file_path="Env_Eval/washmachine_record.txt"
                )

    def stop_judge_contact(self):
        """
        stop camera from judging contact with ground
        """
        self.judge = False

    def stop_capture_video(self):
        """
        stop camera from capturing video frame
        """
        self.capture = False

    def draw_point_cloud(self, save_path: str = None):
        # get point_cloud data
        self.data = self.annotator.get_data()
        self.point_cloud = self.data["data"]
        pointRgb = self.data["info"]["pointRgb"]
        pointRgb_reshaped = pointRgb.reshape((-1, 4))
        self.colors = pointRgb_reshaped / 255.0

        self.point_cloud, self.colors = furthest_point_sampling(
            self.point_cloud, self.colors
        )
        # --draw the picture and save it-- #
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        fig = plt.figure()  # create figure
        ax = fig.add_subplot(111, projection="3d")  # create 3d plot in figure
        # extract x y z from point_cloud data
        # print(self.point_cloud)
        x = self.point_cloud[:, 0]
        y = self.point_cloud[:, 1]
        z = self.point_cloud[:, 2]
        # draw
        ax.scatter(x, y, z, c=self.colors, s=10)
        ax.view_init(elev=20, azim=180)
        # get suitable file name
        if save_path is not None:
            plt.savefig(save_path)
