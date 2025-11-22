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
                fun.setActive(baseBox)
                bpy.ops.object.transform_apply(
                    location=False, rotation=True, scale=False
                )
                break
            else:
                fun.delobj(addBox)

                if attempt == props.max_attempts - 1:
                    self.report({"WARNING"}, f"无法在{props.max_attempts}次尝试内生成")
                    return {"CANCELLED"}

        return {"FINISHED"}


class Branch(bpy.types.Operator):
    """基形规则：Branch"""

    bl_idname = "ronge_adt.branch"
    bl_label = "Branch"

    def execute(self, context):
        props = context.scene.adt_props

        updir = fun.dir2Vec3(fun.randomDir())
        updir1 = fun.dir2Vec3(fun.randomDir())
        dir1 = fun.randomVector(updir)
        dir2 = fun.randomVector(updir)
        dir3 = fun.randomVector(updir1)

        h = fun.randomValue(
            props.min_size * props.add_box_size, props.max_size * props.add_box_size
        )
        w1 = fun.randomValue(
            props.min_size * props.add_box_size, props.max_size * props.add_box_size
        )
        w2 = fun.randomValue(
            props.min_size * props.add_box_size, props.max_size * props.add_box_size
        )
        w3 = fun.randomValue(
            props.min_size * props.add_box_size, props.max_size * props.add_box_size
        )
        d1 = fun.randomValue(props.min_size, props.max_size)
        d2 = fun.randomValue(props.min_size, props.max_size)
        d3 = fun.randomValue(props.min_size, props.max_size)

        box1 = fun.crateBoxWithDir(fun.dir2Vec3(0), updir, dir1, w1, h, d1)
        box2 = fun.crateBoxWithDir(
            fun.dir2Vec3(0) + updir * 0.00001, updir, dir2, w2, h, d2
        )
        box3 = fun.crateBoxWithDir(
            fun.dir2Vec3(0) + updir1 * 0.00002, updir1, dir3, w3, h, d3
        )

        fun.calBool(box1, box2, "add")
        fun.calBool(box1, box3, "add")

        fun.optimizeMesh(box1)
        box1.name = "BaseBox"

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

                fun.setActive(box)
                bpy.ops.object.transform_apply(
                    location=False, rotation=True, scale=False
                )
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

        offset = fun.randomValue(0 - props.offset_maxoffset, props.offset_maxoffset)
        fun.offsetShell(shell, props.offset_minthick, props.offset_maxthick, offset)

        if fun.randomBool():
            fun.calBool(baseBox, shell, "sub")
        else:
            fun.calBool(baseBox, shell, "add")

        return {"FINISHED"}


class Twist(bpy.types.Operator):
    """形变规则：Twist"""

    bl_idname = "ronge_adt.twist"
    bl_label = "Twist"

    def execute(self, context):
        props = context.scene.adt_props

        baseBox = bpy.data.objects["BaseBox"]
        dir = fun.randomDir()

        fun.cutLineWithDir(baseBox, dir)
        fun.addTwist(baseBox, dir, fun.randomValue(0, props.twist_maxangle))

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

        cut1 = fun.crateBoxWithDir(
            pos,
            up,
            dir,
            props.shift_maxcutbox,
            props.shift_maxcutbox,
            props.shift_maxcutbox,
        )
        cut2 = fun.crateBoxWithDir(
            pos,
            up,
            -dir,
            props.shift_maxcutbox,
            props.shift_maxcutbox,
            props.shift_maxcutbox,
        )

        box1 = fun.copyobj(baseBox)
        box2 = fun.copyobj(baseBox)

        fun.calBool(box1, cut1, "sub")
        fun.calBool(box2, cut2, "sub")

        box1.location += tan * fun.randomValue(0, props.shift_maxoffset)
        box2.location -= tan * fun.randomValue(0, props.shift_maxoffset)

        box1.location += dir * 0.00001
        box2.location -= dir * 0.00001

        fun.delobj(baseBox)

        box = fun.calBool(box1, box2, "add")
        box.name = "BaseBox"
        fun.optimizeMesh(box)

        return {"FINISHED"}


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


class Frature(bpy.types.Operator):
    """剔除规则：Frature"""

    bl_idname = "ronge_adt.frature"
    bl_label = "Frature"

    def execute(self, context):
        props = context.scene.adt_props

        baseBox = bpy.data.objects["BaseBox"]
        updir = fun.dir2Vec3(fun.randomDir())
        width = fun.randomValue(props.frature_minwidth, props.frature_maxwidth)

        pos = fun.randomInsidePoint(baseBox)
        dir1 = fun.randomVector(updir)
        dir2 = fun.randomVector(updir)

        whole_wall1 = fun.crateBoxWithDir(
            pos + updir * 0.001, updir, dir1, width, 100, 100, True
        )
        half_wall1 = fun.crateBoxWithDir(
            pos + updir * 0.001, updir, dir1, width, 100, 100, False
        )
        whole_wall2 = fun.crateBoxWithDir(
            pos + updir * 0.001, updir, dir2, width, 100, 100, True
        )
        half_wall2 = fun.crateBoxWithDir(
            pos + updir * 0.001, updir, dir2, width, 100, 100, False
        )

        corner = fun.calBool(whole_wall1, whole_wall2, "mul")
        shell = fun.copyobj(corner)
        shell = fun.offsetShell(shell, 0.0001, 0.0001, 0.0001)
        fixedcorner = fun.calBool(corner, shell, "add")

        shell = fun.copyobj(half_wall1)
        shell = fun.offsetShell(shell, 0.0001, 0.0001, 0.0001)
        fixedhalf_wall1 = fun.calBool(half_wall1, shell, "add")
        
        shell = fun.copyobj(half_wall2)
        shell = fun.offsetShell(shell, 0.0001, 0.0001, 0.0001)
        fixedhalf_pwall2 = fun.calBool(half_wall2, shell, "add")
        
        wall = fun.calBool(fixedhalf_wall1, fixedhalf_pwall2, "add")
        wall = fun.calBool(wall, fixedcorner, "add")
        
        fun.calBool(baseBox, wall, "sub")

        return {"FINISHED"}

class Expland(bpy.types.Operator):
    """剔除规则：Expland"""
    
    bl_idname = "ronge_adt.expland"
    bl_label = "Expland"
    
    def execute(self, context):
        props = context.scene.adt_props
        
        baseBox = bpy.data.objects["BaseBox"]
        center = fun.centerPos(baseBox)
        shifted_center = center + fun.randomVector()*fun.randomValue(props.expland_minoffset, props.expland_maxoffset)
        
        pos = fun.randomInsidePoint(baseBox)
        dir = shifted_center - pos
        cutvolume = fun.crateBoxWithDir(pos, fun.randomVector(dir), dir,1000,1000,1000)
        
        fun.calBool(baseBox, cutvolume, "sub")
        
        return {"FINISHED"}