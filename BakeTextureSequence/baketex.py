import bpy
from bpy.props import *


class BAKETEXSEQ_OT_BakeTexSeq(bpy.types.Operator):
  bl_idname = "baketexseq.bake"
  bl_label = "BakeTexSeq"
  bl_options = {'REGISTER', 'UNDO'}
  
  #--- properties ---#
  inputfolderpath: StringProperty(default = "C:\\This\\Is\\Input\\Folder\\Path", options = {'HIDDEN'})
  outputfolderpath: StringProperty(default = "C:\\This\\Is\\Output\\Folder\\Path", options = {'HIDDEN'})
  prefix: StringProperty(default = "image_", options = {'HIDDEN'})
  startframe: IntProperty(default = 1, options = {'HIDDEN'})
  endframe: IntProperty(default = 250, options = {'HIDDEN'})
  
  
  def baketexseq(self):
    objs = bpy.context.selected_objects
    if not len(objs) > 0:
        self.report({'INFO'}, "Please select mesh sequence")
    else:
        mat = objs[0].material_slots[0].material
        nodes = mat.node_tree.nodes
        link = nodes[0].inputs['Color'].links[0]


        for i in range(self.startframe, self.endframe+1):
            bpy.ops.object.bake(type='COMBINED', save_mode='INTERNAL') 
            texture = link.from_node.image
            framenum = i
            newfilename = self.prefix + "%05d" % framenum + ".png"
            texture.save_render(filepath = bpy.path.abspath(self.outputfolderpath) + newfilename)
            framenum = i+1
            if framenum == self.endframe + 1:
                print("Finished")
            else:
                bpy.context.scene.frame_set(framenum)
                filename = self.prefix + "%05d" % framenum + ".png"
                new_img = bpy.data.images.load(filepath = bpy.path.abspath(self.inputfolderpath) + filename)
                nodes[0].inputs['Color'].links[0].from_node.image = new_img
            
            

  #--- execute ---#
  def execute(self, context):
    self.baketexseq()
#    self.report({'INFO'}, self.inputfolderpath)
#    self.report({'INFO'}, self.outputfolderpath)
#    self.report({'INFO'}, str(self.startframe))
#    self.report({'INFO'}, str(self.endframe))

    return {'FINISHED'}


class BAKETXSEQ_PT_BakePanel(bpy.types.Panel):
  bl_space_type = 'VIEW_3D'
  bl_region_type = 'UI'
  bl_category = "BakeTexSeq"
  bl_label = "BakeTexSeq"

  #--- draw ---#
  def draw(self, context):
    layout = self.layout
    
    layout.prop(context.scene, "input_folder")
    layout.prop(context.scene, "output_folder")
    layout.prop(context.scene, "prefix")
    layout.prop(context.scene, "start_frame")
    layout.prop(context.scene, "end_frame")

    op_prop = layout.operator(BAKETEXSEQ_OT_BakeTexSeq.bl_idname, text = "Bake")
    op_prop.inputfolderpath = context.scene.input_folder
    op_prop.outputfolderpath = context.scene.output_folder
    op_prop.prefix = context.scene.prefix
    op_prop.startframe = context.scene.start_frame
    op_prop.endframe = context.scene.end_frame


classes = [
  BAKETXSEQ_PT_BakePanel,
  BAKETEXSEQ_OT_BakeTexSeq
]

#
# register
#
def register():
  for c in classes:
    bpy.utils.register_class(c)
    
  bpy.types.Scene.input_folder = StringProperty(default = "", subtype='DIR_PATH')
  bpy.types.Scene.output_folder = StringProperty(default = "", subtype='DIR_PATH')
  bpy.types.Scene.prefix = StringProperty(default = "Image_")
  bpy.types.Scene.start_frame = IntProperty(default = 1)
  bpy.types.Scene.end_frame = IntProperty(default = 250)
  

#
# unregister()
#    
def unregister():
  for c in classes:
    bpy.utils.register_class(c)
    
  del bpy.types.Scene.input_folder
  del bpy.types.Scene.output_folder

#
# script entry
#    
if __name__ == "__main__":
  register()