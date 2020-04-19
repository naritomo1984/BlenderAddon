##Addon info
bl_info = {
    "name": "Gridcubes",
    "author": "Tomo Michigami",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "description": "Make grid of cubes",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}



##import modules
import bpy
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)
from bpy.props import (
    IntProperty, 
    FloatProperty,
)

##define class
class OBJECT_OT_gridcubes(Operator):
    bl_label = "GridCubes"
    bl_idname = "object.gridcubes"
    bl_description = "Create grid of cubes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    ##declare the custom properties
    cubeSize: bpy.props.FloatProperty(
        name = "Cube Size",
        default = 2.5,
        min = 1.0,
        max = 10.0,
        description = "The size of cube"
    )
    
    cubeXNum: bpy.props.IntProperty(
        name = "Xrow Number",
        default = 5,
        min = 2,
        max = 10,
        description = "The number of cubes in X row"      
    )
    cubeYNum: bpy.props.IntProperty(
        name = "Yrow Number",
        default = 5,
        min = 2,
        max = 10,
        description = "The number of cubes in Y row"
    )
    
    ##define the dialog function
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    ##defin main function
    def execute(self, context):
        csize = self.cubeSize
        xrow = self.cubeXNum
        yrow = self.cubeYNum
        cubes = []
    
    ##Make cubes
        for y in range(yrow):
            for x in range(xrow):
                bpy.ops.mesh.primitive_cube_add(size=csize, location = (csize * x, csize * y, csize/2.0))
                cube = bpy.context.view_layer.objects.active 
                cubes.append(cube)         

    #Make root object at the center
        rootXpos = ((csize/2.0) * xrow) - csize/2.0
        rootYpos = ((csize/2.0) * yrow) - csize/2.0
        
        bpy.ops.object.empty_add(type="PLAIN_AXES", location=(rootXpos,rootYpos,0))
        rootObj = bpy.context.view_layer.objects.active
        rootObj.name = "root"
        
    #Pareting cubes to the root object
        for cube in cubes:
            ob = bpy.context.scene.objects[str(cube.name)]
            ob.parent = rootObj
            if rootObj:
                ob.matrix_parent_inverse = rootObj.matrix_world.inverted()
        
    #Reset root position to 0 point
        rootObj.location = (0,0,0)
        return {"FINISHED"}
    
##registration
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_gridcubes.bl_idname)
    

def register():
    bpy.utils.register_class(OBJECT_OT_gridcubes)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_gridcubes)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    

if __name__ == "__main__":
    register()