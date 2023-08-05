#!/usr/bin/env python

# $Id: test_docutils_xml.py 5889 2009-04-01 20:00:21Z gbrandl $
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for docutils XML writer.
"""

from __init__ import DocutilsTestSupport

import docutils
import docutils.core
from docutils._compat import b


class DocutilsXMLTestCase(DocutilsTestSupport.StandardTestCase):

    input = b("""\
Test

----------

Test. \xc3\xa4\xc3\xb6\xc3\xbc\xe2\x82\xac""")
    xmldecl = b('<?xml version="1.0" encoding="iso-8859-1"?>\n')
    doctypedecl = b('<!DOCTYPE document PUBLIC "+//IDN docutils.sourceforge.net//DTD Docutils Generic//EN//XML" "http://docutils.sourceforge.net/docs/ref/docutils.dtd">\n')
    generatedby = b('<!-- Generated by Docutils %s -->\n' % docutils.__version__)
    bodynormal = b('<document source="&lt;string&gt;"><paragraph>Test</paragraph><transition/><paragraph>Test. \xe4\xf6\xfc&#8364;</paragraph></document>')
    bodynewlines = b("""\
<document source="&lt;string&gt;">
<paragraph>
Test
</paragraph>
<transition/>
<paragraph>
Test. \xe4\xf6\xfc&#8364;
</paragraph>
</document>
""")
    bodyindents = b("""\
<document source="&lt;string&gt;">
    <paragraph>
        Test
    </paragraph>
    <transition/>
    <paragraph>
        Test. \xe4\xf6\xfc&#8364;
    </paragraph>
</document>
""")

    def test_publish(self):
        settings = {'input_encoding': 'utf8',
                    'output_encoding': 'iso-8859-1',
                    '_disable_config': 1}
        for settings['newlines'] in 0, 1:
            for settings['indents'] in 0, 1:
                for settings['xml_declaration'] in 0, 1:
                    for settings['doctype_declaration'] in 0, 1:

                        expected = b('')
                        if settings['xml_declaration']:
                            expected += self.xmldecl
                        if settings['doctype_declaration']:
                            expected += self.doctypedecl
                        expected += self.generatedby
                        if settings['indents']:
                            expected += self.bodyindents
                        elif settings['newlines']:
                            expected += self.bodynewlines
                        else:
                            expected += self.bodynormal

                        self.assertEqual(docutils.core.publish_string
                                         (source=self.input,
                                          reader_name='standalone',
                                          writer_name='docutils_xml',
                                          settings_overrides=settings),
                                         expected)


if __name__ == '__main__':
    import unittest
    unittest.main()
