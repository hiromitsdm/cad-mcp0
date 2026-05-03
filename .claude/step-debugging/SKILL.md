---
name: step-debugging
description: Debugging playbook for STEP file load failures and geometry parsing issues with build123d on Apple Silicon. Apply when STEP loading raises, or when results look geometrically wrong.
---

# STEP Debugging Playbook

## When `Solid.import_step(path)` raises

1. **Check Python architecture is arm64**:
   `python -c "import platform; print(platform.machine())"` should print `arm64`.
   Rosetta-x86_64 Python with arm64 wheels = mismatch errors.
2. **Check file exists and is readable**:
   `ls -la <path>` and `file <path>` (should say "ISO-10303 STEP" or similar).
3. **Try a known-good file first**:
   Use the canonical test fixture in `fixtures/` to confirm the issue is the file,
   not the install.
4. **Check STEP schema version**:
   STEP AP203, AP214, AP242 are all valid. build123d handles all three but
   AP242 has richer feature info. If a file is unusually old (AP203 only), some
   feature queries may return less data — this is expected, not a bug.
5. **OCCT-level errors**: `Standard_NoSuchObject` or `STEPControl_StepModelType`
   errors usually mean entity references in the STEP are broken. Open the file
   in a viewer to confirm. If the file works in FreeCAD/CAD-Assistant but not
   build123d, it's a build123d limitation — note it and move on.

## When geometry results look wrong

1. **Coordinate frame check**: did you assume world frame but the tool returns
   part-local? Check the tool's docstring. Per `cad-tool-design.md`, default is
   part-local.
2. **Units check**: STEP files can declare millimeters, inches, or meters in
   their unit context. build123d normalizes to mm by default but verify with
   `shape.bbox()` against expected dimensions.
3. **Tolerance check**: cylindrical surfaces in STEP are not always perfectly
   cylindrical due to tessellation. If `find_holes` misses obvious holes,
   loosen `tolerance_mm` from 0.01 to 0.1 and retry.
4. **Assembly vs part check**: bbox of an assembly is the union of its parts,
   not any single part. Don't compare assembly bbox to part bbox without
   `list_assembly_tree` to confirm scope.

## When in doubt
- Open the file in **CAD-Assistant** (free, multi-platform STEP viewer) for
  ground truth.
- The canonical fixture in `fixtures/` has hand-measured ground truth in
  `fixtures/<name>.truth.json`.

## Don't
- Don't add `try/except` blocks that swallow the error to "make it work."
  STEP errors are real signals.
- Don't switch CAD libraries mid-build to dodge a STEP issue. Diagnose first.
