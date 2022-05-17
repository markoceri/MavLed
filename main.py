#!/usr/bin/python
import Interfaces.interfaces
import HostService.HostInstanceMavLed
import threading

if __name__ == "__main__":
    foreverLoop: threading.Event = None
    service: Interfaces.interfaces.iService = None

    service = HostService.HostInstanceMavLed.HostInstanceMavLed()

    foreverLoop = threading.Event()
    foreverLoop.wait()