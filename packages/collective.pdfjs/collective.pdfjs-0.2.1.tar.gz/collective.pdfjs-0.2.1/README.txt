collective.pdfjs - Plone integration for Mozilla's JavaScript PDF reader
========================================================================

Introduction
============

This product adds pdf.js support for Plone.

When installed, it will provide an additional view for the File content-type.

If the view detects a PDF file, it will attempt to render it inline using
pdf.js. If the user browser doesn't have JavaScript enabled, it will embed
any available PDF reader plugin (Acrobat's, Google Chrome native, etc).

To know more about the integrated PDF renderer/viewer, see:

.. _PDF.js Repository: https://github.com/andreasgal/pdf.js

Support
=======

Right now pdf.js has rudimentary support for PDFs, so a lot of them might not
render correctly or even work at all. Development is moving ahead fast, so
expect improvements in the near future.
