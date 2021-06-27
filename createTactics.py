from util import *
from engine import *

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
def createRookSkewer(visualize=False):
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

	board[kingRow][kingCol] = BLACK_PIECES_V[KING] if visualize else BLACK_PIECES_TENSOR[KING]
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
	board[pieceRow][pieceCol] = BLACK_PIECES_V[random.choice(piecesToWin)] if visualize else BLACK_PIECES_TENSOR[random.choice(piecesToWin)]

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
	board[rookRow][rookCol] = WHITE_PIECES_V[ROOK] if visualize else WHITE_PIECES_TENSOR[ROOK]
	#print('rook at ', (rookRow, rookCol))
	#print(board)
	#print(boardToString(board))
	return board if visualize else torch.tensor(board)

'''
Create a knight for such that white forks the king and another piece to win material
1. Choose a final position for the white knight
2. Choose a position for the black king from possible knight moves
3. Choose a position for the black piece from remaining possible knight moves
4. Choose a position for the white knight to start at remaining possible knight moves

'''
def createKnightKingFork(visualize=False):
	# cannot fork in the corer because there are only two possible knight moves
	# all other squares are valid
	board = []
	for i in range(8):
		board.append([0] * 8)
	# 1. Choose a final position for the white knight
	noKnight = [(0,0), (0,7),
				(7,0), (7,7)]
	knightRow = random.randint(0,7)
	knightCol = random.randint(0,7)
	while (knightRow, knightCol) in noKnight:
	#while len(getLegalMoves(KNIGHT,(knightRow, knightCol)) < 3):
		knightRow = random.randint(0,7)
		knightCol = random.randint(0,7)
	#print('knight ends at: ', (knightRow, knightCol))

	# 2. Choose a position for the black king from possible knight moves
	knightMoves = getLegalMoves(KNIGHT, (knightRow, knightCol))
	#print('knightMoves start at: ', knightMoves)
	kingPos = kingRow, kingCol = random.choice(knightMoves)
	# remove the king pos from the possible moves
	knightMoves.remove(kingPos)
	board[kingRow][kingCol] = BLACK_PIECES_V[KING] if visualize else BLACK_PIECES_TENSOR[KING]
	#print('king at: ', (kingRow, kingCol))
	#print('knightMoves: ', knightMoves)
	# 3. Choose a position for the black piece from remaining possible knight moves
	piecePos = pieceRow, pieceCol = random.choice(knightMoves)
	knightMoves.remove(piecePos)
	board[pieceRow][pieceCol] = BLACK_PIECES_V[random.choice((ROOK, QUEEN))] if visualize else BLACK_PIECES_TENSOR[random.choice((ROOK, QUEEN))]
	#print('piece at: ', (pieceRow, pieceCol))
	#print('knightMoves: ', knightMoves)
	#4. Choose a position for the white knight to start at remaining possible knight moves
	knightRow, knightCol = random.choice(knightMoves)
	board[knightRow][knightCol] = WHITE_PIECES_V[KNIGHT] if visualize else WHITE_PIECES_TENSOR[KNIGHT]
	#print('knight at: ', (knightRow, knightCol))
	#print(boardToString(board))
	return board if visualize else torch.tensor(board)
#for i in range(10):

#createRookSkewer()
#print(verifyKnightKingFork(createKnightKingFork()))
