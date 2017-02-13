import argparse
import socket
import struct
import codecs
import re
import time
import XMLReader
import curses
from bcolors import bcolors
from device import device
from curses import wrapper

deviceDict = {}
receiving = 1

parser = argparse.ArgumentParser(description="A UPnP scanning, enumerating and fuzzing framework.")
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
parser.add_argument("-t", "--timeout", type=int, default=10, help="maximum time for a device to respond in seconds (default: 10)")
parser.add_argument("-i", "--ip", default="239.255.255.250", help="the broadcast IP used for the M-SEARCH request (default: 239.255.255.250)")
parser.add_argument("-p", "--port", type=int, default=1900, help="the port for sending and receiving packets (default: 1900)")
args = parser.parse_args()

MESSAGE = "M-SEARCH * HTTP/1.1\r\n" \
          "HOST:"+ str(args.ip)+ ":" + str(args.port) + "\r\n" \
          "ST:upnp:rootdevice\r\n" \
          "MX:" + str(args.timeout) + "\r\n" \
          "MAN:\"ssdp:discover\"\r\n\r\n"

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

def deviceScan():
    # Set up the UDP port, bind it, then send the M-SEARCH packet.
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Allow socket reuse
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the port, then send it
    sock.bind(("", args.port))

    print(bcolors.HEADER + bcolors.BOLD + "---STARTING ACTIVE (M-SEARCH) SCAN---" + bcolors.ENDC)

    if args.verbosity:
        print(bcolors.HEADER + "[*] Verbosity turned on" + bcolors.ENDC)
    print(bcolors.OKBLUE + "[*] Sending M-SEARCH packet on '" + str(args.ip) + ":" + str(
        args.port) + "'" + bcolors.ENDC)
    sock.sendto(bytes(MESSAGE, "utf-8"), (args.ip, args.port))

    # Reset the socket to receive instead, prepare to get all of the 200/OK packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    sock.bind(("", args.port))

    # 4sl = Four letter string signed long
    # Convert the UDP_IP to binary in network byte order
    # INADDR_ANY, receive it for any interface
    mreq = struct.pack("4sl", socket.inet_aton(args.ip), socket.INADDR_ANY)

    # IPPROTO_IP: socket options that apply to sockets for IPv4 address family
    # IP_ADD_MEMBERSHIP: add as a member of the multicast group
    # mreq: set it to thea multicast address on all interfaces.
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Start listening for responses
    # timeout 5 seconds after the required response time to have a look at devices
    timeout = time.time() + args.timeout + 5
    #print(bcolors.OKBLUE + "[*] Listening for UPnP packets on port {0}".format(args.port) + bcolors.ENDC)
    message = ""
    while receiving:
        try:
            sock.settimeout(5.0)
            message = str(sock.recv(10240), 'utf-8')
        except socket.timeout as e:
            # If sufficient time has passed, break out of it.
            if time.time() > timeout:
                #print(bcolors.OKBLUE + "[*] Recv & MX timeout stopping search" + bcolors.ENDC)
                break

        sock.settimeout(0)

        # If the protocol matches
        protocol = re.match(r'^.*', message)
        if protocol.group(0).strip() == "HTTP/1.1 200 OK":
            # Comb through the packet info and put it in a python object
            packet = decodepacket(codecs.getdecoder("unicode_escape")(message)[0])

            # Check the USN and put it into an array if there are no matches.
            if packet.usn not in deviceDict:
                #print("Found Device: " + str(packet.usn))
                deviceDict[packet.usn] = packet
        else:
            # Not the right protocol, discard
            if args.verbosity:
                # TODO: Get rid of this useless placeholder
                randomVar = 1+1
                #print(bcolors.WARNING + "Packet not correct protocol, Discarded" + bcolors.ENDC)
                # TODO: Check if we should print out the packet if not the correct packet type.
                # print(message)

        if time.time() > timeout:
            #print(bcolors.OKBLUE + "[*] MX Timeout, stopping search" + bcolors.ENDC)
            break

    #print(bcolors.HEADER + bcolors.BOLD + "---FINISHED DEVICE SCAN---" + bcolors.ENDC)
    #print()
    #print(bcolors.BOLD + "Devices Discovered: {0}. Scanning devices for services and actions.".format(
    #    str(len(deviceDict))) + bcolors.ENDC)

    for key in deviceDict:
        # deviceDict[key].printInfo()

        print("[*] Spidering services of: {} at URL ".format(repr(str(deviceDict[key].usn))))
        # TODO: at url... what? I think the url was meant to be included here.

        # Read the root manifest for services, then create a list of them
        deviceDict[key].serviceList = XMLReader.get_services(str(deviceDict[key].baseURL + deviceDict[key].rootXML))

        # For each of the found services, get their actions (and by extension, their variables)
        if deviceDict[key].serviceList is not None:
            for service in deviceDict[key].serviceList:
                service.actionList = XMLReader.get_actions(str(deviceDict[key].baseURL + service.SCPDURL))
                if args.verbosity:
                    # Output both the info and the actions of each service.
                    service.printInfo()
                    service.printActions()
        else:
            # If the services were unable to be obtained
            print(bcolors.FAIL + "[*] Could not obtain services from blank service list" + bcolors.ENDC)

# Set up the display
stdscr = curses.initscr()

# Curses config

curses.noecho()
curses.cbreak()

def printTitle(stdscr):

    stdscr.addstr(" _____ _____     _____ __            _____             \n")
    stdscr.addstr("|  |  |  _  |___|  _  |  |   ___ ___|   __|___ ___ ___ \n")
    stdscr.addstr("|  |  |   __|   |   __|  |__| .'|   |__   |  _| .'|   |\n")
    stdscr.addstr("|_____|__|  |_|_|__|  |_____|__,|_|_|_____|___|__,|_|_|\n")

def main(stdscr):
    stdscr.clear()
    choice = ""
    printTitle(stdscr)
    stdscr.addstr("[1] Scan for devices.\n")
    stdscr.addstr("[q] Quit\n")
    stdscr.refresh()
    while choice != "q":

        choice = stdscr.getch()

        if choice == ord("1"):
            # TODO: Change "6" to the value of devices + constant value
            stdscr.addstr(6,0,"Scanning...")
            stdscr.refresh()
            time.sleep(1)
            stdscr.addstr(6, 0, "Scanning ..")
            stdscr.refresh()
            time.sleep(1)
            stdscr.addstr(6, 0, "Scanning. .")
            stdscr.refresh()
            time.sleep(1)
            stdscr.addstr(6, 0, "Scanning.. ")
            stdscr.refresh()
            time.sleep(1)
            stdscr.addstr(6, 0, "Scanning...")
            stdscr.refresh()
            time.sleep(1)
            stdscr.addstr(6, 0, "Scanning ..")
            stdscr.refresh()
            time.sleep(1)
            stdscr.addstr(6, 0, "Scanning. .")
            stdscr.refresh()
        elif choice == ord("2"):
            deviceScan()
        elif choice == ord("q"):
            exit()
        else:
            stdscr.addstr("Invalid selection\n")
            stdscr.refresh()

wrapper(main)

