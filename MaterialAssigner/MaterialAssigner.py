bl_info = {
    "name": "MaterialAssigner",
    "author": "Tomo Michigami",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "description": "Creare material for each object with shader nodes",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}


import bpy
from bpy.types import (
    AddonPreferences,
    Operator,
    Panel,
    PropertyGroup,
)

class OBJECT_OT_materialassigner(Operator):
    bl_label = "MaterialAssigner"
    bl_idname = "object.materialassigner"
    bl_description = "Create material for each object with shader nodes"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', "UNDO"}

    def main(self, obj):
        ##select object, and get object's name
        ##obj = bpy.context.view_layer.objects.active
        matname  = str(obj.name) + "_MAT"

        ##Create material, and get base nodes 
        bpy.data.materials.new(matname)
        mat = bpy.data.materials.get(matname)
        mat.use_nodes = True
        matout = mat.node_tree.nodes.get("Material Output")
        principled = mat.node_tree.nodes.get("Principled BSDF")

        ##Create other nodes
        baseColorTexture = mat.node_tree.nodes.new("ShaderNodeTexImage")
        metallicTexture = mat.node_tree.nodes.new("ShaderNodeTexImage") 
        roughnessTexture = mat.node_tree.nodes.new("ShaderNodeTexImage")
        normalTexture = mat.node_tree.nodes.new("ShaderNodeTexImage")
        heightTexture = mat.node_tree.nodes.new("ShaderNodeTexImage")
        bump = mat.node_tree.nodes.new("ShaderNodeBump")
        mapping = mat.node_tree.nodes.new("ShaderNodeMapping")
        texcoord = mat.node_tree.nodes.new("ShaderNodeTexCoord")


        ##Link each inputs and outputs
        mat.node_tree.links.new(texcoord.outputs['UV'], mapping.inputs['Vector'])
        mat.node_tree.links.new(mapping.outputs['Vector'], baseColorTexture.inputs['Vector'])
        mat.node_tree.links.new(mapping.outputs['Vector'], metallicTexture.inputs['Vector'])
        mat.node_tree.links.new(mapping.outputs['Vector'], roughnessTexture.inputs['Vector'])
        mat.node_tree.links.new(mapping.outputs['Vector'], normalTexture.inputs['Vector'])
        mat.node_tree.links.new(mapping.outputs['Vector'], heightTexture.inputs['Vector'])
        
        mat.node_tree.links.new(baseColorTexture.outputs['Color'], principled.inputs['Base Color'])
        mat.node_tree.links.new(metallicTexture.outputs['Color'], principled.inputs['Metallic'])
        mat.node_tree.links.new(roughnessTexture.outputs['Color'], principled.inputs['Roughness'])
        mat.node_tree.links.new(normalTexture.outputs['Color'], bump.inputs['Normal'])
        mat.node_tree.links.new(heightTexture.outputs['Color'], bump.inputs['Height'])
        mat.node_tree.links.new(bump.outputs['Normal'], principled.inputs['Normal'])


        mat.node_tree.links.new(principled.outputs['BSDF'], matout.inputs['Surface'])


        ##Assign material to object
        obj.data.materials.append(mat)



    def execute(self, context):
        
        ##Grab objects and execute main function for each object
        objs = bpy.context.selected_objects
        for obj in objs:
            self.main(obj)

        return{"FINISHED"}


def menu_func(self, context):
    self.layout.operator(OBJECT_OT_materialassigner.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_materialassigner)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_materialassigner)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

        
    

