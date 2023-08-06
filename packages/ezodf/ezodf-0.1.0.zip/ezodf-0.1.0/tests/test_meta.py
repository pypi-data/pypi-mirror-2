#!/usr/bin/env python
#coding:utf-8
# Author:  mozman --<mozman@gmx.at>
# Purpose: test meta.py
# Created: 28.12.2010
# Copyright (C) 2010, Manfred Moitzi
# License: GPLv3

import os
import unittest
from zipfile import ZipFile

from mytesttools import in_XML

from ezodf.const import GENERATOR
from ezodf.xmlns import XML
from ezodf.meta import Meta

testdata = b"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-meta
xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
xmlns:xlink="http://www.w3.org/1999/xlink"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"
xmlns:ooo="http://openoffice.org/2004/office"
xmlns:grddl="http://www.w3.org/2003/g/data-view#" office:version="1.2"
grddl:transformation="http://docs.oasis-open.org/office/1.2/xslt/odf2rdf.xsl">
<office:meta>
<meta:initial-creator>Manfred Moitzi</meta:initial-creator>
<meta:creation-date>2010-12-29T18:17:19.57</meta:creation-date>
<meta:editing-cycles>2</meta:editing-cycles>
<meta:editing-duration>PT1M56S</meta:editing-duration>
<dc:date>2010-12-29T18:21:31.55</dc:date>
<dc:creator>Manfred Moitzi</dc:creator>
<meta:generator>LibreOffice/3.3$Win32 LibreOffice_project/330m17$Build-3</meta:generator>
<meta:document-statistic meta:table-count="0" meta:image-count="0" meta:object-count="0"
meta:page-count="3" meta:paragraph-count="10" meta:word-count="99"
meta:character-count="999"/>
<meta:user-defined meta:name="Zeit" meta:value-type="date">2010-12-29</meta:user-defined>
<meta:user-defined meta:name="mozman">derWert</meta:user-defined>
</office:meta>
</office:document-meta>
"""

TAGS = ['generator',
        'title',
        'description',
        'subject',
        'initial-creator',
        'creator',
        'creation-date',
        'date',
        'editing-cycles',
        ]

class TestMeta(unittest.TestCase):
    def test_open_from_text(self):
        meta = Meta(testdata)
        self.assertEqual(meta['initial-creator'], "Manfred Moitzi")

    def test_open_from_ElementTree(self):
        xmltree = XML.etree.fromstring(testdata)
        meta = Meta(xmltree)
        self.assertEqual(meta['initial-creator'], "Manfred Moitzi")

    def test_new_Meta(self):
        meta = Meta()
        self.assertEqual(meta['generator'], GENERATOR)

    def test_tobytes_without_manipulation(self):
        meta = Meta(testdata)
        result = meta.tobytes()
        self.assertTrue(in_XML(result, testdata))

    def test_set_metadata(self):
        meta = Meta(testdata)
        meta['creator'] = 'Bob the Builder'
        self.assertEqual(meta['creator'], 'Bob the Builder')

    def test_get_metadata_error(self):
        meta = Meta(testdata)
        with self.assertRaises(KeyError):
            meta['Terminator']

    def test_set_metadata_error(self):
        meta = Meta(testdata)
        with self.assertRaises(KeyError):
            meta['Terminator'] = 'Arnold Schwarzenegger'

    def test_all_tags(self):
        meta = Meta()
        data = "djkwzr648tjdgdhjfzezglhfih"
        for tag in TAGS:
            meta[tag] = data
            self.assertEqual(meta[tag], data)

    def test_editing_cycles(self):
        meta = Meta()
        self.assertRaises(KeyError, meta.__getitem__, 'editing-cycles')
        meta.inc_editing_cycles()
        self.assertEqual(meta['editing-cycles'], '1')
        meta.inc_editing_cycles()
        self.assertEqual(meta['editing-cycles'], '2')

class TestKeywords(unittest.TestCase):
    def test_keyword_in_xml_serialisation(self):
        meta = Meta()
        meta.keywords.add('KEYWORD1')
        self.assertTrue(b'<meta:keyword>KEYWORD1</meta:keyword>' in meta.tobytes())

    def test_add_and_in_operator(self):
        meta = Meta()
        meta.keywords.add('KEYWORD1')
        self.assertTrue('KEYWORD1' in meta.keywords)

    def test_remove_and_in_operator(self):
        meta = Meta()
        KW = 'KEYWORD1'
        meta.keywords.add(KW)
        self.assertTrue(KW in meta.keywords)
        meta.keywords.remove(KW)
        self.assertFalse(KW in meta.keywords)

    def test_iter(self):
        meta = Meta()
        KW = ['KEYWORD1', 'KEYWORD2']
        for keyword in KW:
            meta.keywords.add(keyword)
        result = list(meta.keywords)
        self.assertSequenceEqual(KW, result)

class TestUsertags(unittest.TestCase):
    def test_usertag_in_xml_serialisation(self):
        meta = Meta()
        meta.usertags['TAG1'] = 'VALUE1'
        self.assertTrue(b'<meta:user-defined meta:name="TAG1">VALUE1</meta:user-defined>' in meta.tobytes())

    def test_usertag_with_type_in_xml_serialisation(self):
        meta = Meta()
        meta.usertags.set('TAG1', '100.0', 'float')
        self.assertTrue(b'<meta:user-defined meta:name="TAG1" meta:value-type="float">100.0</meta:user-defined>' in meta.tobytes())

    def test_add_and_in_operator(self):
        meta = Meta()
        meta.usertags['TAG1'] = 'VALUE1'
        self.assertTrue('TAG1' in meta.usertags)

    def test_add_and_get(self):
        meta = Meta()
        meta.usertags['TAG1'] = 'VALUE1'
        self.assertEqual(meta.usertags['TAG1'], 'VALUE1')

    def test_add_and_modify(self):
        meta = Meta()
        meta.usertags['TAG1'] = 'VALUE1'
        self.assertEqual(meta.usertags['TAG1'], 'VALUE1')
        meta.usertags['TAG1'] = 'VALUE2'
        self.assertEqual(meta.usertags['TAG1'], 'VALUE2')

    def test_get_error(self):
        meta = Meta()
        with self.assertRaises(KeyError):
            meta['XXX']

    def test_remove_and_in_operator(self):
        meta = Meta()
        NAME = 'TAG1'
        meta.usertags[NAME] = 'VALUE1'
        self.assertTrue(NAME in meta.usertags)
        del meta.usertags[NAME]
        self.assertFalse(NAME in meta.usertags)

    def test_remove_error(self):
        meta = Meta()
        with self.assertRaises(KeyError):
            del meta.usertags['XXX']

    def test_iter(self):
        meta = Meta()
        TAGS = [('TAG1', 'VALUE1'), ('TAG2', 'KEYWORD2')]
        for name, value in TAGS:
            meta.usertags[name] = value
        result = list(meta.usertags)
        self.assertSequenceEqual(TAGS, result)

    def test_usertags_to_dict(self):
        meta = Meta()
        TAGS = dict([('TAG1', 'VALUE1'), ('TAG2', 'KEYWORD2')])
        for name, value in TAGS.items():
            meta.usertags[name] = value
        result = dict(meta.usertags)
        self.assertDictEqual(TAGS, result)

    def test_typeof_string(self):
        meta = Meta()
        meta.usertags['TAG1'] = 'VALUE1'
        self.assertEqual(meta.usertags.typeof('TAG1'), 'string')

    def test_typeof_float(self):
        meta = Meta()
        meta.usertags.set('TAG1', '100.0', 'float')
        self.assertEqual(meta.usertags.typeof('TAG1'), 'float')

    def test_typeof_error(self):
        meta = Meta()
        with self.assertRaises(KeyError):
            meta.usertags.typeof('Nelson')

class TestStatistic(unittest.TestCase):
    def test_get(self):
        meta = Meta(testdata)
        self.assertEqual(meta.count['word'], 99)
        self.assertEqual(meta.count['character'], 999)
        self.assertEqual(meta.count['paragraph'], 10)
        self.assertEqual(meta.count['page'], 3)
        self.assertEqual(meta.count['table'], 0)
        self.assertEqual(meta.count['sentence'], 0)

    def test_get_keyerror(self):
        meta = Meta(testdata)
        with self.assertRaises(KeyError):
            meta.count['xxx']

    def test_set(self):
        meta = Meta(testdata)
        self.assertEqual(meta.count['word'], 99)
        meta.count['word'] = 17
        self.assertEqual(meta.count['word'], 17)

    def test_set_keyerror(self):
        meta = Meta(testdata)
        with self.assertRaises(KeyError):
            meta.count['xxx'] = 777


if __name__=='__main__':
    unittest.main()