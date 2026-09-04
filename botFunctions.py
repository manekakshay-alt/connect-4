#program imports;
import copy#;

def botMove(board:list, depth:int, turn:str)->(int,float):
    # flag for 'checkmate';
    evaluation:float#;

    # if the depth is 0, return;
    if depth==0:
        return 1,0.0#;
    #ENDIF

    # decrement depth;
    depth = depth-1#;
    
    # get the 3 moves from the WhatTimeIsItBot;
    moves:list#;
    moves = whatTimeIsIt(board,turn)#;

    # if any of the moves are 1.0, instant return;
    for move in moves:
        if move[1]==1.0:
            return move[1],flag#;
        #ENDIF
    #ENDFOR

    # determine next layer of recursion's move team;
    inject:str="N"#;
    if turn=="R":
        inject="Y"#;
    else:
        inject="R"#;
    #ENDIF
    # for each move, recur, sending back up the best one;
    bestMove:int#;
    bestEvaluation:float = 0.0#;
    currentMove:int = 0#;
    currentEvaluation:float#;
    for move in moves:
        # make a local copy of the board;
        currentBoard=copy.deepcopy(board)#;
        # apply this move locally;
        if turn == "R":
            redMove(move[0],currentBoard)#;
        else:
            #bot move (Y);
            yellowMove(move[0],currentBoard)#;
        #ENDIF
        # recur with this move;
        currentMove,currentEvaluation=botMove(currentBoard,depth,inject)#;
        # if it's the best move, make bestMove this move and bestEvaluation this evaluation;
        if currentEvaluation > bestEvaluation:
            bestEvaluation=currentEvaluation#;
            bestMove=currentMove#;
        #ENDIF
    #ENDFOR

    # return this depth bestMove and Evaluation;
    return bestMove,bestEvaluation#;
#ENDMETHOD;

def whatTimeIsIt(board:list,turn:str)->list:

    # get the number of pieces on the board;
    pieces:int=0#;
    for column in board:
        for row in column:
            if row!="N":
                pieces=pieces+1#;
            #ENDIF
        #ENDFOR
    #ENDFOR

    # determine if it is the start, middle or end of the game and apply bonuses;
    startBonus:int=0#;
    middleBonus:int=0#;
    endBonus:int=0#;
    if pieces<8:
        # early game;
        startBonus=0.45#;
        endBonus=0.12#;
    elif pieces<27:
        # mid-game;
        startBonus=0.05#;
        middleBonus=0.5#;
        endBonus=0.05#;
    else:
        # end game;
        middleBonus=0.15#;
        endBonus=0.6#;
    #ENDIF
    
    # create a list with all evaluations and then apply each bonus;
    evaluations:list#;
    # end;
    evaluations.append(EvalTie(board,turn))#;
    evaluations[0][1]=evaluations[0][1]+endBonus#;
    # early;
    evaluations.append(EvalThreat(board))#;
    evaluations[1][1]=evaluations[1][1]+startBonus#;
    # middle;
    evaluations.append(EvalBuild(board,turn))#;
    evaluations[2][1]=evaluations[2][1]+middleBonus#;
    # middle;
    evaluations.append(EvalStrat(board))#;
    evaluations[3][1]=evaluations[3][1]+middleBonus#;
    # end;
    evaluations.append(EvalWin(board))#;
    evaluations[4][1]=evaluations[4][1]+endBonus#;

    # define;
    top3:list = [[1,0.0],[1,0.0],[1,0.0]]##;

    # for each evaluation, if it is in the top 3, add it to the list;
    for evaluation in evaluations:   
        # for each item in the top 3;
        for item in top3:
            # if this bot's evaluation is better than this item in the top3, replace it;
            if evaluation[1]>=item[1]:
                item=evaluation#;
                break#; // break out to stop complete overriding;
            #ENDIF
        #ENDFOR
    #ENDFOR
    
    return top3#;
#ENDMETHOD

def getThreats(board:list,team:str)->list:
    # return concatenated lists for column, row and diagonal threats;
    # format: [[col[base:1]:int, row:int[base:1], diagonal:t/f, direction:"N/S,E/W", lengthOFThreat:int],ect.,ect.,ect.];
    return getColumnThreats(board,team)+getRowThreats(board,team)+getDiagonalThreats(board,team)#;
