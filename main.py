from enviroments.snake.snake_enviroment import SnakeEnviroment
from enviroments.pong.pong_enviroment import PongEnviroment
from agent import Agent

import pygame

if __name__ == "__main__":
    snake_size = (680, 680)
    env = SnakeEnviroment(snake_size, (20, 20), tile_count=16, tile_size=20)
    #env = PongEnviroment((640, 640), (20, 50), (600, 570), (20, 110))
    agent = Agent(env, max_memory=10000, batch_size=64, tile_count=16)
    agent.train()
