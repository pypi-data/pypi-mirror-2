# Copyright (c) 2009 Assembly Organizing
# See also LICENSE.txt

import asm.cms.interfaces
import grok
import megrok.pagelet
import zope.interface


class Layout(megrok.pagelet.Layout):
    grok.context(zope.interface.Interface)
    grok.layer(asm.cms.interfaces.IRetailSkin)

    megrok.pagelet.template('templates/retail.pt')


class Pagelet(megrok.pagelet.Pagelet):

    grok.baseclass()
    grok.layer(asm.cms.interfaces.IRetailSkin)


class RetailTraverser(grok.Traverser):
    """Retail traversers try to map URLs to page *editions* when the URL would
    normally point to a page.

    We also hide the editions' real URLs and point them to the pages' URLs.

    """

    grok.baseclass()

    # This directive is currently ignored due to LP #408819. See workaround
    # below.
    grok.layer(asm.cms.interfaces.IRetailSkin)

    def traverse(self, name):
        if not asm.cms.interfaces.IRetailSkin.providedBy(self.request):
            # Workaround for grok.layer bug
            return
        page = self.get_context()
        subpage = page.get(name)
        if not asm.cms.interfaces.IPage.providedBy(subpage):
            return
        return asm.cms.edition.select_edition(subpage, self.request)

    def get_context(self):
        return self.context


class RootTraverse(RetailTraverser):

    grok.context(zope.app.folder.interfaces.IRootFolder)


class PageTraverse(RetailTraverser):

    grok.context(asm.cms.interfaces.IPage)


class EditionTraverse(RetailTraverser):

    grok.context(asm.cms.interfaces.IEdition)

    def get_context(self):
        return self.context.page


@grok.adapter(asm.cms.interfaces.IEdition, asm.cms.interfaces.IRetailSkin)
@grok.implementer(zope.traversing.browser.interfaces.IAbsoluteURL)
def edition_url(edition, request):
    return zope.component.getMultiAdapter(
        (edition.__parent__, request),
        zope.traversing.browser.interfaces.IAbsoluteURL)


@grok.subscribe(zope.publisher.interfaces.http.IHTTPVirtualHostChangedEvent)
def fix_virtual_host(event):
    if not asm.cms.IRetailSkin.providedBy(event.request):
        return
    root = event.request.getVirtualHostRoot()
    if asm.cms.interfaces.IEdition.providedBy(root):
        # XXX This is extremely hacky but the APIs don't allow me to do
        # better.
        event.request._vh_root = root.__parent__
