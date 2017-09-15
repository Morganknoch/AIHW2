# dictionary for nodes visited
import copy
import time
import queue
import heapq
from operator import itemgetter
#[0 1 2]
#[3 4 5]
#[6 7 8]

# dictionary holding the legal moves that can be performed depending on the location of the '.'
moves = {}
moves[(0,0)] = ['DOWN', 'RIGHT']
moves[(0,1)] = ['LEFT', 'DOWN','RIGHT']
moves[(0,2)] = ['LEFT', 'DOWN']
moves[(1,0)] = ['UP', 'RIGHT', 'DOWN']
moves[(1,1)] = ['LEFT', 'UP', 'RIGHT', 'DOWN']
moves[(1,2)] = ['LEFT', 'UP', 'DOWN']
moves[(2,0)] = ['UP', 'RIGHT']
moves[(2,1)] = ['LEFT', 'UP', 'RIGHT']
moves[(2,2)] = ['LEFT', 'UP']

# dictionary holding the actual locations of the final state
location = {}
location[1] = [0,0]
location[2] = [0,1]
location[3] = [0,2]
location[4] = [1,0]
location[5] = [1,1]
location[6] = [1,2]
location[7] = [2,0]
location[8] = [2,1]
location['.'] = [2,2]

# the input puzzles to the program
a = [['.', 1, 3],[4, 2, 5],[7, 8, 6]]
b = [['.', 5, 2], [1, 8, 3], [4, 7, 6]]
c = [[8, 6, 7], [2, 5, 4], [3, '.', 1]]


# SWITCH THESE TO RUN WITHOUT THE THIRD CASE
init_states=[a, b, c]
# init_states=[a, b]


final_state = [[1,2,3],[4,5,6],[7,8,'.']]

# global variables
numNodesGen = 0
numNodesExpanded = 0
numPrintExpanded = 0
isAstar = False
minQueue = []


#--------------------------------------------------------------
#
#   main()
#       Main function
#
#--------------------------------------------------------------
def main():
    global numNodesGen, numNodesExpanded, numPrintExpanded

    # Iterative Deepening Search for three inputs
    i = 1
    print("\n\n------------------------------------------------------------------------\nIterative Deepening Search: ")
    for input in init_states:
        print("\nInput " + str(i) + ":")
        print("First five nodes expanded: ")
        numNodesGen = 0
        numNodesExpanded = 0
        numPrintExpanded = 0
        start_time = time.time()
        x = IDS(input)
        end_time = time.time() - start_time
        end_time = end_time * 1000                # Convert time in seconds to milliseconds
        # Check for failure
        if( x == None ):
            print("Search Failed!")
        else:
            print("Solution sequence: ") 
            printSequence(x)

        print("Number of nodes expanded: " + str(numNodesExpanded) )
        print("CPU execution time: " + str(end_time) + " ms")
        i = i + 1
    
    # Depth First Graph Search for three inputs
    i = 1
    print("\n\n------------------------------------------------------------------------\nDepth First Graph Search: ")
    for input in init_states:
        print("\nInput " + str(i) + ":")
        print("First five nodes expanded: ")
        numNodesGen = 0
        numNodesExpanded = 0
        numPrintExpanded = 0
        start_time = time.time()
        x = DFGS(input)
        end_time = time.time() - start_time
        end_time = end_time * 1000                # Convert time in seconds to milliseconds
        # Check for failure
        if( x == None ):
            print("Search Failed!")
        else:
            print("Solution sequence: ") 
            printSequence(x)
        print("Number of nodes expanded: " + str(numNodesExpanded) )
        print("CPU execution time: " + str(end_time) + " ms")
        i = i + 1
    
    # A* Search for three inputs
    i = 1
    print("\n\n------------------------------------------------------------------------\nA* search: ")
    for input in init_states:
        global isAstar
        isAstar = True
        print("\nInput " + str(i) + ":")
        print("First five nodes expanded: ")
        numNodesGen = 0
        numNodesExpanded = 0
        numPrintExpanded = 0
        start_time = time.time()
        x = Astar(input)
        end_time = time.time() - start_time
        end_time = end_time * 1000                # Convert time in seconds to milliseconds
        # Check for failure
        if( x == None ):
            print("Search Failed!")
        else:
            print("Solution sequence: ") 
            printSequence(x)
        print("Number of nodes expanded: " + str(numNodesExpanded) )
        print("CPU execution time: " + str(end_time) + " ms")
        i = i + 1
 # main()
        
#--------------------------------------------------------------
#
#   manhattenDistance( node )
#       Calculates the cumulative manhatten distance for the
#       state
#
#--------------------------------------------------------------
def manhattenDistance( node ):
    array = node.array
    total = 0
    i = 0
    for x in array:
        j = 0
        for y in x:
            a, b = location[y]
            total = total + (abs(i-a) + abs(j-b))
            j = j + 1
        i = i + 1
    return total
