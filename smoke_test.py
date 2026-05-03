"""
Layer 1 smoke test: load bracket.step, verify bbox against ground truth.
Pass = exit 0. Fail = exit 1 with diff.
"""
import json
import sys
from pathlib import Path
from build123d import import_step

FIXTURE_DIR = Path(__file__).parent / "fixtures"
STEP_PATH = FIXTURE_DIR / "bracket.step"
TRUTH_PATH = FIXTURE_DIR / "bracket.truth.json"
TOLERANCE = 0.5  # mm — accounts for floating-point and STEP round-trip


def main():
    truth = json.loads(TRUTH_PATH.read_text())
    expected = truth["bbox_mm"]

    print(f"Loading {STEP_PATH} ...")
    shape = import_step(str(STEP_PATH))
    bb = shape.bounding_box()

    got = {"x": bb.size.X, "y": bb.size.Y, "z": bb.size.Z}

    ok = True
    for axis in ("x", "y", "z"):
        diff = abs(got[axis] - expected[axis])
        status = "OK" if diff <= TOLERANCE else "FAIL"
        if status == "FAIL":
            ok = False
        print(f"  bbox.{axis}: expected={expected[axis]:.2f}  got={got[axis]:.2f}  diff={diff:.4f}  [{status}]")

    if ok:
        print("\nSmoke test PASSED")
        sys.exit(0)
    else:
        print("\nSmoke test FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
