"""
test data 009
"""
import os.path


def aaaa(prm1):
    """
    import os.path
    """

    if os.path.exists('token.json'):
        return False

    return True
