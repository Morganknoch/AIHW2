# dictionary for nodes visited
import copy
#[0 1 2]
#[3 4 5]
#[6 7 8]

moves = {}
moves[(0, 0)] = ['DOWN', 'RIGHT']
moves[(0,1)] = ['LEFT', 'DOWN','RIGHT']
moves[(0,2)] = ['LEFT', 'DOWN']
moves[(1,0)] = ['UP', 'RIGHT', 'DOWN']
moves[(1,1)] = ['LEFT', 'UP', 'RIGHT', 'DOWN']
moves[(1,2)] = ['LEFT', 'UP', 'DOWN']
moves[(2,0)] = ['UP', 'RIGHT']
moves[(2,1)] = ['LEFT', 'UP', 'RIGHT']
moves[(2,2)] = ['LEFT', 'UP']

a = [['.', 1, 3],[4, 2, 5],[7, 8, 6]]
#a = [[1,2,3],[4,5,6],[7, '.', 8]]
b = [['.', 5, 2], [1, 8, 3], [4, 7, 6]]
c = [[8, 6, 7], [2, 5, 4], [3, '.', 1]]
init_states=[a,b,c]
final_state = [[1,2,3],[4,5,6],[7,8,'.']]
test = [[1,2,3],[4,5,6],[7,8,'.']]
init_state=a

numNodesGen = 0
numNodesExpanded = 0

def main():
    global numNodesGen, numNodesExpanded
    #x = IDS(a)
    #numNodesGen = 0
    #numNodesExpanded = 0
    #x = IDS(b)
    #numNodesGen = 0
    #numNodesExpanded = 0
    x = IDS(c)
    numNodesGen = 0
    numNodesExpanded = 0

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

        global numNodesGen 
        numNodesGen = numNodesGen + 1

def IDS(start):
    # Iterative Deepening tree search
    limit = 0
    input = copy.deepcopy(start)
    while( numNodesGen <= 1000000 ):     
        result = DLS(input, limit)
        if result:
            return result
        limit = limit + 1

def DLS(start, limit):
    # Depth limited search
    return RecursiveDLS(GameBoardState(start), limit) 

def RecursiveDLS(node,limit):
    # recusive depth limited search
    if node.array == final_state:
        return node
    elif limit == 0:
        return None
    else:
        failure = False
        children = generateChildNodes(node)
        for child in children:
            result = RecursiveDLS(child, limit - 1)
            global numNodesExpanded
            numNodesExpanded = numNodesExpanded + 1
            if not result:
                failure = True
            elif result:
                return result
        if failure:
            return None
    

def DFGS():
    pass

def Astar():
    pass

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
            if y.cost < x.cost:
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
        newstate.cost = holdstate         
    elif move == 'DOWN':
        
        holdi, holdj = findSpace(newstate)
        holdstate = newstate.array[holdi+1][holdj]
        newstate.array[holdi+1][holdj] = '.'
        newstate.array[holdi][holdj] = holdstate
        newstate.cost = holdstate
    elif move == 'LEFT':
        
        holdi, holdj = findSpace(newstate)
        holdstate = newstate.array[holdi][holdj-1]
        newstate.array[holdi][holdj-1] = '.'
        newstate.array[holdi][holdj] = holdstate
        newstate.cost = holdstate
    else:
        
        holdi, holdj = findSpace(newstate)
        holdstate = newstate.array[holdi][holdj+1]
        newstate.array[holdi][holdj+1] = '.'
        newstate.array[holdi][holdj] = holdstate
        newstate.cost = holdstate
    
    

    return newstate

main()