def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('collective.shinythings_various.txt') is None:
        return

    # Add additional setup code here

import codecs
import os

from App.class_init import InitializeClass
from App.special_dtml import DTMLFile
from OFS.Image import File
from zope.contenttype import guess_content_type

from Products.CMFCore.DirectoryView import registerFileExtension
from Products.CMFCore.DirectoryView import registerMetaType
from Products.CMFCore.FSObject import FSObject
from Products.CMFCore.permissions import FTPAccess
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ViewManagementScreens
from Products.CMFCore.utils import _checkConditionalGET
from Products.CMFCore.utils import _dtmldir
from Products.CMFCore.utils import _FSCacheHeaders
from Products.CMFCore.utils import _setCacheHeaders
from Products.CMFCore.utils import _ViewEmulator
from Products.CMFCore.FSFile import FSFile


InitializeClass(FSFile)

registerFileExtension('ttf', FSFile)
registerFileExtension('svg', FSFile)
registerFileExtension('woff', FSFile)
registerFileExtension('eot', FSFile)