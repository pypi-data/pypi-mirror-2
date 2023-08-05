#-*- coding:utf-8 -*-

"""
Provides a template renderer implementation.
"""

from jinja2 import Environment, Template, FileSystemLoader

from pydozeoff.conf import settings


class Jinja2TemplateEngine(object):
    """Jinja2-based template engine.
    """
    def __init__(self):
        self.initialized = False

    def initialize(self):
        """Initializes the template engine.
        """
        if not self.initialized:
            self.initialized = True
            self.env =  Environment(
                loader      = FileSystemLoader(settings["ROOT_DIR"]),
                extensions  = settings["TEMPLATE_ENGINE_EXTENSIONS"],
                auto_reload = settings["DEBUG_MODE"],
            )
            self.env.globals = settings

            self.env.filters.update(settings["TEMPLATE_ENGINE_FILTERS"])
            self.env.tests.update(settings["TEMPLATE_ENGINE_TESTS"])

    def render(self, template_file, context={}):
        """Renders a template.
        """
        template = self.get_template(template_file)
        return template.render(context)

    def get_template(self, template_file):
        """Creates a template object from a file.
        """
        self.initialize()
        return self.env.get_template(template_file)


template_engine = Jinja2TemplateEngine()
