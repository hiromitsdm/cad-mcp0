"""
find_holes — detect cylindrical through- and blind-holes in a part.

Uses OCCT BRepAdaptor_Surface to classify faces as cylindrical, then groups
coaxial faces (counterbores, stepped holes) by axis-centre proximity within
tolerance_mm.  Returns the widest (largest-radius) section of each group as
the representative hole.
"""
import math
from tools._loader import load_part
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder


def find_holes(
    file_path: str,
    part_id: str = "root",
    tolerance_mm: float = 0.01,
) -> list[dict]:
    """
    Find cylindrical holes in a part.

    Returns position, axis, diameter, and depth for each hole in millimetres.
    Coaxial cylindrical faces (counterbores / stepped holes) within tolerance_mm
    are merged into one entry using the largest-diameter section.
    Returns [] if no holes are found.
    """
    shape = load_part(file_path, part_id)
    raw = _extract_cylinders(shape)
    groups = _group_coaxial(raw, tolerance_mm)
    return [_represent(g) for g in groups]


# ---------------------------------------------------------------------------

def _extract_cylinders(shape) -> list[dict]:
    """Return one dict per cylindrical face."""
    results = []
    for face in shape.faces():
        adp = BRepAdaptor_Surface(face.wrapped)
        if adp.GetType() != GeomAbs_Cylinder:
            continue
        cyl = adp.Cylinder()
        ax = cyl.Axis()
        loc = ax.Location()
        d = ax.Direction()
        depth = abs(adp.LastVParameter() - adp.FirstVParameter())
        results.append({
            "radius_mm": cyl.Radius(),
            "depth_mm": depth,
            "axis": [round(d.X(), 6), round(d.Y(), 6), round(d.Z(), 6)],
            "loc": (loc.X(), loc.Y(), loc.Z()),
        })
    return results


def _axes_parallel(a1: list, a2: list, tol: float = 1e-4) -> bool:
    """True if two unit-direction vectors are parallel (same or opposite)."""
    dot = sum(a1[i] * a2[i] for i in range(3))
    return abs(abs(dot) - 1.0) < tol


def _project_to_axis(point: tuple, axis_origin: tuple, axis_dir: list) -> float:
    """Scalar projection of point onto an infinite axis."""
    return sum((point[i] - axis_origin[i]) * axis_dir[i] for i in range(3))


def _dist_point_to_axis(point: tuple, axis_origin: tuple, axis_dir: list) -> float:
    """Perpendicular distance from point to infinite axis."""
    diff = [point[i] - axis_origin[i] for i in range(3)]
    proj = sum(diff[i] * axis_dir[i] for i in range(3))
    perp = [diff[i] - proj * axis_dir[i] for i in range(3)]
    return math.sqrt(sum(x * x for x in perp))


def _group_coaxial(cylinders: list[dict], tolerance_mm: float) -> list[list[dict]]:
    """
    Group cylindrical faces that share the same axis (within tolerance_mm).
    Each group will become one reported hole.
    """
    groups: list[list[dict]] = []
    for cyl in cylinders:
        placed = False
        for group in groups:
            rep = group[0]
            if not _axes_parallel(cyl["axis"], rep["axis"]):
                continue
            dist = _dist_point_to_axis(cyl["loc"], rep["loc"], rep["axis"])
            if dist <= tolerance_mm:
                group.append(cyl)
                placed = True
                break
        if not placed:
            groups.append([cyl])
    return groups


def _represent(group: list[dict]) -> dict:
    """
    Collapse a coaxial group into one hole entry.
    Use the face with the largest radius as the representative section.
    Centre is the axis origin of the representative face.
    """
    rep = max(group, key=lambda c: c["radius_mm"])
    loc = rep["loc"]
    return {
        "center_x_mm": round(loc[0], 4),
        "center_y_mm": round(loc[1], 4),
        "center_z_mm": round(loc[2], 4),
        "diameter_mm": round(rep["radius_mm"] * 2, 4),
        "depth_mm": round(rep["depth_mm"], 4),
        "axis": rep["axis"],
    }
