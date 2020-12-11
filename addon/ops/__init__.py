import bpy
from . import apply_modifiers
from . import uv_unwrap
from . import preview_bevel
from . import bake_bevel
from . import save_normal
from . import save_mask
from . import generate_material


classes = (
    apply_modifiers.ApplyModifiers,
    uv_unwrap.UVUnwrap,
    preview_bevel.PreviewBevel,
    bake_bevel.BakeBevel,
    save_normal.SaveNormal,
    save_mask.SaveMask,
    generate_material.GenerateMaterial,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
