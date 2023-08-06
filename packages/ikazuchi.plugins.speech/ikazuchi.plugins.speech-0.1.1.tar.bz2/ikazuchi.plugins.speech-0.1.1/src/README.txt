`ikazuchi.plugins.speech <https://bitbucket.org/t2y/ikazuchi.plugins.speech>`_
is plugin for `ikazuchi <https://bitbucket.org/t2y/ikazuchi>`_ to provide
Text to Speech feature.

`ikazuchi` is intended to work with other tools since it's a CUI tool.

See the project `documentation <http://t2y.bitbucket.org/ikazuchi/build/html/index.html>`_ for more detail.

Features
========

* Provide Text to Speech feature for given text or translated text

Setup
=====

by easy_install
----------------

Make environment::

   $ easy_install ikazuchi.plugins.speech

by buildout
-----------

Make environment::

   $ hg clone https://bitbucket.org/t2y/ikazuchi.plugins.speech
   $ cd ikazuchi.plugins.speech
   $ python bootstrap.py -d
   $ bin/buildout


Usage
=====

Speak given text with ikazuchi command::

    $ ikazuchi speech -s "hello world"
    use command: /usr/bin/afplay
    sentence:                hello world
    translate_tts(Google):   

Speak translated text with ikazuchi command::

    $ ikazuchi speech -s "hello world" -p
    use command: /usr/bin/afplay
    sentence:                hello world
    translate(Google):       [translated text]
    translate_tts(Google):   

Show which plugins are available::

    $ ikazuchi -h
    usage: ikazuchi [-h] {rstfile,speech,normal} ...

    positional arguments:
      {rstfile,speech,normal}
                            available plugins. 'normal' means ikazuchi's standard
                            feature so it can be abbreviated

    optional arguments:
      -h, --help            show this help message and exit

Show speech plugin help::

    $ ikazuchi speech -h
    usage: ikazuchi speech [-h] [-a API] [-e ENCODING] [-f LANG] [-q] [-t LANG]
                           [-c COMMAND] [-p] [-r READING TARGET FILE]
                           [-s SENTENCE [SENTENCE ...]] [--version]

    optional arguments:
      -h, --help            show this help message and exit
      -a API, --api API     APIs are ['google', 'microsoft']
      -e ENCODING, --encoding ENCODING
                            input/output encoding
      -f LANG, --from LANG  original language
      -q, --quiet           not to show original sentence to stdout
      -t LANG, --to LANG    target language to translate
      -c COMMAND, --command COMMAND
                            use any command to speak(play audio file)
      -p, --post            speak post-translated target sentences
      -r READING TARGET FILE, --read READING TARGET FILE
                            read aloud target file
      -s SENTENCE [SENTENCE ...], --sentences SENTENCE [SENTENCE ...]
                            target sentences
      --version             show program's version number and exit


Requirements
============

* Python 2.6 or later
* ikazuchi 0.5.2 or later
* pyglet 1.1.4 or later
* setuptools or distriubte


License
=======

Apache License 2.0


History
=======

0.1.1 (2011-06-11)
------------------
* fix a minor bug related to the default API name

0.1.0 (2011-06-06)
------------------
* first release

