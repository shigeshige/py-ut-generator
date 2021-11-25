"""
test 002
"""


from tests.pyutgenerator.data import pattern03

from pyutgenerator import ast_util, files, run


def test_get_variable_values():
    """
    test
    """

    file_name = pattern03.__file__
    module = ast_util.create_ast(file_name)
    t_func = ast_util.get_function(module)[0]

    ret = ast_util.get_variable_values(t_func, 'bbb', None)
    assert [i.value for i in ret] == [-1, 0, 1]


def test_output():
    """
    test
    """
    file_name = pattern03.__file__
    module = ast_util.create_ast(file_name)

    pkg, mdn = files.get_package_moduel(file_name)
    t_file = files.get_test_file_name(pkg, mdn)
    ttt1 = run.make_test_code(module, pkg, mdn, True)

    ttt2 = files.read_file(t_file)

    assert ttt1 == ttt2
