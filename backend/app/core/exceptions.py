class EmulatorException(Exception):
    pass


class InvalidCommandException(EmulatorException):
    pass


class DeviceOfflineException(EmulatorException):
    pass