#-*- coding:utf-8 -*-

"""
pydozeoff root module.
"""

import os
import shutil
import sys


__version__   = "0.1.3"
__author__    = "Daniel Fernandes Martins"
__license__   = "BSD"
__copyright__ = "Copyright 2010, Destaquenet Technology Solutions"


def main():
    """Entry point for the command line tool.
    """
    parser, options = _get_cmdline_options()
    if options.presentation_name:
        _create_presentation(parser, options)
    elif options.output_dir:
        _build_presentation(parser, options)
    else:
        _serve_presentation(parser, options)


def _create_presentation(parser, options):
    """Create a new presentation.
    """
    module_dir = os.path.dirname(__file__)
    name = options.presentation_name

    shutil.copytree("%s/conf/slideshow_template" % module_dir, name)
    print >> sys.stderr, "Presentation '%s' created successfuly" % name


def _build_presentation(parser, options):
    """Builds an offline version of a presentation.
    """
    _check_for_settings(parser, options)
    _prepare_env(options)

    out = options.output_dir

    from pydozeoff import webapp
    settings = webapp.settings

    # Sanity checks
    if os.path.exists(out):
        if os.path.isfile(out):
            print >> sys.stderr, "Output directory '%s' must not be a file" % out
            sys.exit(1)
        elif os.path.isdir(out):
            print >> sys.stderr, "Output directory '%s' must not already exist" % out
            sys.exit(1)

    # Copy theme
    theme_from = "%s/%s/%s" % (options.slideshow_path, settings["THEMES_DIR"], settings["THEME"])
    theme_to   = "%s%s" % (out, webapp.THEME_NAMESPACE)
    shutil.copytree(theme_from, theme_to)

    # Copy media
    media_from = "%s/%s" % (options.slideshow_path, settings["MEDIA_DIR"])
    media_to   = "%s%s" % (out, webapp.MEDIA_NAMESPACE)
    shutil.copytree(media_from, media_to)

    # Presentation HTML
    html = open("%s/index.html" % out, mode="w+")
    html.write(webapp.index().encode(settings["ENCODING"]))
    html.close()

    print >> sys.stderr, "Offline version generated at '%s'" % out


def _serve_presentation(parser, options):
    """Bootstraps the app.
    """
    _check_for_settings(parser, options)
    _prepare_env(options)

    from pydozeoff import webapp
    webapp.start(port=options.port, debug_mode=options.debug)


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
    parser = optparse.OptionParser(version="%prog " + __version__)

    parser.add_option("--slideshow-path", "-s", default=".",
        help="path to the presentation root directory (the one with a "
             "slideshow.py file)")

    # Build presentation
    build = optparse.OptionGroup(parser, "Starting/building presentations")
    parser.add_option_group(build)

    build.add_option("--create", "-c", dest="presentation_name", default="",
        help="start a new presentation at PRESENTATION_NAME directory")
    build.add_option("--build", "-b", dest="output_dir", default="",
        help="create offline version of a presentation at OUTPUT_DIR")

    # Serve presentation
    serve = optparse.OptionGroup(parser, "Serving presentations")
    parser.add_option_group(serve)

    serve.add_option("--server-port", "-p", dest="port", type="int", default="8080",
        help="serve the presentation via HTTP at the given PORT")
    serve.add_option("--debug", "-d", action="store_true", default=False,
        help="whether the HTTP server should start in debug mode")

    return (parser, parser.parse_args()[0])
