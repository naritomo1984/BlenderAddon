This script will bake the lighting result as texture sequence.  
Tested with Blender2.8 or higher.  


Usage:  

1.Open this python file in script editor.  
2.Change input/output directory path.  
3.Create new material with "Diffuse BSDF shader" node.   
4.Set "imagetexture" node to "color input" of diffuse shader node.  
5.Set the first texture image of texture sequence at imagetexturenode.  
6.Select a mesh.  
7.Hit run button.  



Currently no UIs. While it's rendering Blender UI will be no renspoding.  
To update the progress, open the output folder and check if new files are created.  
