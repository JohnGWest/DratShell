# only use:
#   socket.socket
#   socket.bind
#   socket.listen
#   socket.accept
#   .recv
#   .send

# DO NOT USE:
#   socket.create_server

class SockHandler:

    def __init__(self, sock):
        self.sock = sock

    def send(self, s, request):
        a = int(len(s) + 8).to_bytes(4, 'little')
        data = a + request + s.encode('utf-8')
        self.sock.send(data)
