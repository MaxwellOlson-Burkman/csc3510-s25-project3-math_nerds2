[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/psOWlUhL)
# Project 3: Hand of the King

## Purpose

The purpose of this project is to ensure that you are able to:
- use Git, GitHub, and GitHub Classroom to access and submit projects
- leverage appropriate software (e.g. VS Code, terminal) to complete programming tasks
- develop Python code for adversarial AI search algorithms with pruning and custom heuristics
- communicate ideas clearly and concisely
- work collaboratively with a peer to creatively solve problems

## Objective

For this project, you will work individually or in pairs to develop a Python-based AI player for [A Game of Thrones: Hand of the King](https://boardgamegeek.com/boardgame/205610/game-thrones-hand-king), a competitive multiplayer card game. Here's how the game works: the standard board consists of 36 colored cards randomly arranged in a 6×6 grid as shown below.

![alt text](https://github.com/FloridaSouthernCS/csc3510-s25-project3/blob/main/data/screenshot.png "Shuffled Cards")

During the game, players take turns moving the purple 1-card to capture one or more other cards. A legal move requires both a direction (up, down, left, right) and a color (identified by the numbered index on the cards). If there is more than one card of the same color along a direction, the only valid move is to the furthest card. When a move is executed, the player making the move captures all cards of the selected color in the specified direction. If the acquisition of new cards results in the current player owning an equal or greater amount of that color than their opponent, the player gains the banner for that color. The game ends when there are no remaining valid moves, and the winner is the player with the most banners.

## Requirements

The code provided here was developed in Python 3.12.2 on Windows 10 using VS Code and a Git Bash terminal. Setup and usage may vary slightly for other operating systems or software tools. You do not need to install any external libraries via pip or venv.

The instructions that follow assume you have properly installed git on your machine. Click [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if you need help doing that.

## Setup

The best way to use this code is to [clone the repository](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository) to your local computer. To do so in VS Code, open a terminal and navigate to the parent directory of your choice using the `cd` command, e.g.:

    $ cd ~/Documents/csc3510
    (NOTE: Your path may be different from the one above!)

Then, use `git clone` to create a new subdirectory called project3 with the code from this repository:

    $ git clone https://github.com/FloridaSouthernCS/csc3510-s25-project3.git project3
    (NOTE: Your link will be slightly different from the one above!)

Enter into the directory and make sure the appropriate files are there by using the `ls` command:

    $ cd project3
    $ ls

## Usage

Use the following commands to play the game:

- To play HOTK with two human players,

        $ python hand_of_the_king.py

- To play HOTK using an AI player (as player1, for example),

        $ python hand_of_the_king.py --player1 ai_player

    where `ai_player` is the name of any file in the players directory that contains the function `choice(board, rows, cols, turn, cards=[], banners=[])`. Use `randy.py` as a template for your own player.

- You can play human vs human, AI vs human, or AI vs AI. Check out the `argparse` code for additional optional command-line arguments.

## Instructions

To earn credit for this project, you must complete the following tasks:

1. Implement a Python-based AI player that leverages the adversarial search techniques we learned in class. Specifically, your player should incorporate the **minimax algorithm with alpha-beta pruning**. Add your AI player to the `players` directory of the repo. The name of your file does not matter, but the contents do matter. At a minimum, you must include a function with the following signature:

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

You can add other code (e.g. helper functions, library imports, global constants) as necessary, but only the `choice` function is called in the `hand_of_the_king.py` program. Your code will be graded on several factors including, but not limited to, length, comments, content, correctness, and performance.

2. An important constraint on your player is that every move must be executed within a strict 5-second time limit. This means you will likely need to **limit the search depth and include a custom heuristic function** to estimate the utility at non-terminal nodes in the game tree. Be creative!

### Important Rules

1. If your AI player needs to access other files that you create from some external data analysis conducted in your development process, consult the instructor first on whether your extra files are allowed.

2. Students are permitted to use generative AI tools to improve their learning on projects, but AI should not complete the project for you! _Any_ AI use must be cited directly in the code (e.g. with a link to the ChatGPT conversation). Consult the syllabus "Special Note on AI Usage" for more details.

3. There is the potential for extra credit at the discretion of the instructor for top-performing AI players (versus your peers and Dr. Eicholtz).

## Submission

"Submitting" the project means pushing to your group repo on GitHub Classroom. Students will earn individual grades that take into account the quality and quantity of their own contributions, so everyone is strongly encouraged to commit early and often. ***The deadline to push changes to your repository for grading is Tuesday, April 22 @ 11:59 PM EST.***