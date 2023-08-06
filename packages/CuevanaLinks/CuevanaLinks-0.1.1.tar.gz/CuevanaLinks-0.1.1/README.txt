************
Cuevanalinks
************

Cuevanalinks_ is a tool to retrieve links of contents in file sharing hosting
services directly from cuevana.tv_

This links are useful as input file to a download manager as Tucan_ or JDownloader_

`Up to date documentation <http://cuevanalinks.readthedocs.org/en/latest/>`_
are hosted on readthedocs.org_

Dependecies
-----------

Cuevanalinks scraps the web using PyQuery_ which is based upon lxml_ .
Also uses plac_ as command line arguments parser. 

Everything is available via `easy_install` or `pip`

.. _Cuevanalinks: https://bitbucket.org/tin_nqn/cuevanalinks/
.. _cuevana.tv: http://www.cuevana.tv
.. _Tucan: http://tucaneando.wordpress.com/
.. _JDownloader: http://jdownloader.org/
.. _PyQuery: http://pyquery.org/
.. _lxml: http://lxml.de/
.. _plac: http://pypi.python.org/pypi/plac
.. _readthedoc.org: http://readthedocs.org

Example usage
-------------


Get help::

    tin@azulita:~$ cuevanalinks -h
    usage: cuevanalinks [-h] [-s] [-l {ES, EN, PT}] title [episode]

    positional arguments:
      title                 Look for a movie or show with this title. If `episode`
                            is empty a movie title is assummed
      episode               Specifies a season/episode of a show. Examples: S01 (a
                            whole season), s02e04, 1x4

    optional arguments:
      -h, --help            show this help message and exit
      -s, --subs            Download subtitles (if available)
      -l {ES, EN, PT}, --language {ES, EN, PT}
                            Define the language of subtitles

Retrieve a specific episode with its subtitle::
    
    tin@azulita:~$ cuevanalinks house 4x10 -s
    Searching 'house' Episode 'S04E10'...

    House M.D. (S04E10): It's a Wonderful Lie (2004)
    -------------------------------------------------

    http://www.megaupload.com/?d=RPI------
    http://bitshare.com/?f=6jw----


    tin@azulita:~$ ls *.srt 
    House M.D. S04E10 - It's a Wonderful Lie (2004).srt

