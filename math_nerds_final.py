# MOB's AI player
# incorporating minimax with alpha-beta pruning

# time limit is 5 seconds so will have to search to a certain depth to find
# optimal move

import os
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(ROOT)
import utils
import math
import copy
import time

def choice(board, rows, cols, turn, cards=[], banners=[]):
    """Search for the best move based on the current game state.
     
    Parameters
    ----------
    board : list of ints
        A flattened list of color indices for each card in the game.
    rows : int
        Number of rows on the board.
    cols : int
        Number of columns on the board.
    turn : int {0, 1}
        An integer that shows which player is the AI.
    cards : list of lists of ints, optional (default=[])
        How many cards does each player own? The syntax cards[i][j] = k
        indicates that the ith player owns k cards of the jth color set.
    banners : list of lists of ints, optional (default=[])
        Which banners does each player own? The syntax banners[i][j] = 1
        indicates that the ith player owns the banner of the jth color set.

    Output
    ------
    which_card : int
        The linear index of the card to choose.
    """

    # grab valid moves from utils function get_valid_moves(board, rows, cols):
    moves = utils.get_valid_moves(board, rows, cols)
    # send over everything, inlcuding list of valid moves to minimax
    initial_game = [board, rows, cols, turn, cards, banners]
    moves.sort(key=lambda m: -score_move(initial_game, m))
    # send over everything, inlcuding list of valid moves to minimax
    next_move = minimax(initial_game, moves)

    return next_move
    

# board, rows, cols, turn, cards, banners, moves
def minimax(initial_game, moves):
    # added time limit 
    time_limit = 3
    start_time = time.time()
    # initialize the "best" move and its utility right away    
    best_action = None
    best_utility = -math.inf

    # Need a value that gets sent aroudn to limit depth to minimize running time
    count_zeros = 0
    for i in range(len(initial_game[0])):
        if initial_game[0][i] == 0:
            count_zeros += 1

    # change depths
    if count_zeros < 8:
        depth = 4
    elif count_zeros < 18:
        depth = 7
    else:
        depth = 12
    
    # initialize alpha and beta
    alpha = -math.inf
    beta = math.inf

    # make copy of initial game so it doesnt get messed up
    beginning_game = copy.deepcopy(initial_game)

    # loop over each valid move -- moves will be a list of ints that return valid moves on the board
    for move in moves:
        new_game = simulate_move(copy.deepcopy(beginning_game), move, beginning_game[3]) # simulate the new move
        if time.time() - start_time > time_limit:
            break
        # check if the new board is terminal, if so check who wins
        if is_terminal_state(new_game):
            # sum(game[board][turn]) --- your sum minus opponent sum
            score = sum(new_game[5][new_game[3]]) - sum(new_game[5][abs(new_game[3]-1)])
            if score > 0:
                utility = 999 # take a move if you would instantly win the game
            else:
                utility = score

        else:
            utility = minvalue(new_game, alpha, beta, depth - 1, start_time)
        
        if utility > best_utility:
            best_utility = utility
            best_action = move
    
    # resolves some errors
    if best_action == None:
        temp = utils.get_valid_moves(initial_game[0], initial_game[1], initial_game[2])
        best_action = temp[0]
    return best_action

def minvalue(game, alpha, beta, max_search_depth, start_time):
    '''Returns the minimum utility available from a given state in the tree.'''
    '''''
    if is_terminal_state(board, rows, cols, turn, cards, banners, moves): # or at desired depth and give it a value
        return 12# need to return a value here
    '''
    ''''
    Notes for how was to score:
    Terminal state:
    have an if statment to return values- my thought process is to check if the moves list is empty
    then call a terminal state cost function that scores the amount of banners each person has.
    so if the other person wins give it a score of something low and then if you win give it a higher score

    Value of taking certain cards:
    We should value taking as mnay cards and what "number they are" such as have a higher value for a 2 than an 8

    
    '''
    time_limit = 3
    game = copy.deepcopy(game)
    moves = utils.get_valid_moves(game[0], game[1], game[2])
    # refernce chatgpt at bottom
    moves.sort(key=lambda m: -score_move(game, m))
    if len(moves) == 0:
        return evaluate(game)

    # now check if the desired depth of search is found -- decrement this for every call
    if max_search_depth == 0:
        return evaluate(game)
    
    u = math.inf
    for move in moves:
        if time.time() - start_time > time_limit:
            break
        new_game = simulate_move(game, move, abs(game[3]-1))
        u = min(u, maxvalue(new_game, alpha, beta, max_search_depth - 1, start_time))
        beta = min(beta, u)
        if alpha >= beta:
            break

    return u

