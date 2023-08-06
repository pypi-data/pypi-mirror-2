Introduction
============
This package provides some nice integrations for PDF heavy web sites.

* Generates thumbnails from PDF
* Adds folder view for pdfs so it can use the generated thumbnail
* Adds OCR for PDF indexing
* Everything configurable so you can choose to not use thumbnail gen or OCR
* use the `@@async-monitor` url to monitor asynchronous jobs that have yet to run


OCR
---

OCR requires Ghostscript to be installed and Tesseract. Just you package management
to install these packages:

  # sudo port install ghostscript tesseract
  
  
Extra
-----

You can convert all at once by calling the url `@@queue-up-all`.

