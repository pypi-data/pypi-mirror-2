HTML Slide style presetation theme for Sphinx.

Features
========
* provide ``htmlslide`` theme for render presentation.


Setup
=====
Make environment with easy_install::

    $ easy_install sphinxjp.themes.htmlslide


Convert Usage
==============
setup conf.py with::

    extensions = ['sphinxjp.themecore']
    html_theme = 'htmlslide'

and run::

    $ make html


Requirements
============
* sphinx 1.0.x or later.
* sphinxjp.themecore


Presentation Environments
==========================
* HTML5 ready browsers (Chrome, Safari)
* Non HTML5 ready browsers only show slide (no-animation)


License
=======
Licensed under the `MIT license <http://www.opensource.org/licenses/mit-license.php>`_ .
See the LICENSE file for specific terms.


