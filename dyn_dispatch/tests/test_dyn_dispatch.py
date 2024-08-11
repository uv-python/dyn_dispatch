from typing import Any
import unittest as test
from dyn_dispatch import dyn_method, dyn_dispatch, dyn_fun, dyn_dispatch_f
from typing import Self


class AClass:
    def __init__(self, i: int, j: int = 0):
        self.i = i

    @dyn_method
    def __add__(self, *_) -> Self:
        return self

    @dyn_method
    def set(self, *_) -> str:  # return the typename
        return ""

# overloaded methods


@dyn_dispatch(AClass, "__add__", AClass)
def add_obj(self, other: AClass) -> AClass:
    return AClass(self.i + other.i, self.i + other.i)


@dyn_dispatch(AClass, "set", int)
def set_int(self, i: int):
    self.i = i
    return f"{type(i)}"


@dyn_dispatch(AClass, "set", str)
def set_str(self, s: str):
    self.set(int(s))
    return f"{type(s)}"


# overloaded functions


@dyn_fun
def double(_: Any) -> tuple[str, Any]:
    return ("", None)


@ dyn_dispatch_f("double", int)
def double_int(i: int) -> tuple[str, int]:
    return ("int", 2*i)


@ dyn_dispatch_f("double", str)
def double_str(i: int) -> tuple[str, int]:
    return ("str", 2*int(i))


class DynDispatchTest(test.TestCase):
    def test_method_dispatch(self):
        a = AClass(3)
        self.assertEqual(a.set(10), f"{type(10)}")
        self.assertEqual(a.i, 10)
        self.assertEqual(a.set("100"), f"{type("100")}")
        self.assertEqual(a.i, 100)

    def test_function_dispatch(self):
        t, r = double(10)
        self.assertEqual(t, "int")
        self.assertEqual(r, 20)
        t, r = double("100")
        self.assertEqual(t, "str")
        self.assertEqual(r, 200)


def run_tests():
    test.main()
