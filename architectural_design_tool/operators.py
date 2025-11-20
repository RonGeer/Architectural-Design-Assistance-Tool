import bpy
from . import functions as fun

class Merge(bpy.types.Operator):
    """第一组类型"""

    bl_idname = "ronge_adt.merge"
    bl_label = "Merge"

    def execute(self, context):
        baseBox = fun.randomCube(1,2,1)
        addBox = fun.randomCube(0.5,1,1)
        print(fun.isIntersect(baseBox,addBox))
        print(fun.isInside(baseBox,addBox))
        # fun.calBool(baseBox,addBox,"add")
        return {"FINISHED"}
