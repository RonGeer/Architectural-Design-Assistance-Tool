import bpy
from . import functions as fun

class Setbase(bpy.types.Operator):
    """设置激活物体为BaseBox"""

    bl_idname = "ronge_adt.setbase"
    bl_label = "SetBase"

    def execute(self, context):
        obj = context.active_object

        obj.name = "BaseBox"

        return {"FINISHED"}

class Merge(bpy.types.Operator):
    """增加规则：Merge"""

    bl_idname = "ronge_adt.merge"
    bl_label = "Merge"

    def execute(self, context):
        props = context.scene.adt_props
        
        baseBox = None
        if fun.isExists("BaseBox"):
            baseBox = bpy.data.objects["BaseBox"]
        else:
            baseBox = fun.randomCube(props.min_size, props.max_size, props.max_area)
            baseBox.name = "BaseBox"
        
        for attempt in range(props.max_attempts):
            addBox = fun.randomCube(props.min_size*props.add_box_size, props.max_size*props.add_box_size, props.max_area)
            
            is_intersecting = fun.isIntersect(baseBox, addBox)
            is_inside = fun.isInside(baseBox, addBox)
            
            if is_intersecting and not is_inside:
                fun.calBool(baseBox, addBox, "add")
                break
            else:
                fun.delobj(addBox)
                
                if attempt == props.max_attempts - 1:
                    self.report({'WARNING'}, 
                              f"无法在{props.max_attempts}次尝试内生成")
                    return {"CANCELLED"}

        return {"FINISHED"}
    
class Nest(bpy.types.Operator):
    """增加规则：Nest"""

    bl_idname = "ronge_adt.nest"
    bl_label = "Nest"

    def execute(self, context):
        props = context.scene.adt_props
        
        baseBox = None
        if fun.isExists("BaseBox"):
            baseBox = bpy.data.objects["BaseBox"]
        else:
            baseBox = fun.randomCube(props.min_size, props.max_size, props.max_area)
            baseBox.name = "BaseBox"
            
        addBox = None
        for attempt in range(props.max_attempts):
            addBox = fun.randomCube(props.min_size*props.add_box_size, props.max_size*props.add_box_size, props.max_area)
            
            is_intersecting = fun.isIntersect(baseBox, addBox)
            is_inside = fun.isInside(baseBox, addBox)
        
            if not is_intersecting and is_inside:
                break
            else:
                fun.delobj(addBox)
            
                if attempt == props.max_attempts - 1:
                        self.report({'WARNING'}, 
                                f"无法在{props.max_attempts}次尝试内生成") 
                        return {"CANCELLED"}
        
        fun.snapEdge(baseBox,addBox,"-z")
        
        return {"FINISHED"}

class Branch(bpy.types.Operator):
    """增加规则：Branch"""

    bl_idname = "ronge_adt.branch"
    bl_label = "Branch"

    def execute(self, context):
        props = context.scene.adt_props
        
        baseBox = None
        if fun.isExists("BaseBox"):
            baseBox = bpy.data.objects["BaseBox"]
        else:
            baseBox = fun.randomCube(props.min_size, props.max_size, props.max_area)
            baseBox.name = "BaseBox"
            
        addBox = None
        for attempt in range(props.max_attempts):
            addBox = fun.randomCube(props.min_size*props.add_box_size, props.max_size*props.add_box_size, props.max_area)
            
            is_intersecting = fun.isIntersect(baseBox, addBox)
            is_inside = fun.isInside(baseBox, addBox)
        
            if is_intersecting and not is_inside:
                fun.calBool(baseBox, addBox, "sub")
                break
            else:
                fun.delobj(addBox)
            
                if attempt == props.max_attempts - 1:
                        self.report({'WARNING'}, 
                                f"无法在{props.max_attempts}次尝试内生成") 
                        return {"CANCELLED"}
        
        return {"FINISHED"}