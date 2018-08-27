import argparse
import json
import socket
import threading
from queue import Queue

# Init parser
parser = argparse.ArgumentParser(usage='%(prog)s [options]', description='Basic port scanner with cmd line handler')

# Add arguments
parser.add_argument('-t', '--target', type=str, default='w3c.pl',
                    help='Set target. (default: w3c.pl)')
parser.add_argument('-w', '--workers', type=int, default=300,
                    help='How many theards to create? (default: 300)')
parser.add_argument('-r', '--range', type=int, default=1000,
                    help='How many ports to scan? (default: 1000)')
parser.add_argument('-i', '--intense', action='store_true',
                    help='Scan only known ports. (default: False)')

# Parse arguments to args
args = parser.parse_args()

threads = args.workers
intense = args.intense
rang = args.range
target = args.target

lib_ports = json.loads(open('ports.json').read())

try:
    ip = socket.gethostbyname(target)
    print('\nChecking: {target} as {ip}\n'.format(target=target, ip=ip))
except socket.gaierror:
    print('This site does not exist or DNS problem')


def port_scan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((target, port))
        try:
            print('Port : {port} is open. ({desc})'.format(port=port, desc=lib_ports[str(port)]))
        except KeyError:
            print('Port : {port} is open.'.format(port=port))
    except socket.timeout:
        pass
    except socket.error:
        pass
    finally:
        s.close()


def threader():
    while True:
        worker = q.get()
        port_scan(worker)
        q.task_done()


q = Queue()

for x in range(threads):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()
if intense:
    for port, desc in lib_ports.items():
        q.put(int(port))
else:
    for worker in range(1, rang):
        q.put(worker)

q.join()
