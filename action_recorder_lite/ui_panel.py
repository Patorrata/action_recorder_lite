import bpy # type: ignore

class VIEW3D_PT_action_recorder(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category   = "ActRec"
    bl_label      = "Action Recorder Lite"
    bl_options    = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, ctx):
        return ctx.mode.startswith('EDIT')   # sólo en Edit Mode

    def draw(self, ctx):
        lay = self.layout
        lay.operator("arl.start_record", icon='REC')
        lay.operator("arl.stop_record",  icon='PAUSE')
        lay.operator("arl.play_macro",   icon='PLAY')
        lay.separator()
        lay.label(text=f"Pasos grabados: {len(__import__('recorder')._RecorderState.buffer)}")

def register():
    bpy.utils.register_class(VIEW3D_PT_action_recorder)

def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_action_recorder)
