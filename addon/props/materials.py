import bpy
from .. import utils


class MaterialsProps(bpy.types.PropertyGroup):
    material_one: bpy.props.PointerProperty(
        name='Material One',
        description='The material used everywhere but worn edges',
        type=bpy.types.Material,
        poll=utils.mat.poll_material,
    )


    material_two: bpy.props.PointerProperty(
        name='Material Two',
        description='The material used on worn edges',
        type=bpy.types.Material,
        poll=utils.mat.poll_material,
    )
