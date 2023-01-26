import csv
import sys
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton
from PyQt5 import Qt
from Encryptor import Encryptor

encryptor = Encryptor()


class HighScore(QMainWindow):

    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.labelHighScore = QLabel(self)
        self.high_score_img = QPixmap('images\\highscore.png')
        self.labelHighScore.setPixmap(self.high_score_img)
        self.labelHighScore.setGeometry(70, 50, 395, 43)
        self.setStyleSheet("background: black;")


        self.left = 400
        self.top = 200
        self.width = 450
        self.height = 470
        palette = QPalette()
        self.setPalette(palette)

        self.__init_ui__()

    def __init_ui__(self):
        self.setGeometry(self.left, self.top, self.width, self.height)


        self.setWindowTitle("High Score")

        self.label1Igrac = QLabel(self)
        self.label1Igrac.setText("1 Player:")
        self.label1Igrac.setGeometry(100, 100,100, 500)
        self.label1Igrac.setAlignment(Qt.Qt.AlignTop)
        self.label1Igrac.setStyleSheet("color: cyan;")


        self.ispis1Igrac = QLabel(self)
        self.ispis1Igrac.setText(self.format_high_score(self.generate_top_10_list(1)))
        self.ispis1Igrac.setGeometry(100, 120,100, 500)
        self.ispis1Igrac.setAlignment(Qt.Qt.AlignTop)
        self.ispis1Igrac.setStyleSheet("color: cyan;")

        self.label2Igrac = QLabel(self)
        self.label2Igrac.setText("2 Player:")
        self.label2Igrac.setGeometry(250, 100, 100, 500)
        self.label2Igrac.setAlignment(Qt.Qt.AlignTop)
        self.label2Igrac.setStyleSheet("color: cyan;")


        self.ispis2Igrac = QLabel(self)
        self.ispis2Igrac.setText(self.format_high_score(self.generate_top_10_list(2)))
        self.ispis2Igrac.setGeometry(250, 120, 100, 500)
        self.ispis2Igrac.setAlignment(Qt.Qt.AlignTop)
        self.ispis2Igrac.setStyleSheet("color: cyan;")


        self.labelGoBack = QLabel(self)
        self.go_back_img = QPixmap('images\\goback.jpeg')
        self.labelGoBack.setPixmap(self.go_back_img)
        self.labelGoBack.setGeometry(115, 316, 395, 43)
        self.labelGoBack.mousePressEvent = self.go_back_on_click

        self.show()

    def generate_top_10_list(self, br_igr):
        loaded_key = encryptor.key_load('mykey.key')
        encryptor.file_decrypt(loaded_key, 'enc_highscore.csv', 'decrypted_highscore.csv')

        with open("decrypted_highscore.csv", "rt") as f:
            high_score_reader = csv.reader(f, delimiter=',')
            high_score_list = [[red[0], int(red[1])] for red in high_score_reader if int(red[2]) == br_igr]
            high_score_list.sort(reverse=True, key=lambda row: row[1])

        if len(high_score_list) <= 10:
            return high_score_list

        else:
            return high_score_list[0:10]


    def format_high_score(self, top_list):
        return "\n".join([row[0] + " " + str(row[1]) for row in top_list])

    def go_back_on_click(self, event):
        self.menu.show()
        self.close()


    def write_high_score(self, ime, score, br_igr):

        with open("highscore.csv", "a+", newline="") as f:
            high_score_writer = csv.writer(f, delimiter=',')
            high_score_writer.writerow([ime, score, br_igr])

        mykey = encryptor.key_create()

        encryptor.key_write(mykey, 'mykey.key')

        loaded_key = encryptor.key_load('mykey.key')

        encryptor.file_encrypt(loaded_key, 'highscore.csv', 'enc_highscore.csv')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HighScore()
    sys.exit(app.exec_())