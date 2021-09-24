#  Python UT generator
This tools generate automatically Python pytest Unit test code.  
This project uses ast module to generate.  
Easy to make coverage test.

### feature

* Generate unit test python file in tests package.
* Generate pytest test function from each function.
* Generate mock patch syntax code.
* Generate argument syntax code to call.
* if function has return value, create assert return.

## Installation

### install pip

```
pip install pyutgenerator
```
https://pypi.org/project/pyutgenerator/


## Run tool.

### genarete test code


```
pyutgen "Input File Name"
```


### sample input file

```
import os


def aaaaa():
    """
    call and return
    """
    return os.path.exists('')

```

### sample out put

```

import pytest
from unittest.mock import patch
from unittest.mock import MagicMock

from tests.pyutgenerator.data import pattern01

def test_aaaaa():
    # plan

    # do
    with\
            patch('tests.pyutgenerator.data.pattern01.os.path') as m1:
        m1.return_value = None
        m1.exists = MagicMock(return_value=None)
        ret = pattern01.aaaaa()

        # check
        assert ret

```
### for future

* regist pypi.
* customize parameter options.
* parameter type for str,list, obj ...
* write return_value.
* exception check.
* call default and pass test.
* genarete various parameters for test.
* web ui for test.

### Prerequisites

not yet

```
not yet
```


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
