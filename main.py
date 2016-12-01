import socket
import struct
import codecs
import re
import time
from mSearch import *


UDP_IP = "239.255.255.250"
UDP_PORT = 1900
MX = 10
MESSAGE = "M-SEARCH * HTTP/1.1\r\n" \
          "HOST:239.255.255.250:1900\r\n" \
          "ST:upnp:rootdevice\r\n" \
          "MX:" + str(MX) + "\r\n" \
          "MAN:\"ssdp:discover\"\r\n\r\n"

devicedict = {}
receiving = 1

def decodepacket(packet):
        cache = cleanReg(re.search(r'(?:CACHE-CONTROL: ?)(.*)', packet))
        date = cleanReg(re.search(r'(?:DATE: ?)(.*)', packet))
        location = cleanReg(re.search(r'(?:LOCATION: ?)(.*)', packet))
        opt = cleanReg(re.search(r'(?:OPT: ?)(.*)', packet))
        nls = cleanReg(re.search(r'(?:NLS: ?)(.*)', packet))
        server = cleanReg(re.search(r'(?:SERVER: ?)(.*)', packet))
        userAgent = cleanReg(re.search(r'(?:X-User-Agent: ?)(.*)', packet))
        st = cleanReg(re.search(r'(?:ST: ?)(.*)', packet))
        usn = cleanReg(re.search(r'(?:USN: ?)(.*)', packet))

        device = mSearch(cache, date, location, opt, nls, server, userAgent, st, usn)
        return device

def cleanReg(result):
    if result:
        return result.group(1)
    else:
        return ""





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


# Start listening for responses
# timeout 5 seconds after the required response time to have a look at devices
timeout = time.time()+ MX+5
while receiving:
    message = str(sock.recv(10240),'utf-8')
    # If the protocol matches
    protocol = re.match(r'^.*', message)
    if protocol.group(0).strip() == "HTTP/1.1 200 OK":

        # Comb through the packet info and put it in a python object

        packet = decodepacket(codecs.getdecoder("unicode_escape")(message)[0])

        # Check the USN and put it into an array if there are no matches.
        if not packet.usn in devicedict:
            print("found device")
            devicedict[packet.usn] = packet

    else:
        # Not the right protocol, discard
        print("not correct protocol")

    # If sufficient time has passed, break out of it.
    if time.time() > timeout:
        break
print("---FINISHED SCANNING---")
for key in devicedict:
    print("----START DEVICE INFO----")
    devicedict[key].printinfo()
    print("----END DEVICE INFO----")
