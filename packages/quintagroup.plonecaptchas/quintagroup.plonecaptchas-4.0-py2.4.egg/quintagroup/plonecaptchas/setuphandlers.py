import logging
from zope.component import getSiteManager
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('quintagroup.plonecaptchas')

def removeBrowserLayer(site):
    """ Remove browser layer.
    """
    from plone.browserlayer.utils import unregister_layer
    from plone.browserlayer.interfaces import ILocalBrowserLayerType

    name="quintagroup.plonecaptchas"
    site = getSiteManager(site)
    registeredLayers = [r.name for r in site.registeredUtilities()
                        if r.provided == ILocalBrowserLayerType]
    if name in registeredLayers:
        unregister_layer(name, site_manager=site)
        logger.log(logging.INFO, "Unregistered \"%s\" browser layer." % name)

def uninstall(context):
    """ Do customized uninstallation.
    """
    if context.readDataFile('qgplonecaptchas_uninstall.txt') is None:
        return
    site = context.getSite()
    removeBrowserLayer(site)
