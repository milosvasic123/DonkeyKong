import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton
from player import Player


class GameOver(QMainWindow):

    def __init__(self, br, sc, menu=None, tournament_winner=None):
        super().__init__()
        self.menu = menu
        oImage = QImage("images\\over.jpg")
        self.label = QLabel(self)
        self.rezz = QLabel(self)
        self.who_is_winner = QLabel(self)
        self.who_is_winner1 = QPixmap('images\\player1-wins.png')
        self.who_is_winner2 = QPixmap('images\\player2-wins.png')
        self.left = 400
        self.top = 200
        self.width = 450
        self.height = 470
        self.score = sc
        if tournament_winner:
            self.tournament_winner = tournament_winner
            self.mario_wins = QPixmap('images\\mario-wins.png')
            self.luigi_wins = QPixmap('images\\luigi-wins.png')
            self.bowser_wins = QPixmap('images\\bowser-wins.png')
            self.wario_wins = QPixmap('images\\wario-wins.png')

        palette = QPalette()
        sImage = oImage.scaled(QSize(450, 470))
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.__init_ui__(br, tournament_winner)

    def __init_ui__(self, br, tournament_winner):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('images\\smr'))

        self.setWindowTitle("Game Over")

        if br == 1 and tournament_winner is None:
            self.who_is_winner.setPixmap(self.who_is_winner1)
            self.who_is_winner.setGeometry(35, 250, 395, 43)

        elif tournament_winner:
            if self.tournament_winner.name == "Mario":
                self.who_is_winner.setPixmap(self.mario_wins)
            elif self.tournament_winner.name == "Luigi":
                self.who_is_winner.setPixmap(self.luigi_wins)
            elif self.tournament_winner.name == "Bowser":
                self.who_is_winner.setPixmap(self.bowser_wins)
            elif self.tournament_winner.name == "Wario":
                self.who_is_winner.setPixmap(self.wario_wins)
            self.who_is_winner.setGeometry(30, 250, 400, 50)
            self.who_is_winner.setScaledContents(True)

        else:
            self.who_is_winner.setPixmap(self.who_is_winner2)
            self.who_is_winner.setGeometry(35, 250, 395, 43)

        self.labelGoBack = QLabel(self)
        self.go_back_img = QPixmap('images\\menu.png')
        self.labelGoBack.setPixmap(self.go_back_img)
        self.labelGoBack.setGeometry(155, 360, 200, 30)
        self.labelGoBack.mousePressEvent = self.go_to_menu_on_click


        self.show()

    def go_to_menu_on_click(self, event):
        self.menu.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GameOver(1, 1, menu=None, tournament_winner=Player("Luigi", "Luigi"))
    sys.exit(app.exec_())
