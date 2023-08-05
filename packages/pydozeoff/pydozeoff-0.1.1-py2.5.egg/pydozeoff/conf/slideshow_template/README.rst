pydozeoff
=========

pydozeoff is a web application written in `Python`_ that generates web-based
presentations.

As a Linux user, I don't have access to so called "professional" presentation
softwares such as Apple Keynote or MS PowerPoint. OpenOffice Impress used to be
my first choice, but I gave up using it since it's a memory/processor hog for
medium-sized presentations.

After a little research, I came across a wonderful tool called `S5`_. It was a
perfect fit, except for the one-big-fat-presentation-html thing and the lack of
syntax highlighting.

This is what I'm trying to solve with this project. So, in other words,
pydozeoff is just a web-based presentation engine for programmers.


:Author: Daniel Fernandes Martins <daniel@destaquenet.com>
:Company: `Destaquenet Technology Solutions`_


Features
--------

* Dynamic slides with `Jinja2`_ template engine
* Syntax highlighting with `Pygments`_
* Each-slide-is-a-file approach
* Play nice with version control systems
* Configurable slide directory structure with support for nested subdirectories
* Uses `S5`_ template model by default, but you can easily make it compatible
  with virtually any web-based presentation engine


Dependencies
------------

* `Python`_ 2.5+
* `Jinja2`_ template engine
* `Pygments`_ syntax highlighter
* `Bottle`_ web framework


Usage
-----

First, run ``easy_install -U pydozeoff`` to install the latest stable
release.


Starting a presentation
```````````````````````

Run ``pydozeoff -c "<PRESENTATION_NAME>"`` to start a new presentation. This
will create a ``presentation_name`` folder in the working directory. This is
what you'll find there:

media/
   All files placed here are served by the web server under the ``/media/``
   namespace. For example, you can access ``company_logo.png`` at
   http://host:port/media/company_logo.png.

slides/
   This is where you put the slides for your presentation. You can nest them
   in as many subdirectories (or sections) as you want.

themes/
   This is where you put the theme used by your presentation. This directory
   also holds a HTML template ready for use with `S5`_.

slideshow.py
   Slideshow configuration module.


Serving a presentation
``````````````````````

Use the ``pydozeoff`` command to serve the presentation::

    $ cd my_presentation
    $ pydozeoff


This command starts a web server which can be accessed at http://localhost:8080/.
Use ``-p <PORT>`` if you want to use a different port number::

    $ pydozeoff -p 9090


To start the presentation in debug mode::

    $ pydozeoff -d


This allows you to modify presentation's settings - and slides - and see the
results right away, without the need to restart the web server. It also prints
full stacktrace messages in case of errors.

All the previous commands will only work if you run ``pydozeoff`` from the
presentation root directory. Use ``-s <DIRECTORY>`` if you need to start
``pydozeoff`` from a different directory::

    $ pydozeoff -s /home/user/presentation/


Run ``pydozeoff -h`` to see all options available.


Configuring a presentation
``````````````````````````

The file ``slideshow.py`` contains detailed instructions on how to configure
the presentation, but here's a common workflow::

    $ cd /my/workspace
    $ pydozeoff -c my_presentation
    $ cd my_presentation
    $ pydozeoff -dp 8080


Point the browser to http://localhost:8080 to see a plain HTML document. It
looks that way because we haven't configured a theme yet.

To do that, download `S5`_ and extract the ``ui/default`` directory to
``themes``. Open the file ``slideshow.py`` and modify the ``THEME`` setting to
``"default"``::

    THEME = "default"


Refresh the browser to see the changes. Ok, now we are ready to add some slides
to our presentation.

First, create a file ``slides/first.html`` that looks like this::

    <h1>{{ TITLE }}</h1>

    <h3>{{ SPEAKER }}</h3>
    <h4>{{ COMPANY }}</h4>

    <div class="handout">
        <p>Slide notes.</p>
    </div>

Also, modify the ``SLIDES`` setting in ``slideshow.py``::

    SLIDES = slides(
        simple("first.html"),
    )


It's also a good time to modify the presentation name, speaker name, and so on::

    TITLE    = u"Are we living in the Matrix?"
    SPEAKER  = u"Morpheus"
    COMPANY  = u"Nebuchadnezzar"
    LOCATION = u"Planet Earth (what's left of it)"
    DATE     = u"2199-07-22"


Refresh the browser again to see the changes. Repeat these last steps for the
next slides.


Fine tunning a presentation
---------------------------

S5 configuration parameters
```````````````````````````

