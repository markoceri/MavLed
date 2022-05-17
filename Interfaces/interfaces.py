import threading

###############################################
#region iService
class iService():
    #region __init__()
    def __init__(self):
        #region Fields
        self.__mtxService: threading.Lock = None
        self.__bServiceStop: bool = None
        self.__thdService: threading.Thread = None
        self.__isActive: bool = None
        #endregion

        self.__mtxService = threading.Lock()
        self.__bServiceStop = False
        self.__isActive = False
    #endregion

    #region abstract runThread()
    def runThread(self) -> None:
        pass
    #endregion

    #region startService()
    def startService(self) -> None:
        self.__mtxService.acquire(blocking=True, timeout=60)
        self.__bServiceStop = False
        self.__isActive = True
        self.__mtxService.release()

        self.__thdService = threading.Thread(target=self.runThread)
        self.__thdService.start()
    #endregion

    #region stopService()
    def stopService(self) -> None:
        self.__mtxService.acquire(blocking=True, timeout=60)
        self.__bServiceStop = True
        self.__mtxService.release()

        self.__thdService.join()

        self.__mtxService.acquire(blocking=True, timeout=60)
        self.__isActive = False
        self.__mtxService.release()    
    #endregion

    #region stopServiceWithoutJoin()
    def stopServiceWithoutJoin(self) -> None:
        self.__mtxService.acquire(blocking=True, timeout=60)
        self.__bServiceStop = True
        self.__mtxService.release()
    #endregion

    #region joinService()
    def joinService(self) -> None:
        status: bool = None

        self.__mtxService.acquire(blocking=True, timeout=60)
        status = self.__bServiceStop
        self.__mtxService.release()

        if not status:
            return
        self.__thdService.join()

        self.__mtxService.acquire(blocking=True, timeout=60)
        self.__isActive = False
        self.__mtxService.release()
    #endregion

    #region stopCycle()
    def stopCycle(self) -> bool:
        ris: bool = False

        self.__mtxService.acquire(blocking=True, timeout=60)
        ris = self.__bServiceStop
        self.__mtxService.release()

        return ris
    #endregion

    #region isActive()
    def isActive(self) -> bool:
        ris: bool = False

        self.__mtxService.acquire(blocking=True, timeout=60)
        ris = self.__isActive
        self.__mtxService.release()

        return ris
    #endregion

#endregion