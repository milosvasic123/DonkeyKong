import csv
import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow
from GorilaMovement import GorilaMovement
from JasminMovement import JasminMovement
from pomocniFajl import isHit, generateBarrel, GorilaFreezeProcess
from multiprocessing import Queue, Process
from BarrelMovement import BarrelMovement
from random import randint
from key_notifier import KeyNotifier
from key_notifier2 import KeyNotifier2
from Force import HeartsMovement
from GameOver import GameOver
from Encryptor import Encryptor
from Bomb import BombsMovement
from Light import LightsMovement
from player import Player
import random

brLevel = 0
encryptor = Encryptor()


class SimMoveDemo(QMainWindow):

    def __init__(self, brojIgraca, lvlNumber, player_1=None, player_2=None, player_3=None, player_4=None, menu=None):
        super().__init__()
        self.menu = menu
        self.player1 = player_1
        self.player2 = player_2
        oImage = QImage("images\\back")
        sImage = oImage.scaled(QSize(1000, 562))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)
        self.tournament = False
        if player_3 and player_4:
            self.br_igr = 1
            self.tournament = True
            self.player3 = player_3
            self.player4 = player_4
            self.list_of_players = [player_1, player_2, player_3, player_4]
        if self.tournament:
            # assign randomly
            self.pobednici = list()
            random.shuffle(self.list_of_players)
            self.player1 = self.list_of_players[0]
            self.player2 = self.list_of_players[1]

            self.next_player1 = self.list_of_players[2]
            self.next_player2 = self.list_of_players[3]
        if self.player1:
            self.pix1 = QPixmap(self.player1.pic_left)
            self.pix11 = QPixmap(self.player1.pic_right)
        if self.player2:
            self.pix12 = QPixmap(self.player2.pic_left)
            self.pix112 = QPixmap(self.player2.pic_right)

        self.pix2 = QPixmap('images\\jasmin')
        self.pix22 = QPixmap('images\\pll')

        self.pix3 = QPixmap('images\\gl')

        self.srce = QPixmap('images\\heart.png')
        self.bomba = QPixmap('images\\bomb.png')
        self.munja = QPixmap('images\\light.png')
        self.pix32 = QPixmap('images\\gr')
        self.izadji = QPixmap('images\\quit.jpeg')
        self.pix4 = QPixmap('images\\barell')

        self.hitSide = False

        self.label2 = QLabel(self)
        self.label4 = QLabel(self)
        self.label3 = QLabel(self)
        self.label30 = QLabel(self)

        self.labelLifes1 = QLabel(self)
        self.labelLifes2 = QLabel(self)
        self.life1ispis = QLabel(self)
        self.life2ispis = QLabel(self)
        self.label1 = QLabel(self)
        self.label11 = QLabel(self)

        self.kraj = None

        self.labelLevel = QLabel(self)
        self.ispisLabel1 = QLabel(self)
        self.playerRez1 = QLabel(self)
        self.playerRez11 = QLabel(self)
        self.playerRez2 = QLabel(self)
        self.playerRez22 = QLabel(self)
        self.gameoverLab = QLabel(self)
        self.izlazIzIgre = QLabel(self)

        self.barrelQueue = Queue()
        self.barrelProcess = Process(target=generateBarrel, args=[self.barrelQueue])
        self.barrels = []
        self.barrelProcess.start()
        self.gorilaStop = Queue()
        self.gorilaStart = Queue()
        self.gorilaBug = Process(target=GorilaFreezeProcess, args=[self.gorilaStart, self.gorilaStop])
        self.gorilaBug.start()

        self.hearts = []
        self.bombs = []

        self.zaustavio = False

        self.heart = QLabel(self)
        self.heart.setPixmap(self.srce)

        self.bomb = QLabel(self)
        self.bomb.setPixmap(self.bomba)

        self.lightbolt = QLabel(self)
        self.lightbolt.setPixmap(self.munja)

        self.prvi = False
        self.drugi = False  # da li su pobedili

        self.izgubioPrvi = False
        self.izgubioDrugi = False

        self.prviSprat = False

        self.poeniPL1 = 0
        self.poeniPL2 = 0
        self.trenutniNivo = lvlNumber
        self.count = 0
        self.count1 = 0
        self.count2 = 0
        self.count3 = 0
        self.count4 = 0
        self.count5 = 0
        self.count6 = 0
        self.count7 = 0

        self.ispisLabel1.setText('Level: ')
        self.ispisLabel1.setStyleSheet('color: blue')

        self.playerRez1.setText(self.player1.name)
        self.playerRez1.setStyleSheet('color: red')
        if self.player2:
            self.playerRez2.setText(self.player2.name)

        self.life1ispis.setText('P1 Life: ')
        self.life1ispis.setStyleSheet('color: red')

        self.life2ispis.setText('P2 Life: ')

        self.playerRez11.setText(str(self.poeniPL1))
        self.playerRez11.setStyleSheet('color: red')

        self.playerRez22.setText(str(self.poeniPL2))

        self.left = 200
        self.top = 100
        self.width = 1000
        self.height = 562

        self.key_notifier = KeyNotifier()

        if (brojIgraca == 1):
            self.key_notifier.key_signal.connect(self.__update_position__)  # -----------------
            self.brojIgracaJedan = True
        else:
            self.brojIgracaJedan = False
            self.key_notifier2 = KeyNotifier2()
            self.key_notifier.key_signal.connect(self.__update_position__)  # -----------------
            self.key_notifier2.key_signal2.connect(self.__update_position2__)  # -----------------
            self.key_notifier2.start()

        self.key_notifier.start()

        self.__init_ui__(brLevel, brojIgraca)

    def __init_ui__(self, brLevel, brojIgraca):
        self.setWindowTitle('Donkey Kong')

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(280, 475, 57, 67)

        self.label2.setPixmap(self.pix2)
        self.label2.setGeometry(475, 0, 40, 75)
        self.promenioSliku = True

        self.label3.setPixmap(self.pix3)
        self.label3.setGeometry(455, 85, 70, 75)

        self.izlazIzIgre.setPixmap(self.izadji)
        self.izlazIzIgre.setGeometry(750, 50, 250, 47)
        self.izlazIzIgre.mousePressEvent = self.shutdown

        brLevel += 1
        font = QtGui.QFont()
        font.setPointSize(20)

        self.labelLevel.setText(str(self.trenutniNivo))
        self.labelLevel.setGeometry(110, 5, 50, 50)
        self.labelLevel.setFont(font)
        self.labelLevel.setStyleSheet('color: blue')

        self.ispisLabel1.setGeometry(2, -20, 100, 100)
        self.ispisLabel1.setFont(font)

        self.lives1 = 3
        self.lives2 = 3

        self.labelLifes1.setText(str(self.lives1))
        self.labelLifes1.setGeometry(110, 15, 100, 100)
        self.labelLifes1.setFont(font)
        self.labelLifes1.setStyleSheet('color: red')

        self.life1ispis.setGeometry(2, 40, 150, 50)
        self.life1ispis.setFont(font)

        self.playerRez1.setGeometry(2, 40, 120, 100)
        self.playerRez11.setGeometry(110, 40, 100, 100)
        self.playerRez1.setFont(font)
        self.playerRez1.setStyleSheet('color: red')
        self.playerRez11.setFont(font)

        if self.tournament:
            self.tournamentLabel = QLabel(self)
            self.tournamentLabel.setText("Tournament")
            self.tournamentLabel.setGeometry(2, 190, 180, 400)
            self.tournamentLabel.setAlignment(QtCore.Qt.AlignTop)
            self.tournamentLabel.setFont(font)
            self.tournamentLabel.setStyleSheet('color: red')

        if (brojIgraca == 2):
            self.brojIgracaJedan = False

            self.playerRez2.setGeometry(2, 110, 100, 100)
            self.playerRez22.setGeometry(110, 110, 100, 100)
            self.playerRez2.setFont(font)
            self.playerRez2.setStyleSheet('color: green')
            self.playerRez22.setFont(font)
            self.playerRez22.setStyleSheet('color: green')

            self.life2ispis.setGeometry(2, 85, 120, 100)
            self.labelLifes2.setGeometry(110, 85, 100, 100)
            self.life2ispis.setFont(font)
            self.life2ispis.setStyleSheet('color: green')
            self.labelLifes2.setText(str(self.lives2))
            self.labelLifes2.setStyleSheet('color: green')
            self.labelLifes2.setFont(font)

            self.label30.setPixmap(self.pix112)
            self.label30.setGeometry(660, 475, 57, 75)

        self.jasminMovement = JasminMovement()
        self.jasminMovement.jasminMovementSignal.connect(self.moveJasmin)
        self.jasminMovement.start()

        self.gorilaMovement = GorilaMovement()
        self.gorilaMovement.gorilaMovementSignal.connect(self.moveGorila)
        self.gorilaMovement.start()

        self.movingBarrels = BarrelMovement()
        self.movingBarrels.barrelMovementSignal.connect(self.moveBarrels)
        self.movingBarrels.start()

        self.heartsMovement = HeartsMovement()
        self.heartsMovement.heartsMovementSignal.connect(self.generateForce)
        self.heartsMovement.start()

        self.bombsMovement = BombsMovement()
        self.bombsMovement.bombsMovementSignal.connect(self.generateBombs)
        self.bombsMovement.start()

        self.lightsMovement = LightsMovement()
        self.lightsMovement.lightsMovementSignal.connect(self.generateLights)
        self.lightsMovement.start()

        self.show()

    def keyPressEvent(self, event):
        a = event.key()
        self.key_notifier.add_key(a)
        if (self.brojIgracaJedan == False):
            b = event.key()
            self.key_notifier2.add_key(b)

    def keyReleaseEvent(self, event):
        a = event.key()
        self.key_notifier.rem_key(a)
        if (self.brojIgracaJedan == False):
            b = event.key()
            self.key_notifier2.rem_key(b)

    def __update_position__(self, key):
        rec1 = self.label1.geometry()

        if key == Qt.Key_Right:
            self.label1.setPixmap(self.pix11)
        elif key == Qt.Key_Left:
            self.label1.setPixmap(self.pix1)

        if key == Qt.Key_1 and self.player1.player_type == "Mario":
            while self.count < 1:
                self.count += 1
                if self.lives1 > 0:
                    self.lives1 *= 2
                    self.labelLifes1.setText(str(self.lives1))

        if key == Qt.Key_2 and self.player1.player_type == "Luigi":
            while self.count1 < 1:
                self.count1 += 1
                if self.poeniPL1 > 0:
                    self.poeniPL1 *= 2
                    self.playerRez11.setText(str(self.poeniPL1))

        if key == Qt.Key_3 and self.player1.player_type == "Bowser":
            while self.count2 < 1:
                self.count2 += 1
                if self.poeniPL2 > 0:
                    self.poeniPL2 -= 2
                    self.playerRez22.setText(str(self.poeniPL2))

        if key == Qt.Key_4 and self.player1.player_type == "Wario":
            while self.count3 < 1:
                self.count3 += 1
                if self.lives2 > 0:
                    self.lives2 -= 1
                    self.labelLifes2.setText(str(self.lives2))

        if key == Qt.Key_Right and rec1.x() <= 660 and (
                rec1.y() == 475 or (rec1.y() == 385 and rec1.x() <= 640) or (rec1.y() == 290 and rec1.x() <= 630) or (
                rec1.y() == 195 and rec1.x() <= 610) or (rec1.y() == 95 and rec1.x() <= 580) or (
                        rec1.y() == 0 and rec1.x() <= 540)):
            self.label1.setGeometry(rec1.x() + 5, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Left and rec1.x() >= 290 and (
                rec1.y() == 475 or (rec1.y() == 385 and rec1.x() >= 300) or (rec1.y() == 290 and rec1.x() >= 310) or (
                rec1.y() == 195 and rec1.x() >= 330) or (rec1.y() == 95 and rec1.x() >= 340) or (
                        rec1.y() == 0 and rec1.x() >= 380)):
            self.label1.setGeometry(rec1.x() - 5, rec1.y(), rec1.width(), rec1.height())
        elif key == Qt.Key_Up:
            if (rec1.x() >= 445 and rec1.x() <= 465 and rec1.y() > 385 and rec1.y() <= 475):
                self.label1.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
                if rec1.y() == 395:
                    self.poeniPL1 += 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 290 and rec1.x() <= 310 and rec1.y() > 290 and rec1.y() <= 385):
                self.label1.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
                if rec1.y() == 305:
                    self.poeniPL1 += 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 620 and rec1.x() <= 640 and rec1.y() > 195 and rec1.y() <= 290):
                self.label1.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
                if rec1.y() == 215:
                    self.poeniPL1 += 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 320 and rec1.x() <= 340 and rec1.y() > 95 and rec1.y() <= 195):
                self.label1.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
                if rec1.y() == 125:
                    self.poeniPL1 += 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 400 and rec1.x() <= 420 and rec1.y() > 0 and rec1.y() <= 95):
                self.label1.setGeometry(rec1.x(), rec1.y() - 5, rec1.width(), rec1.height())
                if rec1.y() == 5:
                    self.poeniPL1 += 1
                    self.playerRez11.setText(str(self.poeniPL1))
        elif key == Qt.Key_Down:
            if (rec1.x() >= 445 and rec1.x() <= 465 and rec1.y() >= 385 and rec1.y() < 475):
                self.label1.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
                if rec1.y() == 395:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 290 and rec1.x() <= 310 and rec1.y() >= 290 and rec1.y() < 385):
                self.label1.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
                if rec1.y() == 305:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 620 and rec1.x() <= 640 and rec1.y() >= 195 and rec1.y() < 290):
                self.label1.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
                if rec1.y() == 215:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 320 and rec1.x() <= 340 and rec1.y() >= 95 and rec1.y() < 195):
                self.label1.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
                if rec1.y() == 125:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))
            elif (rec1.x() >= 400 and rec1.x() <= 420 and rec1.y() >= 0 and rec1.y() < 95):
                self.label1.setGeometry(rec1.x(), rec1.y() + 5, rec1.width(), rec1.height())
                if rec1.y() == 5:
                    self.poeniPL1 -= 1
                    self.playerRez11.setText(str(self.poeniPL1))

    def __update_position2__(self, key):
        rec2 = self.label30.geometry()

        if key == Qt.Key_D:
            self.label30.setPixmap(self.pix112)
        elif key == Qt.Key_A:
            self.label30.setPixmap(self.pix12)

        if key == Qt.Key_M and self.player2.player_type == "Mario":
            while self.count4 < 1:
                self.count4 += 1
                if self.lives2 > 0:
                    self.lives2 *= 2
                    self.labelLifes2.setText(str(self.lives2))

        if key == Qt.Key_L and self.player2.player_type == "Luigi":
            while self.count5 < 1:
                self.count5 += 1
                if self.poeniPL2 > 0:
                    self.poeniPL2 *= 2
                    self.playerRez22.setText(str(self.poeniPL2))

        if key == Qt.Key_B and self.player2.player_type == "Bowser":
            while self.count6 < 1:
                self.count6 += 1
                if self.poeniPL1 > 0:
                    self.poeniPL1 -= 2
                    self.playerRez11.setText(str(self.poeniPL1))

        if key == Qt.Key_V and self.player2.player_type == "Wario":
            while self.count7 < 1:
                self.count7 += 1
                if self.lives1 > 0:
                    self.lives1 -= 1
                    self.labelLifes1.setText(str(self.lives1))



        if key == Qt.Key_D and rec2.x() <= 660 and (
                rec2.y() == 475 or (rec2.y() == 380 and rec2.x() <= 640) or (rec2.y() == 285 and rec2.x() <= 630) or (
                rec2.y() == 185 and rec2.x() <= 610) or (rec2.y() == 95 and rec2.x() <= 580) or (
                        rec2.y() == 0 and rec2.x() <= 540)):
            self.label30.setGeometry(rec2.x() + 5, rec2.y(), rec2.width(), rec2.height())
        elif key == Qt.Key_A and rec2.x() >= 280 and (
                rec2.y() == 475 or (rec2.y() == 380 and rec2.x() >= 300) or (rec2.y() == 285 and rec2.x() >= 310) or (
                rec2.y() == 185 and rec2.x() >= 330) or (rec2.y() == 95 and rec2.x() >= 340) or (
                        rec2.y() == 0 and rec2.x() >= 380)):
            self.label30.setGeometry(rec2.x() - 5, rec2.y(), rec2.width(), rec2.height())
        elif key == Qt.Key_W:
            if (rec2.x() >= 445 and rec2.x() <= 465 and rec2.y() > 380 and rec2.y() <= 475):
                self.label30.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
                if rec2.y() == 395:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 290 and rec2.x() <= 310 and rec2.y() > 285 and rec2.y() <= 380):
                self.label30.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
                if rec2.y() == 305:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 620 and rec2.x() <= 640 and rec2.y() > 185 and rec2.y() <= 285):
                self.label30.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
                if rec2.y() == 215:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 320 and rec2.x() <= 340 and rec2.y() > 95 and rec2.y() <= 185):
                self.label30.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
                if rec2.y() == 125:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 400 and rec2.x() <= 420 and rec2.y() > 0 and rec2.y() <= 95):
                self.label30.setGeometry(rec2.x(), rec2.y() - 5, rec2.width(), rec2.height())
                if rec2.y() == -5:
                    self.poeniPL2 += 1
                    self.playerRez22.setText(str(self.poeniPL2))
        elif key == Qt.Key_S:
            if (rec2.x() >= 445 and rec2.x() <= 465 and rec2.y() >= 380 and rec2.y() < 475):
                self.label30.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
                if rec2.y() == 395:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 290 and rec2.x() <= 310 and rec2.y() >= 285 and rec2.y() < 380):
                self.label30.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
                if rec2.y() == 305:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 620 and rec2.x() <= 640 and rec2.y() >= 185 and rec2.y() < 285):
                self.label30.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
                if rec2.y() == 215:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 320 and rec2.x() <= 340 and rec2.y() >= 95 and rec2.y() < 185):
                self.label30.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
                if rec2.y() == 125:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))
            elif (rec2.x() >= 400 and rec2.x() <= 420 and rec2.y() >= 0 and rec2.y() < 95):
                self.label30.setGeometry(rec2.x(), rec2.y() + 5, rec2.width(), rec2.height())
                if rec2.y() == -5:
                    self.poeniPL2 -= 1
                    self.playerRez22.setText(str(self.poeniPL2))

    def moveJasmin(self):
        self.timerP1 = QTimer(self)
        self.timerP1.start(2000)
        self.timerP1.timeout.connect(self.menjajSliku)
        if isHit(self.label2, self.label1) or isHit(self.label2, self.label30):
            if self.brojIgracaJedan:
                self.label1.setGeometry(280, 475, 75, 75)
                self.lives1 = 3
                self.trenutniNivo += 1
                self.labelLifes1.setText(str(self.lives1))
                self.labelLevel.setText(str(self.trenutniNivo))
            else:
                if isHit(self.label2, self.label1) and isHit(self.label2, self.label30):  # self.prvi and self.drugi:
                    self.trenutniNivo += 1
                    self.labelLevel.setText(str(self.trenutniNivo))
                    self.label1.setGeometry(280, 475, 75, 75)
                    self.label30.setGeometry(660, 475, 75, 75)
                    self.label30.show()
                    self.label1.show()
                    self.drugi = False
                    self.prvi = False

                elif isHit(self.label2, self.label1):
                    self.label1.hide()
                    self.prvi = True
                    self.lives1 = 3
                    self.labelLifes1.setText(str(self.lives1))

                elif isHit(self.label2, self.label30):
                    self.label30.hide()
                    self.drugi = True
                    self.lives2 = 3
                    self.labelLifes2.setText(str(self.lives2))

        if self.lives1 == 0:
            self.label1.setGeometry(200, 475, 75, 75)
            self.label1.hide()
        elif self.lives2 == 0:
            self.label30.setGeometry(200, 475, 75, 75)
            self.label30.hide()

        if self.lives1 == 0 and self.drugi:
            self.drugi = False
            self.trenutniNivo += 1
            self.label30.setGeometry(660, 475, 75, 75)
            self.labelLevel.setText(str(self.trenutniNivo))
            self.label30.show()
            self.izgubioPrvi = True

        if self.lives2 == 0 and self.prvi:
            self.prvi = False
            self.label1.setGeometry(280, 475, 75, 75)
            self.trenutniNivo += 1
            self.labelLevel.setText(str(self.trenutniNivo))
            self.label1.show()
            self.izgubioDrugi = True

        if self.lives1 <= 0 and self.lives2 <= 0:
            if self.izgubioPrvi:
                if not self.tournament:
                    self.write_high_score(self.player2.name, self.poeniPL2, 2)  # dodao
                    self.kraj = GameOver(2, self.poeniPL2, menu=self.menu)
                else:
                    self.tournament_logic(self.player2)

            else:
                if not self.tournament:
                    self.write_high_score(self.player1.name, self.poeniPL1, 2)
                    self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                else:
                    self.tournament_logic(self.player1)
            if not self.tournament:
                self.stop()

    def write_high_score(self, ime, score, br_igr):
        with open("highscore.csv", "a+", newline="") as f:
            high_score_writer = csv.writer(f, delimiter=',')
            high_score_writer.writerow([ime, score, br_igr])

        mykey = encryptor.key_create()

        encryptor.key_write(mykey, 'mykey.key')

        loaded_key = encryptor.key_load('mykey.key')

        encryptor.file_encrypt(loaded_key, 'highscore.csv', 'enc_highscore.csv')

    def tournament_logic(self, player_pobedio):
        self.tournamentLabel.setText(
            str(self.tournamentLabel.text()) + "\n" + str(self.br_igr) + ". " + player_pobedio.name + " wins!")
        self.br_igr += 1
        self.pobednici.append(player_pobedio.player_type)
        for barrel in self.barrels:
            barrel.setGeometry(2000, 2000, 5, 5)
            barrel.hide()
        self.barrels.clear()
        if self.br_igr == 2:
            self.player1 = self.next_player1
            self.player2 = self.next_player2

            self.pix1 = QPixmap(self.next_player1.pic_left)  # ikonice za igrace
            self.pix11 = QPixmap(self.next_player1.pic_right)
            self.pix12 = QPixmap(self.next_player2.pic_left)
            self.pix112 = QPixmap(self.next_player2.pic_right)

            self.label1.setPixmap(self.pix1)
            self.label30.setPixmap(self.pix12)

            self.label1.setGeometry(280, 475, 75, 75)  # label igrac 1
            self.label30.setGeometry(660, 475, 75, 75)
            self.poeniPL1 = 0  # poeni
            self.poeniPL2 = 0
            self.playerRez11.setText(str(self.poeniPL1))
            self.playerRez22.setText(str(self.poeniPL2))
            self.playerRez1.setText(self.player1.name)
            self.playerRez2.setText(self.player2.name)

            self.lives1 = 3
            self.labelLifes1.setText(str(self.lives1))

            self.lives2 = 3
            self.labelLifes2.setText(str(self.lives2))

            self.label1.show()
            self.label30.show()


        elif self.br_igr == 3:
            self.player1 = Player(self.pobednici[0], self.pobednici[0])
            self.player2 = Player(self.pobednici[1], self.pobednici[1])
            self.pix1 = QPixmap(self.player1.pic_left)  # ikonice za igrace
            self.pix11 = QPixmap(self.player1.pic_right)
            self.pix12 = QPixmap(self.player2.pic_left)
            self.pix112 = QPixmap(self.player2.pic_right)

            self.label1.setPixmap(self.pix1)
            self.label30.setPixmap(self.pix12)

            self.label1.setGeometry(280, 475, 75, 75)  # label igrac 1
            self.label30.setGeometry(660, 475, 75, 75)
            self.poeniPL1 = 0  # poeni
            self.poeniPL2 = 0
            self.playerRez11.setText(str(self.poeniPL1))
            self.playerRez22.setText(str(self.poeniPL2))
            self.playerRez1.setText(self.player1.name)
            self.playerRez2.setText(self.player2.name)

            self.lives1 = 3
            self.labelLifes1.setText(str(self.lives1))

            self.lives2 = 3
            self.labelLifes2.setText(str(self.lives2))

            self.label1.show()
            self.label30.show()

        else:
            self.kraj = GameOver(1, self.poeniPL1, menu=self.menu, tournament_winner=player_pobedio)
            self.stop()

    def menjajSliku(self):
        if self.promenioSliku:
            self.label2.setPixmap(self.pix22)
            self.promenioSliku = False
        else:
            self.label2.setPixmap(self.pix2)
            self.promenioSliku = True

    def moveGorila(self):
        rec2 = self.label3.geometry()

        if (rec2.x() >= 580):
            self.hitSide = True
        elif (rec2.x() <= 320):
            self.hitSide = False

        a = randint(0, 100)
        if a % 15 == 0:
            self.hitSide = True

        b = randint(0, 100)
        if b % 13 == 0:
            self.hitSide = False

        if (self.hitSide):
            self.label3.setGeometry(rec2.x() - 10, rec2.y(), rec2.width(), rec2.height())
            self.label3.setPixmap(self.pix3)
        else:
            self.label3.setGeometry(rec2.x() + 10, rec2.y(), rec2.width(), rec2.height())
            self.label3.setPixmap(self.pix32)

        if isHit(self.label1, self.label3):
            if self.lives1 > 0:
                self.lives1 -= 1
                self.labelLifes1.setText(str(self.lives1))
                if self.lives1 == 0:
                    if self.brojIgracaJedan:
                        self.write_high_score(self.player1.name, self.poeniPL1, 1)
                        self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                        self.stop()
                    else:
                        self.label1.setGeometry(200, 475, 75, 75)
                        self.label1.hide()

                        if self.izgubioDrugi:
                            if not self.tournament:
                                self.write_high_score(self.player1.name, self.poeniPL1, 2)
                                self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                                self.stop()
                            else:
                                self.tournament_logic(self.player1)
                        else:
                            self.izgubioPrvi = True

        if isHit(self.label30, self.label3):
            if self.lives2 > 0:
                self.lives2 -= 1
                self.labelLifes2.setText(str(self.lives2))
                if self.lives2 == 0:
                    self.label30.setGeometry(200, 475, 75, 75)
                    self.label30.hide()

                    if self.izgubioPrvi:
                        if not self.tournament:
                            self.write_high_score(self.player2.name, self.poeniPL2, 2)
                            self.kraj = GameOver(2, self.poeniPL2, menu=self.menu)
                            self.stop()
                        else:
                            self.tournament_logic(self.player2)
                    else:
                        self.izgubioDrugi = True

        if not self.zaustavio:
            self.gorilaStop.put(1)
            self.zaustavio = True
            return
        else:
            if self.gorilaStart.empty():
                return
            else:
                a = self.gorilaStart.get()
            self.zaustavio = False

    def moveBarrels(self):
        rec = self.label3.geometry()

        a = randint(0, 100)
        if a % 12 == 0:
            barrel = QLabel(self)
            self.barrels.append(barrel)
            self.barrels[len(self.barrels) - 1].setPixmap(self.pix4)
            self.barrels[len(self.barrels) - 1].setGeometry(rec.x(), rec.y(), 40, 40)
            self.barrels[len(self.barrels) - 1].show()

        for barrel in self.barrels:
            recb = barrel.geometry()
            barrel.setGeometry(recb.x(), recb.y() + 10, recb.width(), recb.height())

            if recb.y() > 600:
                barrel.hide()
                self.barrels.remove(barrel)

            if isHit(barrel, self.label1):
                if self.lives1 > 0:
                    self.lives1 -= 1
                    self.labelLifes1.setText(str(self.lives1))
                    barrel.hide()
                    self.barrels.remove(barrel)

                    if self.lives1 == 0:
                        if self.brojIgracaJedan:
                            self.write_high_score(self.player1.name, self.poeniPL1, 1)
                            self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                            self.stop()
                        else:
                            self.label1.setGeometry(200, 475, 75, 75)
                            self.label1.hide()

                            if self.izgubioDrugi:
                                if not self.tournament:
                                    self.write_high_score(self.player1.name, self.poeniPL1, 1)
                                    self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                                    self.stop()
                                else:
                                    self.tournament_logic(self.player1)
                            else:
                                self.izgubioPrvi = True

            if isHit(barrel, self.label30):
                if self.lives2 > 0:
                    self.lives2 -= 1
                    self.labelLifes2.setText(str(self.lives2))
                    barrel.hide()
                    try:
                        self.barrels.remove(barrel)
                    except:
                        pass

                    if self.lives2 == 0:
                        self.label30.setGeometry(200, 475, 75, 75)
                        self.label30.hide()

                        if self.izgubioPrvi:
                            if not self.tournament:
                                self.write_high_score(self.player2.name, self.poeniPL2, 2)
                                self.kraj = GameOver(2, self.poeniPL2, menu=self.menu)
                                self.stop()
                            else:
                                self.tournament_logic(self.player2)
                        else:
                            self.izgubioDrugi = True

    def generateForce(self):

        self.heart.setGeometry(randint(300, 600), 310, 40, 40)
        self.heart.show()

        self.timerP3 = QTimer(self)
        self.timerP3.start(7000)
        self.timerP3.timeout.connect(self.sakrij)

        # for heart in self.hearts:
        if isHit(self.heart, self.label1):
            self.lives1 += randint(-2, 2)
            self.labelLifes1.setText(str(self.lives1))
            self.heart.hide()
            # self.hearts.remove(heart)

            if self.lives1 <= 0:
                if self.brojIgracaJedan:
                    self.write_high_score(self.player1.name, self.poeniPL1, 1)
                    self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                    self.stop()
                else:
                    self.label1.setGeometry(200, 40, 75, 75)
                    self.label1.hide()
                    self.lives1 = 0
                    self.labelLifes1.setText(str(self.lives1))

                    if self.izgubioDrugi:
                        if not self.tournament:
                            self.write_high_score(self.player1.name, self.poeniPL1, 1)
                            self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                            self.stop()
                        else:
                            self.tournament_logic(self.player1)
                    else:
                        self.izgubioPrvi = True

        if isHit(self.heart, self.label30):
            self.lives2 += randint(-2, 2)
            self.labelLifes2.setText(str(self.lives2))
            self.heart.hide()
            # self.hearts.remove(heart)

            if self.lives2 <= 0:
                self.lives2 = 0
                self.labelLifes2.setText(str(self.lives2))
                self.label30.setGeometry(200, 40, 75, 75)
                self.label30.hide()

                if self.izgubioPrvi:
                    if not self.tournament:
                        self.write_high_score(self.player2.name, self.poeniPL2, 2)
                        self.kraj = GameOver(2, self.poeniPL2, menu=self.menu)
                        self.stop()
                    else:
                        self.tournament_logic(self.player2)
                else:
                    self.izgubioDrugi = True

    def generateBombs(self):

        self.bomb.setGeometry(randint(300, 600), 420, 40, 40)
        self.bomb.show()

        if self.trenutniNivo < 2:
            self.bomb.setGeometry(1, 1, 1, 1)
            self.bomb.hide()

        if isHit(self.bomb, self.label1):
            self.lives1 -= 2
            self.labelLifes1.setText(str(self.lives1))
            self.bomb.hide()

            if self.lives1 <= 0:
                if self.brojIgracaJedan:
                    self.write_high_score(self.player1.name, self.poeniPL1, 1)
                    self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                    self.stop()
                else:
                    self.label1.setGeometry(200, 40, 75, 75)
                    self.label1.hide()
                    self.lives1 = 0
                    self.labelLifes1.setText(str(self.lives1))

                    if self.izgubioDrugi:
                        if not self.tournament:
                            self.write_high_score(self.player1.name, self.poeniPL1, 1)
                            self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                            self.stop()
                        else:
                            self.tournament_logic(self.player1)
                    else:
                        self.izgubioPrvi = True

        if isHit(self.bomb, self.label30):
            self.lives2 -= 2
            self.labelLifes2.setText(str(self.lives2))
            self.bomb.hide()

            if self.lives2 <= 0:
                self.lives2 = 0
                self.labelLifes2.setText(str(self.lives2))
                self.label30.setGeometry(200, 40, 75, 75)
                self.label30.hide()

                if self.izgubioPrvi:
                    if not self.tournament:
                        self.write_high_score(self.player2.name, self.poeniPL2, 2)
                        self.kraj = GameOver(2, self.poeniPL2, menu=self.menu)
                        self.stop()
                    else:
                        self.tournament_logic(self.player2)
                else:
                    self.izgubioDrugi = True

    def generateLights(self):
        self.lightbolt.setGeometry(randint(350, 600), 220, 40, 40)
        self.lightbolt.show()

        if self.trenutniNivo < 3:
            self.lightbolt.setGeometry(1, 1, 1, 1)
            self.lightbolt.hide()

        if isHit(self.lightbolt, self.label1):
            self.lives1 -= 1
            self.labelLifes1.setText(str(self.lives1))
            self.lightbolt.hide()

            if self.lives1 <= 0:
                if self.brojIgracaJedan:
                    self.write_high_score(self.player1.name, self.poeniPL1, 1)
                    self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                    self.stop()
                else:
                    self.label1.setGeometry(200, 40, 75, 75)
                    self.label1.hide()
                    self.lives1 = 0
                    self.labelLifes1.setText(str(self.lives1))

                    if self.izgubioDrugi:
                        if not self.tournament:
                            self.write_high_score(self.player1.name, self.poeniPL1, 1)
                            self.kraj = GameOver(1, self.poeniPL1, menu=self.menu)
                            self.stop()
                        else:
                            self.tournament_logic(self.player1)
                    else:
                        self.izgubioPrvi = True

        if isHit(self.lightbolt, self.label30):
            self.lives2 -= 1
            self.labelLifes2.setText(str(self.lives2))
            self.lightbolt.hide()

            if self.lives2 <= 0:
                self.lives2 = 0
                self.labelLifes2.setText(str(self.lives2))
                self.label30.setGeometry(200, 40, 75, 75)
                self.label30.hide()

                if self.izgubioPrvi:
                    if not self.tournament:
                        self.write_high_score(self.player2.name, self.poeniPL2, 2)
                        self.kraj = GameOver(2, self.poeniPL2, menu=self.menu)
                        self.stop()
                    else:
                        self.tournament_logic(self.player2)
                else:
                    self.izgubioDrugi = True

    def sakrij(self):
        self.heart.hide()

    def stop(self):
        self.jasminMovement.die()
        self.gorilaMovement.die()
        self.barrelProcess.terminate()
        self.heartsMovement.die()
        self.bombsMovement.die()
        self.lightsMovement.die()
        self.movingBarrels.die()
        self.gorilaBug.terminate()
        self.key_notifier.die()
        self.timerP3.stop()
        self.timerP1.stop()

        if not self.brojIgracaJedan:
            self.key_notifier2.die()
        self.close()

    def shutdown(self, event):
        # self.barrelProcess.terminate()
        # self.gorilaBug.terminate()
        self.menu.show()
        self.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimMoveDemo(1, 1)
    sys.exit(app.exec_())
