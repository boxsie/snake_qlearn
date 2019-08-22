import math
import random
import pygame
from collections import namedtuple

from direction import Direction
from snake import Snake
from apple import Apple

class SnakeGame:
    def __init__(self, surface_size, tile_count, tile_size, walls=True, observe_tiles=5, observe_dirs=8):
        pygame.init()
        pygame.display.set_caption('QSnake')

        self._surface_size = surface_size
        self._display = pygame.display.set_mode(self._surface_size)
        self._clock = pygame.time.Clock()
        self._walls = walls
        self._bg_colour = (153, 199, 0)
        self._tile_size = tile_size
        self._tile_count = tile_count
        self._game_over = False
        self._apple_eaten = False

        self._snake = Snake((self._tile_count // 2, self._tile_count // 2))
        self._apple = Apple(self.get_new_apple_pos())

        self._apple_angle = 0
        self._apple_distance = 0
        self._tail_end_angle = 0
        self._observe_tiles = observe_tiles
        self._observe_dirs = observe_dirs
        self._observations = self.observe_area()

        self.state_count = len(self.get_state())
        self.action_count = len(Direction)
        self.score = 0

    def get_state(self):
        return tuple(list(map(lambda x: x[3], self._observations)))

    def get_new_apple_pos(self):
        return (
            math.floor(random.uniform(0, 1) * self._tile_count),
            math.floor(random.uniform(0, 1) * self._tile_count)
        )

    def observe_area(self):
        x_pos = self._snake.position[0]
        y_pos = self._snake.position[1]
        r_delta = (2 * math.pi) / self._observe_dirs

        obvs = []

        for dist in range(1, self._observe_tiles + 1):
            for d in range(self._observe_dirs):
                target_r = (r_delta * d) - (math.pi * 0.5)
                x_end = int(x_pos + math.cos(target_r) * dist)
                y_end = int(y_pos + math.sin(target_r) * dist)
                val = 0
                mod = dist / self._observe_tiles

                if self._apple.position[0] == x_end and self._apple.position[1] == y_end:
                    val = mod

                if not self.check_position_on_grid((x_end, y_end)):
                    val = -mod
                else:
                    for i in self._snake.tail_trail:
                        if i[0] == x_end and i[1] == y_end:
                            val = -mod

                obvs.append((x_end, y_end, target_r, val))
        return obvs

    def check_position_on_grid(self, pos):
        return pos[0] >= 0 and pos[1] >= 0 and pos[0] < self._tile_count and pos[1] < self._tile_count

    def reset(self):
        self._snake.reset()
        self._apple.position = self.get_new_apple_pos()
        self._observations = self.observe_area()
        self._game_over = False
        self.score = 0

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
            self.score += 1

        self._observations = self.observe_area()

        self._apple_angle = (math.atan2(
            self._apple.position[1] - y_pos,
            self._apple.position[0] - x_pos
        ) * 180 / math.pi) / 180

        self._tail_end_angle = self._snake.tail_end_angle() / 180

        self._apple_distance = math.sqrt(
            ((self._apple.position[0] - x_pos) ** 2) +
            ((self._apple.position[1] - y_pos) ** 2)
        )

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

        for o in self._observations:
            x_end = o[0] * self._tile_size
            y_end = o[1] * self._tile_size

            val = o[3]
            if val != 0:
                col = (254 - abs(254 * val), 0, 0) if val < 0 else (0, 254 -  abs(254 * val), 0)
                pygame.draw.rect(self._display, col, (x_end, y_end, self._tile_size, self._tile_size))

        pygame.display.update()
        self._clock.tick(clock_tick)

    def get_reward(self):
        if self._game_over:
            return -1.0
        if self._apple_eaten:
            self._apple_eaten = False
            return 1.0

        # dist_to_apple = math.sqrt(
        #     ((self._apple.position[0] - self._snake.position[0]) ** 2) +
        #     ((self._apple.position[1] - self._snake.position[1]) ** 2)
        # )

        # return -(dist_to_apple / self._tile_count) * 0.1
        return -0.01

    def handle_input(self, action):
        self._snake.set_velocity(Direction(action))

