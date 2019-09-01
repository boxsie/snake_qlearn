from enviroments.snake.snake_enviroment import SnakeEnviroment
from enviroments.pong.pong_enviroment import PongEnviroment
from agent import Agent

import pygame

if __name__ == "__main__":
    snake_size = (640, 640)
    env = SnakeEnviroment(snake_size, (20, 20), tile_count=30, tile_size=20)
    #env = PongEnviroment((640, 640), (20, 50), (600, 570), (20, 110))
    agent = Agent(env, max_memory=500000, batch_size=64)
    agent.train()
