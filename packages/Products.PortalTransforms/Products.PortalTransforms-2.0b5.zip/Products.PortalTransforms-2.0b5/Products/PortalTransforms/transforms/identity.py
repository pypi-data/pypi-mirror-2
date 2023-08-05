"""
A simple identity transform
"""

__revision__ = '$Id: identity.py 9698 2008-05-20 02:48:17Z ldr $'

from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implements

class IdentityTransform:
    """ Identity transform

    return content unchanged.
    """
    implements(ITransform)

    __name__ = "rest_to_text"

    def __init__(self, name=None, **kwargs):
        self.config = {
            'inputs'       : ('text/x-rst',),
            'output'      : 'text/plain',
            }
        self.config_metadata = {
            'inputs'       : ('list', 'Inputs', 'Input(s) MIME type. Change with care.'),
            'output'      : ('string', 'Output', 'Output MIME type. Change with care.'),
            }
        self.config.update(kwargs)

    def __getattr__(self, attr):
        if attr == 'inputs':
            return self.config['inputs']
        if attr == 'output':
            return self.config['output']
        raise AttributeError(attr)

    def name(self):
        return self.__name__

    def convert(self, data, cache, **kwargs):
        cache.setData(data)
        return cache

def register():
    return IdentityTransform()
