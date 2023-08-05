from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import Interface
from five import grok
from AccessControl.Permissions import copy_or_move
from AccessControl.Permissions import delete_objects
from plonetheme.nuplone.skin.interfaces import NuPloneSkin
from plonetheme.nuplone.utils import checkPermission
from plonetheme.nuplone.utils import getFactoriesInContext
from Products.CMFCore.interfaces import ISiteRoot
from OFS.interfaces import ICopyContainer
from OFS.interfaces import ICopySource


grok.templatedir("templates")


class Sitemenu(grok.View):
    grok.context(Interface)
    grok.name("sitemenu")
    grok.layer(NuPloneSkin)
    grok.template("sitemenu")

    @property
    def settings_url(self):
        return "%s/@@settings" % self.navroot_url

    def update(self):
        self.view_type=self.request.get("view_type", "view")

        context=aq_inner(self.context)
        parent=aq_parent(context)
        is_root=ISiteRoot.providedBy(context)
        is_copyable=not is_root and ICopySource.providedBy(context) and checkPermission(context, copy_or_move)
        self.can_delete=not is_root and checkPermission(parent, delete_objects)
        self.can_copy=is_copyable and context.cb_isCopyable()
        self.can_cut=is_copyable and self.can_delete and context.cb_isMoveable()
        self.can_paste=ICopyContainer.providedBy(context) and context.cb_dataValid()


    def factories(self):
        actions=getFactoriesInContext(self.context)
        actions.sort(key=lambda x: x.title)
        return actions
