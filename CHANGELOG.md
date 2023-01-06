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

## [Unreleased]

### Added

- `yaml_conf` is able to read, type-check custom user-defined dataclasses as field in dataclasses. ([#7](https://github.com/karthikrangasai/anton/pull/7))
- `yaml_conf` is able to read, type-check `typing.Dict` type feilds in dataclasses. ([#6](https://github.com/karthikrangasai/anton/pull/6))
- `yaml_conf` is able to read, type-check `typing.List` type feilds in dataclasses. ([#4](https://github.com/karthikrangasai/anton/pull/4))
- Added `yaml_conf` decorator which allows creating dataclasses from yaml files for primitive types by avoiding boilerplate code.

<!-- [0.1.0]: https://github.com/karthikrangasai/anton/releases/tag/v0.1.0 -->

<!--
Any new version:
[M.m.p]: https://github.com/karthikrangasai/anton/compare/v_M._m._p...vM.m.p
-->
