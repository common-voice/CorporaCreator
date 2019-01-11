==============
CorporaCreator
==============

This is a command line tool to create Common Voice corpora.


Installation
===========

After checking this repo out one installs the corresponding python package as follows

``CorporaCreator$ python3 setup.py install``


Usage
===========


Given a ``clips.tsv`` file dumped from the Common Voice database one creates a corpora in the directory ``corpora`` as follows

``CorporaCreator$ create-corpora -d corpora -f clips.tsv``

This will create the corpora in the directory ``corpora`` from the ``clips.tsv`` file.

Each created corpus will contain the files ``valid.tsv``, containing the validated clips; ``invalid.tsv``, containing the invalidated clips; and ``other.tsv``, containing clips that don't have sufficient votes to be considered valid or invalid. In addition it will contain the files ``train.tsv``, the valid clips in the training set; ``dev.tsv``, the valid clips in the validation set; and ``test.tsv``, the valid clips in test set.

The split of ``valid.tsv`` into ``train.tsv``, ``dev.tsv``, and ``test.tsv`` is done such that the number of clips in ``dev.tsv`` or ``test.tsv`` is a "statistically significant" sample relataive to the number of clips in ``train.tsv``. More specificially, if the population size is the number of clips in ``train.tsv``, then the number of clips in ``dev.tsv`` or ``test.tsv`` is the sample size required for a confidence level of 99% and a margin of error of 1% for the ``train.tsv`` population size.

By default no sentence occurs more than once in ``train.tsv``, ``dev.tsv``, and ``test.tsv``. However, one can relax this constraint using the ``-s`` command line parameter. The value of ``-s`` is the number of repeats allows for a sentence. So, for example, if one wanted to allow for a sentence to occur 3 times in a corpus, then one could use

``CorporaCreator$ create-corpora -d corpora -f clips.tsv -s 3``

With or without the use of the ``-s`` command line parameter the result of running ``create-corpora`` will be a directory containing the following files::

    CorporaCreator$ tree corpora
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
    ├── cnh
    │   ├── dev.tsv
    │   ├── invalid.tsv
    │   ├── other.tsv
    │   ├── test.tsv
    │   ├── train.tsv
    │   └── valid.tsv
    .
    .
    .
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
    
    19 directories, 114 files


Contributing
===========

Introduction
------------

The purpose of the ``create-corpora`` command line tool is to provide a jumping-off point for contributors. The data in the alpha release of the Common Voice data is, unfortunately, in need of cleaning and the ``create-corpora`` command line tool provides a plugin for each language that allows for the language communities to aid in cleaning the data.


Detailed Introduction
---------------------

The ``clips.tsv`` file is a `tab separated file`_ containing a dump of the raw data from Common Voice with the following columns:

1) ``client_id`` - A unique identifier for the contributor that was randomly generated
2) ``path`` - The path the the audio file containing the contribution
3) ``sentence`` - The sentence the contributor was asked to read
4) ``up_votes`` - The number of up votes for the contribution
5) ``down_votes`` - The number of down votes for the contribution
6) ``age`` - The age range of the contributor, if the contributor reported it
7) ``gender`` - The gender of the contributor, if the contributor reported it
8) ``accent`` - The accent of the contributor, if the contributor reported it
9) ``locale`` - The locale decribing the language the contributor was reading
10) ``bucket`` - The "bucket" (train, dev, or test) the clip is currently assigned to

The problem is that data in the column ``sentence`` needs to be cleaned, as there are various problems with the data in the ``sentence`` column. For example some sentences contain HTML fragments. Some contain spelling errors. Some contain digits, e.g. "Room 4025" that allow for many valid readings. Some contain errors which we at Mozilla are not even aware of.

So to correct these we outfitted ``create-corpora`` with a common plugin `common.py`_ that is responsible for cleaning sentences in a language agnostic manner. For example, if a sentence contains HTML fragments, then the HTML fragments would be removed by `common.py`_.

The processing of `common.py`_ is done in the method: 

::

def common(sentence):
    """Cleans up the passed sentence in a language independent manner, removing or reformatting invalid data.
    Args:
      sentence (str): Sentence to be cleaned up.
    Returns:
      (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
    """
    ...
    # TODO: Clean up data in a language independent manner
    return sentence


.. _tab separated file: https://en.wikipedia.org/wiki/Tab-separated_values
.. _common.py: https://github.com/mozilla/CorporaCreator/blob/master/src/corporacreator/preprocessors/common.py
