import sys
import json
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap
from API import API_KEY

sys._excepthook = sys.excepthook  # save original excepthook


def exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)  # print exception.
    sys._excepthook(exctype, value, traceback)  # call original excepthoot. I do not why
    sys.exit(1)  # terminate program if above do not do this


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.maps_params = {
            'll': '',
            'size': '300,300',
            'l': 'map',
            'z': '8',
            'spn': '0.005,0.005',
            'pt': ''
        }

    def check_y(self, y):
        if y > 78.0:
            return str(0.0)
        elif y < 0:
            return str(78.0)
        return str(y)

    def check_x(self, x):
        if x < -179.0:
            return str(179.0)
        elif x > 179.0:
            return str(-179.0)
        return str(x)

    def keyPressEvent(self, event):
        try:
            key = event.key()
            super().keyPressEvent(event)
            # вверх с помощью W
            if key == 87:
                y = float(self.maps_params['ll'].split(',')[1]) + 0.5
                y = self.check_y(y)
                self.maps_params['ll'] = (self.maps_params['ll'].split(',')[0] + ',' + y)
            # вниз с помощью S
            elif key == 83:
                y = float(self.maps_params['ll'].split(',')[1]) - 0.5
                y = self.check_y(y)
                self.maps_params['ll'] = (self.maps_params['ll'].split(',')[0] + ',' + y)
            # вправо с помощью D
            elif key == 68:
                x = float(self.maps_params['ll'].split(',')[0]) + 2
                x = self.check_x(x)
                self.maps_params['ll'] = (x + ',' + self.maps_params['ll'].split(',')[1])
            # влево с помощью A
            elif key == 65:
                x = float(self.maps_params['ll'].split(',')[0]) - 2
                x = self.check_x(x)
                self.maps_params['ll'] = (x + ',' + self.maps_params['ll'].split(',')[1])
            # вверх маштаб
            elif key == 16777238:
                a = str(float(self.maps_params['spn'].split(',')[0]) + 5)
                self.maps_params['spn'] = (a + ',' + a)
            # вниз маштаб
            elif key == 16777239:
                a = str(float(self.maps_params['spn'].split(',')[0]) - 5)
                self.maps_params['spn'] = (a + ',' + a)
            self.show_map()
        except:
            self.Error.setText('Ошибка карты')

    def initUI(self):
        self.setGeometry(400, 400, 400, 500)
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
        self.but.clicked.connect(self.show_st)

        self.Error = QLabel("")
        self.Error.move(20, 140)

        self.label = QLabel(self)
        self.label.move(10, 160)

        self.schem_but = QPushButton("Схема", self)
        self.schem_but.move(170, 20)
        self.schem_but.clicked.connect(self.change_map_view_schem)
        self.sput_but = QPushButton("Спутник", self)
        self.sput_but.move(170, 50)
        self.sput_but.clicked.connect(self.change_map_view_sput)
        self.hybr_but = QPushButton("Гибрид", self)
        self.hybr_but.move(170, 80)
        self.hybr_but.clicked.connect(self.change_map_view_hybr)

    def change_map_view_schem(self):
        try:
            self.maps_params['l'] = 'map'
            self.show_map()
        except:
            pass

    def change_map_view_sput(self):
        try:
            self.maps_params['l'] = 'sat'
            self.show_map()
        except:
            pass

    def change_map_view_hybr(self):
        try:
            self.maps_params['l'] = 'sat,skl'
            self.show_map()
        except:
            pass

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
        else:
            self.map = QPixmap('./data/map.png')
            self.label.setPixmap(self.map)
            self.label.resize(300, 300)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
