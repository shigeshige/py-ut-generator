"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""
import ast
from dataclasses import dataclass, field
from typing import List, Optional


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
    values: List = field(default_factory=list)
    ats: Optional[ast.AST] = None


@dataclass
class MockFunc:
    """
    Mock Class
    """
    mock_path: str
    has_return: bool = False
    func_name: Optional[str] = None
    call_count: int = 1
    call_func: Optional[CallFunc] = None
    open_flg: bool = False


@dataclass
class ParseFunc:
    """
    Parse Func Obj
    """
    name: str
    t_func: Optional[ast.FunctionDef] = None
    module_name: str = ''
    pakcage: str = ''
    args: List[FuncArg] = field(default_factory=list)
    calls: List[CallFunc] = field(default_factory=list)
    has_return: bool = False
    class_name: str = ''
    mocks: List[MockFunc] = field(default_factory=list)
    class_func: bool = False

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
