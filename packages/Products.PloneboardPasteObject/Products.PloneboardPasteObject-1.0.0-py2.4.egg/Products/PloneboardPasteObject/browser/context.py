from plone.memoize.view import memoize

from Acquisition import aq_inner

from plone.app.layout.globals.context import ContextState

class PloneboardContextState(ContextState):
    """Information about the state of the current context
    """
    
    @memoize
    def folder(self):
        if self.is_folderish() and not self.is_default_page():
            return aq_inner(self.context)
        else:
            return self.parent()