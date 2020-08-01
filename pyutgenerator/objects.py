
from dataclasses import dataclass

from typing import Optional


@dataclass
class CallFunc:
    module: str
    func_name: str
    has_return: bool = False
    module2: Optional[str] = None
    class_name: Optional[str] = None
    ats = None


@dataclass
class MockFunc:
    mock_path: str
    has_return: bool = False
    func_name: Optional[str] = None
