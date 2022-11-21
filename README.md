# Revitron Dots

Place colored dots on Revit elements based on filter rules.


## Installation

Note that this extensions requires **pyRevit** and **Revitron** to be installed!

### Recommended Installation Methods

In order to use this extension it can either be installed with the [pyRevit CLI](https://www.notion.so/Manage-pyRevit-extensions-fa853768e94240b5b59803e5d7171be3) or using the Revitron [Package Manager](https://revitron-ui.readthedocs.io/en/latest/tools/rpm.html).

### Manual Installation

Alternatively it is also possible to simply clone the repository into the extension directory of pyRevit.

~~~
cd path\to\pyRevit\extensions
git clone https://github.com/revitron/revitron-dots.git revitron-dots.extension
~~~

## Configuration

The extension has to be configured using `.json` files that can be linked individually to Revit models using the 
`Revitron` > `Dots` > `Select Configuration File` button.

### JSON File Anatomy

A configuration file consits of one or more *sets*. Each set defines the *rules* and size that will be applied when running the extension.

~~~json
{
  "Set_01": {
    "radius": 0.5,
    "rules": [...]
  },
  "Set_02": {
    "radius": 0.3,
    "rules": [...]
  }
}
~~~

#### Rules

Rules are used to associate a color with a list of filters. A filter is an object that has two main properties &mdash; a `rule` and a list of `args`. A `rule` is basically just the name of a [Filter](https://revitron.readthedocs.io/en/latest/revitron.filter.html#revitron.filter.Filter) class method. The corresponding arguments can be passed using the `args` field.

~~~json
{
  "Set_01": {
    "radius": 0.5,
    "rules": [
      {
        "color": "#ff2288",
        "filters": [
          {
            "rule": "byStringContains",
            "args": ["Comments", "Some comment"]
          },
          {
            "rule": "...",
            "args": [...]
          }
        ]
      },
      ...
    ]
  },
  "Set_02": {
    ...
  }
}
~~~

A fully working example configuration can be found [here](https://github.com/revitron/revitron-dots/blob/master/example/config.json). It is recommended to use this file and modify to your needs.

## Commands

The following commands are included in the this extension and can be found in `Revitron` tab under the `Dots` pulldown.

| Name | Description |
| --- | --- |
| `Generate Dots in Active View` | Place dots according to the selected set of rules in the currently active view. Exiting dots will be removed. |
| `Remove Dots in View` | Remove all dots from the currently active view |
| `Select Configuartion File` | Select a `.json` configuration file to be linked to your currently active model. |