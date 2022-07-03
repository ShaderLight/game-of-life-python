# game-of-life-python ![GitHub last commit](https://img.shields.io/github/last-commit/shaderlight/game-of-life-python)
A simple implementation of The game of life in Python.

## Table of contents
* [Installation](#installation)
* [General information](#general-information)
    * [Features](#features)
    * [Sample structures](#sample-structures)
* [Building the project](#building-the-project)

## Installation
The project does not require any external libraries to work, aside from `Python` itself (should work with any version from `3.5` and above), as
it was written using only `tkinter`, `logging`, `json` and `os`.

The app can be run in two ways:
- By running the `run.py` script
- By using the binaries included in `Releases` (or compiled by yourself)

## General information
By default the size of grid of cells is `40x30` and the rules are `3/23` (Conway's rules), although
those are easily changeable in the source code.

### Features
- Painting the board by clicking and dragging the cursor across it
- Manual next state triggering
- Automatic clock triggering (by default the clock is adjustable between `1` and `20 Hz`)
- Clearing the board in one click
- Saving the board state to a `.json` file
- Loading the board state from a file

### Sample structures
In `saved_structures` folder there are some sample structures ready to be loaded for demonstrational purposes.
Keep in mind that if you change default grid dimensions, you won't be able to load sample structures as the saves
were created in `40x30` grid.

## Building the project
Building the project is not necessary, although it is fairly easy, using `cx_Freeze` and `setup.py`.
Simply run the following command in root directory.
```
python setup.py build
```