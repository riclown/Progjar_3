import socket
import select
import sys
import threading

# Membuat socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ip_address = '127.0.0.1'
port = 8082
server.bind((ip_address, port))
server.listen(100)
list_of_clients = []
list_of_user = []

# kirim pesan ke client yang lain
def kirimpesan(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

# terima chat client dan kirim
def clientthread(conn, addr):
    while True:
        try:
            data = conn.recv(2048).decode()
            
            # ambil data client lalu kirim ke lient lain
            if data:
                username = data.split(" ")[-1].rstrip('\n')
                print(list_of_user)
                data = ' '.join(data.split(' ')[:-1])
                print('<' + username + '> ' + data)
                message_to_send = '<' + username + '> ' + data
                #ketika kita mau kirim pesan ke client lainnya
                kirimpesan(message_to_send, conn)
            else:
                remove(conn)
        except:
            continue

#jika client sudah dikirim pesan, maka hapus client
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

while True:
    conn, addr = server.accept()
    list_of_clients.append(conn)
    userchat=conn.recv(2048).decode()
    #masukkan username ke list
    list_of_user.append(userchat)
    #for show last connection
    size = 0
    for x in list_of_clients:
        size+=1
    print(list_of_clients[size-1])
    print(' connected\n')
    #karena multi client kita menggunakan fungsi thread
    threading.Thread(target=clientthread, args=(conn, addr)).start()

conn.close()
