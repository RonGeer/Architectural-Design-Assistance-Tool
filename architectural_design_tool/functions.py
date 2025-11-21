import bpy
import random
import bmesh
from mathutils.bvhtree import BVHTree

if 1 == 1:  # 基础函数

    def delobj(obj):
        bpy.data.objects.remove(obj)

    def applyMod(obj, name):
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=name)


if 1 == 1:  # 生成函数

    def randomCube(min_size, max_size, max_area):
        lenghx = random.uniform(min_size, max_size)
        lenghy = random.uniform(min_size, max_size)
        lenghz = random.uniform(min_size, max_size)
        posx = random.uniform(0, max_area)
        posy = random.uniform(0, max_area)
        posz = random.uniform(0, max_area)
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
        """Boolean type:add,sub,mul"""

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


if 1 == 1:  # 逻辑函数

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

        vola = boxA.dimensions[0] * boxA.dimensions[1] * boxA.dimensions[2]
        volb = boxB.dimensions[0] * boxB.dimensions[1] * boxB.dimensions[2]

        if vola > volb:
            outer_obj = boxA
            inner_obj = boxB
        else:
            outer_obj = boxB
            inner_obj = boxA

        inner_verts = [inner_obj.matrix_world @ v.co for v in inner_obj.data.vertices]
        outer_verts = [outer_obj.matrix_world @ v.co for v in outer_obj.data.vertices]
        
        maxx,maxy,maxz,minx,miny,minz = -9999,-9999,-9999,9999,9999,9999
        
        for co in outer_verts:
            if co[0]>maxx:
                maxx = co[0]
            if co[0]<minx:
                minx = co[0]
            if co[1]>maxy:
                maxy = co[1]
            if co[1]<miny:
                miny = co[1]
            if co[2]>maxz:
                maxz = co[2]
            if co[2]<minz:
                minz = co[2]
        
        for co in inner_verts:
            if co[0]>maxx or co[0]<minx or co[1]>maxy or co[1]<miny or co[2]>maxz or co[2]<minz:
                return False
        return True
                
