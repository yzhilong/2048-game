import random
import numpy as np

class Board:
	def __init__(self, nrows, ncols, random_seed=42):
		self.nrows = nrows
		self.ncols = ncols
		self.random = random.Random()
		self.random.seed(random_seed)
		self.board = np.zeros((nrows, ncols))

		self.__add_new_numbers()

	# Initialize with 1/8 of the board filled, with 90% chance of filling
	# with 2, and 10% chance of filling with 4
	def __add_new_numbers(self):

		num_zeros = (self.board == 0).sum()

		for i in range(min((self.nrows*self.ncols)//8, num_zeros)):
			random_row = self.random.randint(0,self.nrows-1)
			random_col = self.random.randint(0,self.ncols-1)
			while self.board[random_row, random_col] != 0:
				random_row = self.random.randint(0,self.nrows-1)
				random_col = self.random.randint(0,self.ncols-1)
			if self.random.random() < 0.9:
				self.board[random_row, random_col] = 2
			else:
				self.board[random_row, random_col] = 4

	def __swap_on_board(self, pos1, pos2):
		val = self.board[pos1]
		self.board[pos1] = self.board[pos2]
		self.board[pos2] = val

	def __left_swipe_on_row(self, row_index):
		left_index = 0
		for i in range(self.ncols):
			if self.board[row_index, i] != 0:
				self.__swap_on_board((row_index, left_index), (row_index, i))
				left_index += 1

		return left_index == self.ncols -1

	def __up_swipe_on_col(self, col_index):
		top_index = 0
		for i in range(self.nrows):
			if self.board[i, col_index] != 0:
				self.__swap_on_board((i, col_index), (top_index, col_index))
				top_index += 1
		return top_index == self.nrows - 1

	def __left_swipe(self):
		for i in range(self.nrows):
			self.__left_swipe_on_row(i)

	def __right_swipe(self):
		for i in range(self.nrows):
			if self.__left_swipe_on_row(i):
				for j in range(self.ncols//2):
					self.__swap_on_board((i, j), (i, -j-1))

	def __up_swipe(self):
		for i in range(self.ncols):
			self.__up_swipe_on_col(i)

	def __down_swipe(self):
		for i in range(self.ncols):
			if self.__up_swipe_on_col(i):
				for j in range(self.nrows//2):
					self.__swap_on_board((j, i), (-j-1, i))

	def __display(self):
		print(self.board)

	def play(self):
		moves = [self.__up_swipe, self.__left_swipe, self.__down_swipe, self.__right_swipe]
		movement_mapping = {char: moves[pos] for pos, char in enumerate('WASD')}
		while self.board.max() < 2048:
			self.__display()
			movement = movement_mapping[input("Play with WASD: ").upper()[0]]
			movement()
			self.__add_new_numbers()
		print('GAME WON')
		self.__display()





