import gym
import numpy as np

def main():
    env = gym.make("Pong-v0")
    obs = env.reset()

    batch_size = 10
    gamma = 0.99
    decay_rate = 0.99
    n_hlayer = 200
    input = 80*80
    l_rate = 0.01

    weights = {
        '1': np.random.randn(n_hlayer,input)/np.sqrt(input),
        '2': np.random.randn(n_hlayer)/np.sqrt(n_hlayer)
    }
