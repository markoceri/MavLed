#!/usr/bin/python3

import Interfaces.interfaces
import threading

##############################################
#region class HostInstanceStatusConst
class HostInstanceStatusConst():
    status_OK: str = "Ok"
    status_WARNING: str = "Warning"
    status_FAULT: str = "Fault"
    status_UNKNOWN: str = "Unknown"
#endregion

##############################################
#region class HostInstance
class HostInstance(Interfaces.interfaces.iService):
    #region __init__()
    def __init__(self):
        super().__init__()

        #region Fields
        self.__status: str = None
        self._statusLock: threading.Lock = None
        #endregion

        self.__status = HostInstanceStatusConst.status_OK
        self._statusLock = threading.Lock()
    #endregion

    #region getStatus()
    def getStatus(self) -> str:
        ris: str = None
        self._statusLock.acquire(blocking=True)
        ris = self.__status
        self._statusLock.release()
        return ris
    #endregion
    
#endregion