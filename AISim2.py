import random
import sys

# This function prints out the board so that it was passed. Returns None.
def drawBoard(board):
    HLINE = ' +---+---+---+---+---+---+---+---+'
    VLINE = ' |   |   |   |   |   |   |   |   |'

    print('   1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end='')
        for x in range(8):
            print('| %s' % (board[x][y]), end=' ')
        print('|')
        print(VLINE)
        print(HLINE)

# Blanks out the board it is passed, except for the original starting position.
def resetBoard(board):
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

    # Starting pieces:
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

# Creates a brand new, blank board data structure.
def getNewBoard():
    board = []
    for i in range(8):
        board.append([' '] * 8)
    return board

# Return False if the player's move on space xstart, ystart is invalid.
# If it is a valid move, returns a list of spaces that would become the
# player's if they made a move here.
def isValidMove(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    # Temporarily set the tile on the board
    board[xstart][ystart] = tile

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # first step in the direction
        y += ydirection # first step in the direction
        # There is a piece belonging to the other player next to our piece.
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # Break out of while loop, then
                    break               # continue in for loop
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction
                # until we reach the original space, noting all the tiles along
                # the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])

    board[xstart][ystart] = ' ' # Restore the empty space
    if len(tilesToFlip) == 0:   # If no tiles flipped, this is not valid move.
        return False
    return tilesToFlip

# Returns true if the coordinates are located on the board.
def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <= 7

# Returns a new board with . making the valid moves the given player can make.
def getBoardWithValidMoves(board, tile):
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard

# Returns a list of [x, y] lists of valid moves for the given player on the
# given board.
def getValidMoves(board, tile):
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

# Determine the score by counting the tiles. Return a dictionary with
# keys 'X' and 'O'.
def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

# Lets the player type which tile they want to be. Returns a list with
# the player's tile as the first item, and the computer's tile as
# the second item.
def enterPlayerTile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    # The first element in the list is the player's tile, the second is
    # the computer's tile.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

# Randomly choose the player who goes first.
def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'

# This function returns True if player wants to play again, otherwise it
# returns False.
def playAgain():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

# Place the tile on the board at xstart, ystart, and flip any of the opponent's
# pieces. Return False if this is an invalid move, True if it is valid.
def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

# Make a duplicate of the board list and return the duplicate
def getBoardCopy(board):
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard

# Returns True if the position is in one of the four corners.
def isOnCorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

# Let the player type in their move. Returns the move as [x, y] (or returns the
# strings 'hints' or 'quit')
def getPlayerMove(board, playerTile):
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, or type quit to end the game, or hints to turn',
              'off/on hints.')
        move = input().lower()
        if move == 'quit':
            return 'quit'
        if move == 'hints':
            return 'hints'

        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('That is not a valid move. Type the x digit (1-8) then the',
                  'y digit (1-8).')
            print('For example, 81 will be the top-right corner.')

    return [x, y]

# Given a board and the computer's tile, determine where to move and
# return that move as a [x, y] list.
def getComputerMove(board, computerTile):
    possibleMoves = getValidMoves(board, computerTile)

    # Randomize the order of the possible moves
    random.shuffle(possibleMoves)

    # Always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    # Go through all the possible moves and remember the best scoring move.
    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

# Prints out the current score.
def showPoints(playerTile, computerTile):
    scores = getScoreOfBoard(mainBoard)
    print('You have %s points. The computer has %s points.' %
            (scores[playerTile], scores[computerTile]))

print('Welcome to Reversi!')

xwins = 0
owins = 0
ties = 0
numGames = int(input('Enter number of games to run: '))

for game in range(numGames):
    print('Game #%s:' % (game), end=' ')
    # Reset the board and game.
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    if whoGoesFirst() == 'player':
        turn = 'X'
    else:
        turn = 'O'

    while True:
        if turn == 'X':
            # X's turn.
            otherTile = 'O'
            x, y = getComputerMove(mainBoard, 'X')
            makeMove(mainBoard, 'X', x, y)
        else:
            # O's turn.
            otherTile = 'X'
            x, y = getComputerMove(mainBoard, 'O')
            makeMove(mainBoard, 'O', x, y)

        if getValidMoves(mainBoard, otherTile) == []:
            break
        else:
            turn = otherTile

    # Display the final score.
    scores = getScoreOfBoard(mainBoard)
    print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))

    if scores['X'] > scores['O']:
        xwins += 1
    elif scores['X'] < scores['O']:
        owins += 1
    else:
        ties += 1

numGames = float(numGames)
xpercent = round(((xwins / numGames) * 100), 2)
opercent = round(((owins / numGames) * 100), 2)
tiepercent = round(((ties / numGames) * 100), 2)
print('X wins %s games (%s%%), O wins %s games (%s%%), ties for %s games (%s%%) of %s games total.' %
        (xwins, xpercent, owins, opercent, ties, tiepercent, numGames))
