# Minimal multiple dispatch framework.
# Type safe: if types not included in overload set exception is raised
# Author: Ugo Varetto
# SPDX license identifier: BSD-3-Clause

from __future__ import annotations
from .dd import dyn_fun, dyn_method, dyn_dispatch, dyn_dispatch_f
from typing import Any


def test() -> bool:
    # Declarations

    ### Class
    class AClass:
        def __init__(self, i: int | float | str, j: int | float | str):
            self.i = i
            self.j = j

        @dyn_method
        def __add__(self, *_) -> AClass:
            ...

        @dyn_method
        def set(self, *_) -> None:
            ...

        @dyn_method
        def multi_type_add(self, *_) -> None:
            ...

    @dyn_dispatch(AClass, "__add__", AClass)
    def add_obj(self, other: AClass) -> AClass:
        return AClass(self.i + other.i, self.j + other.j)

    @dyn_dispatch(AClass, "__add__", int)
    def add_int(self, i: int) -> AClass:
        return AClass(self.i + i, self.j + i)

    @dyn_dispatch(AClass, "set", int)
    def set_int(self, i: int):
        # print("set_int called")
        self.i = i

    @dyn_dispatch(AClass, "set", float)
    def set_float(self, f: float):
        # print("set_float called")
        self.set(int(f))

    @dyn_dispatch(AClass, "set", str)
    def set_str(self, s: str):
        # print("set_str called")
        self.set(int(s))

    @dyn_dispatch(AClass, "set", int, int)
    def set_int_int(self, i: int, j: int):
        # print("set_int_int called")
        self.i, self.j = i, j

    @dyn_dispatch(AClass, "multi_type_add", int | float | str)
    def multi_type_add(self, a: int | float | str) -> AClass:
        self.i += a
        self.j += a
        return self

    ### Functions

    @dyn_fun
    def double(*_):
        ...

    @dyn_dispatch_f("double", float)
    def double_float(f: float) -> float:
        # print("double_float called")
        return 2 * f

    @dyn_dispatch_f("double", int)
    def double_int(i: int) -> int:
        # print("double_int called")
        return 2 * i

    @dyn_dispatch_f("double", str)
    def double_str(s: str) -> str:
        # print("double_str called")
        return s + s

    @dyn_fun
    def triple(*_):
        ...

    @dyn_dispatch_f("triple", float | int | str)
    def triple_impl(v: float | int | str) -> Any:
        return v + v + v

    # Tests
    a = AClass(1, 2)
    b = AClass(5, 6)
    c = a + b
    assert c.i == a.i + b.i
    assert c.j == a.j + b.j

    d = a + 2
    assert d.i == a.i + 2
    assert d.j == a.j + 2

    a.set(2)
    assert a.i == 2
    a.set(3.1)
    assert a.i == 3
    a.set("4")
    assert a.i == 4
    a.set(10, 20)
    assert a.i == 10 and a.j == 20
    try:
        a.set(10.1, 20.3)
        assert False
    except:
        assert True

    astr = AClass("str1", "str2")
    astr.multi_type_add("+2")
    assert astr.i == "str1" + "+2"
    assert astr.j == "str2" + "+2"

    aint = AClass(5, 6)
    aint.multi_type_add(2)
    assert aint.i == 7
    assert aint.j == 8

    assert double(3) == double_int(3)
    assert double(3.2) == double_float(3.2)
    assert double("6") == double_str("6")

    try:
        _ = double(True)
        assert False
    except:
        assert True

    assert triple(2) == 6
    assert triple("c") == "ccc"
    assert abs(triple(1.1) - 3.3) < 1e-15

    return True


if __name__ == "__main__":
    test()
    print("OK")
