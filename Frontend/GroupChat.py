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
        self.update_client_list()

    def initUI(self):
        self.chat_box.setAcceptRichText(True)
        self.chat_box.setOpenExternalLinks(True)

        send_button = QPushButton('Send')
        send_button.pressed.connect(self.send_message)
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
        popup = AddClientToRoom(self, self.room_name, self.list_of_clients, self.nickname)
        popup.show()

    def send_message(self):
        if self.line_edit.text() is not None:
            message = f'{self.nickname}:{self.line_edit.text()}'
            msg = f'ROOM_MSG:{self.room_name}:{message}'
            self.parent.parent.send_room_message_to_server(msg)
            self.line_edit.clear()

    def update_client_list(self):
        print("update client list")
        msg = f'UPDATE_ROOM_LIST:{self.room_name}'
        print(msg)
        self.parent.parent.send_room_message_to_server(msg)


class AddClientToRoom(QDialog):
    def __init__(self, parent, room_name, list_of_clients, nickname):
        super().__init__(parent)
        self.parent = parent
        self.resize(400, 500)
        self.list_of_clients = list_of_clients
        self.room_name = room_name
        self.nickname = nickname
        self.selected_user = None
        self.client_list = QListWidget()
        self.initUI()

    def initUI(self):
        add_button = QPushButton('Add', self)
        add_button.pressed.connect(self.inv_client)
        vbox = QVBoxLayout()

        for client in self.list_of_clients:
            self.client_list.addItem(client)

        label = QLabel('Select a User to add to this chat', self)

        vbox.addWidget(label)
        vbox.addWidget(self.client_list)
        vbox.addWidget(add_button)
        self.setLayout(vbox)

    def inv_client(self):
        if self.client_list.currentItem() is not None:
            current_client = self.client_list.currentItem().text()
            msg = f'ADD_CLIENT_ROOM:{self.room_name}:{current_client}:{self.nickname}'
            self.parent.parent.parent.add_client_to_room(msg)
            self.close()


