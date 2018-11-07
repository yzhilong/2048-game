import numpy as np
import tensorflow as tf
import scipy.optimize as opt
import NxN_2048 as game
import pickle, os, time

def gamestart(n):
	return game.new_elements([[0] * n] * n)

def activation(weight, input_layer):
	matmul = np.matmul(weight, input_layer)
	pos = 1 * (matmul > 0)
	neg = 0.1 * (matmul <= 0)
	return (pos + neg) * matmul + 1

def NN_move(board,w1,w2,w3):
	flat_board = np.array(board).flatten().astype(np.float32) #flat_board has size (n**2, 1)
	h1 = activation(w1, flat_board) #h1 has shape (n, 1)
	#print(h1.shape)
	h2 = activation(w2, h1) #h2 has shape (2*n, 1)
	#print(h2.shape)
	h3 = activation(w3, h2) #h3 has shape (4, 1)
	#print(h3.shape)
	move_func = [game.shiftup,game.shiftdown,game.shiftleft,game.shiftright]
	while True:
		if move_func[np.argmax(h3)](board) != board:
			l = ['up','down','left','right']
			#print(l[np.argmax(h3)])
			return move_func[np.argmax(h3)](board)
		else:
			h3[np.argmax(h3)] = np.NINF

def NN_game(w1,w2,w3):
	board = gamestart(4)
	while game.shiftup(board)!=board or game.shiftdown(board)!=board or game.shiftleft(board)!=board or game.shiftright(board)!=board:
		board = NN_move(board,w1,w2,w3)
		board = game.new_elements(board)
	score = sum(sum(np.array(board)))
	return score

def NN_game_packed_args(args):
	return NN_game(args[0], args[1], args[2])

def NN_train():
	n = 4
	w1 = np.random.randn(n, n**2)
	w2 = np.random.randn(2*n, n)
	w3 = np.random.randn(4, 2*n)
	lambda_ = 10

	#game_score = NN_game_packed_args([w1,w2,w3])
	#print(game_score)

	def cross_entropy(args):
		game_score = NN_game_packed_args(args)
		return game_score + lambda_ * (sum(sum(args[0])) + sum(sum(args[1])) + sum(sum(args[2])))

	for i in range(10000):
		results = opt.minimize(cross_entropy, (w1,w2,w3) , method='BFGS')
		print(results.x[0].shape, results.x[1].shape, results.x[2].shape)
		w1,w2,w3 = results.x[0],results.x[1],results.x[2]
		if i % 1 == 0:
			print('Epoch:', str(i),'		|		Current scoring:', str(NN_game_packed_args((w1,w2,w3))))

	return w1,w2,w3

NN_train()