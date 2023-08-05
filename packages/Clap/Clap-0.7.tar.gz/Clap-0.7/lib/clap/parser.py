"""
clap.parser
===========
Instead of delegating option-parser duties to external libraries, Clap ships
its own parser. It supports options in the form::

- ``-a``
- ``-abc`` (three separate options)
- ``-a value``
- ``-avalue`` (call option a with value)
- ``-abc value`` (c gets the value)
- ``-abcvalue`` (c still gets the value)
- ``--foo``
- ``--foo=value``
- ``--foo value``

However, it doesn't support multi-character options beginning with a single
dash, and it doesn't support DOS-style ``/foo`` options.

:copyright: 2010 Matthew "LeafStorm" Frazier
:license:   MIT/X11, see COPYING for details
"""

import re
import string
import sys

SHORTOPT_RANGE = 'A-Za-z0-9?'
SHORTOPT_CHARS = string.letters + string.digits + '?'
LONGOPT_RANGE = 'A-Za-z0-9-'
LONGOPT_WORD = re.compile(r'^[%s]+$' % LONGOPT_RANGE)
LONG_OPTION = re.compile(r'--([%s]+)(?:=(.+))?' % LONGOPT_RANGE)


def shift(l):
    """
    Deletes and returns the first value of a list. Returns None if the list is
    empty.
    
    :param l: The list to shift from.
    """
    if not l:
        return None
    return l.pop(0)


class OptionError(Exception):
    """
    This is the base class for all exceptions thrown by the option parser.
    """


class OptionDefError(OptionError):
    """
    This error is raised when an option was given an invalid definition.
    """


class OptionParsingError(OptionError):
    """
    These errors can be raised during parsing and indicate that something is
    wrong with the provided arguments.
    """
    desc = 'you did something wrong at option %s'
    
    def __init__(self, option):
        self.option = option
    
    def __str__(self):
        return self.desc % self.option


class DoesNotTakeArgument(OptionParsingError):
    """
    This indicates that the given option does not take an argument.
    """
    desc = 'option %s does not take an argument'


class ArgumentRequired(OptionParsingError):
    """
    This indicates that the given option does take an argument, but one was
    not found.
    """
    desc = 'option %s requires a value'


class IllegalOption(OptionParsingError):
    """
    This indicates that the given option does not exist.
    """
    desc = 'option %s does not exist'


class Option(object):
    """
    This class represent a single option. If you improperly define any of
    these parameters, an :class:`OptionDefError` will be raised.
    
    :param short: The short form of the option. This should be a single letter
                  in the range ``A-Za-z0-9?``. It can also be :obj:`None`, in
                  which case there is no short form.
    :param long: The long form of the option. This should be a word consisting
                 of characters in the range ``A-Za-z0-9-``. It can also be
                 :obj:`None`, in  which case there is no long form. (You must
                 have either a short or a long form. Otherwise it makes no
                 sense.)
    :param argument: Whether the option takes an argument. It can be
                     :obj:`True` (argument is required) or :obj:`False`
                     (argument is forbidden). There are no optional arguments.
    :param target: If given, this is the key in the options dict this will be
                   stored in. If not given, it defaults to the long form, with
                   dashes replaced with underscores.
    :param type: If given, this is used to convert the option argument to a
                 value from a string. It should be a callable that returns a
                 value (like :class:`int`), but if it raises a
                 :class:`ValueError`, an :class:`OptionArgumentInvalid` error
                 will be raised. If this is given, :obj:`argument` is implied
                 to be :obj:`True`.
    :param constant: The value that is used for the option's value if an
                     argument is not given. It defaults to :obj:`True`.
    :param desc: A brief description of an option. This should preferably
                 start with a capital letter, not end in punctuation, and be
                 < 50 characters.
    """
    def __init__(self, short=None, long=None, argument=False, target=None,
                 type=None, constant=True, desc=''):
        if short and short not in SHORTOPT_CHARS:
            raise OptionDefError("-%s is not a valid short option" % short)
        self.short = short
        if long and not LONGOPT_WORD.match(long):
            raise OptionDefError("--%s is not a valid long option" % long)
        self.long = long
        if (not short) and (not long):
            raise OptionDefError("must specify either a short or long option")
        if type:
            argument = True
        if argument not in (True, False):
            raise OptionDefError("argument must be True or False")
        self.argument = argument
        if target is None:
            if long:
                self.target = long
            else:
                raise OptionDefError("target not provided")
        else:
            self.target = target
        self.type = type
        self.constant = constant
        self.desc = desc
    
    def convert(self, value):
        if self.type:
            return self.type(value)
        else:
            return value


