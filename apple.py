import pygame

class Apple:
    def __init__(self, pos):
        self.position = pos
        self._apple_colour = (65, 87, 2)

    def draw(self, display, tile_size):
        pygame.draw.rect(
            display,
            self._apple_colour, (
                self.position[0] * tile_size,
                self.position[1] * tile_size,
                tile_size,
                tile_size)
            )