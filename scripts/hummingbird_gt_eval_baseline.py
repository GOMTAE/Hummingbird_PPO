#!/usr/bin/env python
# ROS packages required
import rospy
import rospkg
# Dependencies required
import gym
import os
import numpy as np
import pandas as pd
import time

# from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, MlpLnLstmPolicy
# from stable_baselines.common.vec_env import DummyVecEnv
# from stable_baselines import A2C, ACKTR, DDPG, PPO1, PPO2, SAC, TRPO, TD3, HER
# from stable_baselines.deepq.policies import MlpPolicy as mlp_dqn
# from stable_baselines.sac.policies import MlpPolicy as mlp_sac
# from stable_baselines.ddpg.policies import MlpPolicy as mlp_ddpg
# from stable_baselines.td3.policies import MlpPolicy as mlp_td3
# from stable_baselines.ddpg.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise

from stable_baselines3.common.utils import get_linear_fn
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize
from stable_baselines3 import DDPG, PPO, A2C, TD3, SAC
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import VecCheckNan
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import CheckpointCallback

# For scheduler
from typing import Callable

# import our task environment
import hummingbird_hover_task_gt_env_ppo_baseline

# from openai_ros.task_envs.cartpole_stay_up import stay_up
# ROS ENV gets started automatically before the training
# from openai_ros.openai_ros_common import StartOpenAI_ROS_Environment -- This has to be solved at the end

# change the directory
os.chdir('/home/ubuntu/catkin_ws/src/hummingbird_pkg/')
rospy.init_node('hummingbird_gt_eval_baseline', anonymous=True, log_level=rospy.FATAL)

# Create the Gym environment

environment_name = rospy.get_param('/hummingbird/task_and_robot_environment_name')
env = gym.make(environment_name)

# log_dir = "/home/ubuntu/catkin_ws/src/hummingbird_pkg/results/trained_model/baseline/PPO_25/"
log_dir = "/home/ubuntu/catkin_ws/src/hummingbird_pkg/results/trained_model/baseline/gt/PPO_2/"

# model = PPO.load(log_dir + "PPO_hummingbird_hover")
model = PPO.load(log_dir + "PPO_hummingbird_hover")
env = DummyVecEnv([lambda: Monitor(env)])
# env = VecNormalize.load(log_dir + "PPO_hummingbird_hover_vec_normalize.pkl", env)
env = VecNormalize.load(log_dir + "PPO_hummingbird_hover_vec_normalize.pkl", env)

env.training = False

obs = env.reset()
for i in range(10000):
    if i % 1000 == 0:
        print(i)
    action, _states = model.predict(obs)
    obs, reward, done, info = env.step(action)