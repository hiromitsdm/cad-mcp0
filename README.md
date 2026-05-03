# cad-mcp

An MCP server that exposes CAD geometry reasoning over STEP files to LLMs. Drop a STEP file, ask geometry questions in natural language, get verifiable answers. Built on [build123d](https://github.com/gumyr/build123d) (OCCT-backed) and the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk). Runs locally with Claude Code.

## Install

Requires Python 3.12, arm64 (Apple Silicon) or x86-64.

```bash
git clone https://github.com/your-org/cad-mcp.git
cd cad-mcp
python3.12 -m venv venv
venv/bin/pip install -r requirements.txt
```

Smoke-test the install:

```bash
venv/bin/python smoke_test.py      # loads bracket.step, checks bbox
venv/bin/python verify_server.py   # connects over MCP stdio, calls all tools
```

## Run

The server starts automatically when Claude Code opens this directory (`.mcp.json` is included). To start it manually:

```bash
venv/bin/python server.py
```

To connect a different STEP file, pass its absolute path in any tool call — no server restart needed.

## Tools

| Tool | Returns |
|---|---|
| `list_assembly_tree` | Part/assembly hierarchy as a tree |
| `get_part_dimensions` | Bounding box (mm) and volume (mm³) |
| `find_holes` | Cylindrical holes: position, diameter, depth (mm) |
| `measure_distance` | Euclidean distance between part reference points (mm) |
| `get_mass_properties` | Mass (kg), centre of mass (mm), moments of inertia (kg·mm²) |

## Demo

Five questions asked against `fixtures/bracket.step` (100 × 60 × 10 mm aluminium bracket, four M5 clearance holes) in Claude Code with the MCP server connected.

---

**Is bracket.step a single part or an assembly?**

Tool: `list_assembly_tree`

```json
{
  "root": {
    "type": "part",
    "name": "part_root",
    "part_id": "root",
    "children": []
  }
}
```

Single part. `part_id: "root"` is passed to all other tools.

---

**What are the overall dimensions and volume?**

Tool: `get_part_dimensions`

```json
{
  "part_id": "root",
  "bbox_mm": { "x": 100.0, "y": 60.0, "z": 10.0 },
  "volume_mm3": 59117.5266
}
```

100 × 60 × 10 mm. Volume is net (material only) — gross minus the four holes.

---

**How many holes, what size?**

Tool: `find_holes`

```json
{
  "holes": [
    { "center_x_mm": -42.0, "center_y_mm": -22.0, "center_z_mm": 0.0,
      "diameter_mm": 5.3, "depth_mm": 10.0, "axis": [0.0, 0.0, 1.0] },
    { "center_x_mm":  42.0, "center_y_mm": -22.0, "center_z_mm": 0.0,
      "diameter_mm": 5.3, "depth_mm": 10.0, "axis": [0.0, 0.0, 1.0] },
    { "center_x_mm": -42.0, "center_y_mm":  22.0, "center_z_mm": 0.0,
      "diameter_mm": 5.3, "depth_mm": 10.0, "axis": [0.0, 0.0, 1.0] },
    { "center_x_mm":  42.0, "center_y_mm":  22.0, "center_z_mm": 0.0,
      "diameter_mm": 5.3, "depth_mm": 10.0, "axis": [0.0, 0.0, 1.0] }
  ]
}
```

Four M5-clearance (5.3 mm) through-holes at the corners, all normal to the XY plane.

---

**What is the space-diagonal distance corner to corner?**

Tool: `measure_distance` with `selector_a: "bbox_min"`, `selector_b: "bbox_max"`

```json
{
  "distance_mm": 117.047,
  "point_a": { "part_id": "root", "selector": "bbox_min",
               "x_mm": -50.0, "y_mm": -30.0, "z_mm": 0.0 },
  "point_b": { "part_id": "root", "selector": "bbox_max",
               "x_mm":  50.0, "y_mm":  30.0, "z_mm": 10.0 }
}
```

√(100² + 60² + 10²) = 117.047 mm. Both resolved points are included for traceability.

---

**Mass and centre of mass in aluminium?**

Tool: `get_mass_properties` with `density_kg_m3: 2700.0`

```json
{
  "mass_kg": 0.159617,
  "volume_mm3": 59117.5266,
  "center_of_mass_mm": { "x_mm": 0.0, "y_mm": 0.0, "z_mm": 5.0 },
  "moments_of_inertia_kg_mm2": {
    "Ixx": 48.772745,
    "Iyy": 132.122917,
    "Izz": 178.235373
  }
}
```

≈ 160 g. Centre of mass at geometric centroid (0, 0, 5) — expected for a symmetric bracket with symmetric holes.
