from zope.component import getUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from plone.memoize import view
import re

from Products.Archetypes.utils import OrderedDict
from Products.CMFPlone.utils import safe_unicode
from zope.annotation import IAnnotations
from collective.annotationbrowser.utils import custom_repr
from collective.annotationbrowser.browser.interfaces import IAnnotationBrowserView

VALUE_MAX_LENGTH = 150

_marker = object()

class AnnotationBrowserView(BrowserView):
    implements(IAnnotationBrowserView)

    @view.memoize_contextless
    def tools(self):
        """ returns tools view. Available items are all portal_xxxxx 
            For example: catalog, membership, url
            http://dev.plone.org/plone/browser/plone.app.layout/trunk/plone/app/layout/globals/tools.py
        """
        return getMultiAdapter((self.context, self.request), name=u"plone_tools")

    @view.memoize_contextless
    def portal_state(self):
        """ returns 
            http://dev.plone.org/plone/browser/plone.app.layout/trunk/plone/app/layout/globals/portal.py
        """
        return getMultiAdapter((self.context, self.request), name=u"plone_portal_state")

    @view.memoize
    def annotations(self):
        context = aq_inner(self.context)
        return IAnnotations(context)
        
    def num_blacklisted(self):
        ann = self.annotations()
        portal = getUtility(IPloneSiteRoot)
        blacklist = portal.getProperty('annotationbrowser.blacklist', [])
        count = 0
        for key in ann.keys():
            for bl in blacklist:
                if re.match(bl, key) is not None:
                    count += 1
                    break
        return count

    def ann_keys(self):
        ann = self.annotations()
        result = list()
        portal = getUtility(IPloneSiteRoot)
        blacklist = portal.getProperty('annbrowser.blacklist', [])
        whitelist = portal.getProperty('annbrowser.whitelist', [])
        if not whitelist:
            whitelist = ['.*',] 
                
        # process blacklist
        for key in ann.keys():
            passed = False
            for wl in whitelist:
                if re.match(wl, key) is not None:
                    passed = True
                    break
            for bl in blacklist:
                if re.match(bl, key) is not None:
                    passed = False
                    break
            if passed:
                result.append(key)
        return result

    def ann_dict(self):
        ann = self.annotations()
        result = OrderedDict()
        for key in sorted(self.ann_keys()):
            is_editable = False
            typ = 'unknown'
            value = ann.get(key, _marker)
            if value is _marker:
                value = 'N/A'
            else:
                if isinstance(value, basestring):
                    typ = 'string'
                    is_editable = True
                elif isinstance(value, int):
                    typ = 'int'
                    is_editable = True
                elif isinstance(value, float):
                    typ = 'float'
                    is_editable = True
            value = custom_repr(value)
            result[key] = dict(value = safe_unicode(value)[:VALUE_MAX_LENGTH], 
                               editable=is_editable, 
                               typ=typ)
        return result

class AnnotationBrowserEdit(BrowserView):
    
    def processForm(self):
        context = aq_inner(self.context)
        if (self.request.form.get('form.submitted', '') == '1') and self.request.form.has_key('submit'):
            ann = IAnnotations(context)
            for k, v  in self.request.form.items():
                if ann.has_key(k):
                    ann[k] = v
        self.request.response.redirect(context.absolute_url() + '/ann_view')
        