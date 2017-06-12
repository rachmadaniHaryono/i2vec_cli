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

Installation
------------

Pip install from this github.

.. code:: bash

    pip install git+git://github.com/rachmadaniHaryono/i2vec_cli.git

Requirements
^^^^^^^^^^^^

- `html-table-parser-python3`_
- `click`_
- `splinter`_
- `structlog`_

Compatibility
-------------

This program work on python 3 and tested on python 3.5

Licence
-------

This project is licensed under the MIT License - see the *LICENSE* file for details


Authors
-------

`i2vec_cli` was written by `Rachmadani Haryono <foreturiga@gmail.com>`_.

.. _`html-table-parser-python3`: https://github.com/rachmadaniHaryono/html-table-parser-python3
.. _`click`: https://click.pocoo.org/4/
.. _`splinter`: https://github.com/cobrateam/splinter
.. _`structlog`: https://github.com/hynek/structlog
