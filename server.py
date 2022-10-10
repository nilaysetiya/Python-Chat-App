import socket
import threading
import sys

host = '127.0.0.1'
port = 42000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

# Send message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle messages from clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Function to listen to requests
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname is {nickname}')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('Connected to server'.encode('ascii'))

        # Start new thread to handle client requests
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == '__main__':

    try:
        receive()
    except KeyboardInterrupt:
        server.close()
        sys.exit()


