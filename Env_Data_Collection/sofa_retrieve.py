"""
Create Garment_Sofa Environment
Include:
    -All components (sofa, franka, garment, camera, other helpful parts)
    -Whole Procedure of Project
"""

# Open the Simulation App
import os
import sys
from omni.isaac.kit import SimulationApp

simulation_app = SimulationApp({"headless": False})

# ---------------------coding begin---------------------#
import numpy as np
import omni.replicator.core as rep
import threading
import time
import random
from termcolor import cprint
from omni.isaac.core import World
from omni.kit.async_engine import run_coroutine
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.rotations import euler_angles_to_quat, quat_to_euler_angles
from omni.physx import acquire_physx_interface
from pxr import UsdGeom, UsdLux, Sdf, Gf, Vt, Usd, UsdPhysics, PhysxSchema
from omni.isaac.core.objects import DynamicCuboid, FixedCuboid
from omni.isaac.sensor import Camera
from omni.kit.viewport.utility import get_active_viewport
from omni.isaac.core.utils.prims import delete_prim, set_prim_visibility
from omni.isaac.core.utils.viewports import set_camera_view

from Env_Config.Config.sofa_config import Config
from Env_Config.Robot.WrapFranka import WrapFranka
from Env_Config.Room.Room import Wrap_room, Wrap_base, Wrap_basket
from Env_Config.Garment.Garment import WrapGarment, Garment
from Env_Config.Utils_Project.utils import (
    get_unique_filename,
    sofa_judge_final_poses,
    write_ply,
    write_ply_with_colors,
    load_sofa_transport_helper,
)
from Env_Config.Utils_Project.Sofa_Collision_Group import Collision_Group
from Env_Config.Utils_Project.AttachmentBlock import AttachmentBlock
from Env_Config.Camera.Sofa_Point_Cloud_Camera import Point_Cloud_Camera
from Env_Config.Camera.Recording_Camera import Recording_Camera
import Env_Config.Utils_Project.utils as util
import copy


