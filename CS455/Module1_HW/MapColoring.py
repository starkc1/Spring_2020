from collections import deque

# CS 455 - Artificial Intelligence
# Module 1 - Search Homework
# Based off the provided python search classes
# Contributers - Cameron Stark & Dustin Cribbs with assitance from Alex Hendrik


class SearchClass: #Base search class with functions for adding, removing and searching
    def __init__(self):
        self.unexpandedList = deque()
        self.expandedList = set()
        self.regionList = []
        self.requestedMaxColors = 3
    
    def getOpen(self): #abstract function for getting the next region
        pass

    def appendUnexpanded(self, region): #add region to unvisted list
        self.unexpandedList.append(region)

    def appendExpanded(self, region): #add region to visited list
        self.expandedList.add(region)

    def goalTest(self): #test if goal has been reached
        for region in self.regionList:
            if region.color < 1:
                return False
        return True

    def getRegionNeighbors(self, region): #gets the neighbors of the self region
        neighborList = []

        for region in region.neighborList:
            
            for item in self.regionList:
                if item.getLabel() == region:
                    if item.color != 0:
                        continue
                    neighborList.append(item)
        
        return neighborList

    def hasRegionBeenExpanded(self, region): #check if self region has been visited
        if region in self.expandedList: return True
        return False

    def printRegions(self): #print function
        for region in self.regionList:
            print(str(region))
    
    def neighborColors(self, region): #gets self region neighbors (children)
        neighborColors = []

        count = 0
        for region in region.neighborList:
            for item in self.regionList:
                if item.getLabel() == region:
                    neighborColors.append(item.color)
        color = 1

        while True:
            if color in neighborColors:
                color += 1
            else:
                break

        return color

    def createUniqueRegionList(self, regionNumber): #creates region list of unique regions
        count = 1

        while count <= regionNumber:
            self.regionList.append(RegionClass("r" + str(count)))
            count += 1

            

    def searching(self, maxColorCount, map, regionNumber): #base searching function 
        self.createUniqueRegionList(regionNumber)
        self.requestedMaxColors = maxColorCount

        count = 0
        for region in self.regionList: #builds region neighbors
            for pair in map:
                if region.getLabel() == pair[0]:
                    if pair[0] not in self.regionList[count].neighborList:
                        self.regionList[count].neighborList.append(pair[1])
                if region.getLabel() == pair[1]:
                    if pair[0] not in self.regionList[count].neighborList:
                        self.regionList[count].neighborList.append(pair[0])

            count += 1
        
        self.appendUnexpanded(self.regionList[0])
        regionCount = 0

        while len(self.unexpandedList) > 0:
            
            currentRegion = self.getOpen()
            
            if self.hasRegionBeenExpanded(currentRegion):
                return None
            else:
                regionCount += 1

                regionColor = self.neighborColors(currentRegion)
                if regionColor <= self.requestedMaxColors:
                    currentRegion.color = regionColor
                else:
                    continue
                
                self.appendExpanded(currentRegion)

                if self.goalTest():
                    print("Goal reached after ", regionCount, " steps")
                    return currentRegion

                for regionNeighbor in self.getRegionNeighbors(currentRegion):
                    regionNeighbor.parent = currentRegion
                    self.appendUnexpanded(regionNeighbor)
            
            



class RegionClass: #base region class with label, parent, neighbor list, depth and color
    
    def __init__(self, label, parent=None):
        
        self.label = label
        self.parent = parent

        self.neighborList = []
        self.color = 0

        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 1

    def getLabel(self):
        return self.label
    
    def getRegionDepth(self):
        return self.depth

    def getRegionParent(self):
        return self.parent

    def __str__(self):
        return "{} = {}".format(self.label, str(colors[self.color]))



colors = [None, "red", "blue", "green", "yellow", "orange", "purple"]

class BFS_Search(SearchClass): 
    def getOpen(self):
        return self.unexpandedList.popleft()

class DFS_Search(SearchClass):
    def getOpen(self):
        return self.unexpandedList.pop()

class IDFS_Search(DFS_Search):

    def __init__(self, limit, step=1):
        super().__init__()
        self.limit = limit
        self.step = step

    def searching(self, maxColorCount, map, regionNumber):
        self.createUniqueRegionList(regionNumber)
        self.requestedMaxColors = maxColorCount
        
        count = 0
        for region in self.regionList: #builds region neighbors
            for pair in map:
                if region.getLabel() == pair[0]:
                    if pair[0] not in self.regionList[count].neighborList:
                        self.regionList[count].neighborList.append(pair[1])
                if region.getLabel() == pair[1]:
                    if pair[0] not in self.regionList[count].neighborList:
                        self.regionList[count].neighborList.append(pair[0])

            count += 1
        
        for limitCount in range(1, self.limit + 1, self.step):
            self.unexpandedList.clear()
            
            self.appendUnexpanded(self.regionList[0])
            self.expandedList.clear()
        
            for region in self.regionList:
                region.color = 0

            regionCount = 0
            depth = 0
            
            while len(self.regionList) > 0:
                
                currentRegion = self.getOpen()
                
                if self.hasRegionBeenExpanded(currentRegion):
                    return None
                else:
                    
                    
                    regionCount += 1
                    
                    regionColor = self.neighborColors(currentRegion)

                    if regionColor <= self.requestedMaxColors:
                        currentRegion.color = regionColor
                        depth += 1
                        currentRegion.depth = depth
                    else:
                        continue

                    self.appendExpanded(currentRegion)

                    if self.goalTest():
                        print("Goal reached after ", regionCount, " steps")
                        return currentRegion
                    
                    
                    if currentRegion.getRegionDepth() < limitCount:
                        for regionNeighbor in self.getRegionNeighbors(currentRegion):
                            regionNeighbor.parent = currentRegion
                            self.appendUnexpanded(regionNeighbor)
                    else: 
                        break
        return None



bfsSearch = BFS_Search()
dfsSearch = DFS_Search()
idfsSearch = IDFS_Search(10, 1)

map = [("r1", "r2"), ("r1", "r3"), ("r2", "r4"), ("r3", "r4")]
bfsSearch.searching(3, map, 4)
bfsSearch.printRegions()

dfsSearch.searching(3, map, 4)
dfsSearch.printRegions()

idfsSearch.searching(3, map, 4)
idfsSearch.printRegions()

