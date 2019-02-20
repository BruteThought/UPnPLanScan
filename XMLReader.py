import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as elementTree
from service import Service
from action import Action
from argument import Argument
from variable import Variable
import curses

# TODO: Somehow pull all of the comments from the xml docs as well
# TODO: Strip all of the inputs for trailing/leading stuff as well as escape characters.


# Get the service information
def get_services(stdscr, device):
    serviceArray = []

    XMLURL = str(device.baseURL + device.rootXML)
    XMLDocument = get_xml_document(stdscr, XMLURL)

    # If the document URL is empty
    if XMLDocument is None:
        stdscr.add("[*] Document at {0} could not be obtained. Skipping.\n".format(repr(XMLURL)), curses.color_pair(2))
        stdscr.refresh()
    else:
        # TODO: need to have a try catch for corrupted/non XML files at the provided location.
        # TODO: narrow down this exception clause
        # try:
        # Get the root of the structure
        root = elementTree.fromstring(XMLDocument)

        # Get the namespace of the device, set to blank if none
        XMLNamespace = re.match('{.*}', root.tag).group(0)
        if XMLNamespace is None:
            stdscr.add('XMLNamespace could not be found, defaulting to blank\n', curses.color_pair(2))
            stdscr.refresh()
            XMLNamespace = ""

        # Get the device node to get the service info.
        device = root.find(XMLNamespace + 'device')
        servicelist = device.find(XMLNamespace + 'serviceList')

        # Find all of the services
        for serviceNode in servicelist.findall(XMLNamespace + 'service'):
            serviceType = serviceNode.find(XMLNamespace + 'serviceType').text
            serviceId = serviceNode.find(XMLNamespace + 'serviceId').text
            copntrolURL = serviceNode.find(XMLNamespace + 'controlURL').text
            eventsubURL = serviceNode.find(XMLNamespace + 'eventSubURL').text
            SCPDURL = serviceNode.find(XMLNamespace + 'SCPDURL').text

            serviceArray.append(Service(serviceType, serviceId, copntrolURL, eventsubURL, SCPDURL))
        # TODO : put this except back in when you figure out what errors you are getting to justify it!
        # except:
        #    stdscr.add("[*] Document at: '{0}' could not be obtained. Skipping.\n".format(repr(XMLURL)), curses.color_pair(2))
        return serviceArray


# Get the actions of the service.
def get_actions(stdscr, device, service):
    # Should change everything into objects, THEN pass them around, rather than passing around XML then selectively parsing.
    XMLURL = str(device.baseURL + service.SCPDURL)

    actionArray = []
    variableDict = {}
    # print(bcolors.OKBLUE + "Attempting to open remote Actions XML document" + bcolors.ENDC)
    XMLDocument = get_xml_document(stdscr, XMLURL)

    # If the document could not be obtained
    if XMLDocument is None:
        stdscr.addstr("[*] Document at {0} could not be obtained. Skipping.\n".format(repr(XMLURL)), curses.color_pair(2))
    else:
        # Get the root of the structure
        root = elementTree.fromstring(XMLDocument)

        # Get the namespace of the device, set to blank if none
        # TODO: Check if Namespace is required for actions
        XMLNamespace = re.match('{.*}', root.tag).group(0)
        if XMLNamespace is None:
            stdscr.addstr("XMLNamespace could not be found, defaulting to blank\n", curses.color_pair(2))
            stdscr.refresh()
            XMLNamespace = ""

        actionList = root.find(XMLNamespace + 'actionList')
        stateVariableList = root.find(XMLNamespace + 'serviceStateTable')

        # Loop through the variable state table in order to get info for later references.
        for variableNode in stateVariableList.findall(XMLNamespace + 'stateVariable'):
            name = variableNode.find(XMLNamespace + 'name')
            data_type = variableNode.find(XMLNamespace + 'dataType')
            default_value = variableNode.find(XMLNamespace + 'defaultValue')
            if name:
                name = name.text
            if data_type:
                data_type = data_type.text
            if default_value:
                default_value = default_value.text
            variableDict[name] = Variable(name, data_type, default_value)

        for actionNode in actionList.findall(XMLNamespace + 'action'):
            name = actionNode.find(XMLNamespace + 'name')
            if name is not None:
                name = name.text

            # Get the variableArray into a key/value structure, then pass it as an argument
            argumentList = get_arguments(actionNode.find(XMLNamespace + 'argumentList'), variableDict)
            actionArray.append(Action(name, argumentList))
        # TODO: need to have a try catch for corrupted/non XML files at the provided location.
        # TODO: narrow down this exception clause
        # stdscr.addstr("Actions XML Document at: '{0}' could not be parsed, skipping.\n".format(XMLURL), curses.color_pair(2))
        # stdscr.refresh()
        return actionArray


# Parse the arguments for an action,
def get_arguments(argumentList, variableDict):
    # TODO: Try/Catch for this section
    argumentArray = []
    XMLNamespace = re.match('{.*}', argumentList.tag).group(0)
    for argumentNode in argumentList.findall(XMLNamespace + 'argument'):
        name = argumentNode.find(XMLNamespace + 'name')
        if name is not None:
            name = name.text

        direction = argumentNode.find(XMLNamespace + 'direction')
        if direction is not None:
            direction = direction.text

        relatedStateVariable = argumentNode.find(XMLNamespace + 'relatedStateVariable')
        if relatedStateVariable is not None:
            relatedStateVariable = relatedStateVariable.text

        # If we already know what that variable is, we can grab the datatype and the default value!
        if relatedStateVariable in variableDict:
            relatedStateVariable = variableDict[relatedStateVariable]
        else:
            # Otherwise put them both down as unknown
            relatedStateVariable = Variable(relatedStateVariable, "?", "?")
        argumentArray.append(Argument(name, direction, relatedStateVariable))
    return argumentArray


# Download the xml document at the provided URL.
def get_xml_document(stdscr, XMLURL):
    # TODO: if the XML fails, it should immediately be saved in raw form for later use.
    # in terms of ps4 for example, it just returns "status=ok" which isn't exactly useful, but could be useful for the user.
    attempts = 0
    while attempts < 3:
        attempts += 1

        # TODO: have to properly validate whether or not it is a valid URL!
        if XMLURL == "":
            stdscr.add("No XML location given! Skipping.", curses.color_pair(2))
            break
        try:
            XMLDocument = urllib.request.urlopen(XMLURL).read()
            return XMLDocument
        except urllib.error.URLError as e:
            # If the document could not be obtained
            stdscr.add("XML fetch error {0}: {1}".format(e, XMLURL), curses.color_pair(2))
        except ValueError as e:
            stdscr.add("{0}".format(e), curses.color_pair(2))
    return None
