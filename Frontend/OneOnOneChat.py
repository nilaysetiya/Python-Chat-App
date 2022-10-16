
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from datetime import datetime


class OneOnOneChat(QWidget):

    def __init__(self, parent, nickname, chat_with):
        super().__init__()
        self.parent = parent
        self.chat_box = QTextBrowser()
        self.line_edit = QLineEdit()

        self.nickname = nickname
        self.chat_with = chat_with
        self.images = []
        self.initUI()

    def initUI(self):
        self.chat_box.setAcceptRichText(True)
        self.chat_box.setOpenExternalLinks(True)

        chat_with_label = QLabel(('Chatting with ' + self.chat_with), self)
        chat_with_label.setFont(QFont('Ariel', 18))

        send_button = QPushButton('Send')
        send_button.pressed.connect(self.send_to_client)
        close_button = QPushButton('Close')
        close_button.pressed.connect(self.back_to_main)
        download_img_button = QPushButton('View and Download Image')
        download_img_button.pressed.connect(self.show_img)
        attach_img_button = QPushButton('Attach Image')
        attach_img_button.pressed.connect(self.attach_file)

        hbox = QHBoxLayout()
        hbox1 = QHBoxLayout()
        hbox.addWidget(self.line_edit)
        hbox.addWidget(send_button)
        hbox1.addWidget(close_button)
        hbox1.addWidget(download_img_button)
        hbox1.addWidget(attach_img_button)

        vbox = QVBoxLayout()
        vbox.addWidget(chat_with_label)
        vbox.addWidget(self.chat_box)
        vbox.addLayout(hbox)
        vbox.addLayout(hbox1)

        self.setLayout(vbox)

        self.setWindowTitle('Chat Client - Logged in as: ' + self.nickname)
        self.setGeometry(750, 250, 600, 750)
        self.show()

    def send_to_client(self):
        if self.line_edit.text() is not None:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.chat_box.append(self.nickname + ' ' + current_time + ': ' + self.line_edit.text())
            msg = f'ONE_ON_ONE:{self.chat_with}:{self.nickname}: {self.line_edit.text()}'
            self.parent.parent.send_one_on_one_to_server(msg)
            self.line_edit.clear()

    def back_to_main(self):
        self.parent.show()
        self.close()

    def send_img_msg_to_client(self, fname):
        msg = f'ONE_ON_ONE:{self.chat_with}:{self.nickname}: Sent an Image {fname}'
        self.parent.parent.send_one_on_one_to_server(msg)

    def attach_file(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        file_name = QFileDialog.getOpenFileName(self, 'openfile', '')
        arr = file_name[0].split('/')
        fname = arr[-1]
        self.chat_box.append(self.nickname + '' + current_time + ': Sent an Image ' + fname)
        msg = f'IMAGE_FROM_CLIENT:{fname}:{self.chat_with}:{self.nickname}'
        self.send_img_msg_to_client(fname)
        self.parent.parent.send_image_to_server(msg, file_name[0])

    def show_img(self):
        print(self.images[-1])
        dlg = ImageDialog(self, f'Received_Files/{self.images[-1]}')
        dlg.show()

    def add_img(self, path):
        self.images.append(path)


class ImageDialog(QDialog):
    def __init__(self, parent, img_path):
        super().__init__(parent)

        self.img_lbl = QLabel()
        self.img_path = img_path
        self.load_img()
        layout = QVBoxLayout()
        layout.addWidget(self.img_lbl)
        self.setLayout(layout)

    def load_img(self):
        pixmap = QPixmap(self.img_path)
        self.img_lbl.setPixmap(QPixmap(pixmap))


