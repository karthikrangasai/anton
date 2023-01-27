# Installation

## Install with pip

```bash
pip install anton
```

## Install from source

```bash
pip install "git+https://github.com/karthikrangasai/anton.git@master#egg=anton"
```

## Installation directions for contributors

**NOTE:** Please install ``anton`` with packages for testing and building docs.

- Fork the [repository](https://github.com/karthikrangasai/anton.git).
- Clone it locally

    ```bash
    git clone https://github.com/[your-username]/anton.git
    ```

- Change the working directory

    ```bash
    cd anton
    ```

- Install ``anton`` in editable mode with all extra packages for development

    ```bash
    poetry install --all-extras
    ```
