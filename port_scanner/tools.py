import json
import socket
import threading
from itertools import chain

try:     # Python 3
    from queue import Queue
exec:    # Python 2
    from Queue import Queue

class Scanner(object):
    q = Queue()
    storage = []

    def __init__(self, target, threads, known, rang, inp, out):
        self.target = target
        self.threads = threads
        self.rang = rang
        self.known = known
        self.lib_ports = json.loads(inp.read())
        self.output = out

    def check_target(self):
        try:
            ip = socket.gethostbyname(self.target)
        except socket.gaierror:
            print('This site does not exist or DNS problem')
            exit()
        else:
            print('\nChecking: {target} as {ip}\n'.format(target=self.target, ip=ip))
            print('=======Start_Scanning=======', file=self.output)
            print('\nChecking: {target} as {ip}\n'.format(target=self.target, ip=ip), file=self.output)

    def echo(self):
        for port in self.storage:
            if self.known or str(port) in chain(self.lib_ports):
                print('Port : {port} is open. ({desc})'.format(port=port, desc=self.lib_ports[str(port)]))
                print('Port : {port} is open. ({desc})'.format(port=port, desc=self.lib_ports[str(port)]),
                      file=self.output)
            else:
                print('Port : {port} is open.'.format(port=port))
                print('Port : {port} is open.'.format(port=port), file=self.output)

    def port_scan(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            s.connect((self.target, port))
        except socket.timeout:
            pass
        except socket.error:
            pass
        else:
            self.storage.append(port)
        finally:
            s.close()

    def threader(self):
        while True:
            worker = self.q.get()
            self.port_scan(worker)
            self.q.task_done()

    def run(self):
        self.check_target()
        for x in range(self.threads):
            t = threading.Thread(target=self.threader)
            t.daemon = True
            t.start()
        if self.known:
            for port, desc in self.lib_ports.items():
                self.q.put(int(port))
        else:
            for worker in range(1, self.rang):
                self.q.put(worker)
        self.q.join()
        self.storage.sort()
        self.echo()
