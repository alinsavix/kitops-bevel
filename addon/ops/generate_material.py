import bpy
from .. import assets
from .. import utils


class GenerateMaterial(bpy.types.Operator):
    bl_idname = 'kob.generate_material'
    bl_label = 'Generate Material'
    bl_description = 'Combine your baked textures and chosen materials into a new material'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and utils.obj.poll_active() and utils.mat.poll_images()


    def execute(self, context):
        preview = utils.addon.preview()
        if preview.previewing:
            bpy.ops.kob.preview_bevel()

        active = context.active_object
        options = utils.addon.options()
        materials = utils.addon.materials()

        if materials.material_one is None:
            name = utils.mat.get_material_name('PAINT_MATTE')
            materials.material_one = assets.append_material(name)

        if not utils.mat.poll_material(None, materials.material_one):
            self.report({'WARNING'}, f'Material {materials.material_one.name} is not compatible')
            return {'CANCELLED'}

        if options.bevel_mode == 'WORN_BEVEL':
            if materials.material_two is None:
                name = utils.mat.get_material_name('STEEL')
                materials.material_two = assets.append_material(name)

            if not utils.mat.poll_material(None, materials.material_two):
                self.report({'WARNING'}, f'Material {materials.material_two.name} is not compatible')
                return {'CANCELLED'}

        context.area.type = 'NODE_EDITOR'
        context.area.ui_type = 'ShaderNodeTree'
        context.area.tag_redraw()

        tree_one = utils.mat.group_material(materials.material_one, 'Material One')
        if options.bevel_mode == 'WORN_BEVEL':
            tree_two = utils.mat.group_material(materials.material_two, 'Material Two')

        name_type = f'UNIQUE_{options.bevel_mode}'
        unique_name = utils.mat.get_material_name(name_type)

        if unique_name in bpy.data.materials:
            material = bpy.data.materials[unique_name]
            bpy.data.materials.remove(material)

        name = utils.mat.get_material_name(options.bevel_mode)
        material = assets.append_material(name)
        material.name = unique_name
        utils.mat.assign_material(active, material)

        material.use_nodes = True
        node_tree = material.node_tree
        nodes = node_tree.nodes
        links = node_tree.links

        if options.bevel_mode == 'NORMAL_BEVEL':
            image_normal = nodes['Image Normal']
            image_normal.image = utils.mat.get_bevel_image('NORMAL')

            normal_map = nodes['Normal Map']
            normal_map.space = options.normal_space

            group_one = nodes['Group One']
            group_one.node_tree = tree_one

            output = nodes['Material Output']

            links.new(group_one.inputs['Normal'], normal_map.outputs['Normal'])
            links.new(output.inputs['Surface'], group_one.outputs['Shader'])

        elif options.bevel_mode == 'WORN_BEVEL':
            image_normal = nodes['Image Normal']
            image_normal.image = utils.mat.get_bevel_image('NORMAL')

            image_mask = nodes['Image Mask']
            image_mask.image = utils.mat.get_bevel_image('MASK')

            normal_map = nodes['Normal Map']
            normal_map.space = options.normal_space

            bump = nodes['Bump']
            normal = nodes['Reroute Normal']

            group_worn_edges = nodes['Group Worn Edge']

            group_one = nodes['Group One']
            group_one.node_tree = tree_one

            group_two = nodes['Group Two']
            group_two.node_tree = tree_two

            shader_mix = nodes['Mix Shader']

            links.new(group_one.inputs['Normal'], bump.outputs['Normal'])
            links.new(group_two.inputs['Normal'], normal.outputs['Output'])

            links.new(shader_mix.inputs[1], group_one.outputs['Shader'])
            links.new(shader_mix.inputs[2], group_two.outputs['Shader'])

        context.space_data.node_tree = node_tree
        bpy.ops.node.select_all(action='DESELECT')

        context.area.type = 'VIEW_3D'
        context.area.tag_redraw()

        self.report({'INFO'}, f'Generated material {unique_name}')
        return {'FINISHED'}
