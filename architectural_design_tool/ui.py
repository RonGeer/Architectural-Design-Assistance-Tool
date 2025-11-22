import bpy

class Auto_panel(bpy.types.Panel):
    """自动生成"""
    
    bl_label = "Auto"
    bl_idname = "VIEW3D_PT_auto_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT"
    
    def draw(self, context):
        layout = self.layout
        
        # 基本参数区域
        box = layout.box()
        box.label(text="生成参数:")
        props = context.scene.adt_props
        box.prop(props, "auto_count", text="自动生成数量")
        box.prop(props, "auto_deformation_count", text="形变执行次数")
        box.prop(props, "auto_culling_count", text="剔除执行次数")
        box.prop(props, "auto_isorder", text="是否按序执行")
        
        # 保存选项区域
        box = layout.box()
        box.label(text="保存选项:")
        box.prop(props, "auto_isarrange", text="是否在场景中展示")
        box.prop(props, "auto_issave", text="是否自动保存")
        if props.auto_issave:
            # 使用两列布局，一行显示路径，一行显示按钮
            row = box.row()
            row.prop(props, "auto_savepath", text="保存路径")
            
            row = box.row()
            row.operator("ronge_adt.browse_save_path", text="浏览文件夹", icon='FILE_FOLDER')
        
        # 执行按钮
        layout.operator("ronge_adt.auto", text="开始自动生成")


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
        
class Extract_panel(bpy.types.Panel):
    """Extract生成"""

    bl_label = "+Extract"
    bl_idname = "VIEW3D_PT_Extract_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT"

    def draw(self, context):
        layout = self.layout
        
        layout.operator("ronge_adt.extract", text="增加Extract")
        
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
        

        
class Shift_panel(bpy.types.Panel):
    """Shift形变"""  
    
    bl_label = "@Shift"
    bl_idname = "VIEW3D_PT_shift_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT" 
    
    def draw(self, context):
        layout = self.layout        
        
        box = layout.box()
        box.label(text="生成参数:")
        props = context.scene.adt_props
        box.prop(props, "shift_maxoffset", text="最大剪切偏移")
        box.prop(props, "shift_maxcutbox", text="最大剪切体大小")
        layout.operator("ronge_adt.shift", text="Shift形变")
        
class Twist_panel(bpy.types.Panel):
    """Twist形变"""  
    
    bl_label = "@Twist"
    bl_idname = "VIEW3D_PT_twist_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT" 
    
    def draw(self, context):
        layout = self.layout        
        
        box = layout.box()
        box.label(text="生成参数:")
        props = context.scene.adt_props
        box.prop(props, "twist_maxangle", text="最大旋转角度")
        box.prop(props,"twist_cutinterval",text="剪切间隔")
        layout.operator("ronge_adt.twist", text="Twist形变")
        
class Carve_panel(bpy.types.Panel):
    """Carve剔除"""  
    
    bl_label = "@Carve"
    bl_idname = "VIEW3D_PT_carve_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT" 
    
    def draw(self, context):
        layout = self.layout        
        
        layout.operator("ronge_adt.carve", text="Carve剔除")
        
class Frature_panel(bpy.types.Panel):
    """Frature剔除"""
    
    bl_label = "@Frature"   
    bl_idname = "VIEW3D_PT_frature_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT" 
    
    def draw(self, context):
        layout = self.layout        
        
        box = layout.box()
        box.label(text="生成参数:")
        props = context.scene.adt_props
        box.prop(props, "frature_maxwidth", text="最大剔除宽度")
        box.prop(props, "frature_minwidth", text="最小剔除宽度")
        layout.operator("ronge_adt.frature", text="Frature剔除")
        
class Expland_panel(bpy.types.Panel):
    """Expland剔除"""

    bl_label = "@Expland"
    bl_idname = "VIEW3D_PT_expland_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ADT" 
    
    def draw(self, context):
        layout = self.layout        
        
        box = layout.box()
        box.label(text="生成参数:")
        props = context.scene.adt_props
        box.prop(props, "expland_maxoffset", text="最大偏移")
        box.prop(props, "expland_minoffset", text="最小偏移")
        layout.operator("ronge_adt.expland", text="Expland剔除")