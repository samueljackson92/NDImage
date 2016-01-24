# NDImage

This tool is a based off an idea I had during my dissertation project. This tools is designed to take a dataset with > 3 dimensions and produce two dimensional projections using scikit-learn's ```manifold``` and ```decomposition``` packages. It also aims to provide an way to interactively examine parts of a projection through a graphical interface.

## Installation

This package requires PyQt4 to be installed on your system. In Mac OSX this can be done easily using homebrew:

```
brew install pyqt
```

Then clone the repository, ```cd`` into the folder and install using pip:

```
pip install -e .
```

## To Do
 - Support for visualising image datatsets
  - In particular, being able to see which image corresponds to a point in the projection
 - Support for evaluating the quality of a projection
