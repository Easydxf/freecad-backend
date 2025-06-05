import FreeCAD
import ImportGui
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

doc = FreeCAD.newDocument()
ImportGui.insert(input_file, doc.Name)
doc.recompute()

__objs__ = [obj for obj in doc.Objects]
ImportGui.export(__objs__, output_file)
print(f"Exported {output_file}")
