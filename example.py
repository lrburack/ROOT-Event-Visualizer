import ROOT
import matplotlib.pyplot as plt
from Visualizer import *
import sys

eventnum = int(sys.argv[1]) if len(sys.argv) > 1 else 0

# This example uses the Visualizer to create a customized decay tree visualization gluon-induced leptoquark production event
# Open a ROOT file and get a TTree
f = ROOT.TFile("Signal_LQToBMu_M_300_single.root")
tree = f.Get("Events")

custom_ids = {-9000007: "LQ-", 9000007: "LQ+"}
base_format = Visualizer.default_format.copy()
base_format.update({"shape": "ellipse", "fontsize": "12"})

# Configure the Visualizer with a color modifier based on particle transverse momentum
viz = Visualizer(custom_ids=custom_ids, 
                 base_format=base_format,
                 modifiers=[
    ColorByProp("GenPart_pt"),
    AnnotateProp("GenPart_pt", fmt="p<SUB>T</SUB>={:.0f}")
])

# Make a tree for event
g = viz.make_tree(tree, eventnum)
g.render(f"decay_tree_event", cleanup=True)