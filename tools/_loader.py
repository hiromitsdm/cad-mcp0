"""
Shared STEP loading and shape-traversal utilities.

All tools import from here so the part_id scheme is consistent.
"""
from pathlib import Path
from build123d import import_step, Compound, Solid, Shape
from OCP.TopoDS import TopoDS_Iterator


def load_step(file_path: str) -> Shape:
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(file_path)
    return import_step(str(p))


def _direct_children(shape: Shape) -> list[Shape]:
    """Return the immediate child shapes of a Compound via OCCT iterator."""
    children = []
    it = TopoDS_Iterator(shape.wrapped)
    while it.More():
        raw = it.Value()
        # wrap back into a build123d Shape
        children.append(Shape.cast(raw))
        it.Next()
    return children


def _has_solid_children(shape: Shape) -> bool:
    if not isinstance(shape, Compound):
        return False
    return any(isinstance(c, (Solid, Compound)) for c in _direct_children(shape))


def build_tree(shape: Shape, part_id: str = "root") -> dict:
    """
    Recursively build the assembly-tree dict for a shape.
    Single Solid → depth-1 tree.  Compound → assembly with children.
    """
    raw_label = getattr(shape, "label", "") or ""
    name = raw_label if raw_label and raw_label != "COMPOUND" else f"part_{part_id}"

    if isinstance(shape, Solid) or not _has_solid_children(shape):
        return {
            "type": "part",
            "name": name,
            "part_id": part_id,
            "children": [],
        }

    children = []
    for i, child in enumerate(_direct_children(shape)):
        if isinstance(child, (Solid, Compound)):
            children.append(build_tree(child, f"{part_id}.{i}"))

    return {
        "type": "assembly",
        "name": name,
        "part_id": part_id,
        "children": children,
    }


def find_by_id(shape: Shape, target_id: str, current_id: str = "root") -> Shape | None:
    """
    Traverse the shape tree and return the sub-shape matching target_id.
    Returns None if not found.
    """
    if current_id == target_id:
        return shape

    if not isinstance(shape, Compound):
        return None

    for i, child in enumerate(_direct_children(shape)):
        if isinstance(child, (Solid, Compound)):
            result = find_by_id(child, target_id, f"{current_id}.{i}")
            if result is not None:
                return result

    return None


def load_part(file_path: str, part_id: str) -> Shape:
    """Load a STEP file and return the sub-shape identified by part_id."""
    root = load_step(file_path)
    if part_id == "root":
        return root
    shape = find_by_id(root, part_id)
    if shape is None:
        raise ValueError(f"part_id {part_id!r} not found in {file_path}")
    return shape
