"""
copyrigth https://github.com/shigeshige/py-ut-generator
"""

from pyutgenerator.objects import MockFunc
from typing import List


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

STR_PRE_FUNC = 'test_'

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


def parse_import(imps):
    """
    """
    return TEMP_IMPORT.format(imps)


def parse_func(
        name,
        pkg,
        mdn,
        inits,
        has_return,
        args,
        mocks: List[MockFunc],
        checks,
        class_name=None,
        class_func=False):
    """
    parse one function.
    """
    run_txt = ''
    if mocks:
        run_txt = STR_TAB
    if class_name is not None:
        # call for Class
        if class_func:
            if has_return:
                runs = run_txt + \
                    STR_RUNS_RETURN.format(mdn, class_name + '.' + name, ', '.join(args))
            else:
                runs = run_txt + STR_RUNS.format(mdn,
                                                 class_name + '.' + name,
                                                 ', '.join(args))
        else:
            runs = run_txt + STR_RUNS_PRE.format(mdn, class_name)
            if has_return:
                runs += run_txt + STR_RUNS_RETURN.format('target', name, ', '.join(args))
            else:
                runs += run_txt + STR_RUNS.format('target', name, ', '.join(args))
    else:
        if has_return:
            runs = run_txt + STR_RUNS_RETURN.format(mdn, name, ', '.join(args))
        else:
            runs = run_txt + STR_RUNS.format(mdn, name, ', '.join(args))
    mck = parse_mocks(mocks)
    mck_ret = parse_mocks_return(mocks)
    if mocks:
        txt_cheks = TEMP_FUNC_CHECK_TAB.format(checks)
    else:
        txt_cheks = TEMP_FUNC_CHECK.format(checks)

    return TEMP_FUNC.format(STR_PRE_FUNC + name, inits, mck, mck_ret, runs) + txt_cheks


def parse_varis(name, value):
    """
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
                txt.append(STR_MOCK_FUNC.format('m' + str(i + 1), moc.func_name))

    return STR_RC.join(txt)


def parse_mocks(mocks: List[MockFunc]):
    """
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
    """
    if tab:
        return STR_RC.join([STR_ASSERT_TAB.format(asst) for asst in asserts])
    else:
        return STR_RC.join([STR_ASSERT.format(asst) for asst in asserts])


def get_test_func(func_name):
    """
    test function name.
    """
    return STR_PRE_FUNC + func_name
