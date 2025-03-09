import random
import sys
import os
sys.path.append(os.getcwd())
from Env_Config.Config.wash_machine_config import Config
import torch

# from isaacsim import SimulationApp
from omni.isaac.kit import SimulationApp

simulation_app = SimulationApp({"headless": False})

# ---------------------coding begin---------------------#
import numpy as np
import omni.replicator.core as rep
import threading
import time
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.rotations import euler_angles_to_quat, quat_to_euler_angles
from omni.physx import acquire_physx_interface
from pxr import UsdGeom, UsdLux, Sdf, Gf, Vt, Usd, UsdPhysics, PhysxSchema
from omni.isaac.core.objects import DynamicCuboid, FixedCuboid
from omni.isaac.sensor import Camera
from omni.kit.viewport.utility import get_active_viewport
from omni.isaac.core.utils.prims import delete_prim, set_prim_visibility
from omni.isaac.core.utils.viewports import set_camera_view

# print(sys.path)

from Env_Config.Robot.WrapFranka import WrapFranka
from Env_Config.Garment.Garment import WrapGarment, Garment
from Env_Config.Utils_Project.utils import (
    add_wm_door,
    change_door_pos,
    compare_position_before_and_after,
    get_unique_filename,
    wm_judge_final_poses,
    load_conveyor_belt,
    load_washmachine_model,
    record_success_failure,
    write_ply,
    write_ply_with_colors,
)
from Env_Config.Utils_Project.WM_Collision_Group import Collision_Group
from Env_Config.Utils_Project.AttachmentBlock import AttachmentBlock
from Env_Config.Camera.WashMachine_Point_Cloud_Camera import Point_Cloud_Camera
from Env_Config.Camera.Recording_Camera import Recording_Camera
from Env_Config.Model.pointnet2_Retrieve_Model import Retrieve_Model
from Env_Config.Model.pointnet2_Place_Model import Place_Model
from Env_Config.Model.pointnet2_Pick_Model import Pick_Model
import Env_Config.Utils_Project.utils as util
from Env_Config.Room.Room import Wrap_base, Wrap_room, Wrap_basket, Wrap_wash_machine


