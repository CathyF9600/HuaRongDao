import copy
from copy import deepcopy
from heapq import heappush, heappop # min-heap
import itertools # tie breaking for heap
import time
import argparse
import sys
import os
import glob
sys.setrecursionlimit(1000000)

#====================================================================================

char_goal = '1'
char_single = '2'

class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v') 
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, \
            self.coord_x, self.coord_y, self.orientation)
    
        

class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = 5

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()


    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = char_goal
                self.grid[piece.coord_y][piece.coord_x + 1] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = char_goal
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def getStringRep(self):
        res = ""
        for row in self.grid:
            for ele in row:
                res = res + ele
        return res

    def move(self, pieces, i, type, dir):
        """
        Move a piece from (srcY, srcX) to (desY, desX) (upper left)
        Return Board.grid
        Procedure: 
        1. find empty space on grid
        2. update piece information (in class Piece) (this function)
        """
        # self.parent = self # inherit the state that we're about to change
        # Update grid
        grid = self.grid
        piece = pieces[i]
        x = piece.coord_x
        y = piece.coord_y
        # If we're moving the 2x2 piece
        if type == "1":
            if dir == "right":
                grid[y][x] = "."
                grid[y+1][x] = "."
                grid[y][x+2] = "1"
                grid[y+1][x+2] = "1"
                piece.coord_x = x + 1
            elif dir == "left":
                grid[y][x+1] = "."
                grid[y+1][x+1] = "."
                grid[y][x-1] = "1"
                grid[y+1][x-1] = "1"
                piece.coord_x = x - 1
            elif dir == "down":
                grid[y][x] = "."
                grid[y][x+1] = "."
                grid[y+2][x] = "1"
                grid[y+2][x+1] = "1"
                piece.coord_y = y + 1
            elif dir == "up":
                grid[y+1][x] = "."
                grid[y+1][x+1] = "."
                grid[y-1][x] = "1"
                grid[y-1][x+1] = "1"
                piece.coord_y = y - 1
        # If we're moving the h piece
        elif type == "h":
            if dir == "left":
                grid[y][x-1] = "<"
                grid[y][x] = ">"
                grid[y][x+1] = "."
                piece.coord_x = x - 1
            elif dir == "right":
                grid[y][x] = "."
                grid[y][x+1] = "<"
                grid[y][x+2] = ">"
                piece.coord_x = x + 1
            elif dir == "down":
                grid[y][x] = "."
                grid[y][x+1] = "."
                grid[y+1][x] = "<"
                grid[y+1][x+1] = ">"
                piece.coord_y = y + 1
            elif dir == "up":
                grid[y][x] = "."
                grid[y][x+1] = "."
                grid[y-1][x] = "<"
                grid[y-1][x+1] = ">"
                piece.coord_y = y - 1 
        # If we're moving the 1x2 piece
        elif type == "v":
            if dir == "down":
                grid[y][x] = "."
                grid[y+1][x] = "^"
                grid[y+2][x] = "v"
                piece.coord_y = y + 1
            elif dir == "up":
                grid[y+1][x] = "."
                grid[y][x] = "v"
                grid[y-1][x] = "^"
                piece.coord_y = y - 1
            elif dir == "left":
                grid[y][x] = "."
                grid[y+1][x] = "."
                grid[y][x-1] = "^"
                grid[y+1][x-1] = "v"
                piece.coord_x = x - 1
            elif dir == "right":
                grid[y][x] = "."
                grid[y+1][x] = "."
                grid[y][x+1] = "^"
                grid[y+1][x+1] = "v"
                piece.coord_x = x + 1 
        # If we're moving the 1x1 piece
        elif type == "2":
            if dir == "down":
                grid[y][x] = "."
                grid[y+1][x] = "2"
                piece.coord_y = y + 1
            elif dir == "up":
                grid[y-1][x] = "2"
                grid[y][x] = "."
                piece.coord_y = y - 1
            elif dir == "left":
                grid[y][x] = "."
                grid[y][x-1] = "2"
                piece.coord_x = x - 1
            elif dir == "right":
                grid[y][x] = "."
                grid[y][x+1] = "2"
                piece.coord_x = x + 1
        return self

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='') # ends with a new line
            print()
    
    def find_empty(self):
        """
        Find the two empty spaces on the board, return their positions
        [(x1, y1), (x2, y2)]

        """
        res = []
        for i, line in enumerate(self.grid):
            for x, ch in enumerate(line):
                if ch == ".":
                    res.append((i,x))                    
        return res
    
    def manhattan(self):
        """
        Returns the vertical distance of the goal piece from goal position.
        It is in Board level since we don't need higher level information, 
        and we need to use it in order to create State object.
        """
        grid = self.grid
        # self.display()
        all_pieces = self.pieces
        for piece in all_pieces:
            if piece.is_goal:
                x = piece.coord_x
                y = piece.coord_y
                # print(x,y)
                # print(abs(1-x) + abs(3-y))
                return abs(1-x) + abs(3-y)



