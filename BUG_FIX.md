# Bug Fix

There are some modifications to isaacsim's backbone code. These are the following:

1. File_Path -> "exts/omni.isaac.motion_generation/omni/isaac/motion_generation/lula/interface_helper.py"

Replace the following code:

```python
    def set_robot_base_pose(self, robot_position: np.array, robot_orientation: np.array) -> None:
        """Update position of the robot base. Until this function is called, Lula will assume the base pose
        to be at the origin with identity rotation.

        Args:
            robot_position (np.array): (3 x 1) translation vector describing the translation of the robot base relative to the USD stage origin.
                The translation vector should be specified in the units of the USD stage
            robot_orientation (np.array): (4 x 1) quaternion describing the orientation of the robot base relative to the USD stage global frame
        """
        # all object poses are relative to the position of the robot base
        robot_position = robot_position * self._meters_per_unit
        robot_rot = quats_to_rot_matrices(robot_orientation)

        if np.any(self._robot_pos - robot_position) or np.any(self._robot_rot - robot_rot):
            self._robot_base_moved = True
        else:
            self._robot_base_moved = False

        self._robot_pos = robot_position
        self._robot_rot = robot_rot
```

to this:

```python
    def set_robot_base_pose(self, robot_position: np.array, robot_orientation: np.array)->None:
        """Update position of the robot base. Until this function is called, Lula will assume the base pose
        to be at the origin with identity rotation.

        Args:
            robot_position (np.array): (3 x 1) translation vector describing the translation of the robot base relative to the USD stage origin.
                The translation vector should be specified in the units of the USD stage
            robot_orientation (np.array): (4 x 1) quaternion describing the orientation of the robot base relative to the USD stage global frame
        """
        import torch

        if isinstance(robot_position, list):
            robot_position = np.array(robot_position)

        # all object poses are relative to the position of the robot base
        robot_position = robot_position * self._meters_per_unit
        robot_rot = quats_to_rot_matrices(robot_orientation)

        if isinstance(robot_position, torch.Tensor):
            robot_position = robot_position.numpy()
        if isinstance(robot_rot, torch.Tensor):
            robot_rot = robot_rot.numpy()
        if isinstance(self._robot_pos, torch.Tensor):
            self._robot_pos = self._robot_pos.numpy()
        if isinstance(self._robot_rot, torch.Tensor):
            self._robot_rot = self._robot_rot.numpy()                  

        if np.any(self._robot_pos - robot_position) or np.any(self._robot_rot - robot_rot):
            self._robot_base_moved = True
        else:
            self._robot_base_moved = False

        self._robot_pos = robot_position
        self._robot_rot = robot_rot
```

2. File_Path -> "exts/omni.isaac.motion_generation/omni/isaac/motion_generation/lula/utils.py"

Replace the following code:

```python
    def set_robot_base_pose(
        self, robot_position: np.array, robot_orientation: np.array
    ) -> None:
        """Update position of the robot base. Until this function is called, Lula will assume the base pose
        to be at the origin with identity rotation.

        Args:
            robot_position (np.array): (3 x 1) translation vector describing the translation of the robot base relative to the USD stage origin.
                The translation vector should be specified in the units of the USD stage
            robot_orientation (np.array): (4 x 1) quaternion describing the orientation of the robot base relative to the USD stage global frame
        """

        # all object poses are relative to the position of the robot base
        robot_position = robot_position * self._meters_per_unit
        robot_rot = quats_to_rot_matrices(robot_orientation)

        if np.any(self._robot_pos - robot_position) or np.any(
            self._robot_rot - robot_rot
        ):
            self._robot_base_moved = True
        else:
            self._robot_base_moved = False

        self._robot_pos = robot_position
        self._robot_rot = robot_rot
```

to this:

```python
    def set_robot_base_pose(
        self, robot_position: np.array, robot_orientation: np.array
    ) -> None:
        """Update position of the robot base. Until this function is called, Lula will assume the base pose
        to be at the origin with identity rotation.

        Args:
            robot_position (np.array): (3 x 1) translation vector describing the translation of the robot base relative to the USD stage origin.
                The translation vector should be specified in the units of the USD stage
            robot_orientation (np.array): (4 x 1) quaternion describing the orientation of the robot base relative to the USD stage global frame
        """
        import torch

        if isinstance(robot_position, list):
            robot_position = np.array(robot_position)

        # all object poses are relative to the position of the robot base
        robot_position = robot_position * self._meters_per_unit
        robot_rot = quats_to_rot_matrices(robot_orientation)

        if isinstance(robot_position, torch.Tensor):
            robot_position = robot_position.numpy()
        if isinstance(robot_rot, torch.Tensor):
            robot_rot = robot_rot.numpy()
        if isinstance(self._robot_pos, torch.Tensor):
            self._robot_pos = self._robot_pos.numpy()
        if isinstance(self._robot_rot, torch.Tensor):
            self._robot_rot = self._robot_rot.numpy()

        if np.any(self._robot_pos - robot_position) or np.any(
            self._robot_rot - robot_rot
        ):
            self._robot_base_moved = True
        else:
            self._robot_base_moved = False

        self._robot_pos = robot_position
        self._robot_rot = robot_rot
```
