import socket
import struct
import codecs

UDP_IP = "239.255.255.250"
UDP_PORT = 1900

MESSAGE = "M-SEARCH * HTTP/1.1\r\n" \
          "HOST:239.255.255.250:1900\r\n" \
          "ST:upnp:rootdevice\r\n" \
          "MX:10\r\n" \
          "MAN:\"ssdp:discover\"\r\n\r\n"

# Set up the UDP port, bind it, then send the M-SEARCH packet.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Allow socket reuse
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Bind the socket to the port, then send it
sock.bind(("", UDP_PORT))
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

# Reset the socket to receive instead, prepare to get all of the 200/OK packets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

sock.bind(("", UDP_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT

# 4sl = Four letter string signed long
# Convert the UDP_IP to binary in network byte order
# INADDR_ANY, receive it for any interface
mreq = struct.pack("4sl", socket.inet_aton(UDP_IP), socket.INADDR_ANY)

# IPPROTO_IP: socket options that apply to sockets for IPv4 address family
# IP_ADD_MEMBERSHIP: add as a member of the multicast group
# mreq: set it to thea multicast address on all interfaces.
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    test = str(sock.recv(10240),'utf-8')
    print(codecs.getdecoder("unicode_escape")(test)[0])
