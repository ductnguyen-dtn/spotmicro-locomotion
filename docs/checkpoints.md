# Training checkpoints

Working notes kept while training the SpotMicro locomotion policy in Isaac Lab,
from the first broken policy through to the current best confirmed baseline. Each
entry records what changed, why, and what the gait actually looked like, including
the experiments that were rejected.

Per-checkpoint config snapshots are in [`../config_snapshots/`](../config_snapshots/).

---

## Checkpoint 1: Early Broken / Fixed-Root Policy

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-05_05-37-25/model_199.pt

**Description:** This checkpoint was trained before the main physics problems were fixed. At that time, the robot still had a fixed-root/body-locking issue, so the policy was not trained in a physically correct environment. When replayed now, it starts from the same corrected default crouched standing pose as the newest checkpoints because the current USD/config has changed. Therefore, its screenshot should be treated as a replay reference, not an exact historical recreation.

**Visual result:** Starts in the same corrected crouched standing pose as the newest run. The important difference is the policy quality and the old training conditions, not the starting pose.

**Status:** Historical/debug checkpoint only. Not useful for final walking.

---

## Checkpoint 2: After Standing Pose / Action Scale Changes, Still Before Full Physics Fix

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-05_07-11-06/model_299.pt

**Description:** This checkpoint was trained after improving the robot’s default crouched standing pose and reducing the action scale, but before the later mass/inertia correction. At this point, the robot configuration was better than the earliest broken runs, but the simulated physics were still not realistic enough for proper gait learning. When replayed now, it uses the current updated USD/config, so the starting pose may look similar to newer checkpoints.

**Visual result:** The robot starts from the corrected crouched stance, but the policy was trained before the final physics improvements. It may show limited or unstable movement and should be treated as an intermediate debugging checkpoint.

**Status:** Intermediate checkpoint. Not final.

---

## Checkpoint 3: First Visible Movement After Root-Joint Fix

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_04-10-49/model_499.pt

**Description:** This checkpoint was trained after the fixed-root problem was solved by removing the PhysicsFixedJoint "root_joint" from the robot’s USD physics file. This was the first major point where the robot was no longer effectively glued in place. When this checkpoint was loaded in Isaac Sim, the scene finally loaded successfully and the robot could be observed moving in the GUI.

**Visual result:** This was the first checkpoint where visible robot movement was confirmed. The robot did not walk correctly, and the motion was unstable, but it proved that the body was free and the policy could produce physical movement in simulation.

**Important note:** This checkpoint was still trained before the 3 kg mass/inertia correction, so the robot’s movement was not physically realistic yet. It should be documented as the first movement breakthrough, not as a successful walking policy.

**Status:** Major debugging milestone. First confirmed visible movement after removing the root-joint lock, but still not a usable gait.

(SAME PICTURE)

---

## Checkpoint 3: Root Joint Removed, Wrong Mass/Inertia

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_04-10-49/model_499.pt

**Description:** This checkpoint was trained after the major fixed-root problem was discovered and the PhysicsFixedJoint "root_joint" was removed from the USD physics file. This was an important debugging milestone because the robot body was finally able to move freely instead of being effectively locked in place. However, this checkpoint was still trained before the 3 kg mass/inertia patch, so the simulated body weight and inertia were still unrealistic.

**Visual result:** When replayed now, this checkpoint may still look visually similar to Checkpoint 1 and Checkpoint 2 because it is being loaded into the current updated USD/config environment. The screenshot should be treated as a replay reference, not an exact recreation of the original training conditions. Historically, this checkpoint showed that the body could finally move, but the motion was unstable and physically unnatural because the mass/inertia values were still wrong.

**Status:** Important debugging checkpoint. It proved the root-joint fix worked, but it is not useful for final walking because the policy was trained with incorrect mass/inertia.

---

## Checkpoint 4: Corrected 3 kg Mass/Inertia, 1000 Iterations

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_12-24-12/model_999.pt

**Description:** This checkpoint was trained after both major physics fixes were applied: the fixed root_joint was removed and the robot’s mass/inertia values were patched to a more realistic 3 kg simulation target. Numerically, this was a major improvement over the earlier checkpoints. The mean reward became positive, the robot survived full episodes, and the base orientation penalty became much smaller.

**Visual result:** Visually, this checkpoint did not produce a good walking gait. The robot became spread-eagled or locked into a low static posture with little to no useful movement. This showed that even though the training metrics improved, the policy had learned a reward hack: staying stable in a bad posture instead of actually stepping forward.

**Status:** Important physics-corrected checkpoint, but visually failed. Not final.

---

## Checkpoint 5: Corrected 3 kg Mass/Inertia, 1000-Iteration Training

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_12-24-12/model_999.pt

**Description:** This checkpoint was trained after the two major physics fixes were completed: the fixed root_joint was removed, and the robot’s mass/inertia values were patched to a more realistic 3 kg simulation target. Numerically, this was a major improvement compared with the earlier wrong-physics runs. The reward became positive, the robot survived full episodes, and the base orientation penalty became much smaller.

**Replay note:** When replayed now, this checkpoint uses the current updated USD/config environment. Therefore, the screenshot may not perfectly reproduce how it looked at the exact time it was originally trained. The checkpoint stores the trained policy weights, but not the old environment settings.

**Visual result:** This checkpoint showed that the robot could remain stable under the corrected physics, but it did not produce a good walking gait. Earlier visual testing showed a low spread-eagle or locked posture with little useful movement. This revealed a reward-hacking problem: the policy learned to stay stable instead of learning to step forward.

**Status:** Important physics-corrected checkpoint. Numerically much better, but visually not a successful walking policy.

---

## Checkpoint 6: Anti-Sprawl Patch, 300-Iteration Smoke Test

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_12-55-28/model_299.pt

**Description:** This checkpoint was trained after the first anti-sprawl/environment simplification patch. The action scale was reduced to 0.05, the velocity command was reduced to 0.10–0.30 m/s, reset randomization was made calmer, push_robot and add_base_mass were disabled, and the orientation and joint posture penalties were increased. The goal was to stop the robot from learning the low spread-eagle locked pose and make it stay closer to a stable crouched stance.

**Replay note:** When replayed now, this checkpoint uses the current updated USD/config environment. The screenshot should be treated as a visual replay under the current setup, not a perfect reproduction of the exact training environment at the time.

**Visual result:** This checkpoint improved the posture compared with the previous spread-eagle behavior. The robot looked less sprawled and its body looked more parallel to the ground, but it still had a spider-like stance and did not show useful stepping or forward movement.

**Status:** Intermediate tuning checkpoint. It improved stability and reduced the worst sprawl behavior, but it was not yet a walking policy.

---

## Checkpoint 7: Tighter Action Scale and Stronger Joint Posture Penalty

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_13-07-35/model_299.pt

**Description:** This checkpoint was trained after further tightening the policy behavior. The action scale was reduced from 0.05 to 0.025, and the joint position penalty was increased from -2.0 to -5.0. The purpose of this patch was to prevent the policy from moving too far away from the robot’s good default crouched standing pose and to reduce the spider-like locked stance seen in earlier runs.

**Replay note:** When replayed now, this checkpoint uses the current updated USD/config environment. This is also the newest checkpoint currently available, so it is the best visual reference for the latest training direction.

**Visual result:** This checkpoint produced the best standing posture so far. The robot no longer looked severely spread-eagled, and the standing position looked much more decent and closer to the intended crouched stance. However, it still did not yet produce clear stepping or walking behavior. This suggests that the robot has learned a better stable stance, but the next stage needs to focus on controlled leg motion and forward movement.

**Status:** Current best stance checkpoint. Not a walking policy yet, but it is the strongest foundation so far for the next training stage.

---

## Checkpoint 8: Longer Training After Stable-Stance Setup

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_13-46-31/model_999.pt

**Description:** This checkpoint was trained after the robot achieved a much better standing posture using the tighter action scale and stronger joint posture penalty setup. The action scale remained low at 0.025, and the joint position penalty remained strong at -5.0, helping the policy stay closer to the good default crouched stance instead of spreading into a spider-like pose. This run extended training from the previous 300-iteration smoke test to 1000 iterations.

**Training result:** This was the strongest numerical training result so far. The mean reward reached about 13.06, which was a major improvement compared with earlier checkpoints. The robot also showed very low velocity tracking error, with base_velocity/error_vel_xy reaching about 0.0366. The base orientation penalty stayed low at around -0.08, suggesting the body remained stable during training.

**Visual result:** Pending visual evaluation. This checkpoint should be tested to see whether the longer training produced actual stepping, controlled leg motion, or forward movement while preserving the improved standing posture.

**Status:** Current newest checkpoint. Best numerical result so far and the most promising checkpoint to test visually for early stepping or forward motion.

---

## Checkpoint 9: Improved Standing Orientation After Reward Rebalance

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_22-03-22/model_299.pt

**Description:** This checkpoint was trained after adjusting the reward balance to reduce the policy’s tendency to stay frozen in an unhelpful stance. The yaw/angular velocity reward was reduced from 5.0 to 1.0, and the linear velocity tracking reward was made stricter by changing the tracking standard deviation from 1.0 to 0.15. Although this patch changed the velocity reward, the immediate goal was still not full walking. The goal was to improve the robot’s standing orientation and prevent it from settling into a lazy frozen posture.

**Training result:** The training completed successfully with no crash or Python traceback. The mean reward became negative, ending around -7.4, showing that the new reward balance made the task harder. However, the robot still survived full episodes and maintained relatively low velocity tracking error. This means the run was useful to test visually, even though the numerical reward was worse than before.

**Visual result:** This checkpoint produced the best standing orientation so far. The robot only slightly leans forward, and that lean appears closer to the intended ready stance. It stays balanced on its feet and does not collapse or spread badly. This suggests that the reward rebalance helped the robot hold a more useful standing posture.

**Status:** Current best standing-orientation checkpoint. This is not yet a walking checkpoint. The next goal is to preserve this good stance while gradually encouraging small leg motion and controlled weight shifting.

---

## Checkpoint 10: First Successful Walking Policy

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_22-39-19/model_299.pt

**Matching config snapshot path:** source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/spot_micro/flat_env_cfg.py.first_walking_checkpoint10

**Description:** This checkpoint is the first major locomotion breakthrough. Before this point, the robot had improved from collapsing or spreading into a stable standing posture, but it was still mostly frozen and did not produce useful forward movement. After loosening the policy by increasing the action scale from 0.025 to 0.04 and reducing the joint position penalty from -5.0 to -3.0, the robot finally began walking forward in simulation.

**Training setup:** This checkpoint was trained after the improved-standing checkpoint. The goal was not to abandon standing stability, but to slightly loosen the policy so the robot could move its legs while still keeping the improved body orientation. The robot retained a reasonable stance and began producing forward locomotion.

**Visual result:** The robot walks forward, which is a major improvement over the previous frozen standing policies. It does not walk perfectly straight yet. The current gait moves forward while drifting or turning toward the right. This means the project has successfully moved from the “standing and balance” stage into the “direction control and gait refinement” stage.

