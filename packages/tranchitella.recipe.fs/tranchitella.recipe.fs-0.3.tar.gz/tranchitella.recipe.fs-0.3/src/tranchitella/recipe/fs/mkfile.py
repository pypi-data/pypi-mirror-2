# tranchitella.recipe.fs
# Copyright (C) 2008-2010 Tranchitella Kft. <http://tranchtella.eu>

import logging
import os


class Recipe(object):
    """Buildout recipe: tranchitella.recipe.fs:mkdir"""

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

    def install(self):
        path = self.options['path']
        template = self.options['template']
        logger = logging.getLogger(self.name)
        if not os.path.isfile(path):
            basedir, name = os.path.split(path)
            if not os.path.isdir(basedir):
                os.makedirs(basedir)
                logger.info("Creating directory %s", basedir)
            data = open(template, 'rb').read()
            options = self.options.copy()
            for k in options.keys():
                options[k] = ' '.join(options[k].split())
            open(path, 'wb').write(data % options)
            logger.info("Creating file %s from template %s", path , template)
            mode = int(self.options.get('mode', '06544'), 8)
            os.chmod(path, mode)
        return ()

    def update(self):
        self.install()
