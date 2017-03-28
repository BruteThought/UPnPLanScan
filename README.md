# UPnPLanScan
UPnPLanScan is a Python 3 program for scanning UPnP compliant devices on your local network for the purpose
of security research.

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

However, it does require to be **RUN AS ROOT** as otherwise sending/receiving packets will not work correctly.
Simply run "main.py" as root to start.

## Usage
UPnPLanScan does most of it's operations through the use of numbered menus, select options using the numpad or number row.
When in "view" mode, use j/k to scroll up or down and 'q' to go back.

An example of usage is to first scan for devices on your network using [1], any devices that are found will be automatically
listed with a numeric id in the menu. Press it's number to perform additional actions like viewing general device information [2]
or scan for further services and actions [3].

## Demo
[![UPnPLanScan Demo](http://i.imgur.com/cjSqaK1.png)](https://www.youtube.com/watch?v=NjcHfEYuTA8)

## Contributing
Feel free to contribute! This tool is still in development, so look for #TODO tags if you would like to improve the stability of the overall application.

We would also like to expand/include some new features, some examples being:
- fuzzing
- run actions with custom parameters
- automatically pick out developer comments from the service manifests for information leakage

If you want to develop one of these features, make sure to check there isn't a branch already in development!
