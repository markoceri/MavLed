import Interfaces.interfaces
import threading
import RPi.GPIO as rpi

###############################################
#region class GPIOManager
class GPIOManager(Interfaces.interfaces.iService):
    #region __init__()
    def __init__(self):
        super().__init__()

        #region Fields
        self.__spinWait: threading.Event = None
        self.__red: int = None
        self.__blue: int = None
        self.__buzzer: int = None
        self.__redState: bool = None
        self.__blueState: bool = None
        self.__buzzerState: bool = None
        #endregion

        self.__red = 3
        self.__blue = 5
        self.__buzzer = 7
        self.__spinWait = threading.Event()

        self.__initializeGPIO()
        self.startService()
    #endregion

    #region __initializeGPIO()
    def __initializeGPIO(self) -> None:
        rpi.setwarnings(False)
        rpi.setmode(rpi.BOARD)

        rpi.setup(self.__red, rpi.OUT)
        rpi.setup(self.__blue, rpi.OUT)
        rpi.setup(self.__buzzer, rpi.OUT)

        self.enableRED()
        self.disableBLUE()
        self.disableBUZZER()
    #endregion

    #region enableRED()
    def enableRED(self) -> None:
        rpi.output(self.__red, 1)
        self.__redState = True
    #endregion

    #region enableBLUE()
    def enableBLUE(self) -> None:
        rpi.output(self.__blue, 1)
        self.__blueState = True
    #endregion

    #region enableBUZZER()
    def enableBUZZER(self) -> None:
        rpi.output(self.__buzzer, 1)
        self.__buzzerState = True
    #endregion

    #region disableRED()
    def disableRED(self) -> None:
        rpi.output(self.__red, 0)
        self.__redState = False
    #endregion

    #region disableBLUE()
    def disableBLUE(self) -> None:
        rpi.output(self.__blue, 0)
        self.__blueState = False
    #endregion

    #region disableBUZZER()
    def disableBUZZER(self) -> None:
        rpi.output(self.__buzzer, 0)
        self.__buzzerState = False
    #endregion

    #region toggleRED()
    def toggleRED(self) -> None:
        if self.__redState:
            self.disableRED()
        else:
            self.enableRED()
    #endregion

    #region toggleBLUE()
    def toggleBLUE(self) -> None:
        if self.__blueState:
            self.disableBLUE()
        else:
            self.enableBLUE()
    #endregion

    #region __manageGPIO()
    def __manageGPIO(self) -> None:
        return
    #endregion

    #region runThread() override
    def runThread(self) -> None:
        while not self.stopCycle():
            self.__manageGPIO()
    #endregion
#endregion