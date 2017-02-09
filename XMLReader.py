import re
import urllib.request
import urllib.error
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from service import service
from action import action
from argument import argument
from variable import variable
from bcolors import bcolors

# TODO: Somehow pull all of the comments from the xml docs as well
# TODO: Strip all of the inputs for trailing/leading stuff as well as escape characters.

def get_arguments(argumentList, variableDict):
    # TODO: Try/Catch for this section
    argumentArray = []
    XMLNamespace = re.match('\{.*\}', argumentList.tag).group(0)
    for argumentNode in argumentList.findall(XMLNamespace + 'argument'):
        name = argumentNode.find(XMLNamespace + 'name').text
        direction = argumentNode.find(XMLNamespace + 'direction').text
        relatedStateVariable = argumentNode.find(XMLNamespace + 'relatedStateVariable').text
        if relatedStateVariable in variableDict:
            relatedStateVariable = variableDict[relatedStateVariable]
        else:
            relatedStateVariable = variable(relatedStateVariable, "?", "?")

        argumentArray.append(argument(name, direction, relatedStateVariable))
    return argumentArray

def get_actions(XMLURL):

    # Should change everything into objects, THEN pass them around, rather than passing around XML then selectively parsing.

    actionArray = []
    variableDict = {}
    # print(bcolors.OKBLUE + "Attempting to open remote Actions XML document" + bcolors.ENDC)
    XMLDocument = get_xml_document(XMLURL)

    # If the document could not be obtained
    if XMLDocument is None:
        print(bcolors.WARNING + "[*] Document at " + repr(XMLURL) + " could not be obtained. Skipping." + bcolors.ENDC)
    else:
        try:
            # Get the root of the structure
            root = ET.fromstring(XMLDocument)

            # Get the namespace of the device, set to blank if none
            # TODO: Check if Namespace is required for actions
            XMLNamespace = re.match('\{.*\}', root.tag).group(0)
            if XMLNamespace is None:
                print(bcolors.WARNING + 'XMLNamespace could not be found, defaulting to blank' + bcolors.ENDC)
                XMLNamespace = ""

            actionList = root.find(XMLNamespace + 'actionList')
            stateVariableList = root.find(XMLNamespace + 'serviceStateTable')

            # Loop through the variable state table in order to get info for later references.
            for variableNode in stateVariableList.findall(XMLNamespace + 'stateVariable'):
                name = variableNode.find(XMLNamespace + 'name').text
                dataType = variableNode.find(XMLNamespace + 'dataType').text
                defaultValue = variableNode.find(XMLNamespace + 'defaultValue').text
                variableDict[name] = variable(name, dataType, defaultValue)

            for actionNode in actionList.findall(XMLNamespace + 'action'):
                name = actionNode.find(XMLNamespace + 'name').text

                # Get the variableArray into a key/value structure, then pass it as an argument
                argumentList = get_arguments(actionNode.find(XMLNamespace + 'argumentList'), variableDict)
                actionArray.append(action(name, argumentList))


        except:
            # TODO: need to have a try catch for corrupted/non XML files at the provided location.
            # TODO: narrow down this exception clause
            print(bcolors.FAIL + "Actions XML Document at: '{0}' could not be parsed, skipping.".format(XMLURL) + bcolors.ENDC)
        return actionArray


def get_services(XMLURL):
    serviceArray = []

    #print(bcolors.OKBLUE + "Attempting to open remote manifest XML document" + bcolors.ENDC)
    XMLDocument = get_xml_document(XMLURL)

    # If the document could not be obtained
    if XMLDocument is None:
        print(bcolors.WARNING + "[*] Document at " + repr(XMLURL) + " could not be obtained. Skipping." + bcolors.ENDC)
    else:
        # TODO: need to have a try catch for corrupted/non XML files at the provided location.
        # TODO: narrow down this exception clause
        try:
            # Get the root of the structure
            root = ET.fromstring(XMLDocument)

            # Get the namespace of the device, set to blank if none
            XMLNamespace = re.match('\{.*\}', root.tag).group(0)
            if XMLNamespace is None:
                print(bcolors.WARNING + 'XMLNamespace could not be found, defaulting to blank' + bcolors.ENDC)
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
                # Service control Protocol Document URL
                SCPDURL = serviceNode.find(XMLNamespace + 'SCPDURL').text

                serviceArray.append(service(serviceType, serviceId, copntrolURL, eventsubURL, SCPDURL))
        except:
            # TODO: this is not printing correctly in some cases, e.g. http://192.168.1.191:40001/ will
            # fuck with the output, not sure why.
            # UPDATE: The repr() function may have fixed this, keep an eye on it and remove this to-do if it seems to be fixed.
            print(bcolors.FAIL + "Service XML Document at: '{0}' could not be parsed, skipping.".format(repr(XMLURL)) + bcolors.ENDC)
        return serviceArray


def get_xml_document(XMLURL):
    # TODO: if the XML fails, it should immediately be saved in raw form for later use.
    # in terms of ps4 for example, it just returns "status=ok" which isn't exactly useful, but could be useful for the user.
    attempts = 0
    while attempts < 3:
        attempts += 1

        # TODO: have to properly validate whether or not it is a valid URL!
        if XMLURL == "":
            print(bcolors.FAIL + "No XML location given! Skipping." + bcolors.ENDC)
            break
        try:
            XMLDocument = urllib.request.urlopen(XMLURL).read()
            return XMLDocument
        except urllib.error.URLError as e:
            # If the document could not be obtained
            print(bcolors.FAIL + "XML fetch error {0}: {1}".format(e, XMLURL) + bcolors.ENDC)
        except ValueError as e:
            print(bcolors.FAIL + "{0}".format(e) + bcolors.ENDC)
    return None