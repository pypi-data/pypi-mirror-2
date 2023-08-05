#!/usr/bin/python
# -*- coding: utf-8 -*-

from megrok import resource
from hurry.slimbox import slimbox


class ImagePopup(resource.ResourceLibrary):
    resource.path('resources')
    resource.name("image.popup")
    resource.resource("popup.js", depends=[slimbox])
