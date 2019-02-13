from device import Device, devices
import re
import time
import socket
import codecs
import struct
import XMLReader
import config

receiving = 1


# Send out the scan packet, get the result, and put it into objects.
# TODO: Add the devices you find to the global devices instead of simply returning
def scan_for_devices(deviceDict):
    # Set up the scanning message
    MESSAGE = "M-SEARCH * HTTP/1.1\r\n" \
              "HOST:" + str(config.getConfig('ip')) + ":" + str(config.getConfig('port')) + "\r\n" \
              "ST:upnp:rootdevice\r\n" \
              "MX:" + str(config.getConfig('timeout')) + "\r\n" \
              "MAN:\"ssdp:discover\"\r\n\r\n"
    # Set up the UDP port, bind it, then send the M-SEARCH packet.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Allow socket reuse
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port, then send it
    sock.bind(("", int(config.getConfig('port'))))
    sock.sendto(bytes(MESSAGE, "utf-8"), (config.getConfig('ip'), int(config.getConfig('port'))))

    # Reset the socket to receive instead, prepare to get all of the 200/OK packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(("", int(config.getConfig('port'))))

    # 4sl = Four letter string signed long
    # Convert the UDP_IP to binary in network byte order
    # INADDR_ANY, receive it for any interface
    mreq = struct.pack("4sl", socket.inet_aton(config.getConfig('ip')), socket.INADDR_ANY)

    # IPPROTO_IP: socket options that apply to sockets for IPv4 address family
    # IP_ADD_MEMBERSHIP: add as a member of the multicast group
    # mreq: set it to thea multicast address on all interfaces.
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Start listening for responses
    # timeout 5 seconds after the required response time to have a look at devices
    timeout = time.time() + int(config.getConfig('timeout')) + 5
    message = ""
    while receiving:
        try:
            sock.settimeout(5.0)
            message = str(sock.recv(10240), 'utf-8')
            text_file = open("output.txt", "a")
            text_file.write(message)
            text_file.close()
        except socket.timeout:
            # If sufficient time has passed, break out of it.
            if time.time() > timeout:
                return deviceDict

        sock.settimeout(0)

        # If the protocol matches
        protocol = re.match(r'^.*', message)
        if protocol.group(0).strip() == "HTTP/1.1 200 OK":
            # Comb through the packet info and put it in a python object
            packet = decode_packet(codecs.getdecoder("unicode_escape")(message)[0])

            # Check the USN and put it into an array if there are no matches.
            if packet.usn not in deviceDict:
                deviceDict[packet.usn] = packet
            # TODO: Should probably do something if I don't get the right package

        if time.time() > timeout:
            return deviceDict


# Decode the response to the M-SEARCH
def decode_packet(receivedPacket):
        cache = cleanReg(re.search(r'(?:CACHE-CONTROL: ?)(.*)', receivedPacket))
        date = cleanReg(re.search(r'(?:DATE: ?)(.*)', receivedPacket))
        location = cleanReg(re.search(r'(?:LOCATION: ?)(.*)', receivedPacket))
        opt = cleanReg(re.search(r'(?:OPT: ?)(.*)', receivedPacket))
        nls = cleanReg(re.search(r'(?:NLS: ?)(.*)', receivedPacket))
        server = cleanReg(re.search(r'(?:SERVER: ?)(.*)', receivedPacket))
        userAgent = cleanReg(re.search(r'(?:X-User-Agent: ?)(.*)', receivedPacket))
        st = cleanReg(re.search(r'(?:ST: ?)(.*)', receivedPacket))
        usn = cleanReg(re.search(r'(?:USN: ?)(.*)', receivedPacket))

        current_device = Device(cache, date, location, opt, nls, server, userAgent, st, usn)
        return current_device


# Clean up the results but return an empty string if there's nothing.
def cleanReg(result):
    if result:
        return result.group(1)
    else:
        return ""


# Scan through all of the services
def scan_device_services(stdscr, device):
    # Read the root manifest for services, then create a list of them
    device.serviceList = XMLReader.get_services(stdscr, device)

    # For each of the found services, get their actions (and by extension, their variables)
    if device.serviceList is not None:
        for service in device.serviceList:
            service.actionList = XMLReader.get_actions(stdscr, device, service)
    else:
        # If the services were unable to be obtained
        stdscr.addstr("[*] Could not obtain services from blank service list")
    return device