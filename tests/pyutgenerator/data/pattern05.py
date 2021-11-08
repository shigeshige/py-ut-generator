"""
test
"""


def aaa():
    b = bbb()
    b.eee()

    bbb().ddd()
    c = b
    b.ddd()


def bbb():
    return C1()


def ccc():
    return C1()


class C1:

    def ddd(self):
        return 1

    def eee(self):
        return 1
