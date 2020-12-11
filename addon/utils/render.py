import bpy
import typing


def setup_compute() -> typing.Tuple[str, typing.List[bool]]:
    '''Setup Cycles compute settings for baking.'''
    context = bpy.context

    cycles = context.preferences.addons['cycles'].preferences
    device_type = cycles.compute_device_type
    devices_use = [device.use for device in cycles.devices]

    devices_type = [device.type for device in cycles.devices]
    devices_cuda = devices_type.count('CUDA')
    devices_opencl = devices_type.count('OPENCL')

    if devices_cuda or devices_opencl:
        cycles.compute_device_type = 'CUDA' if devices_cuda >= devices_opencl else 'OPENCL'

        for device in cycles.devices:
            device.use = device.type == cycles.compute_device_type

    return device_type, devices_use


def reset_compute(device_type: str, devices_use: typing.List[bool]):
    '''Restore Cycles compute settings after baking.'''
    context = bpy.context

    cycles = context.preferences.addons['cycles'].preferences
    cycles.compute_device_type = device_type

    for device, device_use in zip(cycles.devices, devices_use):
        device.use = device_use
