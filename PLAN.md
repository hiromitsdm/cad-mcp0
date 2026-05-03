# CAD-MCP — Plan

<<<<<<< HEAD
Goal: CAD-reasoning MCP server, STEP files, LLM-queryable, weekend build

├── Layer 1 — Environment & primitives        [Day 1, ~2h]
=======
Goal: CAD-reasoning MCP server, STEP files, LLM-queryable, weekend build├── Layer 1 — Environment & primitives        [Day 1, ~2h]
>>>>>>> 58343126dcfacfc7c7343a22ab122d7c6a5392ea
│   ├── 1.1 venv with Python 3.12
│   ├── 1.2 pip install build123d, mcp
│   ├── 1.3 Smoke test: load a public STEP file, list shapes
│   └── 1.4 Pick one canonical test STEP file (commit to repo)
│
├── Layer 2 — Geometry query functions        [Day 1, ~2h]
│   ├── 2.1 list_assembly_tree(file) → JSON of part hierarchy
│   ├── 2.2 get_part_dimensions(file, part_id) → bbox, volume
│   ├── 2.3 find_holes(file, part_id, tolerance_mm) → list of holes
│   ├── 2.4 measure_distance(file, feature_a, feature_b) → mm
│   ├── 2.5 get_mass_properties(file, part_id, material) → mass, COM, inertia
│   └── 2.6 (stretch) detect_threads — if time permits, else parked
│
├── Layer 3 — MCP wrapping                    [Day 2, ~3h]
│   ├── 3.1 MCP server skeleton (Python SDK)
│   ├── 3.2 Wrap each Layer-2 function as an MCP tool with schema
│   ├── 3.3 Local Claude Code connection via .mcp.json
│   └── 3.4 Verify Claude can list and invoke tools
│
├── Layer 4 — Project skills                  [Day 2, ~1.5h]
│   ├── 4.1 .claude/skills/cad-tool-design/SKILL.md
│   └── 4.2 .claude/skills/step-debugging/SKILL.md
│
└── Layer 5 — Validation & polish             [Day 3, ~3h]
<<<<<<< HEAD
    ├── 5.1 End-to-end demo: real STEP, real questions, verifiable answers
    ├── 5.2 README with install + demo
    ├── 5.3 Transcript review and export
    └── 5.4 Submit

Total: ~11.5h budgeted, 12h target. Buffer: 0.5h. If overrun, drop 2.6 (threads) and 5.2 polish, never drop 5.1 (demo).
=======
├── 5.1 End-to-end demo: real STEP, real questions, verifiable answers
├── 5.2 README with install + demo
├── 5.3 Transcript review and export
└── 5.4 Submit

**Total: ~11.5h budgeted, 12h target.** Buffer: 0.5h. If overrun, drop 2.6 (threads) and 5.2 polish, never drop 5.1 (demo).
>>>>>>> 58343126dcfacfc7c7343a22ab122d7c6a5392ea
