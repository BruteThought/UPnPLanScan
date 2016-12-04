import socket
import struct
import codecs
import re
import time
import XMLReader
from bcolors import bcolors
from device import device


UDP_IP = "239.255.255.250"
UDP_PORT = 1900
MX = 10
MESSAGE = "M-SEARCH * HTTP/1.1\r\n" \
          "HOST:239.255.255.250:1900\r\n" \
          "ST:upnp:rootdevice\r\n" \
          "MX:" + str(MX) + "\r\n" \
          "MAN:\"ssdp:discover\"\r\n\r\n"

deviceDict = {}
receiving = 1


def decodepacket(receivedPacket):
        cache = cleanReg(re.search(r'(?:CACHE-CONTROL: ?)(.*)', receivedPacket))
        date = cleanReg(re.search(r'(?:DATE: ?)(.*)', receivedPacket))
        location = cleanReg(re.search(r'(?:LOCATION: ?)(.*)', receivedPacket))
        opt = cleanReg(re.search(r'(?:OPT: ?)(.*)', receivedPacket))
        nls = cleanReg(re.search(r'(?:NLS: ?)(.*)', receivedPacket))
        server = cleanReg(re.search(r'(?:SERVER: ?)(.*)', receivedPacket))
        userAgent = cleanReg(re.search(r'(?:X-User-Agent: ?)(.*)', receivedPacket))
        st = cleanReg(re.search(r'(?:ST: ?)(.*)', receivedPacket))
        usn = cleanReg(re.search(r'(?:USN: ?)(.*)', receivedPacket))

        currentDevice = device(cache, date, location, opt, nls, server, userAgent, st, usn)
        return currentDevice


def cleanReg(result):
    if result:
        return result.group(1)
    else:
        return ""

# Set up the UDP port, bind it, then send the M-SEARCH packet.
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Allow socket reuse
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the port, then send it
sock.bind(("", UDP_PORT))
print(bcolors.HEADER + "---STARTING ACTIVE (M-SEARCH) SCAN---" + bcolors.ENDC)
print(bcolors.OKBLUE + "Sending M-SEARCH packet." + bcolors.ENDC)
sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))

# Reset the socket to receive instead, prepare to get all of the 200/OK packets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

sock.bind(("", UDP_PORT))

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
timeout = time.time() + MX+5
print(bcolors.OKBLUE + "Listening for UPnP packets on port {0}".format(UDP_PORT) + bcolors.ENDC)
while receiving:
    try:
        sock.settimeout(5.0)
        message = str(sock.recv(10240), 'utf-8')
    except socket.timeout as e:
        # If sufficient time has passed, break out of it.
        if time.time() > timeout:
            print("Recv & MX timeout stopping search")
            break

    sock.settimeout(0)

    # If the protocol matches
    protocol = re.match(r'^.*', message)
    if protocol.group(0).strip() == "HTTP/1.1 200 OK":
        # Comb through the packet info and put it in a python object
        packet = decodepacket(codecs.getdecoder("unicode_escape")(message)[0])

        # Check the USN and put it into an array if there are no matches.
        if packet.usn not in deviceDict:
            print("Found Device")
            deviceDict[packet.usn] = packet
    else:
        # Not the right protocol, discard
        print(bcolors.WARNING + "Packet not correct protocol, Discarded" + bcolors.ENDC)

    if time.time() > timeout:
        print("MX Timeout, stopping search")
        break

print(bcolors.HEADER + "---FINISHED DEVICE SCAN---" + bcolors.ENDC)
print(bcolors.HEADER + str(len(deviceDict)) + " devices found. Scanning for services and actions." + bcolors.ENDC + "\n")
for key in deviceDict:
    print(bcolors.OKGREEN + "----START DEVICE INFO----" + bcolors.ENDC)
    deviceDict[key].printinfo()
    print(bcolors.OKGREEN + "----END DEVICE INFO----" + bcolors.ENDC + "\n")

    print(bcolors.OKGREEN + "---Getting Device Services---" + bcolors.ENDC + "\n")
    print(bcolors.OKBLUE + bcolors.BOLD + "Spider services: " + deviceDict[key].usn + bcolors.ENDC)
    deviceDict[key].serviceList = XMLReader.getServices(str(deviceDict[key].baseURL + deviceDict[key].rootXML))

    for service in deviceDict[key].serviceList:
        service.actionList = XMLReader.getActions(str(deviceDict[key].baseURL + service.SCPDURL))
        service.printInfo()
    print(bcolors.OKGREEN + "---End Device Services---" + bcolors.ENDC + "\n")
