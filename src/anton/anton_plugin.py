from typing import Callable, Optional, Type

from mypy.nodes import ARG_NAMED, Argument, Var
from mypy.plugin import ClassDefContext, Plugin
from mypy.plugins import dataclasses
from mypy.plugins.common import add_method
from mypy.types import NoneType, UnionType


ANTON_DECORATORS = ["yaml_conf", "json_conf"]


def anton_dataclass_class_maker_callback(ctx: ClassDefContext) -> bool:
    """Hooks into the class typechecking process to add support for dataclasses."""
    transformer = dataclasses.DataclassTransformer(ctx)
    transformed = transformer.transform()
    if not transformed:
        return False

    conf_path_type = UnionType(
        [
            ctx.api.named_type("builtins.str"),
            ctx.api.named_type("os.PathLike"),
            ctx.api.named_type("pathlib.Path"),
        ]
    )

    init__conf_path__arg = Argument(
        variable=Var("conf_path", conf_path_type), type_annotation=conf_path_type, initializer=None, kind=ARG_NAMED
    )

    args = [init__conf_path__arg]

    add_method(ctx, "__init__", args=args, return_type=NoneType())

    return True


class AntonPlugin(Plugin):
    def get_class_decorator_hook(self, fullname: str) -> Optional[Callable[[ClassDefContext], None]]:
        if any(decorator_name in fullname for decorator_name in ANTON_DECORATORS):
            return anton_dataclass_class_maker_callback  # type: ignore
        return None


def plugin(version: str) -> Type[Plugin]:
    """
    `version` is the mypy version string
    We might want to use this to print a warning if the mypy version being used is
    newer, or especially older, than we expect (or need).
    """
    return AntonPlugin
