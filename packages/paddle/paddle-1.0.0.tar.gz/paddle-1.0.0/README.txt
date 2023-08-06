
REQUIREMENTS:

- setuptools (http://pypi.python.org/pypi/setuptools)

- Scipy (http://www.scipy.org)

For generating the documentation you need:
- sphinx (http://pypi.python.org/pypi/sphinx), version 0.6.7. Newer versions
  do not get along with numpydoc.
- numpydoc (http://pypi.python.org/pypi/numpydoc)

INSTALLATION instructions:

All required extra packages (scipy, sphinx, etc) can be installed through PIP ...

...

DOCUMENTATION:

A sphinx-based documentation can be generated with the command:

sphinx-build docs/ outdir

where outdir is an existing directory where the html is generated, 
e.g. doc/html
