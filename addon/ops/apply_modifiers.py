import bpy
from .. import utils


class ApplyModifiers(bpy.types.Operator):
    bl_idname = 'kob.apply_modifiers'
    bl_label = 'Apply Modifiers'
    bl_description = 'Apply all modifiers on the active object'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and utils.obj.poll_active() and len(context.active_object.modifiers) > 0


    def execute(self, context):
        active = context.active_object
        utils.obj.only_select(active)

        old_mode = utils.obj.mode_set(active, 'OBJECT')
        count = utils.obj.apply_modifiers(active)
        utils.obj.mode_set(active, old_mode)

        self.report({'INFO'}, f'Applied {count} modifiers')
        return {'FINISHED'}
