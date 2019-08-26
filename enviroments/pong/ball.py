import pygame
import math
import random
import numpy as np

class Ball:
    def __init__(self, start_pos, offset, size, max_velocity, min_velocity, friction,):
        self._position = np.array(start_pos)
        self._velocity = np.array([0, 0])
        self._start_pos = start_pos
        self._size = np.array(size)
        self._min_velocity = min_velocity
        self._max_velocity = max_velocity
        self._friction = friction
        self._colour = (65, 87, 2)

    def reset(self):
        self._position = np.array(self._start_pos)
        target_r = math.pi * 2.0 * random.random()
        self._velocity[0] = math.cos(target_r) * self._min_velocity
        self._velocity[1] = math.sin(target_r) * self._min_velocity

    def update(self, time_step):
        self._velocity = self._velocity * self._friction * time_step

        mag = np.linalg.norm(self._velocity)
        if mag > self._max_velocity:
            self._velocity = (self._velocity / mag) * self._max_velocity
        elif mag < self._min_velocity:
            self._velocity = (self._velocity / mag) * self._min_velocity

        self._position = self._position + self._velocity

    def render(self, display):
        pygame.draw.rect(
            display,
            self._colour, (
                self._position[0],
                self._position[1],
                self._size[0],
                self._size[1])
        )

    def check_for_intersect(self, rect_tl, rect_br):
        ball_tl = self._position
        ball_br = self._position + self._size

        if rect_tl[0] > ball_br[0] or ball_tl[0] > rect_br[0]:
            return False

        if rect_tl[1] > ball_br[1] or ball_tl[1] > rect_br[1]:
            return False

        return True

    def bounce(self, normal, force):
        normal = np.array(normal)
        self._velocity = self._velocity - 2 * normal * np.dot(normal, self._velocity)
