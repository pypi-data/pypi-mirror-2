#-*- coding:utf-8 -*-

"""
Provides a web interface to generate and serve a presentation.
"""

import os

from flask import Flask, send_from_directory

from pydozeoff.template import template_engine
from pydozeoff.conf import settings


MEDIA_NAMESPACE = "/media"
THEME_NAMESPACE = "/theme"

app = Flask(__name__.split(".")[0])

def start(port=8080, debug_mode=False):
    """Starts the server.
    """
    app.debug = debug_mode
    app.run(host="0.0.0.0", port=port, use_reloader=debug_mode)

@app.route("/")
def index():
    """Assembles the presentation based on the slideshow settings.
    """
    slides = []
    for slide in settings["SLIDES"]:
        context = {}
        slide_filename = _get_slide_template(slide.path)
        context["content"] = template_engine.render(slide_filename, slide.options)
        context.update(slide.options)
        slides.append(context)
    return template_engine.render(_get_slideshow_template(), locals())


@app.route("%s/<path:file_path>" % MEDIA_NAMESPACE)
def serve_media(file_path):
    """Serves static files from the media directory.
    """
    root_dir = os.path.abspath("%(ROOT_DIR)s/%(MEDIA_DIR)s" % settings)
    return send_from_directory(root_dir, file_path)

@app.route("%s/<path:file_path>" % THEME_NAMESPACE)
def serve_theme(file_path):
    """Serves static files from the theme directory.
    """
    root_dir = os.path.abspath("%(ROOT_DIR)s/%(THEMES_DIR)s/%(THEME)s" % settings)
    return send_from_directory(root_dir, file_path)

def _get_slideshow_template():
    """Returns the slideshow template file.
    """
    return "%(THEMES_DIR)s/template.html" % settings

def _get_slide_template(slide_partial_path):
    """Returns the path for the given relative path.
    """
    path = "%s/%s" % (settings["SLIDES_DIR"], slide_partial_path)
    return os.path.normpath(path).replace(os.sep, "/")
