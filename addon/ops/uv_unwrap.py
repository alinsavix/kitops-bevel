import bpy
from .. import utils


class UVUnwrap(bpy.types.Operator):
    bl_idname = 'kob.uv_unwrap'
    bl_label = 'UV Unwrap'
    bl_description = 'UV Unwrap selected object'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        return context.mode in {'OBJECT', 'EDIT_MESH'} and utils.obj.poll_active()


    def execute(self, context):
        options = utils.addon.options()
        active = context.active_object

        old_mode = utils.obj.mode_set(active, 'OBJECT')
        utils.obj.only_select(active)

        utils.obj.mode_set(active, 'EDIT')
        utils.obj.uv_unwrap(active, options.uv_angle_limit, options.uv_island_margin)

        utils.obj.mode_set(active, old_mode)

        self.report({'INFO'}, f'UV unwrapped {active.name}')
        return {'FINISHED'}
