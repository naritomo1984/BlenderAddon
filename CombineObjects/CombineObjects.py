##Addon info
bl_info = {
    "name": "Combine object",
    "author": "Tomo Michigami",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object",
    "description": "Combines objects and textures",
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
)
import numpy as np
from mathutils import Vector


##define class
class OBJECT_OT_combineobject(Operator):
    bl_label = "Combine object"
    bl_idname = "object.combineobject"
    bl_description = "Combines objects and textures"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    newobjectname: bpy.props.StringProperty(
        name = "new object name",
        default = "Merged",
        description = "New object name"      
    )
    
    resolution: bpy.props.IntProperty(
        name = "resolution",
        default = 2048,
        min = 512,
        max = 4096,
        description = "Result texture size"      
    )
    
    ##define the dialog function
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)



    #create the list of textures
    def getTextures(self,objs):
        channelList = ['Base Color', 'Metallic', 'Roughness']
        texlist = {}
        
        for obj in objs:
            mat = obj.material_slots[0].material
            nodes = mat.node_tree.nodes
            for n in nodes:
                #for Normal map
                if n.type == 'NORMAL_MAP':
                    #Try to see the node has the texture
                    try:
                        if len(n.inputs[1].links) > 0:
                            link = n.inputs[1].links[0]
                            texture = link.from_node.image
                            type = 'Normal'
                            if type not in texlist.keys():
                                texlist[type] = [texture]
                            else:
                                texlist[type].append(texture)
                    #If node does not have any extures.
                    except:
                        print("Check the material to see if there is a texture")
                        
                #For BaseColor, Metallic, Roughness,
                if n.type == 'BSDF_PRINCIPLED':
                    #Loop for other channel(Basecolor, Metallic, Roughness)
                    for ch in channelList:
                        #Try to see the node has the texture
                        try:
                            if len(n.inputs[ch].links) > 0:
                                link = n.inputs[ch].links[0]
                                texture = link.from_node.image
                                type = ch
                                if type not in texlist.keys():
                                    texlist[type] = [texture]
                                else:
                                    texlist[type].append(texture)
                        ##If node does not have any extures.
                        except:
                            print("Check the material to see if there is a texture")
        
        return texlist
                        
    #Merge textures
    def mergeTextures(self, texlist, targetsize, newobjectname):
        newtexlist = {} 
        
        
        ####Get original texture size
        ###Try to see if the texture size is equal
            ### do process
        ###except 
            ### warning(Check texture size
        
        
        for key in texlist:
            imagename = newobjectname + "_" + str(key)
            texs = texlist[str(key)]
            
            texsize = texs[0].size[0]
            arraytexsize = texsize*4
            targettexsize = texsize * 2
            
            img1 = bpy.data.images[texs[0].name]
            img2 = bpy.data.images[texs[1].name]
            img3 = bpy.data.images[texs[2].name]
            img4 = bpy.data.images[texs[3].name]

            np_array1 = np.array(img1.pixels).reshape((texsize,arraytexsize))
            np_array2 = np.array(img2.pixels).reshape((texsize,arraytexsize))
            np_array3 = np.array(img3.pixels).reshape((texsize,arraytexsize))
            np_array4 = np.array(img4.pixels).reshape((texsize,arraytexsize))
            
            bg = bpy.data.images.new(name= imagename, width=targettexsize, height=targettexsize, alpha=True)

            hstack1 = np.hstack((np_array4, np_array3))
            hstack2 = np.hstack((np_array1, np_array2))
            result = np.vstack((hstack1, hstack2))

            bg.pixels = result.ravel()
            bg.scale(targetsize, targetsize)
            filepath = "//"+ imagename + ".png"
            bg.filepath_raw = filepath
            bg.file_format = 'PNG'
            bg.save()
            newtexlist[str(key)] = filepath
        return newtexlist

    #Get UV infomation
    def getObjectAndUVMap(self, objname):
        try:
            obj = bpy.data.objects[objname]
            if obj.type == 'MESH':
                uvMap = obj.data.uv_layers['UVMap']
                return obj, uvMap
        except:
            return None, None
    #Calculate uv scale
    def Scale2D(self, v, s, p):
        return(p[0] + s[0]*(v[0] - p[0]), p[1] + s[1]*(v[1] - p[1]) )

    #Resize and align UVs
    def ScaleUV(self, uvMap, scale, pivot):
        for uvIndex in range(len(uvMap.data)):
            uvMap.data[uvIndex].uv = self.Scale2D(uvMap.data[uvIndex].uv, scale, pivot)
            
    #Merge objects
    def mergeObjects(self, objs, newobjectname):    
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        objlist = {}
        pivotlist = [Vector( (0.0, 1.0) ), Vector( (1.0, 1.0) ), Vector( (1.0, 0.0) ), Vector( (0.0, 0.0) )]
        scale = Vector((0.5, 0.5))

        for i in range(len(objs)):
            objlist[objs[i].name] = i
            obj, uvMap = self.getObjectAndUVMap(objs[i].name)
            self.ScaleUV(uvMap, scale, pivotlist[i])


        for key in objlist:
            bpy.data.objects[key].select_set(True)

        bpy.ops.object.join()
        mergedobj = bpy.context.selected_objects[0]
        mergedobj.name = newobjectname
        return mergedobj


    #Set up new material with new textures and assign to new object
    def assignTextures(self, obj, texlist, newobjectname):
        mat = bpy.data.materials.new(name = newobjectname)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes['Principled BSDF']

        for tex in texlist:
            if tex == "Normal":
                inputname = tex
                normalmapNode = mat.node_tree.nodes.new('ShaderNodeNormalMap')
                mat.node_tree.links.new(bsdf.inputs[inputname], normalmapNode.outputs['Normal'])
                teximage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                teximage.image = bpy.data.images.load(texlist[tex])
                teximage.image.colorspace_settings.name = 'Linear'
                mat.node_tree.links.new(normalmapNode.inputs['Color'], teximage.outputs['Color'])

            else:
                inputname = tex
                teximage = mat.node_tree.nodes.new('ShaderNodeTexImage')
                teximage.image = bpy.data.images.load(texlist[tex])
                if tex != "Base Color":
                    teximage.image.colorspace_settings.name = 'Linear'
                mat.node_tree.links.new(bsdf.inputs[inputname], teximage.outputs['Color'])
            
        obj.data.materials.append(mat)
        
        
        

    ##Main function
    def execute(self, context):
        targetsize = self.resolution
        newobjectname = self.newobjectname      
        
        objs = bpy.context.selected_objects

        oldtexlist = self.getTextures(objs)

        newtexlist = self.mergeTextures(oldtexlist, targetsize, newobjectname)

        mergedobj = self.mergeObjects(objs, newobjectname)
        
        if len(mergedobj.data.materials) > 0:
            mergedobj.data.materials.clear()
        self.assignTextures(mergedobj, newtexlist, newobjectname)
        
        return {"FINISHED"}



    
##Addon registration
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_combineobject.bl_idname)
    

def register():
    bpy.utils.register_class(OBJECT_OT_combineobject)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_combineobject)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    

if __name__ == "__main__":
    register()