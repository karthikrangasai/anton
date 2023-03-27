# anton

`anton` is a Python library for auto instantiating YAML or JSON definitions to user defined dataclasses.

Avoid boilerplate code of YAML or JSON loading and specific runtime type checking before the objects are created.

:::{note}
Currently ``anton`` only supports Python3.8.

Support for Python3.8+ and missing python types will be coming in further versions of the project.
:::

## Usage

Consider a hypothetical YAML configuration file being used:

```yaml
# saved in the file: index.yaml
"""
point1:
  x: 10
  y: 10
point2:
  x: 20
  y: 20
line_segment1:
  first_point:
    x: 0
    y: 0
  second_point:
    x: 10
    y: 10
line_segment2:
  first_point:
    x: 0
    y: 10
  second_point:
    x: 10
    y: 0
```

Assuming the dataclass definitions as:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

@dataclass
class LineSegment:
    first_point: Point
    second_point: Point
```


Before `anton`, to load the YAML configuration one had to ensure types in the YAML files are right and also ensure the exact keys are present in the YAML configuration.

```python
# Define the dataclass
from dataclasses import dataclass

@dataclass
class CustomInput:
    point1: Point
    point2: Point
    line_segment1: LineSegment
    line_segment2: LineSegment


# Loading the YAML configuration to the dataclass:
import typing
import yaml

with open("index.yaml") as stream:
    try:
        conf_dict = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise exc

if not all(key in conf_dict.keys() for key in ["point1", "point2", "line_segment1", "line_segment2"]):
    raise ValueError("Input all the required keys.")

if not (isinstance(conf_dict["point1"], typing.Dict) and all(arg in conf_dict["point1"].keys() for arg in ["x", "y"])):
    raise ValueError("Input `point1` as a mapping with keys `x` and `y`.")

if not (isinstance(conf_dict["point2"], typing.Dict) and all(arg in conf_dict["point2"].keys() for arg in ["x", "y"])):
    raise ValueError("Input `point2` as a mapping with keys `x` and `y`.")

if not (
    isinstance(conf_dict["line_segment1"], typing.Dict)
    and all(arg in conf_dict["line_segment1"].keys() for arg in ["first_point", "second_point"])
):
    raise ValueError("Input `line_segment1` as a mapping with keys `first_point` and `second_point`.")

if not (
    isinstance(conf_dict["line_segment2"], typing.Dict)
    and all(arg in conf_dict["line_segment2"].keys() for arg in ["first_point", "second_point"])
):
    raise ValueError("Input `line_segment2` as a mapping with keys `first_point` and `second_point`.")

custom_input = CustomInput(
    point1=Point(**conf_dict["point1"]),
    point2=Point(**conf_dict["point2"]),
    line_segment1=LineSegment(
        first_point=conf_dict["line_segment1"]["first_point"],
        second_point=conf_dict["line_segment1"]["second_point"],
    ),
    line_segment2=LineSegment(
        first_point=conf_dict["line_segment2"]["first_point"],
        second_point=conf_dict["line_segment2"]["second_point"],
    ),
)
```

With `anton`, all the boilerplate can be avoided by using the decorators `yaml_conf` and `json_conf` that wraps the `dataclasses.dataclass` decorator to provide auto instantiation from YAML and JSON definitions respectively with runtime type checking of values. This helps avoid writing the biolerplate code for loading these definitions.

```python
import anton

@anton.yaml_conf(conf_path="index.yaml")
class CustomInput:
    point1: Point
    point2: Point
    line_segment1: LineSegment
    line_segment2: LineSegment

```
