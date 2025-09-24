# hand_of_the_king.py
# Play "A Game of Thrones: Hand of the King" in Python!
#
# Hand of the King (HOTK) is a game in which players take turns moving a purple card
# in a single direction around a grid of colored cards in order to collect cards of a
# chosen color. Players gain control of a color once they acquire an equal or greater
# number of cards compared to their opponents. The player in control of the most colors
# (there are seven colors total) when no more moves are available on the board is 
# declared the winner.

import argparse
from copy import deepcopy
import os
import pdb
import random
import time
import utils

ROOT = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Play a Game of Thrones: Hand of the King!")
parser.add_argument('--player1', metavar='p1', type=str, help="either 'human' (default) or the name of an AI player file", default='human')
parser.add_argument('--player2', metavar='p2', type=str, help="either 'human' (default) or the name of an AI player file", default='human')
parser.add_argument('-b', '--board', type=str, help="file containing starting board setup (for repeatability)", default=None)
parser.add_argument('-d', '--delay', type=float, help="time (in seconds) to wait between moves (default=1)", default=1)
parser.add_argument('-n', '--num_colors', type=int, help="number of color sets in the game (default=8)", default=8)
parser.add_argument('-s', '--seed', metavar='n', type=int, help="seed for random number generator", default=None)

def main(args):
    print("Let's play a Game of Thrones: Hand of the King!")

    # Initialize the game
    random.seed(args.seed) # set seed for random number generator (for repeatability of shuffled cards, if desired)
    board, rows, cols = utils.load_cards(args.board) if args.board else utils.shuffle_cards(args.num_colors) # load or shuffle cards to make a board array
    num_colors = max(board)
    x0 =  board.index(1) # starting position of the 1-card (which will be needed as a workaround for actually swapping graphics objects)
    gui = utils.make_gui(board, rows, cols)
    cards = [[0] * (num_colors - 1) for i in range(2)] # initialize card collection for each player
    banners = [[0] * (num_colors - 1) for i in range(2)] # initialize banner collection for each player

    # Load AI player(s) if needed
    players = [args.player1, args.player2]
    ai = [None, None]
    for i in range(2):
        if players[i] != "human":
            ai[i] = utils.load_player(players[i])

    # Play the game
    if any(item is not None for item in ai): # if any player is AI, then wait for user to manually start game
        input("Press <Enter> to start game ")
    turn = 0 # toggle between 0 and 1 for player 1 and 2, respectively
    gameover = False
    while not gameover and gui.isOpen():
        # What are the available moves?
        valid_moves = utils.get_valid_moves(board, rows, cols)
        
        # The game ends when there are no more valid moves
        if len(valid_moves) == 0:
            print(f'There are no more remaining moves. Game over.')
            gameover = True
            break

        # Query player to select a card
        if players[turn] == 'human':
            utils.status(gui, f'Player {turn + 1}, choose a move')
            which_card = utils.ask_human(gui)
            if which_card == -1:
                break

        else: # the player is an AI agent
            utils.status(gui, f'Player {turn + 1} ({players[turn]}) is thinking...')
            time.sleep(args.delay)
            # which_card = ai[turn].choice(board.copy(), rows, cols, turn, cards.copy(), banners.copy())
            which_card = ai[turn].choice(deepcopy(board), rows, cols, turn, deepcopy(cards), deepcopy(banners))

        # Make the move if it is valid
        if which_card in valid_moves:
            # print(f"choosing card {which_card}")
            # print(*board)
            # print(*valid_moves)
            color = board[which_card]  # save the color being captured for later
            utils.make_move(gui, board, x0, which_card, cards[turn])
            utils.update_banners(turn, color, cards, banners)
            
            # Switch turns
            turn = abs(turn - 1)
            
            # Stuff for debugging
            print("card collections")
            print(*cards[0])
            print(*cards[1])
            print("banners")
            print(*banners[0])
            print(*banners[1])
            print(f'score: {sum(banners[0])}-{sum(banners[1])}\n')
            
        # Check for keyboard input
        key = gui.checkKey()
        if key:
            if key in ["Escape", "Ctrl+e"]: # exit game
                break
            elif key == 'd': # debug
                pdb.set_trace()

    # Determine the winner and display the result
    if gameover:
        utils.get_winner(gui, players, banners)
        time.sleep(args.delay)

if __name__ == "__main__":
    main(parser.parse_args())