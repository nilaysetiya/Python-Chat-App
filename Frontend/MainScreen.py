import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainScreen(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.connected_clients_list = QListWidget()
        self.rooms_list = QListWidget()

        self.initUI()

    def initUI(self):
        # Buttons
        one_on_one_button = QPushButton('Chat', self)
        create_room_button = QPushButton('Create Room', self)
        join_room_button = QPushButton('Join Room', self)
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

        self.setWindowTitle('Chat Client')
        self.setGeometry(750, 250, 600, 750)
        self.show()

    def add_client(self, client_name):
        self.connected_clients_list.addItem(client_name)
