bl_info = {
    "name": "ObjectPlacer",
    "author": "Tomo Michigami",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "description": "Creare and propagate object in a space based on proxy cube",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}


import bpy
import math
import random

from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)

class OBJECT_OT_objectplacer(Operator):
    bl_label = "ObjectPlacer"
    bl_idname = "object.objectplacer"
    bl_description = "Creare and propagate object in a space based on proxy cube"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', "UNDO"}
                ##calculate distance
    def distance(self, x1, y1, z1, x2, y2, z2):
        distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2) * 1.0)
        return distance

    ##get the length of each axis of bound
    def getLength(self, bound):
        xlength = self.distance(bound[0][0], bound[0][1], bound[0][2], bound[4][0], bound[4][1], bound[4][2])
        ylength = self.distance(bound[0][0], bound[0][1], bound[0][2], bound[3][0], bound[3][1], bound[3][1])
        zlength = self.distance(bound[0][0], bound[0][1], bound[0][2], bound[1][0], bound[1][1], bound[1][2])
        return (xlength, ylength, zlength)
    
    
    ##-------------MainFunction------------
    def main(self, obj):        
        obj = bpy.context.selected_objects[0]
        obj = bpy.data.objects[obj.name]
        bpy.context.object.hide_viewport = True
        rotation = 0.0
        bound = obj.bound_box
        num = 20
        totallength = 0.0

        ##Get origin
        xlength = bound[0][0]
        ylength = bound[0][1] + self.distance(bound[0][0], bound[0][1], bound[0][2], bound[3][0], bound[3][1], bound[3][2]) / 2.0
        origin = (xlength, ylength, bound[0][2])


        boundlength = self.getLength(bound)[0]

        while totallength <= boundlength:
            
            bpy.ops.mesh.primitive_cube_add(size = 1)
            height = random.uniform(4.0, 6.0)
            width  = random.uniform(0.6, 1.2)
            
            bpy.ops.transform.resize(value = (width, 3, height))
            bpy.ops.object.transform_apply(location = True, rotation = True, scale = True)
            newobj = bpy.context.selected_objects[0]
            newobj = bpy.data.objects[newobj.name]
            newbound = newobj.bound_box
            xpos = xlength + totallength + self.getLength(newbound)[0] -  (self.getLength(newbound)[0]/2.0)
            zpos = self.getLength(newbound)[2]/2.0

            ##Move the object to 0 pivot point.
            bpy.ops.transform.translate(value = (0, 0, zpos))
            bpy.ops.object.transform_apply(location = True, rotation = True, scale = True)
            
            ##Rotate the object
            if rotation == 0.0:
                rotation = random.uniform(-15.0, 0.0)
            else:
                rotation = 0.0
            bpy.ops.transform.rotate(value = math.radians(rotation), orient_axis ='Y')
            bpy.ops.object.transform_apply(location = True, rotation = True, scale = True)


            ##Move object towards X axis
            bpy.ops.transform.translate(value = (xpos, ylength, origin[2]))
            bpy.ops.object.transform_apply(location = True, rotation = True, scale = True)

            obj = bpy.context.selected_objects[0]
            obj = bpy.data.objects[newobj.name]
            bound = newobj.bound_box
            totallength += self.getLength(bound)[0]

    def execute(self, context):        
        obj = bpy.context.selected_objects[0]
        self.main(obj)
        return{"FINISHED"}
    

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_objectplacer.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_objectplacer)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_objectplacer)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
        
