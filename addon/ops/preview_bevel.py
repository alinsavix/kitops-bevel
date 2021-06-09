import bpy
from .. import assets
from .. import utils


class PreviewBevel(bpy.types.Operator):
    bl_idname = 'kob.preview_bevel'
    bl_label = 'Preview Bevel'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}


    @classmethod
    def description(cls, context, properties):
        preview = utils.addon.preview()

        if not preview.previewing:
            return f'Preview the bevel {properties.bevel.lower()}'
        else:
            return 'Stop previewing bevel'


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
        return context.mode == 'OBJECT' and utils.obj.poll_active()


    def execute(self, context):
        prefs = utils.addon.prefs()
        options = utils.addon.options()
        preview = utils.addon.preview()

        render = context.scene.render
        cycles = context.scene.cycles
        shading = context.space_data.shading
        active = context.active_object

        if not preview.previewing:
            if 'cycles' not in context.preferences.addons:
                self.report({'WARNING'}, 'Please enable Cycles')
                return {'CANCELLED'}

            preview.previewing = True

            if prefs.auto_device_switch:
                device_type, devices_use = utils.render.setup_compute()
                preview.device_type = device_type

                for device_use in devices_use:
                    preview.devices_use.add()
                    preview.devices_use[-1].name = str(device_use)

            preview.render_engine = render.engine
            if prefs.auto_device_switch:
                preview.cycles_device = cycles.device
            preview.shading_type = shading.type

            preview.shading_scene_lights = shading.use_scene_lights_render
            preview.shading_scene_world = shading.use_scene_world_render

            preview.active_object = active.name

            for obj in context.selected_objects:
                preview.selected_objects.add()
                preview.selected_objects[-1].name = obj.name

            for obj in context.scene.objects:
                if obj.hide_get() == False:
                    preview.visible_objects.add()
                    preview.visible_objects[-1].name = obj.name

            for mat in active.data.materials:
                preview.materials.add()
                preview.materials[-1].name = mat.name

            for poly in active.data.polygons:
                preview.polygons.add()
                preview.polygons[-1].name = str(poly.material_index)

            render.engine = 'CYCLES'
            if prefs.auto_device_switch:
                cycles.device = 'GPU'
            shading.type = 'RENDERED'

            shading.use_scene_lights_render = False
            shading.use_scene_world_render = False

            utils.obj.only_visible(active)
            name = utils.mat.get_material_name(self.bevel)
            mat = assets.append_material(name)
            utils.mat.assign_material(active, mat)

            if self.bevel == 'NORMAL':
                utils.mat.update_bevel_normal(options, context)
            elif self.bevel == 'MASK':
                utils.mat.update_bevel_mask(options, context)

            self.report({'INFO'}, f'Previewing bevel {self.bevel.lower()}')
            return {'FINISHED'}

        else:
            preview.previewing = False

            if prefs.auto_device_switch:
                devices_use = [True if device_use.name == 'True' else False for device_use in preview.devices_use]
                utils.render.reset_compute(preview.device_type, devices_use)
                preview.devices_use.clear()

            render.engine = preview.render_engine
            if prefs.auto_device_switch:
                cycles.device = preview.cycles_device
            shading.type = preview.shading_type

            shading.use_scene_lights_render = preview.shading_scene_lights
            shading.use_scene_world_render = preview.shading_scene_world

            if preview.active_object in bpy.data.objects:
                active = bpy.data.objects[preview.active_object]

                bpy.ops.object.select_all(action='SELECT')
                bpy.ops.object.hide_view_set(unselected=False)

                for item in preview.visible_objects:
                    obj = bpy.data.objects[item.name]
                    obj.hide_set(False)

                for item in preview.selected_objects:
                    if item.name in bpy.data.objects:
                        obj = bpy.data.objects[item.name]
                        obj.select_set(True)

                active.data.materials.clear()

                for item in preview.materials:
                    if item.name in bpy.data.materials:
                        mat = bpy.data.materials[item.name]
                        active.data.materials.append(mat)

                if len(preview.materials) == len(active.data.materials):
                    if len(preview.polygons) == len(active.data.polygons):
                        for index, item in enumerate(preview.polygons):
                            poly = active.data.polygons[index]
                            poly.material_index = int(item.name)

            preview.selected_objects.clear()
            preview.visible_objects.clear()
            preview.materials.clear()
            preview.polygons.clear()

            self.report({'INFO'}, f'Stopped preview')
            return {'FINISHED'}
