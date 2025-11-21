import bpy
import random
import bmesh
import math
from mathutils.bvhtree import BVHTree

if 1 == 1:  # 基础函数

    def randomValue(min, max):
        return random.uniform(min, max)
    
    def randomBool():
        return random.choice([True, False])
    
    def setActive(obj):
        bpy.context.view_layer.objects.active = obj
        
    def copyobj(obj):     
        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        bpy.context.collection.objects.link(new_obj)
        bpy.context.view_layer.objects.active = new_obj
        
        return new_obj
    
    def delobj(obj):
        bpy.data.objects.remove(obj)

    def applyMod(obj, name):
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=name)

    def getBound(obj):
        """OutPut:+x,+y,+z,-x,-y,-z"""
        verts = [obj.matrix_world @ v.co for v in obj.data.vertices]

        maxx, maxy, maxz, minx, miny, minz = (
            -math.inf,
            -math.inf,
            -math.inf,
            math.inf,
            math.inf,
            math.inf,
        )

        for co in verts:
            if co[0] > maxx:
                maxx = co[0]
            if co[0] < minx:
                minx = co[0]
            if co[1] > maxy:
                maxy = co[1]
            if co[1] < miny:
                miny = co[1]
            if co[2] > maxz:
                maxz = co[2]
            if co[2] < minz:
                minz = co[2]

        return maxx, maxy, maxz, minx, miny, minz


if 1 == 1:  # 生成函数

    def randomCube(min_size, max_size, max_area):
        lenghx = randomValue(min_size, max_size)
        lenghy = randomValue(min_size, max_size)
        lenghz = randomValue(min_size, max_size)
        posx = randomValue(0, max_area)
        posy = randomValue(0, max_area)
        posz = randomValue(0, max_area)
        bpy.ops.mesh.primitive_cube_add(
            size=1,
            enter_editmode=False,
            align="WORLD",
            location=(posx, posy, posz),
            scale=(lenghx, lenghy, lenghz),
        )
        cube = bpy.context.active_object
        return cube

    def calBool(baseobj, boolobj, type):
        """Boolean type(string):add,sub,mul"""

        mod = baseobj.modifiers.new(name="Boolean", type="BOOLEAN")

        t = "DIFFERENCE"
        if type == "add":
            t = "UNION"
        if type == "sub":
            t = "DIFFERENCE"
        if type == "mul":
            t = "INTERSECT"

        mod.operation = t
        mod.object = boolobj

        applyMod(baseobj, "Boolean")
        delobj(boolobj)

    def meshTowall(obj, inout="out", thick=0.1):
        """Solidify"""

        mod = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
        mod.thickness = thick

        if inout == "in":
            mod.offset = 1
        else:
            mod.offset = -1

        applyMod(obj, "Solidify")

    def snapEdge(baseobj, moveobj, edgeDir):
        """edgeDir(string):+x,+y,+z,-x,-y,-z"""
        # 获取两个物体的边界框
        base_maxx, base_maxy, base_maxz, base_minx, base_miny, base_minz = getBound(
            baseobj
        )
        move_maxx, move_maxy, move_maxz, move_minx, move_miny, move_minz = getBound(
            moveobj
        )

        # 获取当前moveobj的位置
        move_loc = moveobj.location.copy()

        # 根据边缘方向计算新的位置
        if edgeDir == "+x":  # 将moveobj的+x边缘吸附到baseobj的+x边缘
            new_x = base_maxx - (move_maxx - move_loc.x)
            moveobj.location.x = new_x

        elif edgeDir == "-x":  # 将moveobj的-x边缘吸附到baseobj的-x边缘
            new_x = base_minx + (move_loc.x - move_minx)
            moveobj.location.x = new_x

        elif edgeDir == "+y":  # 将moveobj的+y边缘吸附到baseobj的+y边缘
            new_y = base_maxy - (move_maxy - move_loc.y)
            moveobj.location.y = new_y

        elif edgeDir == "-y":  # 将moveobj的-y边缘吸附到baseobj的-y边缘
            new_y = base_miny + (move_loc.y - move_miny)
            moveobj.location.y = new_y

        elif edgeDir == "+z":  # 将moveobj的+z边缘吸附到baseobj的+z边缘
            new_z = base_maxz - (move_maxz - move_loc.z)
            moveobj.location.z = new_z

        elif edgeDir == "-z":  # 将moveobj的-z边缘吸附到baseobj的-z边缘
            new_z = base_minz + (move_loc.z - move_minz)
            moveobj.location.z = new_z

        else:
            print(f"无效的边缘方向: {edgeDir}，请使用: +x, +y, +z, -x, -y, -z")

    def offsetShell(baseobj, minthick, maxthick, maxoffset):  # 生成offset的外壳模型
        """Solidify"""
        mod = baseobj.modifiers.new(name="Solidify", type="SOLIDIFY")
        mod.solidify_mode = "NON_MANIFOLD"
        mod.nonmanifold_thickness_mode = "CONSTRAINTS"
        mod.thickness = randomValue(minthick, maxthick)
        mod.offset = randomValue(0, maxoffset)
        
        # applyMod(baseobj, "Solidify")


if 1 == 1:  # 逻辑函数

    def isExists(name):  # 判断是否存在
        for obj in bpy.data.objects:
            if obj.name == name:
                return True
        return False

    def isIntersect(boxA, boxB):  # 判断是否相交
        bm1 = bmesh.new()
        bm1.from_mesh(boxA.data)
        bm1.transform(boxA.matrix_world)

        bm2 = bmesh.new()
        bm2.from_mesh(boxB.data)
        bm2.transform(boxB.matrix_world)

        # 使用BVH树检测相交
        bvh1 = BVHTree.FromBMesh(bm1)
        bvh2 = BVHTree.FromBMesh(bm2)

        # 检测相交
        intersect = bvh1.overlap(bvh2)

        # 清理BMesh
        bm1.free()
        bm2.free()

        return bool(intersect)

    def isInside(boxA, boxB):  # 判断是否完全被包围
        """OutPut:isInside(bool),BiggerObj(string):boxA,boxB"""
        vola = boxA.dimensions[0] * boxA.dimensions[1] * boxA.dimensions[2]
        volb = boxB.dimensions[0] * boxB.dimensions[1] * boxB.dimensions[2]

        biggerobj = ""
        if vola > volb:
            outer_obj = boxA
            inner_obj = boxB
            biggerobj = "boxA"
        else:
            outer_obj = boxB
            inner_obj = boxA
            biggerobj = "boxB"

        inner_verts = [inner_obj.matrix_world @ v.co for v in inner_obj.data.vertices]

        maxx, maxy, maxz, minx, miny, minz = getBound(outer_obj)

        for co in inner_verts:
            if (
                co[0] > maxx
                or co[0] < minx
                or co[1] > maxy
                or co[1] < miny
                or co[2] > maxz
                or co[2] < minz
            ):
                return False
        return True, biggerobj
