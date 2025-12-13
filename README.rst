==============
CorporaCreator
==============

This is a command line tool to create Common Voice corpora.


Installation
=============

After checking this repo out one installs the corresponding Python package as follows

``CorporaCreator$ python3 setup.py install``


Usage
===========


Given the ``clips.tsv`` file dumped from the Common Voice database, you can create a corpus (for each language in the ``clips.tsv`` file) as follows:

``CorporaCreator$ create-corpora -d corpora -f clips.tsv``

This will create the corpora in the directory ``corpora`` from the ``clips.tsv`` file.

If you would like to just create corpora for some language(s), you can pass the ``--langs`` flag as follows:

``CorporaCreator$ create-corpora -d corpora -f clips.tsv --langs en fr``

This will create the corpora only for English and French.

Each created corpus will contain the files ``valid.tsv``, containing the validated clips; ``invalid.tsv``, containing the invalidated clips; and ``other.tsv``, containing clips that don't have sufficient votes to be considered valid or invalid. In addition it will contain the files ``train.tsv``, the valid clips in the training set; ``dev.tsv``, the valid clips in the validation set; and ``test.tsv``, the valid clips in test set.

The split of ``valid.tsv`` into ``train.tsv``, ``dev.tsv``, and ``test.tsv`` is done such that the number of clips in ``dev.tsv`` or ``test.tsv`` is a "statistically significant" sample relataive to the number of clips in ``train.tsv``. More specificially, if the population size is the number of clips in ``train.tsv``, then the number of clips in ``dev.tsv`` or ``test.tsv`` is the sample size required for a confidence level of 99% and a margin of error of 1% for the ``train.tsv`` population size.

By default no sentence occurs more than once in ``train.tsv``, ``dev.tsv``, and ``test.tsv``. However, one can relax this constraint using the ``-s`` command line parameter. The value of ``-s`` is the number of repeats allows for a sentence. So, for example, if one wanted to allow for a sentence to occur 3 times in a corpus, then one could use

``CorporaCreator$ create-corpora -d corpora -f clips.tsv -s 3``

With or without the use of the ``-s`` command line parameter, the result of running ``create-corpora`` will be a directory containing the following files::

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


Cleaning Sentences
------------------

The ``clips.tsv`` file is a `tab-separated file`_ containing a dump of the raw data from Common Voice with the following columns:

1) ``client_id`` - A unique identifier for the contributor that was randomly generated when the contributor joined
2) ``path`` - The path to the audio file containing the contribution
3) ``sentence`` - The sentence the contributor was asked to read
4) ``up_votes`` - The number of up votes for the contribution
5) ``down_votes`` - The number of down votes for the contribution
6) ``age`` - The age range of the contributor, if the contributor reported it
7) ``gender`` - The gender of the contributor, if the contributor reported it
8) ``accents`` - The accent of the contributor, if the contributor reported it
9) ``variant`` - The variant of the language that contributor speaks, if the contributor reported it
10) ``locale`` - The locale describing the language the contributor was reading
11) ``segment`` - Shows whether the sentence belongs to a specific segment
12) ``sentence_domain`` - The domain the sentence belongs to
13) ``bucket`` - The "bucket" (train, dev, or test) the clip is currently assigned to

Our problem is that data in the column ``sentence`` needs to be cleaned, as there are various problems with the data in the ``sentence`` column. For example, some sentences contain HTML fragments. Some contain spelling errors. Some contain digits, e.g. "Room 4025" that allow for many valid readings. Some contain errors which we at Mozilla are not even aware of.

