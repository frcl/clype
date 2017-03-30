import inspect
import typing
from typing import List, GenericMeta
from enum import Enum


class ArgMode(Enum):
    Optional = 0
    Required = 1


class ArgNum(Enum):
    Single = 0
    Multiple = 1


def arg_info(anno):
    if (isinstance(anno, typing._Union)
            and anno.__args__[1] == type(None)):
        return (ArgMode.Optional,) + arg_info(anno.__args__[0])
    elif issubclass(anno, List): # might raise unitended TypeError
        return (ArgNum.Multiple,) + arg_info(anno.__args__[0])
    elif isinstance(anno, type) and not isinstance(anno, GenericMeta):
        return (anno,)
    else:
        raise TypeError()


def arg_type(anno):
    try:
        arg_spec = arg_info(anno)
    except TypeError:
        raise TypeError('Unable to parse type annotation "{}"' .format(anno))

    if ArgMode.Optional in arg_spec:
        mode = ArgMode.Optional
    else:
        mode = ArgMode.Required

    if ArgNum.Multiple in arg_spec:
        nargs = ArgNum.Multiple
    else:
        nargs = ArgNum.Single

    return (mode, nargs, arg_spec[-1])


def parse_annotations(func, argp):
    """Add arguments to argp, using type annotations of func

    Arguments
    ---------
    func: callable
        must have type annotations, else a TypeError is raised
    argp: argparse.ArgumentParser
        (sub)parser where arguments read from annotations should be added

    Recognized annotations
    ----------------------
    List[T]:
        arbitrary number of positional arguments of type T
        examples:
            foo(paths: List[Path]) -> foo _path_ [_path_ ...]
    Optional[bool]:
        optional flag
        examples:
            foo(v: Optional[bool]) -> foo -v
            foo(verbose: Optional[bool]) -> foo --verbose
    Optional[T]:
        value of type T given using flag
        examples:
            foo(num: Optional[int]) -> foo --num 3
            foo(names: Optional[List[str]]) -> foo --names lisa mike
    """
    sig = inspect.signature(func)

    for name, param in sig.parameters.items():
        arg_mode, arg_num, param_type = arg_type(param.annotation)
        arg_desc = {}
        names = []
        if arg_mode == ArgMode.Optional:
            if len(name) == 1:
                names.append('-' + name)
            else:
                names.append('--' + name)
        elif arg_mode == ArgMode.Required:
            names.append(name)

        if arg_num == ArgNum.Single:
            pass
        elif arg_num == ArgNum.Multiple:
            arg_desc['nargs'] = '+'

        if param_type == bool:
            arg_desc['action'] = 'store_true'
        else:
            arg_desc['type'] = param_type

        argp.add_argument(*names, **arg_desc)
