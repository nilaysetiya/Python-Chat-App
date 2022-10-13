import socket
import threading
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Frontend.MainScreen import MainScreen


class Login(QWidget):

    def __init__(self):
        super().__init__()

        self.w = None

        self.nickname_edit = QLineEdit(self)
        self.ip_address_edit = QLineEdit(self)
        self.port_edit = QLineEdit(self)

        self.initUI()

    def initUI(self):
        # Main Title
        title_label = QLabel('Login into chat app!', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Ariel', 18))

        # IP Address input
        self.ip_address_edit.setAlignment(Qt.AlignCenter)
        ip_label = QLabel('Enter server IP', self)
        ip_label.setAlignment(Qt.AlignCenter)

        # Port input
        self.port_edit.setAlignment(Qt.AlignCenter)
        port_label = QLabel('Enter server port', self)
        port_label.setAlignment(Qt.AlignCenter)

        # Nickname input
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
        start_server(
            self.ip_address_edit.text(),
            int(self.port_edit.text()),
            self.nickname_edit.text()
        )


def start_server(ip_address, port_no, nick):

    global host
    global port
    global nickname

    host = ip_address
    port = port_no
    nickname = nick

    # Connect to server
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Start receive thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # Start writing thread
    write_thread = threading.Thread(target=write)
    write_thread.start()


# Listen to server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif 'NEW_CLIENT_ADDED' in message:
                arr = message.split(':')
                print(arr)
                ex.w.add_client(arr[1])
            elif 'ADD_EXISTING_CLIENTS' in message:
                arr = message.split(':')
                print(arr)
                for i in range(1, len(arr)):
                    if arr[i] != '':
                        ex.w.add_client(arr[i])
            else:
                print(message)
        except:
            print("error occurred while listening to server")
            client.close()
            break


# Send messages to the server
def write():
    while True:
        message = f'{nickname}: {input()}'
        client.send(message.encode('ascii'))


host = ''
port = 0
nickname = ''
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if __name__ == '__main__':
    try:
        # nickname = input("Choose your nickname:")
        app = QApplication(sys.argv)
        ex = Login()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        client.close()
        sys.exit(app.exec_())