class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces. 
    State has a Board and some extra information that is relevant to the search: 
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, f, depth, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param f: The f value of current state.
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.f = f
        self.depth = depth
        self.parent = parent
        self.id = hash(board)  # The id for breaking ties.

    
    def trace_sol(self):
        f = open("./sol.txt", "a")
        if self.depth == 0:
            return True
        self = self.parent
        if self.trace_sol() == True:
            for i, line in enumerate(self.board.grid):
                for ch in line:
                    f.write(ch) # ends with a new line
                f.write("\n")
            f.write("\n")
            f.close()
            return True
            

class Solvers:
    def __init__(self, startState, endState=None):
        self.startState = startState
        self.endState = endState
        self.currentState = startState
        self.frontierList = []       # contains state
        self.exploredSet = set()       # for pruning
        self.step = 0

    def checkGoal(self) -> bool:
        """
        Check whether currentState is the goal """
        board = self.currentState.board
        grid = board.grid
        if (grid[3][1] == "1" and
            grid[4][1] == "1" and
            grid[3][2] == "1" and
            grid[4][2] == "1"):
            return True
        return False

    def add_successor(self, i, type ,dir, algo):
        """
        Deep copy the current state, move the newState, and add it to the frontier
        """
        if algo == "DFS":
            newBoard = deepcopy(self.currentState.board)
            newBoard = newBoard.move(newBoard.pieces, i, type, dir)
            new_str = newBoard.getStringRep()
            if new_str not in self.exploredSet:
                self.frontierList.append(State(newBoard, 0, self.currentState.depth + 1, self.currentState))
        elif algo == "A*":
            newBoard = deepcopy(self.currentState.board)
            newBoard = newBoard.move(newBoard.pieces, i, type, dir)
            new_str = newBoard.getStringRep()
            if new_str not in self.exploredSet:
                f = newBoard.manhattan() + self.currentState.depth
                id = hash(newBoard)
                heappush(self.frontierList, (f, id, State(newBoard, f, self.currentState.depth + 1, self.currentState)))


    
    def move_near(self, algo) -> None:
        """
        Search all possible ways to move the pieces, and move them,
        Add the state into the frontier.
        algo == "DFS" or "A*"
        """
        board = self.currentState.board
        grid = board.grid
        # self.currentState.board.display()
        # print("depth:", self.currentState.depth)
        e = board.find_empty()    #lower row first
        # print("e", e)
        e1y = e[0][0]
        e1x = e[0][1]
        e2y = e[1][0]
        e2x = e[1][1]
        pieces = board.pieces
        for i in range(len(pieces)):
            piece = pieces[i]
            px = piece.coord_x
            py = piece.coord_y
            if piece.orientation == "h" and grid[py][px+1] == ">":
                if (py == e1y and px == e1x + 1) or (py == e2y and px == e2x + 1):
                    self.add_successor(i, "h" ,"left", algo)
                if (py == e1y and px == e1x - 2) or (py == e2y and px == e2x - 2):
                    self.add_successor(i, "h" ,"right", algo)
                if(py == e1y - 1 and px == e1x and e2x == e1x + 1 and e2y == e1y):
                    self.add_successor(i, "h" ,"down", algo)
                if (py == e1y + 1 and px == e1x and e2x == e1x + 1 and e2y == e1y):
                    self.add_successor(i, "h" ,"up", algo)

            if piece.is_single and grid[py][px] == "2":
                if (py == e1y - 1 and px == e1x) or (py == e2y - 1 and px == e2x):
                    self.add_successor(i, "2" ,"down", algo)
                if (py == e1y + 1 and px == e1x) or (py == e2y + 1 and px == e2x):
                    self.add_successor(i, "2" ,"up", algo)
                if (py == e1y and px == e1x + 1) or (py == e2y and px == e2x + 1):
                    self.add_successor(i, "2" ,"left", algo)
                if (py == e1y and px == e1x - 1) or (py == e2y and px == e2x - 1):
                    self.add_successor(i, "2" ,"right", algo)
            
            if piece.orientation == "v" and grid[py+1][px] == "v":
                if (py == e1y - 2 and px == e1x) or (py == e2y - 2 and px == e2x):
                    self.add_successor(i, "v" ,"down", algo)
                if (py == e1y + 1 and px == e1x) or (py == e2y + 1 and px == e2x):
                    self.add_successor(i, "v" ,"up", algo)
                if (py == e1y and px == e1x + 1 and e2y == e1y + 1 and e2x == e1x):
                    self.add_successor(i, "v" ,"left", algo)
                if (py == e1y and px == e1x - 1 and e2y == e1y + 1 and e2x == e1x):
                    self.add_successor(i, "v" ,"right", algo)

            if piece.is_goal and grid[py][px+1] == "1" and grid[py+1][px] == "1" and grid[py+1][px+1] == "1":
                # if we can move right
                if (py == e1y and px == e1x - 2 and e2y == e1y + 1 and e2x == e1x): 
                    self.add_successor(i, "1" ,"right", algo)
                # if we can move left
                if (py == e1y and px == e1x + 1 and e2y == e1y + 1 and e2x == e1x):
                    self.add_successor(i, "1" ,"left", algo)
                # if we can move down
                if (py == e1y - 2 and px == e1x and e2x == e1x + 1 and e2y == e1y):
                    self.add_successor(i, "1" ,"down", algo)
                # if we can move up
                if (py == e1y + 1 and px == e1x and e2x == e1x + 1 and e2y == e1y):
                    self.add_successor(i, "1" ,"up", algo)



    def run_A_star(self):
        """
        A* algorithm with Manhattan heuristics to find the optimal solution.
        frontierList is a min heap containing:
        (Manhattan heuristic value, state object)

        Tie-breaking rule:
        […] store entries as 3-element list including (the priority, an entry count, and the task). 
        The entry count serves as a tie-breaker so that two tasks with the same priority are returned in 
        the order they were added. And since no two entry counts are the same, the tuple comparison 
        will never attempt to directly compare two tasks.

        The alternative to an entry point is a state id which is a hash value of the board.
        
        """
        # Update current state's heuristic value
        self.currentState.f = self.currentState.board.manhattan()
        # Push (f, state) into the frontier
        heappush(self.frontierList, (self.currentState.f, self.currentState.id, self.currentState))
        # Get string representation of the current state
        # start_str = self.currentState.board.getStringRep()
        i = 1
        while self.frontierList:
        # while self.currentState.depth < 2000:
            print("\nIteration %d\nCurr\n" %i)
            curState = self.frontierList[0][2]
            heappop(self.frontierList)   # Pop the lowest heuristic state out of the frontier
            
            # Get string representation of the current state
            cur_str = curState.board.getStringRep()
            # Update current state for later function calls
            self.currentState = curState
            # cur_id = hash(self.currentState.board)
            if cur_str not in self.exploredSet:
                # Add current state to the explored set
                self.exploredSet.add(cur_str)
                if self.checkGoal():            # Check if current state is the goal state
                    print("\nGoal found!")
                    print("depth:", self.currentState.depth)
                    self.currentState.board.display()
                    self.currentState.trace_sol()        
                    return
                
                filename = "./output/output" + str(i) + ".txt"
                file = open(filename,'w+')
                self.output_to_file(self.currentState, filename)
                
                # Find successors and add them to frontier
                self.move_near("A*")
                
                self.frontier_to_file(filename, "A*")
            
            i += 1


    def run_DFS(self):
        """
        While frontier is not empty,
        Pop a state out of frontier, add it to exploredSet
        Check whether the goal is reach, if not,
        Explore possibilities to move, and add them into the frontier.
        """
        self.frontierList.append(self.currentState)
        start_str = self.currentState.board.getStringRep()
        i = 1
        while len(self.frontierList) != 0:
        # while self.currentState.depth < 2000:
            # print("frontier",len(self.frontierList))
            curState = self.frontierList.pop(-1)   # Pop the last state out of the frontier
            cur_str = curState.board.getStringRep()
            self.currentState = curState    # Update current state for DFS
            cur_id = hash(self.currentState.board)
            if self.checkGoal():            # Check if current state is the goal state
                    print("\nGoal found!")
                    print("depth:", self.currentState.depth)
                    self.currentState.board.display()
                    
                    self.currentState.trace_sol()        
                    return
            elif cur_str not in self.exploredSet:
                filename = "./output/output" + str(i) + ".txt"
                file = open(filename,'w+')
                self.output_to_file(self.currentState, filename)

                # Add current state to the explored set
            
                # Find successors and add them to frontier
                self.move_near("DFS")

                self.exploredSet.add(curState.board.getStringRep())

                self.frontier_to_file(filename, "DFS")
            
            i += 1

                
        print("NOT found!")

    def frontier_to_file(self, filename, algo):
        f = open(filename, "a")
        f.write("\nBegin frontier\n")
        j = 0
        if algo == "DFS":
            for states in self.frontierList:    
                f.write("%d \n" %(j))
                for i, line in enumerate(states.board.grid):
                    for ch in line:
                        f.write(ch) # ends with a new line
                    f.write("\n")
                j += 1
                f.write("\n")
                if states.board.getStringRep() in self.exploredSet:
                    f.write("NOOOOOOOOO\n")
            f.write("frontier done")
            f.close()
        else:
            for heu, _, states in self.frontierList:    
                f.write("%d: %d\n\n" %(j,heu))
                for i, line in enumerate(states.board.grid):
                    for ch in line:
                        f.write(ch) # ends with a new line
                    f.write("\n")
                j += 1
                f.write("\n")
                if states.board.getStringRep() in self.exploredSet:
                    f.write("NOOOOOOOOO\n")
            f.write("frontier done")
            f.close()
    
    def output_to_file(self, state, filename):
        """
        Write state to file
        """
        f = open(filename, "a")
        f.write("\n\nExploring:\n")
        for i, line in enumerate(state.board.grid):
            for ch in line:
                f.write(ch) # ends with a new line
            f.write("\n")
        f.close()
    
    
        f.close()
        

def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    g_found = False

    for line in puzzle_file:

        for x, ch in enumerate(line):
            if ch == '^': # found vertical piece
                pieces.append(Piece(False, False, x, line_index, 'v'))
            elif ch == '<': # found horizontal piece
                pieces.append(Piece(False, False, x, line_index, 'h'))
            elif ch == char_single:
                pieces.append(Piece(False, True, x, line_index, None))
            elif ch == char_goal:
                if g_found == False:
                    pieces.append(Piece(True, False, x, line_index, None))
                    g_found = True

        line_index += 1

    puzzle_file.close()

    board = Board(pieces)
    
    return board



if __name__ == "__main__":
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()
    '''
    
    # read the board from the file
    board = read_from_file("./tests/t1.txt")
    # board.display()
    # board.find_empty()
    # for piece in board.pieces:
        # print(piece)
    # print(board.grid)
    state = State(board, 0, 0, None)
    solvers = Solvers(state)

    with open("./sol.txt", "r+") as f:
        f.truncate(0)

    start = time.time()
    # print(solvers.currentState.board.manhattan())
    # solvers.run_DFS()
    solvers.run_A_star()
    end = time.time()
    print("Time:", end - start)
    print("\n")
    

    




