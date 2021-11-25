"""
test data 008
"""
from pyutgenerator import const

from pyutgenerator.const import FUNC_OPEN

VALUE_01 = 'V1'


def aaaa(prm1):
    """
    const value.
    """
    VALUE_02 = "V2"
    if prm1 == VALUE_01:
        return False
    if prm1 == VALUE_02:
        return False
    if prm1 == const.FUNC_OPEN:
        return False
    if prm1 == FUNC_OPEN:
        return False

    return True
