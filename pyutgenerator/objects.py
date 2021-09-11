"""
Generate test code tool

copyrigth https://github.com/shigeshige/py-ut-generator
"""
from dataclasses import dataclass, field
from typing import Any, List, Optional


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
    ats = None


@dataclass
class MockFunc:
    """
    Mock Class
    """
    mock_path: str
    has_return: bool = False
    func_name: Optional[str] = None

@dataclass
class ParseFunc:
    """
    Parse Func Obj
    """
    name : str
    t_func: Any = None
    mdn: Any = None
    pkg : str = ''
    args : List = None
    calls : List[CallFunc] = None
    has_return: bool  = False
    class_name : str = ''
    mocks : List[MockFunc] = field(default_factory=list)
    class_func : bool = False
