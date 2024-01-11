# Minimal multiple dispatch framework.
# Type safe: if types not included in overload set exception is raised
# Author: Ugo Varetto
# SPDX license identifier: BSD-3-Clause

import sys
from typing import get_args

__max_args = 8


def __expand_unions(type_lists: list[list[type]], expanded: list[list[type]]):
    if len(type_lists) == 0:
        return
    tl = type_lists.pop()
    elem = 0
    while elem < len(tl) and len(get_args(tl[elem])) == 0:
        elem += 1
    if elem >= len(tl):
        expanded.append(tl)
    else:
        arg = get_args(tl[elem])
        for a in arg:
            type_lists.append(tl[:elem] + [a] + tl[elem + 1 :])
    __expand_unions(type_lists, expanded)


"""Expand Unions in cases where the type is represented as a list
of optional types separated with '|' e.g. 'float | int'.
This function generates all the possible combination of signatures generated
from the diffent types.

    Example:
    In [134]: expand_types([float, int | str | float, str, bool | float])
    Out[134]: 
        [[float, float, str, float],
         [float, float, str, bool],
         [float, str, str, float],
         [float, str, str, bool],
         [float, int, str, float],
         [float, int, str, bool]]
"""


def expand_types(types: list[type]) -> list[list[type]]:
    expanded = []
    __expand_unions([types], expanded)
    return expanded


"""Max number of arguments used for the overload resolution.

Only up to __max_args are used when genrating the key and selecting
the overloaded function/method to call.
Default is 8.
"""


def get_max_args() -> int:
    """Return the maximum number of arguments to use for overload resolution.

    Returns:
        Max number of arguments.
    """
    global __max_args
    return __max_args


def set_max_args(m: int) -> None:
    """Set maximum number of arguments to use for overload resolution.
    Args:
        m (int): maximum number of arguments
    Returns:
        None
    """
    global __max_args
    __max_args = m


def __create_overload_table(obj):
    """Create dictionary holding the (types) -> function mapping
    Args:
        obj (module | class): parent object containing the types --> function map
    Returns:
        None
    """
    if getattr(obj, "__overload_table", None):
        return
    else:
        setattr(obj, "__overload_table", dict())


"""Generate overloaded method
Adds a (key, value) pair into the overloaeded method table where:
    * key = (method name, (*types))
    * value = decorated function
Args:
    class_type (class): class type
    method_name (str): method name
    *types (*type): types
Returns:
    decorator
The invocation will match the type of the passed parameters with the function
stored in the overloads table.
"""


def dyn_dispatch(class_type, method_name, *types):
    expanded_types = expand_types(list(types))

    def decorator(f):
        __create_overload_table(class_type)
        global __max_args
        for ts in expanded_types:
            class_type.__overload_table[
                (method_name, tuple(t for t in ts for _ in range(__max_args)))
            ] = f

        def wrapper(*args):
            return f(*args)

        wrapper.__name__ = method_name
        return wrapper

    return decorator


"""Invoke overloaded method

Select function to invoke from type list and invoke function.

Args:
    f: function to invoke
Returns:
    decorated function
Raises:
    AttributeError: in case the overloads table is not found
    TypeError: in case an overload is not found
"""


def dyn_method(f):
    def wrapper(self, *args):
        global __max_args
        key = (f.__name__, tuple(type(t) for t in args for _ in range(__max_args)))
        # error checking, remove for faster execution
        if not getattr(self, "__overload_table", None):
            raise AttributeError(f"No overloaded methods found for '{f.__name__}'")
        if key not in self.__overload_table:
            raise TypeError(
                f"No overload found for method '{f.__name__}' with parameter type(s) '{key[1]}'"
            )
        return self.__overload_table[key](self, *args)

    wrapper.__name__ = f.__name__
    return wrapper


"""Generate overloaded function
Adds a (key, value) pair into the global overloaeded function table where:
    * key = (method name, (*types))
    * value = decorated function
Args:
    fun_name (str): overloaded function name
    *types (*type): types
Returns:
    decorator
The invocation will match the type of the passed parameters with the function
stored in the overloads table.
"""


def dyn_dispatch_f(fun_name, *types):
    expanded_types = expand_types(list(types))

    def decorator(f):
        module = sys.modules[__name__]
        __create_overload_table(module)
        for ts in expanded_types:
            module.__overload_table[(fun_name, tuple(t for t in ts))] = f

        def wrapper(*args):
            return f(*args)

        wrapper.__name__ = fun_name
        return wrapper

    return decorator


def dyn_fun(f):
    """Invoke overloaded function

    Select function to invoke from type list and invoke function.

    Args:
        f: function to invoke
    Returns:
        decorated function
    Raises:
        AttributeError: in case the overloads table is not found
        TypeError: in case an overload is not found
    """

    def wrapper(*args):
        module = sys.modules[__name__]
        key = (f.__name__, tuple(type(t) for t in args))
        # error checking, remove for faster execution
        if not getattr(module, "__overload_table", None):
            raise AttributeError(f"No overloaded methods found for '{f.__name__}'")
        if key not in module.__overload_table:
            raise TypeError(
                f"No overload found for method '{f.__name__}' with parameter type(s) '{key[1]}'"
            )
        return module.__overload_table[key](*args)

    wrapper.__name__ = f.__name__
    return wrapper