class BaseEnv:
    def __init__(
        self,
        random_flag=True,
        model_path=None,
        rgb_flag=False,
        gif_flag=False,
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
        # save gif or not
        self.gif_flag = gif_flag

        # define the world
        self.world = World(backend="torch", device="cpu")
        set_camera_view(
            eye=[-2.0, 1.1, 1.8],
            target=[0.0, 1.7, 0.2],
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
        # self.world.scene.add_default_ground_plane()

        # get environment config
        self.config = Config()

        # set global light
        self.demo_light = rep.create.light(position=[0, 0, 10], light_type="dome")

        # load recording_camera (use this camera to generate gif)
        self.recording_camera = Recording_Camera(
            self.config.recording_camera_position,
            self.config.recording_camera_orientation,
        )

        # load floating_camera (use this camera to generate point_cloud graph)
        if not self.random_flag:
            self.point_cloud_camera = Point_Cloud_Camera(
                self.config.point_cloud_camera_position,
                self.config.point_cloud_camera_orientation,
                garment_num=self.config.garment_num,
                retrieve_model_path=self.model_path,
            )
        else:
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
        )

        # load base_layer
        self.base_layer = Wrap_base(
            self.config.base_layer_position,
            self.config.base_layer_orientation,
            self.config.base_layer_scale,
            self.config.base_layer_usd_path,
            self.config.base_layer_prim_path,
        )

        # load basket
        # self.basket = Wrap_basket(
        #     self.config.basket_position,
        #     self.config.basket_orientation,
        #     self.config.basket_scale,
        #     self.config.basket_usd_path,
        #     self.config.basket_prim_path,
        # )

        delete_prim(f"/World/Room")

        # load room
        self.room = Wrap_room(
            self.config.room_position,
            self.config.room_orientation,
            self.config.room_scale,
            self.config.room_usd_path,
            self.config.room_prim_path,
        )

        for i in range(self.config.garment_num):
            delete_prim(f"/World/Garment/garment_{i}")

        self.config.garment_num = random.choices([3, 4, 5], [0.1, 0.45, 0.45])[0]
        print(f"garment_num: {self.config.garment_num}")

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

        load_sofa_transport_helper(self.world)

        # create collision group
        self.collision = Collision_Group(self.stage)

        # add obstacle to franka's rmpflow motion, in case that franka can avoid collision with washing machine smartly
        # for obstacle in obstacle_list:
        #     self.franka.add_obstacle(obstacle)
        # print("collision add successfully")

        self.world.reset()

        print("--------------------------------------")
        print("ramdom pick point:", self.random_flag)
        if not self.random_flag:
            print("model path:", self.model_path)
        print("save rgb:", self.rgb_flag)
        print("save gif:", self.gif_flag)
        cprint("world load successfully", "green", on_color="on_green")

        # -------------------initialize world------------------- #

        # initialize camera
        self.point_cloud_camera.initialize(self.config.garment_num)

        self.recording_camera.initialize()

        cprint("camera initialize successfully", "green")

        # begin to record gif
        gif_generation_thread = threading.Thread(
            target=self.recording_camera.get_rgb_graph
        )
        if self.gif_flag:
            gif_generation_thread.start()

        # transport garment
        self.garment_transportation()

        cprint("garment transportation finish!", "green")

        for garment in self.garments.garment_group:
            garment.particle_material.set_friction(1.0)
            garment.particle_material.set_damping(10.0)
            garment.particle_material.set_lift(0.0)

        # delete helper
        delete_prim(f"/World/transport_helper/transport_helper_1")
        delete_prim(f"/World/transport_helper/transport_helper_2")
        delete_prim(f"/World/transport_helper/transport_helper_3")
        delete_prim(f"/World/transport_helper/transport_helper_4")

        # set franka to initial position
        self.franka.return_to_initial_position(self.config.initial_position)

        self.create_attach_block()

        cprint("world ready!", "green", on_color="on_green")

    def garment_transportation(self):
        """
        Let the clothes float into the washing machine
        by changing the direction of gravity.
        """
        # change gravity direction
        self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, 0.0, -1))
        self.scene.CreateGravityMagnitudeAttr().Set(15)
        for i in range(100):
            if not simulation_app.is_running():
                simulation_app.close()
            simulation_app.update()

    def create_attach_block(self, init_position=np.array([0.0, 0.0, 1.0]), scale=None):
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
            block_name="attach",
            block_position=init_position,
            block_visible=False,
            scale=scale,
        )
        # update attach collision group
        self.collision.update_after_attach()
        for i in range(100):
            # simulation_app.update()
            self.world.step(render=True)

        cprint("attach block create successfully", "green")

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

        cprint("attach block set successfully", "green")

    def pick_whole_procedure(self):
        while True:
            pc_judge, color_judge = self.point_cloud_camera.get_point_cloud_data()
            # print(pc_judge)
            if pc_judge is None:
                cprint("Finish picking all garments", "green", on_color="on_green")
                break

            # save pc and rgb graph
            _, self.ply_count = self.point_cloud_camera.save_point_cloud(
                sample_flag=True,
                sample_num=4096,
                save_flag=True,
                save_path="Data/Sofa/Retrieve/point_cloud/pointcloud",
            )
            if self.rgb_flag:
                self.point_cloud_camera.get_rgb_graph(
                    save_path="Data/Sofa/Retrieve/rgb/rgb"
                )
            # get pick point
            if self.random_flag:
                pick_point = self.point_cloud_camera.get_random_point()[0]
            else:
                pick_point = self.point_cloud_camera.get_model_point()
            cprint(f"pick_point: {pick_point}", "cyan")

            self.cur = self.point_cloud_camera.get_cloth_picking()
            self.id = self.point_cloud_camera.semantic_id
            cprint(f"picking {self.cur}", "cyan")

            with open("Data/Sofa/Retrieve/Record.txt", "a") as file:
                file.write(f"{pick_point[0]} {pick_point[1]} {pick_point[2]} ")

            # define thread to judge contact with ground
            judge_thread = threading.Thread(
                target=self.recording_camera.judge_contact_with_ground,
                args=("Data/Sofa/Retrieve/Record.txt",),
            )
            # begin judge_final_pose thread
            judge_thread.start()

            # set attach block and pick
            self.set_attach_to_garment(attach_position=pick_point)

            fetch_result = self.franka.fetch_garment_from_sofa(
                self.config.target_positions,
                self.attach,
                error_record_file="Data/Sofa/Retrieve/Record.txt",
            )
            if not fetch_result:
                cprint("fetch current point failed", "red")
                self.recording_camera.stop_judge_contact()
                self.attach.detach()
                self.franka.return_to_initial_position(self.config.initial_position)
                continue

            # stop judge contact with ground thread
            self.recording_camera.stop_judge_contact()

            # detach attach block and open franka's gripper
            self.attach.detach()
            self.franka.open()

            for i in range(100):
                self.world.step(
                    render=True
                )  # render the world to wait the garment fall down

            garment_cur_index = int(self.cur[8:])
            print(f"garment_cur_index: {garment_cur_index}")

            garment_cur_poses = self.garments.get_cur_poses()

            self.garment_index = sofa_judge_final_poses(
                garment_cur_poses,
                garment_cur_index,
                self.garment_index,
                save_path="Data/Sofa/Retrieve/Record.txt",
            )

            for i in range(25):
                self.world.step(
                    render=True
                )  # render the world to wait the garment disappear

            # return to inital position
            # self.franka.return_to_initial_position(self.config.initial_position)

    def random_pick_place(self):
        pick_pc, pick_color = self.point_cloud_camera.get_point_cloud_data(
            sample_flag=True, sample_num=4096
        )
        self.point_cloud_camera.get_rgb_graph()
        pick_point = self.point_cloud_camera.get_random_point()[0]
        place_point = self.point_cloud_camera.get_random_point()[0]
        distance = np.linalg.norm(pick_point - place_point)
        print(f"distance: {distance}")
        while distance < 0.2:
            _, self.ply_count = self.point_cloud_camera.save_pc(pick_pc, pick_color)
            with open("data/Record.txt", "a") as file:
                file.write(
                    f"{pick_point[0]} {pick_point[1]} {pick_point[2]} {place_point[0]} {place_point[1]} {place_point[2]} {self.ply_count} 0 distance_between_points_is_too_close"
                    + "\n"
                )
            pick_pc, pick_color = self.point_cloud_camera.get_point_cloud_data(
                sample_flag=True, sample_num=4096
            )
            pick_point = self.point_cloud_camera.get_random_point()[0]
            place_point = self.point_cloud_camera.get_random_point()[0]
            distance = np.linalg.norm(pick_point - place_point)
            print(f"distance: {distance}")

        cprint(f"pick_point: {pick_point}", "cyan")
        cprint(f"place_point: {place_point}", "cyan")

        pick_ratio = self.point_cloud_camera.get_pc_ratio()
        cprint(f"pick_ratio: {pick_ratio}", "cyan")

        self.set_attach_to_garment(attach_position=pick_point)

        self.config.target_positions[1] = place_point

        fetch_result = self.franka.sofa_pick_place_procedure(
            self.config.target_positions, self.attach
        )

        if not fetch_result:
            cprint("fetch current point failed", "red")
            _, self.ply_count = self.point_cloud_camera.save_pc(pick_pc, pick_color)
            with open("data/Record.txt", "a") as file:
                file.write(
                    f"{pick_point[0]} {pick_point[1]} {pick_point[2]} {place_point[0]} {place_point[1]} {place_point[2]} {self.ply_count} 0 point_unreachable"
                    + "\n"
                )
            # self.attach.detach()
            # self.franka.return_to_initial_position(self.config.initial_position)
            return

        self.attach.detach()
        self.franka.open()
        self.franka.return_to_initial_position(self.config.initial_position)

        place_pc, place_color = self.point_cloud_camera.get_point_cloud_data(
            sample_flag=True, sample_num=4096
        )
        self.point_cloud_camera.get_rgb_graph()
        place_ratio = self.point_cloud_camera.get_pc_ratio()
        cprint(f"place_ratio: {place_ratio}", "cyan")

        if pick_ratio <= place_ratio:
            _, self.ply_count = self.point_cloud_camera.save_pc(pick_pc, pick_color)
            with open("data/Record.txt", "a") as file:
                file.write(
                    f"{pick_point[0]} {pick_point[1]} {pick_point[2]} {place_point[0]} {place_point[1]} {place_point[2]} {self.ply_count} 1 pick_ratio_{pick_ratio}<=place_ratio_{place_ratio}"
                    + "\n"
                )
            _, self.ply_count = self.point_cloud_camera.save_pc(place_pc, place_color)
            with open("data/Record.txt", "a") as file:
                file.write(
                    f"{place_point[0]} {place_point[1]} {place_point[2]} {pick_point[0]} {pick_point[1]} {pick_point[2]} {self.ply_count} 0"
                    + "\n"
                )
        else:
            _, self.ply_count = self.point_cloud_camera.save_pc(pick_pc, pick_color)
            with open("data/Record.txt", "a") as file:
                file.write(
                    f"{pick_point[0]} {pick_point[1]} {pick_point[2]} {place_point[0]} {place_point[1]} {place_point[2]} {self.ply_count} 0"
                    + "\n"
                )
            _, self.ply_count = self.point_cloud_camera.save_pc(place_pc, place_color)
            with open("data/Record.txt", "a") as file:
                file.write(
                    f"{place_point[0]} {place_point[1]} {place_point[2]} {pick_point[0]} {pick_point[1]} {pick_point[2]} {self.ply_count} 1 pick_ratio_{pick_ratio}>place_ratio_{place_ratio}"
                    + "\n"
                )

    def random_pick_model_place(self):
        pick_pc, pick_color = self.point_cloud_camera.get_point_cloud_data(
            sample_flag=True, sample_num=4096
        )
        # self.point_cloud_camera.get_rgb_graph()
        pick_ratio = self.point_cloud_camera.get_pc_ratio()
        cprint(f"pick_ratio: {pick_ratio}", "cyan")
        if pick_ratio > 0.6:
            return
        self.point_cloud_camera.get_rgb_graph()
        pick_point = self.point_cloud_camera.get_random_point()[0]
        place_point = self.point_cloud_camera.get_place_point(
            pick_point=pick_point, pc=pick_pc
        )

        print(f"pick_point: {pick_point}")
        print(f"place_point: {place_point}")

        self.set_attach_to_garment(attach_position=pick_point)

        self.config.target_positions[1] = place_point

        fetch_result = self.franka.sofa_pick_place_procedure(
            self.config.target_positions, self.attach
        )

        if not fetch_result:
            cprint("fetch current point failed", "red")
            _, self.ply_count = self.point_cloud_camera.save_pc(pick_pc, pick_color)
            with open("data/Record.txt", "a") as file:
                file.write(
                    f"{pick_point[0]} {pick_point[1]} {pick_point[2]} {self.ply_count} 0 point_unreachable"
                    + "\n"
                )
            # self.attach.detach()
            # self.franka.return_to_initial_position(self.config.initial_position)
            return

        self.attach.detach()
        self.franka.open()
        self.franka.return_to_initial_position(self.config.initial_position)

        place_pc, place_color = self.point_cloud_camera.get_point_cloud_data(
            sample_flag=True, sample_num=4096
        )
        self.point_cloud_camera.get_rgb_graph()
        place_ratio = self.point_cloud_camera.get_pc_ratio()
        cprint(f"place_ratio: {place_ratio}", "cyan")

        if place_ratio - pick_ratio > 0.1 or place_ratio > 0.6:
            _, self.ply_count = self.point_cloud_camera.save_pc(pick_pc, pick_color)
            with open("data/Record.txt", "a") as file:
                file.write(
                    f"{pick_point[0]} {pick_point[1]} {pick_point[2]} {self.ply_count} 1 pick_ratio_{pick_ratio}<=place_ratio_{place_ratio}"
                    + "\n"
                )
        else:
            _, self.ply_count = self.point_cloud_camera.save_pc(pick_pc, pick_color)
            with open("data/Record.txt", "a") as file:
                file.write(
                    f"{pick_point[0]} {pick_point[1]} {pick_point[2]} {self.ply_count} 0 pick_ratio_{pick_ratio}>place_ratio_{place_ratio}"
                    + "\n"
                )

    def model_pick_whole_procedure(self):
        """
        Use Aff_model to fetch garment from sofa.
        if affordance is not so good, then
            Use Pick_model and Place_model to adapt the garment.
        """
        self.stir = False

        while True:
            aff_pc, aff_color = self.point_cloud_camera.get_point_cloud_data(
                sample_flag=True, sample_num=4096
            )
            if aff_pc is None:
                cprint("Finish picking all garments", "green", on_color="on_green")
                simulation_app.close()

            if not os.path.exists("Env_Eval/sofa_record.txt"):
                with open("Env_Eval/sofa_record.txt", "w") as f:
                    f.write("result ")
            else:
                with open("Env_Eval/sofa_record.txt", "rb") as file:
                    file.seek(-1, 2)
                    last_char = file.read(1)
                    if last_char == b"\n":
                        with open("Env_Eval/sofa_record.txt", "a") as f:
                            f.write("result ")

            aff_ratio = self.point_cloud_camera.get_pc_ratio()
            cprint(f"aff_ratio: {aff_ratio}", "cyan")

            if aff_ratio >= 0.6 or self.stir:
                # _, self.ply_count = self.point_cloud_camera.save_pc(aff_pc, aff_color)
                # self.point_cloud_camera.get_rgb_graph()
                cprint("affordance is good, begin to fetch garment!", "green")
                # _, self.ply_count = self.point_cloud_camera.save_pc(aff_pc, aff_color)
                pick_point = self.point_cloud_camera.get_model_point()
                # pick_point = self.point_cloud_camera.get_random_point()[0]
                cprint(f"pick_point: {pick_point}", "cyan")
                self.cur = self.point_cloud_camera.get_cloth_picking()
                self.id = self.point_cloud_camera.semantic_id
                cprint(f"picking {self.cur}", "cyan")
                # define thread to judge contact with ground
                judge_thread = threading.Thread(
                    target=self.recording_camera.judge_contact_with_ground
                )
                # begin judge_final_pose thread
                judge_thread.start()

                # set attach block and pick
                self.set_attach_to_garment(attach_position=pick_point)

                print("pick target positions: ", self.config.target_positions)

                fetch_result = self.franka.fetch_garment_from_sofa(
                    self.config.target_positions, self.attach
                )
                if not fetch_result:
                    cprint("fetch current point failed", "red")
                    self.recording_camera.stop_judge_contact()
                    self.attach.detach()
                    self.franka.return_to_initial_position(self.config.initial_position)
                    with open("data/Record.txt", "a") as file:
                        file.write(f"0 point_unreachable" + "\n")
                    continue

                # stop judge contact with ground thread
                self.recording_camera.stop_judge_contact()

                # detach attach block and open franka's gripper
                self.attach.detach()
                self.franka.open()

                for i in range(100):
                    self.world.step(
                        render=True
                    )  # render the world to wait the garment fall down

                garment_cur_index = int(self.cur[8:])
                print(f"garment_cur_index: {garment_cur_index}")

                garment_cur_poses = self.garments.get_cur_poses()

                self.garment_index = sofa_judge_final_poses(
                    garment_cur_poses, garment_cur_index, self.garment_index
                )

                for i in range(25):
                    self.world.step(
                        render=True
                    )  # render the world to wait the garment disappear

                self.stir = False

            else:
                cprint(
                    "affordance is not so good, begin to adapt the garment!", "green"
                )
                pick_point = self.point_cloud_camera.get_pick_point(aff_pc)
                # pick_point = self.point_cloud_camera.get_random_point()[0]
                cprint(f"adaption pick_point: {pick_point}", "cyan")
                place_point = self.point_cloud_camera.get_place_point(
                    pick_point=pick_point, pc=aff_pc
                )

                self.set_attach_to_garment(attach_position=pick_point)

                target_positions = copy.deepcopy(self.config.target_positions)
                target_positions[1] = place_point

                print("adaptation target_positions: ", target_positions)

                fetch_result = self.franka.sofa_pick_place_procedure(
                    target_positions, self.attach
                )

                if not fetch_result:
                    cprint("failed", "red")

                self.attach.detach()
                self.franka.open()
                self.franka.return_to_initial_position(self.config.initial_position)

                self.stir = True


if __name__ == "__main__":

    random_flag = sys.argv[1] == "True"
    if not random_flag:
        model_path = sys.argv[2]
    else:
        model_path = None
    rgb_flag = sys.argv[3] == "True"
    gif_flag = sys.argv[4] == "True"

    env = BaseEnv(
        random_flag=random_flag,
        model_path=model_path,
        rgb_flag=rgb_flag,
        gif_flag=gif_flag,
    )

    # rgb = env.recording_camera.camera.get_rgb()

    # file_name= get_unique_filename("tmp", ".png")

    # from Utils_Project.utils import write_rgb_image

    # write_rgb_image(rgb, file_name)

    # env.model_pick_whole_procedure()

    # env.random_pick_place()

    env.pick_whole_procedure()

    if env.gif_flag:
        env.recording_camera.create_gif(
            save_path=get_unique_filename("Data/Sofa/Retrieve/gif/animation", ".gif")
        )

    # while simulation_app.is_running():
    #     simulation_app.update()


# ---------------------coding ending---------------------#

# Close the Simulation App
simulation_app.close()
