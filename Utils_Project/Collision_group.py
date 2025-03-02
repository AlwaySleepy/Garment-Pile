import numpy as np
from pxr import UsdGeom, UsdLux, Sdf, Gf, Vt, Usd, UsdPhysics, PhysxSchema

class Collision_Group:
    def __init__(self, stage):
        # ----------define rigid_collision_group---------- #
        # path
        self.rigid_group_path = "/World/collision_group/rigid_group"
        # collision_group
        self.rigid_group = UsdPhysics.CollisionGroup.Define(stage, self.rigid_group_path)
        # filter(define which group can't collide with current group)
        self.filter_rigid = self.rigid_group.CreateFilteredGroupsRel()
        # includer(push object in the group)
        self.collectionAPI_rigid = Usd.CollectionAPI.Apply(self.filter_rigid.GetPrim(), "colliders")

        # ----------define robot_collision_group---------- #
        self.robot_group_path = "/World/collision_group/robot_group"
        self.robot_group = UsdPhysics.CollisionGroup.Define(stage, self.robot_group_path)
        self.filter_robot = self.robot_group.CreateFilteredGroupsRel()
        self.collectionAPI_robot = Usd.CollectionAPI.Apply(self.filter_robot.GetPrim(), "colliders")

        # ----------define garment_collision_group---------- #
        self.garment_group_path = "/World/collision_group/garment_group"
        self.garment_group = UsdPhysics.CollisionGroup.Define(stage, self.garment_group_path)
        self.filter_garment = self.garment_group.CreateFilteredGroupsRel()
        self.collectionAPI_garment = Usd.CollectionAPI.Apply(self.filter_garment.GetPrim(), "colliders")

        # ----------define conveyor_belt_collision_group---------- #
        self.conveyor_belt_group_path = "/World/collision_group/conveyor_belt_group"
        self.conveyor_belt_group = UsdPhysics.CollisionGroup.Define(stage, self.conveyor_belt_group_path)
        self.filter_conveyor_belt = self.conveyor_belt_group.CreateFilteredGroupsRel()
        self.collectionAPI_conveyor_belt = Usd.CollectionAPI.Apply(self.filter_conveyor_belt.GetPrim(), "colliders")

        # ----------define attach_collision_group---------- #
        self.attach_group_path = "/World/collision_group/attach_group"
        self.attach_group = UsdPhysics.CollisionGroup.Define(stage, self.attach_group_path)
        self.filter_attach = self.attach_group.CreateFilteredGroupsRel()
        self.collectionAPI_attach = Usd.CollectionAPI.Apply(self.filter_attach.GetPrim(), "colliders")

        # ----------define helper_collision_group---------- #
        self.helper_group_path = "/World/collision_group/helper_group"
        self.helper_group = UsdPhysics.CollisionGroup.Define(stage, self.helper_group_path)
        self.filter_helper = self.helper_group.CreateFilteredGroupsRel()
        self.collectionAPI_helper = Usd.CollectionAPI.Apply(self.filter_helper.GetPrim(), "colliders")

        # ----------define helper_collision_group, but filter with garments---------- #
        self.special_group_path = "/World/collision_group/special_group"
        self.special_group = UsdPhysics.CollisionGroup.Define(stage, self.special_group_path)
        self.filter_special = self.special_group.CreateFilteredGroupsRel()
        self.collectionAPI_special = Usd.CollectionAPI.Apply(self.filter_special.GetPrim(), "colliders")


        # push objects to different group
        self.collectionAPI_robot.CreateIncludesRel().AddTarget("/World/Franka")
        self.collectionAPI_rigid.CreateIncludesRel().AddTarget("/World/Wash_Machine")
        self.collectionAPI_rigid.CreateIncludesRel().AddTarget("/World/Base")
        self.collectionAPI_rigid.CreateIncludesRel().AddTarget("/World/Room")


        self.collectionAPI_garment.CreateIncludesRel().AddTarget("/World/Garment")
        self.collectionAPI_conveyor_belt.CreateIncludesRel().AddTarget("/World/Conveyor_belt")
        self.collectionAPI_helper.CreateIncludesRel().AddTarget("/World/Washingmechine_Model")
        self.collectionAPI_special.CreateIncludesRel().AddTarget("/World/Washingmechine_Model/cube8")
        self.collectionAPI_special.CreateIncludesRel().AddTarget("/World/Washingmechine_Model/cube9")
        self.collectionAPI_conveyor_belt.CreateIncludesRel().AddTarget("/World/Base")

        self.collectionAPI_helper.CreateIncludesRel().AddTarget("/World/wm_door")



        # allocate the filter attribute of different groups
        self.filter_robot.AddTarget(self.garment_group_path)    # Franka can't collide with garment
        self.filter_attach.AddTarget(self.rigid_group_path)     # Attach Object can't collide with wash_machine
        self.filter_attach.AddTarget(self.garment_group_path)   # Attach Object can't collide with garment
        self.filter_attach.AddTarget(self.robot_group_path)     # Attach Object can't collide with Franka
        self.filter_conveyor_belt.AddTarget(self.rigid_group_path)  #conveyor_belt can't collide with wash_machine
        self.filter_conveyor_belt.AddTarget(self.robot_group_path)  #conveyor_belt can't collide with Franka
        self.filter_conveyor_belt.AddTarget(self.attach_group_path)    #conveyor_belt can't collide with attach Object
        self.filter_conveyor_belt.AddTarget(self.helper_group_path) #conveyor_belt can't collide with washingmachine_model
        self.filter_helper.AddTarget(self.rigid_group_path)  #washingmachine_model can't collide with wash_machine
        self.filter_helper.AddTarget(self.robot_group_path)  #washingmachine_model can't collide with Franka
        self.filter_helper.AddTarget(self.attach_group_path)    #washingmachine_model can't collide with attach Object
        self.filter_special.AddTarget(self.garment_group_path)
        self.filter_special.AddTarget(self.rigid_group_path)
        self.filter_special.AddTarget(self.robot_group_path)
        

        
    def update_after_attach(self):
        # push attachmentblock to the target group
        self.collectionAPI_attach.CreateIncludesRel().AddTarget("/World/AttachmentBlock")
        
        
    def update_after_transportation(self):
        # add garment_group_path to the filter_conveyor_belt
        self.filter_conveyor_belt.AddTarget(self.garment_group_path)


