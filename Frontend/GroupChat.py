from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class GroupChat(QWidget):

    def __init__(self, parent, nickname, room_name, list_of_clients):
        super().__init__()
        self.parent = parent
        self.nickname = nickname
        self.room_name = room_name
        self.list_of_clients = list_of_clients
        print("list of clients: " + str(self.list_of_clients))
        self.client_list = QListWidget()
        self.chat_box = QTextBrowser()
        self.line_edit = QLineEdit()

        self.initUI()

    def initUI(self):
        send_button = QPushButton('Send')
        send_img_button = QPushButton('Send Image')
        close_button = QPushButton('Close')
        close_button.pressed.connect(self.back_to_main)
        invite_button = QPushButton('Invite')
        invite_button.pressed.connect(self.add_user)

        hbox = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox.addWidget(self.line_edit)
        hbox.addWidget(send_button)
        hbox.addWidget(send_img_button)

        vbox = QVBoxLayout()
        hbox1.addWidget(self.chat_box, 7)
        hbox1.addWidget(self.client_list, 3)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox)
        hbox2.addWidget(close_button)
        hbox2.addWidget(invite_button)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        self.setWindowTitle('Chat Client - Logged in as: ' + self.nickname)
        self.setGeometry(750, 250, 600, 750)
        self.show()

    def back_to_main(self):
        self.parent.show()
        self.close()

    def add_user(self):
        popup = AddClientToRoom(self, self.list_of_clients)
        popup.show()


class AddClientToRoom(QDialog):
    def __init__(self, parent, list_of_clients):
        super().__init__(parent)
        self.resize(400, 500)
        self.list_of_clients = list_of_clients
        self.client_list = QListWidget()
        self.initUI()

    def initUI(self):
        add_button = QPushButton('Add', self)
        vbox = QVBoxLayout()

        for client in self.list_of_clients:
            self.client_list.addItem(client)

        label = QLabel('Select a User to add to this chat', self)

        vbox.addWidget(label)
        vbox.addWidget(self.client_list)
        vbox.addWidget(add_button)
        self.setLayout(vbox)


