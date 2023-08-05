from zope.i18nmessageid import MessageFactory

from AccessControl import allow_module, ModuleSecurityInfo

ProductMessageFactory = MessageFactory('quintagroup.plonecaptchas')
ModuleSecurityInfo('quintagroup.plonecaptchas').declarePublic("ProductMessageFactory")

#from quintagroup.plonecaptchas import config
#allow_module('quintagroup.plonecaptchas.config')

def initialize(context):
    pass
