import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtCore import QCoreApplication

class MyApp(QWidget):

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
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Connect to Server')
        self.setGeometry(1000, 500, 500, 350)
        self.show()


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

