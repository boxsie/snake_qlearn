import math
import pygame

from direction import Direction

class Snake:
    def __init__(self, pos):
        self.position = pos
        self.tail_trail = []
        self._start_pos = pos
        self._velocity = (0, 0)
        self._snake_colour = (65, 87, 2)
        self.reset()

    def add_to_tail(self, pos):
        self.tail_trail.append(pos)

        while len(self.tail_trail) > self._tail_size:
            self.tail_trail.pop(0)

    def check_for_apple_eat(self, apple_pos):
        if apple_pos[0] == self.position[0] and apple_pos[1] == self.position[1]:
            self._tail_size += 1
            return True
        return False

    def check_tail_proximity(self, check_direction):
        x_pos = self.position[0]
        y_pos = self.position[1]

        for i in self.tail_trail:
            if (check_direction == Direction.up and i[1] == y_pos - 1 and i[0] == x_pos) or \
               (check_direction == Direction.right and i[0] == x_pos + 1 and i[1] == y_pos) or \
               (check_direction == Direction.down and i[1] == y_pos + 1 and i[0] == x_pos) or \
               (check_direction == Direction.left and i[0] == x_pos - 1 and i[1] == y_pos):
                return True
        return False

    def tail_end_angle(self):
        return math.atan2(
            self.tail_trail[0][1] - self.position[1],
            self.tail_trail[0][0] - self.position[0]
        ) * 180 / math.pi

    def set_velocity(self, new_dir):
        if new_dir == Direction.up:
            self._velocity = (0, -1)
        elif new_dir == Direction.right:
            self._velocity = (1, 0)
        elif new_dir == Direction.down:
            self._velocity = (0, 1)
        elif new_dir == Direction.left:
            self._velocity = (-1, 0)

    def check_for_intersect(self, pos=None):
        if not pos:
            pos = self.position

        for i in self.tail_trail:
            if i[0] == pos[0] and i[1] == pos[1]:
                return True
        return False

    def update(self):
        self.position = (self.position[0] + self._velocity[0], self.position[1] + self._velocity[1])

    def render(self, display, offset, tile_size):
        for i in self.tail_trail:
            pygame.draw.rect(
                display,
                self._snake_colour, (
                    i[0] * tile_size,
                    i[1] * tile_size,
                    tile_size,
                    tile_size)
                )

    def reset(self):
        self.position = self._start_pos
        self._tail_size = 5
        self.tail_trail = []
        self.set_velocity(Direction.right)
        self.add_to_tail(self.position)
