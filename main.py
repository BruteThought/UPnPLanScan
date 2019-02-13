import argparser
from menu import print_title, print_context, get_command


# Set up the menu.
def main():
    # Print the startup
    print_title()
    print_context()

    # Command loop!
    while True:
        get_command()


# If we booted from console, get the arguments, if not, probably pytest
if __name__ == '__main__':
    argparser.get_cmd_args()
    main()
