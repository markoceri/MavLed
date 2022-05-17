#!/usr/bin/python3.8

import Utils.utils
import Utils.jsonConst
import HostService.HostInstance
import threading
import GPIOService.GPIOManager
import time

from pymavlink import mavutil


##############################################
#region class HostInstanceMavLed
class HostInstanceMavLed(HostService.HostInstance.HostInstance):
    #region __init__()
    def __init__(self):
        super().__init__()

        #region Fields
        self.__configuration: dict = None
        self.__mavlinkConnection: mavutil.mavfile = None
        self.__connectionStatus: bool = None
        self.__gpioManager: GPIOService.GPIOManager.GPIOManager = None
        self.__spinWait: threading.Event = None
        #endregion

        self.__configuration = Utils.utils.getConfiguration()[Utils.jsonConst.MavLink]
        self.__connectionStatus = False
        self.__gpioManager = GPIOService.GPIOManager.GPIOManager()
        self.__spinWait = threading.Event()

        self.__mavlinkConnect()
        self.startService()
    #endregion

    #region setConnectionStatus()
    def setConnectionStatus(self, status: bool) -> None:
        self._statusLock.acquire(blocking=True)
        self.__connectionStatus = status
        self._statusLock.release()
    #endregion

    #region __mavlinkConnect()
    def __mavlinkConnect(self) -> None:
        connectionType: str = None
        connectionString: str = None

        connectionType = self.__configuration[Utils.jsonConst.MavLink_ConnectionType]
        if (connectionType == Utils.jsonConst.MavLink_ConnectionType_TCP):
            connectionString = str.format(
                "{0}:{1}:{2}",
                self.__configuration[Utils.jsonConst.MavLink_ConnectionType],
                self.__configuration[Utils.jsonConst.MavLink_ConnectionHostOrSource],
                self.__configuration[Utils.jsonConst.MavLink_ConnectionPortOrBoundRate]
            )
        elif (connectionType == Utils.jsonConst.MavLink_ConnectionType_UDP):
            connectionString = str.format(
                "{0}:{1}:{2}",
                self.__configuration[Utils.jsonConst.MavLink_ConnectionType],
                self.__configuration[Utils.jsonConst.MavLink_ConnectionHostOrSource],
                self.__configuration[Utils.jsonConst.MavLink_ConnectionPortOrBoundRate]
            )
        elif (connectionType == Utils.jsonConst.MavLink_ConnectionType_SERIAL):
            connectionString = str.format(
                "{0},{1}",
                self.__configuration[Utils.jsonConst.MavLink_ConnectionHostOrSource],
                self.__configuration[Utils.jsonConst.MavLink_ConnectionPortOrBoundRate]
            )
        else:
            self.__mavlinkConnection = None
            self.setConnectionStatus(False)

        try:
            self.__mavlinkConnection = mavutil.mavlink_connection(connectionString)
        except Exception as ex:
            self.__mavlinkConnection = None
            self.setConnectionStatus(False)
    #endregion

    #region __mavlinkConnected()
    def __mavlinkConnected(self) -> bool:
        if self.__mavlinkConnection:
            self.setConnectionStatus(True)
        else:
            self.setConnectionStatus(False)

        return self.__connectionStatus
    #endregion

    #region __mavlinkPopMessage()
    def __mavlinkPopMessage(self):
        msg = None

        if not self.__mavlinkConnected():
            return None

        try:
            msg = self.__getMavLinkMessage()

            if (msg):
                self.setConnectionStatus(True)

                return msg
            else:
                self.setConnectionStatus(False)
                return None
        except Exception as ex:
            self.setConnectionStatus(False)
            return None
    #endregion

    #region __sendMavLinkPing()
    def __sendMavLinkPing(self) -> None:
        if self.__mavlinkConnected():
            self.__mavlinkConnection.mav.ping_send(
                    int(time.time() * 1e6), # Unix time in microseconds
                    0, # Ping number
                    0, # Request ping of all systems
                    0 # Request ping of all components
                )
    #endregion

    #region __getMavLinkMessage()
    def __getMavLinkMessage(self):
        if self.__mavlinkConnected():
            return self.__mavlinkConnection.recv_match()
        else:
            return None
    #endregion

    #region runThread() override
    def runThread(self) -> None:
        msg: dict = None
        msgType: str = None

        while not self.stopCycle():
            msg = self.__mavlinkPopMessage()

            if not msg:
                if not self.__mavlinkConnected():
                    self.__mavlinkConnect()
                #self0__spinWait.wait()
                continue

            #self.__mavlinkConnection.wait_heartbeat()

            self.__spinWait.clear()
            msgType = msg.get_type()

            if (msgType == Utils.jsonConst.MavLink_MessageType_HEARTBEAT):
                self.onMessageHeartbeat(msg)
                continue
    #endregion

    #region onMessageHeartbeat()
    def onMessageHeartbeat(self, msg) -> None:
        self.__gpioManager.toggleRED()
        self.__gpioManager.toggleBLUE()

        print("\n\n*****Got message: %s*****" % msg.get_type())
        print("Message: %s" % msg)
        print("\nAs dictionary: %s" % msg.to_dict())
        # Armed = MAV_STATE_STANDBY (4), Disarmed = MAV_STATE_ACTIVE (3)
        print("\nSystem status: %s" % msg.system_status)
    #endregion

    #region stopServiceWithoutJoin() override
    def stopServiceWithoutJoin(self) -> None:
        super.stopServiceWithoutJoin()
        self.__spinWait.set()
    #endregion

#endregion