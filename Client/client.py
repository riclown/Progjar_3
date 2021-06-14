import socket
import sys
import threading
import os

BUFF_SIZE = 65535
friends = []

## INSTRUCTION
print("Welcome to chat service. First, input your username!")

#  Meminta masukan dari pengguna
ip_chat = '127.0.0.1'
port_chat = 8082
user_chat = input('Username for chat: ')

## INSTRUCTION
print("Next is adding command. Here are list of our available command.")
print("-BROADCAST")
print("-PRIVATE")
print("-ADD")
print("-FRIENDLIST")

def FileExists(filename):
    return os.path.isfile(filename)

# terima dari server
def recv_msg(socket):
    while True:
        data = socket.recv(65535)
        sys.stdout.write(data.decode() + '\n')

def add_friend(client_username):
    friends.append(client_username)
    print("{} have been added as your friend.".format(client_username))

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
        client_socket.send(command.encode())
        ## MINTA MESSAGE
        print("Send Message :")
        message = input()
        message = message + " " + user_chat
        client_socket.send(message.encode())
        ## PRINT MESSAGE
        sys.stdout.write('<You> ')
        message = ' '.join(message.split(' ')[:-1])
        sys.stdout.write(message + '\n')
        continue

    elif command == "PRIVATE":
        ## MINTA TARGET USER
        print("Whom you want to send message to :")
        target = input()
        if target not in friends and target != "":
            print("{} is not recognized as your friend.".format(target))
            continue
        else :
            client_socket.send(command.encode())
            client_socket.send(target.encode())
            ## MINTA MESSAGE
            print("Send Message :")
            message = input()
            message = message + " " + user_chat
            client_socket.send(message.encode())
            ## PRINT MESSAGE
            sys.stdout.write('<You> ')
            message = ' '.join(message.split(' ')[:-1])
            sys.stdout.write(message + '\n')
            continue

    elif command == "ADD":
        print("What is your friend username :")
        friend_username = input()
        add_friend(friend_username)
        continue

    elif command == "FRIENDLIST":
        friend_list()    
        continue

    elif command == "UPLOAD":
        client_socket.send(command.encode("utf-8"))
        filename = input("Insert Filename: ")
        if FileExists(filename):
            print ("File Exist")
            print (filename) #ngetest
            client_socket.send(filename.encode("utf-8"))
            f = open(filename,"rb")
            temp = f.read(1024)
            while (temp):
                client_socket.send(temp)
                temp = f.read(1024)
            f.close()
        else :
            print ("File doesnt Exist")
        continue

    else :
        print ("Command doenst exist\n")
        continue

client_socket.close()
