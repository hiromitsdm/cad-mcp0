"""
3.4 smoke test: connect to the MCP server over stdio, list tools,
call find_holes on the bracket fixture, and validate the result.

Run from repo root:
    venv/bin/python verify_server.py
"""
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

ROOT = Path(__file__).parent
FIXTURE = str(ROOT / "fixtures" / "bracket.step")
SERVER_CMD = str(ROOT / "venv" / "bin" / "python")
SERVER_SCRIPT = str(ROOT / "server.py")

EXPECTED_TOOLS = {
    "list_assembly_tree",
    "get_part_dimensions",
    "find_holes",
    "measure_distance",
    "get_mass_properties",
}


def _parse(call_result) -> any:
    """Return the parsed JSON value from a tool call result."""
    return json.loads(call_result.content[0].text)


async def main() -> bool:
    params = StdioServerParameters(command=SERVER_CMD, args=[SERVER_SCRIPT])
    ok = True

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # --- 3.4a: list tools ---
            tools_result = await session.list_tools()
            found = {t.name for t in tools_result.tools}
            missing = EXPECTED_TOOLS - found
            if missing:
                print(f"FAIL  missing tools: {missing}")
                ok = False
            else:
                print(f"OK    all 5 tools present: {sorted(found)}")

            # --- 3.4b: find_holes end-to-end ---
            r = await session.call_tool("find_holes",
                                        arguments={"file_path": FIXTURE})
            result = _parse(r)
            holes = result["holes"]

            if len(holes) == 4:
                print(f"OK    find_holes returned 4 holes")
            else:
                print(f"FAIL  find_holes: expected 4, got {len(holes)}")
                ok = False

            h = sorted(holes, key=lambda h: (h["center_x_mm"], h["center_y_mm"]))[0]
            pos_ok = abs(h["center_x_mm"] - (-42.0)) < 0.01 and abs(h["center_y_mm"] - (-22.0)) < 0.01
            dia_ok = abs(h["diameter_mm"] - 5.3) < 0.01
            if pos_ok and dia_ok:
                print(f"OK    hole[0] position=({h['center_x_mm']},{h['center_y_mm']}) diameter={h['diameter_mm']}")
            else:
                print(f"FAIL  hole[0]: {h}")
                ok = False

            # --- 3.4c: get_mass_properties (real geometry question) ---
            r2 = await session.call_tool("get_mass_properties",
                                         arguments={"file_path": FIXTURE,
                                                    "density_kg_m3": 2700.0})
            props = _parse(r2)
            mass_ok = abs(props["mass_kg"] - 0.159617) < 1e-4
            com = props["center_of_mass_mm"]
            com_ok = abs(com["z_mm"] - 5.0) < 0.001
            if mass_ok and com_ok:
                print(f"OK    get_mass_properties: mass={props['mass_kg']} kg  COM.z={com['z_mm']} mm")
            else:
                print(f"FAIL  mass_props: {props}")
                ok = False

            # --- 3.4d: list_assembly_tree ---
            r3 = await session.call_tool("list_assembly_tree",
                                         arguments={"file_path": FIXTURE})
            tree = _parse(r3)
            node = tree["root"]
            tree_ok = node["type"] == "part" and node["part_id"] == "root" and node["children"] == []
            if tree_ok:
                print(f"OK    list_assembly_tree: depth-1 tree, type=part")
            else:
                print(f"FAIL  tree: {node}")
                ok = False

    return ok


if __name__ == "__main__":
    passed = asyncio.run(main())
    print("\nLayer 3 smoke test:", "PASSED" if passed else "FAILED")
    sys.exit(0 if passed else 1)
