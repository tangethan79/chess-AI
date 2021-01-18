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
        return self.moves.rootFindMove(inp)

    def getBoard(self, board):
        for node in self.moves.nodes:
            if node.board == board:
                self.moves = node
                break
        self.moves.treeUp()
        return True

class queue:
    def __init__ (self):
        self.store = []
    def enqueue(self, node):
        self.store = self.store + [node]
    def dequeue(self):
        ret = self.store[0]
        self.store = self.store[1:len(self.store)]
        return ret

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
        # print("depth =", self.depth)
        if self.nodes:
            for board in self.nodes:
                board.printMoves()
        else:
            return True

    def rootFindMove(self, minmax):
        best = None
        convert = {0: 63, 1: 62, 2: 61, 3: 60, 4: 59, 5: 58, 6: 57, 7: 56, 8: 55, 9: 54, 10: 53, 11: 52, 12: 51, 13: 50, 14: 49,
         15: 48, 16: 47, 17: 46, 18: 45, 19: 44, 20: 43, 21: 42, 22: 41, 23: 40, 24: 39, 25: 38, 26: 37, 27: 36, 28: 35,
         29: 34, 30: 33, 31: 32, 32: 31, 33: 30, 34: 29, 35: 28, 36: 27, 37: 26, 38: 25, 39: 24, 40: 23, 41: 22, 42: 21,
         43: 20, 44: 19, 45: 18, 46: 17, 47: 16, 48: 15, 49: 14, 50: 13, 51: 12, 52: 11, 53: 10, 54: 9, 55: 8, 56: 7,
         57: 6, 58: 5, 59: 4, 60: 3, 61: 2, 62: 1, 63: 0}
        candidates = []
        startpieces = GetPlayerPositions(self.board, self.player)
        if minmax == 1:
            bestval = -1000000
            for node in self.nodes:
                test = node.alphaBeta(minmax * -1, -1000000, 1000000)
                node.val = test
                endpieces = GetPlayerPositions(node.board, self.player)
                for end in endpieces:
                    if self.board[end] == 2:
                        break
                for start in startpieces:
                    if node.board[start] == 2:
                        break
                candidates = candidates + [[[convert[start],convert[end]], test]]
                if test > bestval:
                    best = [convert[start],convert[end]]
                    bestval = test
        else:
            bestval = 1000000
            for node in self.nodes:
                test = node.alphaBeta(minmax * -1, -1000000, 1000000)
                node.val = test
                endpieces = GetPlayerPositions(node.board, self.player)
                for end in endpieces:
                    if self.board[end] == 2:
                        break
                for start in startpieces:
                    if node.board[start] == 2:
                        break
                candidates = candidates + [[[convert[start],convert[end]], test]]
                if test < bestval:
                    best = [convert[start],convert[end]]
                    bestval = test
        return (best, candidates)

    def alphaBeta(self, minmax, alpha, beta):
        if self.depth == self.maxdepth or self.nodes == None:
            return evalBoard(self.board)
        if minmax == 1:
            value = -1000000
            for node in self.nodes:
                value = max(value, node.alphaBeta(minmax * -1, alpha, beta))
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
        self.depth = self.depth - 2
        if self.depth == self.maxdepth - 2:
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

def GetPlayerPositions(board, player):
    pos = []
    if player == 10:
        for i in range (0, 64):
            if board[i]%10 == 1:
                pos = pos + [i]
    else:
        for i in range (0, 64):
            if board[i]%10 == 0:
                pos = pos + [i]
    return pos

