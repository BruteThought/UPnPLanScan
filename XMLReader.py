import re
import urllib.request
import urllib.error
# noinspection PyPep8Naming
import xml.etree.ElementTree as ET
from service import service
from action import action
from argument import argument
from bcolors import bcolors


def getArguments(argumentList):
    # TODO: Try/Catch for this section
    argumentArray = []
    XMLNamespace = re.match('\{.*\}', argumentList.tag).group(0)
    for argumentNode in argumentList.findall(XMLNamespace + 'argument'):
        name = argumentNode.find(XMLNamespace + 'name').text
        direction = argumentNode.find(XMLNamespace + 'direction').text
        relatedStateVariable = argumentNode.find(XMLNamespace + 'relatedStateVariable').text
        argumentArray.append(argument(name, direction, relatedStateVariable))
    return argumentArray


def getActions(XMLURL):
    actionArray = []
    #print(bcolors.OKBLUE + "Attempting to open remote Actions XML document" + bcolors.ENDC)
    XMLDocument = getXMLDocument(XMLURL)

    # If the document could not be obtained
    if XMLDocument is None:
        print(bcolors.WARNING + "Document at " + XMLURL + " could not be obtained. Skipping." + bcolors.ENDC)
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
            actionList =  root.find(XMLNamespace + 'actionList')
            for actionNode in actionList.findall(XMLNamespace + 'action'):
                name = actionNode.find(XMLNamespace + 'name').text
                argumentList = actionNode.find(XMLNamespace + 'argumentList')
                actionArray.append(action(name, argumentList))
        except:
            # TODO: need to have a try catch for corrupted/non XML files at the provided location.
            # TODO: narrow down this exception clause
            print(bcolors.FAIL + "Actions XML Document at: '{0}' could not be parsed, skipping.".format(XMLURL) + bcolors.ENDC)
        return actionArray


def getServices(XMLURL):
    serviceArray = []

    #print(bcolors.OKBLUE + "Attempting to open remote manifest XML document" + bcolors.ENDC)
    XMLDocument = getXMLDocument(XMLURL)

    # If the document could not be obtained
    if XMLDocument is None:
        print(bcolors.WARNING + "Document at " + XMLURL + " could not be obtained. Skipping." + bcolors.ENDC)
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
            print(bcolors.FAIL + "Service XML Document at: '{0}' could not be parsed, skipping.".format(XMLURL) + bcolors.ENDC)
        return serviceArray


def getXMLDocument(XMLURL):
    # if the XML fails, it should immediately be saved in raw form for later use.
    # in terms of ps4 for example, it just returns "status=ok" which isn't exactly useful
    attempts = 0
    while attempts < 3:
        try:
            # TODO: have to properly validate whether or not it is a valid URL!
            if XMLURL == "":
                print(bcolors.FAIL + "No XML location given! Skipping." + bcolors.ENDC)
                break
            XMLDocument = urllib.request.urlopen(XMLURL).read()
            #print(bcolors.OKBLUE + "XML Document received" + bcolors.ENDC)
            return XMLDocument
        except urllib.error.URLError as e:
            attempts += 1
            print(bcolors.FAIL + "XML fetch error {0}: {1}".format(e, XMLURL) + bcolors.ENDC)
    # If the document could not be obtained
    return None

