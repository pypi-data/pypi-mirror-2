## Controller Python Script "prefs_files_zip_form_set"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Save PloneFilesZip preferences
##
# Copyright (c) 2003-2006 Ingeniweb SAS
#
# This software is subject to the provisions of the GNU General Public
# License, Version 2.0 (GPL).  A copy of the GPL should accompany this
# distribution.  THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL
# EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF TITLE, MERCHANTABILITY,
# AGAINST INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE
#
# More details in the ``LICENSE`` file included in this package.
#
# $Id: prefs_files_zip_form_set.cpy 31831 2006-10-16 09:12:21Z glenfant $

from Products.CMFCore.utils import getToolByName

portal_fileszip = getToolByName(container, 'portal_fileszip')
form = context.REQUEST.form
form['includeRDF'] = form.has_key('includeRDF')
portal_fileszip.manage_changeProperties(**context.REQUEST.form)
state.setNextAction('redirect_to:string:plone_control_panel')
return state.set(portal_status_message="Changes saved.")
