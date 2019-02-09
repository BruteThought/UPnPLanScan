import argparse
import threading
#import scanner
deviceDict = {}
menuDevices = {}

# Set up parsing of commandline arguments.
parser = argparse.ArgumentParser(description="A UPnP scanning, enumerating and fuzzing framework.")
parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
parser.add_argument("-t", "--timeout", type=int, default=10, help="maximum time for a device to respond in seconds (default: 10)")
parser.add_argument("-i", "--ip", default="239.255.255.250", help="the broadcast IP used for the M-SEARCH request (default: 239.255.255.250)")
parser.add_argument("-p", "--port", type=int, default=1900, help="the port for sending and receiving packets (default: 1900)")
args = parser.parse_args()


# Set up the menu.
def main():
    # Print the startup
    print_title()
    print_context()

    # Application loop
    while True:
        get_command()


def print_context():
    # TODO: Print version here
    if args.verbosity:
        print("[*] Verbosity switch is on\n\n")


# Print the main menu
def get_command():
    # TODO: Current device context should be shown in the brackets
    command = input("\033[4m" + "ULS" + "\033[0m" + " device(None) >")
    if command == "a":
        pass
    elif not command:
        # Just loop back to accepting a command.
        pass
    else:
        # Print out an error
        print("[*] Unknown Command: {command}".format(command=command))


# Start the "..." loading loop for scanning until the scan ends
def loading_loop(thread):
    print("Starting scan through IP: " + str(args.ip) + ":" + str(args.port) + "\n")
    # While the scan is still happening
    # TODO: find that python library that was mentioned to me a while back... can probably use that to show the timeout
    print("Scanning...")
    while thread.is_alive():
        pass


# This "proxy" function allows the thread to return a value to the global deviceDict variable
def start_scan():
    global deviceDict
    #deviceDict = scanner.deviceScan(deviceDict, args)


main()
