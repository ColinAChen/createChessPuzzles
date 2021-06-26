from util import *

WHITE = 1
BLACK = 0

PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

WHITE_PIECES = {
	1: 'P',
	2: 'N',
	3: 'B',
	4: 'R',
	5: 'Q',
	6: 'K'
}
BLACK_PIECES = {
	1: 'p',
	2: 'n',
	3: 'b',
	4: 'r',
	5: 'q',
	6: 'k'
}
random.seed(42069)


'''
Rook skewers king to win material without recapturing the rook

1. Choose a random position for the king such that it won't be able to defend the piece after check
2. Choose a random piece on a random axis for the king
3. Choose a ranom place for the rook on the otherside of the king

No skewer is possible when king on x

x x 0 0 0 0 0 0 x x
x x 0 0 0 0 0 0 x x
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
x x 0 0 0 0 0 0 x x
x x 0 0 0 0 0 0 x x

'''
def createRookSkewer():
	#board = np.zeros((8,8))
	board = []
	for i in range(8):
		board.append([0] * 8)
	#print(board)
	# choose a random position for the king
	kingRow = random.randint(0,7)
	kingCol = random.randint(0,7)

	noKing = [(0,0), (0,1), (0,7), (0,8),
			  (1,0), (1,1), (1,7), (1,8),
			  (7,0), (7,1), (7,7), (7,8),
			  (8,0), (8,1), (8,7), (8,8)]
	# no skewer is possible while the king is in the corner
	while (kingRow, kingCol) in noKing:
		kingRow = random.randint(0,8)
		kingCol = random.randint(0,8)

	board[kingRow][kingCol] = BLACK_PIECES[KING]
	#print('king at: ', (kingRow, kingCol))
	#print(board)
	# choose a random piece aligned with the king on a random axis
	# the piece must not be defendable by the king in the next move
	# the piece must allow room for the rook to move on the other side of the king
	pieceCandidates = []
	if kingRow < 6:
		# above the king
		for row in range(0,kingRow-2):
			pieceCandidates.append((row, kingCol))
	if kingRow > 1:
		# below the king
		for row in range(kingRow+3, 8):
			pieceCandidates.append((row, kingCol))
	if kingCol < 6:
		# to the left of the king
		for col in range(0,kingCol-2):
			pieceCandidates.append((kingRow, col))
	if kingCol > 1:
		# to the right of the king
		for col in range(kingCol+3, 8):
			pieceCandidates.append((kingRow, col))
	pieceRow, pieceCol = random.choice(pieceCandidates)

	#print('piece candiates are', pieceCandidates)
	#print('piece at: ', (pieceRow, pieceCol))

	piecesToWin = [KNIGHT, BISHOP, ROOK, QUEEN]
	board[pieceRow][pieceCol] = BLACK_PIECES[random.choice(piecesToWin)]

	# choose a random square to place the rook
	# the rook must be on the opposite side of the piece from the king and cannot be capturable

	rookCandidates = []
	bounds = None
	if kingRow == pieceRow:
		# king and piece are on the same row
		if kingCol < pieceCol:
			# rook must be placed before teh king
			bounds = range(0,kingCol-1)
		else:
			# rook must be placed after the king
			bounds = range(kingCol+2, 8)
		for col in bounds:
				for row in range(0,8):
					if row != kingRow:
						rookCandidates.append((row, col))
	else:
		#king and piece are on the same col
		if kingRow < pieceRow:
			bounds = range(0, kingRow-1)
		else:
			bounds = range(kingRow+2, 8)
		for row in bounds:
				for col in range(0,8):
					if col != kingCol:
						rookCandidates.append((row, col))
	#print('rook candidates are: ', rookCandidates)
	rookRow, rookCol = random.choice(rookCandidates)
	board[rookRow][rookCol] = WHITE_PIECES[ROOK]
	#print('rook at ', (rookRow, rookCol))
	#print(board)
	#print(boardToString(board))
	return board

'''
Create a knight for such that white forks the king and another piece to win material
1. Choose a final position for the white knight
2. Choose a position for the black king from possible knight moves
3. Choose a position for the black piece from remaining possible knight moves
4. Choose a position for the white knight to start at remaining possible knight moves

'''
def createKnightKingFork():
	# cannot fork in the corer because there are only two possible knight moves
	# all other squares are valid
	board = []
	for i in range(8):
		board.append([0] * 8)
	# 1. Choose a final position for the white knight
	noKnight = [(0,0), (0,8),
				(8,0), (8,8)]
	knightRow = random.randint(0,7)
	knightCol = random.randint(0,7)
	while (knightRow, knightCol) in noKnight:
		knightRow = random.randint(0,7)
		knightCol = random.randint(0,7)
	print('knight ends at: ', (knightRow, knightCol))

	# 2. Choose a position for the black king from possible knight moves
	knightMoves = getLegalMoves(KNIGHT, (knightRow, knightCol))
	print('knightMoves start at: ', knightMoves)
	kingPos = kingRow, kingCol = random.choice(knightMoves)
	# remove the king pos from the possible moves
	knightMoves.remove(kingPos)
	board[kingRow][kingCol] = BLACK_PIECES[KING]
	print('king at: ', (kingRow, kingCol))
	print('knightMoves: ', knightMoves)
	# 3. Choose a position for the black piece from remaining possible knight moves
	piecePos = pieceRow, pieceCol = random.choice(knightMoves)
	knightMoves.remove(piecePos)
	board[pieceRow][pieceCol] = BLACK_PIECES[random.choice((ROOK, QUEEN))]
	print('piece at: ', (pieceRow, pieceCol))
	print('knightMoves: ', knightMoves)
	#4. Choose a position for the white knight to start at remaining possible knight moves
	knightRow, knightCol = random.choice(knightMoves)
	board[knightRow][knightCol] = WHITE_PIECES[KNIGHT]
	print('knight at: ', (knightRow, knightCol))
	print(boardToString(board))
	return board
'''
To verify
The knight must be able to move to a position such that the king and piece are both attacked
'''
def verifyKnightKingFork(board):
	# retrieve the positions of each piece
	knightPos = (-1,-1)
	kingPos = (-1,-1)
	piecePos = (-1,-1)
	for i,row in enumerate(board):
		try:
			knightIndex = row.index(WHITE_PIECES[KNIGHT])
		except:
			knightIndex = -1
		try:
			kingIndex = row.index(BLACK_PIECES[KING])
		except:
			kingIndex = -1
		try:
			rookIndex = row.index(BLACK_PIECES[ROOK])
		except:
			rookIndex = -1
		try:
			queenIndex = row.index(BLACK_PIECES[QUEEN])
		except:
			queenIndex = -1
		if knightIndex != -1:
			knightPos = (i, knightIndex)
		if kingIndex != -1:
			kingPos = (i, kingIndex)
		if rookIndex != -1:
			piecePos = (i, rookIndex)
		if queenIndex != -1:
			piecePos = (i, queenIndex)
	if knightPos == (-1,-1) or kingPos == (-1,-1) or piecePos == (-1,-1):
		return False
	#print(knightPos, kingPos, piecePos)
	# check each knight move
	for move in getLegalMoves(KNIGHT, knightPos):
		#print(move)
		checkMoves = getKnightMoves(move)
		if kingPos in checkMoves and piecePos in checkMoves:
			return True
	return False
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
#for i in range(10):

#createRookSkewer()
#print(verifyKnightKingFork(createKnightKingFork()))

	

