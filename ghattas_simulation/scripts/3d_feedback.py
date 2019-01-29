import bpy
import time
import math
import pickle
import os

class sim(bpy.types.Operator):
    bl_idname = "wm.sim"
    bl_label = "Simulation Modal Operator"

    _timer = None
    # baisicly init
    def execute(self, context):
        # maximize to full screen 3D view window
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.screen.screen_full_area(override,use_hide_panels=True)
                    break
        self._fps = 60
        self._home=os.getenv("HOME")
        self._cam = bpy.data.objects['Camera']
        # setup initial location and rotation for camera
        self._cam.location = (0,0,1)
        self._cam.rotation_mode='XYZ'
        self._cam.rotation_euler = (math.radians(90.0),0.0,0.0)
        # setup timer event to update & redraw window at required fps
        wm = context.window_manager
        self._timer = wm.event_timer_add(1/self._fps, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}


    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':
            self.update()

        return {'PASS_THROUGH'}

    def update(self):
        with open(self._home + '/ghattas/src/ghattas_simulation/scripts/current.pkl', 'rb') as pickle_file:
            try:
                current=pickle.load(pickle_file)
                self._cam.rotation_euler.z = math.radians(current['heading'])
                self._cam.location = (current['x'],current['y'],current['z'])
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            except:
                pass

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

bpy.utils.register_class(sim)

bpy.ops.wm.sim()
