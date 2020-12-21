# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####




##This script will bake the lighting result as texture sequence.
##Tested with Blender2.8 or higher.


##Usage:
## 1.Open this python file in script editor.
## 2.Change input/output directory path.
## 3.Create new material with "Diffuse BSDF shader" node. 
## 4.Set "imagetexture" node to "color input" of diffuse shader node. 
## 5.Set the first texture image of texture sequence at imagetexturenode.
## 6.Select a mesh.
## 7.Hit run button.


##Currently no UIs. While it's rendering Blender UI will be no renspoding. 
##To update the progress, open the output folder and check if new files are created.



import bpy

##Change your directory path here(input = original textures, output = save folder for relighted textures)
inputdirectory = "C:\\This\\Is\\OriginalDirectory\\"
outputdirectory = "C:\\This\\Is\\OutputDirectory\\"
##Change sart and end frame.
startframe = 1
endframe = 300
##Change prefix.
prefix = "img"


objs = bpy.context.selected_objects
mat = objs[0].material_slots[0].material
nodes = mat.node_tree.nodes
link = nodes[1].inputs['Color'].links[0]


for i in range(startframe, endframe+1):
    bpy.ops.object.bake(type='COMBINED', save_mode='INTERNAL')
    
    texture = link.from_node.image
    
    framenum = i
    
    newfilename = prefix + "%05d" % framenum + ".png"
    
    texture.save_render(filepath = outputdirectory + newfilename)
    
    framenum = i+1
    
    bpy.context.scene.frame_set(framenum)
        
    filename = prefix + "%05d" % framenum + ".png"
        
    new_img = bpy.data.images.load(filepath = inputdirectory + filename)
        
    nodes[1].inputs['Color'].links[0].from_node.image = new_img
    
    if framenum == endframe:
        print("Finished")
