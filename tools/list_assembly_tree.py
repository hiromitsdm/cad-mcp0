"""
list_assembly_tree — return the part/assembly hierarchy of a STEP file.

Single parts produce a depth-1 tree (root node, children=[]).
Assemblies produce a recursive tree.  part_id values in the output
can be passed directly to other tools.
"""
from tools._loader import load_step, build_tree


def list_assembly_tree(file_path: str) -> dict:
    """
    Load a STEP file and return its part hierarchy as a tree.

    Returns {"root": <node>} where each node has:
      type       "part" | "assembly"
      name       str (STEP label, or auto-generated)
      part_id    str  ("root", "root.0", "root.0.1", …)
      children   list[node]  (empty for leaf parts)
    """
    shape = load_step(file_path)
    return {"root": build_tree(shape)}
