import sys
import HighScore
import Tournament
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QPixmap, QIntValidator, QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton, QLineEdit, QSlider, QListWidget, \
    QListWidgetItem, QFileDialog

import player
from sim_move_demo import SimMoveDemo
from PyQt5.QtCore import Qt
from Encryptor import Encryptor
encryptor = Encryptor()
from player import Player
import  settings

fname = ""
fname1 = ""

class Menu(QMainWindow):

    def __init__(self):
        super().__init__()

        oImage = QImage("images\\mmenu")

        self.label = QLabel(self)
        self.label1Player = QLabel(self)
        self.oneplayer = QPixmap('images\\JedanIgrac.png')

        self.label2Player = QLabel(self)
        self.twoplayer = QPixmap('images\\DvaIgraca.png')

        self.labelTournament = QLabel(self)
        self.tournament = QPixmap('images\\tournament.png')

        self.labelHighScore = QLabel(self)
        self.high_score = QPixmap('images\\highscore.png')

        self.labelQuit = QLabel(self)
        self.quit = QPixmap('images\\quit.jpeg')

        self.e1 = QLineEdit(self) 
        self.e2 = QLineEdit(self)

        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 562

        palette = QPalette()
        sImage = oImage.scaled(QSize(1000, 562))
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.__init_ui__()

    def __init_ui__(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('images\\smr.png'))
        

        self.setWindowTitle("Menu")



        self.label1Player.setPixmap(self.oneplayer)
        self.label1Player.setGeometry(320, 320, 395, 43)
        self.label1Player.mousePressEvent = self.one_players_on_click

        self.label2Player.setPixmap(self.twoplayer)
        self.label2Player.setGeometry(320, 370, 395, 43)
        self.label2Player.mousePressEvent = self.two_players_on_click

        self.labelTournament.setPixmap(self.tournament)
        self.labelTournament.setGeometry(320, 420, 395, 43)
        self.labelTournament.mousePressEvent = self.tournament_on_click

        self.labelHighScore.setPixmap(self.high_score)
        self.labelHighScore.setGeometry(320, 470, 395, 43)
        self.labelHighScore.mousePressEvent = self.high_score_on_click

        self.labelQuit.setPixmap(self.quit)
        self.labelQuit.setGeometry(320, 520, 395, 43)
        self.labelQuit.mousePressEvent = self.quit_on_click

        self.e1.setMaxLength(100)
        self.e1.setFont(QFont("Arial", 20))
        self.e1.setGeometry(100, 320, 200, 43)
        self.e1.setPlaceholderText("Player 1 Name")

        self.e2.setMaxLength(100)
        self.e2.setFont(QFont("Arial", 20))
        self.e2.setGeometry(730, 320, 200, 43)
        self.e2.setPlaceholderText("Player 2 Name")

        self.e1.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")
        self.e2.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")




        self.listPlayer1 = QListWidget(self)
        self.listPlayer1.setFixedHeight(150)

        self.listPlayer2 = QListWidget(self)
        self.listPlayer2.setFixedHeight(150)

        itm1 = QListWidgetItem("Mario")
        itm1.setIcon(QIcon("smr.png"))
        itm2 = QListWidgetItem("Luigi")
        itm2.setIcon(QIcon("lmr.png"))
        itm3 = QListWidgetItem("Bowser")
        itm3.setIcon(QIcon("bmr.png"))
        itm4 = QListWidgetItem("Wario")
        itm4.setIcon(QIcon("wmr.png"))

        self.listPlayer2.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")

        self.listPlayer2.addItem(itm1)
        self.listPlayer2.addItem(itm2)
        self.listPlayer2.addItem(itm3)
        self.listPlayer2.addItem(itm4)
        self.listPlayer2.setCurrentRow(1)

        itm1 = QListWidgetItem("Mario")
        itm1.setIcon(QIcon("smr.png"))
        itm2 = QListWidgetItem("Luigi")
        itm2.setIcon(QIcon("lmr.png"))
        itm3 = QListWidgetItem("Bowser")
        itm3.setIcon(QIcon("bmr.png"))
        itm4 = QListWidgetItem("Wario")
        itm4.setIcon(QIcon("wmr.png"))

        self.listPlayer1.addItem(itm1)
        self.listPlayer1.addItem(itm2)
        self.listPlayer1.addItem(itm3)
        self.listPlayer1.addItem(itm4)

        self.listPlayer1.setCurrentRow(0)

        self.listPlayer1.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")

        self.listPlayer1.setGeometry(100, 370, 200, 43)
        self.listPlayer2.setGeometry(730, 370, 200, 43)

        self.button = QPushButton(self)
        self.button.setText("Add new")
        self.button.setGeometry(100, 476, 200, 43)
        self.button.setStyleSheet("background: black; color: cyan; width:100px; border: 1px solid cyan")
        self.button.clicked.connect(self.clicker)

        self.button1 = QPushButton(self)
        self.button1.setText("Add new")
        self.button1.setGeometry(730, 476, 200, 43)
        self.button1.setStyleSheet("background: black; color: cyan; width:100px; border: 1px solid cyan")
        self.button1.clicked.connect(self.clicker1)

        self.show()

    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Open file")
        itm5 = QListWidgetItem("Other")
        itm5.setIcon(QIcon(fname[0]))
        self.listPlayer1.addItem(itm5)
        settings.fnamep = fname[0]

    def clicker1(self):
        fname1 = QFileDialog.getOpenFileName(self, "Open file")
        itm5 = QListWidgetItem("Other1")
        itm5.setIcon(QIcon(fname1[0]))
        self.listPlayer2.addItem(itm5)
        settings.fnamep1 = fname1[0]

    def one_players_on_click(self, event):
        player_type = self.listPlayer1.selectedItems()[0].text()
        self.one = SimMoveDemo(1, 1, player_1=Player(self.e1.text(), player_type), menu=self)
        self.one.show()
        self.hide()

    def two_players_on_click(self, event):
        player_type1 = self.listPlayer1.selectedItems()[0].text()
        player_type2 = self.listPlayer2.selectedItems()[0].text()
        name_player1 = self.e1.text()
        name_player2 = self.e2.text()
        if len(name_player1.replace(' ','')) == 0:
            name_player1 = player_type1
        if len(name_player2.replace(' ','')) == 0:
            name_player2 = player_type2

        self.two = SimMoveDemo(2, 1, player_1=Player(name_player1, player_type1), player_2=Player(name_player2, player_type2), menu=self)
        self.two.show()
        self.hide()
        
    def tournament_on_click(self, event):
        self.tournament = Tournament.Tournament(self)
        self.tournament.show()
        self.hide()

    def high_score_on_click(self, event):
        self.high_score = HighScore.HighScore(self)
        self.high_score.show()
        self.hide()

    def quit_on_click(self, event):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())
