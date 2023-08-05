##############################################################################
#
# Copyright (c) 2001 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
""" Customizable properties that come from the filesystem.

$Id: FSPropertiesObject.py 110577 2010-04-07 06:33:17Z jens $
"""

from AccessControl.SecurityInfo import ClassSecurityInfo
from Acquisition import ImplicitAcquisitionWrapper
from App.class_init import InitializeClass
from App.special_dtml import DTMLFile
import Globals  # for data
from OFS.Folder import Folder
from OFS.PropertyManager import PropertyManager
from ZPublisher.Converters import get_converter

from Products.CMFCore.DirectoryView import registerFileExtension
from Products.CMFCore.DirectoryView import registerMetaType
from Products.CMFCore.FSObject import FSObject
from Products.CMFCore.permissions import ViewManagementScreens
from Products.CMFCore.utils import _dtmldir


class FSPropertiesObject(FSObject, PropertyManager):

    """FSPropertiesObjects simply hold properties."""

    meta_type = 'Filesystem Properties Object'

    manage_options = ({'label':'Customize', 'action':'manage_main'},)

    security = ClassSecurityInfo()

    security.declareProtected(ViewManagementScreens, 'manage_main')
    manage_main = DTMLFile('custprops', _dtmldir)

    # Declare all (inherited) mutating methods private.
    security.declarePrivate('manage_addProperty')
    security.declarePrivate('manage_editProperties')
    security.declarePrivate('manage_delProperties')
    security.declarePrivate('manage_changeProperties')
    security.declarePrivate('manage_propertiesForm')
    security.declarePrivate('manage_propertyTypeForm')
    security.declarePrivate('manage_changePropertyTypes')

    security.declareProtected(ViewManagementScreens, 'manage_doCustomize')
    def manage_doCustomize(self, folder_path, RESPONSE=None, \
                           root=None, obj=None):
        """Makes a ZODB Based clone with the same data.

        Calls _createZODBClone for the actual work.
        """
        # Overridden here to provide a different redirect target.

        FSObject.manage_doCustomize(self, folder_path, RESPONSE, \
                                    root=root, obj=obj)

        if RESPONSE is not None:
            if folder_path == '.':
                fpath = ()
            else:
                fpath = tuple(folder_path.split('/'))
            folder = self.restrictedTraverse(fpath)
            RESPONSE.redirect('%s/%s/manage_propertiesForm' % (
                folder.absolute_url(), self.getId()))

    def _createZODBClone(self):
        """Create a ZODB (editable) equivalent of this object."""
        # Create a Folder to hold the properties.
        obj = Folder()
        obj.id = self.getId()
        map = []
        for p in self._properties:
            # This should be secure since the properties come
            # from the filesystem.
            setattr(obj, p['id'], getattr(self, p['id']))
            map.append({'id': p['id'],
                        'type': p['type'],
                        'mode': 'wd',})
        obj._properties = tuple(map)

        return obj

    def _readFile(self, reparse):
        """Read the data from the filesystem.
        """
        file = open(self._filepath, 'r') # not 'rb', as this is a text file!
        try:
            lines = file.readlines()
        finally:
            file.close()

        map = []
        lino=0

        for line in lines:

            lino = lino + 1
            line = line.strip()

            if not line or line[0] == '#':
                continue

            try:
                propname, proptv = line.split(':',1)
                #XXX multi-line properties?
                proptype, propvstr = proptv.split( '=', 1 )
                propname = propname.strip()
                proptype = proptype.strip()
                propvstr = propvstr.strip()
                converter = get_converter( proptype, lambda x: x )
                propvalue = converter( propvstr )
                # Should be safe since we're loading from
                # the filesystem.
                setattr(self, propname, propvalue)
                map.append({'id':propname,
                            'type':proptype,
                            'mode':'',
                            'default_value':propvalue,
                            })
            except:
                raise ValueError, ( 'Error processing line %s of %s:\n%s'
                                  % (lino,self._filepath,line) )
        self._properties = tuple(map)

    if Globals.DevelopmentMode:
        # Provide an opportunity to update the properties.
        def __of__(self, parent):
            self = ImplicitAcquisitionWrapper(self, parent)
            self._updateFromFS()
            return self

InitializeClass(FSPropertiesObject)

registerFileExtension('props', FSPropertiesObject)
registerMetaType('Properties Object', FSPropertiesObject)
