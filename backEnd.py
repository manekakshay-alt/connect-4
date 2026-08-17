from random import randint
Board=[["n","n","n","n","n","n"],
       ["n","n","n","n","n","n"],
       ["n","n","n","n","n","n"],
       ["n","n","n","n","n","n"],
       ["n","n","n","n","n","n"],
       ["n","n","n","n","n","n"],
       ["n","n","n","n","n","n"]]



def isTie(board):
  NopTie=0
  for row in board:
    for i in row:
      if i=="n":
        NopTie=1
  return NopTie



def movePossible(move,board):
  check=0
  for i in board[move]:
    if i=="r" or i=="y":
      check=check+1
  if check>=6:
    return False
  else:
    return True

def redmove(column,board):
  for i in range(5, -1, -1):
    if movePossible(column,board)==True:
      if board[column][i]=="n":
        board[column][i]="r"
        return board 
        break
        
def yellowmove(column,board):
  for i in range(5, -1, -1):
    if movePossible(column,board)==True:
      if board[column][i]=="n":
        board[column][i]="y"
        return board 
        break

def column4inaRow(board):
  for column in board:
    red=0
    yellow=0
    winner=0
    for i in column:
       if i=="r":
         red=red+1
         yellow=0
       elif i=="y":
         yellow=yellow+1
         red=0
       else:
         red=0
         yellow=0
       if red==4:
         winner="RED"
         return winner
       elif yellow==4:
         winner="YELLOW"
         return winner

def row4inaRow(board):
  for i in range(6):
    red=0
    yellow=0
    winner=0
    for columns in board:
      if columns[i]=="r":
        red=red+1
        yellow=0
      elif columns[i]=="y":
        yellow=yellow+1
        red=0
      else:
        yellow=0
        red=0
      if red==4:
        winner="RED"
        return winner
      elif yellow==4:
        winner="YELLOW"
        return winner
        
def diagonal4inaRow(board):
  for c in range(4):
    for r in range(3):
      if board[c][r] == "r" and board[c+1][r+1] == "r" and board[c+2][r+2] == "r" and board[c+3][r+3] == "r":
        return "RED"
      elif board[c][r] == "y" and board[c+1][r+1] == "y" and board[c+2][r+2] == "y" and board[c+3][r+3] == "y":
        return "YELLOW"

  for c in range(4):
    for r in range(3, 6):
      if board[c][r] == "r" and board[c+1][r-1] == "r" and board[c+2][r-2] == "r" and board[c+3][r-3] == "r":
        return "RED"
      elif board[c][r] == "y" and board[c+1][r-1] == "y" and board[c+2][r-2] == "y" and board[c+3][r-3] == "y":
        return "YELLOW"

  return 0

      
def win():
  victory=0
  if row4inaRow(Board)=="RED" or  column4inaRow(Board)=="RED" or diagonal4inaRow(Board)=="RED":
    victory="RED"
    return victory
  elif row4inaRow(Board)=="YELLOW" or  column4inaRow(Board)=="YELLOW" or diagonal4inaRow=="YELLOW":
    victory="YELLOW"
    return victory
  else:
    return victory 

def BotMove():
  legality=False
  while legality!=True:
    choice=randint(0,6)
    if movePossible(choice,Board)==True:
      legality=True
  yellowmove(choice,Board)
  column4inaRow(Board)
  
def clear(board):
  for c in range(len(board)):
    for r in range (len(board[c])):
      board[c][r]="n"
  return board
