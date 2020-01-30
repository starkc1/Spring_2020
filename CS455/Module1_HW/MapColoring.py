from collections import deque

# CS 455 - Artificial Intelligence
# Module 1 - Search Homework
# Contributers - Cameron Stark & Dustin Cribbs

class SearchClass:
    def __init__(self):
        self.unexpandedList = deque()
        self.expandedList = set()
        self.regionList = []
        self.requestedMaxColors = 0
    
    def appendUnexpanded(self, region):
        self.unexpandedList.append(region)

    def appendExpanded(self, region):
        self.expandedList.add(region)

    def goalTest(self):
        for region in self.regionList:
            if region.color < 1:
                return False
            else:
                return True

    def getRegionNeighbors(self, region):
        neighborList = []

        for regionIndex in region.neighborList:
            if self.regionList[regionIndex].color != 0:
                continue

            neighborList.append(self.regionList[regionIndex])
        
        return neighborList

    def hasRegionBeenExpanded(self, region):
        if region in self.expandedList:
            return True
        else:
            return False

    def printRegions(self):
        for region in self.regionList:
            print(str(region), "\n")
    
    def neighborColors(self, region):
        neighborColors = []
        count = 0
        for region in region.neighborList:
            if region in self.regionList:
                neighborColors.append(self.regionList[count].color)
            count += 1 
            #neighborColors.append(self.regionList[region].color)
        
        color = 1
        while True:
            if color in neighborColors:
                color += 1
            else:
                break

        return color

    def createUniqueRegionList(self, map):
        for region in map:
            if region[0] not in self.regionList:
                self.regionList.append(RegionClass(region[0]))
            if region[1] not in self.regionList:
                self.regionList.append(RegionClass(region[1]))
            

    def searching(self, maxColorCount, map):
        self.createUniqueRegionList(map)
        self.requestedMaxColors = maxColorCount
        for regionPair in map:
            self.regionList[0].neighborList.append(regionPair[1])
            self.regionList[1].neighborList.append(regionPair[0])
        
        self.appendUnexpanded(self.regionList[0])
        regionCount = 0

        while self.appendUnexpanded:
            
            currentRegion = self.getOpen()

            if self.hasRegionBeenExpanded(currentRegion):
                return None
            else:
                regionCount += 1

                regionColor = self.neighborColors(currentRegion)

                if regionColor > self.requestedMaxColors:
                    continue
                else:
                    currentRegion.color = regionColor
                
                self.appendExpanded(currentRegion)

                if self.goalTest():
                    print("Goal reached after ", regionCount, " steps")
                    return currentRegion
                
                for regionNeighbor in self.getRegionNeighbors(currentRegion):
                    self.appendUnexpanded(regionNeighbor)



class RegionClass:
    
    def __init__(self, label, parent=None):
        
        self.label = label
        self.parent = parent

        self.neighborList = []
        self.color = colors[0]

        if parent:
            self.depth = parent.depth + 1
        else:
            1
    
    def getRegionDepth(self):
        return self.depth

    def getRegionParent(self):
        return self.parent

    def __str__(self):
        string = self.label + " = " + self.color
        return string



colors = ["none", "red", "blue", "green", "yellow", "orange", "purple"]

class BFS_Search(SearchClass):
    def getOpen(self):
        return self.unexpandedList.popleft()


bfsSearch = BFS_Search()
bfsSearch.searching(3, [("r1", "r2"), ("r1", "r3"), ("r2", "r4"), ("r3", "r4")])
bfsSearch.printRegions()