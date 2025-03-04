from omni.isaac.core.utils.prims import is_prim_path_valid, get_prim_at_path
from omni.isaac.core.utils.string import find_unique_string_name
from omni.isaac.core import World
from omni.isaac.core.utils.rotations import euler_angles_to_quat
from omni.isaac.core.prims import XFormPrim
from omni.isaac.core.utils.stage import add_reference_to_stage
import numpy as np
import torch


class Wrap_room:
    def __init__(
        self,
        position=torch.tensor,
        orientation=[0.0, 0.0, 0.0],
        scale=[1, 1, 1],
        usd_path=str,
        prim_path: str = "/World/room",
    ):
        self._room_position = position
        self._room_orientation = orientation
        self._room_scale = scale
        self._room_prim_path = find_unique_string_name(
            prim_path, is_unique_fn=lambda x: not is_prim_path_valid(x)
        )
        self._room_usd_path = usd_path

        # add wash_machine to stage
        add_reference_to_stage(self._room_usd_path, self._room_prim_path)

        self._room_prim = XFormPrim(
            self._room_prim_path,
            name="Room",
            scale=self._room_scale,
            position=self._room_position,
            orientation=euler_angles_to_quat(self._room_orientation, degrees=True),
        )


class Wrap_basket:
    def __init__(
        self,
        position=torch.tensor,
        orientation=[0.0, 0.0, 0.0],
        scale=[1, 1, 1],
        usd_path=str,
        prim_path: str = "/World/basket",
    ):
        self._basket_position = position
        self._basket_orientation = orientation
        self._basket_scale = scale
        self._basket_prim_path = find_unique_string_name(
            prim_path, is_unique_fn=lambda x: not is_prim_path_valid(x)
        )
        self._basket_usd_path = usd_path

        # add wash_machine to stage
        add_reference_to_stage(self._basket_usd_path, self._basket_prim_path)

        self._basket_prim = XFormPrim(
            self._basket_prim_path,
            name="Basket",
            scale=self._basket_scale,
            position=self._basket_position,
            orientation=euler_angles_to_quat(self._basket_orientation, degrees=True),
        )


class Wrap_base:
    def __init__(
        self,
        position=torch.tensor,
        orientation=[0.0, 0.0, 0.0],
        scale=[1, 1, 1],
        usd_path=str,
        prim_path: str = "/World/base",
    ):
        self._base_position = position
        self._base_orientation = orientation
        self._base_scale = scale
        self._base_prim_path = find_unique_string_name(
            prim_path, is_unique_fn=lambda x: not is_prim_path_valid(x)
        )
        self._base_usd_path = usd_path

        # add wash_machine to stage
        add_reference_to_stage(self._base_usd_path, self._base_prim_path)

        self._base_prim = XFormPrim(
            self._base_prim_path,
            name="base",
            scale=self._base_scale,
            position=self._base_position,
            orientation=euler_angles_to_quat(self._base_orientation, degrees=True),
        )


class Wrap_chair:
    def __init__(
        self,
        position=torch.tensor,
        orientation=[0.0, 0.0, 0.0],
        scale=[0.08, 0.08, 0.08],
        usd_path=str,
        prim_path: str = "/World/chair",
    ):
        self._chair_position = position
        self._chair_orientation = orientation
        self._chair_scale = scale
        self._chair_prim_path = find_unique_string_name(
            prim_path, is_unique_fn=lambda x: not is_prim_path_valid(x)
        )
        self._chair_usd_path = usd_path

        # add wash_machine to stage
        add_reference_to_stage(self._chair_usd_path, self._chair_prim_path)

        self._chair_prim = XFormPrim(
            self._chair_prim_path,
            name="chair",
            scale=self._chair_scale,
            position=self._chair_position,
            orientation=euler_angles_to_quat(self._chair_orientation, degrees=True),
        )


class Wrap_wash_machine:
    def __init__(
        self,
        position=torch.tensor,
        orientation=[0.0, 0.0, 0.0],
        scale=[1, 1, 1],
        usd_path=str,
        prim_path: str = "/World/Wash_Machine",
    ):
        self._wm_position = position
        self._wm_orientation = orientation
        self._wm_scale = scale
        self._wm_prim_path = find_unique_string_name(
            prim_path, is_unique_fn=lambda x: not is_prim_path_valid(x)
        )
        self._wm_usd_path = usd_path

        # add wash_machine to stage
        add_reference_to_stage(self._wm_usd_path, self._wm_prim_path)

        self._wm_prim = XFormPrim(
            self._wm_prim_path,
            name="Wash_Machine",
            scale=self._wm_scale,
            position=self._wm_position,
            orientation=euler_angles_to_quat(self._wm_orientation, degrees=True),
        )
