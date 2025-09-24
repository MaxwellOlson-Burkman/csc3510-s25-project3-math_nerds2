# hand_of_the_king_sim.py
# Simulation-only version of "Hand of the King"

import argparse
from copy import deepcopy
import random
import utils
from players import joel

parser = argparse.ArgumentParser(description="Simulate Hand of the King without GUI or human input")
parser.add_argument('--player1', type=str, help="Name of AI player 1", required=True)
parser.add_argument('--player2', type=str, help="Name of AI player 2", required=True)
parser.add_argument('--board', type=str, help="Starting board setup file", default=None)
parser.add_argument('--num_colors', type=int, help="Number of color sets (default=8)", default=8)
parser.add_argument('--seed', type=int, help="Random seed", default=None)
parser.add_argument('--delay', type=float, help="Optional delay between moves (default=0)", default=0)

player1_wins = 0
player1_win_points = 0
player1_losses = 0
player1_losses_points = 0
player1_ties = 0

player2_wins = 0
player2_win_points = 0
player2_losses = 0
player2_losses_points = 0
player2_ties = 0


def main(args):
    # global time
    global player1_wins
    global player1_win_points
    global player1_losses
    global player1_losses_points
    global player1_ties

    global player2_wins
    global player2_win_points
    global player2_losses
    global player2_losses_points
    global player2_ties


    # print("Simulating Hand of the King...")

    random.seed(args.seed)

    # Load or create the board
    board, rows, cols = (
        utils.load_cards(args.board) if args.board else utils.shuffle_cards(args.num_colors)
    )
    num_colors = max(board)
    x0 = board.index(1)  # Starting position of the 1-card

    cards = [[0] * (num_colors - 1) for _ in range(2)]  # Player card collections
    banners = [[0] * (num_colors - 1) for _ in range(2)]  # Player banner collections

    # Load AI players
    ai = [utils.load_player(args.player1), utils.load_player(args.player2)]

    turn = 0
    while True:
        valid_moves = utils.get_valid_moves(board, rows, cols)
        if not valid_moves:
            # print("No more moves. Game over.")
            break

        move = ai[turn].choice(deepcopy(board), rows, cols, turn, deepcopy(cards), deepcopy(banners))

        if move not in valid_moves:
            # print(f"Invalid move attempted by player {turn + 1}. Skipping turn.")
            turn = abs(turn - 1)
            continue

        color = board[move]
        # utils.make_move(None, board, x0, move, cards[turn])
        new_game = joel.simulate_move([deepcopy(board), rows, cols, turn, deepcopy(cards), deepcopy(banners)], move, turn)
        board = deepcopy(new_game[0])
        cards = deepcopy(new_game[4])
        utils.update_banners(turn, color, cards, banners)

        # Print status
        # print(f"Player {turn + 1} played card {move} (color {color})")
        # print(f"Cards: P1={cards[0]} P2={cards[1]}")
        # print(f"Banners: P1={banners[0]} P2={banners[1]}")
        # print(f"Score: P1={sum(banners[0])} - P2={sum(banners[1])}\n")

        turn = abs(turn - 1)

    # Final winner
    # winner = utils.get_winner(None, [args.player1, args.player2], banners, print_result=True)
    # Process player names (this is because "human def human" looks weirder than "Player 1 def Player 2")
    players = [args.player1, args.player2]
    player1 = "Player 1" if players[0] == "human" or players[0] == players[1] else players[0]
    player2 = "Player 2" if players[1] == "human" or players[0] == players[1] else players[1]

    # Compute the score for each player
    score1 = sum(banners[0])
    score2 = sum(banners[1])

    # The player with the higher score wins
    if score1 > score2:
        # status(gui, f"{player1} wins!")
        print(f'{player1} def {player2} {score1}-{score2}')
        player1_wins += 1
        player1_win_points += score1
        
        player2_losses += 1
        player2_losses_points += score2
    elif score2 > score1:
        # status(gui, f"{player2} wins!")
        print(f'{player2} def {player1} {score2}-{score1}')
        player1_losses += 1
        player1_losses_points += score1

        player2_wins += 1
        player2_win_points += score2
    else:
        # status(gui, "It's a tie!")
        print(f'{player1} ties {player2} {score1}-{score2}')
        player1_ties += 1
        player2_ties += 1


if __name__ == "__main__":
    matches_played = 0
    for i in range(5): # 10
        print(i)
        main(parser.parse_args())
        matches_played += 1
    args = parser.parse_args()
    print()
    print("---END OF SIMULATION STATISTICS---")
    print(f"{args.player1} won {player1_wins} times with a total of {player1_win_points + player1_losses_points} points across {matches_played} games. They had {player1_win_points} total points in the wins, with an average of {round((player1_win_points / player1_wins), 3) if player1_wins != 0 else 0} points per win.")
    print(f"{args.player1} lost {player1_losses} times with a total of {player1_win_points + player1_losses_points} points across {matches_played} games. They had {player1_losses_points} total points in the losses, with an average of {round((player1_losses_points / player1_losses), 3) if player1_losses != 0 else 0} points per loss.")
    print(f"{args.player1} averaged {round(((player1_win_points + player1_losses_points)/matches_played), 3)} points per game.")
    print()
    print(f"{args.player2} won {player2_wins} times with a total of {player2_win_points + player2_losses_points} points across {matches_played} games. They had {player2_win_points} total points in the wins, with an average of {round((player2_win_points / player2_wins), 3) if player2_wins != 0 else 0} points per win.")
    print(f"{args.player2} lost {player2_losses} times with a total of {player2_win_points + player2_losses_points} points across {matches_played} games. They had {player2_losses_points} total points in the losses, with an average of {round((player2_losses_points / player2_losses), 3) if player2_losses != 0 else 0} points per loss.")
    print(f"{args.player2} averaged {round(((player2_win_points + player2_losses_points)/matches_played), 3)} points per game.")
    print()
    print(f"There were {player1_ties} ties over the {matches_played} matches")
    print(f"{args.player1} won {round((player1_wins / matches_played * 100), 3)}% of the time")
    print(f"{args.player2} won {round((player2_wins / matches_played * 100), 3)}% of the time")
