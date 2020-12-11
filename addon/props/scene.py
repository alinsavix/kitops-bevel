import bpy
from . options import OptionsProps
from . preview import PreviewProps
from . materials import MaterialsProps


class SceneProps(bpy.types.PropertyGroup):
    options: bpy.props.PointerProperty(type=OptionsProps)
    preview: bpy.props.PointerProperty(type=PreviewProps)
    materials: bpy.props.PointerProperty(type=MaterialsProps)
