pyowfs - a simple wrapper around owfs' libowcapi
================================================

The motivation for this project came out of the fact that the "original" OWFS
provided python bindings are not able to sufficiently access binary data
contained in memory locations of 1wire devices. This is because the
swig-generated bindings handle the binary content of a sensor's memory
locations as a c-string - so when there is a NULL byte somewhere in your
"binary" data, it gets truncated at exactly this position - which obviously
is not what you want.

Note that pyowfs tries not to be API-compatible with the OWFS python
bindings. This is due to the fact that the OWFS python bindings can not
access entries with dots in their names, nor are they able to access entries
in the form of e.g. "pages/page.0". pyowfs addresses this by using a
"dictionary like" interface with ``.get ()`` and ``.put ()`` methods and a
"Directory" node to access subentries.

Typical usage::

    >>> from pyowfs import Connection
    >>> root = Connection ("192.168.2.112:3030")
    >>> for s in root.find () : print s
    ...
    <Sensor /20.C1A00B000000/ - DS2450>
    <Sensor /12.E8F672000000/ - DS2406>
    <Sensor /29.336C08000000/ - DS2408>

disabling the cache is reflected in the %r of the sensor::

    >>> s.use_cache (0)
    >>> for s in root.find () : print s
    ...
    <Sensor /uncached/20.C1A00B000000/ - DS2450>
    <Sensor /uncached/12.E8F672000000/ - DS2406>
    <Sensor /uncached/29.336C08000000/ - DS2408>

find sensors of a specific type::

    >>> s = root.find (type="DS2406")[0]

dump all entries of the sensor::

    >>> for e in s.iter_entries () : print e
    ...
    PIO.BYTE
    PIO.ALL
    PIO.A
    PIO.B
    <Dir '/12.E8F672000000/T8A/'>
    <Dir '/12.E8F672000000/TAI8570/'>
    address
    alias
    channels
    crc8
    family
    flipflop.BYTE
    flipflop.ALL
    flipflop.A
    flipflop.B
    id
    latch.BYTE
    latch.ALL
    latch.A
    latch.B
    locator
    memory
    <Dir '/12.E8F672000000/pages/'>
    power
    present
    r_address
    r_id
    r_locator
    sensed.BYTE
    sensed.ALL
    sensed.A
    sensed.B
    set_alarm
    type

access ``memory``::

    >>> s.get ("memory")
    "h\xaa\xaa\x1d\xc6\x00|\xcd\xa1;P\9d3\xd5\x91" ...

``pages`` is a directory, so lets see whats beneath it::

    >>> s.get ("pages")
    <Dir '/12.E8F672000000/pages/'>
    >>> for e in s.get ("pages").iter_entries () : print e
    ...
    page.ALL
    page.0
    page.1
    page.2
    page.3

access to individual pages::

    >>> s.get ("pages").get ("page.1")
    '\xff\x00\x8b\xa3J\r\x1e\x84\xcd\x90\x15:\x9d' ...
    >>> s.get ("pages").get ("page.2")
    '\xb1k-\x0bQ\x04\xe7\xdfh\xa1\d\xc6\x84|\xcd2' ...

also possible to access long paths directly via underlying libowcapi::

    >>> root.capi.get ("/bus.0/interface/settings/usb/datasampleoffset")
    '           8'
    >>> root.capi.put ("/bus.0/interface/settings/usb/datasampleoffset", "10")
    True
    >>> root.capi.get ("/bus.0/interface/settings/usb/datasampleoffset")
    '          10'

If you find this useful, or have comments and/or suggestions - or want to
write an even smarter owfs wrapper on top of it ;-) - drop me a note on the
owfs-developers mailing list.

have fun,
marcus.
