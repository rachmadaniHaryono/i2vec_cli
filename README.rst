i2vec_cli
=========

Use illustration2vec.net from cli

Usage
-----

Example usage

The content of the following directive

.. code:: bash

 i2vec-cli cat.jpg
 # result
 path:cat.jpg
 [[['#', 'General Tag', 'Confidence', ''],
   ['1.', 'chibi', '', '78.5%'],
   ['2.', 'no humans', '', '37.5%'],
   ['3.', 'cat ears', '', '29.6%'],
  [['#', 'Character Tag', '', ''],
   ['1.', 'gilgamesh', '', '56.0%'],
   ['2.', 'beatrice', '', '40.8%'],
   ['3.', 'kotomine kirei', '', '24.8%']],
  [['#', 'Copyright Tag', '', ''],
   ['1.', 'fate (series)', '', '80.1%'],
   ['2.', 'fate/zero', '', '65.8%'],
   ['3.', 'umineko no naku koro ni', '', '24.6%'],
   ['4.', 'disney', '', '0.686%']],
  [['#', 'Rating', '', ''],
   ['1.', 'safe', '', '93.6%'],
   ['2.', 'questionable', '', '4.74%']]]

or using hydrus format

.. code:: bash

 i2vec-cli cat.jpg --format hydrus
 # result
 path:cat.jpg
 chibi
 no humans
 cat ears
 :3
 food
 parody
 cat
 english
 o o
 bird
 crossover
 character:gilgamesh
 character:beatrice
 character:kotomine kirei
 series:fate (series)
 series:fate/zero
 series:umineko no naku koro ni
 series:disney
 rating:safe

Starting v0.1.1 i2vec_cli also accept url as input, as example:

.. code:: bash

 i2vec-cli http://example.com/cat.jpg --format hydrus
 # result
 url:http://example.com/cat.jpg
 chibi
 no humans
 cat ears
 :3
 food
 parody
 cat
 english
 o o
 bird
 crossover
 #... etc

Starting v0.1.1 i2vec_cli accept `close delay` option so browser don't close directly after the job.
Valid options for close delay are following::

 - -1 : Script will wait till any keyboard press
 - 0 : Script will close directly (default).
 - >0 : Script will delay the close of this amount of time in seconds

Example for close-delay option:

.. code:: bash

 # wait for user input after the job done.
 i2vec-cli cat.jpg --close-delay -1
 # wait for 10 second after the job done
 i2vec-cli cat.jpg --close-delay 10

Starting v0.2.0 i2vec_cli can be used as hydrus tag parser. Here are guide for the configuration::

 - First run i2vec-cli-server
 - Notice where the server run. The example below is used when the server run on 127.0.0.1:5000.
 - Copy the code below to clipboard.
 - Open Hydrus -> 'service' menu -> 'manage parsing script' menu -> 'import' button -> 'from clipboard' menu
 - Check if the server address is the same as in the i2vec-cli-server

Parsing script code:

.. code:: json

 [32, "local i2vec", 1, ["http://127.0.0.1:5000/upload", 1, 0, 0, "file", {}, [[30, 1, ["we got sent back to main gallery page -- title test", 8, [27, 2, [[["head", {}, 0], ["title", {}, 0]], null, [0, 0, "", ""]]], [true, true, "Image List"]]], [30, 1, ["", 0, [27, 2, [[["li", {"class": "tag-type-general"}, null], ["a", {}, 1]], null, [0, 0, "", ""]]], ""]], [30, 1, ["", 0, [27, 2, [[["li", {"class": "tag-type-copyright"}, null], ["a", {}, 1]], null, [0, 0, "", ""]]], "series"]], [30, 1, ["", 0, [27, 2, [[["li", {"class": "tag-type-artist"}, null], ["a", {}, 1]], null, [0, 0, "", ""]]], "creator"]], [30, 1, ["", 0, [27, 2, [[["li", {"class": "tag-type-character"}, null], ["a", {}, 1]], null, [0, 0, "", ""]]], "character"]], [30, 1, ["we got sent back to main gallery page -- page links exist", 8, [27, 2, [[["div", {}, null]], "class", [0, 0, "", ""]]], [true, true, "pagination"]]]]]]


Installation
------------

clone the repo and pip install from this github.

.. code:: bash

   git clone https://github.com/rachmadaniHaryono/i2vec_cli
   cd i2vec_cli
   pip install .
   # or to install it explicitly with python3
   pip3 install .

Requirements
^^^^^^^^^^^^

- `click`_
- `flask`_
- `html-table-parser-python3`_
- `requests`_
- `splinter`_
- `structlog`_

Compatibility
-------------

This program work on python 3 and tested on python 3.5

FAQ
---

I got 'ImportError: No module named html.parser'?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It mean you are installing it with python 2 version. To fix it do the following:

- Uninstall the program first:

.. code:: bash

 pip uninstall .


- Reinstall the program using *pip3*

.. code:: bash

 pip3 install .


Licence
-------

This project is licensed under the MIT License - see the *LICENSE* file for details


Authors
-------

`i2vec_cli` was written by `Rachmadani Haryono <foreturiga@gmail.com>`_.

.. _`click`: https://click.pocoo.org/4/
.. _`flask`: http://flask.pocoo.org
.. _`html-table-parser-python3`: https://github.com/rachmadaniHaryono/html-table-parser-python3
.. _`requests`: https://github.com/requests/requests
.. _`splinter`: https://github.com/cobrateam/splinter
.. _`structlog`: https://github.com/hynek/structlog
.. _`splinter document about driver`: https://splinter.readthedocs.io/en/latest/
