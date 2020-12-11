import bpy
from .. import utils


class OptionsProps(bpy.types.PropertyGroup):
    bevel_mode: bpy.props.EnumProperty(
        name='Bevel Mode',
        description='Whether to bake one or two bevels',
        items=[
            ('NORMAL_BEVEL', 'Normal Bevel', 'Only bake a single bevel, used for shading'),
            ('WORN_BEVEL', 'Worn Bevel', 'Bake two bevels, a smaller one for shading and larger one as mask for the chipped paint material'),
        ],
        default='NORMAL_BEVEL',
    )


    texture_resolution: bpy.props.EnumProperty(
        name='Texture Resolution',
        description='Resolution of the baked texture maps',
        items=[(f'{n}', f'{n}', f'Bake at {n}x{n} pixels') for n in (256, 512, 1024, 2048, 4096, 6144, 8192)],
        default='1024',
    )


    normal_space: bpy.props.EnumProperty(
        name='Normal Space',
        description='What vector space the normal map should be in',
        items=[
            ('TANGENT', 'Tangent', 'Tangent space vectors are relative to the vertex tangents, based on the UV map'),
            ('OBJECT', 'Object', 'Object space vectors are relative to the object origin'),
        ],
        default='OBJECT',
    )


    uv_angle_limit: bpy.props.FloatProperty(
        name='UV Angle Limit',
        description='Angle at which to split UV islands',
        default=30,
        min=1,
        max=89,
        step=1,
        precision=2,
    )


    uv_island_margin: bpy.props.FloatProperty(
        name='UV Island Margin',
        description='Ratio of padding around UV islands',
        default=0.05,
        min=0,
        max=1,
        step=1,
        precision=2,
    )


    bevel_normal: bpy.props.FloatProperty(
        name='Bevel Normal',
        description='Radius of the bevel normal',
        default=0.05,
        min=0,
        soft_max=1000,
        step=1,
        precision=2,
        subtype='DISTANCE',
        unit='LENGTH',
        update=utils.mat.update_bevel_normal,
    )


    bevel_mask: bpy.props.FloatProperty(
        name='Bevel Mask',
        description='Radius of the bevel mask',
        default=0.1,
        min=0,
        soft_max=1000,
        step=1,
        precision=2,
        subtype='DISTANCE',
        unit='LENGTH',
        update=utils.mat.update_bevel_mask,
    )
