# Importation 🛸
*automagically install missing imports*

<a href="https://badge.fury.io/py/importation"><img src="https://badge.fury.io/py/importation.svg" alt="PyPI version"/></a>

Is this a good idea? Probably not.

Should you use this? Probably not.

## What is this?

`importation` hijacks the `import` keyword in Python to test if the module is importable, and auto-installs missing packages.

If you're in a virtual environment, it installs it to your current virtual environment. If not, it creates one at `__pypackages__/importation`, adds it to `sys.path` so packages are discoverable, and installs missing packages there.

It takes [PEP-582](https://www.python.org/dev/peps/pep-0582/) "Python local packages directory" one step further by resolving packages in `__pypackages__` plus auto-installing to them.

## How do I get it?
```
> python -m pip install importation --user
```

## How do I use it?
Just import it.

The act of importing it has the side effect of hijacking Python's import system.

```python
# example.py
import importation  # noqa: 401
import httpx

print("module resolved at", httpx.__file__)
```

Then
```
$ python test.py
# module resolved at /home/__pypackages__/importation/lib/python3.8/site-packages/httpx/__init__.py
```

To debug or view details of what it's doing set the `IMPORTATION_VERBOSE` environment variable:
```
$ IMPORTATION_VERBOSE=1 python test.py
```

## Disclaimer
This has not been tested beyond this extremely simple example.

## Credits
This package was inspired by [PEP-582](https://www.python.org/dev/peps/pep-0582/) and [magicimport.py](https://github.com/dheera/magicimport.py).