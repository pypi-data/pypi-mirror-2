"""
clap.help
=========
This holds HelpFormatters. A ``HelpFormatter`` is responsible for formatting
help. They should all be based on the ``HelpFormatter`` base class, and then
inherit some methods.

:copyright: 2010 Matthew "LeafStorm" Frazier
:license:   MIT/X11, see COPYING for details
"""
import os
import sys
import textwrap
from clap.ansi import ANSI

class BaseHelpFormatter(object):
    """
    HelpFormatters are constructed with a stream. They should format the help
    when certain methods are called. Note that :class:`BaseHelpFormatter`
    itself does not implement these methods, but :class:`HelpFormatter` does.
    
    :meth:`usage`
        Called with one string argument, the usage string. It should print it.
    
    :meth:`text`
        Again, called with one argument, a paragraph of text. It should
        word-wrap the given text and print it.
    
    :meth:`cmd_list`
        This is called with a list/tuple of tuples in the form ``(name,
        description)``. It should print them out, in order.
    
    :meth:`option_list`
        This is called with an iterable of :class:`clap.parser.Option`
        instances. It should print them out, again, in order.
    
    :meth:`start_section`
        This is called with a section title. This should print a header for
        that section, then set up for any indentation that needs to be done.
    
    
    :param stream: The stream to print to. It defaults to :obj:`sys.stdout`.
    :param width: The width of the screen. It will default to the value of the
                  environment variable :obj:`COLUMNS`.
    """
    
    #: The amount each call to :meth:`indent` will indent by.
    indent_by = 2
    
    def __init__(self, stream=None, width=None):
        self.stream = stream or sys.stdout
        self.indent = 0
        self.width = width or int(os.environ.get('COLUMNS', '80')) - 2
    
    #: A property for the screen width minus the current indentation level.
    ewidth = property(lambda s: s.width - s.indent)
    
    #: A property that returns :attr:`indent` number of spaces.
    indentation = property(lambda s: ' ' * s.indent)
    
    def indent(self):
        """
        This will increase the current indentation level by :attr:`indent_by`
        spaces. Any calls to :meth:`write` will be prepended by that much
        indentation.
        """
        self.indent = self.indent + self.indent_by
    
    def dedent(self):
        """
        This will decrease the current indentation level by :attr:`indent_by`
        spaces.
        
        :raises: :class:`RuntimeError` if you try to dedent past 0.
        """
        if self.indent == 0:
            raise RuntimeError("Can't dedent past 0")
        self.indent = self.indent - self.indent_by
    
    def write(self, data='', newline=True, indent=True):
        """
        This writes the given data to the stream. Under normal circumstances,
        the data printed will be indented to the current indentation level.
        
        :param data: The data to write.
        :param newline: Whether to add a newline to the end. (The default is
                        :obj:`True`.)
        :param indent: Whether to indent the line. (The default is
                       :obj:`True`.)
        """
        if newline:
            data = data + '\n'
        if indent:
            data = self.indentation + data
        self.stream.write(data)
    
    def __del__(self):
        del self.stream


class HelpFormatter(BaseHelpFormatter):
    """
    This is what you will actually want to subclass. This is actually a fairly
    complete implementation of HelpFormatter, but it doesn't look that great.
    """
    def usage(self, usage_string):
        self.write("Usage: %s\n" % usage_string)
    
    def text(self, text):
        self.write(textwrap.fill(text, self.width,
            initial_indent=self.indentation,
            subsequent_indent=self.indentation
        ), indent=False)
        self.write()
    
    def cmd_list(self, commands):
        command_width = max(len(c) for (c, d) in commands)
        description_width = self.ewidth - command_width - 2
        for command, desc in commands:
            lines = textwrap.wrap(desc, description_width)
            self.write('%s  %s' % (command.ljust(command_width), lines[0]))
            for line in lines[1:]:
                self.write(' ' * (command_width + 2) + line)
        self.write()
    
    def option_list(self, options):
        options = tuple(options)
        for opt in options:
            title = self._option_title(opt)
            desc = textwrap.wrap((opt.desc or ' '), self.ewidth - 20)
            if not desc:
                self.write(title)
            elif len(title) > 20:
                self.write(title)
                for line in desc:
                    self.write(' ' * 22 + line)
            else:
                self.write('%s  %s' % (title.ljust(20), desc[0]))
                for line in desc[1:]:
                    self.write(' ' * 22 + line)
        self.write()
    
    def _option_title(self, opt):
        if opt.argument:
            if opt.short and opt.long:
                return '-%s __, --%s=__' % (opt.short, opt.long)
            elif opt.short:
                return '-%s __' % opt.short
            elif opt.long:
                return '--%s __' % opt.long
        else:
            if opt.short and opt.long:
                return '-%s, --%s' % (opt.short, opt.long)
            elif opt.short:
                return '-%s' % opt.short
            elif opt.long:
                return '--%s' % opt.long
    
    def start_section(self, heading):
        self.write("%s:" % heading)
    
    def end_section(self):
        pass


class IndentedHelpFormatter(HelpFormatter):
    """
    This is a variant of :class:`HelpFormatter` that indents each section.
    """
    def start_section(self, heading):
        self.write('%s:' % heading)
        self.indent()
    
    def end_section(self):
        self.dedent()


class ANSIHelpFormatter(HelpFormatter):
    """
    This is a variant of :class:`HelpFormatter` that uses ANSI effects as
    provided by :class:`clap.ansi.ANSI`.
    """
    def __init__(self, stream=None, width=None):
        HelpFormatter.__init__(self, stream, width)
        self.ansi = ANSI(self.stream)
    
    def usage(self, usage_string):
        self.ansi.bright()
        self.write("Usage: ", newline=False)
        self.ansi.reset()
        self.write(usage_string)
    
    def start_section(self, heading):
        self.ansi.bright()
        self.write("%s: " % heading)
        self.ansi.reset()
