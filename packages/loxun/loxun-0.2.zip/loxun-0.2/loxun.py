"""
loxun is a Python module to write large output in XML using Unicode and
namespaces. Of course you can also use it for small XML output with plain 8
bit strings and no namespaces.

loxun's features are:

* **small memory foot print**: the document is created on the fly by writing to
  an output stream, no need to keep all of it in memory.

* **easy to use namespaces**: simply add a namespace and refer to it using the
  standard ``namespace:element`` syntax.

* **mix unicode and string**: pass both unicode or plain 8 bit strings to any
  of the methods. Internally loxun converts them to unicode, so once a
  parameter got accepted by the API you can rely on it not resulting in any
  messy ``UnicodeError`` trouble.

* **automatic escaping**: no need to manually handle special characters such
  as ``<`` or ``&`` when writing text and attribute values.

* **robustness**: while you write the document, sanity checks are performed on
  everything you do. Many silly mistakes immediately result in an
  ``XmlError``, for example missing end elements or references to undeclared
  namespaces.

* **open source**: distributed under the GNU Lesser General Public License 3
  or later.

Here is a very basic example. First you have create an output stream. In many
cases this would be a file, but for the sake of simplicity we use a
``StringIO`` here: 

    >>> from StringIO import StringIO
    >>> out = StringIO()
    >>> xml = XmlWriter(out)

Now write the content:

    >>> xml.prolog()
    >>> xml.addNamespace("xhtml", "http://www.w3.org/1999/xhtml")
    >>> xml.startElement("xhtml:html")
    >>> xml.startElement("xhtml:body")
    >>> xml.text("Hello world!")
    >>> xml.element("xhtml:img", {"src": "smile.png", "alt": ":-)"})
    >>> xml.endElement()
    >>> xml.endElement()
    >>> xml.close()

Finally take a look at the results:

    >>> print out.getvalue().rstrip("\\r\\n")
    <?xml version="1.0" encoding="utf-8"?>
    <xhtml:html xlmns:xhtml="http://www.w3.org/1999/xhtml">
      <xhtml:body>
        Hello world!
        <xhtml:img alt=":-)" src="smile.png"/>
      </xhtml:body>
    </xhtml:html>

Writing a simple document
=========================

The following example creates a very simple XHTML document.

To make it simple, the output goes to a string, but you could also use
a file that has been created using
``codecs.open(filename, "wb", encoding)``.

    >>> from StringIO import StringIO
    >>> out = StringIO()

First create an `XmlWriter` to write the XML code to the specified output:

    >>> xml = XmlWriter(out)

Then add the document prolog:

    >>> xml.prolog()
    >>> print out.getvalue().rstrip("\\r\\n")
    <?xml version="1.0" encoding="utf-8"?>

Next add the ``<html>`` start element:

    >>> xml.startElement("html")

Now comes the <body>. To pass attributes, specify them in a dictionary.
So in order to add::

    <body id="top">

use:

    >>> xml.startElement("body", {"id": "top"})

Let' add a little text so there is something to look at:

    >>> xml.text("Hello world!")

Wrap it up: close all elements and the document.

    >>> xml.endElement()
    >>> xml.endElement()
    >>> xml.close()

And this is what we get:

    >>> print out.getvalue().rstrip("\\r\\n")
    <?xml version="1.0" encoding="utf-8"?>
    <html>
      <body id="top">
        Hello world!
      </body>
    </html>

Now the same thing but with a namespace. First create the prolog
and header like above:

    >>> out = StringIO()
    >>> xml = XmlWriter(out)
    >>> xml.prolog()

Next add the namespace:

    >>> xml.addNamespace("xhtml", "http://www.w3.org/1999/xhtml")

Now elements can use qualified element names using a colon (:) to separate
namespace and element name:

    >>> xml.startElement("xhtml:html")
    >>> xml.startElement("xhtml:body")
    >>> xml.text("Hello world!")
    >>> xml.endElement()
    >>> xml.endElement()
    >>> xml.close()

As a result, element names are now prefixed with "xhtml:":

    >>> print out.getvalue().rstrip("\\r\\n")
    <?xml version="1.0" encoding="utf-8"?>
    <xhtml:html xlmns:xhtml="http://www.w3.org/1999/xhtml">
      <xhtml:body>
        Hello world!
      </xhtml:body>
    </xhtml:html>

Version history
===============

Version 0.2, 16-May-2010
------------------------

* Added ``comment()``, ``cdata()`` and ``processingInstruction()`` to write
  these specific XML constructs.
* Added indentation and automatic newline to text if pretty printing is
  enabled.
* Removed newline from prolog in case pretty printing is disabled.
* Fixed missing "?" in prolog.

Version 0.1, 15-May-2010
------------------------

* Initial release.
"""
# Copyright (C) 2010 Thomas Aglassinger
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
#  option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Developer cheat sheet
#
# Buid release:
# > python setup.py sdist --formats=zip
#
# Upload release to PyPI:
# > python setup.py sdist --formats=zip upload
#
# Tag a release in the repository:
# > svn copy -m "Added tag for version 0.x." file:///Users/agi/Repositories/huxml/trunk file:///Users/agi/Repositories/huxml/tags/0.x
import collections
import os
import xml.sax.saxutils
from StringIO import StringIO

