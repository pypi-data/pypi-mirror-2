collective.setuphelpers
=======================

This package provides a few simple functions with common tasks used with initial
site content setup.

This does not aim to be as general as possible but it may speed things up.

>>> from collective.setuphelpers.structure import setupStructure
>>> portal = layer['portal']
>>> STRUCTURE = [{'id':'example-id','title':'Example title','type':'Document'}]
>>> setupStructure(portal, STRUCTURE)
>>> portal['example-id']
<ATDocument at /plone/example-id>
>>> portal.manage_delObjects(['example-id'])

You can use subfolders etc.

>>> setupStructure(portal, layer['test_structure'])
>>> portal['testfolder']['item1'].getText()
'<p>Text body</p>'

And many more - the readme will be improved with the next prerelease