`S5`_ provides a couple of configuration parameters which you can change in
``slideshow.py``::

    CONTROL_VIS  = "hidden"    # "visible" or "hidden"
    DEFAULT_VIEW = "slideshow" # "slideshow" or "outline"


Syntax highlighting
```````````````````

To highlight source code snippets in your slides, just put the code inside a
``{% code "LANGUAGE" %}`` block::

    <h1>Some Python code</h1>

    {% code "python" %}
        class MyClass(object):
            def __init__(self): pass

        my_obj = MyClass()
    {% endcode %}


To configure the syntax highlighter behavior (see
`Pygments documentation <http://pygments.org/docs/formatters/#htmlformatter>`_
for more information)::

    SYNTAX_HIGHLIGHT_OPTIONS = {
        "style": "emacs",
    }


Dividing slides into sections
`````````````````````````````

For medium to large-sized presentations, you might want to separate slides
into sections::

    SLIDES = slides(
        simple("first.html"),       # Points to: slides/first.html
        section("intro",
            bullets("points.html"), # Points to: slides/intro/points.html
        ),
    )


Feel free to nest as many sections as you want.


Passing extra variables to a slide
``````````````````````````````````

Sometimes you don't want to hardcode data inside a slide. In those cases, just
pass them as keyword arguments to the slide definition::

    SLIDES = slides(
        simple("first.html", var1="value1"), # In your slide: {{ var1 }}
    )


If you want to make data available to all slides, just create a setting for
that::

    VAR1 = "value1" # In your slides: {{ VAR1 }}


Extending the template engine
`````````````````````````````

`Jinja2`_ allows you to extend the template engine with custom extensions,
filters and tests (see
`Jinja2 documentation <http://jinja.pocoo.org/2/documentation/>`_ for more
information)::

    TEMPLATE_ENGINE_EXTENSIONS = [
        "pydozeoff.template.ext.code",       # Provides: {% code %}
        "pydozeoff.template.ext.code_style", # Provides: {% code_highlight_css %}

        "my.custom.extension.here",
    ]

    TEMPLATE_ENGINE_FILTERS = {
        "my_filter": my_filter_function, # In your slide: {{ VALUE|my_filter }}
    }

    TEMPLATE_ENGINE_TESTS = {
        "my_test": my_test_function,     # In your slide: {{ VALUE is my_test }}
    }


Template inheritance
````````````````````

`Jinja2`_ supports template inheritance, which allows you to build a base
"skeleton" template that contains all the common elements of your slides and
defines blocks that child templates can override.

For example, create a file ``themes/slide.html``::

    <h1>{% block title %}{% endblock %}</h1>

    {% block content %}{% endblock %}

    <div class="handout">
        {% block handout %}{% endblock %}
    </div>


In your slides::

    {% extends "themes/slide.html" %}

    {% block title %}Slide title{% endblock %}

    {% block content %}
        Slide content
    {% endblock %}

    {% block handout %}
        Slide notes
    {% endblock %}


Changing the default directory structure
````````````````````````````````````````

Modify the following settings to change the way a presentation is organized::

    SLIDES_DIR = "slides"
    MEDIA_DIR  = "media"
    THEMES_DIR = "themes"


Future plans
------------

I don't have any. Sorry.


.. _Destaquenet Technology Solutions: http://www.destaquenet.com/
.. _Python: http://python.org/
.. _S5: http://meyerweb.com/eric/tools/s5/
.. _Jinja2: http://jinja.pocoo.org/2/
.. _Bottle: http://bottle.paws.de/
.. _Pygments: http://pygments.org/
