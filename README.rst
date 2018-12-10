==============
CorporaCreator
==============

This is a command line tool to create Common Voice corpora.


Installation
===========

After checking this repo out one installs the corresponding python package as follows

``CorporaCreator kdavis$ python setup.py install``


Usage
===========


Given a ``clips.tsv`` file dumped from the Common Voice database one creates a corpora in the directory ``corpora`` as follows

``CorporaCreator kdavis$ create-corpora -d corpora -f clips.tsv``

This will create the following files::

    CorporaCreator kdavis$ tree corpora
    corpora
    ├── br
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── ca
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── cv
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── cy
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── de
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── en
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── fr
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── ga-IE
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── it
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── kab
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── ky
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── sl
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── tr
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    ├── tt
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    └── zh-TW
        ├── dev.tsv
        ├── invalid.tsv
        ├── other.tsv
        ├── test.tsv
        ├── train.tsv
        └── valid.tsv
    
    15 directories, 90 files
