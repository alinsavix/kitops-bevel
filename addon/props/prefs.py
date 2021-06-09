import bpy
from .. import ui
from .. import utils


class AddonPrefs(bpy.types.AddonPreferences):
    bl_idname = utils.addon.name()


    panel_category: bpy.props.StringProperty(
        name='Panel Category',
        description='What category to show addon panel in',
        default=ui.panel.MainPanel.bl_category,
        update=utils.addon.update_panel_category,
    )


    filter_materials: bpy.props.BoolProperty(
        name='Filter Materials',
        description='Show only officially supported materials, by checking for the prefix "CW"',
        default=True,
    )


    after_bake_delay: bpy.props.FloatProperty(
        name='After Bake Delay',
        description='For how many seconds to freeze blender after starting a bake, before restoring the scene',
        default=0.5,
        min=0,
        max=10,
        step=1,
        precision=2,
    )


    auto_device_switch: bpy.props.BoolProperty(
        name='Auto Device Switch',
        description='Automatically switch to GPU rendering during bake',
        default=True,
    )


    def draw(self, context):
        layout = self.layout
        box = layout.box()

        box.separator()

        split = box.split(factor=0.5)
        split.label(text='Filter Materials')
        row = split.row()
        row.alignment = 'RIGHT'
        row.prop(self, 'filter_materials', text='')

        split = box.split(factor=0.5)
        split.label(text='Panel Category')
        split.prop(self, 'panel_category', text='')

        split = box.split(factor=0.5)
        split.label(text='After Bake Delay')
        split.prop(self, 'after_bake_delay', text='')

        split = box.split(factor=0.5)
        split.label(text='Auto Device Switch')
        row = split.row()
        row.alignment = 'RIGHT'
        row.prop(self, 'auto_device_switch', text='')

        box.separator()
