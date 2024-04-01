# only use:
#   socket.socket
#   socket.bind
#   socket.listen
#   socket.accept
#   .recv
#   .send

# DO NOT USE:
#   socket.create_server

import socket
import click
import click_params
import ipaddress
import time
import subprocess

import requests

@click.command()
@click.option('-p', '--port', 'port', default=31337, type=int,
    help='Port this server will listen on')
@click.option('-v', '--verbose', 'verbose', count=True,
    help='Verbose output while running')
@click.option('-q', '--quiet', 'quiet', count=True,
    help='Suppress all output')
@click.option('-h', '--host', 'host', default=ipaddress.IPv4Address('127.0.0.1'),
    type=click_params.IP_ADDRESS, help='Host address')
def main(host, port, verbose, quiet):
    h = PrintHandler(verbose, quiet)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(6)
        s.bind((str(host), port))
        try:
            s.listen()
            conn, addr = s.accept()
            with conn:
                h.vprint(f'connected to {addr}')
                try:
                    daemon = DratDaemon(conn, h)
                    daemon.mainloop()
                except Exception as e:
                    h.vvprint(f'Exception occured during main loop:\n\n{e}')
                h.vvprint('Closing connection . . .')
        except Exception as e:
            h.vvprint('Exception occured before main loop:\n\n{e}')
        h.vvprint('Closing socket . . .')
    h.vprint('Exiting . . .')

# Alright alright alright, you got me. It's NOT a daemon.
# But it's a cool project to work on, so it will be in the future.
# And the word is cool. Fite me.
class DratDaemon:

    def __init__(self, conn, h):
        self.conn = conn
        self.h = h

        self.buffer = None
        self.request = None
        self.body = None
        self.exiting = False
        self.timeout = 6
    
    def mainloop(self):
        self.gather_request()

        if self.request != requests.STRT:
            self.h.vvprint('Improper connection information. Terminating.')
            return

        self.timeout = int(self.body)
        self.h.vvprint(f'timeout: {self.timeout}')

        self.body = None
        self.request = None
        while not self.exiting:
            self.gather_request()
            self.h.vprint(f'request: {self.request}')
            self.h.vvprint(f'body: {self.body}')
            self.handle_request()

    def gather_request(self):
        while not self.buffer:
            self.buffer = self.conn.recv(1024)
        bufsize = int.from_bytes(self.buffer[:4], 'little')
        self.request = self.buffer[4:8]
        if bufsize == 8:
            if len(self.buffer) > 8:
                self.buffer = self.buffer[8:]
            else:
                self.buffer = None
        else:
            acc = self.buffer[8:]
            while len(acc) < bufsize - 8:
                acc += self.conn.recv(1024)
            if len(acc) > bufsize - 8:
                self.buffer = acc[bufsize - 8:]
            else:
                self.buffer = None
            self.body = acc.decode('utf-8')

    def handle_request(self):
        if self.request == requests.PRNT:
            self.h.vvprint('Print request received . . .')
            self.h.print(self.body)
        elif self.request == requests.EXIT:
            self.exiting = True
            self.h.vvprint('Exit request received . . .')
        elif self.request == requests.EXEC:
            self.h.vvprint('Execute request received . . .')
            self.h.vprint(self.body)
            ret = subprocess.run(self.body, capture_output=True, shell=True)
            self.h.print(ret.stdout.decode())
        self.request = None
        self.body = None

class PrintHandler:

    def __init__(self, verbose, quiet):
        self.verbose = verbose
        self.quiet = quiet

    def vvprint(self, s, end='\n'):
        if self.verbose > 1:
            print(s, end=end)

    def vprint(self, s, end='\n'):
        if self.verbose > 0:
            print(s, end=end)

    def print(self, s, end='\n'):
        if self.verbose > 0 or not self.quiet:
            print(s, end=end)

if __name__ == '__main__':
    main()
