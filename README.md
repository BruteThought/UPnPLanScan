# UPnPLanScan
A UPnP scanner is a Python 3 program for scanning UPnP compliant devices on your local network.

### Features
- Scan devices on your network using M-SEARCH
- Parse services
- View actions
- View expected variables
- View expected variable types
- View expected output
- View "priority" actions
- Recognise potentially exploitable actions

## Setup
UPnPLanScan is simple to set up and does not require any additional dependencies.
However, it does require to be RUN AS ROOT as otherwise sending/receiving packets will not work correctly.
Simply run "main.py" as root to start.

## Usage
UPnPLanScan does most of it's operations through the use of numbered menus, select options using the numpad or number row.
When in "view" mode, use j/k to scroll up or down and 'q' to go back.

An example of usage is to first scan for devices on your network using "1", any devices that are found will be automatically
listed with a numeric id in the menu. Press it's number to perform additional actions like viewing general device information
or scan for further services and actions.
