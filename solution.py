from deap import base, creator, tools
import numpy as np
import matplotlib.pyplot as plt
import random
from NQueens import NQueens
from eaElitismCallback import eaElitismCallback
import seaborn as sns
import os
import imageio.v2 as iio
from pygifsicle import optimize

RANDOM_SEED = 10
random.seed(RANDOM_SEED)

POPULATION_SIZE = 100
MAX_GENERATIONS = 100
HOF_SIZE = 10
P_CROSSOVER = 0.9
P_MUTAION = 0.1

NUM_QUEENS = 16

n_Queens = NQueens(NUM_QUEENS)

toolbox = base.Toolbox()
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness= creator.FitnessMin)

toolbox.register("randomGen", random.sample, range(NUM_QUEENS), NUM_QUEENS)
toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomGen)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator, POPULATION_SIZE)

def fitness(individual):
    return n_Queens.countViolations(individual),

toolbox.register("evaluate", fitness)
toolbox.register("select", tools.selTournament, tournsize = 3)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb = 1.0/NUM_QUEENS)


def save_best(gen, best, max_gen):
    '''
    Callback function that can be used for saving the best individual of each generation as gif. Note it may slow down the genetic algorithm.
    '''

    plot = n_Queens.plot_board(best)
    if not os.path.exists('sol'):
        os.makedirs('sol')
    plot.title(f"Generation #{gen}\nViolations: {round(best.fitness.values[0],3)}")
    plot.savefig(f"sol/best_{gen}.png", dpi=100)
    plot.clf()
    if gen == max_gen:
        images = []
        for i in range(1,max_gen+1):
            images.append(iio.imread(f"sol/best_{i}.png"))
            # writer.append_data(image)
            # if os.path.exists(f"sol/best_{i}png"):
            os.remove(f"sol/best_{i}.png")
                # print("y")

        iio.mimsave("sol/best.gif", images, format='GIF', duration=0.5)
        optimize("sol/best.gif")

def main():
    population = toolbox.populationCreator()
    stats = tools.Statistics(lambda ind: ind.fitness.values)

    stats.register("avg", np.average)
    stats.register("min", np.min)

    hof = tools.HallOfFame(HOF_SIZE)

    population, logbook = eaElitismCallback(population, toolbox,cxpb=P_CROSSOVER, mutpb=P_MUTAION, ngen=MAX_GENERATIONS, callback=save_best, stats=stats, halloffame=hof, verbose=True)

    best = hof[0]
    
    print(f"best individual: {best}\n fitness: {best.fitness.values}")
    plot = n_Queens.plot_board(best)
    plot.show()

    minFitness, avgFitness = logbook.select("min", "avg")

    sns.set_style("whitegrid")
    plt.plot(minFitness, label="Minimum")
    plt.plot(avgFitness, label="Average")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(loc="upper right")
    plt.show()
    sns.set_style("white")

if __name__=="__main__":
    
    main()
