from plone.memoize.instance import memoize

from plone.app.contentmenu.menu import FactoriesSubMenuItem

class PloneboardFactoriesSubMenuItem(FactoriesSubMenuItem):

    @memoize
    def _addingToParent(self):
        return True
