# dictionary for nodes visited
import copy
import time
import queue
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

init_states=[c]

final_state = [[1,2,3],[4,5,6],[7,8,'.']]

# global variables
numNodesGen = 0
numNodesExpanded = 0
numPrintExpanded = 0
isAstar = False
minQueue = []

def main():
    global numNodesGen, numNodesExpanded, numPrintExpanded

    # Iterative Deepening Search for three inputs
    i = 1
    print("Iterative Deepening Search: ")
    for input in init_states:
        print("Input " + str(i) + ":")
        print("First five nodes expanded: ")
        numNodesGen = 0
        numNodesExpanded = 0
        numPrintExpanded = 0
        start_time = time.time()
        x = IDS(input)
        end_time = time.time() - start_time
        end_time = end_time * 1000                # Convert time in seconds to milliseconds
        print("Solution sequence: ") 
        printSequence(x)
        print("CPU execution time: " + str(end_time) + " ms")
        i = i + 1
    
    #i = 1
    #print("Depth First Graph Search: ")
    ## Depth First Graph Search for three inputs
    #for input in init_states:
    #    print("Input " + str(i) + ":")
    #    print("First five nodes expanded: ")
    #    numNodesGen = 0
    #    numNodesExpanded = 0
    #    numPrintExpanded = 0
    #    start_time = time.time()
    #    x = DFGS(input)
    #    end_time = time.time() - start_time
    #    end_time = end_time * 1000                # Convert time in seconds to milliseconds
    #    print("Solution sequence: ") 
    #    printSequence(x)
    #    print("CPU execution time: " + str(end_time) + " ms")
    #    i = i + 1
    
    #i = 1
    #print("A star search: ")
    #for input in init_states:
    #    global isAstar
    #    isAstar = True
    #    print("Input " + str(i) + ":")
    #    print("First five nodes expanded: ")
    #    numNodesGen = 0
    #    numNodesExpanded = 0
    #    numPrintExpanded = 0
    #    start_time = time.time()
    #    x = Astar(input)
    #    end_time = time.time() - start_time
    #    end_time = end_time * 1000                # Convert time in seconds to milliseconds
    #    print("Solution sequence: ") 
    #    printSequence(x)
    #    print("CPU execution time: " + str(end_time) + " ms")
    #    i = i + 1
      
def manhattenDistance(node):
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

def findSpace(state):
    # find the space ('.') to determine the legal moves that can be taken
    i = 0
    for a in state.array:
        j = 0
        for b in a:
            if b == '.':
                return i,j
            j = j + 1
        i = i + 1           

class GameBoardState(object):
    def __init__(self, state):
        self.array = copy.deepcopy(state)
        self.visited = None  # might not use this
        self.parent = None
        self.children = []
        self.cost = 0
        self.manhattenDistance = 0
        self.tileNumber = 0
        global numNodesGen 
        numNodesGen = numNodesGen + 1

def IDS(start):
    # Iterative Deepening tree search
    limit = 0
    input = copy.deepcopy(start)
    while( numNodesGen <= 100000 ):     
        result = DLS(input, limit)
        if result:
            return result
        limit = limit + 1

def DLS(start, limit):
    # Depth limited search
    return RecursiveDLS(GameBoardState(start), limit) 


# recusive depth limited search
def RecursiveDLS(node, limit):
    
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
    
#--------------------------------------------------------------
#
#   DFGS( start )
#       Perform a Depth First Graph Search starting at the 
#       'start' state. 
#       Returns goal node on success and None object on failure
#
#--------------------------------------------------------------
def DFGS( start ):
    visited = []                # List of visited nodes
    fringe = queue.Queue(0)     # FIFO for fringe

    fringe.put( GameBoardState(start) ) # Put the starting state in the fringe

    # limit DPGS to 100k nodes
    while ( numNodesGen <= 100000 ):
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
            global numPrintExpanded
            if(numPrintExpanded <= 5):
                print(node.array)
                numPrintExpanded = numPrintExpanded + 1
            #count num expanded nodes
            global numNodesExpanded
            numNodesExpanded = numNodesExpanded + 1

    # DFGS()

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

def add_node(node, priority):
    global minQueue
    minQueue.append((priority, node))
    minQueue = sorted(minQueue, key = itemgetter(0))
    #minQueue.reverse()

def remove_node():
    global minQueue
    #minQueue.reverse()
    hold = minQueue.pop(0)
    i, node = hold
        
    tieList = []
    tieList.append((node.tileNumber, node))
    
    # Create list to hold the tied nodes
    for x in minQueue:
        m,n = x
        if i == m:
           tieList.append((n.tileNumber, n))
        else:
            break
    
    # Figure out which node has the biggest tile number
    tieList = sorted(tieList, key=itemgetter(0))
    
    tilenum, newHold = tieList.pop()

#    minQueue.reverse()
    
    # If the current node is still the highest then return it
    if node == newHold:
        return node
    else:                           # else put it back in the minQueue
        minQueue.append((i, node))

    minQueue = sorted(minQueue, key = itemgetter(0))
    
    return newHold

def Astar(start_state):
    # Create first node to start
    global minQueue, numNodesExpanded, numPrintExpanded
    startNode = GameBoardState(start_state)
    startNode.manhattenDistance = manhattenDistance(startNode)
    add_node(startNode, (startNode.cost + startNode.manhattenDistance))
    
    while len(minQueue) != 0 and numNodesExpanded <= 100000:
        node = remove_node()            
        
        if node.array == final_state:
            return node
        for x in legalMoves(node):      # Put all children in fringe
            child = makeNode(x, node)   # create node for child
            node.children.append(child) # add child to parents child list
            child.parent = node  
            add_node(child, (child.cost + child.manhattenDistance))
      
        #if(numPrintExpanded <= 5):
        #    print(node.array)
        #    numPrintExpanded = numPrintExpanded + 1
        print(node.array)
        numNodesExpanded = numNodesExpanded + 1

    return None

    # hasVisited()




def legalMoves(state):
    # returns a list of the legal moves that can be done depending on the location of the '.'
    row, col = findSpace(state)
    return moves[(row,col)]

def generateChildNodes(node):
    # generates all of the child nodes for a given node
    children = []
    for x in legalMoves(node):
        child = makeNode(x, node)
        node.children.append(child)
        child.parent = node
        children.append(child)
        
    children = sortChildren(children)
    return children

def sortChildren(children):
    # sorts children by cost
    for x in children:
        for y in children:
            if y.tileNumber < x.tileNumber:
                hold = children[children.index(x)]
                children[children.index(x)] = children[children.index(y)]
                children[children.index(y)] = hold
    return children

def makeNode(move, state):
    # creates a node with the current state and modifies it to include the new state after the move is done
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
        newstate.cost = state.cost + 1
        newstate.manhattenDistance = manhattenDistance(newstate)

    return newstate

main()