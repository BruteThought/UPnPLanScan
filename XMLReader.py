# TODO: try/catch for missing tags/files
import re
import urllib.request
import xml.etree.ElementTree as ET
from service import service


def getServices(XMLURL):
    print("--Attemtping to open remote XML document---")
    XMLDocument = urllib.request.urlopen(XMLURL).read()
    print("---Document received---")
    root = ET.fromstring(XMLDocument)
    XMLNamespace = re.match('\{.*\}', root.tag).group(0)
    serviceArray = []


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