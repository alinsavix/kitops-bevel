import bpy
from .. import ui


def name() -> str:
    '''The module name for this addon.'''
    return __name__.partition('.')[0]


def prefs() -> bpy.types.AddonPreferences:
    '''The preferences for this addon.'''
    return bpy.context.preferences.addons[name()].preferences


def scene() -> bpy.types.PropertyGroup:
    '''The properties which this addon stores in the scene.'''
    return bpy.context.scene.kitops_bevel


def options() -> bpy.types.PropertyGroup:
    '''All the options for unwrapping and baking.'''
    return bpy.context.scene.kitops_bevel.options


def preview() -> bpy.types.PropertyGroup:
    '''The state of the preview feature.'''
    return bpy.context.scene.kitops_bevel.preview


def materials() -> bpy.types.PropertyGroup:
    '''The materials used for the generate material feature.'''
    return bpy.context.scene.kitops_bevel.materials


def update_panel_category(self=None, context=None):
    '''Change the category for addon panels.'''
    preferences = prefs()

    if not preferences.panel_category:
        preferences.property_unset('panel_category')

    for cls in ui.classes:
        if issubclass(cls, bpy.types.Panel):
            cls.bl_category = preferences.panel_category

            bpy.utils.unregister_class(cls)
            bpy.utils.register_class(cls)
