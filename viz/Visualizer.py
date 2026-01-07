from graphviz import Digraph
from particle import Particle
from viz.helpers import part_format
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

class Modifier:
    def __init__(self):
        pass

    def apply(self, node_props, tree):
        return node_props

class Visualizer:
    default_format = {"shape": "circle", "style": "filled", "fontname": "Times"}
    default_graph_attrs = {"rankdir": "TB", "splines": "true"}

    def __init__(self, modifiers:list[Modifier] = None, custom_ids:dict = None, base_format=None, graph_attrs:dict = None):
        self.modifiers = modifiers
        self.custom_ids = custom_ids if custom_ids is not None else {}
        self.base_format = base_format if base_format is not None else Visualizer.default_format
        self.graph_attrs = graph_attrs if graph_attrs is not None else Visualizer.default_graph_attrs

    def make_tree(self, tree, event_index):
        # 1. Load event
        # 2. Create dictionary of node attributes
        # 3. Go through modifications
        # 4. Render

        nbytes = tree.GetEntry(event_index)
        if nbytes <= 0:
            raise ValueError(f"Could not load event {event_index} from tree {tree.GetName()} with {tree.GetEntries()} entries.")

        # Collect nodes
        ids = tree.GenPart_pdgId
        node_props = [self.base_format.copy() for i in range(len(ids))]

        # Format labels
        for i, pid in enumerate(ids):
            if pid in self.custom_ids:
                label = self.custom_ids[pid]
            else:
                try:
                    p = Particle.from_pdgid(pid)
                    label = f"{p.name}"
                except:
                    label = f"{pid}"
            label = part_format(label)
            node_props[i]['label'] = f'<{label}>'
        
        for modifier in self.modifiers or []:
            node_props = modifier.modify(node_props, tree)

        # Render the tree
        g = Digraph(format="svg")
        for k, v in self.graph_attrs.items():
            g.attr(**{k: str(v)})
        mom = tree.GenPart_genPartIdxMother
        # Add nodes
        for i in range(len(ids)):
            g.node(str(i), **node_props[i])

        # Add edges
        for i in range(len(ids)):
            if mom[i] >= 0:
                g.edge(str(mom[i]), str(i))

        return g
    
#  ---------- Modifiers ----------

class ColorByProp(Modifier):
    def __init__(self, prop_name, cmap=None, colorbar=True, colorbar_label=None):
        super().__init__()
        self.prop_name = prop_name
        self.cmap = cmap
        if self.cmap is None:
            self.cmap = cm.get_cmap('pink_r')
        self.min_v = 0
        self.max_v = 0
        self.colorbar = colorbar
        self.colorbar_label = colorbar_label if colorbar_label is not None else prop_name

    def modify(self, node_props, tree):
        prop_values = getattr(tree, self.prop_name)

        self.min_v = min(prop_values)
        self.max_v = max(prop_values)
        denom = (self.max_v - self.min_v) + 1e-6

        normalized = [(v - self.min_v) / denom for v in prop_values]

        for i, t in enumerate(normalized):
            r, g, b, _ = self.cmap(t)
            node_props[i]["fillcolor"] = mcolors.to_hex((r, g, b))
            lum = 0.2126*r + 0.7152*g + 0.0722*b # fancy color theory way to decide text color
            node_props[i]["fontcolor"] = "black" if lum > 0.5 else "white"

        if self.colorbar:
            self.make_colorbar()

        return node_props
    
    def make_colorbar(self):
        fig, ax = plt.subplots(figsize=(2, 5))
        norm = mcolors.Normalize(vmin=self.min_v, vmax=self.max_v)
        cb1 = cm.ScalarMappable(norm=norm, cmap=self.cmap)
        cb1.set_array([])

        cbar = fig.colorbar(cb1, ax=ax)
        cbar.set_label(self.colorbar_label)
        plt.savefig(f"colorbar_{self.prop_name}.png", bbox_inches='tight')
        plt.close()

class AnnotateProp(Modifier):
    def __init__(self, prop_name, fmt=None):
        super().__init__()
        self.prop_name = prop_name
        self.fmt = fmt
        if self.fmt is None:
            self.fmt = prop_name + "={:.2f}"
        
    def modify(self, node_props, tree):
        prop_values = getattr(tree, self.prop_name)

        for i, v in enumerate(prop_values):
            node_props[i]['label'] = f'<{node_props[i]["label"][1:-1]}<BR/>{self.fmt.format(v)}>'

        return node_props