class BaseOptionParser(object):
    """
    This is the base class for all OptionParsers. It has the logic that
    handles parsing options from a list of option defs, but it doesn't deal
    with storing or doing anything with the data. That is handled by
    subclasses.
    
    When subclassing, be aware that it uses the following attributes for
    itself:
    
    :attr:`argv`
        This stores the arguments being used. It will be modified in real time
    :attr:`options_over`
        If this is :obj:`True`, any encountered options get used as arguments.
        This can be set by subclasses.
    :attr:`_finished`
        When this is set and true, it indicates the parser is done parsing and
        should not parse any more. :meth:`parse` will take care of it itself.
        You don't even need to set it to :obj:`False`.
    
    The subclass should define the methods:
    
    ``short_option(key)``
        This should take a single letter (no leading ``-``) and return either
        an instance of :class:`Option` or :obj:`None`.
    ``long_option(key)``
        This should take a word (no leading ``--``) and return either an
        instance of :obj:`Option` or :obj:`None`.
    ``handle_argument(arg)``
        This takes a whole non-option argument and should do something with
        it.
    ``store_option(option, value=None)``
        This takes the ``Option`` instance and (if the option had a value) the
        value that was captured, and should do something with it.
    ``illegal_short_option(key)``/``illegal_long_option(key, value=None)``
        This is called when ``short_option`` or ``long_option`` returns
        :obj:`None`. (These have a default implementation that raises an
        :obj:`IllegalOption` exception.)
    """
    def parse(self, argv):
        """
        This will parse the given arguments. Please note that each
        :class:`Parser` is only good for one set of arguments, and you should
        destroy it and create a new one if you need to parse a new set of
        arguments. If not, it will raise a :class:`RuntimeError` when you
        call :meth:`parse` again.
        
        :param argv: The arguments to parse. This does NOT default to
                     :obj:`sys.argv`.
        """
        if hasattr(self, '_finished') and self._finished:
            raise RuntimeError("This parser has already parsed options")
        self.argv = argv
        if not hasattr(self, 'options_over'):
            self.options_over = False
        while True:
            arg = shift(self.argv)
            if arg is None:
                break
            if arg == '--':
                self.handle_dbldash()
            elif arg.startswith('--') and not self.options_over:
                key, value = LONG_OPTION.match(arg).groups()
                self.handle_long_option(key, value)
            elif arg.startswith('-') and arg != '-' and not self.options_over:
                self.handle_short_options(arg[1:])
            else:
                self.handle_argument(arg)
        self._finished = True
    
    def handle_dbldash(self):
        self.options_over = True
    
    def handle_long_option(self, key, value=None):
        option = self.long_option(key)
        if option is None:
            self.illegal_long_option(key, value)
        if option.argument:
            if value is None:
                value = shift(self.argv)
                if value is None or value.startswith('-'):
                    raise ArgumentRequired('--%s' % key)
                else:
                    value = option.convert(value)
            else:
                value = option.convert(value)
            self.store_option(option, value)
        else:
            if value:
                raise DoesNotTakeArgument('--%s' % key)
            self.store_option(option)
    
    def handle_short_options(self, letters):
        last_index = len(letters) - 1
        
        for index, key in enumerate(letters):
            option = self.short_option(key)
            if option is None:
                self.illegal_short_option(key)
            if option.argument:
                if index == last_index:
                    value = shift(self.argv)
                    if value is None or value.startswith('-'):
                        raise ArgumentRequired('-%s' % key)
                    else:
                        value = option.convert(value)
                    self.store_option(option, value)
                else:
                    value = option.convert(letters[index+1:])
                    self.store_option(option, value)
                    break
            else:
                self.store_option(option)
    
    def illegal_long_option(self, key, value=None):
        raise IllegalOption('--%s' % key)
    
    def illegal_short_option(self, key):
        raise IllegalOption('-%s' % key)


