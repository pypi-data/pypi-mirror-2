## Controller Validator "prefs_files_zip_form_validate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Validates PloneFilesZip preferences form
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
# $Id: prefs_files_zip_form_validate.vpy 31831 2006-10-16 09:12:21Z glenfant $

import codecs
translate = context.translate
charset_err_msg = "Please enter a valid charset name."

def mytranslate(label):
   return translate(label, default=label, domain='plonefileszip')

# Validating the charset
zipCharset = context.REQUEST.get('zipCharset', None)

if not zipCharset:
   state.setError('zipCharset', mytranslate(charset_err_msg))
else:
   try:
      dummy = codecs.lookup(zipCharset)
   except LookupError, e:
      state.setError('zipCharset', mytranslate(charset_err_msg))

if state.getErrors():
   state.setStatus('failure')
   return state.set(portal_status_message="Please correct the indicated errors.")

# No errors.
return state
