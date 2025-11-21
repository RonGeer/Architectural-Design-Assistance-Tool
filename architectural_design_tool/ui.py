import bpy

class Prop_panel(bpy.types.Panel):
    """全局参数"""

    bl_label = "Props"
    bl_idname = "VIEW3D_PT_prop_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT"
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("ronge_adt.setbase", text="设置BaseBox")
        
        # 添加参数控制
        box = layout.box()
        box.label(text="生成参数:")
        
        props = context.scene.adt_props
        box.prop(props, "min_size", text="最小生成形体")
        box.prop(props, "max_size", text="最大生成形体")
        box.prop(props, "max_area", text="最大生成范围")
        box.prop(props, "max_attempts", text="最大尝试次数")
        box.prop(props, "add_box_size", text="附加体比例")


class Merge_panel(bpy.types.Panel):
    """Merge生成"""

    bl_label = "+Merge"
    bl_idname = "VIEW3D_PT_merge_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT"

    def draw(self, context):
        layout = self.layout
        
        layout.operator("ronge_adt.merge", text="增加Merge")
        
         
# class Nest_panel(bpy.types.Panel):
#     """Nest生成"""

#     bl_label = "+Nest"
#     bl_idname = "VIEW3D_PT_nest_panel"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "ADT"

#     def draw(self, context):
#         layout = self.layout

#         layout.operator("ronge_adt.nest", text="增加Neste")
        
        
class Branch_panel(bpy.types.Panel):
    """Branch生成"""  
    
    bl_label = "+Branch"
    bl_idname = "VIEW3D_PT_branch_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT"

    def draw(self, context):
        layout = self.layout

        layout.operator("ronge_adt.branch", text="增加Branch")
        
class Offset_panel(bpy.types.Panel):
    """Offset形变"""  
    
    bl_label = "@Offset"
    bl_idname = "VIEW3D_PT_offset_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT"

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="生成参数:")
        props = context.scene.adt_props
        box.prop(props, "offset_minthick", text="最小厚度")
        box.prop(props, "offset_maxthick", text="最大厚度")
        box.prop(props, "offset_maxoffset", text="最大偏移")
        
        layout.operator("ronge_adt.offset", text="Offset形变")