import socket
from sys import stdin
import threading


PORT = 6998
# A global list of currently connected clients (e.g. subscribers)
clients = []


def listen(listen_socket):
    global clients
    while 1:
        client_connection, client_address = listen_socket.accept()
        print('New connection from {}'.format(client_address))
        # Clear the buffer, but we won't actually read the request... assume it's
        # for the HTTP stream.
        client_connection.recv(1024)
        # Send the HTTP response header
        client_connection.sendall('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
        clients.append( (client_connection, client_address) )


def sender():
    global clients
    while 1:
        # Read the new data from stdin
        line = stdin.readline()

        broken = []
        # Send the update to all the clients
        for client in clients:
            try:
                client[0].sendall(line)
            except socket.error:
                # If the connection is broken (e.g. someone has disconnected),
                # take note for later removal.
                broken.append(client)

        # Prune the closed connections
        for broke in broken:
            broke[0].close()
            print('{} has closed their connection'.format(broke[1]))
            clients.remove(broke)


def setup_socket():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(('', PORT))
    listen_socket.listen(10)
    print('Serving on {}'.format(PORT))
    return listen_socket


def main():
    listen_socket = setup_socket()

    # Set up the listening thread as a daemon to accept connections
    listener = threading.Thread(target=listen, args=(listen_socket,))
    listener.daemon = True
    listener.start()

    # Start sending updates
    sender()


if __name__ == '__main__':
    main()
