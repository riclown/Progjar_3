import socket
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
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients != connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()
                remove(clients)

def send_msg(client_socket, message):
    client_socket.send(bytes(message, "utf-8"))

# terima chat client dan kirim
def recv_msg(clients, conn, addr):
    while True:
        try:
            command = conn.recv(2048).decode()
            
            # ambil command client lalu kirim ke client lain
            if command:
                if command == "BROADCAST":
                    data = conn.recv(2048).decode()
                    username = data.split(" ")[-1].rstrip('\n')
                    print(list_of_user)
                    data = ' '.join(data.split(' ')[:-1])
                    print('<' + username + '> ' + data)
                    message_to_send = '<' + username + '> ' + data
                    #ketika kita mau kirim pesan ke client lainnya
                    broadcast(message_to_send, conn)
                if command == "PRIVATE":
                    targetuser = conn.recv(2048).decode()
                    data = conn.recv(2048).decode()
                    username = data.split(" ")[-1].rstrip('\n')
                    print(list_of_user)
                    data = ' '.join(data.split(' ')[:-1])
                    print('<' + username + '> ' + data)
                    message_to_send = '<' + username + '> ' + data
                    destination_socket = clients[targetuser][0]
                    send_msg(destination_socket, message_to_send)
            else:
                remove(conn)
        except:
            continue

#jika client sudah dikirim pesan, maka hapus client
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

clients = {}

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
    print('   '+ userchat +' connected\n')
    #karena multi client kita menggunakan fungsi thread
    server_thread = threading.Thread(target=recv_msg, args=(clients, conn, addr))
    server_thread.start()

    clients["{}".format(userchat)] = (conn, addr, server_thread)

conn.close()
