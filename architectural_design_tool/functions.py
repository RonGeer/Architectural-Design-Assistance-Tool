import bpy
import random
import bmesh
import math
from mathutils.bvhtree import BVHTree
from mathutils import Vector, Matrix

if 1:  # 基础函数

    def onePass(id1, id2, offset1, offset2, addname):
        obj = bpy.context.scene.objects["BaseBox"]
        id2 += 1

        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        bpy.context.collection.objects.link(new_obj)
        bpy.context.view_layer.objects.active = new_obj
        new_obj.location = Vector((offset1 * id1, offset2 * id2, 0))
        new_obj.name = str(id1) + addname

    def clean():
        """清理未使用的对象和数据块"""
        # 清理孤立的数据块
        for mesh in bpy.data.meshes:
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)

        for obj in bpy.data.objects:
            if obj.users == 0:
                bpy.data.objects.remove(obj)

        bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP", iterations=1)

    def setBoxPos(obj_id, spacing, is_3d=False):
        """
        螺旋式排列物体位置函数

        参数:
            obj_id: 物体的ID（从0开始）
            spacing: 分割距离（棋盘格单位大小）
            is_3d: 是否使用3D空间排列（默认为False，只在Z=0平面排列）

        返回:
            Vector: 物体应该在的位置（x, y, z）
        """
        if obj_id == 0:
            return Vector((0, 0, 0))  # 第一个物体放在原点

        # 计算物体所在的"层"（从原点开始的螺旋圈数）
        layer = 0
        total_positions = 1  # 原点已占用1个位置

        while True:
            layer += 1
            # 每层的物体数量：2D中是8*layer，3D中是24*layer²+2
            if is_3d:
                layer_positions = 24 * layer * layer + 2  # 立方体的表面积，减去已计算的
            else:
                layer_positions = 8 * layer  # 正方形周长

            if total_positions + layer_positions > obj_id:
                break
            total_positions += layer_positions

        # 计算物体在当前层中的位置（从0开始）
        pos_in_layer = obj_id - total_positions

        if is_3d:
            # 3D螺旋：在一个立方体表面螺旋前进
            # 立方体的尺寸
            cube_size = layer * 2

            # 计算每个面的位置数量
            face_positions = cube_size * cube_size  # 每个面的位置数量

            # 确定物体在哪个面
            if pos_in_layer < face_positions:
                # 底面 (z=-layer)
                x = (pos_in_layer % cube_size) - layer
                y = (pos_in_layer // cube_size) - layer
                z = -layer
            elif pos_in_layer < 2 * face_positions:
                # 前面 (y=layer)
                adjusted_pos = pos_in_layer - face_positions
                x = (adjusted_pos % cube_size) - layer
                z = (adjusted_pos // cube_size) - layer
                y = layer
            elif pos_in_layer < 3 * face_positions:
                # 顶面 (z=layer)
                adjusted_pos = pos_in_layer - 2 * face_positions
                x = layer - (adjusted_pos % cube_size)
                y = (adjusted_pos // cube_size) - layer
                z = layer
            elif pos_in_layer < 4 * face_positions:
                # 后面 (y=-layer)
                adjusted_pos = pos_in_layer - 3 * face_positions
                x = layer - (adjusted_pos % cube_size)
                z = (adjusted_pos // cube_size) - layer
                y = -layer
            elif pos_in_layer < 5 * face_positions:
                # 右面 (x=layer)
                adjusted_pos = pos_in_layer - 4 * face_positions
                y = layer - (adjusted_pos % cube_size)
                z = (adjusted_pos // cube_size) - layer
                x = layer
            else:
                # 左面 (x=-layer)
                adjusted_pos = pos_in_layer - 5 * face_positions
                y = (adjusted_pos % cube_size) - layer
                z = (adjusted_pos // cube_size) - layer
                x = -layer

            # 应用间距
            position = Vector((x * spacing, y * spacing, z * spacing))

        else:
            # 2D螺旋：在一个正方形上螺旋前进
            side_length = layer * 2

            # 计算每条边的位置数量
            edge_positions = side_length

            # 确定物体在哪条边
            if pos_in_layer < edge_positions:
                # 底边 (y=-layer)
                x = (pos_in_layer % edge_positions) - layer
                y = -layer
            elif pos_in_layer < 2 * edge_positions:
                # 右边 (x=layer)
                adjusted_pos = pos_in_layer - edge_positions
                x = layer
                y = (adjusted_pos % edge_positions) - layer
            elif pos_in_layer < 3 * edge_positions:
                # 顶边 (y=layer)
                adjusted_pos = pos_in_layer - 2 * edge_positions
                x = layer - (adjusted_pos % edge_positions)
                y = layer
            else:
                # 左边 (x=-layer)
                adjusted_pos = pos_in_layer - 3 * edge_positions
                x = -layer
                y = layer - (adjusted_pos % edge_positions)

            # 应用间距，2D情况下z=0
            position = Vector((x * spacing, y * spacing, 0))

        return position

    def shuffleList(list):
        random.shuffle(list)
        return list

    def randomInt(min=1, max=3):
        return random.randint(min, max)

    def cross(v1, v2):
        return Vector(
            (
                v1[1] * v2[2] - v1[2] * v2[1],
                v1[2] * v2[0] - v1[0] * v2[2],
                v1[0] * v2[1] - v1[1] * v2[0],
            )
        )

    def dir2Vec3(dir):
        if dir == "+x":
            return Vector((1, 0, 0))
        elif dir == "+y":
            return Vector((0, 1, 0))
        elif dir == "+z":
            return Vector((0, 0, 1))
        elif dir == "-x":
            return Vector((-1, 0, 0))
        elif dir == "-y":
            return Vector((0, -1, 0))
        elif dir == "-z":
            return Vector((0, 0, -1))
        else:
            return Vector((0, 0, 0))

    def randomValue(min=0, max=1):
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
        return obj

    def getBound(obj):
        """OutPut:+x,+y,+z,-x,-y,-z"""

        maxx = maxy = maxz = -float("inf")
        minx = miny = minz = float("inf")

        # 遍历顶点，计算边界框
        for v in obj.data.vertices:
            co = obj.matrix_world @ v.co

            # 更新边界值
            if co.x > maxx:
                maxx = co.x
            if co.x < minx:
                minx = co.x
            if co.y > maxy:
                maxy = co.y
            if co.y < miny:
                miny = co.y
            if co.z > maxz:
                maxz = co.z
            if co.z < minz:
                minz = co.z

        return maxx, maxy, maxz, minx, miny, minz

    def randomInsidePoint(obj):

        maxx, maxy, maxz, minx, miny, minz = getBound(obj)

        posx = randomValue(minx, maxx)
        posy = randomValue(miny, maxy)
        posz = randomValue(minz, maxz)

        return Vector((posx, posy, posz))

    def randomDir():
        return random.choice(["+x", "+y", "+z", "-x", "-y", "-z"])

    def randomVector(dir=Vector((0, 0, 0))):
        """dir为限定的垂直方向（Vector）"""

        rdir = Vector(
            (randomValue(-1, 1), randomValue(-1, 1), randomValue(-1, 1))
        ).normalized()

        if dir == Vector((0, 0, 0)):
            return rdir
        else:
            dir_component = rdir.dot(dir)
            caled_rdir = rdir - dir_component * dir
            return caled_rdir.normalized()

    def centerPos(obj):
        maxx, maxy, maxz, minx, miny, minz = getBound(obj)
        return Vector(((maxx + minx) / 2, (maxy + miny) / 2, (maxz + minz) / 2))


if 1:  # 生成函数

    def snapGround(obj):
        maxx, maxy, maxz, minx, miny, minz = getBound(obj)
        move_distance = -minz
        obj.location.z += move_distance
        return obj

    def addTwist(obj, dir, angle):
        """SimpleDeform"""
        mod = obj.modifiers.new(name="SimpleDeform", type="SIMPLE_DEFORM")

        if dir == "+x" or dir == "-x":
            mod.deform_axis = "X"
        elif dir == "+y" or dir == "-y":
            mod.deform_axis = "Y"
        elif dir == "+z" or dir == "-z":
            mod.deform_axis = "Z"

        mod.angle = angle

        applyMod(obj, "SimpleDeform")

        return obj

    def cutLineWithDir(obj, stringdir, interval=0.05):
        setActive(obj)
        obj.select_set(True)
        maxx, maxy, maxz, minx, miny, minz = getBound(obj)
        imin = 0
        imax = 0

        if stringdir == "+x" or stringdir == "-x":
            imin = minx
            imax = maxx
        if stringdir == "+y" or stringdir == "-y":
            imin = miny
            imax = maxy
        if stringdir == "+z" or stringdir == "-z":
            imin = minz
            imax = maxz

        maxstep = int((imax - imin) / interval)

        dir = dir2Vec3(stringdir)
        start = dir * (imin + interval)

        bpy.ops.object.mode_set(mode="EDIT")
        for i in range(maxstep):

            bpy.ops.mesh.select_all(action="SELECT")

            bpy.ops.mesh.bisect(
                plane_co=start + dir * i * interval,
                plane_no=dir,
                flip=False,
            )
        bpy.ops.object.mode_set(mode="OBJECT")

    def optimizeMesh(obj, merge_threshold=0.001):

        setActive(obj)

        bpy.ops.object.mode_set(mode="EDIT")
        bm = bmesh.from_edit_mesh(obj.data)

        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_threshold)

        bmesh.update_edit_mesh(obj.data)

        bpy.ops.object.mode_set(mode="OBJECT")

        return obj

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
        return baseobj

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

        return applyMod(baseobj, "Solidify")

    def crateBoxWithDir(point, updir, stretchdir, width, height, depth, isCenter=False):

        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align="WORLD")
        box = bpy.context.active_object

        if isCenter:
            box.scale = (width, depth * 2, height)

        else:
            origin_offset = Vector((0, -0.5, 0))

            for vertex in box.data.vertices:
                vertex.co -= origin_offset

            box.scale = (width, depth, height)

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        right_vec = updir.cross(stretchdir).normalized()
        rotation_matrix = Matrix(
            (
                (right_vec.x, stretchdir.x, updir.x, 0),
                (right_vec.y, stretchdir.y, updir.y, 0),
                (right_vec.z, stretchdir.z, updir.z, 0),
                (0, 0, 0, 1),
            )
        )

        box.rotation_euler = rotation_matrix.to_euler()
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        box.location = point

        return box


if 1:  # 逻辑函数

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

    def isPontinside(point, obj):

        maxx, maxy, maxz, minx, miny, minz = getBound(obj)

        if (
            point[0] > maxx
            or point[0] < minx
            or point[1] > maxy
            or point[1] < miny
            or point[2] > maxz
            or point[2] < minz
        ):
            return False
        return True
