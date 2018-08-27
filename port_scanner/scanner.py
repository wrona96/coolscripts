import json
import socket
import threading
from queue import Queue

lib_ports = json.loads(open('ports.json').read())
target = 'w3c.pl'
threads = 300
rang = 1000

try:
    ip = socket.gethostbyname(target)
    print('\nChecking: {target} as {ip}\n'.format(target=target, ip=ip))
except IndentationError:
    print('This site does not exist!!!')


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
# for port, desc in lib_ports.items():
# q.put(int(port))
for worker in range(1, rang):
    q.put(worker)

q.join()
