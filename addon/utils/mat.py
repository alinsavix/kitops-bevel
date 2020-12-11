import bpy
from .. import assets
from .. import utils


def get_bake_type(type: str) -> str:
    '''Return the appropriate bake type for the given purpose.'''
    if type == 'NORMAL':
        return 'NORMAL'
    elif type == 'MASK':
        return 'EMIT'


def find_node(node_tree: bpy.types.NodeTree, bl_idname: str) -> bpy.types.ShaderNode:
    '''Return the first node with the given bl_idname.'''
    return next(node for node in node_tree.nodes if node.bl_idname == bl_idname)


def update_bevel_node(name: str, radius: float):
    '''Update bevel node in material to match bevel radius.'''
    if name in bpy.data.materials:
        mat = bpy.data.materials[name]
        node = find_node(mat.node_tree, 'ShaderNodeBevel')
        node.inputs['Radius'].default_value = radius


def update_bevel_normal(self: bpy.types.PropertyGroup, context: bpy.types.Context):
    '''Update bevel node in bevel normal material to use new radius.'''
    name = get_material_name('NORMAL')
    update_bevel_node(name, self.bevel_normal)


def update_bevel_mask(self: bpy.types.PropertyGroup, context: bpy.types.Context):
    '''Update bevel node in bevel mask material to use new radius.'''
    name = get_material_name('MASK')
    update_bevel_node(name, self.bevel_mask)


def get_material_name(type: str) -> str:
    '''Return the material name that goes with the given type.'''
    if type == 'NORMAL':
        return 'CW-Bake-Normal'
    elif type == 'MASK':
        return 'CW-Bake-Mask'

    elif type == 'PAINT_MATTE':
        return 'CW-Bevel-PaintMatte'
    elif type == 'STEEL':
        return 'CW-Bevel-Steel'

    elif type == 'NORMAL_BEVEL':
        return 'CW-Bevel-Normal'
    elif type == 'WORN_BEVEL':
        return 'CW-Bevel-Worn'

    elif type == 'UNIQUE_NORMAL_BEVEL':
        return f'{bpy.context.active_object.name[0:40]} Normal Bevel'
    elif type == 'UNIQUE_WORN_BEVEL':
        return f'{bpy.context.active_object.name[0:40]} Worn Bevel'


def assign_material(obj: bpy.types.Object, mat: bpy.types.Material):
    '''Clear materials from object, assign desired material.'''
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def get_image_name(type: str) -> str:
    '''Return the image name that goes with the given type.'''
    if type == 'NORMAL':
        return f'{bpy.context.active_object.name[0:40]} Bevel Normal'
    elif type == 'MASK':
        return f'{bpy.context.active_object.name[0:40]} Bevel Mask'


def check_bevel_image(type: str) -> bool:
    '''Return whether the image of this type exists.'''
    name = get_image_name(type)
    return name in bpy.data.images


def get_bevel_image(type: str) -> bpy.types.Image:
    '''Return the image of this type, creating it if necessary.'''
    name = get_image_name(type)

    options = utils.addon.options()
    res = int(options.texture_resolution)

    if name in bpy.data.images:
        return bpy.data.images[name]
    else:
        return bpy.data.images.new(name, res, res)


def reset_image(img: bpy.types.Image):
    '''Reset the given image to make sure we can bake to it.'''
    options = utils.addon.options()
    res = int(options.texture_resolution)

    img.source = 'GENERATED'
    img.generated_width = res
    img.generated_height = res
    img.use_generated_float = False
    img.generated_type = 'BLANK'
    img.generated_color = (0, 0, 0, 1)
    img.colorspace_settings.name = 'Non-Color'


def prepare_image_node(mat: bpy.types.Material, type: str):
    '''Find the first image texture node in the given material, make it active, and assign an appropriate image to it.'''
    node = find_node(mat.node_tree, 'ShaderNodeTexImage')
    mat.node_tree.nodes.active = node
    node.image = get_bevel_image(type)
    reset_image(node.image)


def poll_images() -> bool:
    '''Check whether the necessary images have been baked.'''
    if bpy.context.active_object:
        options = utils.addon.options()

        if options.bevel_mode == 'NORMAL_BEVEL':
            return check_bevel_image('NORMAL')

        elif options.bevel_mode == 'WORN_BEVEL':
            return check_bevel_image('NORMAL') and check_bevel_image('MASK')


def poll_material(self: bpy.types.PropertyGroup, mat: bpy.types.Material) -> bool:
    '''Check whether a material is suitable for use with the material creation feature.'''
    if mat and mat.use_nodes:
        prefs = utils.addon.prefs()

        cw = prefs.filter_materials and mat.name.lower().startswith('cw')
        name = cw or not prefs.filter_materials

        types = {get_material_name(bevel) for bevel in ('NORMAL', 'MASK')}
        name = name and (mat.name not in types)

        node = mat.node_tree.get_output_node('EEVEE')
        shader = node and node.inputs['Surface'].is_linked

        nodes = [node for node in mat.node_tree.nodes if 'Normal' in node.inputs]
        normal = any(not node.inputs['Normal'].is_linked for node in nodes)

        return name and shader and normal


def group_material(mat: bpy.types.Material, name: str) -> bpy.types.ShaderNodeTree:
    '''Add all the necessary nodes of this material to a new node group and return it. Requires shader node editor.'''
    active = bpy.context.active_object

    group_name = f'{active.name} {name}'
    if group_name in bpy.data.node_groups:
        group_tree = bpy.data.node_groups[group_name]
        bpy.data.node_groups.remove(group_tree)

    mat = mat.copy()
    assign_material(active, mat)
    bpy.context.space_data.node_tree = mat.node_tree

    for node in mat.node_tree.nodes[:]:
        if node.bl_idname == 'ShaderNodeOutputMaterial' and not node.is_active_output:
            mat.node_tree.nodes.remove(node)

    bpy.ops.node.select_all(action='SELECT')
    mat.node_tree.get_output_node('EEVEE').select = False
    bpy.ops.node.group_make()

    group = find_node(mat.node_tree, 'ShaderNodeGroup')
    group.node_tree.name = group_name
    group.node_tree.outputs[0].name = 'Shader'

    group.node_tree.inputs.clear()
    group.node_tree.inputs.new('NodeSocketVector', 'Normal')

    if 'hide_value' in group.node_tree.inputs['Normal']:
        group.node_tree.inputs['Normal'].hide_value = True

    group_input = find_node(group.node_tree, 'NodeGroupInput')
    group_input_socket = group_input.outputs['Normal']

    for node in group.node_tree.nodes:
        if 'Normal' in node.inputs and not node.inputs['Normal'].is_linked:
            group.node_tree.links.new(node.inputs['Normal'], group_input_socket)

    node_tree = group.node_tree
    bpy.data.materials.remove(mat)
    return node_tree


def bevel_image_dirty(type: str) -> bool:
    '''Return whether the image of this type exists and has unsaved changes.'''
    name = get_image_name(type)
    if name in bpy.data.images:
        image = bpy.data.images[name]
        return image.is_dirty


def save_bevel_image(type: str):
    '''Open a file save dialog for the image of this type.'''
    bpy.context.area.type = 'IMAGE_EDITOR'
    bpy.context.area.tag_redraw()

    bpy.context.space_data.image = get_bevel_image(type)
    bpy.ops.image.save_as('INVOKE_DEFAULT')

    bpy.context.area.type = 'VIEW_3D'
    bpy.context.area.tag_redraw()
