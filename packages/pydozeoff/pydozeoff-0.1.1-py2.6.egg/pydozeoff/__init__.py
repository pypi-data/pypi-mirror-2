#-*- coding:utf-8 -*-

"""
pydozeoff root module.
"""

import os
import sys


__version__   = "0.1.1"
__author__    = "Daniel Fernandes Martins"
__license__   = "BSD"
__copyright__ = "Copyright 2010, Destaquenet Technology Solutions"


def main():
    """Entry point for the command line tool.
    """
    parser, options = _get_cmdline_options()
    if options.create:
        _create_presentation(parser, options)
    else:
        _serve_presentation(parser, options)


def _create_presentation(parser, options):
    """Create a new presentation.
    """
    from shutil import copytree
    module_dir = os.path.dirname(__file__)
    copytree("%s/conf/slideshow_template" % module_dir, options.create)
    print >> sys.stderr, "Presentation '%s' created successfuly" % options.create


def _serve_presentation(parser, options):
    """Bootstraps the app.
    """
    _check_for_settings(parser, options)

    # Prepare environment
    sys.path.append(options.slideshow_path)
    os.environ["PYDOZEOFF_ROOT_DIR"]   = options.slideshow_path
    os.environ["PYDOZEOFF_DEBUG_MODE"] = ["","1"][options.debug]

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

def _get_cmdline_options():
    """Parses command line options.
    """
    import optparse
    parser = optparse.OptionParser()

    # Create presentation
    parser.add_option("--create", "-c", default="",
        help="create a new presentation")

    # Serve presentation
    serve = optparse.OptionGroup(parser, "Serving presentations")
    parser.add_option_group(serve)

    serve.add_option("--server-port", "-p", default="8080",
        help="port used by the webserver")
    serve.add_option("--slideshow-path", "-s", default=".",
        help="path to the presentation root directory (the one with a "
             "slideshow.py file)")
    serve.add_option("--debug", "-d", action="store_true", default=False,
        help="start server in debug mode")


    return (parser, parser.parse_args()[0])
