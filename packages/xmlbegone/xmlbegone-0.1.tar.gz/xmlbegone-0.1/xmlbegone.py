# Copyright (c) 2010 Sauce Labs Inc
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
#     The above copyright notice and this permission notice shall be
#     included in all copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#     EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#     OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#     NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#     HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#     WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#     FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#     OTHER DEALINGS IN THE SOFTWARE.

# xmlbegone turns reasonable XML into simple dicts.
#
# It does not turn dicts into XML, because making XML easier to
# generate will only encourage people to keep generating XML, and
# that's bad for everyone.
#
# It treats attributes and elements identically, because the
# difference between them is stupid.
#
# If an element (or attribute) contains only text, the text will be
# its value.  If an element contains other elements, or attributes,
# its value will be a dict (actually an OrderedDict).  If it also
# contains text, that is not very reasonable, but we put in in a
# special key called "_text".  We retain whitespace around text, but
# ignore text nodes that contain only whitespace.
#
# Not all reasonable XML is reasonable in the same way, so xmlbegone
# aims to be configurable.  It can optionally convert simple types
# like ints, booleans, and lists when it identifies them in XML.
#
# Why dicts, rather than objects?  By using a dict, we get a thing
# that every Python user knows how to manipulate, especially with
# dict.keys() and dict.iteritems().
#
# by Steven Hazel

import xml.parsers.expat
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


ALL_TYPES = [bool, int, list, dict]
DEFAULT_TYPES = [list, dict]


class SilentlyOrderedDict(OrderedDict):
    def __repr__(self):
        items = []
        for k, v in self.iteritems():
            items.append("%s: %s" % (repr(k), repr(v)))
        return '{%s}' % (', '.join(items))


class XmlBegoneHandler(object):

    def __init__(self, convert_types=DEFAULT_TYPES, text_key="_text"):
        if convert_types is None:
            convert_types = []
        self.convert_types = convert_types
        self.text_key = text_key
        self.data = []
        self.stack = [self.data]
        self.is_in_text = False
        self.count = 0

    def _start_element(self, name, attrs):
        self.is_in_text = False
        self.stack[-1].append([name, attrs.items()])
        self.stack.append(self.stack[-1][-1][-1])

    def _end_element(self, name):
        self.is_in_text = False
        this = self.stack.pop()

    def _char_data(self, text):
        if self.is_in_text or text.strip():
            self.stack[-1].append((self.text_key, text))
            self.is_in_text = True

    def convert_type(self, value):
        if not self.convert_types:
            return value

        if int in self.convert_types:
            try:
                return int(value)
            except:
                pass
        if bool in self.convert_types:
            if value in ["true", "True", "TRUE"]:
                return True
            if value in ["false", "False", "FALSE"]:
                return False

        return value

    def _unify_text(self, data):
        new_data = []
        text = ""
        appending = False
        for k, v in data:
            if appending and k != self.text_key and text:
                new_data.append((self.text_key, text))
                text = ""
                appending = False
            if k == self.text_key:
                text += v
                appending = True
            else:
                new_data.append((k, v))
        if appending and text:
            new_data.append((self.text_key, text))
        return new_data

    def _dictify_toplevel(self, data):
        data = self._unify_text(data)
        ddata = SilentlyOrderedDict(data)
        if not len(ddata) == len(data):
            ddata = SilentlyOrderedDict()
            last_k = None
            for k, v in data:
                if not k in ddata:
                    ddata[k] = v
                elif list in self.convert_types and k == last_k:
                    if not isinstance(ddata[k], list):
                        ddata[k] = [ddata[k]]
                    ddata[k].append(v)
                else:
                    return data
                last_k = k
        if not ddata:
            ddata = ''
        elif len(ddata) == 1 and self.text_key in ddata:
            ddata = ddata[self.text_key]
        if isinstance(ddata, dict) and not dict in self.convert_types:
            return ddata.items()
        return ddata

    def _dictify(self, data):
        if not isinstance(data, list):
            return data
        data2 = []
        for k, v in data:
            if k == self.text_key and not v:
                continue
            data2.append((k, self._dictify(v)))
        data2 = self._dictify_toplevel(data2)
        if isinstance(data2, unicode):
            return self.convert_type(data2)
        else:
            return data2

    def loads(self, text):
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self._start_element
        p.EndElementHandler = self._end_element
        p.CharacterDataHandler = self._char_data
        p.Parse(text, 1)

        return self._dictify(self.data)

    def load(self, file):
        return self.loads(file.read())


def loads(text, **kw):
    return XmlBegoneHandler(**kw).loads(text)

def load(file, **kw):
    return XmlBegoneHandler(**kw).load(file)