def maxvalue(game, alpha, beta, max_search_depth, start_time):
    '''Returns the minimum utility available from a given state in the tree.'''
    time_limit = 3
    game = copy.deepcopy(game)
    moves = utils.get_valid_moves(game[0], game[1], game[2])
    moves.sort(key=lambda m: -score_move(game, m))

    if len(moves) == 0:
        return evaluate(game)
    
    # now check if the desired depth of search is found -- decrement this for every call
    if max_search_depth == 0:
        return evaluate(game)
    
    u = -math.inf
    for move in moves:
        if time.time() - start_time > time_limit:
            break
        new_game = simulate_move(game, move, game[3])
        u = max(u, minvalue(new_game, alpha, beta, max_search_depth - 1, start_time))
        alpha = max(alpha, u)
        if alpha >= beta:
            break

    return u

# checks if a given board is terminal
def is_terminal_state(game):
    return utils.get_valid_moves(game[0], game[1], game[2]) == []

# board, rows, cols, turn, cards, banners
# simulate a given move on the current board
def simulate_move(game, move, player):
    cols = game[2]
    # new copy of game
    new_game = copy.deepcopy(game)

    # make copy of board
    new_board = new_game[0]
    current_location = None

    # find the starting location, where the 1 card is
    for i in range(len(new_board)):
        if new_board[i] == 1:
            current_location = i
            break

    # find the color card in the spot we are trying to move to
    color_in_new_spot = new_board[move]

    # find out if new move is above, below, left, or right of current location
    above = below = left = right = False
    if (move < current_location and move % 6 == current_location % 6):
        above = True
    elif (move < current_location and move % 6 != current_location % 6):
        left = True
    elif (move > current_location and move % 6 != current_location % 6):
        right = True
    elif (move > current_location and move % 6 == current_location % 6):
        below = True

    if above:
        for i in range(move, current_location, cols):
            if new_board[i] == color_in_new_spot:
                new_board[i] = 0
                new_game[4][player][color_in_new_spot - 2] += 1 # game[cards][turn][color]

        new_board[current_location] = 0
        new_board[move] = 1
        utils.update_banners(player, color_in_new_spot, new_game[4], new_game[5])

    if left:
        for i in range(move, current_location):
            if new_board[i] == color_in_new_spot:
                new_board[i] = 0
                new_game[4][player][color_in_new_spot - 2] += 1 # game[cards][turn][color]
                
        new_board[current_location] = 0
        new_board[move] = 1
        utils.update_banners(player, color_in_new_spot, new_game[4], new_game[5])

    if right:
        for i in range(move, current_location, -1):
            if new_board[i] == color_in_new_spot:
                new_board[i] = 0
                new_game[4][player][color_in_new_spot - 2] += 1 # game[cards][turn][color]
                
        new_board[current_location] = 0
        new_board[move] = 1
        utils.update_banners(player, color_in_new_spot, new_game[4], new_game[5])

    if below:
        for i in range(move, current_location, 0-cols):
            if new_board[i] == color_in_new_spot:
                new_board[i] = 0
                new_game[4][player][color_in_new_spot - 2] += 1 # game[cards][turn][color]
                
        new_board[current_location] = 0
        new_board[move] = 1
        utils.update_banners(player, color_in_new_spot, new_game[4], new_game[5])
    
    new_game[0] = new_board
    return new_game

