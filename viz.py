import webbrowser
import argparse
from pathlib import Path
from Visualizer import *
import ROOT
import os
import urllib.parse

parser = argparse.ArgumentParser(description="Visualize decay trees from ROOT TTree files.")
parser.add_argument("root_file", type=str, help="Path to the ROOT file containing the TTree.")
parser.add_argument("event_ind", nargs="?", type=int, help="Event index to visualize (alternative to -e/--event).")
parser.add_argument("--tree_name", type=str, default="Events", help="Name of the TTree in the ROOT file.")
parser.add_argument("-e", "--event", type=int, default=0, help="Event index to visualize.")
parser.add_argument("-s", "--save", default=False, action="store_true", help="Name for the output file.")
parser.add_argument("-do", "--dont_open", default=False, action="store_true", help="Don't open the output visualization in a browser.")
# For modifiers
parser.add_argument("--color_by", type=str, default=None, help="Tree branch name to color nodes by. Colors by pt by default -- use 'none' to disable.")
parser.add_argument("--annotate", nargs="*", default=[], help="Tree branch name to annotate nodes by.")
args = parser.parse_args()

f = ROOT.TFile(args.root_file)
tree = f.Get(args.tree_name)
if not tree:
    raise ValueError(f"Tree '{args.tree_name}' does not exist in the file. Try one of: {[key.GetName() for key in f.GetListOfKeys()[:10]]}")

if args.event_ind is not None:
    eventnum = args.event_ind
else:
    eventnum = args.event

custom_ids = {-9000007: "LQ-", 9000007: "LQ+"}
base_format = Visualizer.default_format.copy()

modifiers = []
if not args.color_by is None:
    if args.color_by.lower() != "none":
        modifiers.append(ColorByProp(args.color_by))
else: # color by pt by default
    modifiers.append(ColorByProp("GenPart_pt"))
for anno in args.annotate:
    modifiers.append(AnnotateProp(anno))

# Configure the Visualizer with a color modifier based on particle transverse momentum
viz = Visualizer(custom_ids=custom_ids, 
                 base_format=base_format,
                 modifiers=modifiers
)

# Make a tree for event
g = viz.make_tree(tree, eventnum)
svg_bytes = g.pipe(format='svg')

save_name = args.root_file.split("/")[-1].replace(".root", f"_event{eventnum}.svg")
if args.save:
    with open(save_name, "wb") as f:
        f.write(svg_bytes)
    print(f"Saved SVG to {save_name}")

# Open the file in a browser
if not args.dont_open:
    svg_str = svg_bytes.decode("utf-8")
    svg_encoded = urllib.parse.quote(svg_str)
    data_uri = f"data:image/svg+xml,{svg_encoded}"
    webbrowser.open(data_uri)