What Needs to be Cleaned?
`````````````````````````

To actually see what needs to be cleaned firsthand, the best thing to do is to run ``create-corpora`` as suggested above:

``CorporaCreator$ create-corpora -d corpora -f clips.tsv``

which will create the corpora in the directory ``corpora`` from the ``clips.tsv`` file. Then examine, for English say, the file ``corpora/en/valid.tsv`` to see which sentences there need cleaning. For other languages you would examine the corresponding file, e.g. for French it would be ``corpora/fr/valid.tsv``.

Language Independent Cleaning
``````````````````````````````

To correct these problems we outfitted ``create-corpora`` with a plugin `common.py`_ that is responsible for cleaning sentences in a language independent manner. For example, if a sentence contains HTML fragments, then the HTML fragments would be removed by `common.py`_.

The language independent cleaning is done by the ``common()`` method in `common.py`_:

::

    def common(sentence):
        """Cleans up the passed sentence in a language independent manner, removing or reformatting invalid data.
        Args:
          sentence (str): Sentence to be cleaned up.
        Returns:
          (boolean,str): A boolean indicating validity and cleaned up sentence.
        """
        ...
        # Clean sentence in a language independent manner
        ...
        return is_valid, sentence

This method is input the sentence to clean, cleans the sentence in a language independent manner, and returns the cleaned sentence along with a boolean indicating its validity.

If the sentence is not able to be cleaned, e.g. it consisted only of HTML fragments, this method can return is_valid set to False.

Currently, `common.py`_ decodes any URL encoded elements of a sentence, removes any HTML tags in a sentence, removes any non-printable characters in a sentence, and marks as invalid any sentence containing digits, in that order. (For the details refer to `common.py`_ .) This seems to catch most language independent problems, but if you see more, please open an issue or make a pull request.


Language Dependent Cleaning
``````````````````````````````

In addition to the language independent plugin `common.py`_  ``create-corpora`` can also support language-dependent cleaning. In order to add language-dependent cleaning, create a plugin named `LOCALE.py` in the `preprocessors` folder with a function definition also named `LOCALE`, where `LOCALE` is whatever ISO language-code is. NOTE: hyphens are not supported, so something like `zh-TW` would be named `zhTW.py`.

For example, the cleaning for English would be done by the ``en()`` method in a file named `en.py`_:

::

    def en(client_id, sentence):
        """Cleans up the passed sentence, removing or reformatting invalid data.
        Args:
          client_id (str): Client ID of sentence's speaker
          sentence (str): Sentence to be cleaned up.
        Returns:
          (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
        """
        # TODO: Clean up en data
        return sentence

This method accepts the sentence to clean along with the client_id of the contributor who read the sentence. It then cleans the sentence in a language dependent manner and returns the cleaned sentence. For a more complex example of what this could look like, refer to `preprocessors/de.py`.

If the sentence is not able to be cleaned, e.g. it is so mangled that it is impossible to determine how to correct it to a valid English sentence, this method can return ``None`` or a string containing only whitespace to indicate the sentence was invalid to begin with.


Language Independent vs Dependent Cleaning
``````````````````````````````````````````

Of note is that in the language dependent case the method that does the cleaning takes not only the sentence but also the client_id of the contributor who read the sentence. In the language independent case this client_id was not present. However, for the language dependent case it's unfortunately required.

A sentence may contain text which is able to be read in many different but valid ways. For example, the sentence "I am in room 4025." can be validly read as "I am in room four oh two five". Equivalently, a valid reading is: "I am in room four zero two five". There are also other valid readings: "I am in room forty twenty five.", "I am in room four thousand twenty five."... To actually determine which of these readings a particular contributor gave, you have to listen to the audio, determine what they said, then replace the digits with text reflecting the contributor's reading, returning this cleaned sentence.


Contributing Code
-----------------

If you are interested in helping clean sentences for a particular language, or even cleaning in a language independent manner in `common.py`_  you can make a pull request that includes your changes. Here we will look at some common ways to correct sentences.


Spelling Corrections
````````````````````

Suppose you found that one, or more English sentences had a misspelling of the word "masquerade" as "masqurade" (sic). As this is concerned with the English language you would write code in the `en.py`_ plugin. A simple solution would be to replace all occurrences of "masqurade" (sic) with "masquerade" in every sentence. One could do this as follows:

::

    def en(client_id, sentence):
        """Cleans up the passed sentence, removing or reformatting invalid data.
        Args:
          client_id (str): Client ID of sentence's speaker
          sentence (str): Sentence to be cleaned up.
        Returns:
          (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
        """
        sentence = sentence.replace("masqurade", "masquerade")
        # TODO: Clean up en data
        return sentence

what you have to be careful about, and which is a complexity that this simple example ignores, is that the word you are replacing can not appear in a context where the replacement is invalid. For example, if "the" were mistyped as "teh", then doing the same replacement of "teh" with "the" would run the risk of converting "tehran" to "theran", an undesired consequence. So you have to be careful.


Abbreviations
`````````````

Suppose you found that one, or more English sentences used the abbreviation "STT" for "speech-to-text". Some people may have read "STT" as the letters "S T T". However, some may have known the abbreviation and read this as "speech-to-text". To determine which was done you have to hear the audio for each reading and write code that handles each contributor individually.

One could do this as follows:

::

    def en(client_id, sentence):
        """Cleans up the passed sentence, removing or reformatting invalid data.
        Args:
          client_id (str): Client ID of sentence's speaker
          sentence (str): Sentence to be cleaned up.
        Returns:
          (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
        """
        if client_id == "8d59b8879856":
            sentence = sentence.replace("STT", "speech-to-text")
        if client_id == "48f3620be0fa":
            sentence = sentence.replace("STT", "S T T")
        # TODO: Clean up en data
        return sentence

To actually hear the audio, you have to request the audio from Mozilla. (See the information distributed with the alpha release as to how to obtain the audio.)

Once you have obtained the audio, you can hear the audio for a given sentence and client_id pair by finding the row corresponding to the sentence + client_id pair in ``clips.tsv``, finding the ``path`` in that row, then playing the file corresponding to the row's ``path`` in the downloaded audio.


Valid Variant Readings
``````````````````````

Suppose you found that one, or more English sentences used the text "room 4025". Some people may have read "room 4025" as "room four oh two five", some as "room four zero two five", some in a completely different way. Again, to determine which way the digits were read, you have to hear the audio for each reading and write code that handles each contributor individually.

One could do this as follows:

::

    def en(client_id, sentence):
        """Cleans up the passed sentence, removing or reformatting invalid data.
        Args:
          client_id (str): Client ID of sentence's speaker
          sentence (str): Sentence to be cleaned up.
        Returns:
          (str): Cleaned up sentence. Returning None or a `str` of whitespace flags the sentence as invalid.
        """
        if client_id == "8d59b8879856":
            sentence = sentence.replace("room 4025", "room four oh two five")
        if client_id == "48f3620be0fa":
            sentence = sentence.replace("room 4025", "room four zero two five")
        # TODO: Clean up en data
        return sentence

To actually hear the audio, you have to request the audio from Mozilla. (See the information distributed with the alpha release as to how to obtain the audio.)

As in the case of abbreviations, you can hear the audio for a given sentence and client_id pair by finding the row corresponding to the sentence + client_id pair in ``clips.tsv``, finding the ``path`` in that row, then playing the file corresponding to the row's ``path`` in the downloaded audio.

.. _tab separated file: https://en.wikipedia.org/wiki/Tab-separated_values
.. _common.py: https://github.com/mozilla/CorporaCreator/blob/master/src/corporacreator/preprocessors/common.py
.. _en.py: https://github.com/mozilla/CorporaCreator/blob/master/src/corporacreator/preprocessors/en.py
