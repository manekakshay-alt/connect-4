
from random import randint

Board = [
    ["N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N"],
    ["N", "N", "N", "N", "N", "N"],
]

def getBoard():
    # create a temporary board;
    temp = []#;
    # for each column in the current board;
    for column in Board:
        temp.append(column.reverse())#;
    #ENDFOR

    return temp#;
#ENDMETHOD

def isTie(board):
  NopTie = False
  for row in board:
    for i in row:
      if i == "N":
        NopTie = True
  return NopTie


def movePossible(move, board):
  check = 0
  for i in board[move]:
    if i == "R" or i == "Y":
      check = check + 1
  if check >= 6:
    return False
  else:
    return True


def redmove(column, board):
  for i in range(5, -1, -1):
    if movePossible(column, board) == True:
      if board[column][i] == "N":
        board[column][i] = "R"
        return board
        break


def yellowmove(column, board):
  for i in range(5, -1, -1):
    if movePossible(column, board) == True:
      if board[column][i] == "N":
        board[column][i] = "Y"
        return board
        break


def column4inaRow(board):
  for column in board:
    red = 0
    yellow = 0
    winner = 0
    for i in column:
      if i == "R":
        red = red + 1
        yellow = 0
      elif i == "Y":
        yellow = yellow + 1
        red = 0
      else:
        red = 0
        yellow = 0
      if red == 4:
        winner = "RED"
        return winner
      elif yellow == 4:
        winner = "YELLOW"
        return winner


def row4inaRow(board):
  for i in range(7):
    print("ye")


def BotMove():
  legality = False
  while legality != True:
    choice = randint(0, 6)
    if movePossible(choice, Board) == True:
      legality = True
  yellowmove(choice, Board)
  column4inaRow(Board)


def clear():
    newboard = Board#;
  for column in newboard:
    for row in column:
      newboard = "N"
  # set inner Board to newboard;
  Board = newBoard#;


if __name__ == "__main__":
    for i in range(4):
        redmove(3, Board)
        BotMove()
        print(Board)
        print(column4inaRow(Board))
