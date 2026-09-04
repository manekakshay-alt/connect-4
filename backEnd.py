from random import randint
from botFunctions1.py import *#;
from botFuncitons2.py import *#;
Board=[["N","N","N","N","N","N"],
       ["N","N","N","N","N","N"],
       ["N","N","N","N","N","N"],
       ["N","N","N","N","N","N"],
       ["N","N","N","N","N","N"],
       ["N","N","N","N","N","N"],
       ["N","N","N","N","N","N"]]


def getBoard():
       dataStore = Board#;
       boardState = []#;
       # for each column in Board, add the reverse to boardState;
       for column in dataStore:
              # reverse the column;
              column.reverse()
              # add the revesed list;
              boardState.append(column)#;
       #ENDFOR
       # return;
       return boardState#;
#ENDMETHOD
       
def isTie(board):
  NopTie=False
  for row in board:
    for i in row:
      if i=="N":
        NopTie=True
  return NopTie


def movePossible(move,board):
  check=0
  # convert move to index format;
  move = move-1#;
  for i in board[move]:
    if i=="R" or i=="Y":
      check=check+1
  if check>=6:
    return False
  else:
    return True

def redMove(column,board):
  # convert move to index format;
  column = column-1#;
  for i in range(5, -1, -1):
         if board[column][i]=="N":
                board[column][i]="R"
                return board
  return board 
        
def yellowMove(column,board):
  # convert move to index format;
  column = column-1#;
  for i in range(5, -1, -1):
         if board[column][i]=="N":
                board[column][i]="Y"
                return board
  return board 

def column4inaRow(board):
  for column in board:
    red=0
    yellow=0
    winner=0
    for i in column:
       if i=="R":
         red=red+1
         yellow=0
       elif i=="Y":
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
      if columns[i]=="R":
        red=red+1
        yellow=0
      elif columns[i]=="Y":
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
      if board[c][r] == "R" and board[c+1][r+1] == "R" and board[c+2][r+2] == "R" and board[c+3][r+3] == "R":
        return "RED"
      elif board[c][r] == "Y" and board[c+1][r+1] == "Y" and board[c+2][r+2] == "Y" and board[c+3][r+3] == "Y":
        return "YELLOW"

  for c in range(4):
    for r in range(3, 6):
      if board[c][r] == "R" and board[c+1][r-1] == "R" and board[c+2][r-2] == "R" and board[c+3][r-3] == "R":
        return "RED"
      elif board[c][r] == "Y" and board[c+1][r-1] == "Y" and board[c+2][r-2] == "Y" and board[c+3][r-3] == "Y":
        return "YELLOW"

  return 0

      
def win():
  if row4inaRow(Board)=="RED" or  column4inaRow(Board)=="RED" or diagonal4inaRow(Board)=="RED":
    return True
  elif row4inaRow(Board)=="YELLOW" or  column4inaRow(Board)=="YELLOW" or diagonal4inaRow=="YELLOW":
    return True
  else:
    return False 

def BotMove():
       # get the botMove;
       move:int#;
       strength:float#;
       move,strength=botMove(getBoard(),4,"Y");
       # if the move isn't legal or the strength is 0;
       if movePossible(choice,Board)==False or strength=0.0:
              legality=False
              while legality!=True:
                     move=randint(1,7)
                     if movePossible(move,Board)==True:
                            legality=True
                     #ENDIF
              #ENDWHILE
       #ENDIF
       return move#;
#ENDMETHOD
  
def clear(board):
  for c in range(len(board)):
    for r in range (len(board[c])):
      board[c][r]="N"
  return board
