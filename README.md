<h1 align = "center">Skeleton Repository</h1>

<div align = "justify">

The **`skeleton`** repository is configured to serve as a starting point for all the products and services related to this organization. The settings files are configured as the name `<file>.conf` and are ignored via the `.gitignore` files, while the repository stores the `<file>.conf-proto` to set up and quickly configure when moving systems.

## Getting Started

The [**`configparser`**](https://docs.python.org/3/library/configparser.html) is a core Python module that can handle configuration files like `*.ini` in Windows or `*.conf` for *nix systems. The file is read as an advanced `dict` that works as a wrapper on a variable. For example:

```shell
# usernames.conf
[DEFAULT]
  name = Debmalya Pramanik

[ADMINISTRATOR]
  name = neuralNOD INC.
```

Using the `configparser`, we can wrap the "username" from the command line/application level as:

```python
from configparser import ConfigParser

username = input("Select Username: ")
configuration = ConfigParser().read("usernames.conf")
print(configuration["name"])
```

</div>
