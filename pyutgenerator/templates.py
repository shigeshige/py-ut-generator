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
    # check
{}
"""

STR_PRE_FUNC = 'test_'

STR_FROM_IMPORT = 'form {} import {}'

STR_VARIS = '    {} = {}'

STR_RUNS = '    {}.{}({})'
STR_RUNS_RETURN = '    ret = {}.{}({})'


def parse_import(imps):
    """
    """
    return TEMP_IMPORT.format(imps)


def parse_func(name, pkg, mdn, inits, has_return, args):
    """
    """
    runs = ''
    if has_return:
        runs = STR_RUNS_RETURN.format(mdn, name, ', '.join(args))
    else:
        runs = STR_RUNS.format(mdn, name, ', '.join(args))
    return TEMP_FUNC.format(STR_PRE_FUNC + name, inits, runs, '')


def parse_varis(name, value):
    """
    """
    return STR_VARIS.format(name, value)
