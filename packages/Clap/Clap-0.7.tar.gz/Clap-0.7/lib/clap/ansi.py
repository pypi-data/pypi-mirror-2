"""
clap.ansi
=========
An extra class for formatting your output with ANSI SGR codes. You can create
your own :class:`ANSI` or use the pre-existing :data:`ansi`, which is preset
for :obj:`sys.stdout`.

:copyright: 2010 Matthew "LeafStorm" Frazier
:license:   MIT/X11, see COPYING for details
"""

import sys


class ANSI(object):
    """
    This is capable of handling the majority of widely-supported SGR codes.
    It is instantiated with a stream, but if the stream is :obj:`None`, it
    will merely return the codes generated instead of write them.
    
    :param stream: The stream to write to. If it is :obj:`None`, the codes
                   will be returned.
    """
    SGR_ESCAPE = '\x1b[%sm'
    COLORS = dict((i, c) for (c, i) in enumerate(
            'black red green yellow blue magenta cyan white'.split()
    ))
    
    def __init__(self, stream=None):
        if stream and not hasattr(stream, 'write'):
            raise TypeError("The stream must have a write method!")
        self.stream = stream
    
    def write(self, data):
        """
        This writes data to the stream. If the stream is :obj:`None`, it just
        returns the data. If the data is an :class:`int`, it will wrap it in
        an escape code before printing.
        
        :param data: The data to write, or an :class:`int` SGR code.
        """
        if isinstance(data, int):
            data = self.SGR_ESCAPE % data
        if self.stream is None:
            return data
        else:
            return self.stream.write(data)
    
    def reset(self):
        """
        Resets all colors and font effects.
        """
        return self.write(0)
    
    def color(self, color):
        """
        Sets the foreground color to the given color.
        
        :param color: The color to set. (Can be an :class:`int` from 1-7 or a
                      :class:`str`.)
        """
        if isinstance(color, str):
            ccode = 30 + self.COLORS[color.lower()]
        else:
            ccode = 30 + color
        return self.write(ccode)
    
    def bgcolor(self, color):
        """
        Sets the background color to the given color.
        
        :param color: The color to set. (Can be an :class:`int` from 1-7 or a
                      :class:`str`.)
        """
        if isinstance(color, str):
            ccode = 40 + self.COLORS[color.lower()]
        else:
            ccode = 40 + color
        return self.write(ccode)
    
    def bright(self):
        """
        Sets "bright" text, which is bold, brighter than normal, or both.
        """
        return self.write(1)
    
    def dim(self):
        """
        Sets "dim" text, which is darker than normal.
        """
        return self.write(2)
    
    def underline(self):
        """
        Sets the text to be underlined.
        """
        return self.write(4)
    
    def inverse(self):
        """
        Sets the text to be in reverse video (background is foreground and
        vice versa).
        """
        return self.write(7)
    
    def _color(col):
        f = lambda self: self.color(col)
        f.__name__ = col
        f.__doc__ = 'Sets the foreground color to %s.' % col
        return f
    
    black = _color('black')
    red = _color('red')
    green = _color('green')
    yellow = _color('yellow')
    blue = _color('blue')
    magenta = _color('magenta')
    cyan = _color('cyan')
    white = _color('white')
    del _color
    
    def _color(col):
        f = lambda self: self.color(col)
        f.__name__ = col + 'bg'
        f.__doc__ = 'Sets the background color to %s.' % col
        return f
    
    blackbg = _color('black')
    redbg = _color('red')
    greenbg = _color('green')
    yellowbg = _color('yellow')
    bluebg = _color('blue')
    magentabg = _color('magenta')
    cyanbg = _color('cyan')
    whitebg = _color('white')
    del _color


#: An :class:`ANSI` instance set to :data:`sys.stdout`.
ansi = ANSI(sys.stdout)

#: An :class:`ANSI` instance set to :data:`None`, so you can access the codes.
ansi_codes = ANSI(None)
