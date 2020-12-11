import bpy
from . import addon
from . import prefs
from . import options
from . import preview
from . import materials
from . import scene


classes = (
    addon.AddonProps,
    prefs.AddonPrefs,
    options.OptionsProps,
    preview.PreviewProps,
    materials.MaterialsProps,
    scene.SceneProps,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.WindowManager.kitops_bevel = bpy.props.PointerProperty(type=addon.AddonProps)
    bpy.types.Scene.kitops_bevel = bpy.props.PointerProperty(type=scene.SceneProps)


def unregister():
    del bpy.types.Scene.kitops_bevel
    del bpy.types.WindowManager.kitops_bevel

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
