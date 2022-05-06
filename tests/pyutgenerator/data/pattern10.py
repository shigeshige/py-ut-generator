"""
test data 010
"""


def aaaa(prm1):
    """
    raise
    """
    if not bool(prm1):
        raise ValueError('test')

    return False


def bbbb(prm1):
    """
    raise
    """
    if not bool(prm1):
        eee = ValueError('test')
        raise eee

    return False
