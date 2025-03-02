'''
Create Garment_WashMachine Environment
Include:
    -All components (wash_machine, franka, garment, camera, other helpful parts)
    -Whole Procedure of Project
'''


# Open the Simulation App
import random
import sys
import os

sys.path.append(os.getcwd())
from config import Config
import torch

# from isaacsim import SimulationApp
from omni.isaac.kit import SimulationApp

simulation_app = SimulationApp({"headless":False})

#---------------------coding begin---------------------#
import numpy as np
import omni.replicator.core as rep
import threading
import time
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.rotations import euler_angles_to_quat,quat_to_euler_angles
from omni.physx import acquire_physx_interface
from pxr import UsdGeom, UsdLux, Sdf, Gf, Vt, Usd, UsdPhysics, PhysxSchema
from omni.isaac.core.objects import DynamicCuboid,FixedCuboid
from omni.isaac.sensor import Camera
from omni.kit.viewport.utility import get_active_viewport
from omni.isaac.core.utils.prims import delete_prim, set_prim_visibility
from omni.isaac.core.utils.viewports import set_camera_view

# print(sys.path)

from Robot.WrapFranka import WrapFranka
from Wash_Machine.Wash_Machine import Wrap_Wash_Machine
from Garment.Garment import WrapGarment, Garment
from Utils_Project.utils import add_wm_door, change_door_pos, compare_position_before_and_after, get_unique_filename, judge_final_poses, load_conveyor_belt,  load_washingmachine_model, record_success_failure, write_ply, write_ply_with_colors
from Utils_Project.Collision_group import Collision_Group
from Utils_Project.AttachmentBlock import AttachmentBlock
from Camera.Point_Cloud_Camera import Point_Cloud_Camera
from Camera.Recording_Camera import Recording_Camera
from Model.pointnet2_seg_ssg import get_model
from Model.pointnet2_Place_Model import Place_Model
from Model.pointnet2_Pick_Model import Pick_Model
import Utils_Project.utils as util
from Room.Room import Wrap_base, Wrap_room,Wrap_busket

