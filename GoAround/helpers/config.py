from enum import Enum


class Modes(Enum):
    bypass = 1
    obfuscate = 2


class BypassMethods(Enum):
    reflection = 1
    scan_buffer_laine = 2


class ObfuscationMethods(Enum):
    mayus = 1
    concatenation = 2
    insertion = 3
