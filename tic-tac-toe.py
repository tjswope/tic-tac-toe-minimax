import pygame
from copy import deepcopy

# constants that will be used to draw grid
SQUARE_WIDTH = 100
ROWS_COLUMNS = 3
IN_A_ROW = 3

WIN = pygame.display.set_mode((SQUARE_WIDTH * ROWS_COLUMNS, SQUARE_WIDTH * ROWS_COLUMNS))
pygame.display.set_caption("tic-tac-toe")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

X_IMAGE = pygame.image.load("x.png")
O_IMAGE = pygame.image.load("o.png")

# makes an actual copy of the object not just a reference to the object. BOXES!
from copy import deepcopy



# A Node will be a box on the grid.
class Square:
    def __init__(self, symbol):
        self.symbol = symbol

    def __eq__(self, other):
        return self.symbol == other.symbol

    # Function will draw the Square on the grid using its image.
    def draw(self, row, column):
        if self.symbol == 'x':
            WIN.blit(X_IMAGE, (row * 100, column * 100))
        else:
            WIN.blit(O_IMAGE, (row * 100, column * 100))


class Matrix:
    def __init__(self):
        self.symbol = "x"
        self.grid = []  # grid will be a 2D list of Nodes
        for i in range(ROWS_COLUMNS):  # iterate through # of ROWS
            self.grid.append([])  # add a 1D array
            for j in range(ROWS_COLUMNS):  # iterate through # of COlS and add None
                self.grid[i].append(None)

    def draw(self):
        WIN.fill(WHITE)  # fill that background with white

        for row in range(len(self.grid)):  # iterate through and draw each Node
            for column in range(len(self.grid[row])):
                if self.grid[row][column] is not None:
                    self.grid[row][column].draw(row, column)

        # draw grid lines
        for i in range(ROWS_COLUMNS):
            pygame.draw.line(WIN, GREY, (0, i * SQUARE_WIDTH), (ROWS_COLUMNS * SQUARE_WIDTH, i * SQUARE_WIDTH))
            for j in range(ROWS_COLUMNS):
                pygame.draw.line(WIN, GREY, (j * SQUARE_WIDTH, 0), (j * SQUARE_WIDTH, ROWS_COLUMNS * SQUARE_WIDTH))

        # tell pygame to update
        pygame.display.update()

    # get the Node at the clicked position
    # figure out which Square was clicked
    # check to see if that Square is None
    # if it is add a new Square to that location, change the symbol
    def get_clicked_square(self, position):
        y, x = position

        row = y // SQUARE_WIDTH
        col = x // SQUARE_WIDTH

        self.grid[row][col]

        if self.grid[row][col] is None:
            self.grid[row][col] = Square(self.symbol)
            if self.check_winner() is not None:
                print("the winner is " + self.symbol)
            self.symbol = 'x' if self.symbol == 'o' else 'o'

    # write check winner
    # check to see if there is a winner, if there is return the winning symbol,
    # else return None.
    def check_winner(self):
        in_a_row = 0
        for row in range(0, ROWS_COLUMNS):
            for column in range(0, ROWS_COLUMNS):
                if (self.grid[row][column] is not None and self.grid[row][column].symbol == self.symbol):
                    in_a_row += 1
                else:
                    in_a_row = 0

                if in_a_row == IN_A_ROW:
                    return self.symbol

            in_a_row = 0

        for column in range(0, ROWS_COLUMNS):
            for row in range(0, ROWS_COLUMNS):
                if (self.grid[row][column] is not None and self.grid[row][column].symbol == self.symbol):
                    in_a_row += 1
                else:
                    in_a_row = 0

                if in_a_row == IN_A_ROW:
                    return self.symbol

            in_a_row = 0

        # diagonal down
        # print("Check diagonal")
        for row in range(0, ROWS_COLUMNS - IN_A_ROW + 1):
            for column in range(0, ROWS_COLUMNS - IN_A_ROW + 1):
                inner_count = 0
                in_a_row = 0
                while row + inner_count < ROWS_COLUMNS and column + inner_count < ROWS_COLUMNS:
                    if (self.grid[row + inner_count][column + inner_count] is not None and self.grid[row + inner_count][
                        column + inner_count].symbol == self.symbol):
                        in_a_row += 1
                    else:
                        in_a_row = 0

                    if in_a_row == IN_A_ROW:
                        return self.symbol

                    inner_count += 1

                in_a_row = 0

        # diagonal up
        for row in range(IN_A_ROW - 1, ROWS_COLUMNS):
            for column in range(0, ROWS_COLUMNS - IN_A_ROW + 1):
                inner_count = 0
                in_a_row = 0
                while row - inner_count >= 0 and column + inner_count < ROWS_COLUMNS:
                    if (self.grid[row - inner_count][column + inner_count] is not None and self.grid[row - inner_count][
                        column + inner_count].symbol == self.symbol):
                        in_a_row += 1
                    else:
                        in_a_row = 0

                    if in_a_row == IN_A_ROW:
                        return self.symbol

                    inner_count += 1

                in_a_row = 0
        in_a_row = 0

    def is_full(self):
        for row in range(0, ROWS_COLUMNS):
            for column in range(0, ROWS_COLUMNS):
                if self.grid[row][column] is None:
                    return False
        return True

    def get_valid_moves(self):
        moves = []

        for row in range(0, ROWS_COLUMNS):
            for column in range(0, ROWS_COLUMNS):
                if self.grid[row][column] is None:
                    moves.append((row, column))
        print(moves)
        return moves

    def print(self):
        print("score = " + str(self.evaluate()))
        for column in range(0, ROWS_COLUMNS):
            for row in range(0, ROWS_COLUMNS):
                if self.grid[row][column] is not None:
                    print(self.grid[row][column].symbol, end = '')
                else:
                    print("_", end = '')
            print()

        print()

    # o is trying to maximize - remember we're not trying to write specific rules, but instead come up with a general algorithm for
    # scoring the board.
    def evaluate(self):
        return 0

    # return the new board after a move.
    # will pass a new board object to the game
    def ai_move(self,board):
      #self.print()
      self.grid = board.grid
      if self.check_winner():
          print(self.symbol + " is the winner")
      self.symbol = 'x' if self.symbol == 'o' else 'o'