class WashingMachineEnv():
    def __init__(self,index=0):
        # define the world
        self.world = World(backend="torch", device="cpu")
        set_camera_view(eye=[-1.5, -1.5, 1.5], target=[0.01, 0.01, 0.01], camera_prim_path="/OmniverseKit_Persp")
        self.index=index
        physx_interface = acquire_physx_interface()
        physx_interface.overwrite_gpu_setting(1)  # garment render request

        #define the stage
        self.stage = self.world.stage

        #define the physics context
        self.scene = self.world.get_physics_context()._physics_scene  
        # set gravity
        self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0, 0.0, -1))
        self.scene.CreateGravityMagnitudeAttr().Set(9.8)

        # set default_ground
        self.world.scene.add_default_ground_plane(z_position=-0.05)

        # get environment config
        self.config = Config()

        # set global light
        self.demo_light=rep.create.light(position=[0,0,0],light_type="dome")

        self.disk_light_inside=rep.create.light(position=[0.13459,-0.07683,0.83689],light_type="disk",intensity=3000)

        self.disk_light_inside2=rep.create.light(position=[0.12834,0.17148,0.74336],light_type="disk",intensity=3000)


        # set local light in washing machine
        self.disk_light=rep.create.light(position=[0.2184,0,1.11234],light_type="rect",intensity=15000,rotation=[0,-42,0])

        # load recording_camera (use this camera to generate gif)
        self.recording_camera = Recording_Camera(self.config.recording_camera_position, self.config.recording_camera_orientation)

        # load point_cloud_camera (use this camera to generate point_cloud graph)
        self.point_cloud_camera = Point_Cloud_Camera(self.config.point_cloud_camera_position, self.config.point_cloud_camera_orientation, garment_num=self.config.garment_num)

        # load franka
        self.franka = WrapFranka(self.world, self.config.robot_position, self.config.robot_orientation, prim_path="/World/Franka", robot_name="franka_robot",recording_camera=self.recording_camera)

        # load washing_machine        
        self.wash_machine = Wrap_Wash_Machine(self.config.wm_position, self.config.wm_orientation, self.config.wm_scale, self.config.wm_usd_path, self.config.wm_prim_path)

        # load room
        # self.room = Wrap_room(self.config.room_position, self.config.room_orientation, self.config.room_scale, self.config.room_usd_path, self.config.room_prim_path)

        # load busket
        # self.busket=Wrap_busket(self.config.busket_position,self.config.busket_orientation,self.config.busket_scale,self.config.busket_usd_path,self.config.busket_prim_path)

        #load base
        # self.base=Wrap_base(self.config.base_position,self.config.base_orientation,self.config.base_scale,self.config.base_usd_path,self.config.base_prim_path)


        # load garment
        self.garments = WrapGarment(
            self.stage, 
            self.scene, 
            self.config.garment_num,
            self.config.clothpath,
            self.config.garment_position,
            self.config.garment_orientation,
            self.config.garment_scale
        )

        self.garment_index=[True]*self.config.garment_num

        # load conveyor_belt
        load_conveyor_belt(self.world)


        # load washingmachine_model
        obstacle_list = load_washingmachine_model(self.world)
        # add_wm_door(self.world)
        
        self.door=FixedCuboid(
                    name="wm_door",
                    position=[-0.39497,0.0,0.225],
                    prim_path="/World/wm_door",
                    scale=np.array([0.05,1,0.55]),
                    orientation=euler_angles_to_quat([0,0,0],degrees=True),
                    size=1.0,
                    color=np.array([180,180,180]),
                    visible=False,
                )
        

        # create collision group
        self.collision = Collision_Group(self.stage)
        
        # add obstacle to franka's rmpflow motion, in case that franka can avoid collision with washing machine smartly
        for obstacle in obstacle_list:
            self.franka.add_obstacle(obstacle)
        print("collision add successfully")



    def garment_into_machine(self):
        '''
        Let the clothes float into the washing machine
        by changing the direction of gravity.
        '''
        # change gravity direction
        self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(1.5, 0.0, -1.2))
        self.scene.CreateGravityMagnitudeAttr().Set(8.0)
        for i in range(650):  #2500
            if not simulation_app.is_running():
                simulation_app.close()
            simulation_app.update()
            if i==250:
                self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(1.5, 0.0, -0.3))
                self.scene.CreateGravityMagnitudeAttr().Set(8.0) 
            if i==400:
                self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(1.5, 0.0, 0.05))
                self.scene.CreateGravityMagnitudeAttr().Set(9.8) 
            # print(i)
            if i==550:       #2200
                print("ready to change")
                # return to the normal gravity direction
                self.scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0.0, 0.0, -1))
                self.scene.CreateGravityMagnitudeAttr().Set(9.8) 


    def remove_conveyor_belt(self):
        '''
        remove conveyor belt and its collision group
        '''
        delete_prim("/World/Conveyor_belt")

        change_door_pos(self.door)
        self.world.step(render=True)
        #self.world.play(
        print("Conveyor Belt Removed!")
                
    def create_attach_block(self, init_position=np.array([0.0, 0.0, 1.0])):
        '''
        Create attachment block and update the collision group at the same time.
        '''
        # create attach block and finish attach
        self.attach = AttachmentBlock(self.world, self.stage, "/World/AttachmentBlock", self.garments.garment_mesh_path)
        self.attach.create_block(block_name="attach", block_position=init_position, block_visible=True)
        print("attach finish!")
        # update attach collision group
        self.collision.update_after_attach()
        for i in range(100):
            simulation_app.update()
        print("Update collision group successfully!")
        
    def set_attach_to_garment(self, attach_position):
        '''
        push attach_block to new grasp point and attach to the garment
        '''
        # set the position of block
        self.attach.set_block_position(attach_position)
        # create attach
        self.attach.attach()
        # render the world
        self.world.step(render=True)

    def get_point_cloud_data(self,filename=None):
        '''
        make franka unvisible before taking point_cloud graph
        when finish taking point_cloud_graph, make franka visible
        '''
        # make franka unvisible then get point cloud data
        # set_prim_visibility(self.franka._robot.prim,False)
        for i in range(30):
            self.world.step(render=True)

        self.point_cloud,self.colors=self.point_cloud_camera.get_point_cloud_data()

        if filename is not None:
            write_ply_with_colors(points=self.point_cloud,colors=self.colors,filename=filename)
            print("write into ply file")



    def pick_point(self,random=True):
        '''
        select random point from point_cloud graph and pick
        record corresponding data into .txt file
        '''
        # get pick point
        if random:
            # select pick point randomly
            pick_point = self.point_cloud_camera.get_random_point()
            print(pick_point)
        else:
            # else use model to get pick point
            pick_point,max_value,output=self.point_cloud_camera.get_model_point()
            print(pick_point)

        # filename,self.ply_counter=get_unique_filename(base_filename=f"data/pointcloud/pointcloud",extension=".ply")

        # write_ply_with_colors(points=self.point_cloud,colors=self.colors,filename=filename)
        self.cur=self.point_cloud_camera.get_cloth_picking()
        self.id=self.point_cloud_camera.id
        print(f"picking {self.cur}")
        # record pick point
        print("get position:",pick_point)
        # with open("data/Record.txt", 'a') as file:

        #     file.write(f"{pick_point[0][0]} {pick_point[0][1]} {pick_point[0][2]} {self.ply_counter} ")

        # attach block to pick point
        self.set_attach_to_garment(pick_point)
        # return True
        return pick_point



    def pick_multiple_times(self,):
        '''
        use for multiple garments picking
        '''

        # recording gif
        # thread_rgb = threading.Thread(target= self.recording_camera.get_rgb_graph)
        # thread_rgb.daemon=True
        # thread_rgb.start()

        while(True):
            success=False

            if len(self.point_cloud_camera.get_point_cloud_data())==0:
                break
            pointcloud,rgb=self.point_cloud_camera.get_point_cloud_data()
            # print(pointcloud)
            if not isinstance(pointcloud,np.ndarray):
                pointcloud=np.array(pointcloud)
            # print(pointcloud)
            if len(pointcloud)==0 or pointcloud.ndim != 2 or pointcloud.shape[1] != 3:
                break
            util.flag_record=True

            self.recording_camera.judge=True

            self.get_point_cloud_data()

            pick_point=self.pick_point()


            thread_judge = threading.Thread(target= self.recording_camera.judge_contact_with_ground)
            thread_judge.daemon=True
            thread_judge.start()
            self.franka.fetch_garment_from_washing_machine(self.config.target_positions, self.attach)


            self.recording_camera.judge=False
            garment_cur_index=int(self.cur[8:])

            self.franka.open()
            self.attach.detach()
            for i in range(100):
                self.world.step(render=True)
            
            garment_cur_poses=self.garments.get_cur_poses(self.garment_index)

            # if not util.flag_record:
            self.garment_index,success=judge_final_poses(garment_cur_poses,garment_cur_index,self.garment_index)

            print(f"success flag:{success}")
            filename =get_unique_filename(base_filename=f"data/retrieval/data",extension=".npz")
            np.savez(file=filename, point_cloud=self.point_cloud, pick_point=pick_point, flag=success)
            print(f"save data into {filename}")


        # recording gif
        # self.recording_camera.capture=False
        # self.recording_camera.create_gif()








if __name__=="__main__":

    if not os.path.exists("data/retrieval"):
        os.makedirs("data/retrieval")

    env = WashingMachineEnv()
    set_prim_visibility(env.franka._robot.prim,False)

    env.world.reset()

    env.point_cloud_camera.initialize(env.config.garment_num)

    env.recording_camera.initialize()



    env.garment_into_machine()


    for garment in env.garments.garment_group:
            garment.particle_material.set_particle_friction_scale(3.5)
            garment.particle_material.set_particle_adhesion_scale(1.0)
            garment.particle_material.set_friction(0.2)
            # garment.particle_material.set_damping(5)


    env.remove_conveyor_belt()
    
    env.create_attach_block()

    env.pick_multiple_times()

 
    for i in range(100):
        env.world.step(render=True)



#---------------------coding ending---------------------#

# Close the Simulation App
simulation_app.close()

