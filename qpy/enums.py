from enum import Enum


class DistributionType(str, Enum):
    EXPONENTIAL = "exponential"
    CONSTANT = "constant";
    NORMAL = "normal"
    UNIFORM = "uniform"

    @staticmethod
    def is_valid(value):
        return value in DistributionType._value2member_map_