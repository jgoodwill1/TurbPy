#!/bin/bash

# Stop execution on error
set -e

# Step 1: Clean any previous builds
echo "Cleaning previous builds..."
rm -rf build/ dist/turbPy.egg-info/ TurbPy/*.c turbPy/*.so

# Step 2: Build the Cython extension
echo "Building Cython extension..."
python setup.py build_ext --inplace



# Step 3: Install the package system-wide
echo "Installing package system-wide..."


pip install cython numpy
pip install --no-build-isolation .

# Done
echo "Installation complete!"
