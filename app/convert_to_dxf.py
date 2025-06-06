# Canvas document: FreeCAD_SheetMetal_Backend
# File: convert_to_dxf.py
import FreeCAD
import ImportGui
import os
import sys
import logging
import SheetMetalUnfolder
import SheetMetal
import Draft

logging.basicConfig(filename='sheetmetal_batch.log', level=logging.INFO, format='%(levelname)s: %(message)s')

def prompt_for_face_selection(planar_faces, obj_name):
    print(f"\nDetected planar faces for part: {obj_name}")
    print("Face areas:")
    for idx, face in enumerate(planar_faces):
        print(f"  {idx}: Area = {face.Area:.2f}")
    try:
        choice = input(f"Use default largest face (index 0) or select manually? [Y/n]: ").strip().lower()
        if choice == 'n':
            selected_idx = int(input(f"Enter face index (0 to {len(planar_faces)-1}): "))
            if 0 <= selected_idx < len(planar_faces):
                return planar_faces[selected_idx]
    except Exception as e:
        logging.error(f"User input error: {str(e)}")
    return planar_faces[0]  # default largest face

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

THICKNESS_THRESHOLD = 5.0  # mm
K_FACTOR = 0.33  # Default K-factor
PART_COUNT = 0
SUCCESS_COUNT = 0
FAIL_COUNT = 0

doc = FreeCAD.newDocument("UnfoldSheetMetal")
ImportGui.insert(input_path, doc.Name)
doc.recompute()
logging.info(f"Loaded STEP file: {input_path}")

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

                base_face = prompt_for_face_selection(planar_faces, obj.Name)

                sm_obj = SheetMetal.makeSheetMetal(obj, base_face)
                sm_obj.KFactor = K_FACTOR
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
                try:
                    logging.info(f"Falling back to 2D projection for: {obj.Name}")
                    view = Draft.makeShape2DView(obj, FreeCAD.ActiveDocument.addObject("Part::Feature", f"{obj.Name}_view"))
                    doc.recompute()
                    dxf_path = os.path.join(output_dir, f"{obj.Name}_fallback_projection.dxf")
                    ImportGui.export([view], dxf_path)
                    logging.info(f"[FALLBACK SUCCESS] Exported: {dxf_path}")
                    SUCCESS_COUNT += 1
                except Exception as e2:
                    logging.error(f"[FALLBACK FAILED] {obj.Name}: {str(e2)}")
                    FAIL_COUNT += 1

logging.info(f"[DONE] Processed: {PART_COUNT}, Succeeded: {SUCCESS_COUNT}, Failed: {FAIL_COUNT}")
print(f"[DONE] Processed: {PART_COUNT}, Succeeded: {SUCCESS_COUNT}, Failed: {FAIL_COUNT}")
