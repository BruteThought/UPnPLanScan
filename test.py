import socket

UDP_IP = ""
UDP_PORT = 9001

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(102400) # buffer size is 1024 bytes
    print("received message:", data)