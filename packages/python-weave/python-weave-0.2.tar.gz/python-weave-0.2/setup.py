####################### BEGIN LICENSE BLOCK #############################
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is Weave Python Client.
#
# The Initial Developer of the Original Code is Mozilla Corporation.
# Portions created by the Initial Developer are Copyright (C) 2009 the Initial
# Developer. All Rights Reserved.
#
# Contributor(s):
#  Michael Hanson <mhanson@mozilla.com> (original author)
#
# Alternatively, the contents of this file may be used under the terms of either
# the GNU General Public License Version 2 or later (the "GPL"), or the GNU
# Lesser General Public License Version 2.1 or later (the "LGPL"), in which case
# the provisions of the GPL or the LGPL are applicable instead of those above.
# If you wish to allow use of your version of this file only under the terms of
# either the GPL or the LGPL, and not to allow others to use your version of
# this file under the terms of the MPL, indicate your decision by deleting the
# provisions above and replace them with the notice and other provisions
# required by the GPL or the LGPL. If you do not delete the provisions above, a
# recipient may use your version of this file under the terms of any one of the
# MPL, the GPL or the LGPL.
#
###################### END LICENSE BLOCK ############################

try:
    from setuptools import setup
    extras = {'install_requires': ['M2Crypto', 'unittest2', 'redis'],
              'zip_safe': False}
except ImportError:
    from distutils.core import setup
    extras = {}

f = open('README')
try:
    README = f.read()
finally:
    f.close()

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
    ('License :: OSI Approved :: GNU Library or Lesser General Public '
     'License (LGPL)'),
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules']

setup(name='python-weave',
      author='Mike Hanson',
      author_email='mhanson@mozilla.com',
      version='0.2',
      url='http://wiki.mozilla.org/Labs/Weave',
      description='A Mozilla Weave client for Python',
      long_description=README,
      packages=['weave', 'weave.tests', 'weave.server'],
      classifiers=classifiers,
      **extras
      )

