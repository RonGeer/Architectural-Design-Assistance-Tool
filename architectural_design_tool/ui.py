import bpy


class ADT_panel(bpy.types.Panel):
    """ADT交互"""

    bl_label = "Get Start"
    bl_idname = "VIEW3D_PT_custom_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT"

    def draw(self, context):
        layout = self.layout
        layout.operator("ronge_adt.adt1", text="adt1")
        row = layout.row()
        row.prop(context.scene.adt_props, "number", text="数字")
