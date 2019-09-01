import pygame

class Apple:
    def __init__(self, pos):
        self.position = pos
        self._apple_colour = (65, 87, 2)

    def render(self, display, offset, tile_size):
        pygame.draw.rect(
            display,
            self._apple_colour, (
                offset[0] + (self.position[0] * tile_size),
                offset[1] + (self.position[1] * tile_size),
                tile_size,
                tile_size)
            )
