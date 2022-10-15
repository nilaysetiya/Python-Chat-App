import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Frontend.OneOnOneChat import OneOnOneChat
from Frontend.GroupChat import GroupChat


class MainScreen(QWidget):
    def __init__(self, parent, nickname):
        super().__init__()

        self.parent = parent
        self.one_on_one_chat = None
        self.group_chat = None
        self.nickname = nickname

        self.initUI()

    def initUI(self):

        self.connected_clients_list = QListWidget()
        self.rooms_list = QListWidget()

        # Buttons
        one_on_one_button = QPushButton('Chat', self)
        one_on_one_button.pressed.connect(self.start_one_on_one_chat)

        create_room_button = QPushButton('Create Room', self)
        create_room_button.pressed.connect(self.create_room)
        join_room_button = QPushButton('Join Room', self)
        join_room_button.pressed.connect(self.start_room_chat)
        grid = QGridLayout()
        self.setLayout(grid)

        # Labels
        connected_clients_label = QLabel('Connected Clients', self)
        connected_clients_label.setFont(QFont('Ariel', 18))
        rooms_label = QLabel('Available Rooms', self)
        rooms_label.setFont(QFont('Ariel', 18))

        grid.addWidget(connected_clients_label, 0, 0)
        grid.addWidget(self.connected_clients_list, 1, 0)
        grid.addWidget(rooms_label, 2, 0)
        grid.addWidget(self.rooms_list, 3, 0)

        grid.addWidget(one_on_one_button, 1, 1)
        grid.addWidget(create_room_button, 2, 1)
        grid.addWidget(join_room_button, 3, 1)

        self.setWindowTitle('Chat Client - Logged in as: ' + self.nickname)
        self.setGeometry(750, 250, 600, 750)
        self.show()

    def add_client(self, client_name):
        self.connected_clients_list.addItem(client_name)

    def start_one_on_one_chat(self):
        if self.connected_clients_list.currentItem() is not None:
            self.one_on_one_chat = OneOnOneChat(self, self.nickname, self.connected_clients_list.currentItem().text())
            self.one_on_one_chat.show()
            self.close()

    def create_room(self):
        msg = f'CREATE_ROOM:{self.nickname}'
        self.parent.send_create_room_to_server(msg)

    def add_room(self, room_name):
        self.rooms_list.addItem(room_name)

    def start_room_chat(self):
        if self.rooms_list.currentItem() is not None:
            list_of_clients = []
            for i in range(self.connected_clients_list.count()):
                list_of_clients.append(self.connected_clients_list.item(i).text())
            self.group_chat = GroupChat(
                self, self.nickname,
                self.rooms_list.currentItem().text(),
                list_of_clients
            )
            self.group_chat.show()
            self.close()

    def get_group_chat(self):
        return self.group_chat
