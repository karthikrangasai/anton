# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Added       -  for new features.
Changed     -  for changes in existing functionality.
Deprecated  -  for soon-to-be removed features.
Removed     -  for now removed features.
Fixed       -  for any bug fixes.
Security    -  in case of vulnerabilities.
-->

## [0.2.0]

### Added

- `anton.yaml_conf` is able to read, type-check any python class as feilds in dataclasses. ([#38](https://github.com/karthikrangasai/anton/pull/38))
- Introduced `anton.json_conf` - JSON support to anton. ([#27](https://github.com/karthikrangasai/anton/pull/37))
- Refactored the package. ([#36](https://github.com/karthikrangasai/anton/pull/36))
- A probable fix for github actions for release. ([#34](https://github.com/karthikrangasai/anton/pull/34))

### Removed

- All the features related to loading and parsing `TOML` configurations. ([#40]((https://github.com/karthikrangasai/anton/pull/40)))

## [0.1.0]

### Added

- Introduced `anton.toml_conf` - TOML support to anton. ([#27](https://github.com/karthikrangasai/anton/pull/27))
- Refactor `tests` module. ([#26](https://github.com/karthikrangasai/anton/pull/26))
- `anton.yaml_conf` is able to read, type-check `typing.Any` and `typing.Optional` type feilds in dataclasses. ([#22](https://github.com/karthikrangasai/anton/pull/22))
- `anton.yaml_conf` is able to read, type-check `typing.Tuple` type feilds in dataclasses. . ([#21](https://github.com/karthikrangasai/anton/pull/21))
- Refactor and rename all references of `pyyamlconf` to `anton`. ([#20](https://github.com/karthikrangasai/anton/pull/20))
- Setup `readthedocs` for the project. ([#17](https://github.com/karthikrangasai/anton/pull/17))
- Add basic documentation for the project. ([#16](https://github.com/karthikrangasai/anton/pull/16))
- Add basic information. ([#8](https://github.com/karthikrangasai/anton/pull/8))
- `pyyamlconf.yaml_conf` is able to read, type-check custom user-defined dataclasses as field in dataclasses. ([#7](https://github.com/karthikrangasai/anton/pull/7))
- `pyyamlconf.yaml_conf` is able to read, type-check `typing.Dict` type feilds in dataclasses. ([#6](https://github.com/karthikrangasai/anton/pull/6))
- `pyyamlconf.yaml_conf` is able to read, type-check `typing.List` type feilds in dataclasses. ([#4](https://github.com/karthikrangasai/anton/pull/4))
- Added `yaml_conf` decorator which allows creating dataclasses from yaml files for primitive types by avoiding boilerplate code.


[Unreleased]: https://github.com/karthikrangasai/anton/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/karthikrangasai/anton/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/karthikrangasai/anton/releases/tag/v0.1.0

<!--
Any new version:
[M.m.p]: https://github.com/karthikrangasai/anton/compare/v_M._m._p...vM.m.p
-->
