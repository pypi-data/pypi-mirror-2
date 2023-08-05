from logging import getLogger
from plone.browserlayer import utils as layerutils
from collective.cu3er.interfaces import ICU3ERSpecific

log = getLogger('collective.cu3er')


def resetLayers(context):
    """Remove custom browserlayer on uninstall."""

    if context.readDataFile('collective.cu3er_uninstall.txt') is None:
        return
    
    if ICU3ERSpecific in layerutils.registered_layers():
        layerutils.unregister_layer(name='collective.cu3er')
        log.info('Browser layer "collective.cu3er" uninstalled.')


