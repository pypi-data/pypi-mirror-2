
Clock widget for toscawidget and turbogears
===========================================

This Widget encapsulates the epiclock JavaScript library
`http://code.google.com/p/epiclock <http://code.google.com/p/epiclock>`_
for inserting clocks and countdowns contents in a standard-friendly manner.

The current epiclock version packaged with this widget is version 3.0
`http://epiclock.googlecode.com/files/epiclock-3.0.fixed.tar.gz <http://epiclock.googlecode.com/files/epiclock-3.0.fixed.tar.gz>`_
From within your controller, simply instantiate an Epiclock
and return this instance to be rendered within your template::

    from tw.epiclock import Epiclock
    from tg import tmpl_context
    ...
    tmpl_context.my_clock = Epiclock("my_clock")

From within your template, simply call the epiclock::

        ${tmpl_context.my_clock()}


Another common use is display server time somewhere in a header zone
in lib/helpers.py::

    from tw.epiclock import Epiclock
    clock = Epiclock("clock", format="j-n-Y G:i:s")

anywhere in templates::

    ${h.clock()}

custom renderers (retros) are not available is this release

in static jquery.dateformat.js and jquery.epiclock.js are for documentation purpose
only the minimized versions are actually injected in your code