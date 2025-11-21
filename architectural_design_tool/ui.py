import bpy


class Merge_panel(bpy.types.Panel):
    """ADT交互"""

    bl_label = "+Merge"
    bl_idname = "VIEW3D_PT_custom_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT"

    def draw(self, context):
        layout = self.layout
        
        # 添加操作按钮
        layout.operator("ronge_adt.merge", text="增加Merge")
        
        # 添加分隔线
        layout.separator()
        
        # 添加参数控制
        box = layout.box()
        box.label(text="生成参数:")
        
        props = context.scene.adt_props
        box.prop(props, "min_size", text="最小生成形体")
        box.prop(props, "max_size", text="最大生成形体")
        box.prop(props, "max_area", text="最大生成范围")
        box.prop(props, "max_attempts", text="最大尝试次数")
