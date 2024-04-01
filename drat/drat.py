# only use:
#   socket.socket
#   socket.bind
#   socket.listen
#   socket.accept
#   .recv
#   .send

# DO NOT USE:
#   socket.create_server

import click
import click_params
import ipaddress
import socket

from cli import DratShell

@click.command()
@click.option('-p', '--port', 'port', default=31337, type=int,
    help='Target port of the server')
@click.option('-v', '--verbose', 'verbose', count=True,
    help='Verbose output while running')
@click.option('-q', '--quiet', 'quiet', default=False,
    help='Suppress all output')
@click.option('--timeout', 'timeout', default=6,
    help='How long (in seconds) host will wait for the connection')
@click.option('--keep-alive-interval', 'interval', default=3,
    help='Interval (in seconds) of pings to the host to keep session alive')
@click.argument('host', nargs=1, type=click_params.IP_ADDRESS)
def main(port, host, verbose, quiet, timeout, interval):
    print(f'Connecting to: {host}:{port}')
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((str(host), port))
            shell = DratShell(s, verbose, quiet, timeout, interval)
            shell.cmdloop()
        except Exception as e:
            print(f'Exception raised during execution:\n\n{e}')
        finally:
            print('Closing socket . . .')

    print('Getting a clean exit . . .')

if __name__ == '__main__':
    main()
