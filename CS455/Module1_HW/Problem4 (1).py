from collections import deque
from enum import IntEnum

# Authors:
# Luis Olivier (CS 455)
# Alex Hendrik (CS 595)
#
# Credit to Dr. Stansbury for sample search algorithms that we modified


# Enum for simplifying color assignment
class Color(IntEnum):
    NA = 0
    Red = 1
    Green = 2
    Blue = 3
    Yellow = 4
    Purple = 5
    Orange = 6

# Node class to represent a map region with an adjacency list and the region color
class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None

        self.adjacencyList = []

        self.color = 0

        self.depth = 0

    def getDepth(self):
        return self.depth

    def getParent(self):
        return self.parent

    # Override for easy result printing
    def __str__(self):
        return "{} = {}".format(self.name, Color(self.color).name)



# Generic superclass containing most of the search functionality
class SearchManager:

    def __init__(self):
        self.openList = deque()
        self.closedList = set()
        self.nodeList = []
        self.colorLimit = 3


    def addToOpen(self, node):
        self.openList.append(node)


    def addToClosed(self, node):
        self.closedList.add(node)


    def getOpen(self):
        pass

    # Check to make sure that all of the regions have a color
    def goalTest(self):
        for node in self.nodeList:
            if node.color == 0: 
                return False
        return True


    # Get successors from a node that do not have an assigned color
    def getNodeSuccessors(self, node):
        successorList = []

        for nodeIndex in node.adjacencyList:
            if self.nodeList[nodeIndex].color != 0:
                continue
            successorList.append(self.nodeList[nodeIndex])
        
        return successorList


    def isNodeClosed(self, node):
        return True if node in self.closedList else False


    def printResult(self):
        if(self.goalTest()):
            for node in self.nodeList:
                print(str(node) + "\n")
        else:
            print("No solution was found...")


    # Return the lowest color value given the adjacent node colors
    def checkAdjacentColors(self, node):
        adjacentColors = []
        for node in node.adjacencyList:
            adjacentColors.append(self.nodeList[node].color)
        color = 1
        while color in adjacentColors:
            color += 1
        return color

    # Create all of the node objects and add them to the master list
    def generateNodes(self, nodeCount):
        i = nodeCount
        while i > 0:
            self.nodeList.append(Node("R{}".format(nodeCount - i)))
            i -= 1

    # Primary search functionality
    def search(self, nodeCount, mapInput):
        self.generateNodes(nodeCount)
        
        # Populate adjacency lists
        for pair in mapInput:
            self.nodeList[pair[0]].adjacencyList.append(pair[1])
            self.nodeList[pair[1]].adjacencyList.append(pair[0])

        self.addToOpen(self.nodeList[0])

        count = 0
        depth = 0

        while len(self.openList) > 0:

            currentNode = self.getOpen()

            if not self.isNodeClosed(currentNode):
                count += 1

                color = self.checkAdjacentColors(currentNode)

                # If the lowest available color is outside of the limit of colors - don't assign
                if color <= self.colorLimit:
                    currentNode.color = color
                    depth += 1
                    currentNode.depth = depth
                else:
                    continue

                self.addToClosed(currentNode)

                if self.goalTest():
                    print("Solution found after {} nodes have been evaluated!".format(count))
                    return currentNode

                for successorNode in self.getNodeSuccessors(currentNode):
                    successorNode.parent = currentNode
                    self.addToOpen(successorNode)

        return None

# Subclass for BFS
class BreadthFirstSearch(SearchManager):

    def getOpen(self):
        return self.openList.popleft()

# Subclass for DFS
class DepthFirstSearch(SearchManager):

    def getOpen(self):
        return self.openList.pop()

# Subclass for IDFS
class IterativeDepthFirstSearch(DepthFirstSearch):

    def __init__(self, limit, step=1):
        super().__init__()
        self.maxdepth = limit
        self.step = step


    def search(self, nodeCount, mapInput):
        self.generateNodes(nodeCount)

        # Populate adjacency lists
        for pair in mapInput:
            self.nodeList[pair[0]].adjacencyList.append(pair[1])
            self.nodeList[pair[1]].adjacencyList.append(pair[0])

        # Start the iterative loop
        for lim in range(1, self.maxdepth + 1, self.step):

            # Reset all iteration variables (bad programming practice using common variables)

            self.openList.clear()
            self.addToOpen(self.nodeList[0])
            self.closedList.clear()

            for node in self.nodeList:
                node.color = 0

            count = 0
            depth = 0

            while len(self.openList) > 0:

                currentNode = self.getOpen()

                if not self.isNodeClosed(currentNode):
                    count += 1

                    color = self.checkAdjacentColors(currentNode)

                    # If the lowest available color is outside of the limit of colors - don't assign
                    if color <= self.colorLimit:
                        currentNode.color = color
                        depth += 1
                        currentNode.depth = depth
                    else:
                        continue

                    self.addToClosed(currentNode)

                    if self.goalTest():
                        print("Solution found after {} nodes have been evaluated!".format(count))
                        return currentNode

                    if currentNode.getDepth() < lim:
                        for successorNode in self.getNodeSuccessors(currentNode):
                            successorNode.parent = currentNode
                            self.addToOpen(successorNode)
                    else:
                        break

        return None
    


# A couple test cases

bfs = BreadthFirstSearch()
dfs = DepthFirstSearch()
idfs = IterativeDepthFirstSearch(8,1)

#solution = search.search(3,[(0,1), (0,2), (1,2)])
#solution = search.search(4,[(0,1),(0,2), (1,3), (2,3)])
#solution = search.search(5,[(0,1),(0,2), (1,3), (2,3), (2,4), (3,4)])

# This specific test case seems to only have one solution so the three algorithms will have identical outputs
solution = bfs.search(6,[(0,1),(0,2), (1,3), (2,3), (2,4), (3,4), (2,5), (4,5)])
solution = dfs.search(6,[(0,1),(0,2), (1,3), (2,3), (2,4), (3,4), (2,5), (4,5)])
solution = idfs.search(6,[(0,1),(0,2), (1,3), (2,3), (2,4), (3,4), (2,5), (4,5)])

print("BFS---------------------------")
bfs.printResult()
print("DFS---------------------------")
dfs.printResult()
print("IDFS---------------------------")
idfs.printResult()
