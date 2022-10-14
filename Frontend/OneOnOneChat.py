import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class OneOnOneChat(QWidget):

    def __init__(self, parent, nickname, chat_with):
        super().__init__()
        self.parent = parent
        self.chat_box = QTextBrowser()
        self.line_edit = QLineEdit()

        self.nickname = nickname
        self.chat_with = chat_with

        self.initUI()

    def initUI(self):
        chat_with_label = QLabel(('Chatting with ' + self.chat_with), self)
        chat_with_label.setFont(QFont('Ariel', 18))

        send_button = QPushButton('Send')
        send_button.pressed.connect(self.send_to_client)
        send_img_button = QPushButton('Send Image')
        close_button = QPushButton('Close')
        close_button.pressed.connect(self.back_to_main)

        hbox = QHBoxLayout()
        hbox.addWidget(self.line_edit)
        hbox.addWidget(send_button)
        hbox.addWidget(send_img_button)

        vbox = QVBoxLayout()
        vbox.addWidget(chat_with_label)
        vbox.addWidget(self.chat_box)
        vbox.addLayout(hbox)
        vbox.addWidget(close_button)

        self.setLayout(vbox)

        self.setWindowTitle('Chat Client - Logged in as: ' + self.nickname)
        self.setGeometry(750, 250, 600, 750)
        self.show()

    def send_to_client(self):
        if self.line_edit.text() is not None:
            self.chat_box.append(self.nickname + ': ' + self.line_edit.text())
            msg = f'ONE_ON_ONE:{self.chat_with}:{self.nickname}: {self.line_edit.text()}'
            self.parent.parent.send_one_on_one_to_server(msg)
            self.line_edit.clear()

    def back_to_main(self):
        self.parent.show()
        self.close()

