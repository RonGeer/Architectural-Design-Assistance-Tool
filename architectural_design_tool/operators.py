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
    """基形规则：Merge"""

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
            addBox = fun.randomCube(
                props.min_size * props.add_box_size,
                props.max_size * props.add_box_size,
                props.max_area,
            )

            is_intersecting = fun.isIntersect(baseBox, addBox)
            is_inside = fun.isInside(baseBox, addBox)

            if is_intersecting and not is_inside:
                fun.calBool(baseBox, addBox, "add")
                break
            else:
                fun.delobj(addBox)

                if attempt == props.max_attempts - 1:
                    self.report({"WARNING"}, f"无法在{props.max_attempts}次尝试内生成")
                    return {"CANCELLED"}

        return {"FINISHED"}
    
class Extract(bpy.types.Operator):
    """基形规则：Extract"""

    bl_idname = "ronge_adt.extract"
    bl_label = "Extract"

    def execute(self, context):
        props = context.scene.adt_props

        baseBox = None
        if fun.isExists("BaseBox"):
            baseBox = bpy.data.objects["BaseBox"]
        else:
            baseBox = fun.randomCube(props.min_size, props.max_size, props.max_area)
            baseBox.name = "BaseBox"

        for attempt in range(props.max_attempts):
            addBox = fun.randomCube(
                props.min_size * props.add_box_size,
                props.max_size * props.add_box_size,
                props.max_area,
            )

            is_intersecting = fun.isIntersect(baseBox, addBox)
            is_inside = fun.isInside(baseBox, addBox)

            if is_intersecting and not is_inside:
                fun.snapEdge(baseBox, addBox, fun.randomDir())
                Basebox1 = fun.copyobj(baseBox)
                addbox1 = fun.copyobj(addBox)
                
                addedbox = fun.calBool(baseBox, addBox, "add")
                
                subbox = fun.calBool(Basebox1, addbox1, "mul")
                shell = fun.copyobj(subbox) 
                shell = fun.offsetShell(shell, 0.0001, 0.0001, 0.0001) 
                fixedsubbox = fun.calBool(subbox, shell, "add")
                
                box = fun.calBool(addedbox, fixedsubbox, "sub")
                fun.optimizeMesh(box)
                break
            else:
                fun.delobj(addBox)

                if attempt == props.max_attempts - 1:
                    self.report({"WARNING"}, f"无法在{props.max_attempts}次尝试内生成")
                    return {"CANCELLED"}

        return {"FINISHED"}


# class Nest(bpy.types.Operator):
#     """剔除规则：Nest"""

#     bl_idname = "ronge_adt.nest"
#     bl_label = "Nest"

#     def execute(self, context):
#         props = context.scene.adt_props

#         baseBox = None
#         if fun.isExists("BaseBox"):
#             baseBox = bpy.data.objects["BaseBox"]
#         else:
#             baseBox = fun.randomCube(props.min_size, props.max_size, props.max_area)
#             baseBox.name = "BaseBox"

#         addBox = None
#         for attempt in range(props.max_attempts):
#             addBox = fun.randomCube(
#                 props.min_size * props.add_box_size,
#                 props.max_size * props.add_box_size,
#                 props.max_area,
#             )

#             is_intersecting = fun.isIntersect(baseBox, addBox)
#             is_inside = fun.isInside(baseBox, addBox)

#             if not is_intersecting and is_inside:
#                 fun.snapEdge(baseBox, addBox, "-z")
#                 addBox.location.z = addBox.location.z - 0.01
#                 fun.calBool(baseBox, addBox, "sub")
#                 break
#             else:
#                 fun.delobj(addBox)

#                 if attempt == props.max_attempts - 1:
#                     self.report({"WARNING"}, f"无法在{props.max_attempts}次尝试内生成")
#                     return {"CANCELLED"}

#         return {"FINISHED"}


class Carve(bpy.types.Operator):
    """剔除规则：Carve"""

    bl_idname = "ronge_adt.carve"
    bl_label = "Carve"

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
            addBox = fun.randomCube(
                props.min_size * props.add_box_size,
                props.max_size * props.add_box_size,
                props.max_area,
            )

            is_intersecting = fun.isIntersect(baseBox, addBox)
            is_inside = fun.isInside(baseBox, addBox)

            if is_intersecting and not is_inside:
                fun.calBool(baseBox, addBox, "sub")
                break
            else:
                fun.delobj(addBox)

                if attempt == props.max_attempts - 1:
                    self.report({"WARNING"}, f"无法在{props.max_attempts}次尝试内生成")
                    return {"CANCELLED"}

        return {"FINISHED"}

class Offset(bpy.types.Operator):
    """形变规则：Offset"""

    bl_idname = "ronge_adt.offset"
    bl_label = "Offset"

    def execute(self, context):
        props = context.scene.adt_props

        baseBox = bpy.data.objects["BaseBox"]
        fun.setActive(baseBox)
        shell = fun.copyobj(baseBox)
        
        offset = fun.randomValue(0-props.offset_maxoffset,props.offset_maxoffset)
        fun.offsetShell(shell, props.offset_minthick, props.offset_maxthick, offset)
        
        if fun.randomBool():
            fun.calBool(baseBox, shell, "sub")
        else:
            fun.calBool(baseBox, shell, "add")


        return {"FINISHED"}

class Shift(bpy.types.Operator):
    """形变规则：Shift"""

    bl_idname = "ronge_adt.shift"
    bl_label = "Shift"

    def execute(self, context):
        props = context.scene.adt_props
        
        baseBox = bpy.data.objects["BaseBox"]
        pos = fun.randomInsidePoint(baseBox)
        up = fun.dir2Vec3(fun.randomDir())
        dir = fun.randomVector(up)
        tan = fun.cross(up, dir)
        
        cut1 = fun.crateBoxWithDir(pos, up, dir,props.shift_maxcutbox, props.shift_maxcutbox, props.shift_maxcutbox)
        cut2 = fun.crateBoxWithDir(pos, up, -dir, props.shift_maxcutbox, props.shift_maxcutbox, props.shift_maxcutbox)
        
        box1 = fun.copyobj(baseBox)
        box2 = fun.copyobj(baseBox)
        
        fun.calBool(box1, cut1, "sub")
        fun.calBool(box2, cut2, "sub")
        
        box1.location += tan*fun.randomValue(0,props.shift_maxoffset)
        box2.location -= tan*fun.randomValue(0,props.shift_maxoffset)
        
        box1.location += dir*0.00001
        box2.location -= dir*0.00001 
        
        fun.delobj(baseBox)
        
        box = fun.calBool(box1, box2, "add")
        box.name = "BaseBox"
        fun.optimizeMesh(box)
        
        # baseBox = bpy.data.objects["BaseBox"]
        # fun.setActive(baseBox)
        # shell = fun.copyobj(baseBox)
        
        # offset = fun.randomValue(0-props.offset_maxoffset,props.offset_maxoffset)
        # fun.offsetShell(shell, props.offset_minthick, props.offset_maxthick, offset)
        
        # if fun.randomBool():
        #     fun.calBool(baseBox, shell, "sub")
        # else:
        #     fun.calBool(baseBox, shell, "add")


        return {"FINISHED"}