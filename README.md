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
pip install pyutgen
```

### genarete test code


```
pyutgen "Input File Name"
```


### sample input file

```

def get_function(modeles):
    """
    """
    funcs = []
    for stm in modeles.body:
        if _equals(stm, const.AST_FUCNTION):
            funcs.append(stm)
    return funcs
```

### sample out put

```

def test_get_function():
    # plan
    module = None
    # do
    with\
            patch('pyutgenerator.ast_util._equals') as m1:
        m1.return_value = None
        ret = ast_util.get_function(module)

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
