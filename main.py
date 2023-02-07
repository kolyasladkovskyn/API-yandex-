import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('карты')

        self.text = QLabel("Координаты:", self)
        self.text.move(0, 0)

        self.ql1 = QLineEdit(self)
        self.ql1.move(0, 30)

        self.ql2 = QLineEdit(self)
        self.ql2.move(150, 30)

        self.text1 = QLabel("маштаб:", self)
        self.text1.move(0, 100)

        self.ql3 = QLineEdit(self)
        self.ql3.move(50, 100)

        self.but = QPushButton("готово", self)
        self.but.move(60, 150)
        self.but.clicked.connect(self.run)

    def run(self):
        map_params = {
            "ll": ",".join([int(self.ql1.text()), int(self.ql2.text())]),
            "spn": ",".join([int(self.ql3.text()), int(self.ql3.text())]),
            "l": "map"
        }
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
