WHITE = 1
BLACK = 0

PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

WHITE_PIECES_V = {
	1: 'P',
	2: 'N',
	3: 'B',
	4: 'R',
	5: 'Q',
	6: 'K'
}
BLACK_PIECES_V = {
	1: 'p',
	2: 'n',
	3: 'b',
	4: 'r',
	5: 'q',
	6: 'k'
}


WHITE_PIECES_TENSOR = {
	1: 10,
	2: 20,
	3: 30,
	4: 40,
	5: 50,
	6: 60
}
BLACK_PIECES_TENSOR = {
	1: 70,
	2: 80,
	3: 90,
	4: 100,
	5: 110,
	6: 120
}

def getLegalMoves(piece, position, color=WHITE):
	if piece == PAWN:
		pass
	elif piece == KNIGHT:
		return getKnightMoves(position)
	elif piece == BISHOP:
		return getBishopMoves(position)
	elif piece == ROOK:
		return getRookMoves(position)
	elif piece == QUEEN:
		rookMoves = getRookMoves(position)
		bishopMoves = getBishopMoves(position)
		return rookMoves.extend(bishopMoves)
	elif piece == KING:
		return getKingMoves

def getPawnMoves(position, color):
	pass
'''
Get the positions the knight can theoretically move to on an empty board
'''
def getKnightMoves(position):
	row, col = position
	checkList = [(-2,-1), (-2,1),
				 (-1,-2), (-1,2),
				 (1,-2),  (1,2),
				 (2,-1),  (2,1)]
	retList = []
	for check in checkList:
		addRow, addCol = check
		if (row + addRow >= 0 and row + addRow < 8
			and col + addCol >= 0 and col + addCol < 8):
			retList.append((row+addRow, col+addCol))
	return retList

'''
Get the positions the bishop can theoretically move to on an empty board
0 . . 8
.
.
8
'''
def getBishopMoves(position):
	row, col = position
	moveList = []
	# up left
	while (row >= 0 and col < 8):
		moveList.append((row-1, col+1))
	# up right
	while (row >= 0 and col >= 0):
		moveList.append((row-1, col-1))
	# down left
	while (row < 8 and col < 8):
		moveList.append((row+1, col+1))
	# down right
	while(row < 8 and col >= 0):
		moveList.append((row+1, col-1))
	return moveList

def getRookMoves(position):
	row, col = position
	moveList = []
	# up
	while (row >= 0):
		moveList.append((row-1, col))
	# down
	while (row < 8):
		moveList.append((row+1, col))
	# left
	while (col >= 0):
		moveList.append((row, col-1))
	# right
	while (col < 8):
		moveList.append((row, col+1))
	return moveList

def getKingMoves(position):
	row, col = position
	moveList = []
	checkList = [(-1, -1), (-1, 0), (-1, 1),
				 ( 0, -1),          ( 0, 1),
				 ( 1, -1), ( 1, 0), ( 1, 1)]
	for check in checkList:
		addRow, addCol = check
		if (row + addRow >= 0 and row + addRow < 8
			and col + addCol >= 0 and col + addCol < 8):
			moveList.append((row+addRow, col+addCol))
	return moveList