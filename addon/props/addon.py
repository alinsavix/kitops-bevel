import bpy
from .. import utils


class AddonProps(bpy.types.PropertyGroup):
    @property
    def name(self) -> str:
        return utils.addon.name()


    @property
    def prefs(self) -> bpy.types.AddonPreferences:
        return utils.addon.prefs()


    @property
    def scene(self) -> bpy.types.PropertyGroup:
        return utils.addon.scene()


    @property
    def options(self) -> bpy.types.PropertyGroup:
        return utils.addon.options()


    @property
    def preview(self) -> bpy.types.PropertyGroup:
        return utils.addon.preview()


    @property
    def materials(self) -> bpy.types.PropertyGroup:
        return utils.addon.materials()
