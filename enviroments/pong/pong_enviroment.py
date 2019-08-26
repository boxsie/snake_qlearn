import math
import random
import pygame
import time

from direction import Direction
from enviroments.pong.paddle import Paddle
from enviroments.pong.ball import Ball

class PongEnviroment:
    def __init__(self, surface_size, offset, court_size, paddle_size):
        pygame.init()
        pygame.display.set_caption('QPong')
        pygame.key.set_repeat

        self._surface_size = surface_size
        self._offset = offset
        self._court_size = court_size
        self._display = pygame.display.set_mode(self._surface_size)
        self._clock = pygame.time.Clock()
        self._bg_colour = (153, 199, 0)
        self._paddle_size = paddle_size
        self._game_over = False
        self._up_pressed = False
        self._down_pressed = False
        self._last_ticks = 0

        self._paddles = [
            Paddle(
                self._offset,
                self._paddle_size,
                friction=40.0,
                force=2.0,
                max_velocity=10.0,
                goal_height=self._court_size[1]
            )
        ]

        self._ball = Ball(
            start_pos=(self._offset[0] + self._court_size[0] * 0.5, self._offset[1] + self._court_size[1] * 0.5),
            offset=self._offset,
            size=(20, 20),
            max_velocity=30,
            min_velocity=10,
            friction=0.1
        )

        self.state_count = len(self.get_state())
        self.action_count = len(Direction)
        self.score = (0, 0)

    def get_state(self):
        return ()

    def suggest_action(self):
        return 0

    def reset(self):
        for p in self._paddles:
            p.reset()
        self._ball.reset()
        self._game_over = False
        self.score = (0, 0)
        self._move_dir = 0
        self._up_pressed = False
        self._down_pressed = False
        self._last_ticks = 0

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                    break
                if event.key == pygame.K_UP:
                    self._up_pressed = True
                if event.key == pygame.K_DOWN:
                    self._down_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self._up_pressed = False
                if event.key == pygame.K_DOWN:
                    self._down_pressed = False

        if self._down_pressed:
            self._paddles[0].move_paddle(1)
        if self._up_pressed:
            self._paddles[0].move_paddle(-1)

        t = time.clock()
        d = t - self._last_ticks

        self._ball.update(d)

        for p in self._paddles:
            p.update(d)

        self._last_ticks = t

        x = self._offset[0] + self._court_size[0]
        y = self._offset[1] + self._court_size[1]

        if self._ball.check_for_intersect(self._offset, (x, self._offset[1])):
            self._ball.bounce((0, -1), 100)
        elif self._ball.check_for_intersect((self._offset[0], y), (x, y)):
            self._ball.bounce((0, 1), 100)
        elif self._ball.check_for_intersect(self._offset, (self._offset[0], y)):
            self._ball.bounce((1, 0), 100)
        elif self._ball.check_for_intersect((x, self._offset[1]), (x, y)):
            self._ball.bounce((-1, 0), 100)
        elif self._ball.check_for_intersect(self._paddles[0]._position, (self._paddles[0]._position[0] + self._paddle_size[0], self._paddles[0]._position[1] + self._paddle_size[1])):
            self._ball.bounce((1, 0), 150)

        return False

    def render(self, clock_tick):
        self._display.fill(self._bg_colour)

        self._ball.render(self._display)

        for p in self._paddles:
            p.render(self._display)

        pygame.draw.rect(
            self._display,
            (65, 87, 2), (
                self._offset[0],
                self._offset[1],
                self._court_size[0],
                self._court_size[1]),
            3
        )

        pygame.display.update()
        self._clock.tick(clock_tick)

    def get_reward(self):

        return -0.01

    def handle_input(self, action):
        self._snake.set_velocity(Direction(action))

