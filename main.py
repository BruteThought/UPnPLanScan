import argparser
from menu import print_title, print_context
import threading
#import scanner
device_dict = {}
menu_devices = {}


# Set up the menu.
def main():
    # Print the startup
    print_title()
    print_context(argparser.cmdargs)

    # Application loop
    while True:
        get_command()


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


# If we booted from console, get the arguments, if not, probably pytest
if __name__ == '__main__':
    print("lol")
    #argparser.get_cmd_args()

main()
