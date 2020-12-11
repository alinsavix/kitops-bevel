import bpy
import bmesh
import math


def poll_active() -> bool:
    '''Return whether the active object exists, is a mesh, and is selected.'''
    active = bpy.context.active_object
    return active and active.type == 'MESH' and active.select_get()


def mode_set(obj: bpy.types.Object, new_mode: str) -> str:
    '''Set mode, returns previous mode.'''
    old_mode = obj.mode

    if old_mode != new_mode:
        bpy.ops.object.mode_set(mode=new_mode)

    return old_mode


def only_select(obj: bpy.types.Object):
    '''Make object the only one selected. Requires object mode.'''
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)


def only_visible(obj: bpy.types.Object):
    '''Make object the only one selected and visible. Requires object mode.'''
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.ops.object.hide_view_set(unselected=True)


def apply_modifiers(obj: bpy.types.Object) -> int:
    '''Apply all modifiers and return the amount of modifiers. Use KIT OPS conver to mesh when it is available. Requires object mode.'''
    count = len(obj.modifiers)

    if 'kitops' in bpy.context.preferences.addons:
        bpy.ops.ko.convert_to_mesh()
    else:
        bpy.ops.object.convert(target='MESH')

    return count


def uv_unwrap(obj: bpy.types.Object, angle_limit: float, island_margin: float):
    '''Smart UV project. Requires edit mode.'''
    bpy.ops.mesh.reveal(select=False)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.mark_seam(clear=True)

    if bpy.app.version < (2, 91, 0):
        bpy.ops.uv.smart_project(angle_limit=angle_limit, island_margin=island_margin, use_aspect=True, stretch_to_bounds=False)
    else:
        bpy.ops.uv.smart_project(angle_limit=math.radians(angle_limit), island_margin=island_margin, correct_aspect=True, scale_to_bounds=False)

    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.uv.seams_from_islands(mark_seams=True, mark_sharp=False)

    bpy.ops.uv.select_all(action='DESELECT')
    bpy.ops.mesh.select_all(action='DESELECT')
