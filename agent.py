import tensorflow as tf
import pygame

from model import Model
from memory import Memory
from game_runner import GameRunner

class Agent:
    def __init__(self, env, max_memory, batch_size):
        self._env = env
        self._model = Model(env.state_count, env.action_count, batch_size=batch_size)
        self._memory = Memory(max_memory=max_memory)
        self._render = False
        self._clock_tick = 15
        self._clock_tick_min = 5
        self._clock_tick_max = 240
        self._model_path = 'models'
        self._focus_high_scores = False

    def train(self):
        with tf.Session() as sess:
            sess.run(self._model.var_init)
            game_runner = GameRunner(sess, self._model, self._env, self._memory, max_eps=0.1, min_eps=1e-5, decay=1e-4, gamma=0.7)
            game_runner.reset()
            i = 0

            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            quit()
                            break
                        elif event.key == pygame.K_s:
                            self._model.save(sess, self._model_path, i)
                        elif event.key == pygame.K_d:
                            self._render = not self._render
                        elif event.key == pygame.K_PAGEUP:
                            self._clock_tick += self._clock_tick_min
                            self._clock_tick = self._clock_tick if self._clock_tick <= self._clock_tick_max else self._clock_tick_max
                            print(f'\nNew clock tick: {self._clock_tick}')
                        elif event.key == pygame.K_PAGEDOWN:
                            self._clock_tick -= self._clock_tick_min
                            self._clock_tick = self._clock_tick if self._clock_tick >= self._clock_tick_min else self._clock_tick_min
                            print(f'\nNew clock tick: {self._clock_tick}')
                        elif event.key == pygame.K_r:
                            self._focus_high_scores = not self._focus_high_scores

                gr_latest = game_runner.update(self._render, self._clock_tick)

                if not self._render and self._focus_high_scores and gr_latest.current_score == gr_latest.highest_score - 1:
                    self._render = True

                if gr_latest.game_complete:
                    i += 1
                    game_runner.reset()

                    if self._render and self._focus_high_scores:
                        self._render = False

                print(f'Epochs:{i + 1:,} | Current score:{gr_latest.current_score:,} | Highest score:{gr_latest.highest_score:,} | Average score:{gr_latest.average_score:,.2f} | Average reward:{gr_latest.average_reward:,.2f} | Current ε:{gr_latest.current_eps:,.5f}  ', end='\r')
