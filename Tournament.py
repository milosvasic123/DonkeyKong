import sys
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton, QLineEdit, QListWidget, QListWidgetItem, \
    QFileDialog

import settings
from sim_move_demo import SimMoveDemo
from player import Player

fname = ""
fname1 = ""
fname2 = ""
fname3 = ""


class Tournament(QMainWindow):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.setStyleSheet("background: black;")

        self.e1 = QLineEdit(self)
        self.e2 = QLineEdit(self)
        self.e3 = QLineEdit(self)
        self.e4 = QLineEdit(self)

        self.labelTournament = QLabel(self)
        self.tournament = QPixmap('images\\tournament.png')

        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 562

        self.__init_ui__()

    def __init_ui__(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle("Tournament")

        self.labelTournament.setPixmap(self.tournament)
        self.labelTournament.setGeometry(350, 20, 395, 43)
        self.labelTournament.mousePressEvent = self.tournament_on_click

        self.e1.setMaxLength(100)
        self.e1.setFont(QFont("Arial", 20))
        self.e1.setGeometry(100, 80, 200, 43)
        self.e1.setPlaceholderText("Player 1 Name")

        self.e2.setMaxLength(100)
        self.e2.setFont(QFont("Arial", 20))
        self.e2.setGeometry(730, 80, 200, 43)
        self.e2.setPlaceholderText("Player 2 Name")

        self.e3.setMaxLength(100)
        self.e3.setFont(QFont("Arial", 20))
        self.e3.setGeometry(100, 320, 200, 43)
        self.e3.setPlaceholderText("Player 3 Name")

        self.e4.setMaxLength(100)
        self.e4.setFont(QFont("Arial", 20))
        self.e4.setGeometry(730, 320, 200, 43)
        self.e4.setPlaceholderText("Player 4 Name")

        self.e1.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")
        self.e2.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")
        self.e3.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")
        self.e4.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")

        self.listPlayer1 = QListWidget(self)
        self.listPlayer1.setFixedHeight(150)
        self.listPlayer2 = QListWidget(self)
        self.listPlayer2.setFixedHeight(150)
        self.listPlayer3 = QListWidget(self)
        self.listPlayer3.setFixedHeight(150)
        self.listPlayer4 = QListWidget(self)
        self.listPlayer4.setFixedHeight(150)

        itm1 = QListWidgetItem("Mario")
        itm1.setIcon(QIcon("smr.png"))
        itm2 = QListWidgetItem("Luigi")
        itm2.setIcon(QIcon("lmr.png"))
        itm3 = QListWidgetItem("Bowser")
        itm3.setIcon(QIcon("bmr.png"))
        itm4 = QListWidgetItem("Wario")
        itm4.setIcon(QIcon("wmr.png"))
        self.listPlayer1.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")
        self.listPlayer1.addItem(itm1)
        self.listPlayer1.addItem(itm2)
        self.listPlayer1.addItem(itm3)
        self.listPlayer1.addItem(itm4)
        self.listPlayer1.setCurrentRow(1)

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
        self.listPlayer3.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")
        self.listPlayer3.addItem(itm1)
        self.listPlayer3.addItem(itm2)
        self.listPlayer3.addItem(itm3)
        self.listPlayer3.addItem(itm4)
        self.listPlayer3.setCurrentRow(1)

        itm1 = QListWidgetItem("Mario")
        itm1.setIcon(QIcon("smr.png"))
        itm2 = QListWidgetItem("Luigi")
        itm2.setIcon(QIcon("lmr.png"))
        itm3 = QListWidgetItem("Bowser")
        itm3.setIcon(QIcon("bmr.png"))
        itm4 = QListWidgetItem("Wario")
        itm4.setIcon(QIcon("wmr.png"))
        self.listPlayer4.setStyleSheet("background: black; color: cyan; border: 1px solid cyan")
        self.listPlayer4.addItem(itm1)
        self.listPlayer4.addItem(itm2)
        self.listPlayer4.addItem(itm3)
        self.listPlayer4.addItem(itm4)
        self.listPlayer4.setCurrentRow(1)

        self.listPlayer1.setGeometry(100, 130, 200, 43)
        self.listPlayer2.setGeometry(730, 130, 200, 43)
        self.listPlayer3.setGeometry(100, 370, 200, 43)
        self.listPlayer4.setGeometry(730, 370, 200, 43)

        self.button = QPushButton(self)
        self.button.setText("Add new")
        self.button.setGeometry(100, 236, 200, 43)
        self.button.setStyleSheet("background: black; color: cyan; width:100px; border: 1px solid cyan")
        self.button.clicked.connect(self.clicker)

        self.button1 = QPushButton(self)
        self.button1.setText("Add new")
        self.button1.setGeometry(730, 236, 200, 43)
        self.button1.setStyleSheet("background: black; color: cyan; width:100px; border: 1px solid cyan")
        self.button1.clicked.connect(self.clicker1)

        self.button2 = QPushButton(self)
        self.button2.setText("Add new")
        self.button2.setGeometry(100, 476, 200, 43)
        self.button2.setStyleSheet("background: black; color: cyan; width:100px; border: 1px solid cyan")
        self.button2.clicked.connect(self.clicker2)

        self.button3 = QPushButton(self)
        self.button3.setText("Add new")
        self.button3.setGeometry(730, 476, 200, 43)
        self.button3.setStyleSheet("background: black; color: cyan; width:100px; border: 1px solid cyan")
        self.button3.clicked.connect(self.clicker3)

        self.labelGoBack = QLabel(self)
        self.go_back_img = QPixmap('images\\goback.jpeg')
        self.labelGoBack.setPixmap(self.go_back_img)
        self.labelGoBack.setGeometry(400, 480, 200, 43)
        self.labelGoBack.mousePressEvent = self.go_back_on_click

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

    def clicker2(self):
        fname2 = QFileDialog.getOpenFileName(self, "Open file")
        itm5 = QListWidgetItem("Other2")
        itm5.setIcon(QIcon(fname2[0]))
        self.listPlayer3.addItem(itm5)
        settings.fnamep2 = fname2[0]

    def clicker3(self):
        fname3 = QFileDialog.getOpenFileName(self, "Open file")
        itm5 = QListWidgetItem("Other3")
        itm5.setIcon(QIcon(fname3[0]))
        self.listPlayer4.addItem(itm5)
        settings.fnamep3 = fname3[0]

    def go_back_on_click(self, event):
        self.menu.show()
        self.close()

    def tournament_on_click(self, event):
        player_type1 = self.listPlayer1.selectedItems()[0].text()
        player_type2 = self.listPlayer2.selectedItems()[0].text()
        player_type3 = self.listPlayer3.selectedItems()[0].text()
        player_type4 = self.listPlayer4.selectedItems()[0].text()

        name_player1 = self.e1.text()
        name_player2 = self.e2.text()
        name_player3 = self.e3.text()
        name_player4 = self.e4.text()

        if len(name_player1.replace(' ', '')) == 0:
            name_player1 = player_type1
        if len(name_player2.replace(' ', '')) == 0:
            name_player2 = player_type2
        if len(name_player3.replace(' ', '')) == 0:
            name_player3 = player_type3
        if len(name_player4.replace(' ', '')) == 0:
            name_player4 = player_type4

        self.tournament = SimMoveDemo(2, 1, player_1=Player(name_player1, player_type1), player_2=Player(name_player2, player_type2), player_3=Player(name_player3, player_type3), player_4=Player(name_player4, player_type4), menu=self)
        self.tournament.show()
        self.hide()

    if __name__ == '__main__':
        app = QApplication(sys.argv)
        ex = Tournament()
        sys.exit(app.exec_())

