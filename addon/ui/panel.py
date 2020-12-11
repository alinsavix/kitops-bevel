import bpy
from .. import icons
from .. import utils


class MainPanel(bpy.types.Panel):
    bl_idname = 'KOB_PT_main_panel'
    bl_label = 'KIT OPS BEVEL'
    bl_category = 'BEVEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        layout = self.layout

        options = utils.addon.options()
        worn_bevel = (options.bevel_mode == 'WORN_BEVEL')

        preview = utils.addon.preview()
        materials = utils.addon.materials()

        row = layout.row()
        row.emboss = 'PULLDOWN_MENU'
        row.label(text='Step 1: Choose bevel mode')

        row = layout.row()
        row.scale_x = row.scale_y = 1.5
        row.prop(options, 'bevel_mode', expand=True)

        layout.separator()

        row = layout.row()
        row.emboss = 'PULLDOWN_MENU'
        row.label(text='Step 2: UV unwrap')

        layout.prop(options, 'uv_angle_limit', slider=True)
        layout.prop(options, 'uv_island_margin', slider=True)

        row = layout.row()
        row.scale_x = row.scale_y = 1.5
        row.operator('kob.apply_modifiers', text='Apply Modifiers', icon='MODIFIER')
        row.operator('kob.uv_unwrap', text='UV Unwrap', icon='UV')

        layout.separator()

        row = layout.row()
        row.emboss = 'PULLDOWN_MENU'
        row.label(text='Step 3: Adjust bevels')

        split = layout.split(factor=0.5)
        split.prop(options, 'bevel_normal', text='Normal')

        row = split.row()
        row.enabled = worn_bevel
        row.prop(options, 'bevel_mask', text='Mask')

        if not preview.previewing:
            split = layout.split(factor=0.5)
            split.scale_x = split.scale_y = 1.5
            split.operator('kob.preview_bevel', text='Preview Normal', icon='HIDE_OFF').bevel = 'NORMAL'

            row = split.row()
            row.enabled = worn_bevel
            row.operator('kob.preview_bevel', text='Preview Mask', icon='HIDE_OFF').bevel = 'MASK'

        else:
            row = layout.row()
            row.scale_x = row.scale_y = 1.5
            row.operator('kob.preview_bevel', text='Stop Preview', icon='HIDE_ON')

        layout.separator()

        row = layout.row()
        row.emboss = 'PULLDOWN_MENU'
        row.label(text='Step 4: Bake images')

        split = layout.split(factor=0.5)
        split.label(text='Texture Resolution')
        split.prop(options, 'texture_resolution', text='')

        split = layout.split(factor=0.5)
        split.label(text='Normal Space')
        split.prop(options, 'normal_space', text='')

        split = layout.split(factor=0.5)
        split.scale_x = split.scale_y = 1.5
        split.operator('kob.bake_bevel', text='Bake Normal', icon='RENDER_STILL').bevel = 'NORMAL'

        row = split.row()
        row.enabled = worn_bevel
        row.operator('kob.bake_bevel', text='Bake Mask', icon='RENDER_STILL').bevel = 'MASK'

        layout.separator()

        row = layout.row()
        row.emboss = 'PULLDOWN_MENU'
        row.label(text='Step 5: Generate material')

        split = layout.split(factor=0.5)
        split.prop(materials, 'material_one', text='')

        row = split.row()
        row.enabled = worn_bevel
        row.prop(materials, 'material_two', text='')

        row = layout.row()
        row.scale_x = row.scale_y = 1.5

        if utils.mat.poll_images():
            row.operator('kob.generate_material', text='Generate Material', icon='MATERIAL')
        else:
            row.alert = True
            row.operator('kob.generate_material', text='You must bake image(s) first', icon='ERROR')

        layout.separator()

        row = layout.row()
        row.emboss = 'PULLDOWN_MENU'
        row.label(text='Step 6: Save images')

        row = layout.row()
        row.scale_x = row.scale_y = 1.5
        row.operator('image.save_all_modified', text='Pack Modified Images', icon='PACKAGE')

        split = layout.split(factor=0.5)
        split.scale_x = split.scale_y = 1.5
        split.operator('kob.save_normal', text='Save Normal', icon='DISK_DRIVE')

        row = split.row()
        row.enabled = worn_bevel
        row.operator('kob.save_mask', text='Save Mask', icon='DISK_DRIVE')

        layout.separator()

        row = layout.row()
        row.emboss = 'PULLDOWN_MENU'
        row.label(text='Documentation')

        row = layout.row()
        row.scale_x = row.scale_y = 1.5
        row.alignment = 'RIGHT'

        op = row.operator('wm.url_open', text='', icon_value=icons.id('question'))
        op.url = 'http://cw1.me/bevel'
