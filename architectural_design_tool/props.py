import bpy

class ADTProps(bpy.types.PropertyGroup):
    
    #全局变量
    max_attempts: bpy.props.IntProperty(
        name="Max Attempts", description="最大尝试次数", default=1000, min=1, max=100000
    ) # pyright: ignore[reportInvalidTypeForm]
    
    min_size: bpy.props.FloatProperty(
        name="Min Size", description="最小生成形体", default=0.5, min=0, max=1000
    ) # pyright: ignore[reportInvalidTypeForm]
    
    max_size: bpy.props.FloatProperty(
        name="Max Size", description="最大生成形体", default=1, min=0, max=1000
    ) # pyright: ignore[reportInvalidTypeForm]
    
    max_area: bpy.props.FloatProperty(
        name="Max Area", description="最大生成位置", default=1, min=0, max=1000
    ) # pyright: ignore[reportInvalidTypeForm]
    
    add_box_size: bpy.props.FloatProperty(
        name="Add Box Size", description="附加体比例", default=0.5, min=0, max=11
    ) # pyright: ignore[reportInvalidTypeForm]
    
    
    #offset变量
    offset_minthick: bpy.props.FloatProperty(
        name="Offset Minthick", description="最小厚度", default=0.05, min=0, max=10
    ) # pyright: ignore[reportInvalidTypeForm]
    
    offset_maxthick: bpy.props.FloatProperty(
        name="Offset Maxthick", description="最大厚度", default=0.1, min=0, max=10
    ) # pyright: ignore[reportInvalidTypeForm]
    
    offset_maxoffset: bpy.props.FloatProperty(
        name="Max Offset", description="最大偏移", default=1, min=0, max=1
    ) # pyright: ignore[reportInvalidTypeForm]
    
    
    #Shift变量
    shift_maxoffset: bpy.props.FloatProperty(
        name="Max Offset", description="最大剪切偏移", default=0.5, min=0, max=10
    ) # pyright: ignore[reportInvalidTypeForm]
    shift_maxcutbox: bpy.props.FloatProperty(
        name="Is Rotate", description="最大剪切体大小", default=1000, min=0, max=999999999
    ) # pyright: ignore[reportInvalidTypeForm]
    
    #Twist变量
    twist_maxangle: bpy.props.FloatProperty(
        name="Max Angle", description="最大旋转角度", default=1.5707963, min=0, max=6.2831852
    ) # pyright: ignore[reportInvalidTypeForm]
    twist_cutinterval: bpy.props.FloatProperty(
        name="Cut Interval", description="剪切间隔", default=0.05, min=0, max=1
    ) # pyright: ignore[reportInvalidTypeForm]
    
    #Frature变量
    frature_minwidth: bpy.props.FloatProperty(
        name="Min Width", description="最小厚度", default=0.05, min=0, max=100
    ) # pyright: ignore[reportInvalidTypeForm]
    frature_maxwidth: bpy.props.FloatProperty(
        name="Max Width", description="最大厚度", default=0.2, min=0, max=100
    ) # pyright: ignore[reportInvalidTypeForm]
    
    #Expland变量
    expland_maxoffset: bpy.props.FloatProperty(
        name="Max Offset", description="最大偏移", default=5, min=0, max=10
    ) # pyright: ignore[reportInvalidTypeForm]
    expland_minoffset: bpy.props.FloatProperty(
        name="Min Offset", description="最小偏移", default=1, min=0, max=10
    ) # pyright: ignore[reportInvalidTypeForm]
    