# manhattenDistance()


#--------------------------------------------------------------
#
#   printSequence( node )
#       Prints the solution sequence
#
#--------------------------------------------------------------
def printSequence(node):
    nodeList = []
    nodeList.append(node)
    hold = node
    while( hold.parent != None):
        nodeList.append(hold.parent)
        hold = hold.parent
    
    nodeList.reverse()

    for item in nodeList:
        print(item.array)

    print("Number of moves to solution: " + str(len(nodeList)))
# printSequence()


#--------------------------------------------------------------
#
#   findSpace(state)
#       Returns the x,y position of the empty space
#
#--------------------------------------------------------------
def findSpace(state):
    i = 0
    for a in state.array:
        j = 0
        for b in a:
            if b == '.':
                return i,j
            j = j + 1
        i = i + 1     
# findSpace()
        

#--------------------------------------------------------------
#
#   Class GameBoardState( state )
#       Represents the state of the game board between moves
#
#--------------------------------------------------------------
class GameBoardState(object):
    def __init__( self, state ):
        self.array = copy.deepcopy(state)
        self.visited = None  # might not use this
        self.parent = None
        self.children = []
        self.pathCost = 0
        self.manhattenDistance = 0
        self.totalCost = 0
        self.tileNumber = 0
        global numNodesGen 
        numNodesGen = numNodesGen + 1

    # Calculate total cost;
    # i.e. path cost to self + estimated cost to goal node
    def calcCost( self ):
        self.calcMD()
        self.totalCost = self.pathCost + self.manhattenDistance

    # Calc states manhatten distance
    def calcMD( self ):
        total = 0
        i = 0
        for x in self.array:
            j = 0
            for y in x:
                a, b = location[y]
                total = total + (abs(i-a) + abs(j-b))
                j = j + 1
            i = i + 1
        self.manhattenDistance = total

    def __lt__( self, other ):
        if( self.totalCost != other.totalCost ):
            return self.totalCost < other.totalCost
        else:
            return self.tileNumber > other.tileNumber
# Class GameBoardState()


#--------------------------------------------------------------
#
#   IDS(start)
#       Performs an Itterative deepening tree search
#
#--------------------------------------------------------------
def IDS(start):

    limit = 0
    input = copy.deepcopy(start)

    # Limit expanded nodes to 100k
    while( numNodesExpanded <= 100000 ):     
        result = DLS(input, limit)
        if result:
            return result
        limit = limit + 1

    # Search failed
    return None
# IDS()


#--------------------------------------------------------------
#
#   DLS(start, limit)
#       Calls the recursive function for DLS
#
#--------------------------------------------------------------
def DLS(start, limit):
    return RecursiveDLS( GameBoardState(start), limit ) 
# DLS()


#--------------------------------------------------------------
#
#   RecursiveDLS(node, limit)
#       Perform a Depth Limited Search to find a solution
#
#--------------------------------------------------------------
def RecursiveDLS( node, limit ):
    # Local Vars
    failure = False

    # The solution has been found
    if node.array == final_state:
        return node
    
    # The depth limit has been reached
    elif limit == 0:
        return None

    # Continue further down the tree
    else:
        # print first five expanded nodes
        global numPrintExpanded
        if(numPrintExpanded <= 5):
            print(node.array)
            numPrintExpanded = numPrintExpanded + 1
        # count num expanded nodes
        global numNodesExpanded
        numNodesExpanded = numNodesExpanded + 1

        # Get children nodes
        children = generateChildNodes(node)

        # Expand each child node
        for child in children:
            result = RecursiveDLS(child, limit - 1)
            if not result:
                failure = True
            elif result:
                return result
        if failure:
            return None
# RecursiveDLS()


#--------------------------------------------------------------
#
#   DFGS( start )
#       Perform a Depth First Graph Search starting at the 
#       'start' state. 
#       Returns goal node on success and None object on failure
#
#--------------------------------------------------------------
def DFGS( start ):
    global numNodesExpanded
    global numPrintExpanded
    visited = []                # List of visited nodes
    fringe = queue.Queue(0)     # FIFO for fringe

    fringe.put( GameBoardState(start) ) # Put the starting state in the fringe

    # limit DPGS to 100k nodes
    while ( numNodesExpanded <= 100000 ):
        # Visited all nodes and didn't find the solution
        if( fringe.empty() == True ):   
            return None
        
        node = fringe.get()

        # Found solution
        if( node.array == final_state ):    
            return node
        
        # If node hasn't been visited
        if( hasVisited(visited, node) == False ):    
            visited.append(node)

            # Put all children in fringe
            for x in legalMoves(node):      
                child = makeNode(x, node)   # create node for child
                node.children.append(child) # add child to parents child list
                child.parent = node         # point child to parent
                fringe.put(child)           # add node to fringe

            # print first five expanded nodes
            if(numPrintExpanded <= 5):
                print(node.array)
                numPrintExpanded = numPrintExpanded + 1
            #count num expanded nodes
            numNodesExpanded = numNodesExpanded + 1
