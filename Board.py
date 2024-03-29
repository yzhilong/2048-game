import random
import numpy as np

class Board:
	def __init__(self, nrows, ncols, random_seed=42):
		self.nrows = nrows
		self.ncols = ncols
		self.random = random.Random()
		self.random.seed(random_seed)
		self.board = np.zeros((nrows, ncols))
		self.score = 0

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
		collapsed = False
		for i in range(self.ncols):
			if self.board[row_index, i] != 0:
				if left_index != i:
					collapsed = True
				self.__swap_on_board((row_index, left_index), (row_index, i))
				left_index += 1

		for i in range(1, self.ncols):
			if self.board[row_index, i] == self.board[row_index, i-1]:
				self.board[row_index, i-1] *= 2
				self.board[row_index, i] = 0
				collapsed = True
				self.score += self.board[row_index, i-1]

		left_index = 0
		for i in range(self.ncols):
			if self.board[row_index, i] != 0:
				self.__swap_on_board((row_index, left_index), (row_index, i))
				left_index += 1

		return collapsed

	def __up_swipe_on_col(self, col_index):
		top_index = 0
		collapsed = False
		for i in range(self.nrows):
			if self.board[i, col_index] != 0:
				if top_index != i:
					collapsed = True
				self.__swap_on_board((top_index, col_index), (i, col_index))
				top_index += 1

		for i in range(1, self.nrows):
			if self.board[i, col_index] == self.board[i-1, col_index]:
				self.board[i-1, col_index] *= 2
				self.board[i, col_index] = 0
				collapsed = True
				self.score += self.board[i-1, col_index]

		top_index = 0
		for i in range(self.nrows):
			if self.board[i, col_index] != 0:
				self.__swap_on_board((top_index, col_index), (i, col_index))
				top_index += 1

		return collapsed

	def __left_swipe(self):
		collapsed = False
		for i in range(self.nrows):
			if self.__left_swipe_on_row(i):
				collapsed = True
		return collapsed

	def __right_swipe(self):
		collapsed = False
		for i in range(self.nrows):
			for j in range(self.ncols//2):
				self.__swap_on_board((i, j), (i, -j-1))
			if self.__left_swipe_on_row(i):
				collapsed = True
			for j in range(self.ncols//2):
				self.__swap_on_board((i, j), (i, -j-1))
		return collapsed

	def __up_swipe(self):
		collapsed = False
		for i in range(self.ncols):
			if self.__up_swipe_on_col(i):
				collapsed = True
		return collapsed

	def __down_swipe(self):
		collapsed = False
		for i in range(self.ncols):
			for j in range(self.nrows//2):
				self.__swap_on_board((j, i), (-j-1, i))
			if self.__up_swipe_on_col(i):
				collapsed = True
			for j in range(self.nrows//2):
				self.__swap_on_board((j, i), (-j-1, i))
		return collapsed

	def __display(self):
		print(self.board)
		print(f"Current score: {self.score}")

	def reset(self):
		self.score = 0
		for i in range(self.nrows):
			for j in range(self.ncols):
				self.board[i, j] = 0

	def play(self):
		moves = [self.__up_swipe, self.__left_swipe, self.__down_swipe, self.__right_swipe]
		movement_mapping = {char: moves[pos] for pos, char in enumerate('WASD')}
		board_copy = Board(self.nrows, self.ncols)
		lost = False
		while self.board.max() < 2048:
			self.__display()
			raw_input_value = input("Play with WASD: ").upper()
			while len(raw_input_value) == 0:
				raw_input_value = input("Play with WASD: ").upper()
			direction = raw_input_value[0]
			while direction not in movement_mapping:
				raw_input_value = input("Play with WASD: ").upper()
				while len(raw_input_value) == 0:
					raw_input_value = input("Play with WASD: ").upper()
				direction = raw_input_value[0]
			did_move = movement_mapping[direction]()
			if did_move:
				self.__add_new_numbers()

				# TODO: Make this more efficient
				board_copy.board = self.board.copy()
				can_swipe_up = board_copy.__up_swipe()
				can_swipe_left = board_copy.__left_swipe()
				if not (can_swipe_left or can_swipe_up):
					lost = True
					break
			else:
				print(f"'{direction}'" + ' is an INVALID MOVE')

		if not lost:
			print('GAME WON')
		else:
			print('GAME LOST')
		self.__display()
		output = self.score
		self.reset()
		return output



if __name__ == "__main__":
	b = Board(4, 4)
	b.play()