**Status:** This is the current most important milestone checkpoint. It should be preserved as the first successful walking policy. The next training goal is not simply to make the robot move more, but to make it walk straighter while preserving the good standing posture and forward locomotion.

**Important note for replaying later:** This checkpoint can be rerun later in simulation to record a short video or create a GIF. However, IsaacLab checkpoints store the trained policy weights, not the full historical environment. If the robot config, reward settings, USD physics, or default pose are changed later, replaying this checkpoint may look different. To reproduce this result more accurately, use the matching config snapshot listed above together with the checkpoint.

---

## Checkpoint 11: Straighter-Walk Experiment with Stronger Yaw Control

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_23-03-02/model_299.pt

**Description:** Checkpoint 11 was trained after Checkpoint 10, which was the first successful walking policy. Checkpoint 10 could walk forward, but it drifted or turned to the right. To improve directional control, the yaw/angular velocity reward was increased from 1.0 to 2.0. The purpose of this change was to encourage the robot to keep its body direction straighter when the yaw command is zero, without removing the walking behavior learned in Checkpoint 10.

**Training setup:** The main change was:

base_angular_velocity reward weight: 1.0 → 2.0

The following important settings were kept the same:

action scale = 0.04joint position penalty = -3.0base linear velocity std = 0.15

This was a small and targeted experiment. The goal was not to make the robot move more aggressively, but to improve straightness while preserving the walking behavior from Checkpoint 10.

**Training result:** The numerical training result looked better than Checkpoint 10. The mean reward improved from around -6.2 in Checkpoint 10 to around -4.1 in Checkpoint 11. The yaw error also improved slightly, ending around 0.11–0.13, compared with around 0.14–0.15 before. The robot survived full episodes, and terrain_out_of_bounds stayed at 0.0, meaning the policy remained stable enough to test visually.

**Visual result:** Visually, Checkpoint 11 did not become a better walking checkpoint than Checkpoint 10. The robot took a promising first diagonal step, with the front-right leg and back-left leg moving forward. However, after that first step, it got stuck and did not complete the second diagonal pair using the front-left leg and back-right leg. This suggests that the robot began learning a trot-like diagonal gait pattern but could not complete the full alternating gait cycle.

**Interpretation:** Checkpoint 11 is an important gait-learning checkpoint, but it is not the best walking checkpoint. It shows that stronger yaw control helped numerically, but it may have made the policy more conservative. The robot tried to step in a more structured diagonal pattern, but it hesitated before switching to the opposite diagonal pair.

**Status:** Useful gait-refinement experiment. Checkpoint 10 remains the better walking milestone because it produces continuous forward walking, even though it drifts right. Checkpoint 11 is valuable because it shows the beginning of a diagonal gait pattern, but the gait cycle is incomplete.

---

## Checkpoint 12: Reduced Action-Smoothness Penalty / Gait-Cycle Experiment

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_23-16-47/model_299.pt

Important intermediate checkpoint from same run:logs/rsl_rl/spot_flat/2026-06-08_23-16-47/model_250.pt

**Description:** Checkpoint 12 was trained after observing that Checkpoint 11 could start a diagonal gait but got stuck after the first diagonal step. The robot moved the front-right leg and back-left leg, but it struggled to switch to the front-left and back-right diagonal pair. To help the robot complete the gait cycle, the action-smoothness penalty was reduced.

**Training setup:** The main change was:

action_smoothness penalty: -1.0 → -0.5

The purpose of this change was to punish action changes less severely. A high action-smoothness penalty can make the robot avoid changing joint commands too quickly. That is useful for preventing jerky motion, but it may also prevent the robot from switching leg pairs during a gait cycle. Reducing the penalty gave the robot more freedom to transition from one diagonal pair to the other.

The following important settings were kept:

action scale = 0.04joint position penalty = -3.0base angular velocity reward weight = 2.0base linear velocity std = 0.15

**Training result:** Numerically, this run looked very promising. The mean reward improved significantly, becoming positive at around +1.1 to +1.2. The action-smoothness penalty became much smaller, around -2.3 to -2.4, compared with around -4.1 in the previous run. The robot still survived full episodes, and terrain_out_of_bounds stayed at 0.0, so the training was stable and worth visually testing.

Visual result for model_150.pt:The robot behaved similarly to Checkpoint 11. It took the first diagonal step but then got stuck and did not continue the full gait cycle.

Visual result for model_200.pt:The robot took the first step, then rotated left in place slightly. It still refused or failed to lift the front-left and back-right legs enough to complete the alternating diagonal gait.

Visual result for model_250.pt:The first two steps looked good, but then the robot rotated left in place. This is not a straight-walking success, but it is a useful observation. The behavior may be useful later when training or testing turning behavior, especially left-turn behavior.

Visual result for model_299.pt:The robot walked forward and left. This means the reduced action-smoothness penalty helped the robot continue moving, but it introduced or amplified a left-direction bias. It is more active than Checkpoint 11, but it does not walk straight.

**Interpretation:** Checkpoint 12 shows that reducing the action-smoothness penalty successfully encouraged more motion. However, it also made the robot less directionally stable and caused a leftward walking or turning bias. This suggests that -0.5 may be too loose, while -1.0 may be too restrictive. A future middle value, such as -0.75, may help preserve gait switching without causing too much left rotation.

**Status:** Useful gait-cycle and turning-behavior experiment. Checkpoint 12 is not currently better than Checkpoint 10 for straight walking, but it provides important information. It shows that the robot can become more active when action changes are less heavily punished, and model_250.pt may be useful later as a clue for left-turn training.

---

## Checkpoint 13: Middle Action-Smoothness Experiment

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-08_23-49-21/model_299.pt

**Description:** Checkpoint 13 was trained after comparing Checkpoint 11 and Checkpoint 12. Checkpoint 11 used an action-smoothness penalty of -1.0, which appeared too restrictive because the robot took the first diagonal step but then got stuck. Checkpoint 12 used an action-smoothness penalty of -0.5, which allowed more continuous motion, but it caused the robot to walk or rotate left. Checkpoint 13 tested a middle value of -0.75 to see whether the robot could gain enough freedom to complete the gait cycle without developing as much leftward bias.

**Training setup:** The main change was:

action_smoothness penalty: -0.5 → -0.75

The purpose of this change was to create a compromise between stability and movement. The -1.0 setting discouraged action changes too much, while the -0.5 setting allowed too much motion and left rotation. The -0.75 value was tested as a middle point.

The following important settings were kept:

action scale = 0.04joint position penalty = -3.0base angular velocity reward weight = 2.0base linear velocity std = 0.15foot clearance weight = 0.5

**Training result:** Numerically, Checkpoint 13 behaved exactly like a middle experiment. The mean reward ended around -1.3 to -1.4, which was better than Checkpoint 11 but not as high as Checkpoint 12. The action-smoothness penalty was around -3.2 to -3.4, which also placed it between the stricter Checkpoint 11 and the looser Checkpoint 12. The robot survived full episodes, and terrain_out_of_bounds stayed at 0.0, so the run was stable and safe to test visually.

**Visual result:** Visually, Checkpoint 13 behaved similarly to Checkpoint 11, but with a noticeable improvement. The robot still took the first diagonal step and then struggled to continue, but it appeared to make more effort to move the front-left and back-right legs. It looked like the robot was trying to push through the left-side/opposite diagonal movement, but the knee or foot lift was not high enough to complete the step successfully.

**Interpretation:** Checkpoint 13 suggests that action smoothness is only part of the problem. The middle value helped the robot attempt the second diagonal pair more clearly, but the robot still could not lift the front-left and back-right legs high enough. This points toward foot clearance or leg-lift reward as the next likely bottleneck. The policy may understand that it needs to switch diagonal pairs, but the swing legs do not clear the ground enough to complete the gait cycle.

**Status:** Useful diagnostic checkpoint. Checkpoint 13 is not better than Checkpoint 10 for continuous walking, but it gives a very important clue: the next improvement may require stronger foot-clearance encouragement, not more action-smoothness tuning. This checkpoint marks the transition from “action switching problem” toward “leg lift / foot clearance problem.”

---

## Checkpoint 14: Increased Foot-Clearance Reward Experiment

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-09_00-13-02/model_299.pt

**Description:** Checkpoint 14 was trained after Checkpoint 13 showed that the robot was trying to activate the opposite diagonal pair, especially the front-left and back-right legs, but those legs did not appear to lift high enough to complete the gait cycle. To test whether the issue was related to insufficient foot lift, the foot-clearance reward was increased.

**Training setup:** The main change before this run was:

foot_clearance reward weight: 0.5 → 1.0

The following important settings were kept:

action scale = 0.04joint position penalty = -3.0base angular velocity reward weight = 2.0action_smoothness penalty = -0.75base linear velocity std = 0.15foot clearance target height = 0.1

The purpose of this experiment was to tell the robot to care more about lifting the swing feet, while keeping the target height the same. The target height was not increased yet because asking for too much leg lift too early could make the robot jumpy or unstable.

**Training result:** Numerically, Checkpoint 14 looked better than Checkpoint 13. The mean reward improved from around -1.3 to approximately -0.1 to -0.2. The foot-clearance reward also increased to around 0.97, showing that the robot was receiving much stronger reward for foot-lift behavior. The robot survived full episodes, and terrain_out_of_bounds stayed at 0.0, so the run remained stable during training.

**Visual result:** Visually, Checkpoint 14 did not solve the gait problem. Instead of completing a clean alternating diagonal gait, the robot turned left. This behavior looked similar to Checkpoint 12, where the robot also moved or rotated left after action changes were loosened. Therefore, although the training reward improved, the visual gait was not better.

**Interpretation:** Checkpoint 14 showed that the problem was not simply a lack of foot-clearance reward. Increasing the foot-clearance weight helped numerically, but it pushed the robot back toward left-turning behavior. This suggests that stronger foot lift alone is not enough. The robot still needs better gait rhythm and left-right stride balance.

**Status:** Useful experiment, but not a better walking checkpoint. Checkpoint 14 should be documented as evidence that increasing foot_clearance from 0.5 to 1.0 improved numerical reward but caused left-turn behavior visually. The next direction was to restore foot clearance back to 0.5 and test a softer yaw-control value.

---

## Checkpoint 15: Config Snapshot for Future Continuation

**Checkpoint 15 policy path:** logs/rsl_rl/spot_flat/2026-06-09_00-35-10/model_299.pt

**Matching config snapshot path:** source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/spot_micro/flat_env_cfg.py.checkpoint15_yaw15_as075_foot05

**Why this config was saved:** This config snapshot was saved because Checkpoint 15 produced meaningful forward movement. The robot still rotated left because the left-front stride was shorter than the right-side stride, but it moved forward a good amount. Since this is a useful training direction, the matching config was preserved before continuing any further experiments.

**Checkpoint 15 key settings:** base angular velocity reward weight = 1.5action_smoothness penalty = -0.75foot_clearance reward weight = 0.5action scale = 0.04joint position penalty = -3.0base linear velocity std = 0.15

