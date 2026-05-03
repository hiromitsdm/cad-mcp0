{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 Goal: CAD-reasoning MCP server, STEP files, LLM-queryable, weekend build\
\
\uc0\u9500 \u9472 \u9472  Layer 1 \'97 Environment & primitives        [Day 1, ~2h]\
\uc0\u9474    \u9500 \u9472 \u9472  1.1 venv with Python 3.12\
\uc0\u9474    \u9500 \u9472 \u9472  1.2 pip install build123d, mcp\
\uc0\u9474    \u9500 \u9472 \u9472  1.3 Smoke test: load a public STEP file, list shapes\
\uc0\u9474    \u9492 \u9472 \u9472  1.4 Pick one canonical test STEP file (commit to repo)\
\uc0\u9474 \
\uc0\u9500 \u9472 \u9472  Layer 2 \'97 Geometry query functions        [Day 1, ~2h]\
\uc0\u9474    \u9500 \u9472 \u9472  2.1 list_assembly_tree(file) \u8594  JSON of part hierarchy\
\uc0\u9474    \u9500 \u9472 \u9472  2.2 get_part_dimensions(file, part_id) \u8594  bbox, volume\
\uc0\u9474    \u9500 \u9472 \u9472  2.3 find_holes(file, part_id, tolerance_mm) \u8594  list of holes\
\uc0\u9474    \u9500 \u9472 \u9472  2.4 measure_distance(file, feature_a, feature_b) \u8594  mm\
\uc0\u9474    \u9500 \u9472 \u9472  2.5 get_mass_properties(file, part_id, material) \u8594  mass, COM, inertia\
\uc0\u9474    \u9492 \u9472 \u9472  2.6 (stretch) detect_threads \'97 if time permits, else parked\
\uc0\u9474 \
\uc0\u9500 \u9472 \u9472  Layer 3 \'97 MCP wrapping                    [Day 2, ~3h]\
\uc0\u9474    \u9500 \u9472 \u9472  3.1 MCP server skeleton (Python SDK)\
\uc0\u9474    \u9500 \u9472 \u9472  3.2 Wrap each Layer-2 function as an MCP tool with schema\
\uc0\u9474    \u9500 \u9472 \u9472  3.3 Local Claude Code connection via .mcp.json\
\uc0\u9474    \u9492 \u9472 \u9472  3.4 Verify Claude can list and invoke tools\
\uc0\u9474 \
\uc0\u9500 \u9472 \u9472  Layer 4 \'97 Project skills                  [Day 2, ~1.5h]\
\uc0\u9474    \u9500 \u9472 \u9472  4.1 .claude/skills/cad-tool-design/SKILL.md\
\uc0\u9474    \u9492 \u9472 \u9472  4.2 .claude/skills/step-debugging/SKILL.md\
\uc0\u9474 \
\uc0\u9492 \u9472 \u9472  Layer 5 \'97 Validation & polish             [Day 3, ~3h]\
    \uc0\u9500 \u9472 \u9472  5.1 End-to-end demo: real STEP, real questions, verifiable answers\
    \uc0\u9500 \u9472 \u9472  5.2 README with install + demo\
    \uc0\u9500 \u9472 \u9472  5.3 Transcript review and export\
    \uc0\u9492 \u9472 \u9472  5.4 Submit}