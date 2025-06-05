import FreeCAD
import ImportGui
import Part
import SheetMetalUnfolder
import os
import sys

input_file = sys.argv[1]
output_dir = sys.argv[2]

FreeCAD.newDocument("conversion")
doc = FreeCAD.ActiveDocument
ImportGui.insert(input_file, doc.Name)
doc.recompute()

for obj in doc.Objects:
    if hasattr(obj, "Shape") and obj.Shape.Faces:
        try:
            # Detect candidate sheet metal part: thin and with bends
            z_thickness = obj.Shape.BoundBox.ZLength
            if z_thickness < 10 and len(obj.Shape.Faces) > 6:
                # Attempt to unfold
                flat_name = f"{obj.Name}_flat"
                flat_obj = SheetMetalUnfolder.unfoldObject(obj)
                flat_obj.Label = flat_name
                doc.addObject("Part::Feature", flat_name).Shape = flat_obj
                doc.recompute()

                output_file = os.path.join(output_dir, f"{obj.Name}.dxf")
                ImportGui.export([doc.getObject(flat_name)], output_file)
                print(f"[INFO] Exported: {output_file}")
        except Exception as e:
            print(f"[ERROR] Failed to process {obj.Name}: {str(e)}")

print("[DONE] Conversion complete.")