VERSION = "0.2"
REPOSITORY_ID, VERSION_DATE = "$Id: loxun.py 19 2010-05-16 08:06:46Z roskakori $".split()[2:4]

class XmlError(Exception):
    """
    Error raised when XML can not be generated.
    """
    pass

def _quoted(value):
    _assertIsUnicode(u"value", value)
    return xml.sax.saxutils.quoteattr(value)

def _validateNotEmpty(name, value):
    """
    Validates that `value` is not empty or `None` and raises `XmlError` in case it is.
    """
    assert name
    if not value:
        raise XmlError(u"%s must not be empty" % name)

def _validateNotNone(name, value):
    """
    Validates that `value` is not `None` and raises `XmlError` in case it is.
    """
    assert name
    if value is None:
        raise XmlError(u"%s must not be %r" % (name, None))


def _assertIsUnicode(name, value):
    assert (value is None) or isinstance(value, unicode), \
        u"value for %r must be of type unicode but is: %r" % (name, value)

def _splitPossiblyQualifiedName(name, value):
    """
    A pair `(namespace, name)` derived from `qualifiedName`.

    A fully qualified name:

        >>> _splitPossiblyQualifiedName(u"element name", u"xhtml:img")
        (u'xhtml', u'img')

    A name in the default namespace:

        >>> _splitPossiblyQualifiedName(u"element name", u"img")
        (None, u'img')

    Improper names result in an `XmlError`:

        >>> _splitPossiblyQualifiedName(u"x", u"")
        Traceback (most recent call last):
        ...
        XmlError: x must not be empty
    """
    assert name
    _assertIsUnicode(u"name", name)
    _assertIsUnicode(u"value", value)

    colonIndex = value.find(u":")
    if colonIndex == -1:
        _validateNotEmpty(name, value)
        result = (None, value)
    else:
        namespacePart = value[:colonIndex]
        _validateNotEmpty(u"namespace part of %s", namespacePart)
        namePart = value[colonIndex+1:]
        _validateNotEmpty(u"name part of %s", namePart)
        result = (namespacePart, namePart)
    # TODO: validate that all parts are NCNAMEs.
    return result

def _joinPossiblyQualifiedName(namespace, name):
    _assertIsUnicode(u"namespace", namespace)
    assert name
    _assertIsUnicode(u"name", name)
    if namespace:
        result = u"%s:%s" % (namespace, name)
    else:
        result = name
    return result

