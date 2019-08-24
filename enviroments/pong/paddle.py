import pygame
import math

class Paddle():
    def __init__(self, offset, size, friction, force, max_velocity, goal_height):
        self._position = (0, 0)
        self._velocity_y = 0
        self._friction = friction
        self._offset = offset
        self._size = size
        self._goal_height = goal_height
        self._force = force
        self._max_velocity = max_velocity
        self._colour = (65, 87, 2)
        self._top = self._offset[1]
        self._bottom = (self._offset[1] + self._goal_height) - self._size[1]

    def reset(self):
        self._position = (self._offset[0], self._offset[1] + self._goal_height * 0.5)
        self._velocity_y = 0

    def update(self, time_step):
        if math.isclose(self._velocity_y, 0, abs_tol=self._max_velocity * 0.1):
            self._velocity_y = 0

        direction = 0
        if self._velocity_y > 0: direction = 1
        elif self._velocity_y < 0: direction = -1

        if abs(self._velocity_y) > self._max_velocity:
            self._velocity_y = self._max_velocity * direction

        self._velocity_y -= self._friction * time_step * direction

        y_pos = self._position[1] + (self._velocity_y * time_step)
        y_pos = max(self._top, min(y_pos, self._bottom))

        self._position = (self._position[0], y_pos)

    def render(self, display):
        pygame.draw.rect(
            display,
            self._colour, (
                self._offset[0] + self._position[0],
                self._offset[1] + self._position[1],
                self._size[0],
                self._size[1])
            )

    def move_paddle(self, direction):
        self._velocity_y += self._force * direction
