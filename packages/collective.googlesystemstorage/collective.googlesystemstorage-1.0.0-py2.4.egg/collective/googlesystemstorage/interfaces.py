"""
Interfaces exposed here
"""
__author__  = 'federica'
__docformat__ = 'restructuredtext'

from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import Interface

class IFSSInfo(IAttributeAnnotatable):
    """Marker for FSSInfo"""
    pass

class IGoogleDocsManaged(Interface):
    """Marker interface for documents stored on Google Docs service"""