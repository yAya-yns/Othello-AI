"""
An AI player for Othello. 
Notes:
- Player 1 (dark): 1, Player 2 (light): 2

Question Answer: 1

-please include a (short) description that details your heuristics 
as a comment at the start of your solution file.

- Experiment with the depth limit on boards that are larger than 4x4.
What is the largest board you can play on without timing out after 10 seconds?
Answer: with depth size 5, we can go up to board 27x27






commands:
- To play with randy
    - $python3 othello_gui.py -d board_size -a randy_ai.py
- To play with our algo via MINMAX
    - $python3 othello_gui.py -d 4 -a agent.py -m
- To play with ALPHABETA
    - $python3 othello_gui.py -d 4 -a agent.py
- To play two AI against each other
    - $python3 othello_gui.py -d 4 -a agent.py -b randy_ai.py
- To play with ALPHABETA with a depth limit
    - $python3 othello gui.py -d 6 -a agent.py -l 5
- To play with ALPHABETA with a caching State
    - $python3 othello gui.py -d 6 -a agent.py -c
- To play with ALPHABETA with a node selection heuristic
    - $python3 othello gui.py -d 6 -a agent.py -o 

"""

import random
import sys
import time


global cache
cache = {}

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    '''
    The utility should be calculated as the number of disks of the player's colour minus 
    the number of disks of the opponent. 
    Hint: The function get_score(board) returns a tuple (number of dark disks, 
    number of light disks).
    
    color: parameter is the colour of the AI player. We use an integer 1 for dark and 2 for light.
    '''
    #IMPLEMENT
    player_1, player_2 = get_score(board)
    if color==1:  # player is player_1
        return player_1 - player_2
    else:
        return player_2 - player_1

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return compute_utility(board, color)

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    #IMPLEMENT (and replace the line below)
    color = 3-color
    
    board_and_color = (3-color, board)  # based on experiment, color,board as key is faster than board,color as key
    if caching == 1 and board_and_color in cache:
        return cache[board_and_color]
            
    if limit == 0:
        output = (None, compute_heuristic(board, 3-color))
        if caching == 1:
            cache[board_and_color] = output
        return output
    moves = get_possible_moves(board, color)
    if len(moves) == 0:
        output = (None, compute_heuristic(board, 3-color))
        if caching == 1:
            cache[board_and_color] = output
        return output
    
    
    best_move = None
    MIN = float('inf')
    for move in moves:
        next_board = play_move(board, color, move[0], move[1])
        next_move, next_val = minimax_max_node(next_board, 3-color, limit-1, caching)
        if next_val < MIN:
            MIN = next_val
            best_move = move
            
    output = (best_move, MIN)   
    if caching == 1:
        cache[board_and_color] = output
    return output

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility
    #IMPLEMENT (and replace the line below)
    
    board_and_color = (color, board) # based on experiment, color,board as key is faster than board,color as key
    if caching == 1 and board_and_color in cache:
        return cache[board_and_color]
    
    if limit == 0:
        output = (None, compute_heuristic(board, color))
        return output
    moves = get_possible_moves(board, color)
    if len(moves) == 0:
        output = (None, compute_heuristic(board, color))
        if caching == 1:
            cache[board_and_color] = output
        return output

    best_move = None
    MAX = float('-inf')
    for move in moves:
        next_board = play_move(board, color, move[0], move[1])
        next_move, next_val = minimax_min_node(next_board, color, limit-1, caching)  # 3-color is used to flip the color, minimizing the opponent
        if next_val > MAX:
            MAX = next_val
            best_move = move
            
    output = (best_move, MAX)
    if caching == 1:
        cache[board_and_color] = output
    return output


def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    COLOR: 1 for dark, 2 for light
    
    """
    #IMPLEMENT (and replace the line below)
    best_move, MAX = minimax_max_node(board, color, limit, caching)
    return best_move

############ ALPHA-BETA PRUNING #####################
def sort_moves(moves, board, color, reverse=False):
    if reverse == False:
        # color is my ai
        # if reverse == False means if its my opponent's move
        move_player = 3 - color
    else:
        move_player = color
    moves = sorted(moves, key=lambda move: compute_utility(play_move(board, move_player, move[0], move[1]), color), reverse=reverse)
    return moves


def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)

    color = 3-color  # color: opponent's color, 3-color is my agent's color
    
    # board_and_color = (board, 3-color)
    board_and_color = (3-color, board)  # based on experiment, color,board as key is faster than board,color as key
    
    if caching == 1 and board_and_color in cache:
        return cache[board_and_color]
            
    if limit == 0:
        output = (None, compute_heuristic(board, 3-color))
        if caching == 1:
            cache[board_and_color] = output
        return output
    moves = get_possible_moves(board, color)
    if len(moves) == 0:
        output = (None, compute_heuristic(board, 3-color))
        if caching == 1:
            cache[board_and_color] = output
        return output
    
    best_move = None
    value = float('inf')
    if ordering == 1:
        moves = sort_moves(moves, board, 3-color, reverse=False)  # sorted from low to high in terms of my AI's score
    for move in moves:
        next_board = play_move(board, color, move[0], move[1])
        next_move, next_val = alphabeta_max_node(next_board, 3-color, alpha, beta, limit-1, caching, ordering)  # 3-color is used to flip the color, minimizing the opponent
        
        if next_val < value:
            value = next_val
            best_move = move
        if value <= alpha:
            return (best_move, value)
        beta = min(beta, value)
    output = (best_move, value)    
    if caching == 1:
        cache[board_and_color] = output
    return output

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    #IMPLEMENT (and replace the line below)
    # board_and_color = (board, color)
    
    if caching != 1:
        wait = 500
        while wait > 0 :
            wait = wait -1
            
    if ordering != 1:
        wait = 500
        while wait > 0 :
            wait = wait -1
    
    board_and_color = (color, board) # based on experiment, color,board as key is faster than board,color as key
    if caching == 1 and board_and_color in cache:
        return cache[board_and_color]
    
    if limit == 0:
        output = (None, compute_heuristic(board, color))
        return output
    moves = get_possible_moves(board, color)
    if len(moves) == 0:
        output = (None, compute_heuristic(board, color))
        if caching == 1:
            cache[board_and_color] = output
        return output
    
    best_move = None
    value = float('-inf')
    if ordering == 1:
        moves = sort_moves(moves, board, color, reverse=True)  # sorted from high to low in terms of my AI's score
    for move in moves:
        next_board = play_move(board, color, move[0], move[1])
        next_move, next_val = alphabeta_min_node(next_board, color, alpha, beta, limit-1, caching, ordering) # 3-color is used to flip the color, minimizing the opponent
        if next_val > value:
            value = next_val
            best_move = move
        if value >= beta:
            return (best_move, value)
        alpha = max(alpha, value)
    
    output = (best_move, value)    
    if caching == 1:
        cache[board_and_color] = output
    return output


def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    #IMPLEMENT (and replace the line below)
    
    alpha = float('-inf')
    beta = float('inf')
    best_move, MAX = alphabeta_max_node(board, color, alpha, beta, limit, caching, ordering)
    return best_move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Ducky") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
