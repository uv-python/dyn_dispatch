# Dynamic dispatch

Simple implementation of multiple dispatch/multimethods.

Overloaded functions are stored inside a `(function name,(*types))` --> `function`
map and invoked by generating a key at run-time from the method/function name and
the list of types 

To allow for overloaded mehtods inside a class decorate an empty method with the @dyn_method decorator
and use the @dyn_dispatch decorator to generate overloaded versions of the declared method outside
the class definition.

Methods accepting a and/or returning a class instance (required to e.g. overload operators for vectors and matrices)
do not work with any of the multiple dispatch packages I have tried.

Note that strong typing is enforced, passing parameters of types different from the one
listed in the decorator will result in throwing an exception.

## Build

`python -m build`

### Type generation

`stubgen -p dyn_dispatch .`

### Run tests

`python -m unittest discover`

### Build documentation

`mkdocs build`

Documentation is found in `./dyn_dispatch/site_docs`.


### Example:


```python
    from typing import Self #required to accept and return class instances in methods
    # class definition   
    class AClass:
        def __init__(self, i: int):
            self.i = i

        @dyn_method #does not work with multimethods and multipledispatch
        def __add__(self, *_) -> Self:
            return self

        @dyn_method
        def set(self, *_) -> None:
            ...

    #overloaded methods
    
    @dyn_dispatch(AClass, "__add__", AClass)
    def add_obj(self, other: AClass) -> AClass:
        return AClass(self.i + other.i, self.i + other.i)

    @dyn_dispatch(AClass, "__add__", int)
    def add_int(self, i: int) -> AClass:
        return AClass(self.i + i, self.j + i)
    
    @dyn_dispatch(AClass, "set", int)
    def set_int(self, i: int):
        self.i = i

    @dyn_dispatch(AClass, "set", str)
    def set_str(self, s: str):
        self.set(int(s))

    # invoke set(int)
    a = AClass(3)
    a.set(10)
    assert a.i == 10

    # invoke set(str)
    a = AClass(4)
    a.set("10")
    assert a.i == 10
```

To generated overloaded versions of free functions use the @dyn_fun decorator to mark an empty function
as overloaeded and the @dyn_dispatch_f decorator to generate overloads.

### Example:


```python
    @dyn_fun
    def double(*_):
        ...

    @dyn_dispatch_f("double", int)
    def double_int(i: int) -> int:
        return 2 * i

    @dyn_dispatch_f("double", str)
    def double_str(s: str) -> str:
        return s + s

    # invoke double(int)
    a = double(2)
    assert a == 4

    # invoke double(str)
    a = double("10")
    assert a = 20
```

## Union types

When types are specified as `<type 1> | <type 2> | ...` all the possible
combinations of signatures are generated allowing to write code like:

```
    @dyn_fun
    def triple(*_):
        ...

    @dyn_dispatch_f("triple", float | int | str)
    def triple_impl(v: float | int | str) -> Any:
        return v + v + v
    
    assert triple(2) == 6
    assert triple("c") == "ccc"
    assert abs(triple(1.1) - 3.3) < 1e-15

```

Any type not in the list will result in an exception being thrown.
