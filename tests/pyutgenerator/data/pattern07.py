"""
test data 001
"""


from typing import Dict


def aaaaa(dic: Dict):
    """
    call and return
    """
    if dic['K1'] == 'V1':
        return True
    if dic.get('K2') == 'V2':
        return True
    if dic.get('K3', '') == 'V3':
        return True
    dic['K4'] = 'V4'
    return False
