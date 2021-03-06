import numpy as np
import random
import operator as op
import copy

# CS 455 - Artificial Intelligence
# Module 2 - Genetic Algorithm Homework
# Based off the provided python GA classes and tutorials online
# Contributers - Cameron Stark & Dustin Cribbs
# Sources - used the below url as basis of understanding how to go about implementing the multi-knapsack problem
    #https://github.com/Somnibyte/Multiple-Knapsack-Problem-Genetic-Algorithm

class GeneticAlgorithm_MultiKnapsack: # Class containing the population creation and run command

    def __init__(self):
        pass

    def createPopulation(self, knapsackCount, knapsackMinWeight, knapsackMaxWeight, itemCount, itemMinWeight, itemMaxWeight, itemMinProfit, itemMaxProfit, populationCount): #create the population with random knapsack values, item values based on parameters
        self.knapsackCount = knapsackCount
        self.itemCount = itemCount
        self.populationCount = populationCount
        self.knapsacks = []
        self.items = []
        self.population = []

        for i in range(0, knapsackCount):
            self.knapsacks.append(Knapsack(i, random.randint(knapsackMinWeight, knapsackMaxWeight)))
        
        for i in range(0, itemCount):
            self.items.append(KnapsackItem(random.randint(itemMinWeight, itemMaxWeight), random.randint(itemMinProfit, itemMaxProfit)))
        
        for i in range(0, populationCount // 2):
            chromosome = Chromosome(knapsackCount, itemCount)
            chromosome.calculateFitness(self.knapsacks, self.items)
            self.population.append(chromosome)
        
        #print("Population Created")
    
    def createPopulation_WithDefined(self, knapsacks, items, populationCount): #create population with user defined knapsacks and items, 
        self.knapsackCount = len(knapsacks)
        self.itemCount = len(items)
        self.populationCount = populationCount
        self.knapsacks = []
        self.items = []
        self.population = []

        for i in range(0, populationCount // 2):
            chromosome = Chromosome(knapsackCount, itemCount)
            chromosome.calculateFitness(self.knapsacks, self.items)
            self.population.append(chromosome)

    def runGenerations(self, mutationRate): #runs the population and generates new children to the knapsack and prints the optimal solution
        mating = Mating()
        bestFitness = self.population[0].fitness
        bestFitnessIndex = 0
        i = 0
        while (len(self.population) < self.populationCount):
            if i < self.populationCount - 1:
                if self.population[i].fitness > 0:
                    parent1 = self.population[i]
                    parent2 = self.population[i + 1]
                    
                    child1, child2 = mating.crossover(parent1.chromosome, parent2.chromosome)
                    child1.calculateFitness(self.knapsacks, self.items)
                    child2.calculateFitness(self.knapsacks, self.items)

                    self.population.append(child1)
                    self.population.append(child2)
                else:
                    child = mating.mutate(self.population[i].chromosome, self.knapsackCount)
                    child.calculateFitness(self.knapsacks, self.items)
                    self.population.append(child)
            else:

                parent1 = self.population[i]
                parent2 = self.population[0]

                child1, child2 = mating.crossover(parent1.chromosome, parent2.chromosome)
                child1.calculateFitness(self.knapsacks, self.items)
                child2.calculateFitness(self.knapsacks, self.items)

                self.population.append(child1)
                self.population.append(child2)

            for j in range(len(self.population)):
                if self.population[j].fitness > bestFitness:
                
                    bestFitness = self.population[j].fitness
                    bestFitnessIndex = j

            if i % 2 > mutationRate:
                child = mating.mutate(self.population[i].chromosome, self.knapsackCount)
                child.calculateFitness(self.knapsacks, self.items)
                self.population[i] = child

            print("Fitness: {} | Chromosome: {} | Generation: {}".format(self.population[i].fitness, self.population[i].chromosome, i))
            i += 1

        print("\nBest Fitness: {} | Chromosome: {}".format(bestFitness, self.population[bestFitnessIndex].chromosome))
        for i in range(len(self.knapsacks)):
            knapsackItems = []
            profit = 0
            for j in range(len(self.population[bestFitnessIndex].chromosome)):
                if self.knapsacks[i].name == self.population[bestFitnessIndex].chromosome[j]:
                    knapsackItems.append(j)
                    profit += self.items[j].profit
            print("Knapsack Name: {} | Items: {} | Profit: {}".format(self.knapsacks[i].name, knapsackItems, profit))


class Mating: #Class to define the two mating processes

    def crossover(self, chromosome1, chromosome2): #defines the crossover functionality with the pivot/cross over point and the new children chromosomes
        crossoverPoint = random.randint(1, len(chromosome1) - 1)

        crossChromosome1 = chromosome1[crossoverPoint:]
        crossChromosome2 = chromosome2[crossoverPoint:]

        chromosome1 = chromosome1[:crossoverPoint]
        chromosome2 = chromosome2[:crossoverPoint]

        chromosome1.extend(crossChromosome2)
        chromosome2.extend(crossChromosome1)

        newChromosome1 = Chromosome(None, None, chromosome1)
        newChromosome2 = Chromosome(None, None, chromosome2)

        return newChromosome1, newChromosome2

    def mutate(self, chromosome, knapsackCount): #defines the mutate functionality which randomly changes the value

        for i in range(len(chromosome)):
            k = random.uniform(0, 1)

            if k > 0.5:
                chromosome[i] = random.randint(0, knapsackCount)
    
        newChromosome = Chromosome(None, None, chromosome)
        return newChromosome


class Chromosome: #Defines the chromosome class
    
    def __init__(self, knapsackCount, itemCount, chromosome = None): #initialize the chromosome with random knapsack values
        self.chromosome = []
        if chromosome == None:
            
            for i in range(0, itemCount):
                self.chromosome.append(random.randint(0,knapsackCount - 1))
            self.fitness = 0
        else:
            self.chromosome = chromosome

    def calculateFitness(self, knapsacks, items): #calculates the fitness for each chromosome
        fitness = 0
        knapsacksCopy = copy.deepcopy(knapsacks)
        for i in range(len(self.chromosome)):
            for knapsack in knapsacksCopy:
                if knapsack.name == self.chromosome[i]:
                    if items[i].weight > knapsack.weightRemaining:
                        continue
                        #fitness += 0
                    else:
                        knapsack.weightRemaining -= items[i].weight
                        fitness += items[i].profit
        self.fitness = fitness


class KnapsackItem:

    def __init__(self, weight, profit):
        self.weight = weight
        self.profit = profit


class Knapsack:

    def __init__(self, name, weightLimit):
        self.name = name
        self.weightLimit = weightLimit
        self.weightRemaining = weightLimit


GA = GeneticAlgorithm_MultiKnapsack()
knapsackCount = 3
knapsackMinWeight = 10
knapsackMaxWeight = 50

itemCount = 5
itemMinWeight = 5
itemMaxWeight = 35
itemMinProfit = 5
itemMaxProfit = 45

populationCount = 20
GA.createPopulation(knapsackCount, knapsackMinWeight, knapsackMaxWeight, itemCount, itemMinWeight, itemMaxWeight, itemMinProfit, itemMaxProfit, populationCount)
mutationRate = 0.65
GA.runGenerations(mutationRate)