def evaluate(game):
    # ideas for total
    # sum of your banners - sum of opponent banners
    # + number of banners you could still get?
    # - number of banners you cant still get?
    # something with total number of cards you own?
    # + your cards - their cards, but maybe only for colors that arent guaranteed
    # give more importance to lower numbers because they are easier to get
    total = 0

    your_banners = sum(game[5][game[3]])
    opponent_banners = sum(game[5][abs(game[3]-1)])
    
    total += (your_banners * 2)
    total -= (opponent_banners * 2)

    # check which banners are still obtainable based on number of remaining cards, enemy cards, and your cards
    # a banner is no longer obtainable if: someone owns at least ceil( (card num + 1)/2 )
    # aka own MORE than half
    guaranteed_wins = 0
    guaranteed_losses = 0
    guaranteed_banners = [0,0,0,0,0,0,0]
    for i in range(len(game[4][0])): # loop over length of cards
        if (game[4][game[3]][i]) >= math.ceil((i+3)/2): # if your card pile owns more than half of that type, += 1
            guaranteed_wins += 1
            guaranteed_banners[i] = 1
    for i in range(len(game[4][0])):
        if (game[4][abs(game[3]-1)][i]) >= math.ceil((i+3)/2): # if opponent card pile owns more than half of that type, -= 1
            guaranteed_losses += 1
            guaranteed_banners[i] = 1

    total += (7 - sum(guaranteed_banners)) # banners you could still get

    # what if we weight guaranteed banners more
    # 4 doesnt seem bad, no idea if there's a better value
    total += (guaranteed_wins * 4)
    total -= (guaranteed_losses * 4)

    # taking the card total and adding weights to each differnt kind of cards
    # and adding another part that goes over gauruanteed baneers that values
    card_totals = [2, 3, 4, 5, 6, 7, 8]
    for i in range(7):
        # get the weight calculation
        weight = 8 / card_totals[i]
        total += game[4][game[3]][i] * weight
        total -= game[4][abs(game[3]-1)][i] * weight
        # check if banner at that index is not gauruanteed
        if guaranteed_banners[i] == 0:
            difference = game[4][game[3]][i] - game[4][abs(game[3]-1)][i]
            total += difference

    # make an endgmae banner grab, try to gai as many banners at end
    cards_left = 36
    for spot in game[0]:
        if spot == 0:
            cards_left -= 1
    # this weighs having more banners way more
    if cards_left < 15:
        total += (your_banners - opponent_banners) * 8
            # this really heavily weighs winning, need 4 or more banners to win
        #if guaranteed_wins >= 4:
            #total += guaranteed_wins * 10


    return total


# new function to score moves, so this makes the funcrtion call better moves first
# https://chatgpt.com/share/6806dc0c-2a74-8004-8912-83181efe5e12 
def score_move(game, move):
    score = 0
    # copy game]
    temp_game = copy.deepcopy(game)
    # get the new state with the next move
    temp_state = simulate_move(temp_game, move, game[3])
    # return the difference between the cards in the new states,
    #  maybe add banners as well
    temp_sum = sum(temp_state[4][temp_state[3]])
    og_sum = sum(game[4][game[3]])
    differnce = temp_sum - og_sum

    # get banners differnce
    temp_banner_total = sum(temp_state[5][temp_state[3]])
    og_banner_total = sum(game[5][game[3]])
    banner_differnce = temp_banner_total - og_banner_total
    
    score = differnce * 2
    score += banner_differnce * 8
    
    return score


if __name__ == "__main__":
    board, rows, cols = utils.shuffle_cards(5)
    player_name = os.path.basename(__file__).split('.')[0].title()
    print("\nBoard:")
    utils.print_board(board, rows, cols)
    print('\nPossible moves:', end=" ")
    print(*sorted(utils.get_valid_moves(board, rows, cols)))
    print(f'\n{player_name}: "My next choice would be {choice(board, rows, cols, 0)}"')