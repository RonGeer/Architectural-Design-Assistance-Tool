import bpy
from . import functions as fun


class Merge(bpy.types.Operator):
    """增加规则：Merge"""

    bl_idname = "ronge_adt.merge"
    bl_label = "Merge"

    def execute(self, context):
        props = context.scene.adt_props
        
        # 根据max_attempts尝试生成满足条件的立方体
        for attempt in range(props.max_attempts):
            # 生成两个随机立方体
            baseBox = fun.randomCube(props.min_size, props.max_size, props.max_area)
            addBox = fun.randomCube(props.min_size, props.max_size, props.max_area)
            
            # 检查是否相交
            is_intersecting = fun.isIntersect(baseBox, addBox)
            is_inside = fun.isInside(baseBox, addBox)
            
            # 如果不相交也不包含，则应用布尔操作并退出循环
            if is_intersecting and not is_inside:
                # 应用布尔操作合并两个立方体
                fun.calBool(baseBox, addBox, "add")
                break
            else:
                # 清理不满足条件的立方体，继续下一次尝试
                fun.delobj(baseBox)
                fun.delobj(addBox)
                
                # 如果达到最大尝试次数，显示提示
                if attempt == props.max_attempts - 1:
                    self.report({'WARNING'}, 
                              f"无法在{props.max_attempts}次尝试内生成不重叠的立方体")

        return {"FINISHED"}
