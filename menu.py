import cmd
#import scanner

deviceDict = {}

def printTitle():
    print(" _____ _____     _____ __            _____             ")
    print("|  |  |  _  |___|  _  |  |   ___ ___|   __|___ ___ ___ ")
    print("|  |  |   __|   |   __|  |__| .'|   |__   |  _| .'|   |")
    print("|_____|__|  |_|_|__|  |_____|__,|_|_|_____|___|__,|_|_|")


def discover():
    print("Discover function ran")
    global deviceDict
    deviceDict = scanner.deviceScan(deviceDict)


def getInfo(deviceID):
    print("Want to get info for device {0}".format(str(deviceID)))


def scan(deviceId):
    print("Want to scan services of device {0}".format(str(deviceId)))



def listServices(deviceId):
    print("Want to list scanned services of device{0}".format(str(deviceId)))


def listActions(deviceId, serviceName):
    print("Want to list actions of device {0}'s service {1}".format(str(deviceId), str(serviceName)))


def alias(deviceID, aliasName):
    print("Want to rename {0} as {1}".format(str(deviceID), str(aliasName)))


def variableFunction(var, var2):
    print(var + var2)


def checkArgs(args, noOfArgs):
    if len(args) - 1 != noOfArgs:
        print("*** invalid number of arguments. Required {0}".format(noOfArgs))
        return False
    return True


class menu(cmd.Cmd):
    intro = "Welcome to UPnPLanScan.    Type help or ? to list commands.\n"
    prompt = "'ULS> "
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
            listActions(lastDevice, sargs[0])
        else:
            listActions(sargs[0], sargs[1])

    def do_alias(self, arg):
        'Give a device an alias to make it more easily recognisable (you can also use the alias in commands!)'
        sarg = arg.split()
        if checkArgs(arg, 2):
            alias(sarg[0], sarg[1])

    def do_quit(self, arg):
        'Exit ULS'
        print("Quitting")
        quit()
        return True


if __name__ == '__main__':
    printTitle()
    menu().cmdloop()
