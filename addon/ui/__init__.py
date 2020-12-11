import bpy
from . import panel
from .. import utils


classes = (
    panel.MainPanel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    utils.addon.update_panel_category()


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
