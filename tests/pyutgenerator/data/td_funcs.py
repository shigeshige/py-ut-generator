"""
test data
"""

import os

def func1():
    """
    func1
    """
    x = 1
    return x


def func2(prm1, prm2):
    """
    func2
    """
    xxx = func1()
    zzz =  prm1 + prm2 + xxx
    print(zzz)

    return func1()


def test_func1():
    """
    """
    i = 1
    return i


class T001:
    def tf01(self):
        aaaa = 1
        os.path('/')
        return aaaa

    @classmethod
    def tf02(c):
        aaaa = 1
        return aaaa
