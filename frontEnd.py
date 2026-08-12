# import module + parts required#;
import PyQt5#;
from PyQt5 import QtWidgets, QtTest
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QGridLayout, QHBoxLayout#;
from PyQt5.QtGui import QIcon, QPixmap#;
from PyQt5.QtCore import Qt#;

class frontEnd(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()#;

        # set variable window attributes;
        self.setWindowTitle("Connect 4")#;
        self.setFixedSize(615,700)#;
        # set window icon to Red Token;
        self.setWindowIcon(QIcon("Red Token.png"))#;

        # initialise ui elements;
        self.__initUI()#;
        
        # show this window;
        self.show()#;
    #end construction

    def __initUI(self):
        # add all ui elements to a central widget for easy management;
        centralWidget = QWidget()#;
        self.setCentralWidget(centralWidget)#;

        # add 3 main parts;
        self.__gameBoard = gameBoard()#;
        self.__information = informationWidget()#;
        self.__playBoard = playBoard()#;

        # define the layout (on the central widget) and add all ui elements to it;
        layout = QGridLayout()#;
        # note to self: notation: layout.addWidget(item,row,column)

        layout.addWidget(self.__gameBoard,2,0)#;
        layout.addWidget(self.__playBoard,1,0)#;
        layout.addWidget(self.__information,0,0)#;
        
        #--;
        centralWidget.setLayout(layout)#;
    #ENDMETHOD

    # DEFINE REQUIRED METHODS:
    
    # getters;
    def getMove(self):
        # display the turn to the user;
        self.__information.setPlayer("R")#;
        self.__playBoard.showPlay()#;

        # get the play from the playBoard ();
        while self.__playBoard.isReady()==False:
            # minimum buffer;
            QtTest.QTest.qWait(1)
        #ENDWHILE

        # return the retrieved move;
        move = self.__playBoard.retrieveMove()#;

        self.__playBoard.closePlay()#;
        # notify that the play has been passed;
        self.__information.passedPlay()#;
        # asume but turn;
        self.__information.setPlayer("Y")#;
        return move#;
    #ENDMETHOD

    #;
    # setters;
    def passBoard(self,board):
        self.__information.clearInfo()#; // also clear information at the same time;
        self.__gameBoard.passBoard(board)#;
    #ENDMETHOD
        
    def returnFalse(self):
        self.__information.falsePlay()#;
    #ENDMETHOD
    
    def returnWin(self,team):
        self.__information.Winner(team)#;
    #ENDMETHOD

    def returnTie(self):
        self.__information.Tie()#;
    #ENDMETHOD
        
#ENDCLASS
    
class gameBoard(QtWidgets.QWidget):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)#;
        # create this layer UI / add elements;
        self.__layout = QGridLayout()#;
        self.setFixedSize(590,535)#;
        self.__initUI()#;
        self.show()#;
    #end construction

    def __initUI(self):
        # construct the empty board;
        self.__constructBoard( [ ["N","N","N","N","N","N"],["N","N","N","N","N","N"],["N","N","N","N","N","N"],["N","N","N","N","N","N"],["N","N","N","N","N","N"],["N","N","N","N","N","N"],["N","N","N","N","N","N"] ])#;
        #--;
        
        self.setLayout(self.__layout)#;
    #ENDMETHOD

    def __constructBoard(self,board):
        # track coordinates;
        x = -1#;
        y = 7#;
        
        # for each token, add a label for it and add the corresponding image;
        for column in reversed(board):
            y = y-1#;
            x = -1#;
            for row in reversed(column):
                x = x+1#;
                localLabel = QLabel(self)#;
                # configure properties;
                localLabel.setFixedSize(80,80)#;
                # set size;
                localLabel.setStyleSheet("border:1px solid black;")#;
                # add image;
                
                if row == "R":
                    # tile is red;
                    pixmap = QPixmap("Red Token.png")#;
                elif row == "Y":
                    # tile is yellow;
                    pixmap = QPixmap("Yellow Token.png")#;
                else:
                    pixmap = QPixmap("Null Token.png")#;
                #ENDIF

                # add this image to label;
                localLabel.setPixmap(pixmap)#;
                localLabel.setScaledContents(True)#;
                #ENDIF

                # add this label to the layout;
                self.__layout.addWidget(localLabel,x,y)#;
            #ENDFOR
        #ENDFOR

        # add a little label to help the player along at the very bottom;
        smallLabel = QLabel("When it is your turn, click on the buttons above the board to play! (you are red)",self)#;
        smallLabel.setFixedSize(600,15)#;
        self.__layout.addWidget(smallLabel,8,0)#;
    #ENDMETHOD

    def passBoard(self,board):
        # clear all tiles and 're-render';
        self.__clearWidgets()#;
        # pass the board for construction;
        self.__constructBoard(board)#;
    #ENDMETHOD

    def __clearWidgets(self):
        # note: (stole this code! source:https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt);
        for i in reversed(range(self.__layout.count())):
            # set it's parent to none;
            self.__layout.takeAt(i).widget().setParent(None)#;
        #ENDFOR
    #ENDMETHOD
        
