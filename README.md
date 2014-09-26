# ogre_parse
==========

## Utilities for parsing OGRE resources in Python.
https://github.com/cyrfer/ogre_parse


The goal of this library is to provide tools to load, manipulate, and write OGRE resources.
Efforts are currently focused on the text-based "script" file formats (.material, .program, .compositor).

### Status:
1. Wrote parsers for many script objects. There is one known parse error at the moment.
2. Implemented string-ification of objects to support writing scripts.
3. Unit tests are plentiful, but more could be added.
4. Dirty-hack utilities show how to leverage the parsers and writers to apply transformations to script objects.

### Goals:
1. Complete tested script parsers and script writers.
2. Cooperate with Python package management systems (e.g. pip).
3. jQuery-like selectors for parsed results.


OGRE is documented here:
http://ogre3d.org
