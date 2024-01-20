<h1 align = "center">Skeleton Repository</h1>

<div align = "justify">

The **`skeleton`** repository is configured to serve as a starting point for all the products and services related to this organization. The settings files are configured as the name `<file>.yaml` and are ignored via the `.gitignore` files, while the repository stores the `<file>.yaml-proto` to set up and quickly configure when moving systems.

## Getting Started

The module uses the **`yaml`** file-format to save the configurations of the settings under the key `config["configurations"]`, while the file description, and header is stored (optionally, for the developers) information and file description. The global `version` key can be checked to find the appropriate version of the configuration file, and settings may indicate different versioning stying.

```yaml
# file.yaml
version: v0.0.1 # currently this denotes the file version

about:
  description: long-description about the file goes here

configurations:
  # key is the instance/search object name
  key: values
```

The previously thought `.conf` and `.ini` file is ignored, as the configuration file does not properly allow indentation and sub-configuration settings that might be needed. The `yaml` file is treated as dictionary in `python` and allows all the dictionary handling abilities.

</div>
