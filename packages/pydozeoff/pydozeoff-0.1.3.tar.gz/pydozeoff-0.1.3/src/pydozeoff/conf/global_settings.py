#-*- coding:utf-8 -*-

# Slideshow settings file

# Presentation info
TITLE    = u""
SPEAKER  = u""
COMPANY  = u""
LOCATION = u""
DATE     = u""

# Directory structure
ROOT_DIR      = "."
SLIDES_DIR    = "slides"
MEDIA_DIR     = "media"
THEMES_DIR    = "themes"

# Engine settings
THEME        = "default"
CONTROL_VIS  = "hidden"
DEFAULT_VIEW = "slideshow"

ENCODING = "utf-8"

# Syntax highlight settings
SYNTAX_HIGHLIGHT_OPTIONS = {
    "style": "default",
}

# Template engine extensions, filters and tests
TEMPLATE_ENGINE_EXTENSIONS = [
    "pydozeoff.template.ext.code",
    "pydozeoff.template.ext.code_style",
]

TEMPLATE_ENGINE_FILTERS = {}
TEMPLATE_ENGINE_TESTS = {}

# Slides
SLIDES = ()
