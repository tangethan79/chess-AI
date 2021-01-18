from chess import GetPieceLegalMoves, IsPositionUnderThreat, printPos, GetMove, GetPlayerPositions
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

class AI:
    def __init__(self, player, board):
        self.player = player
        self.board = board
        # self.moves will be of class TreeNode, it contains a board and all its subboards for a predetermined depth
        self.moves = None

    def initMoves(self):
        # the last parameter of treenode is the max depth that the ai will calculate
        self.moves = TreeNode(self.board, self.player, 1, 4)
        x = self.moves.newNodes()
        return True

    def getmove(self):
        if self.player == 10:
            inp = 1
        else:
            inp = -1
        self.moves = self.moves.rootFindMove(inp)
        return self.moves.board

    def getBoard(self, board):
        for node in self.moves.nodes:
            if node.board == board:
                self.moves = node
                break
        self.moves.treeUp()
        return True

class TreeNode:
    def __init__(self, board, player, depth, maxdepth):
        self.board = board
        self.nodes = []
        self.val = None
        self.player = player
        self.depth = depth
        self.maxdepth = maxdepth

    def newNodes(self):
        # this depth parameter says how many moves to calculate down
        if self.depth == self.maxdepth:
            return True
        else:
            pieces = GetPlayerPositions(self.board, self.player)
            newBoards = []
            for p in pieces:
                legal = GetPieceLegalMoves(self.board, p, None)
                for move in legal:
                    newboard = list(self.board)
                    newboard[move] = self.board[p]
                    newboard[p] = 2
                    # queening check
                    whiteq = [0, 1, 2, 3, 4, 5, 6, 7]
                    blackq = [56, 57, 58, 59, 60, 61, 62, 63]
                    if self.player == 10 and move in whiteq and newboard[move] == 11:
                        newboard[move] = 91
                    elif self.player == 20 and move in blackq and newboard[move] == 10:
                        newboard[move] = 90
                    if self.player == 10:
                        newBoards = newBoards + [TreeNode(newboard, 20, self.depth + 1, self.maxdepth)]
                    else:
                        newBoards = newBoards + [TreeNode(newboard, 10, self.depth + 1, self.maxdepth)]
            # the self.nodes parameter becomes the new boards
            # leave evaluation for later step since only leaves are evaluated
            self.nodes = newBoards
            for node in self.nodes:
                node.newNodes()
            return True

    # recursively prints nodes until leaves are reached
    def printMoves(self):
        printPos(self.board)
        #print("depth =", self.depth)
        if self.nodes:
            for board in self.nodes:
                board.printMoves()
        else:
            return True

    def rootFindMove(self, minmax):
        best = self.nodes[0]
        if minmax == 1:
            bestval = -1000000
            for node in self.nodes:
                test = node.alphaBeta(minmax*-1, -1000000, 1000000)
                node.val = test
                if test > bestval:
                    best = node
                    bestval = test
        else:
            bestval = 1000000
            for node in self.nodes:
                test = node.alphaBeta(minmax * -1, -1000000, 1000000)
                node.val = test
                if test < bestval:
                    best = node
                    bestval = test
        print (bestval)
        return best

    def alphaBeta(self, minmax, alpha, beta):
        if self.depth == self.maxdepth or self.nodes == None:
            return evalBoard(self.board)
        if minmax == 1:
            value = -1000000
            for node in self.nodes:
                value = max(value, node.alphaBeta(minmax*-1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        elif minmax == -1:
            value = 1000000
            for node in self.nodes:
                value = min(value, node.alphaBeta(minmax * -1, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    """
    def findMove(self, minmax, alpha, beta):
        if len(self.nodes[0].nodes) == 0:
            best = self.nodes[0]
            if minmax == -1:
                for node in self.nodes:
                    node.val = evalBoard(node.board)
                    if node.val < best.val:
                        best = node
            else:
                for node in self.nodes:
                    node.val = evalBoard(node.board)
                    if node.val > best.val:
                        best = node
            self.val = best.val
            return best
        else:
            best = self.nodes[0]

            if minmax == -1:
                value = 1000000
                for node in self.nodes:
                    
                    if len(node.nodes) == 0:
                        legal = []
                        bpieces = GetPlayerPositions(node.board, 20)
                        for piece in bpieces:
                            legal = legal + GetPieceLegalMoves(node.board, piece, None)
                        if len(legal) == 0:
                            node.val = 100000
                            print("white checkmate imminent")
                        else:
                            legal = []
                            wpieces = GetPlayerPositions(node.board, 10)
                            for piece in wpieces:
                                legal = legal + GetPieceLegalMoves(node.board, piece, None)
                            if len(legal) == 0:
                                node.val = -100000
                                print("black checkmate imminent")
                    else:
                    node.findMove(minmax * -1, alpha, beta)
                    node.val = min(value, node.val)
                    beta = min(beta, node.val)
                    if node.val < best.val:
                        best = node
                    if alpha >= beta:
                        break
            else:
                value = - 1000000
                for node in self.nodes:
                    
                    if len(node.nodes) == 0:
                        legal = []
                        bpieces = GetPlayerPositions(node.board, 20)
                        for piece in bpieces:
                            legal = legal + GetPieceLegalMoves(node.board, piece, None)
                        if len(legal) == 0:
                            node.val = 100000
                            print("white checkmate imminent")
                        else:
                            legal = []
                            wpieces = GetPlayerPositions(node.board, 10)
                            for piece in wpieces:
                                legal = legal + GetPieceLegalMoves(node.board, piece, None)
                            if len(legal) == 0:
                                node.val = -100000
                                print("black checkmate imminent")
                    else:
                    node.findMove(minmax*-1, alpha, beta)
                    node.val = max(value, node.val)
                    alpha = max(alpha, node.val)
                    if node.val < best.val:
                        best = node
                    if alpha >= beta:
                        break
            self.val = best.val
            return best
            """

    def treeUp(self):
        self.depth = self.depth -2
        if self.depth == self.maxdepth -2:
            self.newNodes()
            return True
        else:
            for node in self.nodes:
                node.treeUp()
            return True


def AImove(board, player):
    pieces = GetPlayerPositions(board, player)
    print(pieces)
    legal = {}
    for p in pieces:
        legal[p] = GetPieceLegalMoves(board, p, None)
    print(legal)
    threatened = {}
    for piece in legal:
        m = []
        for move in legal[piece]:
            newboard = list(board)
            newboard[piece] = 2
            newboard[move] = board[piece]
            if IsPositionUnderThreat(newboard, move, player):
                m = m + [move]
        threatened[piece] = m
    print(threatened)

def evalBoard(board):
    if IsPositionUnderThreat(board, board.index(80), 20):
        bpieces = GetPlayerPositions(board, 20)
        legal = []
        for piece in bpieces:
            legal = legal + GetPieceLegalMoves(board, piece, None)
        if len(legal) == 0:
            return (100000)
    if IsPositionUnderThreat(board, board.index(81), 10):
        legal = []
        wpieces = GetPlayerPositions(board, 10)
        for piece in wpieces:
            legal = legal + GetPieceLegalMoves(board, piece, None)
        if len(legal) == 0:
            return (-100000)
    # knights
    wneval =[-0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5,
             -0.4, -0.2, 0, 0, 0, 0, -0.2, -0.4,
              -0.3,  0,  0.05,  0.1,  0.1,  0.05,  0,  -0.3,
             -0.3, 0, 0.15, 0.1, 0.1, 0.15, 0, -0.3,
             -0.3, 0, 0.15, 0.2, 0.2, 0.15, 0, -0.3,
             -0.3, 0.05, 0.3, 0.15, 0.15, 0.3, 0.05, -0.3,
             -0.4, -0.2, 0, 0.05, 0.05, 0, -0.2, -0.4,
             -0.5, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.5]
    bneval = [0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5,
              0.4, 0.2, 0, -0.05, -0.05, 0, 0.2, 0.4,
              0.3, -0.05, -0.3, -0.15, -0.15, -0.3, -0.05, 0.3,
              0.3, 0, 0.15, -0.2, -0.2, 0.15, 0, 0.3,
              0.3, 0, 0.15, -0.1, -0.1, 0.15, 0, 0.3,
              0.3, 0, -0.05, -0.1, -0.1, -0.05, 0, 0.3,
              0.4, 0.2, 0, 0, 0, 0, 0.2, 0.4,
              0.5, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4, 0.5]

    #kings
    wkeval = [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3,
              -0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3,
              -0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3,
              -0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3,
              -0.2, -0.3, -0.3, -0.4, -0.4, -0.3, -0.3, -0.2,
              -0.1, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.1,
              0, 0, 0, 0, 0, 0, 0, 0,
              0.2, 0.3, 0.1, 0, 0, 0.1, 0.3, 0.2]
    bkeval = [-0.2, -0.3, -0.1, 0, 0, -0.1, -0.3, -0.2,
              0, 0, 0, 0, 0, 0, 0, 0,
              0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.1,
              0.2, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.2,
              0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3,
              0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3,
              0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3,
              0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3]

    #queens
    wqeval = [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2,
              -0.1, 0, 0, 0, 0, 0, 0, -0.1,
              -0.1, 0, 0.05, 0.05, 0.05, 0.05, 0, -0.1,
              -0.05, 0, 0.05, 0.05, 0.05, 0.05, 0, -0.05,
              0, 0, 0.05, 0.05, 0.05, 0.05, 0, -0.05,
              -0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0, -0.1,
              -0.1, 0, 0.05, 0, 0, 0, 0, -0.1,
              -0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2]
    bqeval = [0.2, 0.1, 0.1, 0.05, 0.05, 0.1, 0.1, 0.2,
              0.1, 0, -0.05, 0, 0, 0, 0, 0.1,
              0.1, -0.05, -0.05, -0.05, -0.05, -0.05, 0, 0.1,
              0, 0, -0.05, -0.05, -0.05, -0.05, 0, 0.05,
              0.05, 0, -0.05, -0.05, -0.05, -0.05, 0, 0.05,
              0.1, 0, -0.05, -0.05, -0.05, -0.05, 0, 0.1,
              0.1, 0, 0, 0, 0, 0, 0, 0.1,
              0.2, 0.1, 0.1, 0.05, 0.05, 0.1, 0.1, 0.2]

    #rooks
    wreval = [0, 0, 0, 0, 0, 0, 0, 0,
              0.05, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05,
              -0.05, 0, 0, 0, 0, 0, 0, -0.05,
              -0.05, 0, 0, 0, 0, 0, 0, -0.05,
              -0.05, 0, 0, 0, 0, 0, 0, -0.05,
              -0.05, 0, 0, 0, 0, 0, 0, -0.05,
              -0.05, 0, 0, 0, 0, 0, 0, -0.05,
              0, 0, 0, 0.05, 0.05, 0, 0, 0]
    breval = [0, 0, 0, -0.05, -0.05, 0, 0, 0,
              0.05, 0, 0, 0, 0, 0, 0, 0.05,
              0.05, 0, 0, 0, 0, 0, 0, 0.05,
              0.05, 0, 0, 0, 0, 0, 0, 0.05,
              0.05, 0, 0, 0, 0, 0, 0, 0.05,
              0.05, 0, 0, 0, 0, 0, 0, 0.05,
              -0.05, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.05,
              0, 0, 0, 0, 0, 0, 0, 0]

    #bishops
    wbeval = [-0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2,
              -0.1, 0, 0, 0, 0, 0, 0, -0.1,
              -0.1, 0, 0.05, 0.1, 0.1, 0.05, 0, -0.1,
              -0.1, 0.05, 0.05, 0.1, 0.1, 0.05, 0.05, -0.1,
              -0.1, 0, 0.1, 0.1, 0.1, 0.1, 0, -0.1,
              -0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, -0.1,
              -0.1, 0.05, 0, 0, 0, 0, 0.05, -0.1,
              -0.2, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.2]
    bbeval = [0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2,
              0.1, -0.05, 0, 0, 0, 0, -0.05, 0.1,
              0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, 0.1,
              0.1, 0, -0.1, -0.1, -0.1, -0.1, 0, 0.1,
              0.1, -0.05, -0.05, -0.1, -0.1, -0.05, -0.05, 0.1,
              0.1, 0, -0.05, -0.1, -0.1, -0.05, 0, 0.1,
              0.1, 0, 0, 0, 0, 0, 0, 0.1,
              0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2]

    #pawn
    wpeval = [0, 0, 0, 0, 0, 0, 0, 0,
              0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
              0.1, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.1,
              0.05, 0.05, 0.1, 0.25, 0.25, 0.1, 0.05, 0.05,
              0, 0, 0, 0.3, 0.3, 0, 0, 0,
              0.05, -0.05, -0.1, 0.2, 0.2, -0.1, -0.05, 0.05,
              0.05, 0.1, 0.1, -0.2, -0.2, 0.1, 0.1, 0.05,
              0, 0, 0, 0, 0, 0, 0, 0]
    bpeval = [0, 0, 0, 0, 0, 0, 0, 0,
              -0.05, -0.1, -0.1, 0.2, 0.2, -0.1, -0.1, -0.05,
              -0.05, 0.05, 0.1, -0.2, -0.2, 0.1, 0.05, -0.05,
              0, 0, 0, -0.3, -0.3, 0, 0, 0,
              -0.05, -0.05, -0.1, -0.25, -0.25, -0.1, -0.05, -0.05,
              -0.1, -0.1, -0.2, -0.3, -0.3, -0.2, -0.1, -0.1,
              -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5,
              0, 0, 0, 0, 0, 0, 0, 0]
    val = 0
    for i in range(0,64):
        if board[i] == 10:
            #if IsPositionUnderThreat(board, i, 20):
             #   val = val - 0.1
            val = val + bpeval[i]
            val = val -1
        elif board[i] == 11:
           # if IsPositionUnderThreat(board, i, 10):
            #    val = val + 0.1
            val = val + wpeval[i]
            val = val + 1
        elif board[i] == 20:
           #if IsPositionUnderThreat(board, i, 20):
             #   val = val - 0.1
            val = val + bneval[i]*0.8
            val = val - 3
        elif board[i] == 21:
           # if IsPositionUnderThreat(board, i, 10):
            #    val = val + 0.1
            val = val + wneval[i]*0.8
            val = val +3
        elif board[i] == 30:
            #if IsPositionUnderThreat(board, i, 20):
           #     val = val - 0.1
            val = val + bbeval[i]*0.8
            val = val - 3.25
        elif board[i] == 31:
           # if IsPositionUnderThreat(board, i, 10):
            #    val = val + 0.1
            val = val + wbeval[i]*0.8
            val = val + 3.25
        elif board[i] == 90:
            val = val + bqeval[i]*1.2
           # if IsPositionUnderThreat(board, i, 20):
            #    val = val - 0.1
            val = val - 9
        elif board[i] == 91:
            #if IsPositionUnderThreat(board, i, 10):
            #    val = val + 0.1
            val = val + wqeval[i]*1.2
            val = val + 9
        elif board[i] == 50:
            val = val + breval[i]
            #if IsPositionUnderThreat(board, i, 20):
            #    val = val - 0.1
            val = val -5
        elif board[i] == 51:
            val = val + wreval[i]
           # if IsPositionUnderThreat(board, i, 10):
            #    val = val + 0.1
            val = val + 5
        elif board[i] == 80:
            val = val + bkeval[i]*1.1
            #if IsPositionUnderThreat(board, i, 20):
            #    val = val - 0.1
            val = val - 900
        elif board[i] == 81:
            val = val + wkeval[i]*1.1
            #if IsPositionUnderThreat(board, i, 10):
            #    val = val + 0.1
            val = val + 900

    return val