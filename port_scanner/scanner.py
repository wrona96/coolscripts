import threading
import socket
import json
from queue import Queue


lib_ports = json.loads(open('ports.json').read())
target = '192.168.0.1'
threads = 300
rang = 1000

try:
    ip = socket.gethostbyname(target)
    print('\nChecking: {target} as {ip}\n'.format(target=target, ip=ip))
except:
    print('This site does not exist!!!')

def portscan_custom(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        con = s.connect((target,port))
        try:
            print('Port : {port} is open. ({desc})'.format(port=port, desc=lib_ports[str(port)]))
        except:
            print('Port : {port} is open.'.format(port=port))
        con.close()
    except:
        pass

def threader():
    while True:
        worker = q.get()
        portscan_custom(worker)
        q.task_done()

q = Queue()

for x in range(threads):#Creating threads
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()
#for port, desc in lib_ports.items():#Znane Porty
    #q.put(int(port))
for worker in range(1,rang):#Wszystkie z zakresu
    q.put(worker)

q.join()
