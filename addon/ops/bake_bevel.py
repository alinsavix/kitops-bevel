import bpy
import time
from .. import assets
from .. import utils


class BakeBevel(bpy.types.Operator):
    bl_idname = 'kob.bake_bevel'
    bl_label = 'Bake Bevel'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}


    @classmethod
    def description(cls, context, properties):
        return f'Bake the bevel {properties.bevel.lower()}'


    bevel: bpy.props.EnumProperty(
        name='Bevel',
        description='Which bevel to preview',
        items=[
            ('NORMAL', 'Normal', 'Preview bevel normal'),
            ('MASK', 'Mask', 'Preview bevel mask'),
        ],
        options={'HIDDEN'},
    )


    @classmethod
    def poll(cls, context):
        active = context.active_object
        return context.mode == 'OBJECT' and utils.obj.poll_active()


    def execute(self, context):
        if 'cycles' not in context.preferences.addons:
            self.report({'WARNING'}, 'Please enable Cycles')
            return {'CANCELLED'}

        preview = utils.addon.preview()
        if preview.previewing:
            bpy.ops.kob.preview_bevel()

        device_type, devices_use = utils.render.setup_compute()

        render_engine = context.scene.render.engine
        cycles_device = context.scene.cycles.device
        cycles_samples = context.scene.cycles.samples
        shading_type = context.space_data.shading.type

        context.scene.render.engine = 'CYCLES'
        context.scene.cycles.device = 'GPU'
        context.scene.cycles.samples = 32
        context.space_data.shading.type = 'MATERIAL'

        options = utils.addon.options()

        bake_type = utils.mat.get_bake_type(self.bevel)
        normal_space = options.normal_space

        texture_resolution = int(options.texture_resolution)
        margin = round(texture_resolution * options.uv_island_margin)

        active = context.active_object
        utils.obj.only_select(active)

        mesh_original = active.data
        mesh_copy = mesh_original.copy()
        active.data = mesh_copy

        name = utils.mat.get_material_name(self.bevel)
        mat = assets.append_material(name)
        utils.mat.assign_material(active, mat)
        utils.mat.prepare_image_node(mat, self.bevel)

        if self.bevel == 'NORMAL':
            utils.mat.update_bevel_normal(options, context)
        elif self.bevel == 'MASK':
            utils.mat.update_bevel_mask(options, context)

        if not active.data.uv_layers:
            bpy.ops.kob.uv_unwrap()

        bpy.ops.object.bake(
            'INVOKE_DEFAULT',
            type=bake_type,
            normal_space=normal_space,
            width=texture_resolution,
            height=texture_resolution,
            margin=margin,
            use_selected_to_active=False,
            use_clear=True,
        )

        prefs = utils.addon.prefs()
        time.sleep(prefs.after_bake_delay)

        utils.render.reset_compute(device_type, devices_use)

        context.scene.render.engine = render_engine
        context.scene.cycles.device = cycles_device
        context.scene.cycles.samples = cycles_samples
        context.space_data.shading.type = shading_type

        active.data = mesh_original
        bpy.data.meshes.remove(mesh_copy)

        return {'FINISHED'}
