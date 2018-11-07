import numpy as np
import random

def rowadder(l):
  if l[0]==0:
    if sum(l)>0:
      new_l = [i for i in l[1:]]
      new_l.append(0)
      return rowadder(new_l)
    else:
      return [0] * len(l)
  else:
    for i in range(len(l)):
      for j in range(i+1, len(l)):
        if l[i]==l[j] and sum(l[i+1:j])==0:
          l[i] *= 2
          l[j] = 0
          i = j
    l_new = [element for element in l if element != 0]
    for n in range(len(l) - len(l_new)):
      l_new.append(0)
    return l_new

def boardadder(b):
  new_board = [rowadder(i) for i in b]
  return new_board

def shiftleft(b):
 return boardadder(b)

def flipright(b):
  b_flipped0 = [list(reversed(i)) for i in b]
  return b_flipped0

def shiftright(b):
  flipped_right = flipright(b)
  shifted=shiftleft(flipped_right)
  return flipright(shifted)

def rotleft(b):
  return np.rot90(b,1,(0,1)).tolist()

def rotright(b):
  return np.rot90(b,1,(1,0)).tolist()

def shiftup(b):
  rotated_left=rotleft(b)
  shifted_left=shiftleft(rotated_left)
  return rotright(shifted_left)

def shiftdown(b):
  flipped_down=rotright(b)
  shifted_left=shiftleft(flipped_down)
  return rotleft(shifted_left)

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
  for i in b:
    print(i)

def new_elements(b):
  b = np.array(b)
  num_add = min(random.randint(min(int(0.0625 * b.size),1),
    int(0.125 * b.size)),
   b.size - np.count_nonzero(b))
  n = 0
  while n < num_add:
    added = False
    while added == False:
      i = random.randint(0,len(b)-1)
      j = random.randint(0,len(b[i])-1)
      if b[i,j] == 0:
        b[i,j] = 2 * random.randint(1,2)
        added = True
        n += 1
  return b.tolist()

def game_human(n):
  board = new_elements([[0] * n] * n)
  Turn = 1
  while np.count_nonzero(board) != np.size(board) or shiftup(board) != board or shiftdown(board) != board or shiftleft(board) != board or shiftright(board) != board:
    print('Turn:', Turn, '    |   Score:', sum(sum(np.array(board))),'    |   Highest Tile:',max(np.array(board).reshape(np.size(board))), '\n')
    display(board)
    print()
    new_board = shift(board)
    if new_board == board:
      print('\n')
      for i in range(3):
        print('Invalid move!')
      print('\n')
    else:
      board=new_elements(new_board)
      Turn += 1
      print('\n' * 2)
  print('Game over!','\n')
  display(board)
  print()
  print('Score:', sum(sum(np.array(board))),'    |   Highest Tile:',np.amax(board),'    |   Turns taken:', Turn)

#game_human(10)