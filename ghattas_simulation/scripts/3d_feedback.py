import bpy
import time
import math
import pickle
import os

home=os.getenv("HOME")

def update(current):
    cam.rotation_euler.z = math.radians(current['heading'])
    cam.location = (current['x'],current['y'],current['z'])
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)


for window in bpy.context.window_manager.windows:
    screen = window.screen
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            override = {'window': window, 'screen': screen, 'area': area}
            bpy.ops.screen.screen_full_area(override)
            break


cam = bpy.data.objects['Camera']

cam.location = (0,0,1)

cam.rotation_mode='XYZ'
cam.rotation_euler = (math.radians(90.0),0.0,0.0)

i=0
while i<60*10:
    i+=1
    with open(home + '/ghattas/src/ghattas_simulation/scripts/current.pkl', 'rb') as pickle_file:
        current=pickle.load(pickle_file)
        print('unpickled')
        update(current)
    time.sleep(1/60)
