"""
measure_distance — Euclidean distance between two points on parts.

Each endpoint is a (part_id, selector) pair where selector is one of:
  "centroid"  — centre of the bounding box
  "bbox_min"  — minimum corner (smallest x, y, z)
  "bbox_max"  — maximum corner (largest x, y, z)
"""
import math
from tools._loader import load_part

SELECTORS = ("centroid", "bbox_min", "bbox_max")


def _resolve_point(file_path: str, part_id: str, selector: str) -> tuple[float, float, float]:
    if selector not in SELECTORS:
        raise ValueError(f"selector must be one of {SELECTORS}, got {selector!r}")
    shape = load_part(file_path, part_id)
    bb = shape.bounding_box()
    if selector == "centroid":
        c = bb.center()
        return (c.X, c.Y, c.Z)
    if selector == "bbox_min":
        return (bb.min.X, bb.min.Y, bb.min.Z)
    # bbox_max
    return (bb.max.X, bb.max.Y, bb.max.Z)


def measure_distance(
    file_path: str,
    part_id_a: str,
    selector_a: str,
    part_id_b: str,
    selector_b: str,
) -> dict:
    """
    Measure the Euclidean distance between two reference points on parts.

    selector_a / selector_b: "centroid" | "bbox_min" | "bbox_max"

    Returns distance in millimetres and the resolved coordinates of both points.
    """
    pa = _resolve_point(file_path, part_id_a, selector_a)
    pb = _resolve_point(file_path, part_id_b, selector_b)
    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pa, pb)))
    return {
        "distance_mm": round(dist, 4),
        "point_a": {"part_id": part_id_a, "selector": selector_a,
                    "x_mm": round(pa[0], 4), "y_mm": round(pa[1], 4), "z_mm": round(pa[2], 4)},
        "point_b": {"part_id": part_id_b, "selector": selector_b,
                    "x_mm": round(pb[0], 4), "y_mm": round(pb[1], 4), "z_mm": round(pb[2], 4)},
    }
