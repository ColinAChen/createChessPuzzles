import random
import numpy as np
import cv2

def visualizeBoard(board):
	# create an image of the board
	pass

def boardToString(board):
	#print(board)
	boardString = ''
	for row in board:
		rowString = ''
		for square in row:
			if square == 0:
				rowString += '*'
			else:
				rowString += square
		boardString += rowString
		boardString += '\n'
	return boardString