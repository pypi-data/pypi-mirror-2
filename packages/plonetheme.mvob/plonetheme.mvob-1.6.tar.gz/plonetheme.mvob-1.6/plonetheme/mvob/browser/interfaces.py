from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "MVOB Theme" theme, this interface must be its layer
       (in mvob/viewlets/configure.zcml).
    """
    
    
class ISearchView(Interface):
    """Used to provide python functions to the search results
    """
    def prefs(self):
        '''Used for displaying leadimage'''

    def tag(self, obj, css_class='tileImage', scale='mini'):
        '''Used to crate the tag for the leadimage'''
