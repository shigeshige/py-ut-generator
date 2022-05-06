"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""
import ast
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Module:
    """
    基本のモジュール名、パッケージ
    """
    pakage_name: str = ''
    module_name: str = ''
    file_name: str = ''

    def get_test_file_name(self):
        """
        get test file name from input file.
        """
        return 'tests/' + self.pakage_name.replace('.', '/') + '/test_' + self.module_name + '.py'


@dataclass
class Value:
    """
    Const value class.
    """
    value: Any
    is_literal: bool = False
    description: str = ''
    imports: str = ''

    def __str__(self) -> str:
        if isinstance(self.value, str):
            return "'" + self.value + "'"
        return str(self.value) if self.is_literal else self.description


@dataclass
class CallFunc:
    """
    Function class
    """
    module: str
    func_name: str
    has_return: bool = False
    module2: Optional[str] = None
    class_name: Optional[str] = None
    ats: Optional[ast.Call] = None
    is_with: bool = False
    call_calls: List = field(default_factory=list)


@dataclass
class FuncArg:
    """
    Function arguments.
    """
    arg_name: str
    ats: Optional[ast.AST] = None
    values: List[Value] = field(default_factory=list)
    arg_type: str = ''
    dict_value: Dict = field(default_factory=dict)


@dataclass
class MockFunc:
    """
    Mock Class
    """
    mock_path: str = ''
    has_return: bool = False
    module: Module = Module()
    func_name: Optional[str] = None
    call_count: int = 1
    call_func: Optional[CallFunc] = None
    open_flg: bool = False


@dataclass
class RaiseEx:
    """
    raise info
    """
    excp: str = 'Exception'


@dataclass
class ParseFunc:
    """
    Parse Func Obj
    """
    name: str
    t_func: Optional[ast.FunctionDef] = None
    module: Module = Module()
    args: List[FuncArg] = field(default_factory=list)
    calls: List[CallFunc] = field(default_factory=list)
    has_return: bool = False
    class_name: str = ''
    mocks: List[MockFunc] = field(default_factory=list)
    raises: Optional[List[RaiseEx]] = None
    class_func: bool = False
    imports: List[str] = field(default_factory=list)

    def get_arg_str(self):
        """
        argument to str.
        """
        return [(x.arg_name + '[0]')
                if x.values else x.arg_name for x in self.args]

    def is_mock_open(self) -> bool:
        """
        is mock_open ?
        """
        return bool([elm for elm in self.mocks if elm.open_flg])

    def get_name(self):
        """
        get output name.
        """
        if self.class_func:
            return self.class_name + '.' + self.name
        return self.name
