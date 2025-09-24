# utils.py
# Python library of utility functions related to "A Game of Thrones: Hand of the King".
#
# Author: Matthew Eicholtz

from graphics import *
import importlib
import math
import os
import pdb
import random
import sys
import time

ROOT = os.path.dirname(os.path.realpath(__file__))

def ask_human(gui):
    """Query human player to make a choice.

    Parameters
    ----------
    gui : GraphWin object
        The main graphical user interface object (relies on graphics library).

    Returns
    -------
    which_card : int
        The linear index of the card to choose. If there are any errors, the output will be -1.
    """
    which_card = -1 # default value
    while gui.isOpen():
        # Check for mouse input
        pt = gui.checkMouse()
        if pt:
            x, y = int(pt.getX()), int(pt.getY())
            row = max(0, min(gui.rows - 1, (y - gui.margin // 2) // (gui.card_size + gui.margin)))
            col = max(0, min(gui.cols - 1, (x - gui.margin // 2) // (gui.card_size + gui.margin)))
            # print(f'(x,y)=({x},{y}), (row,col)=({row},{col})')
            which_card = sub2ind(row, col, gui.rows, gui.cols)
            break

        # Check for keyboard input
        if gui.checkKey() in ["Escape", "Ctrl+e"]:
            break

    return which_card

def get_valid_moves(board, rows, cols):
    """Compute the possible remaining moves based on current board state.

    Parameters
    ----------
    board : list of ints
        A flattened version of the board.
    rows : int
        Number of rows on the board.
    cols : int
        Number of columns on the board.

    Returns
    -------
    moves : list of ints
        List of available remaining moves, identified by their linear index on
        the flattened board.
    """

    # Initialize list of moves
    moves = []

    # Get row and col of 1-card (the one that moves!)
    ind = board.index(1)
    row, col = ind // cols, ind % cols

    # Check all directions for possible valid moves
    if row > 0: # up
        possible = [ind - cols * (i + 1) for i in range(row) if board[ind - cols * (i + 1)] != 0]
        possible.reverse()
        colors = []
        for i in possible:
            if board[i] not in colors:
                moves.append(i)
                colors.append(board[i])
    if row < rows - 1: # down
        possible = [ind + cols * (i + 1) for i in range(rows - row - 1) if board[ind + cols * (i + 1)] != 0]
        possible.reverse()
        colors = []
        for i in possible:
            if board[i] not in colors:
                moves.append(i)
                colors.append(board[i])
    if col > 0: # left
        possible = [ind - (i + 1) for i in range(col) if board[ind - (i + 1)] != 0]
        possible.reverse()
        colors = []
        for i in possible:
            if board[i] not in colors:
                moves.append(i)
                colors.append(board[i])
    if col < cols - 1: # right
        possible = [ind + (i + 1) for i in range(cols - col - 1) if board[ind + (i + 1)] != 0]
        possible.reverse()
        colors = []
        for i in possible:
            if board[i] not in colors:
                moves.append(i)
                colors.append(board[i])
    
    return moves

def get_winner(gui, players, banners):
    """Determine the winner based on total number of banners and display result.

    Parameters
    ----------
    gui : GraphWin object
        The main graphical user interface object (relies on graphics library).
    players : list of str
        List of player names.
    banners : list of lists of ints
        List identifying which player owns each banner. The syntax banners[i][j]
        indicates the ith player has the jth banner.

    Returns
    -------
    None
    """
    # Process player names (this is because "human def human" looks weirder than "Player 1 def Player 2")
    player1 = "Player 1" if players[0] == "human" or players[0] == players[1] else players[0]
    player2 = "Player 2" if players[1] == "human" or players[0] == players[1] else players[1]

    # Compute the score for each player
    score1 = sum(banners[0])
    score2 = sum(banners[1])

    # The player with the higher score wins
    if score1 > score2:
        status(gui, f"{player1} wins!")
        print(f'{player1} def {player2} {score1}-{score2}')
    elif score2 > score1:
        status(gui, f"{player2} wins!")
        print(f'{player2} def {player1} {score2}-{score1}')
    else:
        status(gui, "It's a tie!")
        print(f'{player1} ties {player2} {score1}-{score2}')

def ind2sub(index, rows, cols):
    """Convert a linear index to 2D row and column subscripts.

    Parameters
    ----------
    index : int
        Linear index of an item in a flattened 1D array.
    rows : int
        Number of rows in the desired 2D array.
    cols : int
        Number of columns in the desired 2D array.

    Returns
    -------
    row : int
        The corresponding row in the 2D array.
    col : int
        The corresponding column in the 2D array.

    """
    row = index // cols
    col = index % cols
    return row, col

def load_cards(file):
    """Initialize the board by loading 'pre-shuffled' cards from file.

    Parameters
    ----------
    file : str
        Text file containing comma-separated lists of cards on the board.
        Each card is identified by the color index of its group.
        The number of rows and columns on the board is dictated by the
        arrangement of cards in the file.

    Returns
    -------
    board : list of ints
        A flattened version of the board.
    rows : int
        Number of rows on the board.
    cols : int
        Number of columns on the board.
    """
    board = []
    rows = 0
    cols = None
    with open(file, "r") as f:
        for line in f:
            values = [int(x) for x in line.strip().split(",")]
            board.extend(values)
            rows += 1
            if cols is None:
                cols = len(values)
            elif cols != len(values):
                raise ValueError(f"Inconsistent number of columns at row {rows}")

    return board, rows, cols

def load_colors(file=os.path.join(ROOT, "data", "colors.txt")):
    """Load hex color codes for cards (fill and border).
    
    Parameters
    ----------
    file : str, optional (default=data/colors.txt)
        Filename containing hex color codes, two per line.
        The fill is listed first, then the border.

    Returns
    -------
    colors : list of lists of strings
        colors[i][0] and colors[i][1] refer to the fill and border color
        codes for the ith card type.
    """
    colors = []
    with open(file, "r") as f:
        for line in f:
            color_pair = line.strip().split(",")
            colors.append(color_pair)

    return colors

def load_player(name):
    """Load an AI player from file.
    
    Parameters
    ----------
    name : str
        Filename in 'players' directory for the AI player to load.

    Returns
    -------
    player : importlib module (or 0 for error)
        Module of AI player that must contain a function called "choice".
        If the player was not loaded correctly, the output will be 0.
    """
    if name is not None:
        print(f"Loading AI player: {name}")
        try:
            sys.path.append(os.path.join(ROOT, 'players')) # add directory containing AI player to system path
            player = importlib.import_module(name)
        except ImportError:
            print(f"\tERROR: Cannot import AI player")
            return 0

        if not hasattr(player, 'choice'):
            print(f"\tERROR: This AI player does not have a 'choice' function")
            return 0

        return player
    else:
        print(f"\tERROR: No AI player name was provided. Check inputs.")
        return 0

def make_gui(board, rows, cols, card_size=60, margin=10):
    """Create the graphical user interface for the game.

    Parameters
    ----------
    board : list of ints
        A flattened version of the board.
    rows : int
        Number of rows on the board.
    cols : int
        Number of columns on the board.
    card_size : int, optional (default=60)
        Height and width of cards, in pixels.
    margin : int, optional (default=10)
        Space in between cards, in pixels.

    Returns
    -------
    gui : GraphWin object
        The main graphical user interface object (relies on graphics library).
    """

    # Read colors from file
    colors = load_colors()

    # Make game window
    wid = cols * card_size + margin * (cols + 1)
    hei = rows * card_size + margin * (rows + 1) + 30 # the extra 30 is for instructions at the bottom
    gui = GraphWin("A Game of Thrones: Hand of the King", wid, hei)
    
    # Make card objects
    for row in range(rows):
        for col in range(cols):
            # Compute position and color of card
            x1 = margin * (col + 1) + card_size * col
            y1 = margin * (row + 1) + card_size * row
            x2 = x1 + card_size
            y2 = y1 + card_size
            whichcolor = board[cols * row + col] # index of the color for the card in the current (row, col)
            # print(f'row={row}, col={col}, index={cols * row + col}, color={whichcolor}')
            
            # Create rectangle
            card = Rectangle(Point(x1, y1), Point(x2, y2))
            card.setFill(colors[whichcolor - 1][0])
            card.setOutline(colors[whichcolor - 1][1])
            card.setWidth(4)
            card.draw(gui)

            # Add text identifier
            txt = Text(Point(x1 + 8, y1 + 6), whichcolor)
            txt.setSize(18)
            txt.setTextColor(colors[whichcolor - 1][1])
            txt.draw(gui)

    # Add text message at bottom
    txt = Text(Point(wid // 2, hei - 20), "")
    txt._reconfig("anchor", "c")
    txt.setSize(12)
    txt.draw(gui)

    # Attach relevant properties to the gui
    gui.rows = rows
    gui.cols = cols
    gui.card_size = card_size
    gui.margin = margin

    return gui

def make_move(gui, board, x0, x, collection):
    """Move the 1-card in the GUI to the position on the board specified by the input index,
    capturing cards of the same color along the way. Update the player's card collection accordingly.
    
    Parameters
    ----------
    gui : GraphWin object
        The main graphical user interface object (relies on graphics library).
    board : list of ints
        A flattened version of the board.
    x0 : int
        The initial (at the start of the game) linear index of the 1-card.
        This is important because it defines where the card is in the list
        of objects embedded in the GUI.
    x : int
        Linear index to move the 1-card to.
    collection : list of ints
        The array of card counts for each color set owned by the current player.

    Returns
    -------
    None
    """
    # Get relevant data
    items = gui.items[:-1]
    cards = items[::2]
    txt = items[1::2]

    x1 = board.index(1) # index of the 1-card on the board
    # print(f'moving from {x1} to {x}')

    # Remove captured cards from board
    d = gui.width + 100 # distance to move cards (the 100 ensures they move off the board)
    color = board[x] # color of the main captured card
    cards[x].move(d, 0)
    txt[x].move(d, 0)
    board[x] = 1 # the 1-card moves here
    collection[color - 2] += 1 # index decreases by 2 due to 0-indexing and the first color set being 2 (not 1)
    if abs(x - x1) < gui.cols: # move is either left or right
        dx = (x - x1) * (gui.card_size + gui.margin)
        dy = 0
        if x < x1: # left
            possible = range(x + 1, x1)
        else: # right
            possible = range(x1 + 1, x)
    else: # move is either up or down
        dx = 0
        dy = ((x - x1) // gui.cols) * (gui.card_size + gui.margin)
        if x < x1: # up
            possible = range(x + gui.cols, x1, gui.cols)
        else: # down
            possible = range(x1 + gui.cols, x, gui.cols)

    for i in possible:
        if board[i] == color:
            cards[i].move(d, 0)
            txt[i].move(d, 0)
            board[i] = 0  # there is no card in this position anymore
            collection[color - 2] += 1

    # Move the 1-card to the correct position
    cards[x0].move(dx, dy)
    txt[x0].move(dx, dy)
    board[x1] = 0

def print_board(board, rows, cols):
    """Display the board in the terminal in 2D.
    
    Parameters
    ----------
    board : list of ints
        A flattened version of the board.
    rows : int
        Number of rows on the board.
    cols : int
        Number of columns on the board.

    Returns
    -------
    None
    """
    for row in range(rows):
        print(*board[row*cols:(row+1)*cols])

def shuffle_cards(num_colors=8):
    """Initialize the board by shuffling the cards.
    
    Parameters
    ----------
    num_colors : int, optional (default=8)
        Number of color sets on the board (including the 1-card that moves).
        Value must be in the range [3, 8].

    Returns
    -------
    board : list of ints
        A flattened version of the board.
    rows : int
        Number of rows on the board.
    cols : int
        Number of columns on the board.
    """
    board = [[i] * i for i in range(1, num_colors + 1)]
    board = [item for sublist in board for item in sublist]
    random.shuffle(board)

    rows, cols = triangular_factors(num_colors)

    return board, rows, cols

def sub2ind(row, col, rows, cols):
    """Convert row and column subscripts to a linear index.

    Parameters
    ----------
    row : int
        The row index of an item in a 2D array.
    col : int
        The column index of an item in a 2D array.
    rows : int
        Number of rows in the 2D array.
    cols : int
        Number of columns in the 2D array.

    Returns
    -------
    index : int
        The corresponding linear index in the flattened 1D array.
    """
    return cols * row + col

def run_tests():
    """Run basic tests using some of the other utility functions."""
    print()
    print("Testing load_cards() function:")
    board, rows, cols = load_cards(os.path.join(ROOT, "data", "board0.txt"))
    print(*board)
    print(f'rows={rows}, columns={cols}')

    print()
    print("Testing load_colors() function:")
    print(load_colors())

    print()
    print("Testing shuffle_cards() function:")
    for num_colors in range(3, 9):
        board, rows, cols = shuffle_cards(num_colors)
        print(*board)
        print(f'rows={rows}, columns={cols}')

    print()
    print("Testing make_gui() function:")
    board, rows, cols = load_cards(os.path.join(ROOT, "data", "board0.txt"))
    print(*board)
    print(f'rows={rows}, columns={cols}')
    gui = make_gui(board, rows, cols)
    while True:
        if gui.isClosed() or gui.checkKey() in ["Escape", "Ctrl+e"]:
            break
    gui.close()

    for n in range(3, 9):
        board, rows, cols = shuffle_cards(n)
        print(*board)
        print(f'rows={rows}, columns={cols}')
        gui = make_gui(board, rows, cols)
        time.sleep(1)
        # while True:
        #     if gui.isClosed() or gui.checkKey() in ["Escape", "Ctrl+e"]:
        #         break
        gui.close()

def status(gui, msg):
    """Update the text status in the GUI.

    Parameters
    ----------
    gui : GraphWin object
        The main graphical user interface object (relies on graphics library).
    msg : str
        The string message to display in the gui.

    Returns
    -------
    None
    """
    if gui.isOpen():
        txt = gui.items[-1] # the text to update should be the last object created
        txt.setText(msg)

def triangular_factors(n):
    """Map an integer to a tuple of integers such that the product 
    of the tuple is equal to the sum of integers from 1 to n. The
    purpose of this function is to generate reasonable board sizes
    given the desired number of color sets in the game.

    Parameters
    ----------
    n : int
        The desired number of color sets in the game.

    Returns
    -------
    factors : tuple of ints
        The size of the board (rows, cols).
    """
    total = n * (n + 1) // 2 # sum from 1 to n
    sqrt_total = int(math.isqrt(total))

    for a in range(sqrt_total, 0, -1):
        if total % a == 0:
            b = total // a
            return (a, b)

def update_banners(turn, color, cards, banners):
    """Check to see if current player should capture a banner.

    Parameters
    ----------
    turn : int {0, 1}
        Whose turn is it?
    color : int
        Index of the color in question for the current move.
    cards : list of lists of ints
        How many cards does each player own? The syntax cards[i][j] = k
        indicates that the ith player owns k cards of the jth color set.
    banners : list of lists of ints
        Which banners does each player own? The syntax banners[i][j] = 1
        indicates that the ith player owns the banner of the jth color set.

    Returns
    -------
    None
    """
    player = turn
    opponent = abs(turn - 1)
    color_index = color - 2
    if cards[player][color_index] >= cards[opponent][color_index]:
        banners[player][color_index] = 1
        banners[opponent][color_index] = 0

if __name__ == "__main__":
    run_tests()