class OptionParser(BaseOptionParser):
    """
    This class actually does something with its options. Initialize it with
    the option definitions and a few other keyword arguments, call
    :meth:`parse`, and then access :attr:`arguments` and :attr:`option_values`
    for the positional arguments and option values, respectively.
    
    However, it's best not to use instances of this class directly. They are
    not reusable - once you parse some arguments, the parser has too much
    leftover state to parse again. The best way to use it is with the
    :func:`parse` function.
    
    :param optiondefs: An iterable of :class:`Option` instances.
    :param interspersed_options: If this is :obj:`False`, once the first
                                 non-option argument is encountered, the
                                 parser will treat everything following as a
                                 regular positional argument. The default is
                                 :obj:`True`.
    :param callback: If this is given, it should take the
                     :class:`OptionParser` instance, the :class:`Option`
                     instance, and the captured value (if any). If it returns
                     :obj:`None`, the value will be saved as normal. If it
                     returns anything else, it will not.
    """
    def __init__(self, optiondefs, interspersed_options=True, callback=None):
        self.defs = tuple(optiondefs)
        self.interspersed = interspersed_options
        self.options_over = False
        self.sort_defs(self.defs)
        self.option_values = {}
        self.arguments = []
        self._finished = False
        self.callback = callback
    
    def sort_defs(self, defs):
        self.short_opts, self.long_opts = {}, {}
        for option in defs:
            if option.short:
                if option.short in self.short_opts:
                    raise OptionDefError("There is already an option for -%s"
                                         % option.short)
                self.short_opts[option.short] = option
            if option.long:
                if option.long in self.long_opts:
                    raise OptionDefError("There is already an option for --%s"
                                         % option.long)
                self.long_opts[option.long] = option
        self.short_option = self.short_opts.get
        self.long_option = self.long_opts.get
    
    def set_defaults(self, defaults):
        """
        This updates the :attr:`option_values` dictionary with the given
        defaults.
        
        :param defaults: The values to update the option values with.
        """
        self.option_values.update(defaults)
    
    def store_option(self, option, value=None):
        if self.callback:
            if self.callback(self, option, value) is not None:
                return
        if value is None:
            self._save_value(option.target, option.constant)
        else:
            self._save_value(option.target, value)
    
    def _save_value(self, target, value):
        target = target.replace('-', '_')
        if (target in self.option_values and
            isinstance(self.option_values[target], list)):
            self.option_values[target].append(value)
        else:
            self.option_values[target] = value
    
    def handle_argument(self, arg):
        if (not self.interspersed) and (not self.options_over):
            self.options_over = True
        self.arguments.append(arg)


def parse(optiondefs, argv=None, defaults=None, interspersed_options=True,
          callback=None, parser_cls=OptionParser):
    """
    This will parse the arguments. It is preferred to use this instead of
    :class:`OptionParser` directly because it handles the parser's lifecycle
    behind the scenes.
    
    It returns a 2-tuple. The first item is a dictionary, that maps option
    names to values. The second item is a list, of the positional arguments
    captured.
    
    Everything besides :obj:`optiondefs` and :obj:`argv` should be passed as
    keyword arguments in case the option order is changed later.
    
    :param optiondefs: A list of :class:`Option` instances.
    :param argv: The arguments to actually parse. If not given, they default
                 to ``sys.argv[1:]``.
    :param defaults: A dictionary of default values. If given, the option
                     values dict will be updated with them before parsing.
    :param interspersed_options: If this is :obj:`False`, once the first
                                 non-option argument is encountered, the
                                 parser will treat everything following as a
                                 regular positional argument. The default is
                                 :obj:`True`.
    :param callback: If this is given, it should take the
                     :class:`OptionParser` instance, the :class:`Option`
                     instance, and the captured value (if any). If it returns
                     :obj:`None`, the value will be saved as normal. If it
                     returns anything else, it will not.
    :param parser_cls: The parser class to use. It defaults to
                       :class:`OptionParser`.
    """
    parser = parser_cls(optiondefs, interspersed_options=interspersed_options,
                        callback=callback)
    if defaults:
        parser.set_defaults(defaults)
    if argv is None:
        argv = sys.argv[1:]
    parser.parse(argv)
    return parser.option_values, parser.arguments
