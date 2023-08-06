`ikazuchi <https://bitbucket.org/t2y/ikazuchi>`_
helps to translate document using web translate APIs efficiently.
`ikazuchi` is intended to work with other tools since it's a CUI tool.

See the project `documentation <http://t2y.bitbucket.org/ikazuchi/build/html/index.html>`_ for more detail.


Features
========

* Translate GNU gettext catalog named PO file with good reference from web API
* Translate reST document file keeping with the format
* Translate any string passed from command line argument
* Translate any string in Vim using ":pyfile" command
* Detect language of any string passed from command line argument


Setup
=====

by easy_install
----------------

Make environment::

   $ easy_install ikazuchi

by buildout
-----------

Make environment::

   $ hg clone https://t2y@bitbucket.org/t2y/ikazuchi
   $ cd ikazuchi
   $ python bootstrap.py -d
   $ bin/buildout


Usage
=====

Execute ikazuchi command::

    $ ikazuchi -s "i can translate"
    sentence:                i can translate
    translated(Google):      [Actually, translated sentence]

    $ ikazuchi -d -s "hello"
    sentence:                hello
    detect(Google):          [{u'isReliable': False, u'confidence': 0.01737435, u'language': u'en'}]

All command option are::

    $ ikazuchi -h
    usage: ikazuchi [-h] [-v] [-a API] [-d] [-e ENCODING] [-f LANG] [-l]
                    [-p POFILE] [-q] [-r RSTFILE] [-s SENTENCE [SENTENCE ...]]
                    [-t LANG]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -a API, --api API     APIs are ['google', 'microsoft']
      -d, --detect          detect language for target sentence
      -e ENCODING, --encoding ENCODING
                            input/output encoding
      -f LANG, --from LANG  original language
      -l, --languages       show supported languages
      -p POFILE, --pofile POFILE
                            target po file
      -q, --quiet           not to show original sentence to stdout
      -r RSTFILE, --rstfile RSTFILE
                            target reST file
      -s SENTENCE [SENTENCE ...], --sentences SENTENCE [SENTENCE ...]
                            target sentences
      -t LANG, --to LANG    target language to translate


Requirements
============

* Python 2.6 or later
* polib 0.5.5 or later
* setuptools or distriubte


License
=======

Apache License 2.0


History
=======

0.4.1 (2011-05-31)
------------------
* upgrade enrai/raimei scripts with updated Translate API
* add setting apikey feature for Translator with configuration file
* add LICENSE file for distribution
* fixed some minor bugs

0.4.0 (2011-05-23)
------------------
* add -l(languages) option
* add -r(rst file) option
* upgrade v1 to v2 for Google Translator
* Change license to Apache License 2.0

0.3.0 (2011-02-17)
------------------
* add -d(detect) option
* add more api for Microsoft Translator
* refactor translator architecture

0.2.0 (2011-02-07)
------------------
* add -q(quiet) and -e(encoding) option

0.1.0 (2011-01-22)
------------------
* first release

