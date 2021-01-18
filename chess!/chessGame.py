from chess import GetPieceLegalMoves, IsPositionUnderThreat, printPos, GetMove, GetPlayerPositions
from AI import AI, TreeNode, evalBoard
# first digit represents piece (1: pawn, 2: knight, 3: bishop, 5: rook, 9: queen, 8: king)
# second digit represents color (1: white, 0: black)
# a 2 means the space is blank

board = [50, 20, 30, 90, 80, 30, 20, 50,
         10, 10, 10, 10, 10, 10, 10, 10,
          2,  2,  2,  2,  2,  2,  2,  2,
          2,  2,  2,  2,  2,  2,  2,  2,
          2,  2,  2,  2,  2,  2,  2,  2,
          2,  2,  2,  2,  2,  2,  2,  2,
         11, 11, 11, 11, 11, 11, 11, 11,
         51, 21, 31, 91, 81, 31, 21, 51]
"""
board = [2, 80, 2, 2, 2, 2, 2, 2,
         2, 10, 10, 2, 2, 2, 10, 2,
          2,  2,  2,  2,  2,  10,  2,  10,
          2,  2,  2,  2,  2,  11,  2,  11,
          2,  2,  2,  2,  31,  2,  2,  2,
          2,  2,  50,  2,  2,  2,  2,  2,
         10, 2, 11, 2, 2, 2, 81, 2,
         2, 2, 2, 2, 2, 2, 2, 51]
"""

done = False
start = True
test1 = AI(10, board)
while not(done):
    printPos(board)
    print("white turn")

    print(evalBoard(board))
    # board = GetMove(board, 10)
    test1.board = board
    test1.initMoves()
    board = test1.getmove()
    if start:

        test = AI(20, board)
        test.initMoves()
        start = False
    else:
        test.board = board
    # finds the enemy king
    enking = board.index(80)
    # if the king is threatened,
    if IsPositionUnderThreat(board, enking, 20):
        # find all enemy pieces
        # and check if they have legal moves
        enpieces = GetPlayerPositions(board, 20)
        legal = []
        for piece in enpieces:
            legal = legal + GetPieceLegalMoves(board, piece, None)
        if len(legal) == 0:
            # if there are no legal moves, it is checkmate, the game ends
            print("black is in checkamte, white wins")
            break

    printPos(board)
    print("black turn")
    print(evalBoard(board))
    test.initMoves()
    board = test.getmove()
    enking = board.index(81)
    if IsPositionUnderThreat(board, enking, 10):
        enpieces = GetPlayerPositions(board, 10)
        legal = []
        for piece in enpieces:
            legal = legal + GetPieceLegalMoves(board, piece, None)
        if len(legal) == 0:
            print("white is in checkamte, black wins")
            break