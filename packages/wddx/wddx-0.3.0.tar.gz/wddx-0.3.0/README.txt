
====
WDDX
====

A python decoder for the WDDX XML serialisation format.

WDDX was an XML data serialisation format created in 1998, initially for the
ColdFusion server environment, then open-sourced. It has faded into history
now, having lost out to JSON, YAML, and native serialisation.  According to
its `Wikipedia article <http://en.wikipedia.org/wiki/WDDX>`_ WDDX was a
precursor to SOAP -- which may help explain some of the latter's
brain-damage...

This module is a straight-forward decoder for WDDX packets that I wrote
while extracting the data from a PHP (which included early built-in support
for the format) project that had a home-brewed ORM.

I have decoded many thousands of packets with it, YMMV.

It has good support for the parts of the WDDX standard that the PHP wddx
functions actually use, but probably poor support of the full standard. It's
impossible to actually tell because the specification is no longer online!
DNS entries for wddx.org expired in 2010, last year as I write this.


Example
=======

The API follows the example given by the json, pickle, and marshall modules.
You can see lots more examples in the test folder, including recursive
sequence and mapping types.

>>> import wddx
>>> xml = """
... <wddxPacket version='1.0'>
... <data>
...     <number>3.1415926</number>
...     <null />
...     <string>Hello, world</string>
...     <number>42</number>
...     <dateTime>1998-06-12T04:32:12</dateTime>
... </data>
... </wddxPacket>
... """
>>> wddx.loads(xml)
[3.1415926, None, 'Hello, world', 42, datetime.datetime(1998, 6, 12, 4, 32, 12)]


TODO
====

This module is by no means a full WDDX implementation.  The format is
practically dead -- at the time of writing the WDDX specification websites
were off-line.  (Indeed, I wrote this module to help retire a legacy
data-storage engine written back when WDDX looked like a promising
interchange format.)

Below are the key deficiencies.  I'm not planning on rectifying any of these
myself, they are documented here in case anybody else wants to take the module
over...


Python 2 Support
----------------

The module is currently Python 3 only, but will run with minor changes under
Python 2.


Encoding Support
----------------

The world needs less WDDX packets, not more.  I have resisted the temptation
to write the missing dump() and dumps() functions, even though it might be
fun to do so...


Date-time Parsing
-----------------

Parsing of date-time values is weak.  WDDX represents date-time values using
full ISO 8601 encoding.  This should be decoded using a full ISO 8601 parser,
not the fragile datetime.strptime() I used.  There is no such parser in the
standard library, and I was loath to bring in an external dependency for
a field I wasn't using.


Nicities and Details
--------------------

I've only implemented enough of the WDDX specification to handle all of the
packets I had.  Partly because that was enough to 'stratch my itch', but
mostly because I was unable to find a copy of the spec.

For example, I found a presentation online with a slide that mentions in
passing that the WDDX string type can contain  control characters in
strings, eg. <char code='0C'/>.  This feature, and probably many others, is
entirely unsupported.
