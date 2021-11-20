"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""

from typing import List, cast

from pyutgenerator.objects import FuncArg, MockFunc, ParseFunc, CallFunc

STR_PRE_FUNC = 'test_'

TEMP_IMPORT = """
import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

{}
"""

TEMP_IMPORT_OPEN = """
import pytest
from unittest.mock import patch
from unittest.mock import mock_open
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
STR_MOCK_OPEN = "            patch('{}', mock_open(read_data='')) as {}"
STR_MOCK_RETURN0 = '        {}.return_value'
STR_MOCK_RETURN = '        {}.return_value = {}'
STR_MOCK_RETURN_MOCK = '        {}.return_value = MagicMock()'
STR_MOCK_RETURN_MOCK2 = '        {}.return_value.{} = MagicMock()'
STR_MOCK_RETURN_MUL = '        {}.side_effect = [{}]'
STR_MOCK_FUNC = '        {}.{} = MagicMock(return_value=None)'
STR_MOCK_FUNC2 = '{}.{} = MagicMock(return_value=None)'

STR_RC = '\n'
STR_ASSERT = '    assert {}'
STR_ASSERT_TAB = '        assert {}'
STR_TAB = '    '


def parse_import(pkg, mdn, mock_open_flg=False):
    """
    parse import
    """
    owenr = f'from {pkg} import {mdn}'
    if not pkg:
        owenr = f'import {mdn}'
    if not mock_open_flg:
        return TEMP_IMPORT.format(owenr)

    return TEMP_IMPORT_OPEN.format(owenr)


def parse_func(fpo: ParseFunc):
    """
    parse one function.
    """
    mdn = fpo.module_name
    run_txt = ''
    checks = ''

    if fpo.has_return:
        checks = parse_assert(['ret'], fpo.mocks)
    inits = '\n'.join([parse_varis(arg) for arg in fpo.args])

    if fpo.mocks:
        run_txt = STR_TAB
    if fpo.class_name:
        # call for Class
        if fpo.class_func:
            if fpo.has_return:
                runs = run_txt + \
                    STR_RUNS_RETURN.format(
                        mdn, fpo.class_name + '.' + fpo.name, ', '.join(fpo.get_arg_str()))
            else:
                runs = run_txt + STR_RUNS.format(mdn,
                                                 fpo.class_name + '.' + fpo.name,
                                                 ', '.join(fpo.get_arg_str()))
        else:
            runs = run_txt + STR_RUNS_PRE.format(mdn, fpo.class_name)
            if fpo.has_return:
                runs += run_txt + \
                    STR_RUNS_RETURN.format('target', fpo.name, ', '.join(fpo.get_arg_str()))
            else:
                runs += run_txt + \
                    STR_RUNS.format('target', fpo.name, ', '.join(fpo.get_arg_str()))
    else:
        if fpo.has_return:
            runs = run_txt + \
                STR_RUNS_RETURN.format(mdn, fpo.name, ', '.join(fpo.get_arg_str()))
        else:
            runs = run_txt + \
                STR_RUNS.format(mdn, fpo.name, ', '.join(fpo.get_arg_str()))
    mck = parse_mocks(fpo.mocks)
    mck_ret = parse_mocks_return(fpo.mocks)
    if fpo.mocks:
        txt_cheks = TEMP_FUNC_CHECK_TAB.format(checks)
    else:
        txt_cheks = TEMP_FUNC_CHECK.format(checks)

    return TEMP_FUNC.format(STR_PRE_FUNC + fpo.name, inits, mck, mck_ret, runs) + txt_cheks


def parse_varis(func_arg: FuncArg):
    """
    parse variers
    """
    value = 'None'
    if func_arg.values:
        value = '[' + ', '.join(map(str, func_arg.values)) + ']'
    if func_arg.dict_value.keys():
        value = str(func_arg.dict_value)
    elif func_arg.arg_type == 'dict':
        value = '{}'
    return STR_VARIS.format(func_arg.arg_name, value)


def _parse_mock_call(call_func: CallFunc, txt: str):
    """
    mock for mock
    """

    txts = []
    if call_func:
        for call in call_func.call_calls:
            ccall = cast(CallFunc, call)
            ttt = STR_MOCK_FUNC2.format(txt, ccall.func_name)
            txts.append(ttt)
            if ccall.call_calls:
                for cc2 in ccall.call_calls:
                    txts.extend(_parse_mock_call(cc2, ttt))
    return txts


def parse_mocks_return(mocks: List[MockFunc]):
    """
    m.return_value = None
    """
    txt = []
    for i, moc in enumerate(mocks):
        ttt = ''
        if moc.open_flg:
            continue
        if moc.call_func and moc.call_func.is_with:
            ttt = STR_MOCK_RETURN_MOCK.format('m' + str(i + 1))
            txt.append(ttt)
            ttt = STR_MOCK_RETURN_MOCK2.format('m' + str(i + 1), '__enter__')
            txt.append(ttt)
        elif moc.call_func and moc.call_func.call_calls:
            ttt = STR_MOCK_RETURN_MOCK.format('m' + str(i + 1))
            txt.append(ttt)
            txt.extend(_parse_mock_call(moc.call_func, STR_MOCK_RETURN0.format('m' + str(i + 1))))
        elif moc.has_return:
            if moc.call_count > 1:
                ttt = STR_MOCK_RETURN_MUL.format('m' + str(i + 1), ', '.join(['None'] * moc.call_count))
                txt.append(ttt)
            else:
                ttt = STR_MOCK_RETURN.format('m' + str(i + 1), 'None')
                txt.append(ttt)
            if moc.func_name:
                ttt = STR_MOCK_FUNC.format('m' + str(i + 1), moc.func_name)
                txt.append(ttt)

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
        if moc.open_flg:
            txt.append(STR_MOCK_OPEN.format(moc.mock_path, 'm' + str(i + 1)))
        else:
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
    return STR_RC.join([STR_ASSERT.format(asst) for asst in asserts])
