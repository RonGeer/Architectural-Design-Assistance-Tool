import bpy

def delobj(obj):
    bpy.data.objects.remove(obj)

def applyMod(obj,name):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=name)

def calBool(baseobj,boolobj,type):
    """Boolean type:add,sub,mul"""
    
    mod = baseobj.modifiers.new(name="Boolean", type='BOOLEAN')
      
    t = 'DIFFERENCE' 
    if type == 'add':
        t = 'UNION'
    if type == 'sub':
        t == 'DIFFERENCE' 
    if type == 'mul':
        t = 'INTERSECT'
        
    mod.operation = t
    mod.object = boolobj
    
    applyMod(baseobj,"Boolean")
    delobj(boolobj)

def meshTowall(obj,inout = "out",thick = 0.1):
    """Solidify"""
    
    mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod.thickness = thick
    
    if inout == "in":
        mod.offset = 1
    else:
        mod.offset = -1
        
    applyMod(obj,"Solidify")