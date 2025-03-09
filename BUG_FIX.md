# Bug Fix

There are some modifications to isaacsim's backbone code. These are the following (you can ):

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
    def get_pose_rel_robot_base(trans, rot, robot_pos, robot_rot):
        inv_rob_rot = robot_rot.T

        if trans is not None:
            trans_rel = inv_rob_rot @ (trans - robot_pos)
        else:
            trans_rel = None

        if rot is not None:
            rot_rel = inv_rob_rot @ rot
        else:
            rot_rel = None

        return trans_rel, rot_rel
```

to this:

```python
    def get_pose_rel_robot_base(trans, rot, robot_pos, robot_rot):
        import torch
        import numpy as np
        inv_rob_rot = robot_rot.T
        if isinstance(robot_pos, torch.Tensor):
            robot_pos = robot_pos.numpy()

        if trans is not None:
            result = trans - robot_pos
            if isinstance(result, np.ndarray):
                trans_rel = inv_rob_rot @ result
            elif isinstance(result, torch.Tensor):
                trans_rel = inv_rob_rot @ result.numpy()
        else:
            trans_rel = None

        if rot is not None:
            rot_rel = inv_rob_rot @ rot
        else:
            rot_rel = None

        return trans_rel, rot_rel
```

3. File Path -> "exts/omni.isaac.motion_generation/omni/isaac/motion_generation/lula/world.py"

Replace the following code:

```python
    def add_cuboid(
        self,
        cuboid: Union[objects.cuboid.DynamicCuboid, objects.cuboid.FixedCuboid, objects.cuboid.VisualCuboid],
        static: Optional[bool] = False,
        robot_pos: Optional[np.array] = np.zeros(3),
        robot_rot: Optional[np.array] = np.eye(3),
    ):
        """Add a block obstacle.

        Args:
            cuboid (core.objects.cuboid): Wrapper object for handling rectangular prism Usd Prims.
            static (bool, optional): If True, indicate that cuboid will never change pose, and may be ignored in internal
                world updates. Since Lula specifies object positions relative to the robot's frame
                of reference, static obstacles will have their positions queried any time that
                set_robot_base_pose() is called.  Defaults to False.


        Returns:
            bool: Always True, indicating that this adder has been implemented
        """

        if cuboid in self._static_obstacles or cuboid in self._dynamic_obstacles:
            carb.log_warn(
                "A cuboid was added twice to a Lula based MotionPolicy.  This has no effect beyond adding the cuboid once."
            )
            return False

        side_lengths = cuboid.get_size() * cuboid.get_local_scale() * self._meters_per_unit

        trans, rot = get_prim_pose_in_meters_rel_robot_base(cuboid, self._meters_per_unit, robot_pos, robot_rot)

        lula_cuboid = lula.create_obstacle(lula.Obstacle.Type.CUBE)
        lula_cuboid.set_attribute(lula.Obstacle.Attribute.SIDE_LENGTHS, side_lengths.astype(np.float64))
        lula_cuboid_pose = get_pose3(trans, rot)
        world_view = self._world.add_world_view()
        lula_cuboid_handle = self._world.add_obstacle(lula_cuboid, lula_cuboid_pose)
        world_view.update()

        if static:
            self._static_obstacles[cuboid] = lula_cuboid_handle
        else:
            self._dynamic_obstacles[cuboid] = lula_cuboid_handle

        return True
```

to this:

```python
    def add_cuboid(
        self,
        cuboid: Union[objects.cuboid.DynamicCuboid, objects.cuboid.FixedCuboid, objects.cuboid.VisualCuboid],
        static: Optional[bool] = False,
        robot_pos: Optional[np.array] = np.zeros(3),
        robot_rot: Optional[np.array] = np.eye(3),
    ):
        """Add a block obstacle.

        Args:
            cuboid (core.objects.cuboid): Wrapper object for handling rectangular prism Usd Prims.
            static (bool, optional): If True, indicate that cuboid will never change pose, and may be ignored in internal
                world updates. Since Lula specifies object positions relative to the robot's frame
                of reference, static obstacles will have their positions queried any time that
                set_robot_base_pose() is called.  Defaults to False.


        Returns:
            bool: Always True, indicating that this adder has been implemented
        """
        import torch
        if cuboid in self._static_obstacles or cuboid in self._dynamic_obstacles:
            carb.log_warn(
                "A cuboid was added twice to a Lula based MotionPolicy.  This has no effect beyond adding the cuboid once."
            )
            return False

        side_lengths = cuboid.get_size() * cuboid.get_local_scale() * self._meters_per_unit

        trans, rot = get_prim_pose_in_meters_rel_robot_base(cuboid, self._meters_per_unit, robot_pos, robot_rot)

        lula_cuboid = lula.create_obstacle(lula.Obstacle.Type.CUBE)
        if isinstance(side_lengths, torch.Tensor):
            side_lengths = side_lengths.numpy()
        lula_cuboid.set_attribute(lula.Obstacle.Attribute.SIDE_LENGTHS, side_lengths.astype(np.float64))
        lula_cuboid_pose = get_pose3(trans, rot)
        world_view = self._world.add_world_view()
        lula_cuboid_handle = self._world.add_obstacle(lula_cuboid, lula_cuboid_pose)
        world_view.update()

        if static:
            self._static_obstacles[cuboid] = lula_cuboid_handle
        else:
            self._dynamic_obstacles[cuboid] = lula_cuboid_handle

        return True
