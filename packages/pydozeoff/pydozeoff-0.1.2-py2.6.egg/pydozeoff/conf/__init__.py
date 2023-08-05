#-*- coding:utf-8 -*-

"""
Provides classes to handle slideshow settings.
"""

import os

import pydozeoff
from pydozeoff.conf import global_settings

# Slideshow settings
import slideshow as _slideshow_settings


class LazySettings(dict):
    """Implements the slideshow settings dictionary.
    """
    def __init__(self):
        self.initialized = False

    def initialize(self):
        """Initializes this object if it's not yet initialized.
        """
        if not self.initialized:
            self.initialized = True
            self._copy_members(global_settings)
            self._copy_members(_slideshow_settings)
            self._copy_env()


    def _copy_members(self, module):
        """Copies public members from a module to this settings object.
        """
        for name in dir(module):
            if name.startswith("_"):
                continue
            self[name] = getattr(module, name)

    def _copy_env(self):
        """Copies important environment variables to this settings object.
        """
        self["VERSION"] = pydozeoff.__version__
        self["ROOT_DIR"]   = os.environ.get("PYDOZEOFF_ROOT_DIR", ".")
        self["DEBUG_MODE"] = bool(os.environ.get("PYDOZEOFF_DEBUG_MODE", ""))

    def __getitem__(self, item):
        """Returns the corresponding setting, and initialize this object if
        necessary.
        """
        self.initialize()
        return super(LazySettings, self).__getitem__(item)


settings = LazySettings()
