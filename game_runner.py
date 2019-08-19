import random
import math
import numpy as np

class GameRunner:
    def __init__(self, sess, model, env, memory, max_eps, min_eps, decay, gamma):
        self._sess = sess
        self._env = env
        self._model = model
        self._memory = memory
        self._max_eps = max_eps
        self._min_eps = min_eps
        self._decay = decay
        self._gamma = gamma
        self._eps = self._max_eps
        self._steps = 0
        self._reward_store = []
        self._max_x_store = []


    def run(self, render=True, clock_tick=60):
        self._env.reset()
        state = np.array(self._env.get_state())
        tot_reward = 0
        max_x = -100

        while True:
            if render:
                self._env.render(clock_tick)

            action = self._choose_action(state)
            self._env.handle_input(action)

            is_game_complete = self._env.update()
            reward = self._env.get_reward()
            next_state = None if is_game_complete else np.array(self._env.get_state())

            self._memory.add_sample((state, action, reward, next_state))
            self._replay()

            self._steps += 1
            self._eps = self._min_eps + (self._max_eps - self._min_eps) * math.exp(-self._decay * self._steps)

            state = next_state
            tot_reward += reward

            if is_game_complete:
                self._reward_store.append(tot_reward)
                self._max_x_store.append(max_x)
                break


    def _choose_action(self, state):
        if random.random() < self._eps:
            return random.randint(0, self._model.num_actions - 1)
        return np.argmax(self._model.predict_one(state, self._sess))


    def _replay(self):
        batch = self._memory.sample(self._model.batch_size)
        states = np.array([val[0] for val in batch])
        next_states = np.array([(np.zeros(self._model.num_states) if val[3] is None else val[3]) for val in batch])

        q_s_a = self._model.predict_batch(states, self._sess)

        q_s_a_d = self._model.predict_batch(next_states, self._sess)

        x = np.zeros((len(batch), self._model.num_states))
        y = np.zeros((len(batch), self._model.num_actions))

        for i, b in enumerate(batch):
            state, action, reward, next_state = b[0], b[1], b[2], b[3]
            current_q = q_s_a[i]

            if next_state is None:
                current_q[action] = reward
            else:
                current_q[action] = reward + self._gamma + np.amax(q_s_a_d[i])

            x[i] = state
            y[i] = current_q

        self._model.train_batch(self._sess, x, y)
