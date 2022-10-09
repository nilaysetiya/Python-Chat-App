import re
import socket
import threading

host = '127.0.0.1'
port = 42000


# Listen to server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("error occucred while listening to server")
            client.close()
            break

# Send messages to the server
def write():
    while True:
        message = f'{nickname}: {input()}'
        client.send(message.encode('ascii'))

if __name__ == '__main__':
    nickname = input("Choose your nickname:")

    # Connect to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Start receive thread
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # Start writing thread
    write_thread = threading.Thread(target=write)
    write_thread.start()