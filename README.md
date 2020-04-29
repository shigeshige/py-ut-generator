# py-ut-generator
This tools generate Python pytest UT code.

### feature

* create test python file in tests.
* create pytest function from each function.
* create mock patch.
* create argument to call.
* if function has return value, create assert return.



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
    # init
    modeles = None
    # run
    with\
            patch('pyutgenerator.ast_util._equals') as m1:
        ret = ast_util.get_function(modeles)

        # check
        assert ret

```
### for future

* write return_value.
* call default and pass test.
* genarete various parameters for test.

## Getting Started

not yet

### Prerequisites

not yet

```
not yet
```

### Installing

not yet


```
not yet
```



## Running

now No command line or shell.  
call python dilectry.

```
python pyutgen.py "Input File Name"
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
