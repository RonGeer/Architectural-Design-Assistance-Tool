import bpy

class ADTProps(bpy.types.PropertyGroup):
    # number: bpy.props.FloatProperty(
    #     name="Number", description="数字", default=42, min=0, max=1000
    # ) # pyright: ignore[reportInvalidTypeForm]
    
    min_size: bpy.props.FloatProperty(
        name="Min Size", description="最小生成形体", default=0.5, min=0, max=1000
    ) # pyright: ignore[reportInvalidTypeForm]
    
    max_size: bpy.props.FloatProperty(
        name="Max Size", description="最大生成形体", default=1, min=0, max=1000
    ) # pyright: ignore[reportInvalidTypeForm]
    
    max_area: bpy.props.FloatProperty(
        name="Max Area", description="最大生成范围", default=1, min=0, max=1000
    ) # pyright: ignore[reportInvalidTypeForm]
    
    max_attempts: bpy.props.IntProperty(
        name="Max Attempts", description="最大尝试次数", default=200, min=1, max=1000
    ) # pyright: ignore[reportInvalidTypeForm]
    