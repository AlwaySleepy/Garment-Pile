from omni.isaac.core.utils.prims import is_prim_path_valid, get_prim_at_path
from omni.isaac.core.utils.string import find_unique_string_name
from omni.isaac.core import World
from omni.isaac.core.utils.rotations import euler_angles_to_quat
from omni.isaac.core.prims import XFormPrim
from omni.isaac.core.utils.stage import add_reference_to_stage
import numpy as np
import torch

class Wrap_Wash_Machine:
    def __init__(self, position=torch.tensor, orientation=[0.0, 0.0, 0.0], scale=[1, 1, 1], usd_path=str, prim_path:str="/World/Wash_Machine"):
        self._wm_position = position
        self._wm_orientation = orientation
        self._wm_scale = scale
        self._wm_prim_path = find_unique_string_name(prim_path,is_unique_fn=lambda x: not is_prim_path_valid(x))
        self._wm_usd_path = usd_path

        # add wash_machine to stage
        add_reference_to_stage(self._wm_usd_path, self._wm_prim_path)

        self._wm_prim = XFormPrim(
            self._wm_prim_path, 
            name="Wash_Machine", 
            scale=self._wm_scale, 
            position=self._wm_position, 
            orientation=euler_angles_to_quat(self._wm_orientation, degrees=True)
        )