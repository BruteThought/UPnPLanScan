# TODO: try/catch for missing tags/files
import re
import urllib.request, urllib.error
import xml.etree.ElementTree as ET
from service import service
from bcolors import bcolors


def getServices(XMLURL):
    XMLDocument = ""
    serviceArray = []
    attempts = 0

    print(bcolors.OKBLUE + "Attempting to open remote XML document" + bcolors.ENDC)
    # if the XML fails, it should immediately be saved in raw form for later use.
    # in terms of ps4 for example, it just returns "status=ok" which isn't exactly useful
    while attempts < 3:
        try:
            XMLDocument = urllib.request.urlopen(XMLURL).read()
            print(bcolors.OKBLUE + "XML Document received" + bcolors.ENDC)
            break
        except urllib.error.URLError as e:
            attempts += 1
            print(bcolors.FAIL + "XML fetch error %d: %s" % (e.args[0], e.args[1]) + bcolors.ENDC)

    # If the document could not be obtained
    if XMLDocument == "":
        print(bcolors.WARNING + "Document at " + XMLURL +  " could not be obtained. Skipping." + bcolors.ENDC)
    else:
        root = ET.fromstring(XMLDocument)
        XMLNamespace = re.match('\{.*\}', root.tag).group(0)
        if XMLNamespace is None:
            print(bcolors.WARNING+ 'XMLNamespace could not be found, defaulting to blank' + bcolors.ENDC)
            XMLNamespace = ""
        device = root.find(XMLNamespace + 'device')
        servicelist = device.find(XMLNamespace + 'serviceList')
        for serviceNode in servicelist.findall(XMLNamespace + 'service'):
            serviceType = serviceNode.find(XMLNamespace + 'serviceType').text
            serviceId = serviceNode.find(XMLNamespace + 'serviceId').text
            copntrolURL = serviceNode.find(XMLNamespace + 'controlURL').text
            eventsubURL = serviceNode.find(XMLNamespace + 'eventSubURL').text
            SCPDURL = serviceNode.find(XMLNamespace + 'SCPDURL').text
            serviceArray.append(service(serviceType, serviceId, copntrolURL, eventsubURL, SCPDURL))
        return serviceArray


