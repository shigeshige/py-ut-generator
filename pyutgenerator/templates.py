"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""

from typing import List

from pyutgenerator.objects import MockFunc, ParseFunc

STR_PRE_FUNC = 'test_'

TEMP_IMPORT = """
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

{}
"""

TEMP_FUNC = """
def {}():
    # plan
{}
    # do
{}
{}
{}
"""

TEMP_FUNC_CHECK = """
    # check
{}
"""
TEMP_FUNC_CHECK_TAB = """
        # check
{}
"""


STR_FROM_IMPORT = 'form {} import {}'

STR_VARIS = '    {} = {}'

STR_RUNS = '    {}.{}({})'
STR_RUNS_RETURN = '    ret = {}.{}({})'

STR_RUNS_PRE = '''    target = {}.{}()
'''

STR_WITH = '    with\\'
STR_MOCK = "            patch('{}') as {}"
STR_MOCK_RETURN = '        {}.return_value = {}'
STR_MOCK_FUNC = '        {}.{} = MagicMock(return_value=None)'

STR_RC = '\n'
STR_ASSERT = '    assert {}'
STR_ASSERT_TAB = '        assert {}'
STR_TAB = '    '


def parse_import(pkg, mdn):
    """
    parse import
    """
    owenr = f'from {pkg} import {mdn}'
    if not pkg:
        owenr = f'import {mdn}'

    return TEMP_IMPORT.format(owenr)


def parse_func(fpo: ParseFunc):
    """
    parse one function.
    """
    mdn = fpo.module_name
    run_txt = ''
    checks = ''

    if fpo.has_return:
        checks = parse_assert(['ret'], fpo.mocks)
    inits = '\n'.join([parse_varis(arg, 'None') for arg in fpo.args])

    if fpo.mocks:
        run_txt = STR_TAB
    if fpo.class_name:
        # call for Class
        if fpo.class_func:
            if fpo.has_return:
                runs = run_txt + \
                    STR_RUNS_RETURN.format(
                        mdn, fpo.class_name + '.' + fpo.name, ', '.join(fpo.args))
            else:
                runs = run_txt + STR_RUNS.format(mdn,
                                                 fpo.class_name + '.' + fpo.name,
                                                 ', '.join(fpo.args))
        else:
            runs = run_txt + STR_RUNS_PRE.format(mdn, fpo.class_name)
            if fpo.has_return:
                runs += run_txt + \
                    STR_RUNS_RETURN.format('target', fpo.name, ', '.join(fpo.args))
            else:
                runs += run_txt + \
                    STR_RUNS.format('target', fpo.name, ', '.join(fpo.args))
    else:
        if fpo.has_return:
            runs = run_txt + STR_RUNS_RETURN.format(mdn, fpo.name, ', '.join(fpo.args))
        else:
            runs = run_txt + STR_RUNS.format(mdn, fpo.name, ', '.join(fpo.args))
    mck = parse_mocks(fpo.mocks)
    mck_ret = parse_mocks_return(fpo.mocks)
    if fpo.mocks:
        txt_cheks = TEMP_FUNC_CHECK_TAB.format(checks)
    else:
        txt_cheks = TEMP_FUNC_CHECK.format(checks)

    return TEMP_FUNC.format(STR_PRE_FUNC + fpo.name, inits, mck, mck_ret, runs) + txt_cheks

def parse_varis(name, value):
    """
    parse variers
    """
    return STR_VARIS.format(name, value)


def parse_mocks_return(mocks: List[MockFunc]):
    """
    m.return_value = None
    """
    txt = []
    for i, moc in enumerate(mocks):
        if moc.has_return:
            txt.append(STR_MOCK_RETURN.format('m' + str(i + 1), 'None'))
            if moc.func_name:
                txt.append(STR_MOCK_FUNC.format(
                    'm' + str(i + 1), moc.func_name))

    return STR_RC.join(txt)


def parse_mocks(mocks: List[MockFunc]):
    """
    parse mocks.
    """
    txt = []
    if not mocks:
        return ''
    txt.append(STR_WITH)
    for i, moc in enumerate(mocks):
        txt.append(STR_MOCK.format(moc.mock_path, 'm' + str(i + 1)))
        if len(mocks) - 1 == i:
            txt[-1] += ':'
        else:
            txt[-1] += ',\\'
    return STR_RC.join(txt)


def parse_assert(asserts, tab=False):
    """
    parse assert.
    """
    if tab:
        return STR_RC.join([STR_ASSERT_TAB.format(asst) for asst in asserts])
    else:
        return STR_RC.join([STR_ASSERT.format(asst) for asst in asserts])