def GetMove(board, player):
    translate = {"a8":0, "b8":1, "c8":2, "d8":3, "e8":4, "f8":5, "g8":6, "h8":7, "a7":8, "b7":9, "c7":10, "d7":11, "e7":12, "f7":13, "g7":14, "h7":15, "a6":16, "b6":17, "c6":18, "d6":19, "e6":20, "f6":21, "g6":22, "h6":23, "a5":24, "b5":25, "c5":26, "d5":27, "e5":28, "f5":29, "g5":30, "h5":31, "a4":32, "b4":33, "c4":34, "d4":35, "e4":36, "f4":37, "g4":38, "h4":39, "a3":40, "b3":41, "c3":42, "d3":43, "e3":44, "f3":45, "g3":46, "h3":47, "a2":48, "b2":49, "c2":50, "d2":51, "e2":52, "f2":53, "g2":54, "h2":55, "a1":56, "b1":57, "c1":58, "d1":59, "e1":60, "f1":61, "g1":62, "h1":63}
    pieces = GetPlayerPositions(board,player)
    while True:
        start = input("start: ")
        if start in translate:
            start = translate[start]
            if start in pieces:
                legal = GetPieceLegalMoves(board, start, None)
                if len(legal) == 0:
                    print("not valid")
                else:
                    break
            else:
                print("not valid")
        else:
            print("not valid")
    legal = GetPieceLegalMoves(board, start, None)
    while True:
        end = input("end: ")
        if end in translate:
            end = translate[end]
            if end in legal:
                break
            else:
                print("not valid")
        else:
            print("not valid")
    newboard = []
    for p in board:
        newboard = newboard + [p]
    newboard[start] = 2
    newboard[end] = board[start]
    # queening check
    whiteq = [0,1,2,3,4,5,6,7]
    blackq = [56,57,58,59,60,61,62,63]
    if player == 10 and end in whiteq and board[start] == 11:
        newboard[end] = 91
    elif player == 20 and end in blackq and board[start] == 10:
        newboard[end] = 90
    return newboard

