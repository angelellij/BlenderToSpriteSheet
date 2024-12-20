import os
import bpy
from math import radians, floor
from mathutils import Vector
from PIL import Image

#Base
directions = 8
size = 256

#Camera
camera_position = (0, -28, 18) #x, y, z
camera_rotation = (65, 0, 0) #x, y, z
delete_extra_cameras = True
track_bone = "mixamorig:Spine"

#Light
light_data = [18000, 1, 0.1, 1] #power, diffuse, specular, volume
light_position = (0, -25, 18) #x, y, z
delete_extra_lights = True

#File directory
path = "/home/javier/Documents/Blender/Spritesheets"

#Change Every Time
name = "tensu" #File Name
animations = [ #in the order of the fbx file names
    #[desired_animation_spritesheet_name, start_frame, end_frame, frames_step]
    #['attack', 0, 167, 4],
    #['idle', 0, 59, 4],
    ['roll', 0, 71, 4],
    #['run', 0, 21, 3],
    #['throw', 56, 124, 4],
]

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                with bpy.context.temp_override(window =window, screen=screen,area=area):
                    bpy.ops.console.scrollback_append(text=str(data), type="OUTPUT")     

def get_armature(index:int):
    if index == 0: return bpy.data.objects.get("Armature")
    n = str(index)
    while len(n) < 3:
        n = f"0{n}"
    return bpy.data.objects.get(f"Armature.{n}")
                  
def hide_armature(armature, hide:bool = True) -> None:
    for child in armature.children:
        child.hide_render = hide

#Delete extra lights and cameras
for key in bpy.data.objects.keys():
    if "Light." in key and delete_extra_lights: 
        obj = bpy.data.objects.get(key)
        if obj.type != "LIGHT": continue
        bpy.data.objects.remove(obj)
    elif "Camera." in key and delete_extra_cameras: 
        obj = bpy.data.objects.get(key)
        if obj.type != "CAMERA": continue
        bpy.data.objects.remove(obj)

scene = bpy.data.scenes['Scene']
scene.render.film_transparent = True
scene.render.resolution_x = size
scene.render.resolution_y = size

camera = bpy.data.objects['Camera']
camera_position = Vector(camera_position)
camera_position = camera_position
camera.location = camera_position

camera.rotation_euler.x = radians(camera_rotation[0])
camera.rotation_euler.y = radians(camera_rotation[1])
camera.rotation_euler.z = radians(camera_rotation[2])

light = bpy.data.objects['Light']
light_position = Vector(light_position)
light.location = light_position

light.data.energy = light_data[0]
light.data.diffuse_factor = light_data[1]
light.data.specular_factor = light_data[2]
light.data.volume_factor = light_data[3]

# Folder of animations
new_path = os.path.join(path, name)
if not os.path.exists(new_path): os.makedirs(new_path)  # Create the directory

# Prepare Armature and rotator

armature = bpy.data.objects.get("Armature")
rotator = bpy.data.objects.get("Circle")
if rotator == None:
    bpy.ops.mesh.primitive_circle_add(radius=4, location=(0, 0, 0))
    rotator = bpy.data.objects.get("Circle")

for anim_i in range(len(animations)):
    armature = get_armature(anim_i)
    if armature == None: continue
    hide_armature(armature)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = rotator
    if armature.parent != rotator:  
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

#Start taking pictures
for anim_i in range(len(animations)):

    armature = get_armature(anim_i)
    hide_armature(armature, False)
    
    render_paths = []
    anim_name = animations[anim_i][0]
    start_frame = animations[anim_i][1]
    end_frame = animations[anim_i][2]
    anim_step = animations[anim_i][3]
    anim_length = floor((end_frame - start_frame) / anim_step)
    
    bone = None
    if track_bone != "" and type(track_bone) == str:
        bone = armature.pose.bones.get(track_bone)
    
    for i in range(directions):
        rotator.rotation_euler = (0,0, radians(-(360/directions) * i))
        file = os.path.join(new_path, f"{i}_")
        render_paths.append(file)
        
        for j in range(anim_length):
            bpy.context.scene.frame_current = start_frame + j * anim_step
            bpy.context.scene.render.filepath = file + str(j)
            
            if bone != None:
                print((armature.matrix_world @ bone.tail))
                camera.location.x = camera_position.x + (armature.matrix_world @ bone.tail).x
                camera.location.y = camera_position.y + (armature.matrix_world @ bone.tail).y
                light.location.x = light_position.x + (armature.matrix_world @ bone.tail).x
                light.location.y = light_position.y + (armature.matrix_world @ bone.tail).y
            bpy.ops.render.render(write_still=True)
            
    sheet = Image.new('RGBA', (size * anim_length, size*len(render_paths)))
    for i in range(len(render_paths)):
        for j in range(anim_length):
            image_path = f'{render_paths[i]}{str(j)}.png'
            image = Image.open(image_path)
            sheet.paste(image, (size*j, size*i))
            os.remove(image_path)
            
    sheet.save(f'{new_path}/{anim_name}.png')

    #Reset
    rotator.rotation_euler = (0,0,0)
    hide_armature(armature)

    print("--- SPRITESHEETS CREATED ---")
