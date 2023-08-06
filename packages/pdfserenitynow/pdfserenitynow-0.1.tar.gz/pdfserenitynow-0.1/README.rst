PDF Serenity Now
==========================

PDF Serenity Now was born from my increasing contact with annoying PDFs. The
biggest culprit is multi-layered PDFs which take forever to print, if you can
get them to print at all. I created the original script to convert these PDFs
to a more printer-friendly format (for the KIP series of plotters), namely
flattened TIF Group 4. I can also use a JPG version of PDFs for easy viewing on
our web-based content management system.

At this time, it converts a folder of PDFs to a folder of TIFs. It handles
large, crappy, multi-layer PDFs if you have enough RAM. ImageMagic does all of
the hard work.

In the future it will be smarter about converting and offer more target
formats. The ultimate goal is a service where users can upload/submit a crappy
PDF and have nice sets of TIFs and JPGs returned to them or put into their
destination of choice. It will have a web control panel where you can monitor
and manipulate conversions in progress or in a queue.

Credits
-------

- `Distribute`_
- `ImageMagick`_
- `modern-package-template`_
- `Pdftk`_

.. _`Distribute`: http://pypi.python.org/pypi/distribute
.. _`ImageMagick`: http://www.imagemagick.org/
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
.. _`Pdftk`: http://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/

