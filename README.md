<div align="center">

# anton

[![CI testing](https://github.com/karthikrangasai/anton/actions/workflows/ci-testing.yml/badge.svg)](https://github.com/karthikrangasai/anton/actions/workflows/ci-testing.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Documentation Status](https://readthedocs.org/projects/anton/badge/?version=latest)](https://anton.readthedocs.io/en/latest/?badge=latest)

<!-- [![PyPI](https://img.shields.io/pypi/v/anton)](Add PyPI Link here) -->
<!-- [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/karthikrangasai/anton/blob/master/training_notebook.ipynb) -->

</div>

`anton` is a Python library for auto instantiating yaml definitions to user defined dataclasses.

Avoid boilerplate and get runtime type checking before the objects are created.

<!-- ## Installation

```bash
pip install anton
``` -->

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

`yaml_conf` lets you avoid writing the biolerplate code for loading the `yaml` file and parsing the python dictionary to instantiate the Dataclass object as follows:

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
ExampleClass(integer=23, string='Hello world', point=Point(x=0, y=0), line_segment=LineSegment(first_point=Point(x=10, y=10), second_point=Point(x=10, y=10)))
```

## Roadmap

Currently the project only supports Python3.8

Runtime type checking is supported for the following types:
- int
- float
- str
- bool
- typing.List
- typing.Dict
- typing.Union
- Any user defined dataclass

The ultimate aim is to support all python versions Python3.8+ and all possible type combinations.

## Contributing

Pull requests are welcome !!! Please make sure to update tests as appropriate.

For major changes, please open an issue first to discuss what you would like to change.

Please do go through the [Contributing Guide](https://github.com/karthikrangasai/anton/blob/master/CONTRIBUTING.md) if some help is required.

Note: `anton` currently in active development. Please [open an issue](https://github.com/karthikrangasai/anton/issues/new/choose) if you find anything that isn't working as expected.
