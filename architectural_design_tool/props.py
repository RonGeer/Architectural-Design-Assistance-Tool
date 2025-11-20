import bpy


class ADTProps(bpy.types.PropertyGroup):
    number: bpy.props.FloatProperty(
        name="Number", description="要打印的数字", default=42, min=0, max=1000
    ) # pyright: ignore[reportInvalidTypeForm]
