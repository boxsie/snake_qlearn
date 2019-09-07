import tensorflow as tf
import pygame
import os

from snake_qlearn.model import Model
from snake_qlearn.memory import Memory
from snake_qlearn.game_runner import GameRunner

class Agent:
    def __init__(self, env, max_memory, batch_size, tile_count, headless=False):
        self._env = env
        self._model = Model(
            num_states=env.state_count*2,
            num_actions=env.action_count,
            batch_size=batch_size,
            learning_rate=1e-3,
            grid_size=tile_count,
            frames_per_state=2)
        self._memory = Memory(max_memory=max_memory)
        self._render = False
        self._clock_tick = 15
        self._clock_tick_min = 5
        self._clock_tick_max = 240
        self._model_path = 'models'
        self._last_model_idx = self._get_last_save_idx()
        self._focus_high_scores = False
        self._headless = headless
        if (headless):
            os.environ["SDL_VIDEODRIVER"] = "dummy"

    def train(self):
        with tf.Session() as sess:
            sess.run(self._model.var_init)
            game_runner = GameRunner(sess, self._model, self._env, self._memory, max_eps=1.0, min_eps=1e-1, decay=1e-4, gamma=0.97)
            game_runner.reset()
            i = 0

            while True:
                if not self._headless:
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                self.exit()
                                break
                            elif event.key == pygame.K_s:
                                self._last_model_idx += 1
                                self.save_model(sess, self._last_model_idx)
                            elif event.key == pygame.K_l:
                                self.load_model(sess, self._last_model_idx)
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

                print(f'Epochs:{i + 1:,} | Current score:{gr_latest.current_score:,} | Highest score:{gr_latest.highest_score:,} | Current time:{gr_latest.current_time:,.2f}s | Average score:{gr_latest.average_score:,.2f} | Average reward:{gr_latest.average_reward:,.2f} | Average time:{gr_latest.average_time:,.2f}s | Current ε:{gr_latest.current_eps:,.5f}  ', end='\r')

    def save_model(self, sess, model_name):
        self._model.save(sess, self._model_path, model_name)
        self._memory.save(self._model_path, model_name)

    def load_model(self, sess, model_name):
        self._model.load(sess, self._model_path, model_name)
        self._memory.load(self._model_path, model_name)

    def exit():
        pygame.quit()
        quit()

    def _get_last_save_idx(self):
        model_idxs = [0]
        for f in listdir(self._model_path):
            print(f)
            if isfile(join(self._model_path, f)):
                try:
                    idx = int(f.split('.')[0])
                    model_idxs.append(idx)
                except ValueError:
                    pass
        return max(model_idxs)