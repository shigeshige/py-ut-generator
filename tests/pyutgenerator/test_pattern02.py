"""
test 002
"""


from tests.pyutgenerator.data import pattern02

from pyutgenerator import ast_util, files, run


def test_01():
    """
    test
    """
    file_name = pattern02.__file__
    module = ast_util.create_ast(file_name)
    mmodule = files.get_package_moduel(file_name)

    t_func = ast_util.get_function(module)[0]
    calls = ast_util.get_calls(t_func)
    has_return = ast_util._has_return_call(calls[0].ats, t_func)
    assert has_return

    mocks = ast_util.get_mocks(calls, module, mmodule)
    assert mocks[0].mock_path == 'f01'


def test_output():
    """
    test
    """
    file_name = pattern02.__file__
    module = ast_util.create_ast(file_name)

    mmodule = files.get_package_moduel(file_name)
    t_file = mmodule.get_test_file_name()
    ttt1 = run.make_test_code(module, mmodule, True)

    ttt2 = files.read_file(t_file)

    assert ttt1 == ttt2
