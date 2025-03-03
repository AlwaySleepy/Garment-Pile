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


class Wrap_busket:
    def __init__(
        self,
        position=torch.tensor,
        orientation=[0.0, 0.0, 0.0],
        scale=[1, 1, 1],
        usd_path=str,
        prim_path: str = "/World/room",
    ):
        self._busket_position = position
        self._busket_orientation = orientation
        self._busket_scale = scale
        self._busket_prim_path = find_unique_string_name(
            prim_path, is_unique_fn=lambda x: not is_prim_path_valid(x)
        )
        self._busket_usd_path = usd_path

        # add wash_machine to stage
        add_reference_to_stage(self._busket_usd_path, self._busket_prim_path)

        self._busket_prim = XFormPrim(
            self._busket_prim_path,
            name="Busket",
            scale=self._busket_scale,
            position=self._busket_position,
            orientation=euler_angles_to_quat(self._busket_orientation, degrees=True),
        )


class Wrap_base:
    def __init__(
        self,
        position=torch.tensor,
        orientation=[0.0, 0.0, 0.0],
        scale=[1, 1, 1],
        usd_path=str,
        prim_path: str = "/World/room",
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
