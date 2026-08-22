# SpotMicro Locomotion

Reinforcement learning locomotion for a hand-built SpotMicro quadruped: the physical build,
the URDF to USD conversion that made it simulable, and the Isaac Lab task that trained it
from postural collapse to stable forward walking across 18 documented checkpoints.

Full training history, including the experiments that failed and were rejected, is in
[`docs/checkpoints.md`](docs/checkpoints.md).

## The robot

| | |
|---|---|
| Actuators | 12x MG996R servos, three per leg (hip, thigh, knee) |
| Controller | ESP32-S |
| Servo driver | PCA9685, 16 channel 12-bit PWM |
| IMU | MPU-6050 |
| Input | Wireless PS2 receiver |
| Power | 12 V 4 A supply stepped down to 5 V for the servo rail |
| Mass | 1.5 kg measured |

Electronics were wired and integrated by hand. Firmware and the ROS stack come from
[mike4192/spotMicro](https://github.com/mike4192/spotMicro); the work here was bring-up,
servo calibration, and hardware testing against it, not authoring that firmware.

## The bug that blocked everything

Early training produced nonzero policy outputs and zero motion. Debug output showed the
network was doing something:

```
actions:          [0.706 -0.054 0.162 0.204 0.193 0.757 -0.508 0.05 -0.344 -0.333 0.451 0.411]
obs_base_lin_vel: [0.000, 0.000, 0.000]
```

Nonzero actions with a base velocity pinned at exactly zero is not a policy that has failed
to learn. It is a body that cannot move. Grepping the USD physics layer found the cause:

```
def PhysicsFixedJoint "root_joint"
{
    prepend rel physics:body0 = </spot_micro_rviz>
    prepend rel physics:body1 = </spot_micro_rviz/Geometry/base_link>
}
```

The articulation root was welded to the world. Every policy trained before this was
optimising against a robot bolted in place. Removing the joint immediately produced motion:

```
step 0    obs_base_lin_vel: [-0.875  0.124 -0.692]
step 150  obs_base_lin_vel: [-0.316  0.772 -0.065]
```

The symptom pointed at the network and the cause was in the asset. Checking that the
observation actually responds to the action is cheaper than another training run.

## Getting to a walking gait

After the physics fix, mass and inertia were corrected to the measured 1.5 kg and the
default pose changed from all-zeros to a crouched stance. Training then moved through
standing stability before locomotion.

The step that produced walking was loosening the policy rather than adding reward: action
scale from 0.025 to 0.04, joint position penalty from -5.0 to -3.0. Checkpoint 10 is the
first policy that walks forward.

Everything after that is gait quality: yaw drift, path straightness, foot clearance, and a
persistently weak rear-left leg. Each experiment was promoted only after side-by-side
diagnostic comparison against its parent checkpoint, and several were rejected outright.

**Checkpoint 18, current best baseline:**

```
heading_drift               -0.035
rear_left_foot_xz_activity   0.03
lateral_velocity            -1.0
base_angular_velocity        1.8

yaw mean_abs        1.15 deg
base_y mean_abs     0.0176 m
rear_left  z_range  0.0085
rear_right z_range  0.0200
```

**This is not a solved gait.** Rear-left z-range is less than half rear-right, so the robot
walks with real asymmetry. Two later branches that attacked it, an X-only rear-left stride
reward and a front-right overactivity penalty, both made path and yaw worse and were
rejected. The likely reading is that those penalties targeted a compensating behaviour
rather than the root cause.

## Layout

```
isaac_lab/spot_micro/       the task: env cfg, robot cfg, reward and event terms, PPO cfg
isaac_lab/patches/          reward functions added to Isaac Lab's own spot mdp module
config_snapshots/           the exact flat_env_cfg.py behind each checkpoint and experiment
urdf/                       URDF adapted for Isaac Sim import, with relative mesh paths
docs/checkpoints.md         all 35 training notes, in order
```

Checkpoint notes reference their matching snapshot by name, so any result in the history
can be reproduced with the config that actually produced it. Policy weights are not
included.

## Use

Drop the task into an Isaac Lab checkout and apply the reward patch:

```bash
cp -r isaac_lab/spot_micro \
  <IsaacLab>/source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/

cd <IsaacLab>
git apply <this-repo>/isaac_lab/patches/spot-mdp-custom-rewards.patch
```

Train and replay:

```bash
./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/train.py \
  --task Isaac-Velocity-Flat-SpotMicro-v0

./isaaclab.sh -p scripts/reinforcement_learning/rsl_rl/play.py \
  --task Isaac-Velocity-Flat-SpotMicro-Play-v0 --viz kit
```

`--viz kit` is required to get a window. Recent Isaac Lab defaults to headless when the
flag is absent, and `--headless` is deprecated, so a run with no flag looks identical to a
broken one.

### Building the USD

The converted USD is not committed. Its internal payload references are absolute paths, so
it would not load anywhere but the machine that produced it, and it is one command to
regenerate.

`urdf/spot_micro_isaac.urdf` expects the STL meshes alongside it at `urdf/stl/`. Those come
from the upstream project:

```bash
git clone https://github.com/mike4192/spotMicro /tmp/spotmicro-upstream
cp -r /tmp/spotmicro-upstream/spot_micro_rviz/urdf/stl urdf/stl
```

Then convert, and remove the root joint:

```bash
cd <IsaacLab>
./isaaclab.sh -p scripts/tools/convert_urdf.py \
  <this-repo>/urdf/spot_micro_isaac.urdf  <somewhere>/spot_micro.usd
```

Delete the `PhysicsFixedJoint "root_joint"` block from the generated
`spot_micro.usd/<name>/payloads/Physics/physics.usda`. Without this the base is welded to
the world and no policy can move the robot, which is the failure described above.

Finally, point the task at it. `spot_micro_robot_cfg.py` reads `SPOT_MICRO_USD`:

```bash
export SPOT_MICRO_USD=<somewhere>/spot_micro.usd/<name>/<name>.usda
```

Note that the `.usd` produced by the importer is a directory, not a file; the root layer to
reference is the `.usda` inside it.

## Credits

Robot design, ROS stack, and firmware: [mike4192/spotMicro](https://github.com/mike4192/spotMicro) (MIT).
Simulation and RL framework: [NVIDIA Isaac Lab](https://github.com/isaac-sim/IsaacLab).
The task derives from Isaac Lab's Spot environment, developed by
[The AI Institute](https://theaiinstitute.com/) to specifications from Boston Dynamics.
