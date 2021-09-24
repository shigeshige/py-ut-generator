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

@dataclass
class ParseFunc:
    """
    Parse Func Obj
    """
    name : str
    t_func: Optional[ast.FunctionDef] = None
    module_name: str = ''
    pakcage : str = ''
    args : List[str] = None
    calls : List[CallFunc] = None
    has_return: bool  = False
    class_name : str = ''
    mocks : List[MockFunc] = field(default_factory=list)
    class_func : bool = False
