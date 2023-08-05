
First, getting the "test bed" up and running

    >>> from os.path import join
    >>> import StringIO
    >>> from plone.oofill.tests import getTestfilesDir
    >>> dirpath = getTestfilesDir()

We grab the OOFill utility

    >>> from zope.component import queryUtility
    >>> from plone.oofill.interfaces import IOOFillEngine
    >>> IOOFillEngine
    <InterfaceClass plone.oofill.interfaces.IOOFillEngine>
    >>> engine = queryUtility(IOOFillEngine)
    >>> engine
    <plone.oofill.oofillengine.OOFillEngine object at ...>
    
Try to do the filling.
    
    >>> odtfile = file(join(dirpath, "test1.odt"))
    >>> odtfile
    <open file '...', mode 'r' at ...>
    >>> odtlen = len(odtfile.read())
    >>> odtfile.seek(0)
    
    >>> class MyView: pass
    
    >>> outfile = engine.fillFromObject(odtfile, MyView())
    >>> outfile
    <StringIO.StringIO instance at ...>
    
    >>> outfile.len == odtlen
    True

