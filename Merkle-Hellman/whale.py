import numpy as np

class WhaleOptimization:
    def __init__(self, cipher, pub_key):
        self.cipher = cipher
        self.pub_key = pub_key
        self.population_size = len(pub_key)

    def __generate_initial_population(self):
        return None

