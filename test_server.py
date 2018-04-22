

import socket
import pickle

TCP_IP = '0.0.0.0'
TCP_PORT = 9999
BUFFER_SIZE = 1024
MESSAGE = {'red':50,'blue':75,'green':0}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(pickle.dumps(MESSAGE))
data = s.recv(BUFFER_SIZE)
s.close()

