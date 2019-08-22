from snake_game import SnakeGame
from agent import Agent

if __name__ == "__main__":
    snake_size = (640, 640)
    snake = SnakeGame(snake_size, tile_count=32, tile_size=20)
    agent = Agent(snake, max_memory=5000000, batch_size=64)
    agent.train()
