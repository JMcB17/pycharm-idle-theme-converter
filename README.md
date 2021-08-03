# pycharm-idle-theme-converter
There are plenty of great colour themes for [PyCharm](https://www.jetbrains.com/pycharm/) but not many for [IDLE](https://docs.python.org/3/library/idle.html).

You might still want to use IDLE though, as a light editor when you don't want to wait to open bigger ones, or because you're used to it.

The solution - convert PyCharm editor colour themes for use in IDLE with this easy tool.    
(todo: support vscode or something?)

## Installation
Pip commands:    
Windows    
```bat
py -m pip install idle-theme-converter
```
GNU/Linux
```sh
python3 -m pip install idle-theme-converter
```

You can now use the tool with `python -m idletheme` or just `idletheme`.

## Usage
For usage information just do `idletheme -h`

Darcula
https://gist.github.com/AndBondStyle/4951e36afd0d939f54870ed553ea350d
https://github.com/JetBrains/intellij-community/blob/master/platform/platform-resources/src/DefaultColorSchemesManager.xml
https://github.com/JetBrains/intellij-community/tree/master/colorSchemes/src/colorSchemes
https://github.com/d1ffuz0r/pycharm-themes
https://github.com/phillipjohnson/intellij-colorblind-settings

self-hosting like a cool compiler B) because you can use it to import a theme into IDLE then use that IDLE to work on this program