# this function will be called recursively
# current_board will be a board object - based on this board
# depth - how far am i making this tree - every time we call this function the depth will decrease by one.
# max_player - boolean value - are we trying minimize or maximize?
# game - the actual game object.
def minimax(current_board, depth, max_player, symbol):
# evaluate position when we reach the depth of the tree, evaluations bubble up.
    if depth == 0 or current_board.is_full() or current_board.check_winner() is not None:
        return current_board.evaluate(), current_board

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(current_board, 'o'):
            evaluation = minimax(move, depth - 1, False, 'x')[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(current_board, 'x'):
            evaluation = minimax(move, depth - 1, True, 'o')[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

    return minEval, best_move


# This function crates a deep copy of the current board, determines all possible moves that color can make, and returns a list that contains the boards that would result from the possible moves.
def get_all_moves(board, symbol):
    moves = []  # this array will contain Boards

    possible_moves = board.get_valid_moves()  # gets an array that contains the lowest open row in each column. It's main purpose is to see if a column is full so that we can skip over that row.
    for row_column in possible_moves:  # loop through each column
        row, column = row_column
        temp_board = deepcopy(board)  # creates a deep copy of the board as opposed to a shallow copy.
        temp_board.grid[row][column] = Square(symbol) # add a piece to the new copy of board in column
        temp_board.print()                      # uncomment if you want to debug your algorothim to see what moves are being considered.
        moves.append(temp_board)  # add the new board to the list

    return moves

def main():
    matrix = Matrix()
    matrix.draw()

    run = True  # boolean that will control our main while loop

    while run:
        matrix.draw()
        if matrix.symbol == 'x':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if pygame.mouse.get_pressed()[0]:  # left button
                    matrix.get_clicked_square(pygame.mouse.get_pos())

        else:
            value, new_board = minimax(matrix, 2, True, 'o')
            matrix.ai_move(new_board)

    pygame.quit()

main()
