# anton

`anton` is a Python library for auto instantiating yaml definitions to user defined dataclasses.

Avoid boilerplate code of yaml loading and specific runtime type checking before the objects are created.

`yaml_conf` handles type checking for almost all python types.

```{note}

    Currently `anton` only supports Python3.8.

    Support for Python3.8+ and missing python types will be coming in further versions of the project.
```

## Usage

Given a `yaml` file definition in a file `index.yaml` as follows:

```yaml
# index.yaml
integer: 23
string: "Hello world"
point:
  x: 0
  y: 0
line_segment:
  first_point:
    x: 10
    y: 10
  second_point:
    x: 10
    y: 10
```

`anton` provides a super easy to use decorator `yaml_conf` that wraps the `dataclasses.dataclass` decorator to provide auto instantiation from yaml definitions with runtime type checking of values.

This helps avoid writing the biolerplate code for loading `yaml` files as follows:

```py
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
>>> @yaml_conf(conf_path="index.yaml")
... class ExampleClass:
...     integer: int
...     string: str
...     point: Point
...     line_segment: LineSegment
...
>>> example_obj = ExampleClass()
>>> example_obj
ExampleClass(
    integer=23,
    string='Hello world',
    point=Point(x=0, y=0),
    line_segment=LineSegment(
        first_point=Point(x=10, y=10),
        second_point=Point(x=10, y=10)
    )
)
```
