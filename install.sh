#!/bin/bash
# Name this install_viz.sh and make it executable

# 1. Create a new conda environment
conda create -n viz-env python=3.10 -y
conda init
conda activate viz-env

# 2. Install conda packages
conda install -c conda-forge root particle numpy matplotlib -y
pip install graphviz

# 3. Install your Python package
pip install git+https://github.com/lrburack/ROOT-Event-Visualizer.git

echo "Installation complete! Run: conda activate viz-env"