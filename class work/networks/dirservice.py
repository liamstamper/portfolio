import sys
import socket
import threading
import json

class DirectoryService:
    def __init__(self, port):
        self.port = port
        self.directory = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', port))
        self.sock.listen(5)

    def handle_client(self, conn, addr):
        data = conn.recv(1024)
        message = json.loads(data.decode('utf-8'))
        if message['operation'] == 'register':
            self.directory[message['user']] = message['addr']
        elif message['operation'] == 'lookup':
            user = message['user']
            if user in self.directory:
                addr = self.directory[user]
                response = {'addr': addr}
            else:
                response = {'addr': 'UNKNOWN'}
            response = json.dumps(response).encode('utf-8')
            conn.sendall(response)
        conn.close()

    def start(self):
        while True:
            conn, addr = self.sock.accept()
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dirservice.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    directory_service = DirectoryService(port)
    directory_service.start()
