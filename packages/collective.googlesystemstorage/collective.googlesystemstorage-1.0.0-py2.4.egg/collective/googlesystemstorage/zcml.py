"""
ZCML gss namespace handling, see meta.zcml
"""

__author__  = 'federica'
__docformat__ = 'restructuredtext'

import logging
from zope.interface import Interface
from zope.configuration.fields import GlobalObject, Tokens, PythonIdentifier

from iw.fss import config
from collective.googlesystemstorage.GoogleSystemStorage import GoogleSystemStorage

class ITypeWithGSSDirective(Interface):
    """Schema for gss:typeWithGSS directive"""

    class_ = GlobalObject(
        title=u'Class',
        description=u'Dotted name of class of AT based content type using GSS',
        required=True)

    fields = Tokens(
        title=u'Fields',
        description=u'Field name or space(s) separated field names',
        value_type=PythonIdentifier(),
        required=True)


def typeWithGSS(_context, class_, fields):
    """Register our monkey patch"""

    _context.action(
        discriminator=(class_.__module__,class_.__name__),
        callable=patchATType,
        args=(class_, fields)
        )


logger = logging.getLogger(config.PROJECTNAME)
LOG = logger.info

def patchATType(class_, fields):
    """Processing the type patch"""
    global patchedTypesRegistry

    for fieldname in fields:
        field = class_.schema[fieldname]
        former_storage = field.storage
        field.storage = GoogleSystemStorage()
        field.registerLayer('storage', field.storage)
        if patchedTypesRegistry.has_key(class_):
            patchedTypesRegistry[class_][fieldname] = former_storage
        else:
            patchedTypesRegistry[class_] = {fieldname: former_storage}
        LOG("Field '%s' of %s is stored in file system.", fieldname, class_.meta_type)
    return

# We register here the types that have been patched for migration purpose
patchedTypesRegistry = {
    # {content class : {field name: storage, ...}, ...}
    }
