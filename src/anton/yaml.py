import inspect
from dataclasses import dataclass
from os import PathLike
from pathlib import Path
from typing import Union

from anton.core.getter import get_init_arguments
from anton.core.loader import yaml_load

StrOrBytesPath = Union[str, Path, PathLike]


def _yaml_conf_wrapper(
    cls,
    /,
    *,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
):

    dataclass_cls = dataclass(cls, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen)  # type: ignore
    actual_init = getattr(dataclass_cls, "__init__")
    setattr(dataclass_cls, "init_setter", actual_init)

    def __init__(self, conf_path: StrOrBytesPath) -> None:
        conf_as_dict = yaml_load(conf_path)
        pos_args, kw_args = get_init_arguments(
            conf_as_dict,
            getattr(dataclass_cls, "__dataclass_fields__"),
            [(x, y.annotation, y.default) for x, y in inspect.signature(actual_init).parameters.items()][1:],
        )
        getattr(self, "init_setter")(*pos_args, **kw_args)

    setattr(dataclass_cls, "__init__", __init__)

    return dataclass_cls


def yaml_conf(
    *,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
):
    """
    A super easy to use decorator that wraps the
    `dataclasses.dataclass <https://docs.python.org/3.8/library/dataclasses.html#dataclasses.dataclass>`_
    decorator to provide auto instantiation from yaml definitions with runtime type checking of values.

    Args:
        cls: A python class defintion with all the fields.
            (Refer to the docs of `dataclasses <https://docs.python.org/3.8/library/dataclasses.html>`_.)

        conf_path: Path to the yaml file containing the appropriate definition.
        init: If true (the default), a ``__init__()`` method will be generated.
              If the class already defines ``__init__()``, this parameter is ignored.
        repr: If true (the default), a ``__repr__()`` method will be generated.
        eq: If true (the default), an ``__eq__()`` method will be generated.
        order: If true (the default is False), ``__lt__()``, ``__le__()``, ``__gt__()``, and ``__ge__()`` methods will be generated.
        unsafe_hash: If False (the default), a ``__hash__()`` method is generated according to how eq and frozen are set.
        frozen: If ``True`` (the default is ``False``), assigning to fields will generate an exception.

    Returns:
        A dataclass definition equipped with auto instantiation from YAML files and runtime type checking.

    .. note::

        Except `conf_path` all other arguments to :py:func:`anton.yaml.yaml_conf` are directly passed on
        to :py:func:`dataclasses.dataclass`.


    Examples
    ________

    .. doctest::

        >>> import tempfile
        >>> from dataclasses import dataclass
        >>> from anton import yaml_conf
        >>>
        >>> @dataclass
        ... class Point:
        ...     x: int
        ...     y: int
        ...
        >>> @dataclass
        ... class LineSegment:
        ...     first_point: Point
        ...     second_point: Point
        ...
        >>> temp_file = tempfile.NamedTemporaryFile()
        >>> _ = temp_file.write(
        ... b\"""
        ... integer: 23
        ... string: "Hello world"
        ... point:
        ...     x: 0
        ...     y: 0
        ... line_segment:
        ...     first_point:
        ...         x: 10
        ...         y: 10
        ...     second_point:
        ...         x: 10
        ...         y: 10
        ... \""")
        >>> temp_file.flush()
        >>>
        >>> @yaml_conf()
        ... class ExampleClass:
        ...     integer: int
        ...     string: str
        ...     point: Point
        ...     line_segment: LineSegment
        ...
        >>> ExampleClass(conf_path=temp_file.name)
        ExampleClass(integer=23, string='Hello world', point=Point(x=0, y=0), line_segment=LineSegment(first_point=Point(x=10, y=10), second_point=Point(x=10, y=10)))

    .. testcleanup::

        >>> temp_file.close()

    """

    def wrap(cls):
        return _yaml_conf_wrapper(cls, repr=repr, eq=eq, order=order, unsafe_hash=unsafe_hash, frozen=frozen)

    return wrap
