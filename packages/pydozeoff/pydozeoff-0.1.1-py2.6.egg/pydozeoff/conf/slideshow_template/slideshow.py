#-*- coding:utf-8 -*-

"""
Slideshow settings file.
"""

# Slide definition shortcuts. See "SLIDES" below for more information
from pydozeoff.conf.slide import *


# If you want to see all settings available and their default values, please
# import the "global_settings" module, like this:
#
#     >>> from pydozeoff.conf import global_settings
#     >>> dir(global_settings)
#     ...list of settings...
#     >>> global_settings.DEFAULT_VIEW
#     'slideshow'


# All settings defined in this file are exposed to slide templates

# Presentation info
TITLE    = u"Presentation title"
SPEAKER  = u"Author name"
COMPANY  = u"Company"
LOCATION = u"Location"
DATE     = u"yyyy-mm-dd"

# Feel free to add your own settings
MY_SETTING = "Some text here!"

# Copy a S5 theme to the "themes" directory and change this setting accordingly
# Visit http://meyerweb.com/eric/tools/s5/ for more information
THEME = "some_theme"

# Presentation slides
SLIDES = slides(

    # Each entry points to a file under the "slides" directory
    # simple("first.html"),

    # There are shortcut functions to the most common slide types. All they do
    # is add style classes to the slide <div>, so you might need to tweak the
    # CSS files of your theme to handle them properly

    # bullets("file.html"), # For bullet point slides
    # simple ("file.html"), # For short text sentences
    # image  ("file.html"), # For images
    # code   ("file.html"), # For source code snippets

    # You can use keyword args to complement the slide template context
    # bullets("second.html", custom_title="Configurable title"),

    # You can also separate your slides into subdirectories, to keep them
    # organized. Feel free to nest as many sections as you want
    # section("subsection",
    #     code ("first.html"),
    #     image("second.html"),
    # ),
)
