from collections import deque
from enum import IntEnum

class Color(IntEnum):
    NA = 0
    Red = 1
    Green = 2
    Blue = 3

    #TODO implement color limit selector

class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

        self.adjacencyList = []

        self.color = Color(0)

        self.depth = parent.depth + 1 if parent else 1

    def getDepth(self):
        return self.depth

    def getParent(self):
        return self.parent

    def __str__(self):
        return "{} = {}".format(self.name, Color(self.color).name)




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

    def goalTest(self):
        for node in self.nodeList:
            if node.color < 1: return False
        return True

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
        for node in self.nodeList:
            print(str(node) + "\n")

    def checkAdjacentColors(self, node):
        adjacentColors = []
        for node in node.adjacencyList:
            adjacentColors.append(self.nodeList[node].color)
        color = 1
        while True:
            if color in adjacentColors:
                color += 1
            else:
                break
        return color



    def generateNodes(self, nodeCount):
        i = nodeCount
        while i > 0:
            self.nodeList.append(Node("R{}".format(nodeCount - i)))
            i -= 1


    def search(self, nodeCount, mapInput):
        self.generateNodes(nodeCount)
        
        for pair in mapInput:
            
            self.nodeList[pair[0]].adjacencyList.append(pair[1])
            self.nodeList[pair[1]].adjacencyList.append(pair[0])

        self.addToOpen(self.nodeList[0])
        count = 0

        while len(self.openList) > 0:

            currentNode = self.getOpen()

            if not self.isNodeClosed(currentNode):
                count += 1

                color = self.checkAdjacentColors(currentNode)

                if color <= self.colorLimit:
                    currentNode.color = color
                else:
                    continue

                self.addToClosed(currentNode)

                if self.goalTest():
                    print("Solution found after {} nodes have been evaluated!".format(count))
                    print("Goal depth is {}".format(currentNode.getDepth()))
                    return currentNode

                for successorNode in self.getNodeSuccessors(currentNode):
                    self.addToOpen(successorNode)

        return None

class BreadthFirstSearch(SearchManager):
    def getOpen(self):
        return self.openList.popleft()

class DepthFirstSearch(SearchManager):
    def getOpen(self):
        return self.openList.pop()
    


search = BreadthFirstSearch()
#search = DepthFirstSearch()
#solution = search.search(3,[(0,1), (0,2), (1,2)])
solution = search.search(4,[(0,1),(0,2), (1,3), (2,3)])
search.printResult()