#ENDCLASS

class playBoard(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)#;
        # create this layer UI / add elements;
        self.__layout = QGridLayout()#;
        self.setFixedSize(590,100)#;
        self.__initUI()#;
        # configure retrive play settings;
        self.__send = False#;
        self.__play = int()#;
        # don't show on loading, only do this when it's the player's turn (otherwise hidden);
        self.show()#;
        self.closePlay()#;
    #end construction;

    def __initUI(self):
        # // note; use "↓" for button text;

        # make 7 new buttons;
        self.__buttons = [QPushButton("↓",self),QPushButton("↓",self),QPushButton("↓",self),QPushButton("↓",self),QPushButton("↓",self),QPushButton("↓",self),QPushButton("↓",self)]#;

        # for each of the 7 buttons, configure their settings and add then to layout;
        x = 0#; x coordinate;
        for button in self.__buttons:
            button.setStyleSheet("font-size:20px;")#;
            button.setFixedSize(80,80)#;

            # add newButton to layout;
            self.__layout.addWidget(button,0,x)#;
            x = x+1#; // increment x;
        #ENDFOR

        # set commands for each button (can only do this manually);
        self.__buttons[0].clicked.connect(lambda:self.__click(1))#;
        self.__buttons[1].clicked.connect(lambda:self.__click(2))#;
        self.__buttons[2].clicked.connect(lambda:self.__click(3))#;
        self.__buttons[3].clicked.connect(lambda:self.__click(4))#;
        self.__buttons[4].clicked.connect(lambda:self.__click(5))#;
        self.__buttons[5].clicked.connect(lambda:self.__click(6))#;
        self.__buttons[6].clicked.connect(lambda:self.__click(7))#;

        # set the layout of this widget to self.__layout;
        self.setLayout(self.__layout)#;
    #ENDMETHOD

    def __click(self,column):
        # on a click of a button send a signal out for this button having been clicked;
        self.__play = column#;
        self.__send = True#;
    #ENDMETHOD

    def closePlay(self):
        # hide the buttons from the player and disable them;
        for button in self.__buttons:
            button.hide()#;
        #ENDFOR
        # clear send for next play;
        self.__send = False#;
    #ENDMETHOD

    def showPlay(self):
        # show all buttons;
        for button in self.__buttons:
            button.show()#;
        #ENDFOR
    #ENDMETHOD

    def isReady(self):
        return self.__send#;
    #ENDMETHOD

    def retrieveMove(self):
        return self.__play#;
    #ENDMETHOD
    
#ENDCLASS

