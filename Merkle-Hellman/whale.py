import numpy as np

class WhaleOptimization:
    def __init__(self, cipher, pub_key, pop_size):
        self.cipher = cipher
        self.pub_key = np.array(pub_key)
        self.pop_size = pop_size


    def __generate_initial_population(self):
        # Generate random number values
        uniform_values = np.random.uniform(0.0, 1.0, (self.pop_size, len(self.pub_key)))

        # Generate initial population
        population = np.zeros((self.pop_size, len(self.pub_key)), dtype=int)
        population[uniform_values >= 0.5] = 1

        return population


    def __evaluate_population(self, population, target):
        # Compute sum of values from public key for all agents
        sum_vals = np.sum(population * self.pub_key, axis=1)

        # Compute the maximum difference between the sum and the target value
        max_diff = np.maximum(target, sum_vals - target)

        # Compute fitness
        fitness = np.empty(len(sum_vals), dtype=np.float64)

        idx_small_sum = np.where(sum_vals < target)
        idx_big_sum = np.where(sum_vals >= target)

        fitness[idx_small_sum] = 1 - np.sqrt(np.abs(sum_vals[idx_small_sum] - target) / target)
        fitness[idx_big_sum] = 1 - (np.abs(sum_vals[idx_big_sum] - target) / max_diff[idx_big_sum])**(1 / 6)

        print(idx_small_sum)
        print(idx_big_sum)

        return fitness


    def __evaluate_individual(self, individual, target):
        # Compute sum of values from public key for all agents
        sum_val = np.sum(individual * self.pub_key)

        # Compute the maximum difference between the sum and the target value
        max_diff = np.maximum(target, sum_val - target)

        # Compute fitness
        if sum_val < target:
            fitness = 1 - np.sqrt(np.abs(sum_val - target) / target)
        else:
            fitness = 1 - (np.abs(sum_val - target) / max_diff)**(1/6)

        return fitness


    def __sigmoid_function(self, whale):
        probs = 1 / (1 + np.exp(whale))
        rands = np.random.uniform(0.0, 1.0, whale.shape)

        whale_bin = np.zeros(whale.shape, int)
        whale_bin[rands <= probs] = 1

        return whale_bin



    def __mutation(self, whale):
        whale_mut = np.copy(whale)

        probs = np.random.uniform(0.0, 1.0, len(whale))
        whale_mut[np.logical_and(probs < 0.5, whale_mut == 1)] = 0
        whale_mut[np.logical_and(probs >= 0.5)] = 1

        return whale_mut

    def attack(self, b=1, mutation_rate=0.5, max_iter=1000000):
        sols = []

        # Repeat this process for each target
        for target in self.cipher:
            # Number of iterations
            t = 0

            # Generate intial population and evaluate it
            population = self.__generate_initial_population()
            fitness = self.__evaluate_population(population, target)

            # Select best agent
            idx_best = np.argmax(fitness)

            best_agent = population[idx_best]
            best_fitness = fitness[idx_best]

            # Do this for each whale
            while not best_fitness == 1.0 and t < max_iter:

                # Generate a value
                a = 2 - t * (2 / max_iter)

                for whale, i in zip(population, range(len(population))):
                    # Generate values
                    A = 2 * a * np.random.uniform(0.0, 1.0) - a
                    C = 2 * np.random.uniform(0.0, 1.0)
                    l = np.random.uniform(-1.0, 1.0)
                    p = np.random.uniform(0.0, 1.0)

                    if p < 0.5:
                        if np.abs(A) < 1.0:
                            distance = np.abs(C * best_agent - whale)
                            new_whale = best_agent - A * distance
                        else:
                            rand_whale = population[np.random.choice(len(population))]
                            distance = np.abs(C * rand_whale - whale)
                            new_whale = rand_whale - A * distance
                    else:
                        distance = np.abs(best_agent - whale)
                        new_whale = distance * np.exp(b * l) * np.cos(2 * np.pi * l) + best_agent

                    new_whale_bin = self.__sigmoid_function(new_whale)
                    fitness = self.__evaluate_individual(new_whale_bin, target)

                    if np.random.uniform(0.0, 1.0) < mutation_rate:
                        whale_mut = self.__mutation(new_whale_bin)

                        fitness_mut = self.__evaluate_individual(whale_mut, target)

                        if fitness_mut > fitness:
                            fitness = fitness_mut
                            new_whale_bin = whale_mut


                    population[i] = new_whale_bin
                    if fitness > best_fitness:
                        best_fitness = fitness
                        best_agent = new_whale_bin
                        print(best_agent)
                        print(best_fitness)
                        print(t)

                t += 1

            sols.append((best_agent, best_fitness))



            print(population)
            print(fitness)
            print(idx_best)
            print(best_fitness)
            print(best_agent)
