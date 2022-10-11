import socket
import threading
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Chat Client')
        self.setGeometry(750, 250, 1200, 750)
        self.show()


class Login(QWidget):

    def __init__(self):
        super().__init__()

        self.w = None

        self.initUI()

    def initUI(self):
        # IP Address input
        ip_address_edit = QLineEdit(self)
        ip_address_edit.setAlignment(Qt.AlignCenter)
        ip_label = QLabel('Enter server IP', self)
        ip_label.setAlignment(Qt.AlignCenter)

        # Port input
        port_edit = QLineEdit(self)
        port_edit.setAlignment(Qt.AlignCenter)
        port_label = QLabel('Enter server port', self)
        port_label.setAlignment(Qt.AlignCenter)

        # Nickname input
        nickname_edit = QLineEdit(self)
        nickname_edit.setAlignment(Qt.AlignCenter)
        nickname_label = QLabel('Enter a nickname', self)
        nickname_label.setAlignment(Qt.AlignCenter)

        # Connect button
        connect_button = QPushButton('Connect', self)
        connect_button.clicked.connect(self.connect_button_on_click)

        vbox = QVBoxLayout()
        vbox.addWidget(ip_label)
        vbox.addWidget(ip_address_edit)
        vbox.addWidget(port_label)
        vbox.addWidget(port_edit)
        vbox.addWidget(nickname_label)
        vbox.addWidget(nickname_edit)
        vbox.addStretch(1)
        vbox.addWidget(connect_button)

        self.setLayout(vbox)

        self.setWindowTitle('Connect to Server')
        self.setGeometry(750, 250, 500, 350)
        self.show()

    def connect_button_on_click(self):
        self.w = MainScreen()
        self.w.show()


# # Listen to server
# def receive():
#     while True:
#         try:
#             message = client.recv(1024).decode('ascii')
#             if message == 'NICK':
#                 client.send(nickname.encode('ascii'))
#             else:
#                 print(message)
#         except:
#             print("error occucred while listening to server")
#             client.close()
#             break

# # Send messages to the server
# def write():
#     while True:
#         message = f'{nickname}: {input()}'
#         client.send(message.encode('ascii'))

host = '127.0.0.1'
port = 42000

if __name__ == '__main__':
    try:
        # nickname = input("Choose your nickname:")

        # # Connect to server
        # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # client.connect((host, port))

        # # Start receive thread
        # receive_thread = threading.Thread(target=receive)
        # receive_thread.start()

        # # Start writing thread
        # write_thread = threading.Thread(target=write)
        # write_thread.start()

        app = QApplication(sys.argv)
        ex = Login()
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        # client.close()
        sys.exit(app.exec_())
