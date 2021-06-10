#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 20:11:04 2021

@author: basuki
"""
import socket
import select
import sys
from threading import Thread


#meminta masukan dari pengguna
ip_chat = '127.0.0.1'
port_chat = 8082
user_chat = input('username for chat: ')

#connect ke server dengan ip chat dan user chat
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip_chat, port_chat))

#connect ke ftp dengan username ftp dan password ftp


#kirim chat serta command
def send_msg(sock):
    while True:
        message = input()
        message = message + " " + user_chat
        sock.send(message.encode())
        sys.stdout.write('<You> ')
        message = ' '.join(message.split(' ')[:-1])
        sys.stdout.write(message + '\n')
        sys.stdout.flush()

# terima dari server
def recv_msg(sock):
    while True:
        data = sock.recv(2048)
        sys.stdout.write(data.decode() + '\n')

Thread(target=send_msg, args=(server,)).start()
Thread(target=recv_msg, args=(server,)).start()


while True:
    # antrian baru
    sockets_list = [server]
    
    # ambil dari antrian
    read_socket, write_socket, error_socket = select.select(sockets_list, [], [])
    
    # Looping untuk menerima dan mengirim pesan
    for socks in read_socket:
        if socks == server:
            recv_msg(socks)
        else:
            send_msg(socks)

server.close()
