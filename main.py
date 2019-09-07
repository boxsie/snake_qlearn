
from enviroments.pong.pong_enviroment import PongEnviroment
from agent import Agent

import pygame

if __name__ == "__main__":
    #env = PongEnviroment((640, 640), (20, 50), (600, 570), (20, 110))
    agent = Agent(max_memory=10000, batch_size=64, tile_count=16)
    agent.train()
