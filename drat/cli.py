import cmd
import sys
import time
import threading

import requests
from handler import SockHandler

lock = threading.Lock()
event = threading.Event()

class DratShell(cmd.Cmd):
    def __init__(self, s, verbose, quiet, timeout, interval):
        self.prompt = 'Drat > '
        self.s = SockHandler(s)
        self.verbose = verbose
        self.quiet = quiet
        super(DratShell, self).__init__(stdin=sys.stdin, stdout=sys.stdout)
        with lock:
            self.s.send(str(timeout), requests.STRT)
        self.living = threading.Thread(target=keep_alive, args=(self.s, interval))
        self.living.start()
    def do_send(self, arg):
        'sends raw text to host'
        self.vprint(f'sending: {arg}')
        with lock:
            self.s.send(arg, requests.PRNT)
    def do_upper(self, arg):
        'make string uppercase, then sends to host'
        self.vprint(f'making upper: {arg}')
        try:
            up = arg.upper()
            self.vprint(f'upper: {up}')
            with lock:
                self.s.send(up, requests.PRNT)
        except:
            self.vprint(f'failed to make upper: {arg}')
    def do_double(self, arg):
        'doubles a value then sends it to the host'
        self.vprint(f'doubling: {arg}')
        try:
            doublearg = int(arg) * int(arg)
            self.vprint(f'doubled: {doublearg}')
            with lock:
                self.s.send(str(doublearg), requests.PRNT)
        except:
            self.vprint(f'failed to double: {arg}')
    def do_exec(self, arg):
        'executing command on the host'
        self.vprint(f'executing: {arg}')
        with lock:
            self.s.send(arg, requests.EXEC)
    def do_exit(self, arg):
        'exits drat shell'
        event.set()
        with lock:
            self.s.send('', requests.EXIT)
        self.living.join()
        self.vprint('Closing Drat shell . . .')
        return True
    def vvprint(self, s, end='\n'):
        if self.verbose > 1:
            print(s, end=end)
    def vprint(self, s, end='\n'):
        if self.verbose > 0:
            print(s, end=end)
    def print(self, s, end='\n'):
        if self.verbose > 0 or self.quiet != True:
            print(s, end=end)

def keep_alive(s, interval):
    while True:
        if event.is_set():
            break
        with lock:
            s.send('', requests.PASS)
        time.sleep(interval)

if __name__ == '__main__':
    d = DratShell()
    d.cmdloop()