#ENDMETHOD

def getColumnThreats(board:list,team:str)->list:
    threats:list#; // return value;

    # initialise variables;
    antiTeam = "N"#;
    if team=="R":
        antiTeam="Y"#;
    else:
        # team=Yellow;
        antiTeam="R"#;
    #ENDIF
    threatCounter:int = 0#;
    theatContinue:int = 0#;
    continueThreat:bool = False#;
    
    # for each piece;
    for column in board:
        for currentPiece in column:
            # if the piece is this player's;
            if currentPiece==team:
                # continue/initialise this threat and/or increment threatCounter;
                continueThreat=True#;
                threatCounter = threatCounter+1#;
                threatContinue = threatContinue+1#;
            elif currentPiece==antiTeam:
                # else, if it's of the opponent's team, this is no longer a threat;
                continueThreat=False#;
                threatCounter = 0#;
                threatContinue = 0#;
            else:
                # else, just increment threatContinue if the threat is to be continued;
                if continueThreat:
                    threatContinue=threatContinue+1#;
                #ENDIF
            #ENDIF

            # if threat continue = 4, reset and note down this threat;
            if threatContinue==4:
                threatContinue=0#;
                continueThreat=False#;

                # document;
                threats.append([column+1,currentPiece-3,False,"N",threatCounter])#;
                threatCounter=0#;
            #ENDIF
        #ENDFOR
    #ENDFOR
                
    return threats#;
#ENDMETHOD

class threatInstance():
    def __init__(self,originColumn_:int,originRow_:int,flipDirectionFlag:bool):
        self.threatCounter:int = 0#;
        self.threatContinue:int = 0#;
        self.originColumn:int = originColumn_#;
        self.originRow:int = originRow_#;
        self.flag = flipDirectionFlag#;
    # end construction
#ENDCLASS

def getRowThreats(board:list,team:str)->list:
    threats:list#; // return value;
    threatInstances:list#;

    # initialise variables;
    antiTeam = "N"#;
    if team=="R":
        antiTeam="Y"#;
    else:
        # team=Yellow;
        antiTeam="R"#;
    #ENDIF
    
    # for each piece;
    for row in range(6):
        for column in range(7):
            # set the current piece;
            currentPiece=board[column][row]#;
            # if the piece is this player's;
            if currentPiece==team:
                # continue / initialise threats;
                newThreat = threatInstance(column+1,row+1,False)#;
                threatInstances.append(newThreat)#;
                # for each threat, continue/increment;
                for threat in threatInstances:
                    threat.threatCounter=threat.threatCounter+1#;
                    threat.threatContinue=threat.threatContinue+1#;
                #ENDFOR
            elif currentPiece==antiTeam:
                # else, if the piece is of the opposing team's, clear all threat instances;
                threats = []#;
            else:
                # else, just increment threatContinue for each threat;
                # also create a new threat that points West;
                newThreat = threatInstance(column+1,row+1+3,True)#;
                threatInstances.append(newThreat)#;
                
                for threat in threatInstances:
                    threat.threatContinue=threat.threatContinue+1#;
                #ENDFOR
            #ENDIF

            # for each threat, if threatContinue is =4, document it then remove all threats;
            threatPositions:list#;
            direction:str#;
            for threatCount in range(len(threatInstances)):
                threat = threatInstances[threatCount]#;
                if threat.threatContinue==4:
                    # configure the direction of the threat;
                    if threat.flag==False:
                        direction="E"#;
                    else:
                        direction="W"#;
                    #ENDIF
                    threats.append([threat.Column,threat.Row,False,direction,threat.threatCounter])#;
                    threatPositions.append(threatCount)#;
                #ENDIF
            #ENDFOR

            # remove all accounted for threats;
            threatsRemoved:int = 0#;
            for count in threatPositions:
                # remove the threat, and increment threatsRemoved to allow for the correct position to be identifed;
                threatInstances[count-threatsRemoved]#;
                threatsRemoved=threatsRemoved+1#;
            #ENDFOR
        #ENDFOR
    #ENDFOR
                
    return threats#;
#ENDMETHOD

