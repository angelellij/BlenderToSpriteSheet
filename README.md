
This script converts animations in blender to spritesheets in one single run. Te objective was to be able to just download a mixamo animation and, withought changing anything outside the script be able to export a spritesheet. This should allow to 1) Save parameters like size, camera distance, light values on script meaning your spritesheets will be alike, 2) minimal changes are than only on the script everytime so to avoid work done on blender.

# Requirements

You need to have python with the PILLOW library installed.

# Inspirations 
This script was based mainly from CambiramMax's script: https://www.youtube.com/watch?v=16jF6ON1q5c&list=LL&index=4&t=15s and a little bit from FoozleCC
https://www.youtube.com/watch?v=l1Io7fLYV4o&list=LL&index=5&t=1s. However I added some improvements like moving the camera and lights automatically to allow to get non "Inplace" animations from Mixamo working. It also auto hides Armatures if more than one animation appears.

# Values you can and probably want to change:
```
#Base
directions = 8 #This is how many angles you want (probably 8 or 4)
size = 256 #This is the size in pixels of each sprite in my case is 256 by 256

#Camera
camera_position = (0, -28, 18) #x, y, z
camera_rotation = (65, 0, 0) #x, y, z
delete_extra_cameras = True #When importing Mixamo you get an extra camara for each imported animation. This automatically cleans the scene
track_bone = "mixamorig:Spine" #If the animation was not in-place, this allows to make spritesheet be done correctly. If inplace you can replace this with ""

#Light
light_data = [18000, 1, 0.1, 1] #power, diffuse, specular, volume
light_position = (0, -25, 18) #x, y, z
delete_extra_lights = True #When importing Mixamo you get an extra light for each imported animation. This automatically cleans the scene.

#File directory
path = "/home/javier/Documents/Blender/Spritesheets"

#Change Every Time
name = "tensu" #Folder Name
animations = [ #in the order of the fbx file names
    #[desired_animation_spritesheet_name, start_frame, end_frame, frames_step]
    #['attack', 0, 167, 4],
    #['idle', 0, 59, 4],
    ['roll', 0, 71, 4],
    #['run', 0, 21, 3],
    #['throw', 56, 124, 4],
]
```
