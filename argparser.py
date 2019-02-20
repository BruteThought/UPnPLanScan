import argparse


# Set some defaults, in case the way it was started was... weird.
class DefaultArgs(object):
    def __init__(self):
        self.verbosity = False
        self.timeout = 10
        self.ip = "239.255.255.250"
        self.port = 1900

# TODO: load the config here to overwrite any defaults. Order is 1) Builtin 2) config 3) flags


# Set cmdargs as default initially
cmdargs = DefaultArgs()


# If it runs correctly (from standard CMD), look for arguments from the command line instead.
def get_cmd_args():
    # Set up parsing of commandline arguments.
    parser = argparse.ArgumentParser(description="A UPnP scanning, enumerating and fuzzing framework.")
    parser.add_argument("-v", "--verbosity", help="increase output verbosity", action="store_true")
    parser.add_argument("-t", "--timeout", type=int, default=10, help="maximum time for a device to respond in seconds \
    (default: 10)")
    parser.add_argument("-i", "--ip", default="239.255.255.250", help="the broadcast IP used for the M-SEARCH request \
    (default: 239.255.255.250)")
    parser.add_argument("-p", "--port", type=int, default=1900, help="the port for sending and receiving packets \
    (default: 1900)")

    # Make it globally accessable
    global cmdargs
    cmdargs = parser.parse_args()
