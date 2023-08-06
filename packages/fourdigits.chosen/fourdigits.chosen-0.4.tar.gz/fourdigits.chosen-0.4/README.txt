Introduction
============

This package is a Plone integration of the Chosen javascript library by Harvest.

Chosen
======
Chosen is a library for making long, unwieldy select boxes more user friendly.

jQuery support: 1.4+
Prototype support: 1.7+
For documentation, usage, and examples, see: http://harvesthq.github.com/chosen

Chosen Credits

Built by Harvest (http://www.getharvest.com/)
Concept and development by Patrick Filler (http://www.patrickfiller.com/)
Design and CSS by Matthew Lettini (http://matthewlettini.com/)

Plone integration by Roel Bruggink (http://jaroel.nl)

The jQuery based implementation is the only supported version.

Buildout
========
This repository includes a buildout.cfg which allows you to create a test
instance for this package.
1. Run:
  python26 bootstrap.py
  ./bin/buildout
  ./bin/instance
2. Add a new Plone site and select fourdigits.chosen at the 'Add-ons' section.
