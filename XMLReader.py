# TODO: try/catch for missing tags/files
import re
import urllib.request, urllib.error
import xml.etree.ElementTree as ET
from service import service


def getServices(XMLURL):
    XMLDocument = ""
    serviceArray = []
    attempts = 0

    print("--Attempting to open remote XML document---")
    # if the XML fails, it should immediately be saved in raw form for later use.
    # in terms of ps4 for example, it just returns "status=ok" which isn't exactly useful
    while attempts < 3:
        try:
            XMLDocument = urllib.request.urlopen(XMLURL).read()
            print("---Document received---")
            break
        except urllib.error.URLError as e:
            attempts += 1
            print("XML fetch error %d: %s" % (e.args[0], e.args[1]))

    # If the document could not be obtained
    if XMLDocument == "":
        print("Document at " + XMLURL +  " could not be obtained. Skipping.")
    else:
        root = ET.fromstring(XMLDocument)
        XMLNamespace = re.match('\{.*\}', root.tag).group(0)
        if XMLNamespace is None:
            print('XMLNamespace could not be found, defaulting to blank')
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


