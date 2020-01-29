from collections import deque

class SearchClass:
    """
    Abstract implementation of uninformed search algorithm and supporting methods
    """

    def __init__(self):
        """
        Initializes the Search class by creating the open list and closed list.
        """
        self.openL = deque() # python class for queues and stacks
        self.closedL = set() # empty list
        

    def addOpen(self, node):
        """
        Abstract method to add a new node to the open list.
        @param node - search node to add to the open list
        """
        pass

    
    def getOpen(self):
        """
        Abstract method to return the front of the open list.
        @return front of open list (based on data structure used)
        """
        pass

    def addClosed(self, node):
        """
        Adds a search node's state to the closed list.
        @param node - node that is closed (i.e. visited)
        """
        self.closedL.add(node)

    def isClosed(self, node):
        """
        Determines if a search node is in the closed list
        based upon the node's state.
        @return True if state is closed; False if it is not.
        """
        if node in self.closedL: return True
        return False
    
    def printPath(self, end):
        """
        Prints the solution path.  It builds a string, which 
        it finally prints once it has traversed from the tail of
        the solution path to its head.
        
        Note: a recursive solution could work, but exceeds the 
        Python recursive depth limit for problems with deep solution
        paths.
    
        @param end - last node in the solution path
        """
        strPath = ""
        cur = end
        while cur:
            strPath = "" + str(cur) + "\n" + strPath
            cur = cur.parent
        print(strPath)

        
    def search(self, initialS, goal=None):
        """
        Implements search method
        @param initialS - initial state
        @param goal - target goal state (default None)
        @return search node at solution state
        """
        # Initial state Added to front of open list
        self.addOpen(initialS)
        counter = 0

        # Loop until open list is empty
        while len(self.openL) > 0:
            
            # Current Node is next open in the open list
            curN = self.getOpen()
            
            # Cycle Avoidance - determines if current node is already
            #   closed.  O(n) operation.
            if not self.isClosed(curN):
                counter += 1
                
                # Add node to closed list
                self.addClosed(curN)

                # Determine if current node is goal
                if curN.goalTest(goal):
                    print("Solution Found - " + str(counter) + " Nodes Evaluated.")
                    print("Goal depth: " + str(curN.depth))
                    return curN 
                
                # Interate on successors of current node
                for successorS in curN.getSuccessors():
                    self.addOpen(successorS)
                    
        # Return none if no solution found.    
        return None    
        
class SearchNode:
    """
    Abstract implementation of a search node for uninformed search
    """
    
    def __init__(self, state, parent=None):
        """
        Initializes the node with the current state and parent, if provided.
        @param state - problem state to be stored in node.
        @param parent - parent node (optional)
        """
        self.state = state
        self.parent = parent
        
        # New node's depth is parent's depth + 1
        if parent: 
            self.depth = parent.depth + 1
        else:
            self.depth = 1
            
    def getDepth(self):
        """
        @return depth of node
        """
        return depth
    
    def __eq__(self, other):
        """
        Abstract method to determine if two nodes are storing equal
        state values.
        @param other - other state node
        @return true if equivalent states; false otherwise
        """
        pass
    
    def __hash__(self):
        """
        Abstract method to return has value of node based on string representation of state.
        """
        pass
    
    def __str__(self):
        """
        Abstract method to represent the state stored in the node as a string
        @return string representation of state
        """
        pass
    
    def getSuccessors(self):
        """
        Abstract successor function
        @return list of successors for node
        """
        pass

    
    def goalTest(self, goal):
        """
        Abstract method for goal test.
        @param goal - goal condition for goal test
        """
        pass


class BreadthFirstSearch(SearchClass):
    """
    Concrete implementation of SearchClass for BreadthFirstSearch algorithm
    
    The open list is a queue.
    """
    
    def addOpen(self, node):
        """
        Appends node to the end of a queue.
        @param node - search node to add to queue.
        """
        self.openL.append(node)
        
    def getOpen(self):
        """
        Dequeues and returns front of open queue.
        @return search node at front of queue
        """
        return self.openL.popleft()