---
name: cad-tool-design
description: Conventions for designing MCP tools in this CAD server. Apply when adding new tools or modifying existing tool schemas. Ensures consistency, LLM-friendliness, and unit safety across the tool surface.
---

# CAD Tool Design Conventions

When designing or modifying any MCP tool in this server, follow these conventions strictly.

## Naming
- Tool names are verb phrases: `find_holes`, `measure_distance`, `get_mass_properties`.
- Never noun-only names like `holes` or `dimensions`.
- Verbs by category: `list_*` for hierarchies, `get_*` for properties of one thing,
  `find_*` for searching matches, `measure_*` for spatial relationships,
  `detect_*` for heuristic recognition.

## Inputs
- Every tool that touches geometry takes `file_path` (absolute) as the first input.
- Every spatial tolerance uses `tolerance_mm` with a sensible default. Never make
  the LLM pass a tolerance for the simple case.
- Units must be in field names: `diameter_mm`, `density_kg_m3`. Never bare `diameter`.
- Optional inputs are explicit: do not require the LLM to pass `null`.

## Outputs
- Always JSON-serializable. Never return raw OCCT or build123d objects.
- "No matches" returns an empty array, never an error.
- Errors only for: invalid file path, malformed STEP, unsupported entity type.
- Coordinates in part-local frame unless the tool name explicitly says `world_*`.
- All physical quantities have units in field names.

## Tool description text (the `description` field)
- One sentence that says: what it returns, in what units, with what scope.
- Bad: "Returns information about holes."
- Good: "Find cylindrical holes in a part. Returns position, axis, diameter,
  and depth for each in millimeters."

## Adding a new tool
1. Write the schema in `tools/schemas.py` following these conventions.
2. Implement in `tools/<tool_name>.py` as a pure function.
3. Wire into the MCP server in `server.py`.
4. Add one row to the README's tool table.
5. Add one verifiable test case to `validation/cases.json`.
