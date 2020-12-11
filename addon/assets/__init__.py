import bpy
import pathlib


def append_material(name: str) -> bpy.types.Material:
    '''Append desired material from the materials blend file and return it.'''
    if name not in bpy.data.materials:
        path = pathlib.Path(__file__).resolve()
        path = str(path.parent / 'materials.blend')

        with bpy.data.libraries.load(path) as (data_from, data_to):
            data_to.materials = [name]

    return bpy.data.materials[name]