def getDiagonalThreats(board:list,team:str)->list:
    # establish where the diagonals are and what are in them;
    # note: only the diagonals that matter are accounted for;
    
    diagonals:list#;
    # column diagonals;
    for column in range(4):
        # for each piece in the square in which the diagonal is bound, produce a new diagonal;
        diagonals.append([])#;
        for diagonalPosition in range(6-column):
            diagonals[column].append((board[diagonalPosition+column][diagonalPosition],(diagonalPosition+column,diagonalPosition)))#;
        #ENDFOR
    #ENDFOR
    # row diagonals;
    for row in range(3):
        # don't re-add the middle most diagonal;
        if row==0:
            continue#;
        #ENDIF

        # for each other diagonal, form the square in which it is bound, adding all pieces to that new diagonal;
        diagonals.append([])#;
        for diagonalPosition in range(6-row):
            diagonals[row+4].append((board[diagonalPosition][diagonalPosition+row],(diagonalPosition,diagonalPosition+row)))#;
        #ENDFOR
    #ENDFOR

    # for each diagonal do as below;
    threats:list#;
    threatInstances:list#;

    # initialise detection variables;
    antiTeam = "N"#;
    if team=="R":
        antiTeam="Y"#;
    else:
        # team=Yellow;
        antiTeam="R"#;
    #ENDIF

    # for each piece on the board;
    for diagonal in diagonals:
        for currentPiece in diagonal:

            if currentPiece[0]==team:
                # generate a new threat;
                newThreat=threatInstance(currentPiece[1][0],currentPiece[1][1],False)#;
                threatInstances.append(newThreat)#;

                # for each threat, continue/increment;
                for threat in threatInstances:
                    threat.threatCounter=threat.threatCounter+1#;
                    threat.threatContinue=threat.threatContinue+1#;
                #ENDFOR
            elif currentPiece[0]==antiTeam:
                # clear threatInstances, as no threats can continue through an opponent's piece;
                threatInstances = []#;
            else:
                # else:
                # generate a new Westward threat;
                newThreat=threatInstance(currentPiece[1][0],currentPiece[1][1],True)#;
                threatInstances.append(newThreat)#;
                
                # for each threat, increment threatContinue only;
                for threat in threatInstances:
                    threat.threatContinue=threat.threatContinue+1#;
                #ENDFOR
            #ENDIF

            # for each threat, if threatContinue is =4, document it then remove all threats;
            threatPositions:list#;
            direction:str#;
            for threatCount in range(len(threatInstances)):
                threat = threatInstances[threatCount]#;
                if threat.threatContinue==4:
                    # configure the direction of the threat;
                    if threat.flag==False:
                        direction="E"#;
                    else:
                        direction="W"#;
                    #ENDIF
                    threats.append([threat.Column,threat.Row,True,direction,threat.threatCounter])#;
                    threatPositions.append(threatCount)#;
                #ENDIF
            #ENDFOR

            # remove all accounted for threats;
            threatsRemoved:int = 0#;
            for count in threatPositions:
                # remove the threat, and increment threatsRemoved to allow for the correct position to be identifed;
                threatInstances[count-threatsRemoved]#;
                threatsRemoved=threatsRemoved+1#;
            #ENDFOR
        #ENDFOR
    #ENDFOR

    return threats#;
#ENDMETHOD

def getThreatSlots(board:list,increment:int,originColumn:int,originRow:int,diagonal:bool,vertical:bool)->list:
    # get the team being pointed at;
    team:str = board[originColumn][originRow]#;

    threatSlots:list#; // return list;

    # continue for 4:
    for i in range(4):
        # if this piece isn't on the original team, add it to the return list;
        if board[originColumn][originRow]!=team:
            # add the column of this threat slot;
            threatSlots.append(originColumn)#;
        #ENDIF
        # increment view in direction given;
        if diagonal==True:
            # increment originRow and originColumn by increment;
            originRow=originRow+increment#;
            originColumn=originColumn+increment#;
        else:
            # else, non diagonal movement, increment in column if verticle;
            if vertical==True:
                originRow=originRow+increment#;
            else:
                # else, horizontal movement;
                originColumn=originColumn+increment#;
            #ENDIF
        #ENDIF
    #ENDFOR

    return threatSlots#;
#ENDMETHOD

