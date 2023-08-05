
tw.swfobject documentation
==============================

This Widget encapsulates the google code swfobject JavaScript library
`http://code.google.com/p/swfobject/`_ for embedding Shockwave Flash content in a standards-friendly manner.

The current swfobject version packaged with this widget is version 2.2
`http://swfobject.googlecode.com/files/swfobject_2_2.zip`_

Example:

From within your controller, simply instantiate a SwfObject and return this instance to be rendered with your template::

    swfobject = SwfObject(swf = "/path/to/mycontent.swf", width = 640, height = 480, flashvars = {"myvar": 0})

From within your template, simply call the swfobject::

    ${swfobject()}