# DFGS()


#--------------------------------------------------------------
#
#   Astar( start_state )
#       Find solution path using A* algotithm
#
#--------------------------------------------------------------
def Astar( start_state ):
    # Local Vars
    global numNodesExpanded, numPrintExpanded
    minHeap = []

    # Create first node to start
    startNode = GameBoardState( start_state )
    startNode.calcCost()

    # Place startNode into min heap
    heapq.heappush( minHeap, startNode )
    
    while len(minHeap) != 0 and numNodesExpanded <= 100000:
        # Get smallest cost node from heap
        node = heapq.heappop( minHeap )   
        
        # We found the goal node
        if node.array == final_state:
            return node

        # Put children into minHeap
        for x in legalMoves(node):      # Put all children in fringe
            child = makeNode(x, node)   # create node for child
            node.children.append(child) # add child to parents child list
            child.parent = node  
            heapq.heappush( minHeap, child )
      
        # print first five expanded nodes
        if(numPrintExpanded <= 5):
            print(node.array)
            numPrintExpanded = numPrintExpanded + 1
        # count num expanded nodes
        numNodesExpanded = numNodesExpanded + 1

    return None
# Astar()


#--------------------------------------------------------------
#
#   hasVisited( list_visited, node )
#       Check if 'node' is in the list 'list_visited'.
#
#--------------------------------------------------------------
def hasVisited( list_visited, node ):
    for x in list_visited:
        if node.array == x:
            return True

    return False
# hasVisited()


#--------------------------------------------------------------
#
#   legalMoves( state )
#       Returns a list of the legal moves that can be done
#       depending on the location of the '.'
#
#--------------------------------------------------------------
def legalMoves(state):
    row, col = findSpace(state)
    return moves[(row,col)]
# legalMoves()


#--------------------------------------------------------------
#
#   generateChildNodes( node )
#       Generates all of the child nodes for a given node
#
#--------------------------------------------------------------
def generateChildNodes(node):
    # Local Vars
    children = []

    # Get the children
    for x in legalMoves(node):
        child = makeNode(x, node)
        node.children.append(child)
        child.parent = node
        children.append(child)
        
    children = sortChildren(children)
    return children
# generateChildNodes()


#--------------------------------------------------------------
#
#   sortChildren( children )
#       Sorts children by tile ID being moved, small -> big
#
#--------------------------------------------------------------
def sortChildren(children):
    for x in children:
        for y in children:
            if y.tileNumber < x.tileNumber:
                hold = children[children.index(x)]
                children[children.index(x)] = children[children.index(y)]
                children[children.index(y)] = hold
    return children
# sortChildren()


#--------------------------------------------------------------
#
#   makeNode(move, state)
#       Creates a node with the specified 'move' applied to the
#       'state'
#
#--------------------------------------------------------------
def makeNode(move, state):
    newstate = GameBoardState(state.array)

    if move == 'UP':
        holdi, holdj = findSpace(newstate)
        holdstate = newstate.array[holdi-1][holdj]
        newstate.array[holdi-1][holdj] = '.'
        newstate.array[holdi][holdj] = holdstate
        newstate.tileNumber = holdstate         
    elif move == 'DOWN':
        
        holdi, holdj = findSpace(newstate)
        holdstate = newstate.array[holdi+1][holdj]
        newstate.array[holdi+1][holdj] = '.'
        newstate.array[holdi][holdj] = holdstate
        newstate.tileNumber = holdstate
    elif move == 'LEFT':
        
        holdi, holdj = findSpace(newstate)
        holdstate = newstate.array[holdi][holdj-1]
        newstate.array[holdi][holdj-1] = '.'
        newstate.array[holdi][holdj] = holdstate
        newstate.tileNumber = holdstate
    else:
        
        holdi, holdj = findSpace(newstate)
        holdstate = newstate.array[holdi][holdj+1]
        newstate.array[holdi][holdj+1] = '.'
        newstate.array[holdi][holdj] = holdstate
        newstate.tileNumber = holdstate
    
    global isAstar

    if isAstar == True:
        newstate.pathCost = state.pathCost + 1
        newstate.calcCost()

    return newstate
# makeNode()


# Call main function
main()