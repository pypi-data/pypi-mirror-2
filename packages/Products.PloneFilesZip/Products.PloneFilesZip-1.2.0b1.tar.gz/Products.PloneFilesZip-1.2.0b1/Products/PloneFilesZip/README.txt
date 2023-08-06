=============
PloneFilesZip
=============

By the `Ingeniweb <http://www.ingeniweb.com>`_ team.

About
=====

Adds a document action to folders (and folderish contents) that enables to
download all files and images from archetypes based contents available from that
folder in a ZIP file.

Optionally, the user may get the DC metadata of the contents that provide files
in XML-RDF format in the ZIP file.

Zip archives inner structure
============================

All files in the Zip archives are recorded in the path ::

  [rel_path "/"] content_id "/" field_id "/" file_name

All DC metadata in the Zip archives are recorded in the path ::

  [rel_path "/"] content_id ".rdf"

With :

* rel_path -- The relative path to the folderish that contains the content object.

* content_id -- The id of a content that has a FileField or ImageField.

* field_id -- The name of the FileField or ImageField.

* file_name -- The original file name (as recorded in the field). An extension
  is provided if the original filename doesn't have one.

Requirements
============

* Plone 2.0.5 or Plone 2.1 +

* Archetypes 1.3.3 +

* Any AT based content type with a FileField, ImageField, or
  AttachmentField. (ATContenTypes do the job)

Optional products
-----------------

* ATContentTypes 0.2 +, on Plone 2.0.x

* AttachmentField 1.3 + and AttachmentField based content types like PloneExFile

* LinguaPlone 0.7 +. If LinguaPlone is detected, the user downloads the files
  from contents in preferred language.

Warning
-------

FileSystemStorage users must upgrade to a version later than 2005/10/20.

Configuring
===========

After installing PloneZipFiles using the usual quick installer, you **must**
open the ``portal_fileszip`` tool in ZMI and follow the instructions from the
**Overview** tab.

You may configure from the "PloneFilesZip Settings" control panel too.

Customizing
===========

Custom fields
-------------

You can create and register your own retrivers for your custom fields. See
``retrivers.py`` to see how we handle FileFields, ImageFields and
AttachmentFields.

Basically, you just need to provide a class that implements the
'IFileRetriever' and register it like this ::

  try:
      from Products.PloneZipFiles import HAS_PLONE_FILES_ZIP
  except ImportError, e:
      HAS_PLONE_FILES_ZIP = False
  ...
  if HAS_PLONE_FILES_ZIP:
      from Products.PloneZipFiles.interfaces import IFieldRetriever
      from Products.PloneZipFiles.registry import GlobalRegistry

      class MyFieldRetriever:

          __implements__ = Products.IFieldRetriever

          field_type = 'my_field'

          def __init__(self, field, content):
              ...

          def fileName(self):
              ...

          def mimeType(self):
              ...

          def fileBody(self):
              ...

      GlobalRegistry.register(MyFieldRetriever)

See 'interfaces.py' for details about methods signatures and docs.

Custom types
------------

Most AT based content don't need to provide specific support for
PloneFilesZip. Anyway, if your content type does not support the standard AT
schema interface (means that 'your_content.Schema().fields()' does not provide
all fields), your code must include and register a custom type retriever like
this ::

  try:
      from Products.PloneZipFiles import HAS_PLONE_FILES_ZIP
  except ImportError, e:
      HAS_PLONE_FILES_ZIP = False
  ...
  if HAS_PLONE_FILES_ZIP:
      from Products.PloneZipFiles.interfaces import ITypeRetriever
      from Products.PloneZipFiles.registry import GlobalRegistry

      class MyTypeRetriever:

          __implements__ = Products.ITypeRetriever

          meta_type = 'my_type'

        def __init__(self, content):
            ...

        def getFieldRetrievers(self):
            ...

      GlobalRegistry.register(MyFieldRetriever)

See 'interfaces.py' for details about methods signatures and docs.

You can find an example of type retriever in the latest PloneArticle product.

Custom inner structure policies
-------------------------------

You can customize the way the files are organized into your zip archive.

you have to implement and register a ZipStructurePolicy class that implements a
getZipFilePath method, that builds inner file path from document container path,
file name and field path

container_path is the absolute path of the plone document where the file is
stored field_path is the relative path of the file field into the document
object

you will include in your product a plone zip policy module like this ::

    from Products.PloneFilesZip.interfaces import IZipStructurePolicy
    from Products.PloneFilesZip.policies import AbstractZipStructurePolicy, PolicyRegistry

    class MyZipStructurePolicy(AbstractZipStructurePolicy):
        '''
            The inner structure of the zip file
            corresponds to the inner structure of the objects.
        '''

        __implements__ = (IZipStructurePolicy,)

        id = 'my_policy_id'
        label = "Policy title"
        label_msgid = 'my_policy_title_i18n_msgid'
        help = "Policy help text"
        help_msgid = "my_policy_help_i18n_msgid"


        def getZipFilePath(self,
                        container_path=None,
                        file_name=None,
                        field_path=None,):
            ...

    PolicyRegistry.registerPolicy(MyZipStructurePolicy)


See 'interfaces.py' for details about methods signatures and docs.

Copyright and license
=====================

Copyright (c) 2006 Ingeniweb SAS

This software is subject to the provisions of the GNU General Public License,
Version 2.0 (GPL).  A copy of the GPL should accompany this distribution.  THIS
SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE
DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE,
MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE

See the ``.../PloneFilesZip/LICENSE`` file that comes with this product.

Testing
=======

Please read ``.../PloneFilesZipe/tests/README.txt``

Download
========

Add ``Products.PloneFilesZip`` in the ``eggs`` list of your Zope instance.


Support
=======

Mail to `Ingeniweb support <mailto:support@ingeniweb.com>`_.

`Donations <http://sourceforge.net/project/project_donations.php?group_id=74634>`_
are welcome for new features requests.

Credits
=======

* `Gilles Lenfant <mailto:gilles.lenfant@ingeniweb.com>`_, main developer
* `Arthur Albano <mailto:arthuralbano@hotmail.com>`_,
  Brasilian-Portugese translation
* `Thomas Desvenain <mailto:thomas.desvenain@ingeniweb.com>`_, policies developer

Feedback
========

Contributions are welcome too:

* Report success/problems with other File like fields and storages (please
  provide configuration info, test cases and tracebacks with bug reports).

* Provide translations for your native language.

