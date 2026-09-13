def yellowMove(column,board):
  # convert move to index format;
  column = column-1#;
  for i in range(6):
         if board[column][i]=="N":
                board[column][i]="Y"
                return board
  return board

def redMove(column,board):
  # convert move to index format;
  column = column-1#;
  for i in range(6):
         if board[column][i]=="N":
                board[column][i]="R"
                return board
  return board 
