# --*-- coding: utf-8 --*--

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

from yaco.deliverancethemeselector.interfaces import IDTSSupport
from yaco.deliverancethemeselector.interfaces import IDTSSettingsAnnotations

def setDeliveranceThemeSelectorHeader(site, event):
    """ Add the 'X-Deliverance-Page-Class' header in the request
    """
    if not IPloneSiteRoot.providedBy(site):
        return

    request = event.request

    for skip in ('portal_css', 'portal_javascripts', 'portal_kss'):
        if skip in request.TraversalRequestNameStack:
            return

    stack = []
    stack.extend(request.TraversalRequestNameStack)
    stack.extend(site.getPhysicalPath())
    stack = [x for x in stack if not x in ['', '/', 'virtual_hosting']]
    stack.append('')
    stack.reverse()

    portal_catalog = getToolByName(site, 'portal_catalog')
    while stack:
        item = stack.pop()
        if not item: break
        path = '/'.join(stack)

        query = {}
        query['id'] = str(item)
        query['path'] = {'query' : path}
        query['object_provides'] = IDTSSupport.__identifier__

        brains = portal_catalog.unrestrictedSearchResults(query)
        if brains:
            brain = brains[0]
            objpath = brain.getPath()
            anno = IDTSSettingsAnnotations(site.unrestrictedTraverse(objpath))
            request.response.setHeader(anno.getHeader(), anno.getTheme())
            break
