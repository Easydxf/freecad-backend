import FreeCAD
import ImportGui
import Part
import MeshPart
import os
import sys

input_file = sys.argv[1]
output_dir = sys.argv[2]

doc = FreeCAD.newDocument()
ImportGui.insert(input_file, doc.Name)
doc.recompute()

def is_sheet_metal_shape(obj):
    # Heuristic: thin, prismatic shape with large flat faces
    shape = obj.Shape
    thickness_threshold = 2.5  # mm
    try:
        bounds = shape.BoundBox
        thickness = min(bounds.XLength, bounds.YLength, bounds.ZLength)
        return thickness < thickness_threshold
    except:
        return False

def flatten_shape(shape):
    # Very simplified "flattening": project shape to XY plane
    sections = shape.Section(Part.makePlane(1000, 1000))
    projection = sections.Project([FreeCAD.Vector(0, 0, 1)])
    return projection

dxf_count = 0
for obj in doc.Objects:
    if hasattr(obj, "Shape") and is_sheet_metal_shape(obj):
        flat = flatten_shape(obj.Shape)
        export_path = os.path.join(output_dir, f"part_{dxf_count}.dxf")
        Part.export([flat], export_path)
        print(f"Exported: {export_path}")
        dxf_count += 1

print(f"Total DXFs created: {dxf_count}")
