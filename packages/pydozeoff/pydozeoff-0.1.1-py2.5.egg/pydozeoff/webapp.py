#-*- coding:utf-8 -*-

"""
Provides a web interface to generate and serve a presentation.
"""

from bottle import route, send_file, run, debug

from pydozeoff.template import template_engine
from pydozeoff.conf import settings


def start(port=8080, debug_mode=False):
    """Starts the server.
    """
    if debug_mode: debug(True)
    run(host="0.0.0.0", port=port, reloader=debug_mode)


@route("/")
def index():
    """Assembles the presentation based on the slideshow settings.
    """
    slides = []
    for slide in settings["SLIDES"]:
        context = {}
        slide_filename = _get_slide_template(slide.name)
        context["content"] = template_engine.render(slide_filename, slide.options)
        context.update(slide.options)
        slides.append(context)
    return template_engine.render(_get_slideshow_template(), locals())


@route('/media/(?P<filename>.+)')
def serve_media(filename):
    """Serves static files from the media directory.
    """
    send_file(filename, root="%(ROOT_DIR)s/%(MEDIA_DIR)s" % settings)


@route('/theme/(?P<filename>.+)')
def serve_template_media(filename):
    """Serves static files from the theme directory.
    """
    send_file(filename, root="%(ROOT_DIR)s/%(THEMES_DIR)s/%(THEME)s" % settings)


def _get_slideshow_template():
    """Returns the slideshow template file.
    """
    return "%(THEMES_DIR)s/template.html" % settings

def _get_slide_template(slide_partial_path):
    """Returns the path for the relative.
    """
    return "%s/%s" % (settings["SLIDES_DIR"], slide_partial_path)
