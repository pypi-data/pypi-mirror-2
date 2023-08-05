collective.annotationbrowser
============================

This package allows to browse zope.annotation based items. Package provides
"ann_view" browser view which lists all available (and allowed) annotation
keys and their values.

By default, all annotation keys are shown. It is possible to define blacklist
and whitelist. Go to /Plone Site/manage_propertiesForm and add
'annbrowser.blacklist' and/or 'annbrowser.whitelist' properties (type: list).
If no whitelist is defined, .* is used. There is no blacklist by default.

Annotation editor
-----------------

Page /ann_edit allows site manager to edit basic annotation values (strings,
integers and floats currently).