def EvalBuild(board:list,turn:str)->list:
    #---
    # outline:
    # determine what threats the bot has;
    # determine what threats the player has;
    # immediately block any 3s with high strength;
    # if all moves block any of the bot's threats, then return strength 0.0;
    #
    # eval (set=0.4):
    # not building on a 2/threat +=0.05;
    # if we are forseeably building up towards a diagonal threat, += 0.1;
    # if this move does not lead to any immediate player 3/threats, += 0.05;
    #---

    # get all 2/3 threats;
    threatsBot:list#;
    threatsPlayer:list#;
    if turn=="Y":
        threatsBot = getThreats(board,"Y")#;
        threatsPlayer = getThreats(board,"R")#;
    else:
        # turn = player's;
        threatsBot = getThreats(board,"R")#;
        threatsPlayer = getThreats(board,"Y")#;
    #ENDIF

    
    # if there is a 3-threat from the player, return immediately with strength 0.0, there are other bots that deal with this;
    for threat in threatsPlayer:
        if threat[4]==3:
            return [1,0.0]#;
        #ENDIF
    #ENDFOR

    blocked:bool=True#;
    originalThreatLength:int = len(threatsBot)#;
    strength:int#;
    bestMove:list = [1,0.0]#;
    # for each move;
    for move in range(1,7):
        # set the strength to 0.4;
        strength=0.4#;
        # make a local copy of the board;
        currentBoard=copy.deepcopy(board)#;
        # apply the move to the board;
        if turn=="Y":
            yellowMove(move,currentBoard)#;
        else:
            redMove(move,currentBoard)#;
        #ENDIF
        # if this blocks a threat, continue;
        newThreats:list = getThreats(currentBoard,team)#;
        if len(newThreats)<originalThreatLength:
            continue#;
        else:
            # else, clear the blocked latch;
            blocked = False#;
        #ENDIF

        # if this move doesn't build on a 2+ threat, strength+=0.05;
        if len(newThreats)==originalThreatLength:
            strength+=0.05#;
        #ENDIF
            
        # if this move forseeably builds to a diagonal threat, strength+=0.1;
        # get moveColumn, moveRow;
        moveColumn:int = move-1#;
        moveRow:int#;
        for row in range(6):
            # if it's blank, just go to the next;
            if currentBoard[move-1][row]=="N" and row!=5:
                continue#;
            else:
                # else, it is not blank or it's the last row;
                # the row of the move is 1 below this one if it's now [5];
                moveRow=row-1#;
                if row==5:
                    moveRow=5#;
                #ENDIF
                break#;
            #ENDIF
        #ENDFOR
            
        for threat in newThreats:
            # for each threat, if the move we just made is in this threat, then increment strength by 0.1;
            if threat[2]==True and threat[3]==2:
                # define the increment;
                increment:int#;
                if threat[3]=="E":
                    increment=1#;
                else:
                    # else, westward direction;
                    increment=-1#;
                #ENDIF
                # locate the origin of this threat;
                threatColumn:int=threat[1]-1#;
                threatRow:int=threat[0]-1#;
                # follow the trajectory of this threat for 4 moves;
                for i in range(4):
                    # if this is the same column and row, then the move is a part of this threat, increment strength and break;
                    if threatColumn==moveColumn and threatRow==moveRow:
                        strength=strenght+0.1#;
                        break#;
                    #ENDIF
                    # increment threatColumn,threatRow;
                    threatColumn=threatColumn+increment#;
                    threatRow=threatRow+increment#;
                #ENDFOR
            #ENDIF (else, next);
        #ENDFOR
                    
        # if this move doesn't lead to any player 3-threats, strength+=0.05;
        noThreeThreats:bool=True#;
        for threat in newThreats:
            # if this threat is of length 3:
            if threat[3]==3:
                noThreeThreats=False#;
                break#;
            #ENDIF
        #ENDFOR

        if noThreeThreats==True:
            strength=strength+0.05#;
        #ENDIF

        # if this move has the greatest strength so far, make it the greatest;
        if bestMove[1]<strength:
            # set new best move;
            bestMove[0]=move#;
            bestMove[1]=strength#;
        #ENDIF
    #ENDFOR

    # if blocked still == True, then all moves remove threats, return strength 0;
    if blocked==True:
        return [1,0.0]#;
    #ENDIF

    # if strength is somehow >1, set to 1.0;
    if bestMove[1]>1:
        bestMove[1]=1.0#;
    #ENDIF
    
    return bestMove#;
