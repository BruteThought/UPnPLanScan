import curses


def scrollPad(stdscr, stringInput):
    # Get the current size of the window and save it
    height, width = stdscr.getmaxyx()

    # Get number of newlines in a string
    splitInput = stringInput.split("\n")
    inputHeight = len(splitInput)

    # If the line would wrap around, add 1 to the inputheight
    for line in splitInput:
        lineLength = len(line)

        # Tabs are equal to 1 in len, but 8 in spaces, so add 7 to get everything back in alignment.
        tabNo = len(line.split("\t"))
        lineLength += tabNo * 7

        if lineLength >= width:
            inputHeight += 1

    # Create a new pad with maximum width and however high the string is, including a line position
    mypad = curses.newpad(inputHeight, width)
    mypad_pos = 0
    mypad.addstr(stringInput)
    addStatus(stdscr)

    # For some reason the background is blank for "gapped" areas of input, this workaround resets the background
    # TODO: Find a cleaner way to do this so that output doesn't have to be dim.
    mypad.bkgd(0, curses.A_DIM)

    # Once all of the input is added to the pad, refresh the region (whole screen minus 2 for index and status bar.
    mypad.refresh(mypad_pos, 0, 0, 0, height - 2, width)

    # Wait for the input from the user to scroll up/down
    while True:
        cmd = mypad.getch()
        # Go down by one unless it's the end of the file.
        if cmd == ord("j") and mypad_pos < inputHeight - height + 1:

            mypad_pos += 1
            addStatus(stdscr)
            mypad.refresh(mypad_pos, 0, 0, 0, height - 2, width)

        # Go up by one, unless we go "over the top".
        elif cmd == ord("k") and mypad_pos > 0:
            mypad_pos -= 1
            addStatus(stdscr)
            mypad.refresh(mypad_pos, 0, 0, 0, height - 2, width)
        elif cmd == ord("q"):
            break


# The instruction bar at the bottom.
def addStatus(stdscr):
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height - 1, 0, "[j] Down [k] Up [q] Back")
    stdscr.refresh()
