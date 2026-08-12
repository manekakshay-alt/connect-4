# import the front end , the back end and the bot, set objects as .frontEnd and .backEnd and .bot:
from frontEnd import *#;
from backEnd import *#;
import time#;

frontEnd = frontEnd()#;
#--;

def game():
    # at the start of the game, clear the board;
    clear()#;
    currentBoardState = getBoard()#;
    frontEnd.passBoard(currentBoardState)#;
    
    # set the player to the user;
    player = "R"#;
    currentMove = int()#;
    playing = True#; // set playing to true as long as the game continues;
    
    while playing:
        # get this player's move;
        currentMove = turn(player)#;
        # while any future attempted moves aren't legal, re-request it (player exclusive);
        while not(isLegalMove(currentMove)):
            # tell the user that the move ain't legal:
            frontEnd.returnFalse()#;
            currentMove = turn("R")#;
        #ENDWHILE
        # pass the new board to the front end;
        currentBoardState = backEnd.getBoard()#;
        frontEnd.passBoard(currentBoardState)#;
        
        # if the game has been won or tied, dsiplay and exit;
        if isWin():
            # tell the user;
            frontEnd.returnWin(player)#;
            # exit.
            playing=False#;
        elif boardIsFull():
            # tell the user;
            frontEnd.returnTie()#;
            # exit;
            playing=False#;
        #ENDIF
        
        # toggle Player;
        player = togglePlayer(player)#;
        # loop;
    #ENDWHILE
#ENDMETHOD

def togglePlayer(player):
    if player=="R":
        return "Y"#;
    else:
        return "R"#;
    #ENDIF
#ENDMETHOD
    
def turn(player):
    move = int()#;
    
    if player=="Y":
        move = BotMove()#;
        
    else:
        # else, it's the user's turn (R);
        # get the user's move from the front end once ready;
        move = frontEnd.getMove()#;
            
    #ENDIF

    # return the move retrieved;
    return move#;
#ENDMETHOD


# prog.
game()#;
