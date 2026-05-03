"""
Generate bracket.step and bracket.truth.json.

Geometry: flat bracket, 100 × 60 × 10 mm, four M5-clearance holes
(diameter 5.3 mm, through) centred 8 mm from each corner edge.

Run from repo root:
    venv/bin/python fixtures/make_fixture.py
"""
import json
import math
from pathlib import Path
from build123d import (
    BuildPart,
    Box,
    Cylinder,
    Location,
    Locations,
    Align,
    Mode,
    export_step,
)

# --- geometry parameters (all mm) ---
LENGTH = 100.0
WIDTH = 60.0
THICKNESS = 10.0
HOLE_DIAMETER = 5.3        # M5 clearance
HOLE_RADIUS = HOLE_DIAMETER / 2.0
EDGE_OFFSET = 8.0          # centre-to-nearest-edge distance

# hole centre positions (x, y) in part frame, z=0 at bottom face
hole_xy = [
    (-LENGTH / 2 + EDGE_OFFSET, -WIDTH / 2 + EDGE_OFFSET),
    ( LENGTH / 2 - EDGE_OFFSET, -WIDTH / 2 + EDGE_OFFSET),
    (-LENGTH / 2 + EDGE_OFFSET,  WIDTH / 2 - EDGE_OFFSET),
    ( LENGTH / 2 - EDGE_OFFSET,  WIDTH / 2 - EDGE_OFFSET),
]

with BuildPart() as bracket:
    Box(LENGTH, WIDTH, THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN))
    for x, y in hole_xy:
        with Locations(Location((x, y, 0))):
            Cylinder(
                HOLE_RADIUS, THICKNESS,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
                mode=Mode.SUBTRACT,
            )

out_dir = Path(__file__).parent
step_path = out_dir / "bracket.step"
export_step(bracket.part, str(step_path))

# --- compute truth from the same parameters, not from OCC readback ---
hole_volume = math.pi * HOLE_RADIUS**2 * THICKNESS
gross_volume = LENGTH * WIDTH * THICKNESS
net_volume = gross_volume - 4 * hole_volume

truth = {
    "description": "Flat bracket 100×60×10 mm, four M5-clearance through-holes at corners",
    "bbox_mm": {"x": LENGTH, "y": WIDTH, "z": THICKNESS},
    "gross_volume_mm3": round(gross_volume, 4),
    "net_volume_mm3": round(net_volume, 4),
    "holes": [
        {
            "id": i,
            "center_x_mm": x,
            "center_y_mm": y,
            "center_z_mm": 0.0,
            "diameter_mm": HOLE_DIAMETER,
            "depth_mm": THICKNESS,
            "axis": [0, 0, 1],
        }
        for i, (x, y) in enumerate(hole_xy)
    ],
    "mass_density_kg_m3_reference": 2700.0,
    "mass_kg_at_reference_density": round(
        net_volume * 1e-9 * 2700.0, 6
    ),
}

truth_path = out_dir / "bracket.truth.json"
truth_path.write_text(json.dumps(truth, indent=2))

print(f"Written: {step_path}")
print(f"Written: {truth_path}")
print(f"Net volume: {net_volume:.1f} mm³  |  Mass (Al 2700): {truth['mass_kg_at_reference_density']:.6f} kg")
