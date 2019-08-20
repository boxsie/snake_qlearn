import tensorflow as tf
import pygame as pygame

from snake_game import SnakeGame
from model import Model
from memory import Memory
from game_runner import GameRunner

if __name__ == "__main__":
    SNAKE_SIZE = (450, 450)
    SNAKE = SnakeGame(SNAKE_SIZE)
    MODEL = Model(num_states=SNAKE.state_count, num_actions=SNAKE.action_count, batch_size=128)
    MEM = Memory(max_memory=5000000)
    SAVE_CNT = 1000
    RENDER = False
    CLOCK_TICK = 30
    CLOCK_TICK_MIN = 1
    CLOCK_TICK_MAX = 240
    MODEL_PATH = 'models'

    with tf.Session() as sess:
        sess.run(MODEL.var_init)

        GR = GameRunner(sess, MODEL, SNAKE, MEM, max_eps=0.65, min_eps=0.01, decay=0.01, gamma=0.04)
        SAVER = tf.train.Saver()
        CNT = 1

        while True:
            EVENTS = pygame.event.get()
            for event in EVENTS:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                        break
                    elif event.key == pygame.K_s:
                        MODEL.save(sess, MODEL_PATH, CNT)
                    elif event.key == pygame.K_d:
                        RENDER = not RENDER
                    elif event.key == pygame.K_PAGEUP:
                        CLOCK_TICK += 15
                        CLOCK_TICK = CLOCK_TICK if CLOCK_TICK <= CLOCK_TICK_MAX else CLOCK_TICK_MAX
                        print(f'New clock tick: {CLOCK_TICK}')
                    elif event.key == pygame.K_PAGEDOWN:
                        CLOCK_TICK -= 15
                        CLOCK_TICK = CLOCK_TICK if CLOCK_TICK >= CLOCK_TICK_MIN else CLOCK_TICK_MIN
                        print(f'New clock tick: {CLOCK_TICK}')

            GR.run(RENDER, CLOCK_TICK)

            if CNT % SAVE_CNT == 0:
                MODEL.save(sess, MODEL_PATH, CNT)

            print(f'Snakes killed:{CNT:,} Highest score:{GR.get_high_score():,} Average score:{GR.get_average_score():,}', end='\r')
            CNT += 1
