import random
import math
import numpy as np
import time

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
        self._score_store = []
        self._time_store = []
        self._state = None
        self._prev_state = None
        self._total_reward = 0
        self._start_time = 0

    def reset(self):
        self._env.reset()
        s = self._env.get_state()
        self._state = np.array(s + s)
        self._total_reward = 0
        self._start_time = time.time()

    def update(self, render=True, clock_tick=60):
        if render:
            self._env.render(clock_tick)

        action = self._choose_action(self._state)
        self._env.handle_input(action)

        is_game_complete = self._env.update()
        reward = self._env.get_reward()
        next_state = None if is_game_complete else np.array(self._env.get_state())

        if self._prev_state is None:
            self._prev_state = next_state
        else:
            combined_state = None if next_state is None else np.concatenate((self._prev_state, next_state), axis=0)

            self._memory.add_sample((self._state, action, reward, combined_state))
            self._replay()

            self._steps += 1
            self._eps = self._min_eps + (self._max_eps - self._min_eps) * math.exp(-self._decay * self._steps)

            self._state = combined_state
            self._prev_state = next_state
            self._total_reward += reward

            if is_game_complete:
                self._reward_store.append(self._total_reward)
                self._score_store.append(self._env.score)
                self._time_store.append(time.time() - self._start_time)

        return UpdateItem(
            game_complete=is_game_complete,
            highest_score=max(self._score_store) if self._score_store else 0,
            average_score=sum(self._score_store) / len(self._score_store) if self._score_store else 0,
            average_reward=sum(self._reward_store) / len(self._reward_store) if self._reward_store else 0,
            current_eps=self._eps,
            current_score=self._env.score,
            current_time=time.time() - self._start_time,
            average_time=sum(self._time_store) / len(self._time_store) if self._time_store else 0,
        )

    def _choose_action(self, state):
        rnd = random.random()
        if rnd < self._eps:
            return random.randint(0, self._model.num_actions - 1)
        return np.argmax(self._model.predict_one(state, self._sess))

    def _replay(self):
        batch = self._memory.sample(self._model.batch_size)
        states = np.array([val[0] for val in batch])
        next_states = np.array([(np.zeros(self._model.num_states) if val[3] is None else val[3]) for val in batch])

        # predict Q(s,a) given the batch of states
        q_s_a = self._model.predict_batch(states, self._sess)

        # predict Q(s',a') - so that we can do gamma * max(Q(s'a')) below
        q_s_a_d = self._model.predict_batch(next_states, self._sess)

        # setup training arrays
        x = np.zeros((len(batch), self._model.num_states))
        y = np.zeros((len(batch), self._model.num_actions))

        for i, b in enumerate(batch):
            state, action, reward, next_state = b[0], b[1], b[2], b[3]

            # get the current q values for all actions in state
            current_q = q_s_a[i]

            # update the q value for action
            if next_state is None:
                # in this case, the game completed after action, so there is no max Q(s',a')
                # prediction possible
                current_q[action] = reward
            else:
                current_q[action] = reward + self._gamma * np.amax(q_s_a_d[i])
            x[i] = state
            y[i] = current_q

        self._model.train_batch(self._sess, x, y)

class UpdateItem:
    def __init__(self, game_complete, highest_score, average_score, average_reward, average_time, current_eps, current_score, current_time):
        self.game_complete = game_complete
        self.highest_score = highest_score
        self.average_score = average_score
        self.average_reward = average_reward
        self.current_eps = current_eps
        self.current_score = current_score
        self.current_time = current_time
        self.average_time = average_time