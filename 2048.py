import numpy as np
import random

def rowadder(l):
 if l[0]==0:
  if sum(l)>0:
   return rowadder((l[1],l[2],0))
  else:
   return [0,0,0]
 else:
  if l[0]==l[1]:
   return [2*l[0],l[2],0]
  elif l[1]==l[2]:
   return [l[0],2*l[1],0]
  elif l[0]==l[2] and l[1]==0:
   return [2*l[0],0,0]
  elif l[0]!=l[2] and l[1]==0:
   return [l[0],l[2],0]
  else:
   return l

def boardadder(b):
 return [rowadder(b[0]),rowadder(b[1]),rowadder(b[2])]

def shiftleft(b):
 return boardadder(b)

def flipright(b):
 row0 = list(reversed(b[0]))
 row1 = list(reversed(b[1]))
 row2 = list(reversed(b[2]))
 b_flipped0 = [row0,row1,row2]
 return b_flipped0

def shiftright(b):
  flipped_right = flipright(b)
  shifted=shiftleft(flipped_right)
  return flipright(shifted)

def flipup(b):
  return np.rot90(b,1,(0,1)).tolist()

def flipdown(b):
  return np.rot90(b,1,(1,0)).tolist()

def shiftup(b):
  flipped_up=flipup(b)
  shifted_up=shiftleft(flipped_up)
  return flipdown(shifted_up)

def shiftdown(b):
  flipped_down=flipdown(b)
  shifted_down=shiftleft(flipped_down)
  return flipup(shifted_down)

def shift(b):
  movement=input('Use WASD to move: ').lower()
  moves = ['w','a','s','d']
  move_func = (shiftup, shiftleft,shiftdown,shiftright)
  if movement not in moves:
    print('Only WASD allowed as input!')
    shift(b)
  else:
    return move_func[moves.index(movement)](b)

def display(b):
  print(b[0])
  print(b[1])
  print(b[2])

def new_elements(b):
  num_add = min(random.randint(1,2), np.size(b) - np.count_nonzero(b))
  n = 0
  while n < num_add:
    added = False
    while added == False:
      i = random.randint(0,2)
      j = random.randint(0,2)
      if b[i][j] == 0:
        b[i][j] += 2 * random.randint(1,2)
        added = True
        n += 1
  return b

def game():
  board = new_elements([[0,0,0],[0,0,0],[0,0,0]])
  Turn = 1
  while np.count_nonzero(board) != np.size(board) or shiftup(board) != board or shiftdown(board) != board or shiftleft(board) != board or shiftright(board) != board:
    print('Turn:', Turn, '    |   Score:', sum(sum(np.array(board))),'    |   Highest Tile:',max(np.array(board).reshape(np.size(board))), '\n')
    display(board)
    print()
    new_board = shift(board)
    if new_board == board:
      print('Invalid move!')
    else:
      board=new_elements(new_board)
      Turn += 1
      print('\n' * 2)
  print('Game over!','\n')
  display(board)
  print()
  print('Score:', sum(sum(np.array(board))),'    |   Highest Tile:',max(np.array(board).reshape(np.size(board))),'    |   Turns taken:', Turn)

game()