**Important note:** If future experiments become worse, this config snapshot can be restored together with the Checkpoint 15 policy path. This helps reproduce the forward-moving but left-rotating gait for continued debugging.

---

## Checkpoint 15: Reduced Yaw Control / Forward-Left Asymmetric Gait

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-09_00-35-10/model_299.pt

**Description:** Checkpoint 15 was trained after Checkpoint 14 showed left-turn behavior when the foot-clearance reward was increased to 1.0. Since stronger foot clearance did not solve the gait problem and seemed to bring back left turning, the foot-clearance reward was restored to 0.5. The yaw/angular velocity reward was also reduced from 2.0 to 1.5 to test whether slightly weaker yaw control would allow smoother gait development without making the robot too stiff during diagonal leg switching.

**Training setup:** The main changes before this run were:

base angular velocity reward weight: 2.0 → 1.5foot_clearance reward weight: 1.0 → 0.5

The following important settings were kept:

action scale = 0.04joint position penalty = -3.0action_smoothness penalty = -0.75base linear velocity std = 0.15

The purpose of this experiment was to find a middle point between the earlier checkpoints. A yaw reward of 1.0 allowed continuous walking but with right drift, while a yaw reward of 2.0 improved yaw numerically but made the gait more stiff or incomplete. The 1.5 value was tested as a compromise.

**Training result:** Numerically, this run completed successfully and stayed stable. The robot survived full episodes, and terrain_out_of_bounds remained 0.0. The mean reward ended around -2.4 to -2.5, which was worse than Checkpoint 13 but still much better than some earlier failed policies. The yaw error ended around 0.11, which was acceptable, and the velocity tracking error stayed reasonably low. This made the checkpoint worth visual testing even though the reward was not the best.

**Visual result:** Visually, Checkpoint 15 showed useful forward movement. The robot moved forward a good amount, but the gait was asymmetric. The left-front leg had a shorter stride than the right-side gait stride. Because the right side appeared to move more strongly than the left-front side, the robot moved forward while also rotating left. This was not a clean straight gait, but it showed that the robot was producing meaningful forward locomotion.

**Interpretation:** Checkpoint 15 shows that the main issue has become a left-right stride balance problem. The robot is no longer simply falling, freezing, or failing to move. It can move forward, but the stride lengths are uneven. The shorter left-front stride causes the body to rotate left while moving forward. This suggests that future improvements may need to focus on gait symmetry and balanced diagonal stepping, not only yaw reward, action smoothness, or foot clearance separately.

**Status:** Useful forward-motion checkpoint, but not the best straight-walking policy yet. Checkpoint 10 remains the first major continuous walking milestone, while Checkpoint 15 provides a clearer diagnosis of the current gait problem: asymmetric stride length, especially the shorter left-front stride. The next step should be to compare earlier checkpoints from this same run, such as model_250.pt, to see whether there is a better balance between forward motion and left rotation.

---

## Checkpoint 16: Continued Training from Checkpoint 15 / Straighter Walking with Rear-Left Drag

**Checkpoint path:** logs/rsl_rl/spot_flat/2026-06-09_01-01-51/model_898.pt

**Continued from:** logs/rsl_rl/spot_flat/2026-06-09_00-35-10/model_299.pt

**Matching Checkpoint 15 config snapshot path:** source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/spot_micro/flat_env_cfg.py.checkpoint15_yaw15_as075_foot05

**Matching Checkpoint 16 config snapshot path:** source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/spot_micro/flat_env_cfg.py.checkpoint16_straight_rearleft_drag

**Description:** Checkpoint 16 was created by continuing training from Checkpoint 15. Checkpoint 15 produced meaningful forward movement, but the robot rotated left because the left-front stride was shorter than the right-side stride. The goal of continuing training was to see whether the policy could improve its stride balance over more iterations while keeping the forward movement learned in Checkpoint 15.

**Training setup:** This run continued from the Checkpoint 15 policy instead of starting completely from scratch. The key settings were:

base angular velocity reward weight = 1.5action_smoothness penalty = -0.75foot_clearance reward weight = 0.5action scale = 0.04joint position penalty = -3.0base linear velocity std = 0.15

The purpose was to preserve the useful forward-moving gait from Checkpoint 15 and give the model more training time to improve direction control and stride balance.

**Training result:** The continued-training run reached model_898.pt. Near the end of training, the robot survived full episodes and did not go out of bounds. The velocity tracking error was low, and the yaw error stayed reasonably controlled. The numerical results suggested that the policy had become more stable and was worth testing visually.

**Visual result:** Visually, Checkpoint 16 walked straighter than the previous checkpoints. This was a major improvement over Checkpoint 15, which moved forward but rotated left. However, a new issue appeared: the back-left leg was not really being used. It looked like the robot was dragging the back-left leg along instead of actively lifting and stepping with it.

**Interpretation:** Checkpoint 16 is likely the best straight-walking direction so far, but the gait is still not healthy or balanced. The policy seems to have found a way to move forward more straight by relying mostly on the other legs, while the rear-left leg contributes very little. This means the main problem has shifted again: it is no longer mainly a direction-control problem, but a rear-left leg engagement and gait-balance problem.

**Status:** Current best straight-walking checkpoint, but not the final gait. It should be preserved as an important milestone because it shows the first clear improvement toward straighter forward walking. The next experiment is to gently increase foot-clearance reward from 0.5 to 0.7, aiming to encourage the rear-left leg to lift and participate more without returning to the stronger 1.0 foot-clearance setting that previously caused left-turn behavior.

---

## Checkpoint 17: Camera Fix

Problem:

The camera snaps back to a fixed isometric-like robot-following view when I try to manually rotate or pan.

My hypothesis:

The viewer configuration is attached to the robot root, so IsaacLab keeps resetting the camera relative to the robot instead of letting me freely inspect from other angles.

Why I think this:

The config contains ViewerCfg with origin_type="asset_root" and asset_name="robot", which suggests the camera is following the robot. Visually, the camera keeps returning to the same robot-centered view.

Change I will test:

Change the viewer behavior so the camera is less locked to the robot-following view.

Expected result:

I should be able to rotate and inspect the robot from the rear, side, and diagonal angles without the view snapping back immediately.

How I will verify:

Replay Checkpoint 17 again and manually rotate the camera around the robot. If the camera stays where I place it long enough to inspect the rear legs, the change worked.

---

## Checkpoint 17: Experiment: Base-relative foot-height diagnostic

**Run name:** Base-relative foot-height diagnostic

**Checkpoint:** 2026-06-09_03-07-45/model_1000.pt

**Code/config changed:** Only the diagnostic script, if needed:

~/IsaacLab/scripts/reinforcement_learning/rsl_rl/record_spot_micro_policy.py

No reward, training, policy, physics, observation, or action configuration change.

**Hypothesis:** rear_left_foot_link will still have a lower maximum vertical position relative to base_link than the other three feet.

**Why I think this:** The previous world-frame diagnostic showed that the rear-left foot had the lowest maximum and lowest mean height in both episodes. However, world-frame height can also be affected by base height, body roll, and body pitch.

**Expected behavior:** If the rear-left leg itself is moving lower relative to the robot body, the base-relative foot-height data should still show a lower rear-left maximum than the other feet.

**Actual behavior:** Not measured yet.

**Visual observation:** The rear-left leg appears to lift less clearly than the other legs. This is a visual observation only.

**Quantitative evidence:** Not collected yet for base-relative foot height.

**What this experiment is testing:** Whether the rear-left vertical asymmetry comes from the leg’s motion relative to the body, rather than only from whole-body height, roll, or pitch.

**What would support the hypothesis:** rear_left_foot_link has a lower maximum base-relative vertical position than the other feet in both episodes.

**What would disprove the hypothesis:** The rear-left base-relative maximum is similar to the other feet, suggesting that the lower world-frame height may be caused mainly by body orientation or base motion.

**Keep/reject:** Not applicable. This is a diagnostic-only experiment.

**Next experiment:** Measure all four foot positions relative to base_link during steady walking and compare minimum, maximum, range, and mean for each foot.

---

## Checkpoint 17: Experiment: Foot-Height Diagnostic

Run name:

Checkpoint 17 foot-height diagnostic

Checkpoint:

2026-06-09_03-07-45/model_1000.pt

Code/config changed:

Only diagnostic script, if needed. No reward/training config change.

Hypothesis:

Front-right foot has the clearest lift cycle. Front-left and rear feet have lower vertical lift or weaker swing cycles.

Expected behavior:

Foot-height data should show front_right_foot reaching higher z-values than front_left_foot, rear_left_foot, and rear_right_foot.

Actual behavior:

Not measured yet.

Keep/reject:

Not applicable. This is diagnostic only.

Next experiment:

Measure all four foot z-heights over time during replay.

---

## Checkpoint 17: Experiment: Lower Scaled Heading Drift Weight

Experiment - Lower Scaled Heading Drift Weight

Problem:

Scaled heading_drift at -0.05 improved yaw but suppressed rear-left foot motion.

Hypothesis:

The scaled heading penalty was too restrictive. Reducing its weight from -0.05 to -0.02 may preserve some yaw control while allowing rear-left stride/lift to recover.

Change I will test:

heading_drift weight: -0.05 → -0.02

Everything else stays fixed:

rear_left_foot_xz_activity = 0.03

lateral_velocity = -1.0

base_angular_velocity = 1.8

diagonal rewards = 0.0

rear_foot_xz_velocity_symmetry = 0.0

Expected result:

1. yaw mean_abs:

2. rear_left x_range:

3. rear_left z_range:

4. base_y mean_abs:

What could go wrong:

Yaw may worsen again if heading control becomes too weak.

Rear-left motion may still fail to recover.

Path_y may remain worse than CP17.

Verification plan:

Run diagnostic and compare rear_left x_range, rear_left z_range, yaw mean_abs, base_y mean_abs, and visual replay.

---

Actual result:

Reducing scaled heading_drift from -0.05 to -0.02 restored rear-left foot motion. Rear-left x_range improved to 0.0070 / 0.0073 and rear-left z_range improved to 0.0067 / 0.0072. However, yaw mean_abs worsened significantly to 1.7277° / 1.6786°, which is too high for a new checkpoint.

Good signs:

Rear-left stride and lift recovered above the CP17 baseline.

The robot did not lose episode stability.

Base_y mean_abs was moderate at 0.0365 / 0.0386.

Bad signs:

Yaw drift became unacceptable.

Heading control is too weak at -0.02.

Keep or reject:

Reject as new best.

What I learned:

The scaled heading reward has a real tradeoff. At -0.05, yaw is controlled but rear-left movement is suppressed. At -0.02, rear-left movement recovers but yaw control fails. The likely useful range is between -0.02 and -0.05.

Next experiment:

Test scaled heading_drift at -0.035 while keeping rear_left_foot_xz_activity = 0.03 and all other settings fixed.

---

## Checkpoint 17: Experiment: Rear-Left X_Z Activity + Heading Drift Penalty

Run name:

rear_left_xz003_yaw18_heading20_from_current_best

Checkpoint:

logs/rsl_rl/spot_flat/2026-06-16_23-48-06_rear_left_xz003_yaw18_heading20_from_current_best/model_598.pt