# in order to check if a move is legal, one must check if moving said piece
# results in a check of your own king
# this unfortunately means you have to call IsUnderThreat which already calls
# GetPieceLegalMoves
# I added in an extra parameter to except this if the function is from
# IsUnderThreat to prevent infinite function calls
# I'm not sure if theres a better solution
def GetPieceLegalMoves(board, position, pin):
    piece = board[position]
    legal = []
    # pawn check
    if piece == 10 or piece == 11:
        if piece == 10:
            f = position + 8
            if board[f] == 2:
                legal = legal + [f]
            if f not in [15, 23, 31, 39, 47, 55]:
                r = f+1
                if r <64:
                    if board[r] % 10 == 1:
                        legal = legal + [r]
            if f not in [8, 16, 24, 32, 40, 48]:
                l = f-1
                if board[l] % 10 == 1:
                    legal = legal + [l]
        if piece == 11:
            f = position - 8
            if board[f] == 2:
                legal = legal + [f]
            if f not in [15, 23, 31, 39, 47, 55]:
                r = f+1
                if board[r] % 10 == 0:
                    legal = legal + [r]
            if f not in [8, 16, 24, 32, 40, 48]:
                l = f-1
                if board[l] % 10 == 0:
                    legal = legal + [l]
    # knight check
    elif piece == 20 or piece == 21:

        uur = position - 15
        udr = position - 6
        uul = position - 17
        udl = position - 10

        ddl = position + 15
        dul = position + 6
        ddr = position + 17
        dur = position + 10

        # each of these values corresponds to a specific possible position a knight can take. u means up, d means down,
        # r means right, and l means left.
        opt = [uur, udr, uul, udl, ddl, dul, ddr, dur]
        for o in opt:
            if o >= 0 and o <= 63:
                if not(position in [7, 15, 23, 31, 39, 47, 55, 63] and o in [uur, udr, ddr, dur]):
                    # this refers to the rightmost edge of the board
                    if not(position in [0, 8, 16, 24, 32, 40, 48, 56] and o in [uul, udl, ddl, dul]):
                        # this refers to the leftmost edge of the board
                        if not(position in [6, 14, 22, 30, 38, 46, 54, 62] and o in [udr, dur]):
                            # this refers to column g
                            if not (position in [1, 9, 17, 25, 33, 41, 49, 57] and o in [udl, dul]):
                                # this refers to column b
                                if board[o]% 10 != board[position] % 10:
                                    # check if occupied space is same colour or not
                                    legal = legal + [o]
    # rook check
    elif piece == 50 or piece == 51:
        inc = position
        # down check
        while True:
            inc = inc + 8
            if inc <= 63 and board[inc] % 10 != board[position] % 10:
                # overflows are when over 63
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # up check
        while True:
            inc = inc - 8
            if inc >=0 and board[inc] % 10 != board[position] % 10:
                # overflows are when under 0
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # left check
        while True:
            inc = inc -1
            if inc >=0 and not(inc in [7, 15, 23, 31, 39, 47, 55, 63]) and board[inc] % 10 != board[position] % 10:
                # if the increment is on the rightmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # right check
        while True:
            inc = inc +1
            if  inc <= 63 and not(inc in [0, 8, 16, 24, 32, 40, 48, 56]) and board[inc] % 10 != board[position] % 10:
                # if the increment is on the leftmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
    # bishop check
    elif piece == 30 or piece == 31:
        inc = position
        # down left check
        while True:
            inc = inc + 7
            if inc >= 0 and inc <= 63 and not (inc in [7, 15, 23, 31, 39, 47, 55, 63]) and board[inc] % 10 != board[
                position] % 10:
                # if the increment is on the rightmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # down right check
        while True:
            inc = inc + 9
            if inc >= 0 and inc <= 63 and not (inc in [0, 8, 16, 24, 32, 40, 48, 56]) and board[inc] % 10 != board[
                position] % 10:
                # if the increment is on the leftmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # up left check
        while True:
            inc = inc - 9
            if inc >= 0 and inc <= 63 and not (inc in [7, 15, 23, 31, 39, 47, 55, 63]) and board[inc] % 10 != board[
                position] % 10:
                # if the increment is on the rightmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # up right check
        while True:
            inc = inc - 7
            if inc >= 0 and inc <= 63 and not (inc in [0, 8, 16, 24, 32, 40, 48, 56]) and board[inc] % 10 != board[
                position] % 10:
                # if the increment is on the leftmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
    # queen check
    elif piece == 90 or piece == 91:
        inc = position
        # down left check
        while True:
            inc = inc + 7
            if inc >= 0 and inc <= 63 and not (inc in [7, 15, 23, 31, 39, 47, 55, 63]) and board[inc] % 10 != board[
                position] % 10:
                # if the increment is on the rightmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # down right check
        while True:
            inc = inc + 9
            if inc >= 0 and inc <= 63 and not (inc in [0, 8, 16, 24, 32, 40, 48, 56]) and board[inc] % 10 != board[
                position] % 10:
                # if the increment is on the leftmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # up left check
        while True:
            inc = inc - 9
            if inc >= 0 and inc <= 63 and not (inc in [7, 15, 23, 31, 39, 47, 55, 63]) and board[inc] % 10 != board[
                position] % 10:
                # if the increment is on the rightmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # up right check
        while True:
            inc = inc - 7
            if inc >= 0 and inc <= 63 and not (inc in [0, 8, 16, 24, 32, 40, 48, 56]) and board[inc] % 10 != board[
                position] % 10:
                # if the increment is on the leftmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position

        # horizontal starts here
        # down check
        while True:
            inc = inc + 8
            if inc <= 63 and board[inc] % 10 != board[position] % 10:
                # overflows are when over 63
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # up check
        while True:
            inc = inc - 8
            if inc >= 0 and board[inc] % 10 != board[position] % 10:
                # overflows are when under 0
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # left check
        while True:
            inc = inc - 1
            if inc >= 0 and not (inc in [7, 15, 23, 31, 39, 47, 55, 63]) and board[inc] % 10 != board[position] % 10:
                # if the increment is on the rightmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
        inc = position
        # right check
        while True:
            inc = inc + 1
            if inc <= 63 and not (inc in [0, 8, 16, 24, 32, 40, 48, 56]) and board[inc] % 10 != board[position] % 10:
                # if the increment is on the leftmost edge, it has overflowed to the next line
                legal = legal + [inc]
                if board[inc] >= 10:
                    break
            else:
                break
    # king check
    elif piece == 80 or piece == 81:
        u = position - 8
        d = position + 8
        l = position - 1
        r = position + 1

        ul = position - 9
        ur = position - 7
        dl = position + 7
        dr = position + 9

        # each of these values corresponds to a specific possible position a knight can take. u means up, d means down,
        # r means right, and l means left.
        opt = [u, d, l, r, ul, ur, dl, dr]
        for o in opt:
            if o >= 0 and o <= 63:
                if not (position in [7, 15, 23, 31, 39, 47, 55, 63] and o in [r, ur, dr]):
                    # this refers to the rightmost edge of the board
                    if not (position in [0, 8, 16, 24, 32, 40, 48, 56] and o in [l, ul, dl]):
                        # this refers to the leftmost edge of the board
                        if board[o] % 10 != board[position] % 10:
                            # check if occupied space is same colour or not
                            legal = legal + [o]

    if not pin:
        # this makes hypothetical board for every possible move a piece can make
        # if the resulting move causes a check for the friendly king, it is removed
        # from the legal moves
        # check which colour is playing for king check
        if board[position] % 10 == 0:
            player = 20
        else:
            player = 10
        legal2 = []
        for i in legal:
            legal2 = legal2 + [i]
        for move in legal2:
            newboard = list(board)
            newboard[position] = 2
            newboard[move] = board[position]
            # this finds where the friendly king is in the potential board
            if player == 20:
                king = newboard.index(80)
            else:
                king = newboard.index(81)

            if IsPositionUnderThreat(newboard, king, player):
                legal.remove(move)
        # remember to check if resulting moves cause check of the same colour!
    return legal

