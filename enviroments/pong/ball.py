import pygame
import math
import random
import numpy as np

class Ball:
    def __init__(self, start_pos, offset, size, max_velocity, min_velocity, friction,):
        self._position = np.array(start_pos)
        self._velocity = np.array([0, 0])
        self._start_pos = start_pos
        self._size = size
        self._min_velocity = min_velocity
        self._max_velocity = max_velocity
        self._friction = friction
        self._colour = (65, 87, 2)

    def reset(self):
        self._position = np.array(self._start_pos)
        target_r = math.pi * 2.0 * random.random()
        self._velocity[0] = math.cos(target_r) * self._min_velocity
        self._velocity[1] = math.sin(target_r) * self._min_velocity
        print(self._velocity)

    def update(self, time_step):
        self._velocity = self._velocity * self._friction * time_step

        mag = np.linalg.norm(self._velocity)
        if mag > self._max_velocity:
            self._velocity = (self._velocity / mag) * self._max_velocity
        elif mag < self._min_velocity:
            self._velocity = (self._velocity / mag) * self._min_velocity
        print(self._velocity)

        self._position = self._position + (self._velocity * time_step)

    def render(self, display):
        pygame.draw.rect(
            display,
            self._colour, (
                self._position[0],
                self._position[1],
                self._size[0],
                self._size[1])
        )

    def bounce(self, normal, force):
        self._velocity = self._velocity - (math.pow(self._velocity * normal, 2) * normal)
