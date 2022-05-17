import json
import time

configuration: dict = None

#region configLoader()
def configLoader() -> None:
    global configuration
    filename:str = "config.json"
    fp = open(filename, "r")
    configuration = json.load(fp)
    fp.close()
#endregion

#region getConfiguration()
def getConfiguration() -> dict:
    global configuration

    if (configuration == None):
        configLoader()
    return configuration
#endregion

#region getTMS()
def getTMS() -> int:
    return int(time.time())
#endregion