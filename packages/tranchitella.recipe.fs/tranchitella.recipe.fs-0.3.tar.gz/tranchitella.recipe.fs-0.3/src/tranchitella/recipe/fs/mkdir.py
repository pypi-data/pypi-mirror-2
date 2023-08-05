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
        logger = logging.getLogger(self.name)
        for target in filter(None, self.options['paths'].splitlines()):
            if not os.path.isdir(target):
                logger.info("Creating directory %s", target)
                os.mkdir(target)
        return ()

    def update(self):
        self.install()
