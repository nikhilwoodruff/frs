# Conventions
This document sets out the standards followed in setting variable names and any other names in this package, as well as the structure of the package.

## Variable names
When naming variables:
- only contain alphabetical and underscore characters may be used
- capitalised abbreviations should remain capitalised and abbreviated. Avoid abbreviating non-capitalised words, especially near capitalised abbreviated words
- compact names where possible, but prioritise readability. If one has both the hierachical FRS dataset field documentation, and the list of variable names from this package, each variable name in this package should be matchable to the original name without any other assistance

## Structure
General tools for the package are in the main folder. Within ```tables/``` there is a Python module for each FRS table. Each module contains a ```parse``` function which takes a line of the table and the current data for the lowest-level relevant entity (e.g. for an account, the person it refers to is passed, while for a household, only the household can be passed). After this function, the module can contain any auxilary data structures for parsing, e.g. account type names, and finally a list of all fieldnames added must be present. After this, any enumerable variables can be listed.