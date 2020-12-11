import bpy
from .. import utils


class SaveMask(bpy.types.Operator):
    bl_idname = 'kob.save_mask'
    bl_label = 'Save Mask'
    bl_description = 'Save the mask image for this object to disk'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and utils.obj.poll_active() and utils.mat.check_bevel_image('MASK')


    def execute(self, context):
        utils.mat.save_bevel_image('MASK')
        return {'FINISHED'}
