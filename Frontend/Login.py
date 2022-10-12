import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Frontend.MainScreen import MainScreen
from client import start_server


class Login(QWidget):

    def __init__(self):
        super().__init__()

        self.w = None

        self.nickname_edit = None
        self.ip_address_edit = None
        self.port_edit = None

        self.initUI()

    def initUI(self):
        # Main Title
        title_label = QLabel('Login into chat app!', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Ariel', 18))

        # IP Address input
        self.ip_address_edit = QLineEdit(self)
        self.ip_address_edit.setAlignment(Qt.AlignCenter)
        ip_label = QLabel('Enter server IP', self)
        ip_label.setAlignment(Qt.AlignCenter)

        # Port input
        self.port_edit = QLineEdit(self)
        self.port_edit.setAlignment(Qt.AlignCenter)
        port_label = QLabel('Enter server port', self)
        port_label.setAlignment(Qt.AlignCenter)

        # Nickname input
        self.nickname_edit = QLineEdit(self)
        self.nickname_edit.setAlignment(Qt.AlignCenter)
        nickname_label = QLabel('Enter a nickname', self)
        nickname_label.setAlignment(Qt.AlignCenter)

        # Connect button
        connect_button = QPushButton('Connect', self)
        connect_button.clicked.connect(self.connect_button_on_click)

        vbox = QVBoxLayout()
        vbox.addWidget(title_label)
        vbox.addWidget(ip_label)
        vbox.addWidget(self.ip_address_edit)
        vbox.addWidget(port_label)
        vbox.addWidget(self.port_edit)
        vbox.addWidget(nickname_label)
        vbox.addWidget(self.nickname_edit)
        vbox.addStretch(1)
        vbox.addWidget(connect_button)

        self.setLayout(vbox)

        self.setWindowTitle('Connect to Server')
        self.setGeometry(750, 250, 500, 350)
        self.show()

    def connect_button_on_click(self):
        self.w = MainScreen(self)
        self.w.show()
        self.close()
        start_server()
