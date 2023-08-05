"""Script to spawn server on current machine as a windows service.

To install, start, stop, debug, or perform other tasks with the service,
run this module from the command line. If you run it without any arguments,
a help message will be printed describing how to run it.

Generally, the things you want to do are

SpawnAsService.py --startup auto install
SpawnAsService.py start
SpawnAsService.py stop
SpawnAsService.py debug
"""

import os, sys, logging, logging.handlers
import win32serviceutil, win32service, win32event

from superpy.scripts import Spawn
from superpy.utils import WindowsUtils
from superpy.core import config

class SuperpyService(win32serviceutil.ServiceFramework):
    """Class to act as superpy service.
    """
    _svc_name_ = 'SuperpyService'
    _svc_display_name_ = 'Superpy parallel processing server'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" requrest will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        "Stop the service."
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        "Start the service."

        handler = self.SetupLogging()

        WindowsUtils.SetPriority('REALTIME_PRIORITY_CLASS')
        logging.info('Redirect stdout and stderr to handler.')
        sys.stdout = handler.stream
        sys.stderr = handler.stream
        _server = Spawn.SpawnServer(daemon=True)

        logging.info('Running until we see service stop event')
        # Now just wait for a stop request
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

        # Time to shutdown.
        # Since we started server as daemon, just exit program by returning.
        return None


    @staticmethod
    def SetupLogging():
        "Arrange output to go to log file."

        logging.getLogger('').setLevel(config.defaultLogLevel)
        logging.info('Set log level to %s from config.'%config.defaultLogLevel)

        logFile = config.serviceLogFile
        if (os.path.exists(logFile)):
            try:
                os.remove(logFile)
            except Exception, e:
                logging.error(
                    'Unable to remove log file due to error: %s' %str(e) )
        handler = logging.handlers.RotatingFileHandler(
            logFile, maxBytes=20000000, backupCount=2)
        logging.getLogger('').addHandler(handler)
        return handler

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(SuperpyService)