class informationWidget(QtWidgets.QWidget):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)#;
        # store tokens for dynamic icon setting later;
        self.__redIcon = QPixmap("Red Token.png")#;
        self.__yellowIcon = QPixmap("Yellow Token.png")#;
        # create this layer UI / add elements;
        self.__layout = QHBoxLayout()#;
        self.setFixedSize(600,50)#;
        self.__initUI()#;
        self.show()#;
    #ENDMETHOD

    def __initUI(self):

        # add the game information labels;
        self.__status = QLabel("Game Status: Loading",self)#;
        self.__TurnIcon = QLabel(self)#;
        self.__Turn = QLabel("Turn: Loading",self)#;
        self.__Legal = QLabel("Play: Evaluating",self)#;
        # make the font sizes readable and adjust attributes;
        self.__Legal.setStyleSheet("font-size:20px;" "color:blue;")#; // green=Legal, red=Illegal, Blue = Evaluating;
        self.__status.setStyleSheet("font-size:20px;" "color:blue;")#; // green=Playing, Blue = other;
        self.__Turn.setStyleSheet("font-size:20px;" "color:black;")#; // red / gold as per player; black for Loading;

        # add turn icon as a small item in front of Turn process;
        self.__TurnIcon.setFixedSize(20,20)#;
        self.__TurnIcon.setPixmap(QPixmap("Null Token.png"))#;
        self.__TurnIcon.setScaledContents(True)#;

        # add elements to grid;
        self.__layout.addWidget(self.__status)#;
        # add a small buffer for better asthetic;
        buffer = QLabel(self)#;
        buffer.setFixedSize(20,50)#;
        self.__layout.addWidget(buffer)#;
        self.__layout.addWidget(self.__TurnIcon)#;
        self.__layout.addWidget(self.__Turn)#;
        self.__layout.addWidget(self.__Legal)#;
         
        self.setLayout(self.__layout)#;
    #ENDMETHOD

    def setPlayer(self, team):
        # check team, update text and icon accordingly;
        # set the text to Playing and configure style sheet;
        self.__status.setText("Game Status: Playing")#;
        self.__status.setStyleSheet("font-size:20px;" "color:green;")#;
        
        if team=="R":
             # set the icon to a red token;
             self.__TurnIcon.setPixmap(self.__redIcon)
             # configure Turn info;
             self.__Turn.setText("Turn: Player")#;
             self.__Turn.setStyleSheet("font-size:20px;" "color:red;")#;
             
        else:
            # else, team=Yellow;
            # set the icon to a yellow! token;
            self.__TurnIcon.setPixmap(self.__yellowIcon)
            # configure Turn info;
            self.__Turn.setText("Turn: Bot")#;
            self.__Turn.setStyleSheet("font-size:20px;" "color:#ffc003;")#; // colour=gold;
        #ENDIF
    #ENDMETHOD

    def __displayGameEnd(self,flag,team):
        # update game status;
        self.__status.setStyleSheet("font-size:20px;" "color:blue;")#;
        self.__Turn.setText("Turn: Gamer Over!  ")#;
        # hide "Legal" info;
        self.__Legal.hide()#;
        # flip the token to the other player, assumed to pass turn after this;
        self.__toggleIcon(flag,team)#;
        if flag=="Win":
            # display winner text;
            if team=="R":
                self.__status.setText("Game Status: Player won!")#;
            else:
                # team=Yellow;
                self.__status.setText("Game Status: Bot won!")#;
            #ENDIF
        else:
            #flag=Tie;
            self.__status.setText("Game Status: Result: Tie!")#;
        #ENDIF
    #ENDMETHOD

    def __toggleIcon(self,flag,team):
        if flag=="Win":
            # display winner Icon;
            if team=="R":
                self.__TurnIcon.setPixmap(self.__redIcon)#;
            else:
                # winner = Yellow;
                self.__TurnIcon.setPixmap(self.__yellowIcon)#;
            #ENDIF
        else:
            #flag=Tie, make icon Null;
            self.__TurnIcon.setPixmap(QPixmap("Null Token.png"))#;
        #ENDIF
    #ENDMETHOD

    # outer call methods:

    def clearInfo(self):
        # clear all information to defaults;
        self.__status.setText("Game Status: Loading")#;
        self.__Turn.setText("Turn: Loading")#;
        self.__Legal.setText("Play: Evaluating")#;
        self.__Legal.setStyleSheet("font-size:20px;" "color:blue;")#;
        self.__status.setStyleSheet("font-size:20px;" "color:blue;")#;
        self.__Turn.setStyleSheet("font-size:20px;" "color:black;")#;
    #ENDMETHOD
    
    def falsePlay(self):
        # display to user that move was illegal;
        self.__Legal.setText("Play: ILLEGAL")#;
        self.__Legal.setStyleSheet("font-size:20px;" "color:red;")#;
    #ENDMETHOD

    def passedPlay(self):
        # display to user that move was illegal;
        self.__Legal.setText("Play: LEGAL")#;
        self.__Legal.setStyleSheet("font-size:20px;" "color:green;")#;
    #ENDMETHOD

    def Winner(self,team):
        self.__displayGameEnd("Win",team)#;
    #ENDMETHOD

    def Tie(self):
        self.__displayGameEnd("Tie","")#;
    #ENDMETHOD
        
#ENDCLASS

# make this for some reason?;
app = QApplication([])#;
