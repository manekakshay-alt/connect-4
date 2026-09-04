def TwoInACoulmn(board):
  count=-1
  for column in board:
    yellow=0
    count=count+1
    for i in column:
      if i=="y":
        yellow=yellow+1
      elif i=="n" and yellow==2:
        return count
      else:
        yellow=0
  return False 


def TwoInARow(board):
  for i in range(6):
    yellow = 0
    count = -1
    for column in board:
      count = count + 1
      if column[i] == "y":
        yellow = yellow + 1
      elif column[i] == "n" and yellow == 2:
        if i == 5 or (column[i+1] == "r" or column[i+1] == "y"):
          return count
        else:
          yellow = 0 
      else:
        yellow = 0

  return False
        



def ThreeInAColumn(board):
  count=-1
  for column in board:
    yellow=0
    count=count+1
    for i in column:
      if i=="y":
        yellow=yellow+1
      elif i=="n" and yellow==3:
        return count
      else:
        yellow=0
  return False 

def ThreeInARow(board):
  for i in range(6):
    yellow = 0
    count = -1
    for column in board:
      count = count + 1
      if column[i] == "y":
        yellow = yellow + 1
      elif column[i] == "n" and yellow == 3:
        if i == 5 or (column[i+1] == "r" or column[i+1] == "y"):
          return count
        else:
          yellow = 0 
      else:
        yellow = 0

  return False

def EasyWin(Board):
  if ThreeInAColumn(Board)!=False:
   return ThreeInAColumn(Board) 
  elif ThreeInARow(Board)!=False:
    return ThreeInARow(Board)

