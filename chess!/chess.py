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