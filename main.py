import sys
import json
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
from API import API_KEY


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.maps_params = {
            'll': '',
            'size': '200,300',
            'l': 'map',
            'z': '8',
            'spn': '0.005,0.005',
            'pt': ''
        }

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('карты')

        self.text = QLabel("Координаты:", self)
        self.text.move(10, 0)

        self.text1 = QLabel("X", self)
        self.text1.move(10, 30)

        self.text2 = QLabel("Y", self)
        self.text2.move(10, 50)

        self.ql1 = QLineEdit(self)
        self.ql1.move(20, 25)

        self.ql2 = QLineEdit(self)
        self.ql2.move(20, 50)

        self.text3 = QLabel("Маштаб:", self)
        self.text3.move(10, 75)

        self.mashtab = QLineEdit(self)
        self.mashtab.move(10, 100)

        self.but = QPushButton("Готово", self)
        self.but.move(30, 130)
        self.but.clicked.connect(self.shower)

        self.Error = QLabel("")
        self.Error.move(20, 140)

        self.label = QLabel(self)
        self.label.size = 100
        self.label.move(50, 140)

    def show_st(self):
        self.maps_params['ll'] = ','.join([self.ql1.text(), self.ql2.text()])
        self.maps_params['spn'] = f'{self.mashtab.text()},{self.mashtab.text()}'
        self.show_map()

    def show_map(self):
        try:
            response = requests.get("https://static-maps.yandex.ru/1.x/",
                                    params=self.maps_params)
            with open("data/map.png", "wb") as file:
                file.write(response.content)
        except requests.exceptions.ConnectionError:
            self.Error.setText('Connection failed')
            self.Error.show()
        else:
            self.Error.hide()
            self.map = QPixmap('data/map.png')
            self.label.setPixmap(self.map)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
