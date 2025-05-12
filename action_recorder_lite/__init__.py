bl_info = {
    "name": "Action Recorder Lite",
    "author": "Tu Nombre",
    "version": (0, 1, 0),
    "blender": (4, 4, 0),
    "location": "View 3D > UI > ActRec",
    "description": "Graba y reproduce operadores como macro",
    "category": "Object",
}

from . import recorder, ui_panel
mods = (recorder, ui_panel)

def register():
    for m in mods: m.register()

def unregister():
    for m in reversed(mods): m.unregister()