```

4. File Path -> "exts/omni.isaac.core/omni/isaac/core/utils/torch/tensor.py"

Replace the following code:

```python
def expand_dims(data, axis):
    return torch.unsqueeze(data, axis)
```

to this:

```python
def expand_dims(data, axis):
    import numpy as np
    if isinstance(data, np.ndarray):
        data = torch.Tensor(data)
    elif isinstance(data, list): 
        data = torch.tensor(data)
    return torch.unsqueeze(data, axis)
```

5. File Path -> "exts/omni.isaac.core/omni/isaac/core/controllers/articulation_controller.py"

Replace the following code:

```python
    def apply_action(self, control_actions: ArticulationAction) -> None:
        """[summary]

        Args:
            control_actions (ArticulationAction): actions to be applied for next physics step.
            indices (Optional[Union[list, np.ndarray]], optional): degree of freedom indices to apply actions to.
                                                                   Defaults to all degrees of freedom.

        Raises:
            Exception: [description]
        """
        applied_actions = self.get_applied_action()
        joint_positions = control_actions.joint_positions
        if control_actions.joint_positions is not None:
            joint_positions = self._articulation_view._backend_utils.convert(
                control_actions.joint_positions, device=self._articulation_view._device
            )
            joint_positions = self._articulation_view._backend_utils.expand_dims(joint_positions, 0)
            if control_actions.joint_indices is None:
                for i in range(control_actions.get_length()):
                    if joint_positions[0][i] is None or np.isnan(
                        self._articulation_view._backend_utils.to_numpy(joint_positions[0][i])
                    ):
                        joint_positions[0][i] = applied_actions.joint_positions[i]
        joint_velocities = control_actions.joint_velocities
        if control_actions.joint_velocities is not None:
            joint_velocities = self._articulation_view._backend_utils.convert(
                control_actions.joint_velocities, device=self._articulation_view._device
            )
            joint_velocities = self._articulation_view._backend_utils.expand_dims(joint_velocities, 0)
            if control_actions.joint_indices is None:
                for i in range(control_actions.get_length()):
                    if joint_velocities[0][i] is None or np.isnan(joint_velocities[0][i]):
                        joint_velocities[0][i] = applied_actions.joint_velocities[i]
        joint_efforts = control_actions.joint_efforts
        if control_actions.joint_efforts is not None:
            joint_efforts = self._articulation_view._backend_utils.convert(
                control_actions.joint_efforts, device=self._articulation_view._device
            )
            if np.all(np.isnan(joint_efforts)):
                joint_efforts = None
            else:
                joint_efforts = self._articulation_view._backend_utils.expand_dims(joint_efforts, 0)

        self._articulation_view.apply_action(
            ArticulationActions(
                joint_positions=joint_positions,
                joint_velocities=joint_velocities,
                joint_efforts=joint_efforts,
                joint_indices=control_actions.joint_indices,
            )
        )
        return
```

to this:

```python
    def apply_action(self, control_actions: ArticulationAction) -> None:
        """[summary]

        Args:
            control_actions (ArticulationAction): actions to be applied for next physics step.
            indices (Optional[Union[list, np.ndarray]], optional): degree of freedom indices to apply actions to.
                                                                   Defaults to all degrees of freedom.

        Raises:
            Exception: [description]
        """
        applied_actions = self.get_applied_action()
        joint_positions = control_actions.joint_positions
        if control_actions.joint_positions is not None:
            for i in range(len(joint_positions)):
                if joint_positions[i] is None:
                    joint_positions[i] = -100.0
            joint_positions = self._articulation_view._backend_utils.convert(
                control_actions.joint_positions, device=self._articulation_view._device
            )
            joint_positions = self._articulation_view._backend_utils.expand_dims(joint_positions, 0)
            if control_actions.joint_indices is None:
                for i in range(control_actions.get_length()):
                    if joint_positions[0][i] == -100.0 or np.isnan(
                        self._articulation_view._backend_utils.to_numpy(joint_positions[0][i])
                    ):
                        joint_positions[0][i] = applied_actions.joint_positions[i]
        joint_velocities = control_actions.joint_velocities
        if control_actions.joint_velocities is not None:
            joint_velocities = self._articulation_view._backend_utils.convert(
                control_actions.joint_velocities, device=self._articulation_view._device
            )
            joint_velocities = self._articulation_view._backend_utils.expand_dims(joint_velocities, 0)
            if control_actions.joint_indices is None:
                for i in range(control_actions.get_length()):
                    if joint_velocities[0][i] is None or np.isnan(joint_velocities[0][i]):
                        joint_velocities[0][i] = applied_actions.joint_velocities[i]
        joint_efforts = control_actions.joint_efforts
        if control_actions.joint_efforts is not None:
            joint_efforts = self._articulation_view._backend_utils.convert(
                control_actions.joint_efforts, device=self._articulation_view._device
            )
            if np.all(np.isnan(joint_efforts)):
                joint_efforts = None
            else:
                joint_efforts = self._articulation_view._backend_utils.expand_dims(joint_efforts, 0)

        self._articulation_view.apply_action(
            ArticulationActions(
                joint_positions=joint_positions,
                joint_velocities=joint_velocities,
                joint_efforts=joint_efforts,
                joint_indices=control_actions.joint_indices,
            )
        )
        return
```

6. File Path -> "exts/omni.isaac.franka/omni/isaac/franka/franka.py"

Replace the following code:

```python
usd_path = assets_root_path + "/Isaac/Robots/Franka/franka.usd" # line 60
```

to this:

```python
usd_path = "/home/XXX[change]/Garment-Pile/Assets/Robot/franka.usd"
```