import numpy as np
import matplotlib.pyplot as plt
import sys

class Chromosome:
    """ 
    Implements an abstract chromosome class data type
    """
    
    def crossover(self, other):
        """
        Abstract method to implement cross-over between two chromosomes.
        @param other - other chromosome
        @return child1, child2 - output of the chromosome's children resultant from crossover
        """
        pass
    
    
    def mutate(self):
        """
        Abstract method to implement mutate operation on a chromosome.
        @return mutated chromosome
        """
        pass
    
    
    def getFitness(self):
        """
        Abstract method to implement the fitness evaluation for the chromosome.
        @return fitness value
        """
        pass
    
    def clone(self):
        """
        Abstract method to clone an instance of a chromosome
        """
        pass
    
    def __str__(self):
        """
        Abstract method to generate a string representation of the chromosome for printing.
        """
        pass

class GeneticAlgorithm:
    """
    Defines an abstract class for genetic algorithm.  All methods are implemetned
    except for buildInitialPopulation, which must be tailored to the Chromosome class
    used.
    """
    
    def __init__(self, popSize, generations, cross, mutate):
        """
        Initialization method for genetic algorithm class
        @param popSize - population size
        @param generations - number of generations the algorithm will run
        @param cross - probability of a crossover occuring during reproduction
        @param mutate - probability of a mutation occuring following reproduction
        """
        
        # Set GA parameter class variables
        self.populationSize = popSize
        self.numGenerations = generations
        self.probC = cross
        self.probM = mutate
        self.bests = []
        self.averages = []
        
        # Initialize list class variables for population and roulette wheel
        self.population = [None for i in range(0,popSize)]
        self.roulette_min = [0 for i in range(0,popSize)]
        self.roulette_max = [0 for i in range(0,popSize)]
        
    def buildInitialPopulation(self):
        """
        Abstract method to generate a population of chromosomes.
        """
        pass
    
    def calculateRoulette(self):
        """
        Constructs a roulette wheel for parent selection.
        """
        
        # Determine the total fitness
        sum = 0
        for chromosome in self.population:
            sum = sum + chromosome.getFitness()
        
        # Generates roulette wheel where roulette_max[i] - roulette_min[i] == chromosome[i].getFitness()
        self.roulette_min[0] = 0
        for i in range(0, self.populationSize):
            if i != 0:
                self.roulette_min[i] = self.roulette_max[i-1]
            self.roulette_max[i] = self.roulette_min[i] + self.population[i].getFitness() / sum

    def pickChromosome(self):
        """
        Using roulette wheel, returns the index of a parent for reproduction.
        @return index of chromosome to reproduce.
        """
        spin = np.random.uniform()
        for i in range(0,self.populationSize):
            if spin > self.roulette_min[i] and spin <= self.roulette_max[i]:
                return i
        return self.populationSize-1
    

    def reproductionLoop(self):
        """ 
        Implements the GA algorithm's reproduction loop.  It is called once per generation.
        """
        newPop = []

        # Look through population populationSize/2 times
        #  each iteration generates two children
        for i in range(0, self.populationSize, 2):
            
            # Clone parents - Python copies by reference so we want to
            #  make sure we do not update the parents by mistake.
            x = self.population[self.pickChromosome()].clone()
            y = self.population[self.pickChromosome()].clone()
            
            # Crossover given crossover probabilty
            if (np.random.uniform() < self.probC):
                x, y = x.crossover(y)                
            
            # Mutate given mutate probability for each child
            if (np.random.uniform() < self.probM):
                x.mutate()
                
            if (np.random.uniform() < self.probM):
                y.mutate()
            
            # Add Children to new population
            newPop.append(x)
            newPop.append(y)
            
        # Update GA population with new population
        self.population = newPop    
    
    
    def getBest(self):
        """
        Prints the results of the current generation.  
        @return best chromosome
        """
        
        best = self.population[0]
        sum = 0
        fit = []
        
        for chromosome in self.population:
            sum = sum + chromosome.getFitness()
            if chromosome.getFitness() > best.getFitness():
                best = chromosome
        
        self.bests.append(best.getFitness())
        self.averages.append(sum/self.populationSize)
        print("Best State: " + str(best.getFitness()) + ",  Avg. State: " + str(sum/self.populationSize))
        return best
    
    def plotScores(self):
        plt.plot(self.bests)
        plt.plot(self.averages)
        plt.ylim(bottom=0)
        plt.show()
    
    
    def runGA(self, target=sys.maxsize):
        """
        Implements the main GA population loop
        """
        
        # Initialize Variables toTrack best by generation and overall
        best = None
        bestOverall = None
        
        # Build initial poulation
        self.buildInitialPopulation()
        for i in range(0, self.numGenerations):

            # Generate roulette wheel for current population
            self.calculateRoulette()
        
            # Execute the GA reproduction loop for this generation
            self.reproductionLoop()
        
            # print generation's fitness and get best chromosome
            best = self.getBest()
            
            # Track the best
            if bestOverall is None:
                bestOverall = best
            elif best.getFitness() > bestOverall.getFitness():
                bestOverall = best
            
            # If target is reached, end algorithm
            if best.getFitness() >= target:
                print("Solution found at generation " + str(i))
                bestOverall = best
                break
        
        # Prints the best overall solution
        print("Best overall Solution")
        print("Fitness: " + str(bestOverall.getFitness()))
        print(bestOverall)
        self.plotScores()