def IsPositionUnderThreat(board, position, player):
    enemy_legal = []
    if player == 10:
        enemy = 20
    else:
        enemy = 10
    enemy_pieces = GetPlayerPositions(board, enemy)
    for p in range(0, len(enemy_pieces)):
        enemy_legal = enemy_legal + GetPieceLegalMoves(board, enemy_pieces[p], 1)
    if position in enemy_legal:
        return True
    else:
        return False

def printPos(board):
    pboard = ["","","","","","","",""]
    pieces = {10:"bP|",11:"wP|",20:"bN|",21:"wN|",30:"bB|",31:"wB|",50:"bR|",51:"wR|",90:"bQ|",91:"wQ|",80:"bK|",81:"wK|"}
    for i in range(0,8):
        if board[i] in pieces:
            pboard[0] = pboard[0] + pieces[board[i]]
        else:
            if i%2 == 0:
                pboard[0] = pboard[0] + "# |"
            else:
                pboard[0] = pboard[0] + "_ |"
    for i in range(8,16):
        if board[i] in pieces:
            pboard[1] = pboard[1] + pieces[board[i]]
        else:
            if i%2 == 1:
                pboard[1] = pboard[1] + "# |"
            else:
                pboard[1] = pboard[1] + "_ |"
    for i in range(16,24):
        if board[i] in pieces:
            pboard[2] = pboard[2] + pieces[board[i]]
        else:
            if i%2 == 0:
                pboard[2] = pboard[2] + "# |"
            else:
                pboard[2] = pboard[2] + "_ |"
    for i in range(24,32):
        if board[i] in pieces:
            pboard[3] = pboard[3] + pieces[board[i]]
        else:
            if i%2 == 1:
                pboard[3] = pboard[3] + "# |"
            else:
                pboard[3] = pboard[3] + "_ |"
    for i in range(32,40):
        if board[i] in pieces:
            pboard[4] = pboard[4] + pieces[board[i]]
        else:
            if i%2 == 0:
                pboard[4] = pboard[4] + "# |"
            else:
                pboard[4] = pboard[4] + "_ |"
    for i in range(40,48):
        if board[i] in pieces:
            pboard[5] = pboard[5] + pieces[board[i]]
        else:
            if i%2 == 1:
                pboard[5] = pboard[5] + "# |"
            else:
                pboard[5] = pboard[5] + "_ |"
    for i in range(48,56):
        if board[i] in pieces:
            pboard[6] = pboard[6] + pieces[board[i]]
        else:
            if i%2 == 0:
                pboard[6] = pboard[6] + "# |"
            else:
                pboard[6] = pboard[6] + "_ |"
    for i in range(56,64):
        if board[i] in pieces:
            pboard[7] = pboard[7] + pieces[board[i]]
        else:
            if i%2 == 1:
                pboard[7] = pboard[7] + "# |"
            else:
                pboard[7] = pboard[7] + "_ |"
    print("  a  b  c  d  e  f  g  h")
    inc = 8
    for row in pboard:
        print(str(inc),row)
        inc = inc-1
    return True

def getLevelOrder(root):
    ret = []
    c = queue()
    c.enqueue(root)
    while len(c.store) > 0:
        x = c.dequeue()
        ret = ret + [x.board]
        for i in x.nodes:
            c.enqueue(i)
    return ret

def chessPlayer(board, player):

    new = []
    dict = {2:2,10:10,20:11,30:12,50:13,80:14,90:15,11:20,21:21,31:22,51:23,81:24,91:25}
    for i in range(63, -1, -1):
        piece = dict[board[i]]
        new = new + [piece]

    ai = AI(player, board)
    ai.initMoves()
    board = ai.getmove()
    x = getLevelOrder(ai.moves)
    return(True,board[0],board[1], x)