Problem:

The previous model improved rear-left activity but learned a step-turn-left exploit.

Hypothesis:

Adding a heading-drift penalty will prevent the robot from rotating away from its starting direction while still allowing some rear-left foot activity improvement.

Why I think this:

The failed lateral-velocity experiment showed that body-frame lateral velocity can be exploited by turning the robot. Heading drift is measured relative to the starting heading, so a 45° turn should be punished directly.

Change tested:

Added heading_drift penalty.

Reduced rear_left_foot_xz_activity from 0.04 to 0.03.

Set lateral_velocity back to -1.0.

Kept base_angular_velocity at 1.8.

Expected result:

The robot should avoid the step-turn-left behavior. Rear-left x/z activity may be lower than the previous activity-only run, but should still improve compared with the current best.

Training signs:

heading_drift reward was small at about -0.0005.

rear_left_foot_xz_activity was about 0.0064.

base velocity yaw error was about 0.1209.

Actual diagnostic result:

Pending.

Keep or reject:

Pending diagnostic and visual replay.

Next step:

Run diagnostic on model_598.pt and compare rear-left x_range, rear-left z_range, yaw mean_abs, and base_y mean_abs.

---

## Checkpoint 17: Experiment: Rear-Left X_Z Activity with Heading-Drift Penalty

Run name:

rear_left_xz003_yaw18_heading20_from_current_best

Checkpoint:

logs/rsl_rl/spot_flat/2026-06-16_23-48-06_rear_left_xz003_yaw18_heading20_from_current_best/model_598.pt

Code/config changed:

Added heading_drift penalty.

Reduced rear_left_foot_xz_activity from 0.04 to 0.03.

Set lateral_velocity back to -1.0.

Kept base_angular_velocity at 1.8.

Kept diagonal rewards and rear_foot_xz_velocity_symmetry off.

Hypothesis:

A heading-drift penalty should reduce the step-turn-left exploit because it punishes yaw change relative to the episode starting heading.

Expected behavior:

Robot should avoid step-turning left while retaining some rear-left stride/lift improvement.

Actual diagnostic behavior:

Rear-left x_range improved moderately to 0.0085 / 0.0084.

Rear-left z_range improved mildly to 0.0069 / 0.0068.

Path base_y mean_abs was decent at 0.0235 / 0.0299.

Yaw mean_abs was too high at 1.4071° / 1.2629°.

Good signs:

Rear-left stride improved compared with current best.

Path_y stayed fairly controlled.

Reward setup was active.

Bad signs:

Yaw drift remained too high.

Rear-left lift improvement was weaker than the lateral20 model.

Training heading_drift reward looked small, but diagnostic yaw was still not good enough.

Keep or reject:

Reject as new best.

What I learned:

Heading-drift reward helped address the exploit conceptually, but this implementation/weight did not protect yaw strongly enough. Training reward values are not proof; diagnostic yaw and visual replay are required.

Next experiment:

Do not continue from this checkpoint. Return to current best. Investigate whether heading_drift reward is measuring the same yaw as the diagnostic, then either strengthen heading_drift or improve the yaw-drift reward implementation.

---

Actual result:

The scaled heading-drift reward successfully reduced yaw mean_abs to 0.7127° / 0.6278°. However, rear-left foot motion collapsed: rear_left x_range dropped to 0.0054 / 0.0055 and rear_left z_range dropped to 0.0044 / 0.0044. Base_y mean_abs also worsened to 0.0439 / 0.0433.

Good signs:

Yaw control improved substantially.

The scaled heading reward was active and effective.

No obvious reward setup mistake.

Bad signs:

Rear-left stride and lift are now worse than the CP17 baseline.

The core rear-left underuse problem was not solved.

Path_y drift worsened.

Keep or reject:

Reject as new best.

What I learned:

A stronger/scaled heading penalty can reduce yaw, but it can also suppress the body and foot motions needed for gait recovery. A good checkpoint must improve yaw and rear-left movement together, not trade one for the other.

Next step:

Do not continue from this checkpoint. Return to CP17 current best. The next experiment should balance heading control with preserving rear-left x/z activity.

---

## Checkpoint 17: Experiment: Scaled Heading Drift Weight 0.035

**Parent checkpoint**

Checkpoint 17 current best model:

logs/rsl_rl/spot_flat/2026-06-15_05-57-07/model_299_better_walk_shape_slight_right_drift_left_yaw.pt

**Run name**

rear_left_xz003_scaled_heading0035_from_current_best

**Final checkpoint tested**

logs/rsl_rl/spot_flat/2026-06-17_06-34-56_rear_left_xz003_scaled_heading0035_from_current_best/model_598.pt

**Problem**

Previous scaled heading-drift experiments showed a tradeoff.

When scaled heading_drift was set to -0.05, yaw control improved, but rear-left foot motion became too weak.

When scaled heading_drift was reduced to -0.02, rear-left foot motion recovered, but yaw drift became too large.

This means the useful heading_drift weight is probably between -0.02 and -0.05.

**Hypothesis**

A scaled heading_drift weight of -0.035 may provide a better balance between yaw control and rear-left foot movement.

The heading penalty should be strong enough to reduce yaw drift, but not so strong that it suppresses rear-left stride and lift.

**Change I tested**

heading_drift weight:

-0.02 → -0.035

**Everything else stayed fixed**

rear_left_foot_xz_activity = 0.03lateral_velocity = -1.0base_angular_velocity = 1.8diagonal rewards = 0.0rear_foot_xz_velocity_symmetry = 0.0

**Expected result**

- yaw mean_abs: better than the -0.02 run, worse than the -0.05 run, hopefully near or below 1.0°.
- rear_left x_range: lower than the -0.02 run, higher than the -0.05 run, hopefully above 0.0063.
- rear_left z_range: lower than the -0.02 run, higher than the -0.05 run, hopefully above 0.0050.
- base_y mean_abs: should remain controlled, ideally not worse than about 0.043.

**What could go wrong**

The heading penalty may still be too weak, causing yaw drift to remain too high.

The heading penalty may still be too strong, causing rear-left movement to drop again.

The robot may show good numbers but still exploit the reward visually by crab-walking, step-turning, or dragging the rear-left foot.

**Verification plan**

Run diagnostic on model_598.pt and compare:

- rear_left x_range
- rear_left z_range
- yaw_deg mean_abs
- base_y mean_abs
- focused rear-left asymmetry comparison

If the diagnostic looks promising, run visual replay.

A model should not become a new checkpoint unless both diagnostic and visual replay pass.

**Diagnostic result**

The -0.035 scaled heading_drift experiment produced the best balance so far in the scaled-heading series.

Rear-left motion improved above the CP17 baseline:

rear_left x_range = 0.0079 / 0.0078rear_left z_range = 0.0085 / 0.0085

Path control was strong:

base_y mean_abs = 0.0176 / 0.0187

Yaw improved compared with the -0.02 run, but remained slightly above the ideal target:

yaw mean_abs = 1.1544° / 1.1015°

**Comparison with previous scaled-heading experiments**

**heading_drift = -0.05**

Result:

yaw mean_abs = 0.7127° / 0.6278°rear_left x_range = 0.0054 / 0.0055rear_left z_range = 0.0044 / 0.0044base_y mean_abs = 0.0439 / 0.0433

Interpretation:

Yaw was good, but rear-left stride and lift collapsed below the CP17 baseline.

Verdict:

Rejected as new best.

**heading_drift = -0.02**

Result:

yaw mean_abs = 1.7277° / 1.6786°rear_left x_range = 0.0070 / 0.0073rear_left z_range = 0.0067 / 0.0072base_y mean_abs = 0.0365 / 0.0386

Interpretation:

Rear-left motion recovered, but yaw drift became unacceptable.

Verdict:

Rejected as new best.

**heading_drift = -0.035**

Result:

yaw mean_abs = 1.1544° / 1.1015°rear_left x_range = 0.0079 / 0.0078rear_left z_range = 0.0085 / 0.0085base_y mean_abs = 0.0176 / 0.0187

Interpretation:

This is the best balance so far. Rear-left stride and lift are above the CP17 baseline, and path_y is very controlled. Yaw is much better than the -0.02 run, but still slightly above the ideal target of under 1.0°.

**Good signs**

Rear-left stride and lift are above the CP17 baseline.

Path_y is better than previous scaled-heading runs.

Yaw is much better than the -0.02 run.

The robot completed full episodes without terrain_out_of_bounds termination.

The reward setup was correct and matched the intended controlled experiment.

**Bad signs**

Yaw mean_abs is still slightly above the ideal <1.0° target.

Rear-right still has much larger x/z ranges than rear-left.

Diagnostic numbers alone are not enough to prove the gait is good.

Visual replay is required to check for step-turning, crab-walk, rear-left dragging, or unnatural compensation.

**Keep or reject**

Candidate for visual replay.

Not promoted yet.

Not Checkpoint 18 yet.

Still part of Checkpoint 17 experiments.

**What I learned**

The scaled heading_drift reward has a real tradeoff.

At -0.05, heading control is strong but rear-left motion is suppressed.

At -0.02, rear-left motion recovers but heading control is too weak.

At -0.035, the model gives the best balance so far: rear-left motion improves, path_y is controlled, and yaw is reduced compared with -0.02.

However, a model cannot become a new checkpoint based on diagnostic numbers alone. Visual replay is required.

**Next step**

Run visual replay on model_598.pt.

Visual replay should answer:

- Does it walk forward, or does it step-turn?
- Does the body face mostly forward?
- Does the rear-left foot visibly lift and swing, or still drag?
- Does it crab-walk sideways?
- Is it better than the CP17 current best visually?

If visual replay shows clean forward walking with no step-turning, no crab-walk, and no rear-left dragging, this model can become a candidate for a new checkpoint.

If visual replay shows compensation or unstable behavior, reject it and continue experimenting from the CP17 current best.

Repeat diagnostic result:

A second diagnostic run confirmed the same result. Rear-left base-frame z_range stayed at 0.0085 / 0.0085, confirming that rear-left lift improvement is real and repeatable. Rear-left x_range also stayed at 0.0079 / 0.0078. Path_y remained strong with base_y mean_abs = 0.0176 / 0.0187, and yaw mean_abs remained 1.1544° / 1.1015°.

Back-leg lift interpretation:

Rear-left lift improved above the CP17 baseline, but it is still not symmetric with rear-right. Rear-left z_range is about 0.0085, while rear-right z_range is about 0.0200 / 0.0202. Therefore, this model improves rear-left lift but does not fully solve rear-left/rear-right asymmetry.

Visual observation:

Visual replay looked much better than previous experiments. The robot drifted less, yawed less, and the back legs moved more. Rear-left lift still needs caution because the diagnostic shows it is improved but remains weaker than rear-right.

Current verdict:

Candidate for new checkpoint, but not perfect. Promotion depends on whether the visual replay is clearly better than CP17 current best and has no obvious step-turning, crab-walk, or rear-left dragging.

---

## Checkpoint 17: Experiment Log: Rear-Foot Symmetry Reward and Remaining Rear-Left Drag

