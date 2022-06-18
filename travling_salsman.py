import operator
import random
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


class City:
    def __init__(self, city, x, y):
        self.city = city
        self.x = x
        self.y = y
    
    def distance(self, city):
        xDis = abs(self.x - city.x)
        yDis = abs(self.y - city.y)
        distance = ((xDis ** 2) + (yDis ** 2))**0.5
        return distance
    
    def __repr__(self):
        return self.city

class FitnessCalculator:
    def __init__(self, route):

        self.route = route
        self.distance = 0
        self.fitness= 0.0
    
    def routeDistance(self):
        if self.distance == 0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromCity = self.route[i]
                toCity = None
                if i < len(self.route)-1:
                    toCity = self.route[i + 1]
                else:
                    toCity = self.route[0]
                pathDistance += fromCity.distance(toCity)
            self.distance = pathDistance
        return self.distance

    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness


def createRoute(cityList):
    route = random.sample(cityList, len(cityList))
    return route


def generate_popuation(population_size, cityList):
    population = []

    for i in range(0, population_size):
        population.append(createRoute(cityList))
    return population


def sort_routes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = FitnessCalculator(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)


def selection(sorted_population, size_of_the_fittest):
    selectionResults = []
    df = pd.DataFrame(np.array(sorted_population), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, size_of_the_fittest):
        selectionResults.append(sorted_population[i][0])

    for i in range(0, len(sorted_population) - size_of_the_fittest):
        pick = 100*random.random()
        for i in range(0, len(sorted_population)):
            if pick <= df.iat[i,3]:
                selectionResults.append(sorted_population[i][0])
                break
    return selectionResults


def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

def reproduction(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child


def reproductionPopulation(matingpool, size_of_the_fittest):
    children = []
    length = len(matingpool) - size_of_the_fittest
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,size_of_the_fittest):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = reproduction(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children


def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop
def new_generation(currentGen, size_of_the_fittest, mutationRate):
    sorted_population = sort_routes(currentGen)
    selectionResults = selection(sorted_population, size_of_the_fittest)
    matingpool = matingPool(currentGen, selectionResults)
    children = reproductionPopulation(matingpool, size_of_the_fittest)
    new_generation = mutatePopulation(children, mutationRate)
    return new_generation
def geneticAlgorithm(population, population_size, size_of_the_fittest, mutationRate, generations):

    pop = generate_popuation(population_size, population)
    # print("Initial distance: " + str(1 / sort_routes(pop)[0][1]))
    
    for i in range(0, generations):
        pop = new_generation(pop, size_of_the_fittest, mutationRate)
    print(pop[0])
    print(len(pop[0]))
    # print("Final distance: " + str(1 / sort_routes(pop)[0][1]))
    bestRouteIndex = sort_routes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute



with open('data.txt') as f:
    lines = f.readlines()

city_array = []
for i in lines:
    arr = i.split()
    city_array.append(arr)
cityList = []

for city, latittude, longtude in city_array:
    city_class =City(city = city, x=float(latittude), y=float(longtude))
    cityList.append(city_class)
geneticAlgorithm(population=cityList, population_size=65, size_of_the_fittest=15, mutationRate=0.01, generations=300)

def geneticAlgorithmPlot(population, population_size, size_of_the_fittest, mutationRate, generations):
    pop = generate_popuation(population_size, population)
    progress = []
    progress.append(1 / sort_routes(pop)[0][1])
    
    for i in range(0, generations):
        pop = new_generation(pop, size_of_the_fittest, mutationRate)
        progress.append(1 / sort_routes(pop)[0][1])
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()
geneticAlgorithmPlot(population=cityList, population_size=100, size_of_the_fittest=10, mutationRate=0.01, generations=500)
