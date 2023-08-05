.. -*-doctest-*-


============================
collective.annotationbrowser
============================

    >>> from zope.annotation import IAnnotations
    >>> from zope.publisher.browser import TestRequest
    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> from zope.interface import alsoProvides
    >>> from BTrees.OOBTree import OOBTree
    >>> from collective.annotationbrowser.browser.view import AnnotationBrowserView
    >>> from collective.annotationbrowser.browser.view import AnnotationBrowserEdit
    >>> portal = self.portal
    >>> request = TestRequest()
    >>> alsoProvides(request, IAttributeAnnotatable)
    >>> ann = IAnnotations(portal)

Test base annotation keys provided by Plone itself

    >>> view = AnnotationBrowserView(portal, request)
    >>> self.assertEqual(view.annotations(), ann)
    >>> view.ann_keys()
    ['plone.contentrules.localassignments', 'plone.portlets.contextassignments']
    >>> view = AnnotationBrowserView(portal['news'], request)
    >>> view.ann_keys()
    ['plone.contentrules.localassignments']
    
Let's add custom simple annotation key

    >>> ann = IAnnotations(portal)
    >>> ann['my.key'] = 'MY VALUE'
    >>> view = AnnotationBrowserView(portal, request)
    >>> self.failUnless('my.key' in view.ann_keys())
    >>> value = view.ann_dict()['my.key']
    >>> self.assertEqual(value['typ'], 'string')
    >>> self.assertEqual(value['value'], 'MY VALUE')
    >>> self.assertEqual(value['editable'], True)

Not so simple annotation value is not editable

    >>> ann = IAnnotations(portal)
    >>> ann['my.key'] = [1,2,3,4,5,6]
    >>> view = AnnotationBrowserView(portal, request)
    >>> value = view.ann_dict()['my.key']
    >>> self.assertEqual(value['typ'], 'unknown')
    >>> self.assertEqual(value['value'], u'[1, 2, 3, 4, 5, 6]')
    >>> self.assertEqual(value['editable'], False)

Try to edit a value

    >>> ann = IAnnotations(portal)
    >>> ann['my.key'] = ' My value'
    >>> request = TestRequest(form={'submit':'submit', 'form.submitted':'1', 'dummy':1, 'my.key':'Other value'})
    >>> view = AnnotationBrowserEdit(portal, request)
    >>> view.processForm()
    >>> ann = IAnnotations(portal)
    >>> self.assertEqual(ann['my.key'], 'Other value')

New keys must not be added to the annotations:

    >>> self.failIf('dummy' in ann.keys())

Test traverser

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> browser.handleErrors = False
    >>> self.portal.error_log._ignored_exceptions = ()

Login
    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

    >>> browser.open(portal_url + '/++annotation++plone.contentrules.localassignments')
    >>> browser.contents
    '<plone.contentrules.engine.assignments.RuleAssignmentManager object at 0x...>'

Create custom key in the annotations

    >>> IAnnotations(self.portal)['annotationbrowser.test'] = 'dummy'

Does the key exist ?     

    >>> browser.open(portal_url + '/ann_view')
    >>> 'annotationbrowser.test' in browser.contents
    True

Check the value

    >>> browser.open(portal_url + '/++annotation++annotationbrowser.test')
    >>> browser.contents
    "'dummy'"

Remove the key

    >>> browser.open(portal_url + '/ann_remove?keyname=annotationbrowser.test')

User is redirected to ann_view, so check the page

    >>> browser.open(portal_url + '/ann_view')
    >>> 'annotationbrowser.test' in browser.contents
    False

Key is gone.

    >>> IAnnotations(self.portal).has_key('annotationbrowser.test')
    False

