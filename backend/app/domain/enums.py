from enum import Enum


class DeviceStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"


class DeviceMode(str, Enum):
    NORMAL = "normal"
    MAINTENANCE = "maintenance"
    SAFE = "safe"


class DeviceError(str, Enum):
    SENSOR_FAILURE = "sensor_failure"
    OVERHEAT = "overheat"
    COMMUNICATION_TIMEOUT = "communication_timeout"
    VOLTAGE_DROP = "voltage_drop"


class CommandType(str, Enum):
    START = "start"
    STOP = "stop"
    RESET = "reset"
    SET_MODE = "set_mode"
    INJECT_ERROR = "inject_error"