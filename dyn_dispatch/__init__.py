"""Implementation of multiple dispatch/multimethods.

To allow for overloaded mehtods inside a class decorate an empty method with the @dyn_method decorator
and use the @dyn_dispatch decorator to generate overloaded versions of the declared method outside
the class definition.

Example:
    # class definition   
    class AClass:
        def __init__(self, i: int, j: int = 0):
            self.i = i

        @dyn_method
        def __add__(self, *_) -> AClass:
            ...

        @dyn_method
        def set(self, *_) -> None:
            ...

    #overloaded methods
    
    @dyn_dispatch(AClass, "__add__", AClass)
    def add_obj(self, other: AClass) -> AClass:
        return AClass(self.i + other.i, self.j + other.j)

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

To generated overloaded versions of free functions use the @dyn_fun decorator to mark an empty function
as overloaeded and the @dyn_dispatch_f decorator to generate overloads.

Example:

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

"""
from dd import (
    get_max_args,
    set_max_args,
    dyn_dispatch,
    dyn_dispatch_f,
    dyn_method,
    dyn_fun,
)
from test import test
