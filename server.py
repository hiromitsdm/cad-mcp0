"""
CAD-reasoning MCP server.

Exposes five tools over stdio for use with Claude Code (local only).
All geometry is computed by build123d (OCCT-backed).  STEP files are
loaded on each call — no shared state between calls.

Start manually:  venv/bin/python server.py
Claude Code picks it up automatically via .mcp.json.
"""
from mcp.server.fastmcp import FastMCP

from tools.list_assembly_tree import list_assembly_tree as _tree
from tools.get_part_dimensions import get_part_dimensions as _dims
from tools.find_holes import find_holes as _holes
from tools.measure_distance import measure_distance as _dist
from tools.get_mass_properties import get_mass_properties as _mass

mcp = FastMCP("cad-mcp")


@mcp.tool()
def list_assembly_tree(file_path: str) -> dict:
    """List the part/assembly hierarchy of a STEP file as a tree. Returns type, name, part_id, and children for each node; single parts produce a depth-1 tree with children=[]."""
    return _tree(file_path)


@mcp.tool()
def get_part_dimensions(file_path: str, part_id: str = "root") -> dict:
    """Return the axis-aligned bounding box extents and volume of a part. Extents in millimetres, volume in mm³."""
    return _dims(file_path, part_id)


@mcp.tool()
def find_holes(
    file_path: str,
    part_id: str = "root",
    tolerance_mm: float = 0.01,
) -> list:
    """Find cylindrical holes in a part. Returns position (mm), axis direction, diameter (mm), and depth (mm) for each hole. Returns [] if none found."""
    return _holes(file_path, part_id, tolerance_mm)


@mcp.tool()
def measure_distance(
    file_path: str,
    part_id_a: str,
    selector_a: str,
    part_id_b: str,
    selector_b: str,
) -> dict:
    """Measure Euclidean distance in mm between two reference points on parts. selector must be one of: centroid, bbox_min, bbox_max."""
    return _dist(file_path, part_id_a, selector_a, part_id_b, selector_b)


@mcp.tool()
def get_mass_properties(
    file_path: str,
    density_kg_m3: float,
    part_id: str = "root",
) -> dict:
    """Return mass (kg), centre of mass (mm), and principal moments of inertia (kg·mm²) for a part at the given material density."""
    return _mass(file_path, density_kg_m3, part_id)


if __name__ == "__main__":
    mcp.run()
