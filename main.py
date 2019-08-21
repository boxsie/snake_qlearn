from snake_game import SnakeGame
from agent import Agent

if __name__ == "__main__":
    snake_size = (640, 640)
    snake = SnakeGame(snake_size)
    agent = Agent(snake, max_memory=50000, batch_size=64)
    agent.train()
