import random

class Memory:
    def __init__(self, max_memory):
        self._max_memory = max_memory
        self._samples = []

    def add_sample(self, sample):
        self._samples.append(sample)
        if len(self._samples) > self._max_memory:
            self._samples.pop(0)

    def sample(self, sample_count):
        if sample_count > len(self._samples):
            return random.sample(self._samples, len(self._samples))

        return random.sample(self._samples, sample_count)
