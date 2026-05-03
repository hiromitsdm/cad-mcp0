"""
get_mass_properties — mass, centre of mass, and moments of inertia.

Uses OCCT BRepGProp for volume integration; density supplied by caller.
All lengths in mm, mass in kg, inertia in kg·mm².
"""
from tools._loader import load_part
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps


def get_mass_properties(
    file_path: str,
    part_id: str = "root",
    density_kg_m3: float = ...,
) -> dict:
    """
    Return mass, centre of mass, and principal moments of inertia for a part.

    density_kg_m3: material density in kg/m³ (required).
    Lengths in mm, mass in kg, inertia in kg·mm².
    """
    if density_kg_m3 is ...:
        raise TypeError("density_kg_m3 is required")

    shape = load_part(file_path, part_id)

    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped, props)

    volume_mm3 = props.Mass()          # OCCT "mass" = volume when no density set
    com = props.CentreOfMass()

    # inertia matrix from OCCT is volume-weighted (mm^5); scale to kg·mm²
    density_kg_per_mm3 = density_kg_m3 / 1e9
    mass_kg = volume_mm3 * density_kg_per_mm3

    mat = props.MatrixOfInertia()
    # diagonal entries are Ixx, Iyy, Izz in mm^5; convert to kg·mm²
    def to_kg_mm2(v_mm5: float) -> float:
        return round(v_mm5 * density_kg_per_mm3, 6)

    return {
        "part_id": part_id,
        "density_kg_m3": density_kg_m3,
        "volume_mm3": round(volume_mm3, 4),
        "mass_kg": round(mass_kg, 6),
        "center_of_mass_mm": {
            "x_mm": round(com.X(), 4),
            "y_mm": round(com.Y(), 4),
            "z_mm": round(com.Z(), 4),
        },
        "moments_of_inertia_kg_mm2": {
            "Ixx": to_kg_mm2(mat.Value(1, 1)),
            "Iyy": to_kg_mm2(mat.Value(2, 2)),
            "Izz": to_kg_mm2(mat.Value(3, 3)),
        },
    }
