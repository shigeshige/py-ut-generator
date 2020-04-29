"""
copyrigth https://github.com/shigeshige/py-ut-generator
"""

TEMP_IMPORT = """
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

{}
"""

TEMP_FUNC = """
def {}():
    # init
{}
    # run
{}
{}
    # check
{}
"""

STR_PRE_FUNC = 'test_'

STR_FROM_IMPORT = 'form {} import {}'

STR_VARIS = '    {} = {}'

STR_RUNS = '    {}.{}({})'
STR_RUNS_RETURN = '    ret = {}.{}({})'

STR_WITH = '    with\\'
STR_MOCK = '            patch({}) as {}'

STR_RC = '\n'


def parse_import(imps):
    """
    """
    return TEMP_IMPORT.format(imps)


def parse_func(name, pkg, mdn, inits, has_return, args, mocks):
    """
    """
    runs = ''
    if has_return:
        runs = STR_RUNS_RETURN.format(mdn, name, ', '.join(args))
    else:
        runs = STR_RUNS.format(mdn, name, ', '.join(args))
    mck = parse_mocks(mocks)
    return TEMP_FUNC.format(STR_PRE_FUNC + name, inits, mck, runs, '')


def parse_varis(name, value):
    """
    """
    return STR_VARIS.format(name, value)


def parse_mocks(mocks):
    """
    """
    txt = []
    if not mocks:
        return ''
    txt.append(STR_WITH)
    for i, m in enumerate(mocks):
        txt.append(STR_MOCK.format(m[0], 'm' + str(i + 1)))
        if len(mocks) - 1 == i:
            txt[-1] += ':'
        else:
            txt[-1] += ',\\'
    return STR_RC.join(txt)