#ENDMETHOD

def EvalTie(board:list,turn:str)->list:
    #---
    # outline:
    # block all opponent threats;
    # if there are no threats:
    # try and fill up the middle;
    # otherwise play as far out to the side as possible;
    #---;

    # get all opponent threats;
    playerThreats:list#;
    if turn=="Y":
        playerThreats=getThreats(board,"R")#;
    else:
        # team=="R":
        playerThreats=getThreats(board,"Y")#;
    #ENDIF

    # if there is a 3-threat from the player, return immediately with strength 1.0;
    for threat in playerThreats:
        if threat[4]==3:
            # go to this threat and block it;
            if threat[2]==False:
                # non diagonal;
                if threat[3]=="N":
                    # column threat, play in this column;
                    return [threat[0],1.0]#;
                else:
                    # row threat, find the direction and origin;
                    # define increment;
                    direction:int#;
                    if threat[3]=="E":
                        direction=1#;
                    else:
                        # else, westward direction (left, -1);
                        direction=-1#;
                    #ENDIF

                    # find the first blocking move and return;
                    return getThreatSlots(board,direction,threat[0]-1,threat[1]-1,False,False)[0]#;
                #ENDIF
            else:
                # diagonal, define increment;
                direction:int#;
                if threat[3]=="E":
                    direction=1#;
                else:
                    # else, westward direction (left, -1);
                    direction=-1#;
                #ENDIF

                # find the first blocking move and return;
                return getThreatSlots(board,direction,threat[0]-1,threat[1]-1,True,False)[0]#;
            #ENDIF
                
        # else, threats are of length 2 or non existent;
        #ENDIF
    #ENDFOR

    # for 2-threats;
    bestSlots:list#;
    for threat in playerThreats:
        if threat[4]==2:
            # retrieve each possible slot for this threat to be countered;
            increment:int#;
            vertical:bool#;
            if threat[3]=="N" or threat[3]=="E":
                increment=1#;
            else:
                # South or West;
                increment=-1#;
            #ENDIF
            if threat[2]==False and (threat[3]=="N" or threat[3]=="S"):
                vertical=True#;
            else:
                # else, diagonal, or horizontal, set vertical to false;
                vertical=False#;
            #ENDIF
            threatSlots=getThreatSlots(board,increment,threat[0]-1,threat[1]-1,threat[2],vertical)#;

            # select the most central threat slot;
            minimum:int=7#;
            bestSlot:int=0#;
            for threatSlot in threatSlots:
                # if this is the closest slot to the centre, then set it to be the choice;
                if abs(3-threatSlot)<=minmum:
                    bestSlot=threatSlot#;
                    minimum=3-threatSlot#;
                #ENDIF
            #ENDFOR
            # if there were no updates to bestSlot, return strength 0;
            if bestSlot==0:
                return [1,0.0]#;
            #ENDIF

            # add the best slot to the bestSlots list;
            bestSlots.append(bestSlot)#;
        #ENDIF
    #ENDFOR

    # return the modal bestSlot with strength 0.75, if it's tied the last is passed;
    counts:list = [0,0,0,0,0,0,0]#;
    if len(bestSlots>0):
        # for each slot, count the number of bestSlots that appear there;
        for slot in bestSlots:
            counts[slot] = counts[slot]+1#;
        #ENDFOR

        # get the greatest slot;
        greatest:int=0#;
        greatestPosition:int=0#;
        for element in len(counts):
            if counts[element]>=greatest:
                greatest=counts[element]#;
                greatestPosition=element#;
            #ENDIF
        #ENDFOR

        # return;
        return [greatestPosition,0.75]#;
    #ENDIF

    # if there are no threats, try these moves in order;
    remainderMoves:list = [3,0,6,1,5,2,4]#;
    for move in remainderMoves:
        # assume this column is full;
        columnFull=True#;
        for row in board[move]:
            # for each piece, if it is empty;
            if row=="N":
                # then the column is not full, break;
                columnFull=False#;
                break#;
            #ENDIF
        #ENDFOR

        if columnFull==False:
            # if the column isn't full, play here;
            return [move,0.65]#;
        #ENDIF
    #ENDFOR

    # if someone went awry, return the default case;
    return [1,0.0]#;
#ENDMETHOD
