##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from zif.headincludes.resourcelibrary import LibraryInfo, library_info
from zope.app import zapi
from zope.app.publisher.browser import directoryresource
from zope.app.publisher.browser.metadirectives import IBasicResourceInformation
from zope.app.publisher.browser.resourcemeta import allowed_names
from zope.configuration.exceptions import ConfigurationError
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.security.checker import CheckerPublic, NamesChecker
import os.path
import zope.configuration.fields

#Unchanged from zc.resourcelibrary

class IResourceLibraryDirective(IBasicResourceInformation):
    """
    Defines a resource library
    """

    name = zope.schema.TextLine(
        title=u"The name of the resource library",
        description=u"""\
        This is the name used to disambiguate resource libraries.  No two
        libraries can be active with the same name.""",
        required=True,
        )

    require = zope.configuration.fields.Tokens(
        title=u"Require",
        description=u"The resource libraries on which this library depends.",
        required=False,
        value_type=zope.schema.Text(),
        )


class IDirectoryDirective(Interface):
    """
    Identifies a directory to be included in a resource library
    """

    source = zope.configuration.fields.Path(
        title=u"Source",
        description=u"The directory containing the files to add.",
        required=True,
        )

    include = zope.configuration.fields.Tokens(
        title=u"Include",
        description=u"The files which should be included in HTML pages which "
                    u"reference this resource library.",
        required=False,
        value_type=zope.schema.Text(),
        )


#leaving the old code for the moment
#def handler(name, dependencies, *provideAdapterArgs):
def handler(name, dependencies, required,provided,adapter_name,factory,info=''):
    if dependencies:
        for dep in dependencies:
            if dep not in library_info:
                raise ConfigurationError(
                    'Resource library "%s" has unsatisfied dependency on "%s".'
                    % (name, dep))
    zapi.getGlobalSiteManager().registerAdapter(
        factory, required, provided, adapter_name, info)
#zapi.getGlobalSiteManager().provideAdapter(*provideAdapterArgs)


INCLUDABLE_EXTENTIONS = ('.js', '.css')

class ResourceLibrary(object):

    def __init__(self, _context, name, require=(),
                 layer=IDefaultBrowserLayer, permission='zope.Public'):
        self.name =  name
        self.layer = layer

        if permission == 'zope.Public':
            permission = CheckerPublic
        self.checker = NamesChecker(allowed_names, permission)

        # make note of the library in a global registry
        library_info[name] = LibraryInfo()
        library_info[name].required.extend(require)

    def directory(self, _context, source, include=()):
        if not os.path.isdir(source):
            raise ConfigurationError("Directory %r does not exist" % source)

        for file_name in include:
            ext = os.path.splitext(file_name)[1]
            if ext not in INCLUDABLE_EXTENTIONS:
                raise ConfigurationError(
                    'Resource library doesn\'t know how to include this '
                    'file: "%s".' % file_name)

        # remember which files should be included in the HTML when this library
        # is referenced
        library_info[self.name].included.extend(include)

        factory = directoryresource.DirectoryResourceFactory(
            source, self.checker, self.name)

        _context.action(
            discriminator = ('resource', self.name, IBrowserRequest, self.layer),
            callable = handler,
            args = (self.name, library_info[self.name].required, (self.layer,),
                    Interface, self.name, factory, _context.info),
            )
