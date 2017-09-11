import numpy as np

# dictionary for nodes visited

    
#[0 1 2]
#[3 4 5]
#[6 7 8]

moves = {}
moves[0] = ['DOWN', 'RIGHT']
moves[1] = ['LEFT', 'DOWN','RIGHT']
moves[2] = ['LEFT', 'DOWN']
moves[3] = ['UP', 'RIGHT', 'DOWN']
moves[4] = ['LEFT', 'UP', 'RIGHT', 'DOWN']
moves[5] = ['LEFT', 'UP', 'DOWN']
moves[6] = ['UP', 'RIGHT']
moves[7] = ['LEFT', 'UP', 'DOWN']
moves[8] = ['LEFT', 'UP']

a = [[1,2,3],[4,5,6],[7,8, '.']]
b = [[], [], []]
c = [[], [], []]
init_states=[a,b,c]
final_state = [[1,2,3],[4,5,6],[7,8,'.']]
init_state=a

numNodes = 0

def findSpace(state):
    i = 0
    for a in final_state:
        j = 0
        for b in a:
            if b == '.':
                return i,j
            j = j + 1
        i = i + 1
            

print(findSpace(final_state))

class GameBoardState(object):
    def __init__(self, state):
        self.array = state
        self.visited = None  # might not use this
        self.parent = None
        self.children = []
        self.moves = moves

def IDS(limit):
    # Iterative Deepening tree search
    limit = 0
    while( numNodes != 100000 ):
        result = DLS(limit)
        if result:
            return result

def DLS(limit):
    return RecursiveDLS(GameBoardState(init_state), limit) 

def RecursiveDLS(state,limit):
    if state == final_state:
        return state
    elif limit == 0:
        return None
    else:
        failure = False
        for x in legalMoves(state):
            child = makeNode(x, state)
            state.children.append(child)
            child.parent = state
            result = RecursiveDLS(child, limit - 1)
            
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
    return moves[state.index('.')]

def makeNode(move, state):
    if move == 'UP':
        newstate = GameBoardState(state)
        holdi, holdj = findSpace(newstate.array)
        holdstate = newstate.array[holdi-1][holdj]
        newstate.array[holdi-1][holdj] = '.'
        newstate.array[holdi][holdj] = holdstate
        
    elif move == 'DOWN':
        newstate = GameBoardState(state)
        holdi, holdj = findSpace(newstate.array)
        holdstate = newstate.array[holdi+1][holdj]
        newstate.array[holdi+1][holdj] = '.'
        newstate.array[holdi][holdj] = holdstate

    elif move == 'LEFT':
        newstate = GameBoardState(state)
        holdi, holdj = findSpace(newstate.array)
        holdstate = newstate.array[holdi][holdj-1]
        newstate.array[holdi][holdj-1] = '.'
        newstate.array[holdi][holdj] = holdstate
    else:
        newstate = GameBoardState(state)
        holdi, holdj = findSpace(newstate.array)
        holdstate = newstate.array[holdi][holdj+1]
        newstate.array[holdi][holdj+1] = '.'
        newstate.array[holdi][holdj] = holdstate
    
    numNodes = numNodes + 1

    return newstate