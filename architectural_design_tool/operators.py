import bpy
from . import functions as fun


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
        
        for attempt in range(props.max_attempts):
            addBox = fun.randomCube(props.min_size, props.max_size, props.max_area)
            
            is_intersecting = fun.isIntersect(baseBox, addBox)
            is_inside = fun.isInside(baseBox, addBox)
            
            if is_intersecting and not is_inside:
                fun.calBool(baseBox, addBox, "add")
                baseBox.name = "BaseBox"
                break
            else:
                # 清理不满足条件的立方体，继续下一次尝试
                fun.delobj(addBox)
                
                # 如果达到最大尝试次数，显示提示
                if attempt == props.max_attempts - 1:
                    self.report({'WARNING'}, 
                              f"无法在{props.max_attempts}次尝试内生成不重叠的立方体")

        return {"FINISHED"}
    
class Nest(bpy.types.Operator):
    """增加规则：Nest"""

    bl_idname = "ronge_adt.nest"
    bl_label = "Nest"

    def execute(self, context):
        props = context.scene.adt_props
        
        

        return {"FINISHED"}
