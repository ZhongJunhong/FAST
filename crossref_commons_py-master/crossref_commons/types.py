from enum import Enum, auto


class OutputType(Enum):

    JSON = auto()
    XML = auto()
    REFSTRING = auto()


class EntityType(Enum):

    PUBLICATION = auto()
    MEMBER = auto()