**Context**

The previous best baseline was:

2026-06-09_03-07-45/model_1000.pt

This model had the most natural gait so far, but it still showed two main problems:

- The robot slowly drifted/yawed to the right.
- The rear-left foot appeared lower or dragging during walking.

Earlier diagnostics showed that the rear-left foot had a strong mean bias compared with the rear-right foot. The most suspicious joint was rear_left_foot, because its action mean and joint position mean were much more negative than rear_right_foot.

Old baseline comparison:

- rear_left_foot vs rear_right_foot
- action_mean_delta ≈ -3.17
- joint_pos_mean_delta ≈ -0.132

The config/runtime diagnostic showed that joint limits and default positions were symmetric between the rear-left and rear-right foot joints, so the asymmetry was unlikely to be caused by a hardcoded default-position or joint-limit offset. The working hypothesis was that the learned policy had developed a biased rear-left foot command.

**Experiment 1: Rear-Foot Joint Symmetry Reward**

**Hypothesis**

If the rear-left foot dragging is partly caused by a learned rear-left foot joint mean bias, then adding a small rear-left/rear-right foot joint symmetry penalty should reduce the rear-left foot joint bias.

**Config Change**

A new reward function was added to flat_env_cfg.py:

def rear_foot_joint_symmetry(env, asset_cfg: SceneEntityCfg = SceneEntityCfg("robot")) -> torch.Tensor:

"""Penalize rear-left foot joint position bias relative to rear-right foot."""

asset = env.scene[asset_cfg.name]

joint_names = list(asset.data.joint_names)

rear_left_foot_id = joint_names.index("rear_left_foot")

rear_right_foot_id = joint_names.index("rear_right_foot")

joint_pos = asset.data.joint_pos

if not isinstance(joint_pos, torch.Tensor):

joint_pos = wp.to_torch(joint_pos)

rear_left_foot_pos = joint_pos[:, rear_left_foot_id]

rear_right_foot_pos = joint_pos[:, rear_right_foot_id]

return torch.square(rear_left_foot_pos - rear_right_foot_pos)

Reward term added:

rear_foot_joint_symmetry = RewardTermCfg(

func=rear_foot_joint_symmetry,

weight=-0.25,

params={

"asset_cfg": SceneEntityCfg("robot"),

},

)

The weight was intentionally small because this was a controlled experiment. The goal was to test whether a gentle symmetry penalty could reduce the rear-foot bias without overpowering the main walking rewards.

**Debugging Notes**

The first attempted training run did not use the new reward because the reward patch had not actually landed in flat_env_cfg.py.

Evidence:

grep did not find rear_foot_joint_symmetry in flat_env_cfg.py

**Conclusion:** that training run could not be treated as a valid symmetry experiment.

After manually editing the config in VS Code, the reward appeared in the Reward Manager:

rear_foot_joint_symmetry | -0.25

The first runtime error occurred because @configclass was accidentally placed above the reward function instead of above class SpotRewardsCfg. This caused Python to apply @configclass to a function, which failed because @configclass expects a class.

The second runtime error occurred because asset.data.joint_pos was a Warp array during CPU execution, not a Torch tensor. This was fixed by converting it with:

wp.to_torch(joint_pos)

After these fixes, a 5-iteration sanity check passed and the reward appeared in the reward table.

**Training Run**

Started from:

logs/rsl_rl/spot_flat/2026-06-09_03-07-45/model_1000.pt

New run folder:

logs/rsl_rl/spot_flat/2026-06-15_05-10-51

Highest saved checkpoint:

model_299.pt

The 300-iteration run completed successfully. The reward stayed active and did not destabilize training.

Late training values showed:

Episode_Reward/rear_foot_joint_symmetry ≈ -0.0008 to -0.0012

Mean episode length = 150.00

terrain_out_of_bounds = 0.0000

This means the robot survived full episodes and did not go out of bounds during training.

**Diagnostic Result: model_299.pt**

Diagnostic checkpoint:

logs/rsl_rl/spot_flat/2026-06-15_05-10-51/model_299.pt

**Rear Foot Joint Symmetry Result**

Old baseline:

rear_left_foot vs rear_right_foot:

action_mean_delta ≈ -3.17

joint_pos_mean_delta ≈ -0.132

New model:

Episode 1:

rear_left_foot vs rear_right_foot:

action_mean_delta = 0.2348

joint_pos_mean_delta = 0.0141

Episode 2:

rear_left_foot vs rear_right_foot:

action_mean_delta = 0.2260

joint_pos_mean_delta = 0.0141

This is a major numerical improvement. The rear-left foot joint mean bias was largely removed.

**New Compensation Problem**

Although the rear foot joint mean bias improved, the rear leg joints became more asymmetric:

Episode 1:

rear_left_leg vs rear_right_leg:

action_mean_delta = 2.1271

joint_pos_mean_delta = 0.0937

Episode 2:

rear_left_leg vs rear_right_leg:

action_mean_delta = 2.1083

joint_pos_mean_delta = 0.0934

This suggests the policy may have compensated through the rear leg joints after the rear foot joints were forced to become more symmetric.

**Foot Height / Clearance Result**

Base-frame foot height showed that rear-left foot vertical range became very small:

Episode 1:

rear_left_foot_link range = 0.0055

rear_right_foot_link range = 0.0150

Episode 2:

rear_left_foot_link range = 0.0054

rear_right_foot_link range = 0.0149

This means the rear-left foot was moving much less vertically than the rear-right foot.

Visual replay confirmed that the back-left foot still appeared to drag. The robot also still drifted to the right, while the head stayed mostly forward.

**Interpretation**

The rear-foot joint symmetry reward was a partial success.

It successfully fixed the specific numerical issue it targeted:

rear_left_foot joint/action mean bias

However, it did not fix the visible gait problem:

rear-left foot still visually drags

robot still drifts right

head remains mostly forward

This suggests the original hypothesis was partly right but incomplete.

Updated hypothesis:

The remaining right drift is probably not mainly a yaw-heading issue. Since the head stays forward while the robot drifts right, the issue is more likely caused by lateral gait asymmetry or uneven rear-limb propulsion.

The rear-left drag is likely caused by rear-left limb motion as a whole, not only the rear-left foot joint mean. The rear-left foot has too little vertical motion, and the policy may be compensating through the rear-left/rear-right leg joints.

**Current Conclusion**

Do not increase the rear-foot joint symmetry reward yet.

Reason:

The symmetry reward already fixed the rear-foot joint mean bias. Making it stronger may increase compensation through other joints and make the gait less natural.

Next experiment should target the physical behavior directly:

rear-left foot clearance / rear-left foot vertical lift

instead of only targeting joint angle symmetry.

**Proposed Next Experiment**

Add a small reward or penalty that directly targets the rear-left foot link height/clearance in space.

Purpose:

Reduce visible rear-left dragging.

Increase rear-left foot vertical motion.

Reduce right drift caused by uneven rear-left limb motion.

This should start from:

logs/rsl_rl/spot_flat/2026-06-15_05-10-51/model_299.pt

The next experiment should remain controlled:

- Keep rear_foot_joint_symmetry = -0.25.
- Add only one new rear-left clearance term.
- Start from the successful symmetry checkpoint.
- Run a 5-iteration sanity check first.
- If the reward loads and does not crash, run 300 iterations.
- Compare visual replay and diagnostic results against 2026-06-15_05-10-51/model_299.pt.

Success criteria:

1. Rear-left foot visually drags less.

2. Robot drifts right less while head stays forward.

3. Rear-left base-frame foot vertical range increases from about 0.0055.

4. Walking remains stable and natural.

5. No new rear-right dragging appears.

---

## Checkpoint 17: Foot-Clearance 0.7 Continued Run / Best Balanced Gait Candidate

**Run folder:** logs/rsl_rl/spot_flat/2026-06-09_03-07-45/

Matching Checkpoint 17 config snapshot path:

`source/isaaclab_tasks/isaaclab_tasks/manager_based/locomotion/velocity/config/spot_micro/flat_env_cfg.py.checkpoint17_foot07_best_gait_model1000`

**Main tested checkpoint paths:** logs/rsl_rl/spot_flat/2026-06-09_03-07-45/model_950.ptlogs/rsl_rl/spot_flat/2026-06-09_03-07-45/model_1000.ptlogs/rsl_rl/spot_flat/2026-06-09_03-07-45/model_1050.ptlogs/rsl_rl/spot_flat/2026-06-09_03-07-45/model_1100.ptlogs/rsl_rl/spot_flat/2026-06-09_03-07-45/model_1197.pt

**Description:** Checkpoint 17 was trained by continuing from Checkpoint 16, after increasing the foot-clearance reward from 0.5 to 0.7. The goal was to preserve Checkpoint 16’s straighter walking while encouraging the legs, especially the previously dragging rear-left leg, to lift and participate more.

**Training setup:** The main change was:

foot_clearance reward weight: 0.5 → 0.7

The following key settings were kept:

base angular velocity reward weight = 1.5action_smoothness penalty = -0.75action scale = 0.04joint position penalty = -3.0base linear velocity std = 0.15

**Training result:** The run completed successfully and stayed stable. The robot survived full episodes and did not go out of bounds. Numerically, the mean reward improved compared with Checkpoint 16, and the foot-clearance reward increased as expected. This made the run worth visual testing. The logs showed stable episode completion and no terrain-out-of-bounds failure.

Visual result by checkpoint:

model_950.ptThis checkpoint was poor for straight walking. The robot rotated left around the front-left foot, using it almost like a pivot point. This checkpoint is not useful as a straight-walking candidate.

model_1000.ptThis was the best balanced gait candidate so far. The robot walked straight, appeared to lift and use all legs, and showed a fuller stride. Toward the end, it drifted slightly to the right, but the overall gait quality looked strong. This checkpoint should be preserved as the best full-gait candidate from this run.

model_1050.ptThis checkpoint drifted a little less than model_1000.pt, but the strides looked shorter. It may be straighter, but also more conservative. This should be preserved as a backup candidate: straighter but less energetic than model_1000.pt.

model_1100.ptThis checkpoint performed about 1.5 trot-gait cycles, then turned about 30 degrees left, and then repeated that pattern. This shows that a trot rhythm was emerging, but the heading control was not stable. The robot still had a periodic left-turn bias.

model_1197.ptThis checkpoint completed about one trot-gait cycle, but then turned left using the front-left leg as a pivot. The front-left leg still did not lift enough. This suggests that increasing foot clearance to 0.7 helped the gait cycle somewhat, but did not fully solve the front-left leg engagement problem and may have contributed to left-pivot behavior later in training.

**Interpretation:** Checkpoint 17 shows that the robot is now very close to a useful trot gait. The best checkpoint in this run was not the final checkpoint. Instead, model_1000.pt appeared visually better than later checkpoints. This is important because reinforcement learning checkpoints do not always improve visually over time. Later models began developing left-pivot or left-turn behavior, while model_1000.pt had the best combination of stride quality, leg usage, and straight walking.

**Status:** Current best gait candidate:logs/rsl_rl/spot_flat/2026-06-09_03-07-45/model_1000.pt

