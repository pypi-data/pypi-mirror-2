Produce & Publish Lite
======================

Produce & Publish Lite is a stripped down version of the Produce & Publish
platform (www.produce-and-publish.com). It implements a PDF generation
functionality for the Plone content-management system (www.plone.org).

Limitations
-----------
* supports Apache FOP 1.0 or PISA as PDF backend
* no support for the Produce & Publish server (conversion will
  take place inside Plone - may block worker threads of Zope)

Requirements
------------
* requires Plone 4 or higher (untested with Plone 3.x)

Installation
------------

* add ``zopyx.smartprintng.lite`` to the ``eggs`` option
  of your buildout.cfg and re-run buildout (as usual)
* read carefully the ``zopyx.convert2`` documentation (especially the
  section related to the configuration of Apache FOP)

Installation of Apache using ``zc.buildout``
--------------------------------------------

You can automatically install and configure Apache FOP through
your buildout configuration::

    [buildout]
    parts = 
        ...
        fop

    [instance]
    ...
    environment-vars = 
        FOP_HOME ${buildout:directory}/parts/fop


    [fop]
    recipe = hexagonit.recipe.download
    strip-top-level-dir = true
    url = http://apache.openmirror.de/xmlgraphics/fop/binaries/fop-1.0-bin.tar.gz


Usage
-----
The module supports conversion to PDF either using the FOP converter or PISA
(installed automatically).  Add ``@@asPlainPDF`` to the URL of a Plone
document, news item or topic in order to convert the current content to PDF.
This is use the default PDF converter (Apache FOP). In order to convert the
HTML content using PISA you have to use ``@@asPlainPDF?converter=pdf-pisa``.


Supplementary information
-------------------------

PDF support for your own content-types:

    http://docs.produce-and-publish.com/connector/content-types.html

Registering your own resource directories:

    http://docs.produce-and-publish.com/connector/resource-directories.html#registering-your-own-resource-directory


License
-------
Produce & Publish Lite is published under the GNU Public License V 2 (GPL 2).


Author
------

| ZOPYX Limited
| c/o Andreas Jung
| Charlottenstr. 37/1
| D-72070 Tuebingen, Germany
| www.zopyx.com
| info@zopyx.com
