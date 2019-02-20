import cmd
from scanner import scan_for_devices
from device import selected_device, devices
import argparser


# Print the title when the application starts
def print_title():
    print(" _____ _____     _____ __            _____             ")
    print("|  |  |  _  |___|  _  |  |   ___ ___|   __|___ ___ ___ ")
    print("|  |  |   __|   |   __|  |__| .'|   |__   |  _| .'|   |")
    print("|_____|__|  |_|_|__|  |_____|__,|_|_|_____|___|__,|_|_|")


# Print any extra information such as version/switches
def print_context():
    # TODO: Print version here
    if argparser.cmdargs.verbosity:
        print("[*] Verbosity switch is on\n\n")


# Print the main menu
def get_command():
    # TODO: add tab completion.
    command = input("\033[4m" + "ULS" + "\033[0m" + " device({0}) > ".format(get_selected_device_name())).split()
    if command[0] == "scan":
        # TODO: should probably make it so that scanning devices/services are parsed differently.\
        #  Could take a LONG time on busy networks, so maybe scan all/devices/services
        scan_for_devices()
        print(devices)
    elif command[0] == "help":
        # TODO: print out a list of the possible commands and how to use them
        print("Printing help")
    elif command[0] == "info":
        # TODO: should probably make it so that displaying device/service/function info are parsed differently.
        print("Display info on a topic")
    elif command[0] == "clear":
        # TODO: Clear the currently selected device
        print("Clearing device")
    elif command[0] == "alias":
        # TODO: Create an alias for a certain device (maybe the one currently selected? \
        #  Alternatively, could number in list and use that.)
        print("Creating alias")
    elif command[0] == "quit":
        quit()
        return True
    elif not command:
        # Just loop back to waiting for a command.
        pass
    else:
        # Print out an error
        print("[*] Unknown Command: {command}".format(command=command))


# Return the selected devices name (truncated to not take up the full menu)
def get_selected_device_name():
    if selected_device is not None:
        device_name = str(selected_device)

        # If device name is very long, shorten it to limit menu length
        if len(device_name) > 15:
            device_name = device_name[0:11] + "..."
        return device_name
    else:
        return "None"


def discover():
    print("Discover function ran")
    scan_for_devices()


def get_info(deviceID):
    print("Want to get info for device {0}".format(str(deviceID)))


def scan(deviceId):
    print("Want to scan services of device {0}".format(str(deviceId)))



def info_services(deviceId):
    print("Want to list scanned services of device{0}".format(str(deviceId)))


def info_actions(deviceId, serviceName):
    print("Want to list actions of device {0}'s service {1}".format(str(deviceId), str(serviceName)))


def alias(deviceID, aliasName):
    print("Want to rename {0} as {1}".format(str(deviceID), str(aliasName)))


def variable_function(var, var2):
    print(var + var2)


def check_args(args, noOfArgs):
    if len(args) - 1 != noOfArgs:
        print("*** invalid number of arguments. Required {0}".format(noOfArgs))
        return False
    return True


class menu(cmd.Cmd):
    file = None

    def do_discover(self, arg):
        'Discover UPnP Devices on the local network'
        discover()

    def do_info(self, arg):
        'Print the device information (such as IP address, userverversion, useragent etc)'
        sarg = arg.split()
        if checkArgs(arg, 1):
            getInfo(sarg[0])

    def do_scan(self, arg):
        'Scan the device for services and service information (such as function names, arguments etc)'
        sarg = arg.split()
        if checkArgs(arg, 1):
            scan(sarg[0])

    def do_list(self, arg):
        'List the devices services, if any have been found through scanning.'
        sarg = arg.split()
        if checkArgs(arg, 1):
            listServices(sarg[0])

    # TODO: Should probably be a cleaner way of doing this
    def do_actions(self, arg):
        'Get the function names and arguments of a service'
        sargs = arg.split()
        noOfArgs = len(sargs)
        print(str(noOfArgs))
        if noOfArgs != 1 and noOfArgs != 2:
            print("*** invalid number of arguments. Required 2/3")
            return

        # If no device is specified in the argument list
        if noOfArgs == 1:
            print("No device specified, using last previously referred device")
            # TODO: Setup last known used device
            lastDevice = "TODO"
            list_actions(lastDevice, sargs[0])
        else:
            list_actions(sargs[0], sargs[1])

    def do_alias(self, arg):
        'Give a device an alias to make it more easily recognisable (you can also use the alias in commands!)'
        sarg = arg.split()
        if check_args(arg, 2):
            alias(sarg[0], sarg[1])
