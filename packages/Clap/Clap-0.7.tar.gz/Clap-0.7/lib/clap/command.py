"""
clap.command
============
This implements the Command class. Commands are run by the Base, and represent
a single "thing" the program can do - even single-command bases have a Command
that is responsible for them.

The basic way to set up a command is to create a subclass of class:`Command`
that overrides the :obj:`run` method, and some of the attributes. The
:obj:`run` method should have a signature of ``(options, arguments)`` and be
written to work on an instance instead of a class.

You can also use the :func:`command` decorator to generate :class:`Command`
classes from a function without having to create a class manually.

:copyright: 2010 Matthew "LeafStorm" Frazier
:license:   MIT/X11, see COPYING for details
"""
import copy
import itertools
import textwrap

DEFAULT_USAGE = '[OPTIONS]'

#: An object only used to take descriptions from an object's docstring.
DOC = object()

class Command(object):
    """
    In addition to the ``run(options, arguments)`` method, you can (and
    should) also override:
    
    :attr:`name`
        The command's name.
    :attr:`aliases`
        An iterable of aliases for the command.
    :attr:`usage`
        The command's usage, not including the command name or program name
        (defaults to ``[OPTIONS]``).
    :attr:`short_desc`
        A brief (should be < 50 chars) description of the command.
    :attr:`long_desc`
        If this is not given, the docstring is used. It is the long
        description of the help, non-word-wrapped. It should explain what the
        command does in detail.
    :attr:`defaults`
        The default values for the command's options. This should be a
        dictionary. (You can also define a :meth:`get_defaults` method
        returning a dictionary of defaults to replace the default defaults.)
    :attr:`interspersed_options`
        Whether to allow options to be mixed in with the positional arguments.
        If this is :obj:`False`, the parser will stop accepting options upon
        the first non-option argument.
    
    The most important part is the options. You can have a static iterable of
    :class:`Option` instances named :attr:`options`, as well as an instance
    method named :attr:`get_options` that returns an iterable. A property
    named :attr:`all_options` does a union of both.
    
    When a command is added to a base, its :meth:`set_base` method is called.
    This sets the :attr:`base` attribute to the given base.
    """
    name = None
    aliases = ()
    usage = DEFAULT_USAGE
    short_desc = ''
    long_desc = ''
    options = ()
    base = None
    defaults = dict()       # NEVER modify the class level defaults dict!
    interspersed_options = True
    
    def get_options(self):
        return ()
    
    @property
    def all_options(self):
        return tuple(itertools.chain(self.options, self.get_options()))
    
    @property
    def all_defaults(self):
        if hasattr(self, 'get_defaults'):
            d = self.defaults.copy()
            d.update(self.get_defaults())
            return d
        else:
            return self.defaults.copy()
    
    def set_base(self, base):
        self.base = base
    
    def __call__(self):
        # this way, you can pass a class or an instance to add_command
        return self
    
    def run(self, options, arguments):
        """
        You should override this method to do whatever you want this command
        to do when it is called from the command line.
        
        :param options: A dictionary of option values.
        :param arguments: A list or tuple of positional arguments.
        """
        raise NotImplementedError("You didn't override the run method.")


def create_command(name, runfunc, aliases=(), options=(), short_desc='',
                   usage=DEFAULT_USAGE, long_desc='', class_name=None,
                   defaults=None, interspersed_options=True,
                   base_class=Command):
    """
    This can be used to create a command. The first two arguments are the name
    and run function (this will not be transformed with ``staticmethod`` or
    anything).
    
    :param name: The command's name, e.g. ``commit``.
    :param runfunc: The run function. This will not be transformed by
                    :func:`staticmethod`, so you may want to wrap it if you
                    don't need the actual object within the function.
    :param aliases: Aliases for the command.
    :param options: An iterable of options.
    :param short_desc: A short description. It should be < 50 characters.
    :param usage: The command's usage string. The default is ``[OPTIONS]``.
    :param long_desc: A longer description of the command.
    :param class_name: The class name to use (by default, it is constructed
                       from the command name).
    :param defaults: Default option values.
    :param interspersed_options: Whether or not to allow interspersed options.
    :param base_class: The base class to subclass from. The default is
                       :class:`Command`.
    """
    if class_name is None:
        class_name = (''.join(part.title() for part in name.split('_')) + 
        'Command')
    if defaults is None:
        defaults = {}
    namespace = dict(name=name, run=runfunc, aliases=aliases, options=options,
                     usage=usage, short_desc=short_desc, long_desc=long_desc,
                     defaults=defaults,
                     interspersed_options=interspersed_options)
    return type(class_name, (base_class,), namespace)


def command(options=(), aliases=(), short_desc='', long_desc='',
            usage='', name=None, static=True, interspersed_options=False,
            base_class=Command):
    """
    This is a magical command decorator. You pass it various options, and it
    will return a function you can decorate another function with to make it
    a command.
    
    :param options: A list/tuple of options.
    :param aliases: A list/tuple of aliases for the command.
    :param short_desc: A brief (< 50 characters) description of the command.
                       If this is :data:`DOC`, the function's docstring will
                       be used.
    :param long_desc: A longer description of the command. If this is
                      :data:`DOC`, the function's docstring will be used.
    :param usage: The command's usage string. It defaults to ``[OPTIONS]``.
    :param name: The name of the command. If not given, it will be equal to
                 the :obj:`__name__` of the function.
    :param interspersed_options: Whether or not to allow interspersed options.
    :param static: Whether to wrap it in :func:`staticmethod` or not,
                   obviating the need to use :obj:`self` in the argument list.
    :param base_class: The base class to subclass from. The default is
                       :class:`Command`.
    """
    def wrapper(fn):
        class_name = fn.__name__
        if not name:
            cmd_name = class_name
        else:
            cmd_name = name
        # the stupid ``cmd_`` names are there so Python doesn't mark the
        # function arguments as locals and throw an UnboundLocalError
        if static:
            fn = staticmethod(fn)
        if short_desc is DOC:
            cmd_short_desc = fn.__doc__
        else:
            cmd_short_desc = short_desc
        if long_desc is DOC:
            cmd_long_desc = textwrap.dedent(fn.__doc__)
        else:
            cmd_long_desc = long_desc
        return create_command(name=cmd_name, class_name=class_name,
               options=options, aliases=aliases, short_desc=cmd_short_desc,
               long_desc=cmd_long_desc, usage=usage, runfunc=fn,
               interspersed_options=interspersed_options,
               base_class=base_class)
    return wrapper
