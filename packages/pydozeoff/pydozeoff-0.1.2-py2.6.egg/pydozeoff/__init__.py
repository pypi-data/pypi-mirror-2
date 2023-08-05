#-*- coding:utf-8 -*-

"""
pydozeoff root module.
"""

import os
import shutil
import sys


__version__   = "0.1.2"
__author__    = "Daniel Fernandes Martins"
__license__   = "BSD"
__copyright__ = "Copyright 2010, Destaquenet Technology Solutions"


def main():
    """Entry point for the command line tool.
    """
    parser, options = _get_cmdline_options()
    if options.create:
        _create_presentation(parser, options)
    elif options.build:
        _build_presentation(parser, options)
    else:
        _serve_presentation(parser, options)


def _create_presentation(parser, options):
    """Create a new presentation.
    """
    module_dir = os.path.dirname(__file__)
    shutil.copytree("%s/conf/slideshow_template" % module_dir, options.create)
    print >> sys.stderr, "Presentation '%s' created successfuly" % options.create


def _build_presentation(parser, options):
    """Builds an offline version of a presentation.
    """
    _check_for_settings(parser, options)
    _prepare_env(options)

    from pydozeoff import webapp
    settings = webapp.settings

    # Sanity checks
    if os.path.exists(options.build):
        if os.path.isfile(options.build):
            print >> sys.stderr, "Output directory '%s' must not be a file" % options.build
            sys.exit(1)
        elif os.path.isdir(options.build):
            print >> sys.stderr, "Output directory '%s' must not already exist" % options.build
            sys.exit(1)

    # Copy theme
    theme_from = "%s/%s/%s" % (options.slideshow_path, settings["THEMES_DIR"], settings["THEME"])
    theme_to   = "%s%s" % (options.build, webapp.THEME_NAMESPACE)
    shutil.copytree(theme_from, theme_to)

    # Copy media
    media_from = "%s/%s" % (options.slideshow_path, settings["MEDIA_DIR"])
    media_to   = "%s%s" % (options.build, webapp.MEDIA_NAMESPACE)
    shutil.copytree(media_from, media_to)

    # Presentation HTML
    out = open("%s/index.html" % options.build, mode="w+")
    out.write(webapp.index().encode(settings["ENCODING"]))
    out.close()

    print >> sys.stderr, "Offline version generated at '%s'" % options.build


def _serve_presentation(parser, options):
    """Bootstraps the app.
    """
    _check_for_settings(parser, options)
    _prepare_env(options)

    from pydozeoff import webapp
    webapp.start(port=options.server_port, debug_mode=options.debug)


def _check_for_settings(parser, options):
    """Checks whether the slideshow settings module exists.
    """
    module_path = "%s/slideshow.py" % options.slideshow_path
    if not os.path.exists(module_path):
        print >> sys.stderr, "File not found: %s" % module_path
        parser.print_help()
        sys.exit(1)


def _prepare_env(options):
    """Prepares the environment.
    """
    sys.path.append(options.slideshow_path)
    os.environ["PYDOZEOFF_ROOT_DIR"]   = options.slideshow_path
    os.environ["PYDOZEOFF_DEBUG_MODE"] = ["","1"][options.debug]


def _get_cmdline_options():
    """Parses command line options.
    """
    import optparse
    parser = optparse.OptionParser()

    parser.add_option("--slideshow-path", "-s", default=".",
        help="path to the presentation root directory (the one with a "
             "slideshow.py file)")

    # Build presentation
    build = optparse.OptionGroup(parser, "Starting/building presentations")
    parser.add_option_group(build)

    build.add_option("--create", "-c", default="",
        help="start a new presentation")
    build.add_option("--build", "-b", default="",
        help="create offline version of a presentation at the given directory")

    # Serve presentation
    serve = optparse.OptionGroup(parser, "Serving presentations")
    parser.add_option_group(serve)

    serve.add_option("--server-port", "-p", default="8080",
        help="port used by the webserver")
    serve.add_option("--debug", "-d", action="store_true", default=False,
        help="start server in debug mode")

    return (parser, parser.parse_args()[0])


    return (parser, parser.parse_args()[0])
