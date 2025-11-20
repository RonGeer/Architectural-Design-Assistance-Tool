import bpy
import functions as fun

class ADT1(bpy.types.Operator):
    """第一组类型"""

    bl_idname = "ronge_adt.adt1"
    bl_label = "ADT1"

    def execute(self, context):
        fun.calBool()
        return {"FINISHED"}