class washmachineEnv:
    def __init__(
        self,
        random_flag=True,
        model_path=None,
        rgb_flag=False,
    ):
        # random select retrieve point or not
        self.random_flag = random_flag
        # if not random, load model
        if not self.random_flag:
            self.model_path = model_path
        else:
            self.model_path = None
        # save judge_rgb or not
        self.rgb_flag = rgb_flag

        # define the world
        self.world = World(backend="torch", device="cpu")
        set_camera_view(
            eye=[-1.5, -1.5, 1.5],
            target=[0.01, 0.01, 0.01],
            camera_prim_path="/OmniverseKit_Persp",
        )
        physx_interface = acquire_physx_interface()
        physx_interface.overwrite_gpu_setting(1)  # garment render request

        # define the stage
        self.stage = self.world.stage

        # define the physics context
        self.scene = self.world.get_physics_context()._physics_scene
        # set gravity
        self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0, 0.0, -1))
        self.scene.CreateGravityMagnitudeAttr().Set(9.8)

        # set default_ground
        self.world.scene.add_default_ground_plane(z_position=-0.05)

        # get environment config
        self.config = Config()

        # set global light
        self.demo_light = rep.create.light(position=[0, 0, 0], light_type="dome")

        self.disk_light_inside = rep.create.light(
            position=[0.13459, -0.07683, 0.83689], light_type="disk", intensity=3000
        )

        self.disk_light_inside2 = rep.create.light(
            position=[0.12834, 0.17148, 0.74336], light_type="disk", intensity=3000
        )

        # set local light in washing machine
        self.disk_light = rep.create.light(
            position=[0.2184, 0, 1.11234],
            light_type="rect",
            intensity=15000,
            rotation=[0, -42, 0],
        )

        # load recording_camera (use this camera to generate gif)
        self.recording_camera = Recording_Camera(
            self.config.recording_camera_position,
            self.config.recording_camera_orientation,
        )

        # load point_cloud_camera (use this camera to generate point_cloud graph)
        self.point_cloud_camera = Point_Cloud_Camera(
            self.config.point_cloud_camera_position,
            self.config.point_cloud_camera_orientation,
            garment_num=self.config.garment_num,
        )

        # load franka
        self.franka = WrapFranka(
            self.world,
            self.config.robot_position,
            self.config.robot_orientation,
            prim_path="/World/Franka",
            robot_name="franka_robot",
            recording_camera=self.recording_camera,
        )

        # load wash_machine
        self.wash_machine = Wrap_wash_machine(
            self.config.wm_position,
            self.config.wm_orientation,
            self.config.wm_scale,
            self.config.wm_usd_path,
            self.config.wm_prim_path,
        )

        # load room
        # self.room = Wrap_room(
        #     self.config.room_position,
        #     self.config.room_orientation,
        #     self.config.room_scale,
        #     self.config.room_usd_path,
        #     self.config.room_prim_path,
        # )

        # load basket
        # self.basket = Wrap_basket(
        #     self.config.basket_position,
        #     self.config.basket_orientation,
        #     self.config.basket_scale,
        #     self.config.basket_usd_path,
        #     self.config.basket_prim_path,
        # )

        # load base
        # self.base = Wrap_base(
        #     self.config.base_position,
        #     self.config.base_orientation,
        #     self.config.base_scale,
        #     self.config.base_usd_path,
        #     self.config.base_prim_path,
        # )

        # load garment
        self.garments = WrapGarment(
            self.stage,
            self.scene,
            self.config.garment_num,
            self.config.clothpath,
            self.config.garment_position,
            self.config.garment_orientation,
            self.config.garment_scale,
        )

        self.garment_index = [True] * self.config.garment_num

        # load conveyor_belt
        load_conveyor_belt(self.world)

        # load washmachine_model
        obstacle_list = load_washmachine_model(self.world)

        self.door = FixedCuboid(
            name="wm_door",
            position=[-0.39497, 0.0, 0.225],
            prim_path="/World/wm_door",
            scale=np.array([0.05, 1, 0.55]),
            orientation=euler_angles_to_quat([0, 0, 0], degrees=True),
            size=1.0,
            color=np.array([180, 180, 180]),
            visible=False,
        )

        # create collision group
        self.collision = Collision_Group(self.stage)

        # add obstacle to franka's rmpflow motion, in case that franka can avoid collision with washing machine smartly
        for obstacle in obstacle_list:
            self.franka.add_obstacle(obstacle)
        print("collision add successfully")

        # load retrieval model
        self.garment_model = Retrieve_Model(normal_channel=False).cuda()
        self.garment_model.load_state_dict(
            torch.load("Env_Config/Model/wm_retrieve_model_finetuned.pth")
        )
        self.garment_model.eval()

        # load place model
        if not self.random_flag:
            self.place_model = Place_Model(normal_channel=False).cuda()
            self.place_model.load_state_dict(torch.load(self.model_path))
            self.place_model.eval()

        print("ramdom select point:", self.random_flag)
        if not self.random_flag:
            print("model path:", self.model_path)
        print("save rgb:", self.rgb_flag)

    def garment_into_machine(self):
        """
        Let the clothes slide into the washing machine through the conveyor belt (which is invisible)
        by changing the direction of gravity.
        """
        # change gravity direction
        self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(1.5, 0.0, -1.2))
        self.scene.CreateGravityMagnitudeAttr().Set(8.0)
        for i in range(650):
            if not simulation_app.is_running():
                simulation_app.close()
            simulation_app.update()
            if i == 250:
                self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(1.5, 0.0, -0.3))
                self.scene.CreateGravityMagnitudeAttr().Set(8.0)
            if i == 400:
                self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(1.5, 0.0, 0.05))
                self.scene.CreateGravityMagnitudeAttr().Set(9.8)
            if i == 550:
                print("ready to change")
                # return to the normal gravity direction
                self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, 0.0, -1))
                self.scene.CreateGravityMagnitudeAttr().Set(9.8)

    def remove_conveyor_belt(self):
        """
        remove conveyor belt and its collision group
        """
        delete_prim("/World/Conveyor_belt")

        change_door_pos(self.door)
        self.world.step(render=True)
        # self.world.play(
        print("Conveyor Belt Removed!")

    def create_attach_block(self, init_position=np.array([0.0, 0.0, 1.0])):
        """
        Create attachment block and update the collision group at the same time.
        """
        # create attach block and finish attach
        self.attach = AttachmentBlock(
            self.world,
            self.stage,
            "/World/AttachmentBlock",
            self.garments.garment_mesh_path,
        )
        self.attach.create_block(
            block_name="attach", block_position=init_position, block_visible=True
        )
        print("attach finish!")
        # update attach collision group
        self.collision.update_after_attach()
        for i in range(100):
            simulation_app.update()
        print("Update collision group successfully!")

    def set_attach_to_garment(self, attach_position):
        """
        push attach_block to new grasp point and attach to the garment
        """
        # set the position of block
        self.attach.set_block_position(attach_position)
        # create attach
        self.attach.attach()
        # render the world
        self.world.step(render=True)

    def get_point_cloud_data(
        self,
        filename="Data/WashMachine/Stir_Random/point_cloud/pointcloud",
        save=True,
        counter=None,
    ):
        """
        get point cloud data and save it into .ply file if needed
        """
        for i in range(30):
            self.world.step(render=True)

        self.point_cloud, self.colors = self.point_cloud_camera.get_point_cloud_data()

        if counter is not None:
            ply_filename = f"{filename}_{counter}.ply"
        else:
            ply_filename, self.count = get_unique_filename(filename, ".ply")

        if save:
            write_ply_with_colors(
                points=self.point_cloud,
                colors=self.colors * 255.0,
                filename=ply_filename,
            )
        print(f"write into ply file -> {ply_filename}")

    def stir_whole_procedure(self):
        # get point cloud data
        if self.random_flag:
            self.get_point_cloud_data(
                filename="Data/WashMachine/Stir_Random/point_cloud/pointcloud",
                save=False,
            )
        else:
            self.get_point_cloud_data(
                filename="Data/WashMachine/Stir_Model/point_cloud/pointcloud",
                save=False,
            )

        # set franka to be visible
        # set_prim_visibility(self.franka._robot.prim, True)
        # use model to get percentage_below_threshold to judge whether to stir
        pick_point, max_value, output = self.point_cloud_camera.get_model_point()
        count_below_threshold = (output > 0.93).sum().item()
        total_elements = output.numel()
        percentage_below_threshold = count_below_threshold / total_elements
        print("percentage_below_threshold", percentage_below_threshold)
        # judge stir conditions
        if percentage_below_threshold < 0.044:
            print("start to stir")
            self.stir(self.point_cloud)

    def stir(self, point_cloud):
        index = 0
        continue_stir = True
        while continue_stir:

            if self.random_flag:
                self.get_point_cloud_data(
                    filename="Data/WashMachine/Stir_Random/point_cloud/pointcloud"
                )
            else:
                self.get_point_cloud_data(
                    filename="Data/WashMachine/Stir_Model/point_cloud/pointcloud"
                )

            if self.rgb_flag:
                if self.random_flag:
                    rgb_filename = get_unique_filename(
                        "Data/WashMachine/Stir_Random/rgb/rgb", ".png"
                    )
                    print(rgb_filename)
                    self.point_cloud_camera.get_rgb(file_name=rgb_filename)
                    print(f"write into rgb file -> {rgb_filename}")
                else:
                    rgb_filename = get_unique_filename(
                        "Data/WashMachine/Stir_Model/rgb/rgb", ".png"
                    )
                    print(rgb_filename)
                    self.point_cloud_camera.get_rgb(file_name=rgb_filename)
                    print(f"write into rgb file -> {rgb_filename}")

            set_prim_visibility(self.franka._robot.prim, True)

            point_cloud = self.point_cloud

            garment_model_input = point_cloud.reshape(1, -1, 3)
            garment_model_input = torch.Tensor(garment_model_input).to("cuda:0")
            garment_model_output = self.garment_model(garment_model_input)

            max_value, indices = torch.max(garment_model_output, dim=1, keepdim=False)
            pick_max_value = max_value.item()

            count_below_threshold = (garment_model_output > 0.9).sum().item()
            total_elements = garment_model_output.numel()
            pick_percentage_below_threshold = count_below_threshold / total_elements

            print("garment_max_value", pick_max_value)
            print("garment_percentage_below_threshold", pick_percentage_below_threshold)

            # choose pick/place point
            point_cloud = self.point_cloud

            if self.random_flag:
                num_points = point_cloud.shape[0]
                dis = 0
                while dis < 0.13:
                    # select pick and place point randomly
                    pick, place = random.sample(range(num_points), 2)
                    dis = torch.norm(
                        torch.tensor(point_cloud[place])
                        - torch.tensor(point_cloud[pick])
                    ).item()

            else:
                # select pick point randomly
                num_points = point_cloud.shape[0]
                pick = random.sample(range(num_points), 1)[0]

                pick_pc = point_cloud
                pick_pc[0] = point_cloud[pick]

                place_pc = point_cloud

                pick_pc = torch.Tensor(pick_pc.reshape(1, -1, 3)).to("cuda:0")
                place_pc = torch.Tensor(place_pc.reshape(1, -1, 3)).to("cuda:0")

                place_model_output = self.place_model(
                    pick_pc.transpose(2, 1), place_pc.transpose(2, 1)
                )

                max_value, indices = torch.max(place_model_output, dim=1, keepdim=False)
                place = indices

            stir_pick = point_cloud[pick]
            stir_place = point_cloud[place]

            print("pick point", stir_pick)
            print("place point", stir_place)

            if self.random_flag:
                with open("Data/WashMachine/Stir_Random/Record.txt", "a") as file:
                    file.write(
                        f"{stir_pick[0]} {stir_pick[1]} {stir_pick[2]} {stir_place[0]} {stir_place[1]} {stir_place[2]} "
                    )
            else:
                with open("Data/WashMachine/Stir_Model/Record.txt", "a") as file:
                    file.write(f"{stir_pick[0]} {stir_pick[1]} {stir_pick[2]} ")

            self.set_attach_to_garment(stir_pick)

            # execute stir
            if self.random_flag:
                self.franka.pick(
                    self.config.target_positions,
                    self.attach,
                    error_record_file="Data/WashMachine/Stir_Random/Record.txt",
                )
                self.franka.place(
                    stir_place,
                    self.attach,
                    error_record_file="Data/WashMachine/Stir_Random/Record.txt",
                )
            else:
                self.franka.pick(
                    self.config.target_positions,
                    self.attach,
                    error_record_file="Data/WashMachine/Stir_Model/Record.txt",
                )
                self.franka.place(
                    stir_place,
                    self.attach,
                    error_record_file="Data/WashMachine/Stir_Model/Record.txt",
                )

            self.franka.open()
            self.attach.detach()
            for i in range(30):
                self.world.step(render=True)

            self.franka.adjust_after_stir()

            # after stir
            if self.random_flag:
                self.get_point_cloud_data(
                    filename="Data/WashMachine/Stir_Random/point_cloud_after_stir/pointcloud",
                    counter=self.count,
                )
            else:
                self.get_point_cloud_data(
                    filename="Data/WashMachine/Stir_Model/point_cloud_after_stir/pointcloud",
                    counter=self.count,
                )

            if self.rgb_flag:
                if self.random_flag:
                    rgb_filename = f"Data/WashMachine/Stir_Random/rgb_after_stir/rgb_{self.count}.png"
                    self.point_cloud_camera.get_rgb(file_name=rgb_filename)
                    print(f"write into rgb file -> {rgb_filename}")
                else:
                    rgb_filename = f"Data/WashMachine/Stir_Model/rgb_after_stir/rgb_{self.count}.png"
                    self.point_cloud_camera.get_rgb(file_name=rgb_filename)
                    print(f"write into rgb file -> {rgb_filename}")

            pick_point, max_value, output = self.point_cloud_camera.get_model_point()

            place_max_value = max_value.item()

            count_below_threshold = (output > 0.93).sum().item()
            total_elements = output.numel()
            place_percentage_below_threshold = count_below_threshold / total_elements

            print("place_percentage_below_threshold", place_percentage_below_threshold)

            if place_percentage_below_threshold > 0.05:

                continue_stir = False
                if self.random_flag:
                    with open("Data/WashMachine/Stir_Random/Record.txt", "a") as file:
                        file.write(
                            f"1 success pick_percentage: {pick_percentage_below_threshold} place_percentage: {place_percentage_below_threshold}"
                            + "\n"
                        )
                else:
                    with open("Data/WashMachine/Stir_Model/Record.txt", "a") as file:
                        file.write(
                            f"1 success pick_percentage: {pick_percentage_below_threshold} place_percentage: {place_percentage_below_threshold}"
                            + "\n"
                        )
                print("stir success")
            elif place_max_value - pick_max_value > 0.1:
                continue_stir = False
                if self.random_flag:
                    with open("Data/WashMachine/Stir_Random/Record.txt", "a") as file:
                        file.write(
                            f"1 success pick_percentage: {pick_percentage_below_threshold} place_percentage: {place_percentage_below_threshold}"
                            + "\n"
                        )
                else:
                    with open("Data/WashMachine/Stir_Model/Record.txt", "a") as file:
                        file.write(
                            f"1 success pick_percentage: {pick_percentage_below_threshold} place_percentage: {place_percentage_below_threshold}"
                            + "\n"
                        )
                print("stir success")
            elif (
                place_percentage_below_threshold - pick_percentage_below_threshold
                > 0.02
            ):
                continue_stir = False
                if self.random_flag:
                    with open("Data/WashMachine/Stir_Random/Record.txt", "a") as file:
                        file.write(
                            f"1 success pick_percentage: {pick_percentage_below_threshold} place_percentage: {place_percentage_below_threshold}"
                            + "\n"
                        )
                else:
                    with open("Data/WashMachine/Stir_Model/Record.txt", "a") as file:
                        file.write(
                            f"1 success pick_percentage: {pick_percentage_below_threshold} place_percentage: {place_percentage_below_threshold}"
                            + "\n"
                        )
                print("stir success")
            else:
                if self.random_flag:
                    with open("Data/WashMachine/Stir_Random/Record.txt", "a") as file:
                        file.write(
                            f"0 fail pick_percentage: {pick_percentage_below_threshold} place_percentage: {place_percentage_below_threshold}"
                            + "\n"
                        )
                else:
                    with open("Data/WashMachine/Stir_Model/Record.txt", "a") as file:
                        file.write(
                            f"0 fail pick_percentage: {pick_percentage_below_threshold} place_percentage: {place_percentage_below_threshold}"
                            + "\n"
                        )
                print("stir fail")

            index += 1
            if index >= 2:
                continue_stir = False

            set_prim_visibility(self.franka._robot.prim, False)

            for i in range(30):
                self.world.step(render=True)

        return pick_point, index


if __name__ == "__main__":

    random_flag = sys.argv[1] == "True"
    if not random_flag:
        model_path = sys.argv[2]
    else:
        model_path = None
    rgb_flag = sys.argv[3] == "True"

    env = washmachineEnv(random_flag, model_path, rgb_flag)

    env.world.reset()

    env.point_cloud_camera.initialize()

    env.recording_camera.initialize()

    # set franka to be invisible
    set_prim_visibility(env.franka._robot.prim, False)

    env.garment_into_machine()

    for garment in env.garments.garment_group:
        garment.particle_material.set_particle_friction_scale(3.5)
        garment.particle_material.set_particle_adhesion_scale(1.0)
        garment.particle_material.set_friction(0.2)

    env.remove_conveyor_belt()

    env.create_attach_block()

    env.stir_whole_procedure()

    for i in range(100):
        env.world.step(render=True)


# ---------------------coding ending---------------------#

# Close the Simulation App
simulation_app.close()
