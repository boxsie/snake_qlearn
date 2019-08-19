import math
import random
import pygame

from direction import Direction
from snake import Snake
from apple import Apple

class SnakeGame:
    def __init__(self, surface_size, walls=True):
        pygame.init()
        pygame.display.set_caption('QSnake')

        self._surface_size = surface_size
        self._display = pygame.display.set_mode(self._surface_size)
        self._clock = pygame.time.Clock()
        self._walls = walls
        self._bg_colour = (153, 199, 0)
        self._tile_size = 15
        self._tile_count = 30
        self._game_over = False
        self._apple_eaten = False

        self._snake = Snake((self._tile_count // 2, self._tile_count // 2))
        self._apple = Apple(self.get_new_apple_pos())

        self._apple_angle = 0
        self._tail_end_angle = 0
        self._up_status = 0
        self._right_status = 0
        self._down_status = 0
        self._left_status = 0

        self.state_count = len(self.get_state())
        self.action_count = len(Direction)

    def get_state(self):
        return (
            self._apple_angle,
            self._tail_end_angle,
            self._up_status,
            self._right_status,
            self._down_status,
            self._left_status
        )

    def get_new_apple_pos(self):
        return (
            math.floor(random.uniform(0, 1) * self._tile_count),
            math.floor(random.uniform(0, 1) * self._tile_count)
        )

    def reset(self):
        self._snake.reset()
        self._apple.position = self.get_new_apple_pos()
        self._game_over = False

    def update(self):
        self._snake.update()
        self._game_over = self._snake.check_for_intersect()

        x_pos = self._snake.position[0]
        y_pos = self._snake.position[1]

        if not self._game_over:
            if self._walls:
                if x_pos < 0 or x_pos > self._tile_count - 1 or \
                y_pos < 0 or y_pos > self._tile_count - 1:
                    self._game_over = True
            else:
                if x_pos < 0:
                    x_pos = self._tile_count - 1
                elif x_pos > self._tile_count - 1:
                    x_pos = 0

                if y_pos < 0:
                    y_pos = self._tile_count - 1
                elif y_pos > self._tile_count - 1:
                    y_pos = 0

                self._snake.position = (x_pos, y_pos)

        if self._game_over:
            return True

        self._snake.add_to_tail(self._snake.position)

        if self._snake.check_for_apple_eat(self._apple.position):
            self._apple.position = self.get_new_apple_pos()
            self._apple_eaten = True

        self._apple_angle = (math.atan2(
            self._apple.position[1] - y_pos,
            self._apple.position[0] - x_pos
        ) * 180 / math.pi) / 180

        self._tail_end_angle = self._snake.tail_end_angle() / 180

        self.build_state()
        return False

    def render(self, clock_tick):
        self._display.fill(self._bg_colour)

        self._snake.draw(self._display, self._tile_size)
        self._apple.draw(self._display, self._tile_size)

        x_pos = self._snake.position[0]
        y_pos = self._snake.position[1]

        line_start = (
            (x_pos * self._tile_size) + (self._tile_size * 0.5),
            (y_pos * self._tile_size) + (self._tile_size * 0.5)
        )

        dist_to_apple = math.sqrt(
            ((self._apple.position[0] - x_pos) ** 2) +
            ((self._apple.position[1] - y_pos) ** 2)
        )

        x_end = line_start[0] + math.cos(self._apple_angle) * (dist_to_apple * self._tile_size)
        y_end = line_start[1] + math.sin(self._apple_angle) * (dist_to_apple * self._tile_size)

        pygame.draw.line(self._display, (254, 254, 0), line_start, (x_end, y_end), 1)

        pygame.display.update()
        self._clock.tick(clock_tick)

    def build_state(self):
        self._up_status = 0
        self._right_status = 0
        self._down_status = 0
        self._left_status = 0

        x_pos = self._snake.position[0]
        y_pos = self._snake.position[1]
        x_apple = self._apple.position[0]
        y_apple = self._apple.position[1]

        up_pos = y_pos - 1 if self._walls or y_pos - 1 >= 0 else self._tile_count - 1
        right_pos = x_pos + 1 if self._walls or x_pos < self._tile_count - 1 else 0
        down_pos = y_pos + 1 if self._walls or y_pos + 1 < self._tile_count else 0
        left_pos = x_pos - 1 if self._walls or x_pos - 1 >= 0 else self._tile_count - 1

        if self._walls:
            if up_pos < 0: self._up_status = -1
            if right_pos >= self._tile_count: self._right_status = -1
            if down_pos >= self._tile_count: self._down_status = -1
            if left_pos < 0: self._left_status = -1

        self._up_status = -1 if self._snake.check_tail_proximity(Direction.up) else self._up_status
        self._right_status = -1 if self._snake.check_tail_proximity(Direction.right) else self._right_status
        self._down_status = -1 if self._snake.check_tail_proximity(Direction.down) else self._down_status
        self._left_status = -1 if self._snake.check_tail_proximity(Direction.left) else self._left_status

        if up_pos == y_apple and x_pos == x_apple:
            self._up_status = 1
        if right_pos == x_apple and y_pos == y_apple:
            self._right_status = 1
        if down_pos == y_apple and x_pos == x_apple:
            self._down_status = 1
        if left_pos == x_apple and y_pos == y_apple:
            self._left_status = 1

    def get_reward(self):
        if self._game_over:
            return -100.0
        if self._apple_eaten:
            self._apple_eaten = False
            return 100.0

        return -0.1

    def handle_input(self, action):
        self._snake.set_velocity(Direction(action))
