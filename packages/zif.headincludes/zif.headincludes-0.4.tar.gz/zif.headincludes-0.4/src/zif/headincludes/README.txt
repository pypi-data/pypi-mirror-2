================
zif.headincludes
================

This is a wsgi middleware application intended for use with
paste.deploy, zope.paste, and zope3.

It serves as a wsgi filter to create on-the-fly &lt; script> and
&lt;style> tags inside the &lt;head> of HTML documents.  It was designed
for output from a Zope3 application, but the wsgi filter itself, in
headincluder.py, has no Zope3 dependencies.

The idea is that subobjects of a document may separately need special
resources, but it is difficult to know whether a resource is asked for
multiple times when documents are dynamically generated.  For Zope3,
headincludes replaces the functionality of zc.resourcelibrary, which
also implements this idea. In fact, mostly because headincludes
"borrows" code from zc.resourcelibrary, they may be installed
side-by-side, but only one can be used at a time, because they both
implement &lt;zope:resourceLibrary> tags for zcml and the
&lt;tal:resource_library> statement for PageTemplates.

headincludes works by creating a key in the wsgi environment,
'wsgi.html.head.includes' that is a list of urls that need to be
referenced in the head of the HTML document for the current request. 
The application registers a need for the reference by appending the url
for the reference to the list.  Urls that end in ".css" and ".js" in
that list trigger the middleware to insert &lt;style> or &lt;script>
tags into the &lt;head> of the document after the application is done
creating the HTML.

headincludes tries to maintain as much compatibility as possible with
zc.resourcelibrary.  The need() function has been rewritten, and using
the headincludes version will be a simple matter of changing the import
statement. The &lt;tal:resource_library> statement is also still
functional.

One new thing headincludes allows is arbitrary includes without needing
to register the resource.  urls can be placed in the includes list at
any time that request.environ can be accessed.  Just append any desired
url to the list, e.g.,

::

  try:
      request.environ['wsgi.html.head.includes'].append('/scripts/my_url.js')
  except KeyError:
      (handle case when the filter is not available)

Alternatively, headincludes has a utility that provides IHeadIncludeRegistration:

::

  from zope.component import getUtility
  from zif.headincludes.interfaces import IHeadIncludeRegistration
  registrar = getUtility(IHeadIncludeRegistration)
  if registrar:
      registrar.register('scripts/my_url.js')


Dependencies
------------

For zope3, headincludes requires Sidnei da Silva's zope.paste

zope.paste is available at http://svn.zope.org/zope.paste/trunk/

::

    cd [path.to.zope3.src.directory]/zope
    svn co http://svn.zope.org/zope.paste/trunk/ paste

Instructions for zope.paste are at http://awkly.org/

zope.paste requires paste.deploy.  paste.deploy can be obtained from the cheese
shop.  Presuming you have setuptools installed,

::

    sudo easy_install.py PasteDeploy

This (headincludes) package can be unzipped and installed anywhere on the Python
path.


Setup
-----

Follow Sidnei's instructions for setting up zope.paste. It involves
putting the usual zope.paste-configure.zcml file in [zope3 instance]/etc/site-packages.
There is also a parameter to change in [zope3 instance]/etc/zope.conf. 
The new twist is a paste.ini file in [zope3 instance]/etc

For Zope3, copy the headincludes-configure.zcml and
headincludes-meta.zcml files into [zope3 instance]/etc/package-includes
directory.

An example paste.ini file looks like:

::

    [pipeline:Paste.Main]
    pipeline = gzipper headincludes main

    [app:main]
    paste.app_factory = zope.paste.application:zope_publisher_app_factory

    [filter:gzipper]
    paste.filter_factory=gzipper.gzipper:filter_factory
    compress_level=6
    nocompress=jp gz zip
    tempfile=0

    [filter:headincludes]
    paste.filter_factory=zif.headincludes.headincluder:filter_factory
    location=top


Configuration
-------------

The paste.ini file above shows an example of the configuration option for
headincludes

- **location** is where in the &lt;head> you want the new tags.  "top" is the
  default, and places the new script and/or style tags just after the &lt;head>
  element.  Any other value will place the tags just before the &lt;/head> tag.
