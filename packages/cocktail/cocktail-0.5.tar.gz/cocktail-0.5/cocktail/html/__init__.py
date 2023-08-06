#-*- coding: utf-8 -*-
u"""
Provides classes for building reusable (X)HTML components.

This package supplies all the necessary building blocks to create visual
components that can be easily composited, inherited and overlayed to maximize
code reuse in the presentation layer.

Some of its most notable features include:

* Components can be written in plain python or in XML
* Handles dependencies on client side scripts and stylesheets
* Integration with jQuery
* Support for multiple rendering modes (HTML4, XHTML)

Also, an extensive set of ready made components is provided as well, covering a
wide assortment of needs: forms, tables, calendars, etc.
"""
from cocktail.html.element import (
    Element,
    Content,
    PlaceHolder,
    get_current_renderer
)
from cocktail.html.resources import Resource, Script, StyleSheet
from cocktail.html.renderers import HTML4Renderer, HTML5Renderer, XHTMLRenderer
from cocktail.html.overlay import Overlay
from cocktail.html.utils import (
    alternate_classes,
    first_last_classes,
    html5_tag,
    html5_attr,
    escape_attrib
)

