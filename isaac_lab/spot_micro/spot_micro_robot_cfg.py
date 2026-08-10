import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg

import os

# Point this at your converted USD. Note that the .usd produced by IsaacLab's
# convert_urdf.py is a DIRECTORY, and the root layer to reference is the .usda
# inside it. See the repository README for the conversion step.
SPOT_MICRO_USD = os.environ.get(
    "SPOT_MICRO_USD",
    os.path.expanduser("~/spotMicro/spot_micro_rviz/usd/spot_micro_merged.usd/spot_micro_isaac/spot_micro_isaac.usda"),
)

SPOT_MICRO_JOINTS = [
    "front_left_shoulder",
    "front_right_shoulder",
    "rear_left_shoulder",
    "rear_right_shoulder",
    "front_left_leg",
    "front_right_leg",
    "rear_left_leg",
    "rear_right_leg",
    "front_left_foot",
    "front_right_foot",
    "rear_left_foot",
    "rear_right_foot",
]

SPOT_MICRO_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=SPOT_MICRO_USD,
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=100.0,
            max_angular_velocity=100.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False,
            solver_position_iteration_count=4,
            solver_velocity_iteration_count=0,
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.42),
        joint_pos={
            # shoulder / hip roll joints
            "front_left_shoulder": 0.15,
            "front_right_shoulder": -0.15,
            "rear_left_shoulder": 0.15,
            "rear_right_shoulder": -0.15,

            # upper leg / thigh pitch joints
            "front_left_leg": 0.75,
            "front_right_leg": 0.75,
            "rear_left_leg": 0.75,
            "rear_right_leg": 0.75,

            # lower leg / knee-like joints
            "front_left_foot": -1.20,
            "front_right_foot": -1.20,
            "rear_left_foot": -1.20,
            "rear_right_foot": -1.20,
        },
        joint_vel={".*": 0.0},
    ),
    actuators={
        "legs": ImplicitActuatorCfg(
            joint_names_expr=SPOT_MICRO_JOINTS,
            effort_limit_sim=80.0,
            velocity_limit_sim=40.0,
            stiffness=300.0,
            damping=20.0,
        ),
    },
)
