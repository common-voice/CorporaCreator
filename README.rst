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

This will create the corpora in the directory ``corpora`` from the ``clips.tsv`` file.

Each created corpus will contain the files ``valid.tsv``, containing the validated clips; ``invalid.tsv``, containing the invalidated clips; and ``other.tsv``, containing clips that don't have sufficient votes to be considered valid or invalid. In addition it will contain the files ``train.tsv``, the valid clips in the training set; ``dev.tsv``, the valid clips in the validation set; and ``test.tsv``, the valid clips in test set.

The split of ``valid.tsv`` into ``train.tsv``, ``dev.tsv``, and ``test.tsv`` is done such that the number of clips in ``dev.tsv`` or ``test.tsv`` is a "statistically significant" sample relataive to the number of clips in ``train.tsv``. More specificially, if the population size is the number of clips in ``train.tsv``, then the number of clips in ``dev.tsv`` or ``test.tsv`` is the sample size required for a confidence level of 99% and a margin of error of 1% for the ``train.tsv`` population size.

By default no sentence occurs more than once in ``train.tsv``, ``dev.tsv``, and ``test.tsv``. However, one can relax this constraint using the ``-s`` command line parameter. The value of ``-s`` is the number of repeats allows for a sentence. So, for example, if one wanted to allow for a setence to occur 3 times in a corpus, then one could use

``CorporaCreator kdavis$ create-corpora -d corpora -f clips.tsv -s 3``

With or without the use of the ``-s`` command line parameter the result of running ``create-corpora`` will be a directory containing the following files::

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
