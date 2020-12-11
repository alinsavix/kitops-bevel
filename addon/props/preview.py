import bpy


class PreviewProps(bpy.types.PropertyGroup):
    previewing: bpy.props.BoolProperty()

    device_type: bpy.props.StringProperty()
    devices_use: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

    render_engine: bpy.props.StringProperty()
    cycles_device: bpy.props.StringProperty()
    shading_type: bpy.props.StringProperty()

    shading_scene_lights: bpy.props.BoolProperty()
    shading_scene_world: bpy.props.BoolProperty()

    active_object: bpy.props.StringProperty()

    selected_objects: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    visible_objects: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

    materials: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    polygons: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
