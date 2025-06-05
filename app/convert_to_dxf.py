import FreeCAD
import ImportGui
import Part
import Mesh
import sys
import os

input_path = sys.argv[1]
output_dir = sys.argv[2]

doc = FreeCAD.newDocument("conversion")
ImportGui.insert(input_path, doc.Name)
doc.recompute()

for obj in doc.Objects:
    if obj.TypeId == "Part::Feature":
        shape = obj.Shape
        # Heuristic: Identify flat-ish or thin parts likely to be sheet metal
        if shape.BoundBox.ZLength < 5:  # Adjust threshold as needed
            try:
                flat_face = max(shape.Faces, key=lambda f: f.Area)
                dxf_path = os.path.join(output_dir, f"{obj.Name}.dxf")
                Draft.makeShape2DView(obj, FreeCAD.ActiveDocument.addObject("Part::Feature", f"{obj.Name}_view"))
                doc.recompute()
                ImportGui.export([obj], dxf_path)
                print(f"[INFO] Exported: {dxf_path}")
            except Exception as e:
                print(f"[ERROR] Failed to export {obj.Name}: {str(e)}")

print("[DONE] Conversion complete.")
