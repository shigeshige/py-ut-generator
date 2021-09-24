"""
test 001
"""


from pyutgenerator import ast_util, files, run

from tests.pyutgenerator.data import pattern01


def test_01():
    """
    test
    """
    file_name = pattern01.__file__
    module = ast_util.create_ast(file_name)
    pkg, mdn = files.get_package_moduel(file_name)

    t_func = ast_util.get_function(module)[0]
    calls = ast_util.get_calls(t_func)
    has_return = ast_util._has_return_call(calls[0].ats, t_func)
    assert has_return

    mocks = ast_util.get_mocks(calls, module, pkg, mdn)
    assert mocks[0].mock_path == 'tests.pyutgenerator.data.pattern01.os.path'