**Backup candidate:** logs/rsl_rl/spot_flat/2026-06-09_03-07-45/model_1050.pt

The next step should be to preserve the current config and decide whether to continue from model_1000.pt or train a small refinement from that checkpoint, rather than continuing from the later model_1197.pt.

---

## Checkpoint 17: Leg Lift Height

Problem:

Checkpoint 17 model_1000 walks forward, but visually only the front-right foot appears to lift clearly. The front-left foot lifts less, and both rear feet appear to drag or slide.

My hypothesis:

The policy is not producing balanced swing phases for all four feet. It may be relying mostly on the front-right leg for clear stepping while the other feet have lower clearance or shorter swing motion.

Why I think this:

With the camera unlocked, I can now inspect the rear legs more clearly. Visually, the front-right foot lifts the most, the front-left foot lifts only slightly, and the rear feet appear to stay close to the ground.

Measurement I need:

Measure vertical foot height over time for all four feet:

front_right_foot, front_left_foot, rear_right_foot, rear_left_foot.

Expected result:

If my hypothesis is correct, front_right_foot should show the clearest and highest lift cycle, while the front-left and rear feet should show lower peak height or weaker swing cycles.

Next experiment:

Modify or run a diagnostic script to print/log each foot’s vertical position over time during replay of Checkpoint 17 model_1000.

---

## Checkpoint 17: Re-Observation Log

**Run ID:** Checkpoint 17 re-observationDate/time: Not recordedParent checkpoint: Checkpoint 17Checkpoint/model tested: logs/rsl_rl/spot_flat/2026-06-09_03-07-45/model_1000.ptConfig snapshot path: flat_env_cfg.py.checkpoint17_foot07_best_gait_model1000

**Code/config change**

No code or config was changed during this test. This was a visual re-evaluation of a previously trained checkpoint.

**One main variable changed**

No training variable was changed. The purpose was observation only.

**Reason for the test**

I did not clearly remember what Checkpoint 17 model_1000.pt looked like, so I replayed it to observe the gait more carefully before making another reward or symmetry change.

**My hypothesis**

My hypothesis was that Checkpoint 17 model_1000.pt has the best natural gait so far, but slowly drifts to the right.

**Expected result**

I expected the robot to walk forward with a relatively smooth and full gait, but with some rightward drift near the end of the simulation.

**Visual observation**

The robot walks forward with a fairly smooth stride. The back of the robot stays level, which is a good sign because the body does not appear to collapse, bounce badly, or drag. The stride length looks fairly natural and not extremely short or stiff.

However, the robot’s body path gradually drifts right. The yaw also turns clockwise/right with the body. Visually, the issue seems most noticeable during the diagonal phase involving the front-left leg and rear-right leg. During that phase, the front-left leg appears to act like a pivot when it steps down, which may be contributing to the clockwise yaw.

The front legs appear to be doing more of the work than the rear legs, but this is only a visual observation. I am not fully sure which leg is strongest or weakest yet.

**Quantitative evidence**

No new numerical measurement was collected in this observation. The current evidence is visual only.

Useful measurements to collect next include:

- yaw rate during the walking phase
- left/right lateral velocity
- joint position trajectories
- joint velocity trajectories
- foot lift and foot placement timing
- estimated stride length for each diagonal pair
- front-left and rear-right coordination during the suspected pivot phase

**Failure mode**

The main failure mode appears to be slow clockwise/right yaw and rightward drift while walking forward. The suspected visual cause is an imbalance during the front-left + rear-right diagonal step, but this is not proven yet.

**What improved**

Compared with earlier checkpoints, this model has one of the best overall walking forms so far. It has smoother stride quality, better forward movement, and less obvious foot dragging.

**What got worse / remaining issue**

The robot still does not maintain a straight heading. It gradually yaws and drifts right. The diagonal gait may be asymmetric, especially during the front-left + rear-right phase, but that needs measurement before changing rewards.

**What this proves**

This proves that Checkpoint 17 model_1000.pt is still a strong baseline checkpoint for gait quality and forward walking.

**What this does NOT prove**

This does not prove that the front-left leg is definitely the cause of the yaw. It also does not prove that stride length is unequal, because no foot trajectory, contact timing, or joint trajectory measurements were collected yet.

**Keep or reject**

Keep as the current best baseline checkpoint.

**Next experiment**

Before changing rewards, improve camera control so the robot can be observed from multiple angles without the view snapping back. Then measure stride difference or diagonal-pair asymmetry using joint positions, joint velocities, or foot trajectory estimates.

**The next measurement target should be:** front-left + rear-right diagonal behavior during the phase where the robot visually starts yawing clockwise.

---

## Checkpoint 18: Candidate (USED - check new doc) - Improved Rear-Left Lift with Better Path Control

Candidate - Improved Rear-Left Lift with Better Path Control

Parent checkpoint:

Checkpoint 17 current best

Candidate model:

logs/rsl_rl/spot_flat/2026-06-17_06-34-56_rear_left_xz003_scaled_heading0035_from_current_best/model_598.pt

Main change:

scaled heading_drift weight = -0.035

rear_left_foot_xz_activity = 0.03

lateral_velocity = -1.0

base_angular_velocity = 1.8

Why this became a candidate:

- visual replay looked much better

- less drifting

- less yawing

- back legs moved more

- repeat diagnostic confirmed rear-left lift improvement

Key diagnostic numbers:

rear_left x_range = 0.0079 / 0.0078

rear_left z_range = 0.0085 / 0.0085

rear_right z_range = 0.0200 / 0.0202

base_y mean_abs = 0.0176 / 0.0187

yaw mean_abs = 1.1544° / 1.1015°

Honest limitation:

Rear-left lift improved, but rear-right still lifts much more. This is not a fully symmetric gait yet.

Promotion condition:

This folder can be renamed from “Checkpoint 18 Candidate” to “Checkpoint 18” only after final side-by-side visual comparison with the CP17 current best confirms that this model is clearly better overall.

---

Training result:

Training completed successfully.

Final checkpoint:

logs/rsl_rl/spot_flat/2026-06-18_04-11-24_rear_left_xz004_heading0035_from_cp18_candidate/model_897.pt

Final training-log signs:

rear_left_foot_xz_activity reward increased to 0.0083.

heading_drift remained small at -0.0048.

path_two_point_tracking was -0.0010.

lateral_velocity was -0.0017.

error_vel_yaw was 0.1012.

No terrain_out_of_bounds termination occurred.

Interpretation before diagnostic:

Training log looks promising, but this does not prove better gait. Diagnostic must confirm rear-left x/z range, yaw, and path_y.

---

## Checkpoint 18: Current Best Confirmed Baseline

**Improved Rear-Left Lift with Better Path/Yaw Control**

**Parent checkpoint**

Checkpoint 17 current best

**Official Checkpoint 18 model**

logs/rsl_rl/spot_flat/2026-06-17_06-34-56_rear_left_xz003_scaled_heading0035_from_current_best/model_598.pt

**Main configuration changes**

- heading_drift = -0.035
- rear_left_foot_xz_activity = 0.03
- lateral_velocity = -1.0
- base_angular_velocity = 1.8

**Why this is promoted to Checkpoint 18**

This model was first labeled as a candidate because visual replay and diagnostics showed improved overall walking quality compared with Checkpoint 17. It is now promoted to official Checkpoint 18 after side-by-side comparison against later experimental branches.

The model showed:

- Better overall gait stability than later branches
- Less visually concerning yaw than the X-only branch
- More natural-looking movement than the front-right-overactivity branch
- Better compromise between path control, yaw control, and rear-leg movement
- No evidence that later reward stacking produced a cleaner gait

**Key diagnostic numbers**

- rear_left x_range = 0.0079 / 0.0078
- rear_left z_range = 0.0085 / 0.0085
- rear_right z_range = 0.0200 / 0.0202
- base_y mean_abs = 0.0176 / 0.0187
- yaw mean_abs = 1.1544° / 1.1015°

**Comparison against later branches**

**Compared with X-only rear-left stride model**

**X-only model:** logs/rsl_rl/spot_flat/2026-06-18_22-15-12_rear_left_xonly003_heading0035_resume_from_750/model_899.pt

The X-only model improved path straightness and rear-left stride, but visual replay showed more left yaw and a more forced-looking gait. It was useful diagnostically, but not clean enough to replace Checkpoint 18.

**Verdict:** keep as diagnostic branch, not current best.

**Compared with front-right-overactivity penalty model**

**Front-right-overactivity model:** logs/rsl_rl/spot_flat/2026-06-18_23-40-11_xonly003_front_right_overactivity003_from_xonly899/model_1198.pt

This branch worsened yaw/path and failed to fix the diagonal imbalance. The penalty likely attacked a compensating behavior instead of the root cause.

**Verdict:** reject.

**Honest limitation**

Checkpoint 18 is not a solved gait.

The rear-left leg is still weak compared with the rear-right leg. Rear-left x-range and z-range remain much smaller than rear-right. This means the model has better overall walking control, but not full gait symmetry.

The rear-left issue remains the main target for future experiments.

**Final status**

Checkpoint 18 is now the official current best baseline.

It should be used as the parent checkpoint for the next controlled experiment.

**Status:** CURRENT BEST CONFIRMED BASELINE

---

## Checkpoint 18: Experiment: Increase Rear-Left XZ Activity from 0.03 to 0.04

**Parent checkpoint**

Checkpoint 18 Candidate:

logs/rsl_rl/spot_flat/2026-06-17_06-34-56_rear_left_xz003_scaled_heading0035_from_current_best/model_598.pt

**New experiment run**

Run name:

rear_left_xz004_heading0035_from_cp18_candidate

Final checkpoint tested:

logs/rsl_rl/spot_flat/2026-06-18_04-11-24_rear_left_xz004_heading0035_from_cp18_candidate/model_897.pt

**Problem**

The Checkpoint 18 Candidate improved the robot’s walking compared with the previous Checkpoint 17 baseline. Visual replay showed less drifting, less yawing, and more back-leg movement.

However, the diagnostic still showed rear-left/rear-right asymmetry.

Checkpoint 18 Candidate diagnostic:

rear_left z_range = 0.0085 / 0.0085rear_right z_range = 0.0200 / 0.0202

rear_left x_range = 0.0079 / 0.0078rear_right x_range = 0.0188 / 0.0190

This means rear-left lift and stride improved, but rear-right was still doing much more work.

**Hypothesis**

Increasing rear_left_foot_xz_activity from 0.03 to 0.04 may encourage the rear-left foot to lift and swing slightly more.

The goal is not to make all legs perfectly equal. The goal is to improve useful rear-left movement without destroying the better heading and path control from the Checkpoint 18 Candidate.

**Why I thought this might work**

The Checkpoint 18 Candidate already had a better visual gait and better rear-left movement than earlier experiments. But rear-left was still weaker than rear-right.

Since the remaining problem was rear-left underactivity, a small increase in rear_left_foot_xz_activity seemed like a reasonable controlled experiment.

