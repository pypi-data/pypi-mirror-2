#-*- coding:utf-8 -*-

"""
Most common slide types.
"""

__all__ = ["slides", "section", "simple", "bullets", "code", "image",]

def slides(*elements):
    """Defines the sequence of slides for the presentation.
    """
    return _collect_slides(elements, [])

def _collect_slides(elements, current):
    """Recursively collects all slides.
    """
    for element in elements:
        if isinstance(element, Slide):
            current.append(element)
        elif isinstance(element, Section):
            _collect_slides(element.elements, current)
    return current


def section(name, *elements):
    """Defines a parent section, which is just a parent directory.
    """
    return Section(name, *elements)

def simple(filename, **kwargs):
    """Defines a slide composed of a couple lines of text.
    """
    opt = {"classes": "simple"}; opt.update(kwargs)
    return Slide(filename, **opt)

def bullets(filename, **kwargs):
    """Configures a slide composed of bullet points.
    """
    opt = {"classes": "bullets"}; opt.update(kwargs)
    return Slide(filename, **kwargs)

def code(filename, **kwargs):
    """Configures a slide composed of source code snippets.
    """
    opt = {"classes": "code"}; opt.update(kwargs)
    return Slide(filename, **opt)

def image(filename, **kwargs):
    """Configures a slide that displays a image.
    """
    opt = {"classes": "image"}; opt.update(kwargs)
    return Slide(filename, **opt)


class Element(object):
    def __init__(self, name):
        self._name = name
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def get_name(self):
        if not self._parent:
            return self._name
        return "%s/%s" % (self.parent.name, self._name)

    parent = property(get_parent, set_parent)
    name   = property(get_name)


class Section(Element):
    def __init__(self, name, *elements):
        super(Section, self).__init__(name)
        for element in elements:
            element.set_parent(self)
        self._elements = elements

    def get_elements(self):
        return self._elements

    elements = property(get_elements)

class Slide(Element):
    def __init__(self, name, **kwargs):
        super(Slide, self).__init__(name)
        self._options = kwargs

    def get_options(self):
        return self._options

    options = property(get_options)
