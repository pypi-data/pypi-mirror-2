==============
UnicodeLexicon
==============
---------------------------------------
A Unicode aware lexicon for ZCTextIndex
---------------------------------------

Motivation
==========

The standard ZCTextIndex lexicon only deals with 8-bit strings (and only
if you get the zope.conf *locale* setting right).
It does not handle Unicode or UTF-8. UnicodeLexicon fills this gap.

Installation
============

This product adds a ZCTextIndex Unicode Lexicon type to Zope. The
lexicon comes with word splitters, stop word removers, a case normalizer,
and two accent normalizers.

If you have GenericSetup installed, you can use the included extension
profile to create a UnicodeLexicon in your portal_catalog and update
the *Title*, *Description*, and *SearchableText* ZCTextIndexes.

There is no upgrade path from UnicodeLexicon 1.0. If you have 1.0 on your
system, you have to delete and recreate the lexicon.

Pipeline Elements
=================

The splitter works with all languages that separate words with
whitespace characters.

The stop word remover knows about English language stop words only.

The accent normalizer comes in two flavors. There is a normalizer for Latin
and Western European text (fr, es, pt, it, en, nl), and one for German and
Scandinavian text (de, dk, no, se, fi, is). The latter keeps the umlaut
characters ä, ö, and ü in tact.

Caveats
=======

The lexicon assumes either Unicode or UTF-8. If your application uses
a different encoding, you must change the ``enc`` constant in
UnicodeSplitter.py accordingly.

Related
=======

For CJK text you will want to use the standard ZCTextIndex lexicon in
conjunction with CJKSplitter_. For Greek text you will want the standard
ZCTextIndex lexicon with GRSplitter_.

.. _CJKSplitter: http://www.zope.org/Members/panjunyong/CJKSplitter
.. _GRSplitter: http://pypi.python.org/pypi/qi.GRSplitter

