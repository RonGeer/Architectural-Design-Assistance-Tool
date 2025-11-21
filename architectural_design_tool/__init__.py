bl_info = {
    "name": "Architectural Design Tool",
    "author": "RonGe",
    "version": (0, 1),
    "blender": (4, 5, 3),
    "description": "Blender-based Architectural Design Assistant Tool",
}
import bpy
from . import operators
from . import ui
from . import props


classes = [
    operators.Setbase,
    operators.Merge,
    operators.Extract,
    operators.Offset,
    operators.Twist,
    operators.Shift,
    operators.Carve,
    operators.Branch,
    # operators.Nest,
    props.ADTProps,
    ui.Prop_panel,
    ui.Merge_panel,
    ui.Branch_panel,
    ui.Extract_panel,
    ui.Offset_panel,
    ui.Twist_panel,
    ui.Shift_panel,
    
    # ui.Nest_panel,
    
    
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.adt_props = bpy.props.PointerProperty(type=props.ADTProps)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.adt_props


if __name__ == "__main__":
    register()
