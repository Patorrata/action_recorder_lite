import bpy, time # type: ignore

class _RecorderState:
    recording = False
    buffer = []          # lista de (idname, kwargs)
    _last_len = 0
    _timer = None

def _capture_ops(self, context):
    wm_ops = context.window_manager.operators
    cur_len = len(wm_ops)
    if cur_len != _RecorderState._last_len:
        new_ops = wm_ops[_RecorderState._last_len:]
        for op in new_ops:
            # sólo guardamos operadores con ejecución exitosa
            if op.bl_idname not in {'SCREEN_OT_animation_play', 'WM_OT_redraw_timer'}:
                _RecorderState.buffer.append(
                    (op.bl_idname, {p.identifier: getattr(op, p.identifier)
                                    for p in op.bl_rna.properties if p.is_runtime})
                )
        _RecorderState._last_len = cur_len
    return .1            # sigue llamándose cada 0.1 s

class ARL_OT_record(bpy.types.Operator):
    """Start recording operators"""
    bl_idname = "arl.start_record"
    bl_label  = "⏺ Record"

    def execute(self, ctx):
        if _RecorderState.recording:
            self.report({'INFO'}, "Ya grabando…")
            return {'CANCELLED'}
        _RecorderState.recording = True
        _RecorderState.buffer.clear()
        _RecorderState._last_len = len(ctx.window_manager.operators)
        _RecorderState._timer = ctx.window_manager.event_timer_add(0.1, window=ctx.window)
        ctx.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, ctx, _event):
        if not _RecorderState.recording:      # lo pararán desde otro operador
            ctx.window_manager.event_timer_remove(_RecorderState._timer)
            return {'FINISHED'}
        _capture_ops(self, ctx)
        return {'PASS_THROUGH'}

class ARL_OT_stop(bpy.types.Operator):
    """Stop recording"""
    bl_idname = "arl.stop_record"
    bl_label  = "⏹ Stop"

    def execute(self, ctx):
        if not _RecorderState.recording:
            self.report({'WARNING'}, "No se estaba grabando.")
            return {'CANCELLED'}
        _RecorderState.recording = False
        self.report({'INFO'}, f"Grabados {_RecorderState.buffer.len()} operadores.")
        return {'FINISHED'}

class ARL_OT_play(bpy.types.Operator):
    """Replay recorded operators"""
    bl_idname = "arl.play_macro"
    bl_label  = "▶ Play"

    def execute(self, ctx):
        if not _RecorderState.buffer:
            self.report({'WARNING'}, "Nada que reproducir.")
            return {'CANCELLED'}
        for idname, kwargs in _RecorderState.buffer:
            op_mod, op_name = idname.lower().split("_ot_")
            getattr(getattr(bpy.ops, op_mod), op_name)(**kwargs)
            time.sleep(0.01)              # mini retardo para ver el efecto
        return {'FINISHED'}

def register():
    bpy.utils.register_class(ARL_OT_record)
    bpy.utils.register_class(ARL_OT_stop)
    bpy.utils.register_class(ARL_OT_play)

def unregister():
    bpy.utils.unregister_class(ARL_OT_play)
    bpy.utils.unregister_class(ARL_OT_stop)
    bpy.utils.unregister_class(ARL_OT_record)
