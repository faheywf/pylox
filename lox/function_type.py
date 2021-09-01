import enum

class FunctionType(enum.Enum):
    NONE, FUNCTION, INITIALIZER, METHOD = range(4)