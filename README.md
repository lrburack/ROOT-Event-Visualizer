# ROOT-Event-Visualizer
Configurable event visualizer for making particle trees from ROOT files 

<div align="center">
  <img style="width:80%; height:auto;" alt="image" src="https://github.com/user-attachments/assets/e992a7ed-fed7-4015-b62c-2d9df720c915" />
</div>
<p style="text-align:center;">
  A gluon-induced leptoquark production event, nodes colored by $p_T$. This plot was automatically generated from a root file.
</p>


Appearance is fully customizable through creating custom implementations of the Modifer class. Currently implemented are modifiers to color and annotate nodes with particle attributes. 

## Installation
`pip install git+https://github.com/lrburack/ROOT-Event-Visualizer.git`

Package dependencies:
`conda install conda-forge::root`
`pip install graphviz numpy matplotlib particle`

## Commandline usage
With the package installed, you can run 
`viz [root_file] [event_number] [options and flags]`

Options:
- --treename. The tree name to read events from ("Events" by default)
- -s/--save. Save the svg image?
- -do/--dont_open. Don't open the image in your browser?
- --color_by. The branch to color nodes by ("GenPart_pt" by default)
- --annotate. Branches to annotate. List space separated after flag 