I also noticed from the physical robot that making front and back legs lift exactly the same can make the robot tip backward. Because of that, the goal was controlled rear-left improvement, not perfect equality.

**Change tested**

rear_left_foot_xz_activity:

0.03 → 0.04

**Everything else stayed fixed**

heading_drift = -0.035lateral_velocity = -1.0base_angular_velocity = 1.8rear_foot_xz_velocity_symmetry = 0.0diagonal rewards = 0.0

**Expected result**

- rear_left z_range:Slightly higher than 0.0085, hopefully around 0.0090–0.0110.
- rear_left x_range:Slightly higher than 0.0078–0.0079, hopefully around 0.0085–0.0100.
- yaw mean_abs:May get slightly worse than 1.10–1.15°, because stronger rear-left motion may disturb heading.
- base_y mean_abs:May get slightly worse than 0.0176–0.0187, but should ideally remain below 0.03.
- visual behavior:Rear-left foot should visibly lift and swing more. The robot should still walk forward with less drift than older experiments. Ideally, it should not step-turn, crab-walk, or pitch backward.

**What could go wrong**

The rear-left activity reward may make the robot exaggerate rear-left motion instead of walking naturally.

Yaw may increase again.

Path_y may get worse.

The robot may wobble, crab-walk, or step-turn.

The robot may pitch backward or become less stable if the rear-left lift becomes too aggressive.

The diagnostic may improve rear-left z_range but the visual gait may become worse.

**Training result**

Training completed successfully.

Final checkpoint:

logs/rsl_rl/spot_flat/2026-06-18_04-11-24_rear_left_xz004_heading0035_from_cp18_candidate/model_897.pt

Final training-log signs:

rear_left_foot_xz_activity reward increased to 0.0083.heading_drift remained small at -0.0048.path_two_point_tracking was -0.0010.lateral_velocity was -0.0017.error_vel_yaw was 0.1012.No terrain_out_of_bounds termination occurred.

Training log looked promising, but diagnostic was required to confirm the gait.

**Diagnostic result**

The reward setup was correct:

heading_drift = -0.035rear_left_foot_xz_activity = 0.04lateral_velocity = -1.0base_angular_velocity = 1.8

**What improved**

Rear-left vertical lift improved slightly.

Checkpoint 18 Candidate:

rear_left z_range = 0.0085 / 0.0085

New 0.04 run:

rear_left z_range = 0.0095 / 0.0094

So the hypothesis partly worked. Increasing rear_left_foot_xz_activity did increase rear-left vertical lift.

Rear-right lift also reduced:

Checkpoint 18 Candidate:

rear_right z_range = 0.0200 / 0.0202

New 0.04 run:

rear_right z_range = 0.0149 / 0.0162

This means rear-left/rear-right vertical lift asymmetry became less extreme.

**What got worse**

Rear-left forward/back stride got worse.

Checkpoint 18 Candidate:

rear_left x_range = 0.0079 / 0.0078

New 0.04 run:

rear_left x_range = 0.0063 / 0.0062

This is a meaningful regression. The rear-left foot lifted slightly more, but it did not swing forward/back more. It became more like “extra lift without useful stride.”

Yaw also got worse.

Checkpoint 18 Candidate:

yaw mean_abs = 1.1544° / 1.1015°

New 0.04 run:

yaw mean_abs = 1.6154° / 1.4986°

This means the stronger rear-left activity reward disturbed heading control.

Path_y stayed good:

base_y mean_abs = 0.0148 / 0.0144

So the robot did not drift sideways badly, but it yawed more. That suggests the body orientation became worse even though the robot stayed close to the path.

**Interpretation**

Increasing rear_left_foot_xz_activity from 0.03 to 0.04 improved rear-left vertical lift slightly and reduced rear-left/rear-right vertical lift imbalance.

However, it also reduced useful rear-left forward/back stride and worsened yaw.

This means the extra reward encouraged more vertical rear-left activity, but not better walking mechanics.

The model became more active but not more useful.

**Keep or reject**

Reject.

Do not promote.

Do not replace the Checkpoint 18 Candidate.

The better model remains:

logs/rsl_rl/spot_flat/2026-06-17_06-34-56_rear_left_xz003_scaled_heading0035_from_current_best/model_598.pt

**What I learned**

More rear-left activity is not automatically better.

At rear_left_foot_xz_activity = 0.03, the model had better yaw and better rear-left stride.

At rear_left_foot_xz_activity = 0.04, the model had slightly better rear-left lift, but worse rear-left stride and worse yaw.

The rear-left activity reward has a tradeoff. Increasing it too much may create “lift without useful stride” and disturb heading.

Therefore, the next experiment should not simply increase rear_left_foot_xz_activity again.

**Next step**

Return to the Checkpoint 18 Candidate.

Do not test rear_left_foot_xz_activity = 0.05.

The next experiment should target useful rear-left stride or rear-left/rear-right balance more carefully.

Possible future directions:

- Separate rear-left X stride reward from rear-left Z lift reward.
- Reward rear-left forward/back movement more than vertical lift.
- Penalize excessive rear-right dominance carefully.
- Add a better symmetry target that does not destroy yaw.
- Compare visual replay before trusting any new diagnostic improvement.

**Current status after this experiment**

Checkpoint 18 Candidate remains the best model so far.

This 0.04 experiment is rejected but valuable because it shows the limit of simply increasing rear-left X/Z activity.

---

## Checkpoint 18: Experiment Documentation: Rear-Right Overdominance Penalty from CP18

**Status**

**Type:** Experiment, not checkpointPromotion status: Not promotedCurrent official best remains: CP18 model_598

Official CP18 baseline:

logs/rsl_rl/spot_flat/2026-06-17_06-34-56_rear_left_xz003_scaled_heading0035_from_current_best/model_598.pt

Experiment model:

logs/rsl_rl/spot_flat/2026-06-19_05-45-16_exp_rear_right_overdominance003_from_cp18/model_897.pt

CP18 is the current best walking baseline, but it still has a clear rear-leg amplitude imbalance.

The rear-right foot has much larger X/Z motion than the rear-left foot.

In CP18:

rear_left z_range  ≈ 0.0085 / 0.0085

rear_right z_range ≈ 0.0200 / 0.0202

rear_left x_range  ≈ 0.0079 / 0.0078

rear_right x_range ≈ 0.0188 / 0.0190

This suggests the robot is relying much more on the rear-right leg than the rear-left leg.

However, CP18 still has relatively good body path behavior compared with later experiments:

CP18 base_y mean_abs ≈ 0.0176 / 0.0187

CP18 yaw mean_abs    ≈ 1.1544° / 1.1015°

So the problem is not simply “make rear-left move more.” The real problem is:

Can we reduce rear-right overdominance without damaging body path, yaw, or lateral stance geometry?

The hypothesis was:

CP18’s rear-left/rear-right amplitude imbalance is partly caused by rear-right overdominance.

If we penalize rear-right X/Z speed only when it exceeds rear-left X/Z speed, the policy may reduce rear-right dominance and produce a more balanced rear gait.

The intended mechanism:

rear_right_overdominance_xz penalty

→ reduce excessive rear-right X/Z motion

→ improve rear-left vs rear-right amplitude balance

→ preserve or improve body path/yaw

This was an asymmetric penalty, not a symmetric equality penalty. The goal was not to make both rear legs weak. The goal was to reduce rear-right dominance only when rear-right exceeded rear-left.

CP18 showed strong rear X/Z amplitude imbalance.

In CP18, rear-right had much larger Z lift range:

rear_left z_range  ≈ 0.0085 / 0.0085

rear_right z_range ≈ 0.0200 / 0.0202

gap ≈ 0.0115–0.0117

CP18 also showed much larger rear-right X stride range:

rear_left x_range  ≈ 0.0079 / 0.0078

rear_right x_range ≈ 0.0188 / 0.0190

gap ≈ 0.0110–0.0112

CP18 foot-Y placement was fairly centered:

front stance width ≈ 0.1998 / 0.1996

rear stance width  ≈ 0.1992 / 0.1993

front center_offset ≈ -0.0008 / -0.0008

rear center_offset  ≈ -0.0017 / -0.0017

So CP18’s main visible gait issue was rear X/Z amplitude imbalance, not obviously bad lateral foot mean placement.

Added a new reward term:

rear_right_overdominance_xz

Conceptual reward:

If rear_right_xz_speed > rear_left_xz_speed:

penalize the excess

else:

no penalty

Intended meaning:

Do not force both rear legs to be equal at all times.

Only punish rear-right when it dominates rear-left too much in X/Z foot speed.

Reward weight:

rear_right_overdominance_xz = -0.03

The experiment was trained from CP18.

Experiment run:

2026-06-19_05-45-16_exp_rear_right_overdominance003_from_cp18

Final model tested:

model_897.pt

If the hypothesis was correct, then compared with CP18:

Expected improvements:

rear-left X/Z amplitude should increase

rear-right X/Z amplitude should decrease or become less dominant

rear-left vs rear-right X/Z amplitude gap should shrink

Expected safety requirements:

base_y mean_abs should stay near CP18 or improve

yaw mean_abs should stay near CP18 or improve

foot-Y center_offset should not shift significantly

stance width should not change significantly

Promotion condition:

The experiment can only become a checkpoint if it improves rear amplitude balance without worsening path/yaw/stance geometry.

**6.1 Rear Z amplitude improved**

CP18:

rear_left z_range  ≈ 0.0085 / 0.0085

rear_right z_range ≈ 0.0200 / 0.0202

gap ≈ 0.0115–0.0117

Experiment:

rear_left z_range  ≈ 0.0104 / 0.0104

rear_right z_range ≈ 0.0164 / 0.0166

gap ≈ 0.0060–0.0062

Interpretation:

Rear Z amplitude gap shrank by roughly half.

This supports the amplitude-imbalance part of the hypothesis.

**6.2 Rear X amplitude improved**

CP18:

rear_left x_range  ≈ 0.0079 / 0.0078

rear_right x_range ≈ 0.0188 / 0.0190

gap ≈ 0.0110–0.0112

Experiment:

rear_left x_range  ≈ 0.0095 / 0.0094

rear_right x_range ≈ 0.0152 / 0.0153

gap ≈ 0.0057–0.0059

Interpretation:

Rear X amplitude gap also shrank by roughly half.

The reward changed the intended rear X/Z amplitude mechanism.

**6.3 Path got worse**

CP18:

base_y mean_abs ≈ 0.0176 / 0.0187

Experiment:

base_y mean_abs ≈ 0.0314 / 0.0320

Interpretation:

The robot drifted sideways more.

Even though rear X/Z amplitude balance improved, body path tracking worsened.

**6.4 Yaw got worse slightly**

CP18:

yaw mean_abs ≈ 1.1544° / 1.1015°

Experiment:

yaw mean_abs ≈ 1.3347° / 1.2112°

Interpretation:

Yaw was not catastrophically worse, but it did worsen.

The experiment did not beat CP18 in body orientation behavior.

**6.5 Foot-Y stance geometry changed**

CP18 front stance width:

**Episode 1:** 0.1998

**Episode 2:** 0.1996

Experiment front stance width:

**Episode 1:** 0.2040

**Episode 2:** 0.2039

Front stance widened by about:

+0.0042 m = +4.2 mm

CP18 rear stance width:

**Episode 1:** 0.1992

**Episode 2:** 0.1993

Experiment rear stance width:

**Episode 1:** 0.1977

**Episode 2:** 0.1978

Rear stance narrowed by about:

-0.0015 m = -1.5 mm

CP18 center offsets:

front center_offset ≈ -0.0008

rear center_offset  ≈ -0.0017

Experiment center offsets:

front center_offset ≈ -0.0045 to -0.0046

rear center_offset  ≈ -0.0030

Interpretation:

The experiment shifted average foot placement more toward the robot’s right side.

The reward did not only change rear X/Z amplitude.

It also changed lateral stance geometry.

**6.6 Joint/action evidence points toward shoulder/hip compensation**

The shoulder/hip abduction joints are the joints most directly responsible for lateral foot placement.

Conceptual conclusion:

Shoulder/hip abduction joints affect foot-Y placement and yaw because they move the leg side-to-side.

Leg swing and foot/knee joints affect forward stride and vertical clearance more directly.

CP18 front-right shoulder joint position mean:

front_right_shoulder joint_pos_mean ≈ -0.0997 / -0.0978

Experiment front-right shoulder joint position mean:

front_right_shoulder joint_pos_mean ≈ -0.1908 / -0.1896

Interpretation:

The experiment caused a large front-right shoulder compensation.

This likely contributed to the widened front stance and shifted lateral foot placement.

The experiment partially supported the hypothesis.

Supported:

Rear-right overdominance was real.

The reward reduced rear X/Z amplitude imbalance.

Rear-left increased and/or rear-right decreased, shrinking the rear X/Z gap.

Not supported:

Fixing rear X/Z amplitude this way did not improve overall gait.

The robot’s path got worse.

Yaw got slightly worse.

Foot-Y stance geometry shifted.

The policy appeared to compensate through shoulder/hip abduction, especially front-right shoulder behavior.

Final verdict:

exp_rear_right_overdominance003_from_cp18 is not promoted.

CP18 remains the official best checkpoint.

This experiment is useful as a mechanism diagnostic but rejected as a model.

Short version:

Mechanism useful.

Model rejected.

Do not call this CP19.

The robot’s gait problem is not pure rear X/Z amplitude imbalance.

The better current diagnosis is:

Rear X/Z amplitude imbalance is real, but CP18 may be using rear-right dominance as a compensation strategy for body stability.

When rear-right dominance is reduced, the policy compensates elsewhere, especially in shoulder/hip abduction and lateral stance geometry.

That compensation worsens base_y and yaw behavior.

This means the next problem is likely:

B) lateral foot placement / stance geometry

C) yaw-body coupling

Reason:

Lateral foot placement changes the support polygon and the direction of ground reaction forces.

Yaw-body coupling depends on left/right push symmetry, force timing, foot placement, and moment arms around the center of mass.

Important distinction:

Foot amplitude is kinematics.

Yaw/path behavior is body dynamics.

A more balanced foot trajectory does not automatically mean better body motion.

Do not immediately add another reward.

Next diagnostic should focus on:

Which joints create the lateral stance shift and yaw moment?

Specifically inspect:

front_left_shoulder

front_right_shoulder

rear_left_shoulder

rear_right_shoulder

Questions to answer:

1. Did the overdominance experiment change shoulder/hip abduction more than CP18?

2. Did front-right shoulder compensation cause the widened front stance?

3. Is yaw error correlated with front-right shoulder position/action?

4. Is base_y drift correlated with foot-Y center_offset or shoulder action asymmetry?

5. Is rear X/Z improvement being bought by worse lateral stance geometry?

Suggested next diagnostic:

Add focused shoulder/hip abduction comparison:

- action_mean

- action_range

- joint_pos_mean

- joint_pos_range

- joint_vel_range

for all four shoulder joints.

Also add left/right shoulder pair deltas:

- front_left_shoulder vs front_right_shoulder

- rear_left_shoulder vs rear_right_shoulder

- front_right_shoulder vs rear_right_shoulder

Current next hypothesis:

The overdominance reward improves rear X/Z amplitude but causes shoulder/hip abduction compensation, especially in the front-right shoulder, which shifts foot-Y placement and worsens yaw/path behavior.

Next isolated experiment should not happen until the shoulder/yaw mechanism is measured.

This experiment is valuable because it produced a real mechanism result.

It answered:

Can a reward reduce rear-right overdominance?

Yes.

Does that make the robot better overall?

No.

Why not?

Because it changes lateral stance geometry and likely yaw-body coupling.

This is a serious robotics result, not just an IsaacLab reward tweak.

---

## Checkpoint 18: Experiment: Rear-left X-only stride activity

Experiment:

Rear-left X-only stride activity

Problem:

Rear-left motion improved in the Checkpoint 18 Candidate, but it is still weaker than rear-right. The remaining issue is not only foot lift; rear-left forward/back stride is also still smaller than rear-right. The rejected 0.04 XZ experiment showed that increasing X and Z together is too blunt: it slightly improved rear-left lift, but rear-left x_range got worse and yaw got worse.

My hypothesis:

Rewarding rear-left X-only stride activity may improve useful forward/back rear-left movement without encouraging extra vertical kicking. This may produce a more useful gait than rewarding X and Z together.

Why I think this:

The previous 0.04 XZ experiment increased rear-left lift but reduced rear-left forward/back stride and worsened yaw. That suggests the policy may exploit the reward by creating vertical activity rather than useful stride. An X-only reward should target the actual missing behavior more directly.

I also suspect action_smoothness and joint penalties may make the policy prefer less movement, because no movement can be “smooth.” But this experiment does not directly test action_smoothness yet. It tests whether a focused rear-left X stride reward can overcome rear-left underuse without disturbing yaw too much.

Change I will test:

Disable rear_left_foot_xz_activity.

Add rear_left_foot_x_activity.

Expected result:

1. rear_left x_range:

Slightly higher than 0.0078–0.0079, hopefully around 0.0085–0.0100.

2. rear_left z_range:

May stay around 0.0085 or slightly lower. I should not expect a large z increase because this experiment does not reward Z lift directly.

3. yaw mean_abs:

Hopefully stays near 1.1° and does not rise above 1.5°.

4. base_y mean_abs:

Ideally stays below 0.03.

5. visual behavior:

Rear-left should show more useful forward/back swing. It should not just lift higher. The robot should still walk forward with no obvious step-turning, crab-walk, or exaggerated rear-left kicking.

What could go wrong:

The X-only reward may not improve rear-left stride.

The robot may increase rear-left sliding rather than useful stepping.

Yaw may get worse if the extra rear-left stride disturbs heading.

Path_y may get worse.

The robot may look less natural even if the rear_left x_range improves.

The policy may still underuse rear-left because action_smoothness and joint penalties make smaller motion easier.

---

Actual result:

The X-only rear-left stride experiment improved the target metric. Rear-left x_range increased from the CP18 Candidate baseline of about 0.0079 / 0.0078 to 0.0107 / 0.0108. Rear-left z_range also improved from about 0.0085 / 0.0085 to 0.0153 / 0.0153, even though Z was not directly rewarded.

Yaw stayed approximately the same as the CP18 Candidate. The X-only model produced yaw mean_abs = 1.1581° / 1.0972°, compared with the CP18 Candidate’s 1.1544° / 1.1015°. Path_y also stayed strong, with base_y mean_abs = 0.0160 / 0.0081.

Interpretation:

The X-only reward worked better than the previous XZ reward increase. It improved useful rear-left stride without causing the yaw regression seen in the 0.04 XZ experiment. This suggests that rewarding rear-left forward/back stride is a cleaner direction than rewarding combined X/Z activity.

Remaining concern:

Rear-left is still not equal to rear-right. Rear-right x_range remains higher at 0.0182 / 0.0183. The model also needs visual replay because diagnostic improvement does not guarantee natural walking.

Keep or reject:

Candidate for visual replay. Do not promote yet.

Next step:

Run visual replay on model_899.pt and compare it directly against the CP18 Candidate model_598.pt.

---

Visual replay observation:

The robot still walks forward, and rear-left foot movement appears improved. However, the front-right foot seems to push harder off the ground, causing the robot to yaw left. The rear-left knee/leg joint still appears underactive visually.

Diagnostic interpretation:

The rear-left leg joint is not frozen, but it remains weaker than the rear-right leg. In the diagnostic, rear_left_leg joint_pos_range was about 0.1453 / 0.1464, while rear_right_leg joint_pos_range was about 0.2415 / 0.2424.

Conclusion:

The X-only reward improved rear-left foot stride, but it may not have fixed the deeper rear-left leg/knee underuse. Do not promote this model yet.

---

## Checkpoint 18: Experiment: Rear-left / front-right foot joint activity balance

**Experiment:** Rear-left / front-right foot joint activity balance

**Problem:** The X-only stride experiment improved rear-left foot movement, but visual replay still shows the front-right foot pushing harder off the ground and causing the robot to yaw left. The rear-left foot/ankle joint is not frozen, but it still appears less active than the front-right foot/ankle joint.

**Diagnostic evidence:** rear_left_foot joint_pos_range = 0.0817 / 0.0833front_right_foot joint_pos_range = 0.1416 / 0.1393

This suggests a diagonal imbalance between rear-left and front-right.

**My hypothesis:** The robot may be overusing the front-right foot joint to compensate for weaker rear-left contribution. This front-right over-push may be creating a yaw moment and causing left yaw.

**Why I think this:** Visual replay shows the front-right foot pushing harder off the ground. The diagnostic also shows the front-right foot joint has much larger motion range than the rear-left foot joint. A smoother-motion policy may prefer a gait shape where rear-left does less and front-right compensates.

**Change I will test:** Add a gentle penalty for front_right_foot joint velocity being much larger than rear_left_foot joint velocity.

Keep rear_left_foot_x_activity active, because the X-only reward improved rear-left stride.

**Keep fixed:** heading_drift = -0.035rear_left_foot_xz_activity = 0.0rear_left_foot_x_activity = 0.03lateral_velocity = -1.0base_angular_velocity = 1.8rear_foot_xz_velocity_symmetry = 0.0diagonal position rewards = 0.0

Expected result:

- rear_left_foot joint_pos_range:May increase slightly or stay near 0.08.
- front_right_foot joint_pos_range:Should decrease slightly from about 0.14 if front-right over-pushing is reduced.
- rear_left x_range:Should stay near 0.0107 / 0.0108 and should not collapse below 0.008.
- yaw mean_abs:Hopefully improves below about 1.1°, or at least does not get worse.
- visual behavior:The robot should still walk forward. The front-right foot should look less aggressive. Rear-left/front-right diagonal motion should look more balanced. The robot should yaw less left.

**What could go wrong:** The penalty may reduce front-right activity too much and weaken propulsion.Rear-left x_range may collapse.Yaw may still remain.The robot may walk slower or look less natural.The policy may find another compensation pattern instead of truly improving diagonal balance.

---
