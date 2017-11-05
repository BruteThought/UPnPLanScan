from configparser import ConfigParser

configParse = ConfigParser()


def createConfig():
    configParse.read('config.ini')
    if not configParse.has_section('main'):
        configParse.add_section('main')
        configParse.set('main', 'ip', '239.255.255.250')
        configParse.set('main', 'port', '1900')
        configParse.set('main', 'timeout', '10')
        configParse.set('main', 'verbosity', 'False')

        with open('config.ini', 'w') as f:
            configParse.write(f)


def getConfig(request):
    try:
        return configParse.get('main', str(request))
    except:
        print("Attempt to get {0} from config failed".format(str(request)))


def setConfig(request, value):
    try:
        configParse.set('main', str(request), str(value))
    except:
        print("Attempt to set {0} with value {1} failed".format(str(request), str(value)))
