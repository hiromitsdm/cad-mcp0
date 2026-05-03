"""
get_part_dimensions — bounding box and volume of one part or assembly.
"""
from tools._loader import load_part


def get_part_dimensions(file_path: str, part_id: str = "root") -> dict:
    """
    Return the axis-aligned bounding box and volume of a part.

    Bounding box is in the part's own coordinate frame (world frame for
    the root shape).  Volume excludes voids (pockets, holes).

    Returns:
      part_id    str
      bbox_mm    {x, y, z}  — full extents in millimetres
      volume_mm3 float
    """
    shape = load_part(file_path, part_id)
    bb = shape.bounding_box()
    return {
        "part_id": part_id,
        "bbox_mm": {
            "x": round(bb.size.X, 4),
            "y": round(bb.size.Y, 4),
            "z": round(bb.size.Z, 4),
        },
        "volume_mm3": round(shape.volume, 4),
    }