class XmlWriter(object):
    # Marks to start/end CDATA.
    _CDATA_START = u"<![CDATA["
    _CDATA_END = u"]]>"

    # Marks to start/end processing instrution.
    _PROCESSING_START = u"<?"
    _PROCESSING_END = u"?>"

    # Possible value for _writeElement()'s ``close`` parameter.
    _CLOSE_NONE = u"none"
    _CLOSE_AT_START = u"start"
    _CLOSE_AT_END = u"end"
    
    def __init__(self, output, pretty=True, encoding=u"utf-8", errors=u"strict"):
        assert output is not None
        assert encoding
        assert errors
        self._output = output
        self._pretty = pretty
        self._indent = u"  "
        self._newline = unicode(os.linesep, "ascii")
        self._encoding = self._unicoded(encoding)
        self._errors = self._unicoded(errors)
        self._namespaces = {}
        self._elementStack = collections.deque()
        self._namespacesToAdd = collections.deque()
        self._isOpen = True
        self._contentHasBeenWritten = False

    @property
    def isPretty(self):
        """Pretty print the output?"""
        return self._pretty

    @property
    def encoding(self):
        """The encoding used when writing to the `output`."""
        return self._encoding

    @property
    def output(self):
        """The stream where the output goes, typically a filelike object."""
        return self._output

    def _encoded(self, text):
        assert text is not None
        _assertIsUnicode(u"text", text)
        return text.encode(self._encoding, self._errors)

    def _unicoded(self, text):
        """
        Same value as `text` but converted to unicode in case `text` is a string.
        `None` remains `None`.
        """
        if text is None:
            result = None
        elif isinstance(text, unicode):
            result = text
        else:
            result = unicode(text, "ascii")
        return result

    def _elementName(self, name, namespace):
        assert name
        if namespace:
            result = u"%s:%s" % (namespace, name)
        else:
            result = name
        return result

    def _validateIsOpen(self):
        if not self._isOpen:
            raise XmlError("operation must be performed before writer is closed")

    def _validateNamespaceItem(self, itemName, namespace, qualifiedName):
        if namespace:
            if namespace not in self._namespaces:
                raise XmlError(u"namespace '%s' for %s '%s' must be added before use" % (namespace, itemName, qualifiedName))

    def _write(self, text):
        assert text is not None
        _assertIsUnicode(u"text", text)
        self._output.write(self._encoded(text))
        if not self._contentHasBeenWritten and text:
            self._contentHasBeenWritten = True

    def _writeIndent(self):
        self._write(self._indent * len(self._elementStack))

    def _writePrettyIndent(self):
        if self._pretty:
            self._writeIndent()

    def _writePrettyNewline(self):
        if self._pretty:
            self.newline()

    def _writeEscaped(self, text):
        assert text is not None
        _assertIsUnicode("text", text)
        self._write(xml.sax.saxutils.escape(text))

    def newline(self):
        self._write(self._newline)

    def addNamespace(self, name, uri):
        assert name
        assert uri
        if self._elementStack:
            raise NotImplemented(u"currently namespace must be added before first element")

        uniName = self._unicoded(name)
        uniUri = self._unicoded(uri)
        if uniName in self._namespaces:
            raise ValueError(u"namespace %r must added only once but already is %r" % (uniName, uniUri))
        self._namespacesToAdd.append((uniName, uniUri))

    def prolog(self, version=u"1.0"):
        """
        Write the XML prolog.

        The encoding depends on the encoding specified when initializing the writer.

        This is what the default prolog looks like:

            >>> from StringIO import StringIO
            >>> out = StringIO()
            >>> xml = XmlWriter(out)
            >>> xml.prolog()
            >>> print out.getvalue().rstrip("\\r\\n")
            <?xml version="1.0" encoding="utf-8"?>

        You can change the version or encoding:

            >>> out = StringIO()
            >>> xml = XmlWriter(out, encoding=u"ascii")
            >>> xml.prolog(u"1.1")
            >>> print out.getvalue().rstrip("\\r\\n")
            <?xml version="1.1" encoding="ascii"?>
        """
        self.processingInstruction(u"xml", "version=%s encoding=%s" %
            (_quoted(version), _quoted(self._encoding))
        )

    def _writeElement(self, namespace, name, close, attributes={}):
        _assertIsUnicode("namespace", namespace)
        assert name
        _assertIsUnicode("name", name)
        assert close
        assert close in (XmlWriter._CLOSE_NONE, XmlWriter._CLOSE_AT_START, XmlWriter._CLOSE_AT_END)
        assert attributes is not None

        actualAttributes = {}

        # Process new namespaces to add.
        while self._namespacesToAdd:
            namespaceName, uri = self._namespacesToAdd.pop()
            if namespaceName:
                actualAttributes[u"xlmns:%s" % namespaceName] = uri
            else:
                actualAttributes[u"xlmns"] = uri
            self._namespaces[namespaceName] = uri

        # Convert attributes to unicode.
        for qualifiedAttributeName, attributeValue in attributes.items():
            uniQualifiedAttributeName = self._unicoded(qualifiedAttributeName)
            attributeNamespace, attributeName = _splitPossiblyQualifiedName(u"attribute name", uniQualifiedAttributeName)
            self._validateNamespaceItem(u"attribute", attributeNamespace, attributeName)
            actualAttributes[uniQualifiedAttributeName] = self._unicoded(attributeValue)

        self._validateNamespaceItem(u"element", namespace, name)
        if namespace:
            element = u"%s:%s" % (namespace, name)
        else:
            element = name
        if self._pretty:
            self._write(self._indent * len(self._elementStack))
        self._write(u"<")
        if close == XmlWriter._CLOSE_AT_START:
            self._write(u"/")
        self._write(element)
        for attributeName in sorted(actualAttributes.keys()):
            _assertIsUnicode(u"attribute name", attributeName)
            value = actualAttributes[attributeName]
            _assertIsUnicode(u"value of attribute %r" % attributeName, value)
            self._write(u" %s=%s" % (attributeName, _quoted(value)))
        if close == XmlWriter._CLOSE_AT_END:
            self._write(u"/")
        self._write(u">")
        if self._pretty:
            self.newline()

    def startElement(self, qualifiedName, attributes={}):
        """
        Start element with name `qualifiedName`, optionally using a namespace
        prefix separated with a colon (:) and `attributes`.

        Example names are "img" and "xhtml:img" (assuming the namespace prefix
        "xtml" has been added before using `addNamespace()`).

        Attributes are a dictionary containing the attribute name and value, for
        example:

        {
            "src": "../some.png",
            "xhtml:alt": "some image"
        }
        """
        uniQualifiedName = self._unicoded(qualifiedName)
        namespace, name = _splitPossiblyQualifiedName(u"element name", uniQualifiedName)
        self._writeElement(namespace, name, XmlWriter._CLOSE_NONE, attributes)
        self._elementStack.append((namespace, name))

    def endElement(self, expectedQualifiedName=None):
        """
        End element that has been started before using `startElement`,
        optionally checking that the name matches `expectedQualifiedName`.

        As example, consider the following writer with a namespace:

            >>> from StringIO import StringIO
            >>> out = StringIO()
            >>> xml = XmlWriter(out)
            >>> xml.addNamespace("xhtml", "http://www.w3.org/1999/xhtml")

            Now start a couple of elements:

            >>> xml.startElement("html")
            >>> xml.startElement("head")
            >>> xml.startElement("xhtml:body")

            Try to end a mistyped element:

            >>> xml.endElement("xhtml:doby")
            Traceback (most recent call last):
                ...
            XmlError: element name must be xhtml:doby but is xhtml:body

            Try again properly:

            >>> xml.endElement("xhtml:body")

            End an element without an expected name:

            >>> xml.endElement()

            Try to end another mistyped element, this time without namespace:

            >>> xml.endElement("xml")
            Traceback (most recent call last):
                ...
            XmlError: element name must be xml but is html
        """
        try:
            (namespace, name) = self._elementStack.pop()
        except IndexError:
            raise XmlError(u"element stack must not be empty")
        if expectedQualifiedName:
            # Validate that actual element name matches expected name.
            uniExpectedQualifiedName = self._unicoded(expectedQualifiedName)
            actualQualifiedName = _joinPossiblyQualifiedName(namespace, name)
            if actualQualifiedName != expectedQualifiedName:
                self._elementStack.append((namespace, name))
                raise XmlError(u"element name must be %s but is %s" % (uniExpectedQualifiedName, actualQualifiedName))
        self._writeElement(namespace, name, XmlWriter._CLOSE_AT_START)

    def element(self, qualifiedName, attributes={}):
        uniQualifiedName = self._unicoded(qualifiedName)
        namespace, name = _splitPossiblyQualifiedName(u"element name", uniQualifiedName)
        self._writeElement(namespace, name, XmlWriter._CLOSE_AT_END, attributes)

    def text(self, text):
        """
        Write `text` using escape sequences if needed.

        Using a writer like

            >>> from StringIO import StringIO
            >>> out = StringIO()
            >>> xml = XmlWriter(out)

        you can write some text:

            >>> xml.text("<this> & <that>")
            >>> print out.getvalue().rstrip("\\r\\n")
            &lt;this&gt; &amp; &lt;that&gt;
        """
        _validateNotNone(u"text", text)
        if self._pretty:
            self._writeIndent()
        uniText = self._unicoded(text)
        self._writeEscaped(uniText)
        if self._pretty:
            self.newline()

    def comment(self, text, embedInBlanks=True):
        """
        Add a comment to the output.
        
        As example set up a writer:

            >>> from StringIO import StringIO
            >>> out = StringIO()
            >>> xml = XmlWriter(out)
            
        Now add the comment

            >>> xml.comment("some comment")

        And the result is:

            >>> print out.getvalue().rstrip("\\r\\n")
            <!-- some comment -->

        A comment can spawn multiple lines. If pretty is enabled, the lines
        will be indented. Again, first set up a writer:
        
            >>> from StringIO import StringIO
            >>> out = StringIO()
            >>> xml = XmlWriter(out)
            
        Then add the comment

            >>> xml.comment("some comment\\nspawning mutiple\\nlines")

        And the result is:

            >>> print out.getvalue().rstrip("\\r\\n")
            <!--
            some comment
            spawning mutiple
            lines
            -->
        """
        uniText = self._unicoded(text)
        if not embedInBlanks and not uniText:
            raise XmlError("text for comment must not be empty, or option embedInBlanks=True must be set")
        if u"--" in uniText:
            raise XmlError("text for comment must not contain \"--\"")
        hasNewline = (u"\n" in uniText) or (u"\r" in uniText)
        hasStartBlank = uniText and uniText[0].isspace()
        hasEndBlank = (len(uniText) > 1) and uniText[-1].isspace()
        self._writePrettyIndent()
        self._write(u"<!--");
        if hasNewline:
            if self._pretty:
                self.newline()
            elif embedInBlanks and not hasStartBlank:
                self._write(u" ")
            for uniLine in StringIO(uniText):
                if self._pretty:
                    self._writeIndent()
                self._writeEscaped(uniLine.rstrip("\n\r"))
                self.newline()
            self._writePrettyIndent()
        else:
            if embedInBlanks and not hasStartBlank:
                self._write(u" ")
            self._writeEscaped(uniText)
            if embedInBlanks and not hasEndBlank:
                self._write(u" ")
        self._write(u"-->");
        if self._pretty:
            self.newline()

    def cdata(self, text):
        """
        Write a CDATA section.
        
        As example set up a writer:

            >>> from StringIO import StringIO
            >>> out = StringIO()
            >>> xml = XmlWriter(out)
            
        Now add the CDATA section:

            >>> xml.cdata("some data\\nlines\\n<tag>&&&")

        And the result is:

            >>> print out.getvalue().rstrip("\\r\\n")
            <![CDATA[some data
            lines
            <tag>&&&]]>
        """
        self._rawBlock(u"CDATA section", XmlWriter._CDATA_START, XmlWriter._CDATA_END, text)

    def processingInstruction(self, target, text):
        """
        Write a processing instruction.
        
        As example set up a writer:

            >>> from StringIO import StringIO
            >>> out = StringIO()
            >>> xml = XmlWriter(out)
            
        Now add the processing instruction:

            >>> xml.processingInstruction("xsl-stylesheet", "href=\\"some.xsl\\" type=\\"text/xml\\"")

        And the result is:

            >>> print out.getvalue().rstrip("\\r\\n")
            <?xsl-stylesheet href="some.xsl" type="text/xml"?>
        """
        targetName = u"target for processing instrution"
        _validateNotNone(targetName, text)
        _validateNotEmpty(targetName, text)
        uniFullText = self._unicoded(target)
        if text:
            uniFullText += " "
            uniFullText += self._unicoded(text)
        self._rawBlock(u"processing instruction", XmlWriter._PROCESSING_START, XmlWriter._PROCESSING_END, uniFullText)

    def _rawBlock(self, name, start, end, text):
        _assertIsUnicode("name", name)
        _assertIsUnicode("start", start)
        _assertIsUnicode("end", end)
        _validateNotNone(u"text for %s" % name, text)
        uniText = self._unicoded(text)
        if end in uniText:
            raise XmlError("text for %s must not contain \"%s\"" % (name, end))
        self._writePrettyIndent()
        self._write(start)
        self._write(uniText)
        self._write(end)
        self._writePrettyNewline()
        
    def raw(self, text):
        """
        Write raw `text` without escaping, validation and pretty printing.

        Using a writer like

            >>> from StringIO import StringIO
            >>> out = StringIO()
            >>> xml = XmlWriter(out)

        you can use ``raw`` for good and add for exmaple a doctype declaration:
        
            >>> xml.raw("<!DOCTYPE html PUBLIC \\"-//W3C//DTD XHTML 1.0 Transitional//EN\\" \\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\\">")
            >>> print out.getvalue().rstrip("\\r\\n")
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

        but you can also do all sorts of evil things which can invalidate the XML document:

            >>> out = StringIO()
            >>> xml = XmlWriter(out)
            >>> xml.raw(">(^_^)<  not particular valid XML &&&")
            >>> print out.getvalue().rstrip("\\r\\n")
            >(^_^)<  not particular valid XML &&&
        """
        _validateNotNone(u"text", text)
        uniText = self._unicoded(text)
        self._write(uniText)

    def close(self):
        """
        Close the writer, validate that all started elements have ended and
        prevent further output.

        Using a writer like

            >>> from StringIO import StringIO
            >>> out = StringIO()
            >>> xml = XmlWriter(out)

        you can write an element without closing it:

            >>> xml.startElement("some")

        However, once you try to close the writer, you get:
            >>> xml.close()
            Traceback (most recent call last):
                ...
            XmlError: elements must end: </some>
        """
        remainingElements = ""
        while self._elementStack:
            if remainingElements:
                remainingElements += ", "
            namespace, name = self._elementStack.pop()
            remainingElements += u"</%s>" % self._elementName(name, namespace)
        if remainingElements:
            raise XmlError(u"elements must end: %s" % remainingElements)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
