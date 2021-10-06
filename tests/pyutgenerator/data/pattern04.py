"""
test
"""


def aaa():

    with bbb() as f:
        f.read(1)


def bbb():
    return open("aaaa.xxxx", "a")
