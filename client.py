import socket
import sys
import threading

BUFF_SIZE = 65535
friends = []

#meminta masukan dari pengguna
ip_chat = '127.0.0.1'
port_chat = 8082
user_chat = input('Username for chat: ')

# terima dari server
def recv_msg(socket):
    while True:
        data = socket.recv(65535)
        sys.stdout.write(data.decode() + '\n')

def add_friend(client_username):
    friends.append(client_username)
    print("SUCCESS! {} have been added as your friend.".format(client_username))

def friend_list():
    print("Your FriendList:")
    for friend in friends:
        print(" - {}".format(friend))


#connect ke server dengan ip chat dan user chat
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip_chat, port_chat))
client_socket.send(user_chat.encode())

client_thread = threading.Thread(target=recv_msg, args=(client_socket,))
client_thread.start()

while True:
    print ("Input Command :")
    command = input()

    if command == "BROADCAST":
        print("Send Message :")
        message = input()
        message = message + " " + user_chat
        client_socket.send(message.encode())
        sys.stdout.write('<You> ')
        message = ' '.join(message.split(' ')[:-1])
        sys.stdout.write(message + '\n')
        continue

    elif command == "PRIVATE":
        print ("Masuk Private")
        continue

    elif command == "ADD":
        print("What is your friend username :")
        friend_username = input()
        add_friend(friend_username)
        continue

    elif command == "FRIENDLIST":
        friend_list()    
        continue

    else :
        print ("Command doenst exist\n")
        continue

client_socket.close()
