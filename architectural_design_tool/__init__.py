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

# from . import props


classs = [
    operators.ADT1,
    #   props.ADTProps,
    ui.ADT_panel,
]


def register():
    for cls in classs:
        bpy.utils.register_class(cls)

    # bpy.types.Scene.adt_props = bpy.props.PointerProperty(type=props.ADTProps)


def unregister():
    for cls in classs:
        bpy.utils.unregister_class(cls)

    # del bpy.types.Scene.adt_props


if __name__ == "__main__":
    register()
