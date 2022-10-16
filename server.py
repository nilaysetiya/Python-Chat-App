import socket
import threading
import sys
import ssl

host = '127.0.0.1'
port = 42000

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(certfile='cert.pem', keyfile='cert.pem')
context.load_verify_locations('cert.pem')
context.set_ciphers('AES128-SHA')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()
server = context.wrap_socket(server, server_side=True)

clients = []
nicknames = []
rooms = []
room_names = []


class Room:
    id = 1

    def __init__(self, owner):
        self.owner = owner
        self.id = Room.id
        Room.id = Room.id + 1
        self.room_clients = []
        self.room_clients.append(owner)
        index = clients.index(owner)
        self.owner_name = nicknames[index]
        self.room_name = 'Room ' + str(self.id) + ' By ' + self.owner_name
        room_names.append(self.room_name)
        self.show_room_for_clients(self.owner, self.owner_name)

    def broadcast_message_to_everyone(self, msg):
        print('room length is: ' + str(len(self.room_clients)))
        for temp_client in self.room_clients:
            temp_client.send(msg.encode('ascii'))

    def show_room_for_clients(self, temp_client, client_name):
        temp_client.send(f'NEW_ROOM_CREATED:{self.room_name}:{client_name}'.encode('ascii'))

    def add_client(self, room_client, room_client_name):
        self.room_clients.append(room_client)
        self.show_room_for_clients(room_client, room_client_name)

    def update_client_lists(self):
        msg = f'UPDATE_ROOM_LIST:{self.room_name}:'
        for temp_client in self.room_clients:
            index = clients.index(temp_client)
            name = nicknames[index]
            msg = msg + name + ':'

        for temp_client in self.room_clients:
            temp_client.send(msg.encode('ascii'))

    def send_img_to_everyone(self, path):
        for temp_client in self.room_clients:
            temp_client.send(f'ROOM_IMG:{path}'.encode('ascii'))
            send_file = open(f'Server_Files/{path}', 'rb')
            data = send_file.read(1024)
            while data:
                temp_client.send(data)
                data = send_file.read(1024)
            send_file.close()
            temp_client.send('EOF'.encode('ascii'))


# Send message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)


def new_client_added(client_name):
    for client in clients:
        client.send(('NEW_CLIENT_ADDED:' + client_name).encode('ascii'))


def update_existing_client_list():
    joint_names = ''
    for name in nicknames:
        joint_names = joint_names + name + ':'
    return joint_names


# Handle messages from clients
def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            if 'ONE_ON_ONE' in message:
                arr = message.split(':')
                index = nicknames.index(arr[1])
                temp_client = clients[index]
                temp_client.send(message.encode('ascii'))
                temp_client = None
            elif 'CREATE_ROOM' in message:
                arr = message.split(':')
                index = nicknames.index(arr[1])
                rooms.append(Room(clients[index]))
            elif 'ADD_CLIENT_ROOM' in message:
                arr = message.split(':')
                print(arr)
                if arr[3] in arr[1]:
                    room_index = room_names.index(arr[1])
                    temp_room = rooms[room_index]
                    index = nicknames.index(arr[2])
                    temp_client = clients[index]
                    temp_room.add_client(temp_client, arr[2])
            elif 'ROOM_MSG' in message:
                arr = message.split(':')
                room_index = room_names.index(arr[1])
                temp_room = rooms[room_index]
                msg = f'ROOM_MSG:{arr[1]}:{arr[2]}:{arr[3]}'
                temp_room.broadcast_message_to_everyone(msg)
            elif 'UPDATE_ROOM_LIST' in message:
                arr = message.split(':')
                print(arr)
                room_index = room_names.index(arr[1])
                temp_room = rooms[room_index]
                temp_room.update_client_lists()
            elif 'IMAGE_FROM_CLIENT' in message:
                arr = message.split(':')
                print(arr)
                output_file = open(f'Server_Files/{arr[1]}', 'wb')
                data = client.recv(1024)
                while data:
                    if data.isascii():
                        break
                    output_file.write(data)
                    data = client.recv(1024)
                output_file.close()

                # send to both clients
                temp_index1 = nicknames.index(arr[2])
                temp_index2 = nicknames.index(arr[3])
                temp_client_1 = clients[temp_index1]
                temp_client_2 = clients[temp_index2]

                temp_client_1.send(f'IMAGE_FROM_SERVER:{arr[1]}'.encode('ascii'))
                output_file1 = open(f'Server_Files/{arr[1]}', 'rb')
                output_data = output_file1.read(1024)
                while output_data:
                    temp_client_1.send(output_data)
                    output_data = output_file1.read(1024)
                output_file1.close()
                temp_client_1.send('EOF'.encode('ascii'))

                temp_client_2.send(f'IMAGE_FROM_SERVER:{arr[1]}'.encode('ascii'))
                output_file2 = open(f'Server_Files/{arr[1]}', 'rb')
                output_data = output_file2.read(1024)
                while output_data:
                    temp_client_2.send(output_data)
                    output_data = output_file2.read(1024)
                output_file2.close()
                temp_client_2.send('EOF'.encode('ascii'))

            elif 'ROOM_IMG' in message:
                arr = message.split(':')
                print(arr)
                output_file = open(f'Server_Files/{arr[2]}', 'wb')
                data = client.recv(1024)
                while data:
                    if data.isascii():
                        break
                    output_file.write(data)
                    data = client.recv(1024)
                output_file.close()

                temp_room_index = room_names.index(arr[1])
                temp_room = rooms[temp_room_index]
                temp_room.send_img_to_everyone(arr[2])

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

        # Advertise new client to existing clients
        new_client_added(nickname)

        # Update new client's list with existing clients
        client.send(('ADD_EXISTING_CLIENTS:' + update_existing_client_list()).encode('ascii'))

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
