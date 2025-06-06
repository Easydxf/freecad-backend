import FreeCAD
import ImportGui
import Part
import os
import sys
import logging
import SheetMetalUnfolder
import SheetMetal

logging.basicConfig(filename='sheetmetal_batch.log', level=logging.INFO, format='%(levelname)s: %(message)s')

if len(sys.argv) != 3:
    logging.error("Usage: convert_to_dxf.py <input_step_file> <output_directory>")
    sys.exit(1)

input_path = sys.argv[1]
output_dir = sys.argv[2]

if not os.path.isfile(input_path):
    logging.error(f"Input file does not exist: {input_path}")
    sys.exit(1)

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

THICKNESS_THRESHOLD = 5.0
DEFAULT_K_FACTOR = 0.3

doc = FreeCAD.newDocument("UnfoldSheetMetal")
ImportGui.insert(input_path, doc.Name)
doc.recompute()

PART_COUNT = 0
SUCCESS_COUNT = 0
FAIL_COUNT = 0

for obj in doc.Objects:
    if hasattr(obj, "Shape") and obj.TypeId == "Part::Feature":
        shape = obj.Shape
        dims = [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength]

        if min(dims) < THICKNESS_THRESHOLD:
            PART_COUNT += 1
            try:
                planar_faces = [f for f in shape.Faces if f.Surface.isPlanar()]
                if not planar_faces:
                    raise Exception("No planar faces found.")

                sm_obj = None
                for base_face in sorted(planar_faces, key=lambda f: f.Area, reverse=True):
                    try:
                        sm_obj = SheetMetal.makeSheetMetal(obj, base_face)
                        doc.recompute()
                        break
                    except Exception:
                        continue

                if not sm_obj:
                    raise Exception("Sheet Metal feature creation failed.")

                # Optional: Set K-factor here if needed
                sm_obj.KFactor = DEFAULT_K_FACTOR
                doc.recompute()

                flat_obj = SheetMetalUnfolder.Flatten(sm_obj)
                doc.recompute()

                output_file = os.path.join(output_dir, f"{obj.Name}_flat.dxf")
                __objs__ = [flat_obj]
                ImportGui.export(__objs__, output_file)
                del __objs__

                logging.info(f"[SUCCESS] Exported: {output_file}")
                SUCCESS_COUNT += 1
            except Exception as e:
                logging.error(f"[FAILED] {obj.Name}: {str(e)}")
                FAIL_COUNT += 1

logging.info(f"[DONE] Processed: {PART_COUNT}, Succeeded: {SUCCESS_COUNT}, Failed: {FAIL_COUNT}")
print(f"[DONE] Processed: {PART_COUNT}, Succeeded: {SUCCESS_COUNT}, Failed: {FAIL_COUNT}")
