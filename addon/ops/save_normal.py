import bpy
from .. import utils


class SaveNormal(bpy.types.Operator):
    bl_idname = 'kob.save_normal'
    bl_label = 'Save Normal'
    bl_description = 'Save the normal image for this object to disk'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and utils.obj.poll_active() and utils.mat.check_bevel_image('NORMAL')


    def execute(self, context):
        utils.mat.save_bevel_image('NORMAL')
        return {'FINISHED'}
