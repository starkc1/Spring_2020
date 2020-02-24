import numpy as np
import random
import operator as op

# CS 455 - Artificial Intelligence
# Module 2 - Genetic Algorithm Homework
# Based off the provided python GA classes and tutorials online
# Contributers - Cameron Stark & Dustin Cribbs

class GeneticAlgorithm_SingleKnapsack: #Class for implementation of GA for knapsack problem

    def __init__(self): #On class creation initialize class parameters
        self.spaceLimit = 0
        self.weights = []
        self.values = []
        self.parents = []
        self.newparents = []
        self.chromosomeLength = 0
        self.bests = []
        self.best_p = []
        self.iterated = 1
        self.populationSize = 0

    
    def createPop(self): #create chromosome population

        for i in range(self.populationSize):
            parent = []
            for k in range(0,self.chromosomeLength):
                k = random.randint(0,1)
                parent.append(k)
            self.parents.append(parent)

    def props(self, weights, values, spaceLimit, populationSize, cromLength): #Define GA properties

        self.weights = weights
        self.values = values
        self.chromosomeLength = cromLength
        self.spaceLimit = spaceLimit
        self.populationSize = populationSize
        self.createPop()
 
    def fitness(self, chrom): #Calculate fitness for the inserted chromosom

        weightSum = 0
        valueSum = 0

        for index, i in enumerate(chrom):
            if i == 0:
                continue
            else:
                weightSum += self.weights[index]
                valueSum += self.values[index]

        if weightSum > self.spaceLimit:
            return 0
        else:
            return valueSum
        
    def generations(self): #Create parents and fitness for the generations that will be mated
        best = self.populationSize // 2

        for i in range(len(self.parents)):
            parent = self.parents[i]
            fitness = self.fitness(parent)
            self.bests.append((fitness, parent))
        
        self.bests.sort(key=op.itemgetter(0), reverse = True)
        self.best_p = self.bests[:best]
        self.best_p = [x[1] for x in self.best_p]

    def mutation(self, chrom): #Performs the mutation of the chromosome based on random value, and flipping hte bits based on that

        for i in range(len(chrom)):
            k = random.uniform(0, 1)

            if k > 0.5:
                if chrom[i] == 1:
                    chrom[i] = 0
                else: 
                    chrom[i] = 1

        return chrom

    def crossover(self, chrom1, chrom2): #Performs the crossover of the two chromosomes based on a random crossover point and exchanging the bits after that point between the two

        crossPoint = random.randint(1, len(chrom1) - 1)

        crossChrom1 = chrom1[crossPoint:]
        crossChrom2 = chrom2[crossPoint:]

        chrom1 = chrom1[:crossPoint]
        chrom2 = chrom2[:crossPoint]

        chrom1.extend(crossChrom2)
        chrom2.extend(crossChrom1)

        return chrom1, chrom2

    def knapsackRun(self): #Performs the knapsack optimization process

        self.generations()
        newParents = []
        population = len(self.best_p) - 1

        randomPop = random.sample(range(population), population)
        
        print("Weights: {} \nValues: {}".format(self.weights, self.values))

        for i in range(0, population):
            if i < population - 1:
                bestChrom1 = self.best_p[i]
                bestChrom2 = self.best_p[i + 1]

                chrom1Child, chrom2Child = self.crossover(bestChrom1, bestChrom2)
                
                newParents.append(chrom1Child)
                newParents.append(chrom2Child)
            else:
                bestChrom1 = self.best_p[i]
                bestChrom2 = self.best_p[0]

                chrom1Child, chrom2Child = self.crossover(bestChrom1, bestChrom2)

                newParents.append(chrom1Child)
                newParents.append(chrom2Child)
        
        for i in range(len(newParents)):
            newParents[i] = self.mutation(newParents[i])

        bestFitness = self.fitness(newParents[0])
        bestChromIndex = 0
        for i in range(len(newParents)):
            currFitness = self.fitness(newParents[i])
            print("Current Chromosome: {}, Fitness: {}".format(newParents[i], currFitness))
            if (currFitness > bestFitness):
                bestFitness = currFitness
                bestChromIndex = i

        self.printResult(newParents[bestChromIndex])

    def printResult(self, chrom):
        fitness = self.fitness(chrom)
        print("\nOptimal Solution: {} \nfitness: {} \n".format(chrom, fitness))

    def createWeights(self, low, high, length):
        weights = []
        for i in range(0, length):
            weights.append(random.randint(low, high))
        return weights

    def createValues(self, low, high, length):
        values = []
        for i in range(0, length):
            values.append(random.randint(low, high))
        return values

Knapsack_GA = GeneticAlgorithm_SingleKnapsack()
lengthOfItemsArray = 10
knapsackMaxWeight = 25
populationSize = 50

weights = Knapsack_GA.createWeights(1, knapsackMaxWeight, lengthOfItemsArray)
values = Knapsack_GA.createValues(5, 50, lengthOfItemsArray)

Knapsack_GA.props(weights, values, knapsackMaxWeight, populationSize, lengthOfItemsArray)

Knapsack_GA.knapsackRun()
#https://github.com/Pantzan/KnapsackGA/blob/master/knapsack.py
