##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""Z3c development recipes

$Id:$
"""

import os
import logging
import zc.buildout


class MkfileSetup:

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        self.mode = int(options.get('mode', '0644'), 8)
        options['content']
        self.originalPath = options['path']
        options['path'] = os.path.join(
                              buildout['buildout']['directory'],
                              self.originalPath,
                              )
        self.createPath = options.get('createpath', 'False').lower() in [
            'true', 'on', '1']
        if (    not self.createPath
            and not os.path.isdir(os.path.dirname(options['path']))
           ):
            logging.getLogger(self.name).error(
                'Cannot create file %s. %s is not a directory.',
                options['path'], os.path.dirname(options['path']))
            raise zc.buildout.UserError('Invalid Path')

    def install(self):
        path = self.options['path']
        if self.createPath:
            dirname = os.path.dirname(self.options['path'])
            if not os.path.isdir(dirname):
                logging.getLogger(self.name).info(
                    'Creating directory %s', dirname)
                os.makedirs(dirname)
        f = file(path, 'w')
        logging.getLogger(self.name).info(
            'Writing file %s', path)
        f.write(self.options['content'])

        f.close()
        os.chmod(path, self.mode)
        return path

