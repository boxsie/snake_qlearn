from enviroments.snake.snake_enviroment import SnakeEnviroment
from enviroments.pong.pong_enviroment import PongEnviroment
from agent import Agent

import pygame

if __name__ == "__main__":
    #snake_size = (640, 640)
    #env = SnakeEnviroment(snake_size, tile_count=32, tile_size=20)
    env = PongEnviroment((640, 640), 110)
    env.reset()
    while True:
        env.update()
        env.render(60)

    #agent = Agent(env, max_memory=5000000, batch_size=64)
    #agent.train()
