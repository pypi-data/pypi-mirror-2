"""
clap.base
=========
This actually runs the programs in question. You have two basic types:
:class:`SingleBase` and :class:`MultiBase`. :class:`SingleBase` is
instantiated with a single command, and the base is just responsible for
handling help and management for that command. :class:`MultiBase` can have
multiple commands added to it with the :meth:`~MultiBase.add_command` method,
as well as global options, and dispatches to them based on the first
non-option argument.

:copyright: 2010 Matthew "LeafStorm" Frazier
:license:   MIT/X11, see COPYING for details
"""
import itertools
import os.path
import sys
import traceback
from clap.command import Command
from clap.help import HelpFormatter
from clap.parser import Option, OptionParser, OptionParsingError, parse

class ScriptError(BaseException):
    """
    If your command encounters an error due to something the user did, raise
    :class:`ScriptError` with the error message, like this::
    
        raise ScriptError("can't read from a file and stdin at the same time")
    
    The Base will automatically display it as it would a usage error, without
    the full traceback listing.
    
    :param msg: The message to display to the user. The preferred style is
                lowercase with no message at the end.
    :param status: The status code to exit with. The default is 1.
    """
    def __init__(self, msg, status=1):
        self.msg = msg
        self.status = status
    
    def __str__(self):
        return self.msg


class Base(object):     # no, I'm not calling it BaseBase
    """
    This is the base class for Bases. It handles the stuff common to both
    kinds of Base.
    """
    #: The exit code to use when a traceback is caught. The default is 120,
    #: because it is a nice round number out of the way of special codes.
    TRACEBACK_EXIT_CODE = 120
    
    #: The subclass of :class:`clap.help.BaseHelpFormatter` to format help
    #: with.
    help_formatter_class = HelpFormatter
    #: The parser class to parse arguments with.
    parser_class = OptionParser
    
    def run_command(self, cmd, *args, **kwargs):
        """
        This will run a command with the given positional and keyword
        arguments, automatically catching :class:`ScriptError` and other
        kinds of :class:`Exception`. If you want to provide additional
        arguments to your commands, you can override this method and use
        ``Base.run_command(self, cmd, whatever)``. (The actual :class:`Base`
        classes always call it with the options dictionary and arguments
        list.)
        
        :param cmd: The command to run.
        :param args: Extra positional arguments.
        :param kwargs: Extra keyword arguments.
        """
        try:
            cmd.run(*args, **kwargs)
        except ScriptError, exc:
            self.usage_error(exc.msg, cmd)
            self.exit(exc.status)
        except Exception, exc:
            self.print_traceback(exc)
            self.exit(self.TRACEBACK_EXIT_CODE)
    
    def print_traceback(self, err=None):
        """
        This is called with the exception when an exception inheriting from
        :class:`Exception` is caught while the command is being run. By
        default, it displays "An error has occurred." and prints the
        traceback. You may want to override this so you can hide the traceback
        from your users, or display a message about the traceback.
        """
        print("An error has occured.")
        traceback.print_exc()
        
    def parse(self, *args, **kwargs):
        """
        This invokes the :func:`clap.parser.parse` function with the given
        arguments and keyword arguments, but it catches errors and uses the
        parser class specified by :attr:`parser_class`.
        """
        try:
            return parse(parser_cls=self.parser_class, *args, **kwargs)
        except OptionParsingError, e:
            self.usage_error(str(e))
            self.exit(1)
        
    def exit(self, code=0):
        """
        This is called to exit the program, optionally with an error code. You
        can override this to do something before shutting the program down.
        """
        sys.exit(code)


class SingleBase(Base):
    """
    This kind of Base accepts one Command, and you give it during
    construction. To run it, you call :meth:`run` with the arguments.
    
    By default, its :attr:`use_help` attribute is True. This injects a
    ``-h``/``--help`` option into the options list which will display help
    when encountered.
    
    :param command: The :class:`clap.command.Command` to use.
    :param program_name: The name to use for the program in usage messages. It
                         defaults to the basename of the script's path.
    """
    #: Whether to add a "help" option or not
    use_help = True
    #: The message to print on a usage error if :attr:`use_help` is
    #: :obj:`False`.
    help_message = None
    
    def __init__(self, command, program_name=None):
        self.program_name = program_name or os.path.basename(sys.argv[0])
        self.command = command()
        self.command.set_base(self)
    
    def run(self, argv=None):
        """
        This is the entry point for running the program. Call this with the
        command-line arguments (or not, in which case it will use
        ``sys.argv[1:]``), and it will handle parsing options and invoking
        the command.
        """
        if argv is None:
            argv = sys.argv[1:]
        if self.use_help:
            self._help_option = Option('h', 'help', desc="display usage "
                                       "information")
            self.options = (self._help_option,) + self.command.all_options
        else:
            self.options = self.command.all_options
        options, arguments = self.parse(self.options, argv,
            defaults=self.command.all_defaults,
            interspersed_options=self.command.interspersed_options,
            callback=self._callback
        )
        self.run_command(self.command, options, arguments)
    
    def _callback(self, parser, option, value=None):
        if self.use_help and option is self._help_option:
            self.show_help()
            self.exit()
        else:
            return self.callback(parser, option, value)
    
    def callback(self, parser, option, value=None):
        """
        This is used as a callback when parsing options. If it returns
        something other than :obj:`None`, the value will not be stored.
        
        :param parser: The :class:`clap.parser.OptionParser` parsing the
                       options.
        :param option: The :class:`clap.parser.Option` instance being
                       processed.
        :param value: The value captured as the option's argument (or
                      :obj:`None` if it wasn't found).
        """
        pass
    
    def usage_error(self, msg, command=None):
        print("Usage: %s %s" % (self.program_name, self.command.usage))
        if self.use_help:
            print("(type %s --help for more information)" % self.program_name)
        elif self.help_message:
            print self.help_message
        print("")
        print("%s: %s" % (self.program_name, msg))
    
    def show_help(self):
        fmt = self.help_formatter_class()
        fmt.usage('%s %s' % (self.program_name, self.command.usage))
        fmt.text(self.command.long_desc)
        fmt.start_section("Options")
        fmt.option_list(self.options)
        fmt.end_section()
        del fmt


class HelpCommand(Command):
    """
    This is the default help command used with the :class:`MultiBase`. It will
    print out a list of commands and global options when used alone, and a
    command description and list of command options when used with a command
    name.
    """
    name = 'help'
    usage = '[OPTIONS] [COMMAND]'
    short_desc = "Displays help on commands"
    long_desc = """\
This prints help for the application. If no command is given, it will print \
general application help and global options. If a command is given, it will \
print the help for that command, and the command's specific options.
    """
    
    def run(self, options, arguments):
        fmt = self.base.help_formatter_class()
        if arguments:
            command_name = arguments[0]
            try:
                command = self.base.command_map[command_name]
            except KeyError:
                raise ScriptError("command %s does not exist" % command_name)
            fmt.usage('%s [OPTIONS] %s %s' %
                      (self.base.program_name, command.name, command.usage))
            if command.long_desc:
                fmt.text(command.long_desc)
            elif command.short_desc:
                fmt.text(command.short_desc)
            fmt.start_section('Options')
            fmt.option_list(command.options)
            fmt.end_section()
            fmt.start_section('Global Options')
            fmt.option_list(self.base.global_options)
            fmt.end_section()
        else:
            fmt.usage('%s [OPTIONS] COMMAND ...' % self.base.program_name)
            if self.base.long_desc:
                fmt.text(self.base.long_desc)
            fmt.start_section("Commands")
            fmt.cmd_list((cmd.name, cmd.short_desc)
                         for cmd in self.base.commands)
            fmt.end_section()
            fmt.start_section("Global Options")
            fmt.option_list(self.base.global_options)
            fmt.end_section()


class MultiBase(Base):
    """
    This base handles programs with multiple "subcommands", like hg, git, or
    svn. You add commands with the :meth:`add_command` method. Like
    :class:`SingleBase`, call :meth:`run` to run the program.
    
    By default, its :attr:`use_help` attribute is True. This injects a
    ``help`` command into the commands list, which will give information on
    the entire program or just a certain command.
    
    :param program_name: The name to use for the program in usage messages. It
                         defaults to the basename of the script's path.
    """
    #: Whether to add a "help" option or not
    use_help = True
    #: The message to print on a usage error if :attr:`use_help` is
    #: :obj:`False`.
    help_message = None
    
    #: Options that apply to all commands.
    global_options = ()
    #: Defaults for global options.
    global_defaults = {}
    #: A long description of the program.
    long_desc = None
    
    def __init__(self, program_name=None):
        self.program_name = program_name or os.path.basename(sys.argv[0])
        self.commands = []
        self.command_map = {}
    
    def add_command(self, command):
        """
        This adds a command to the commands list. The command's name will
        override other commands already named or aliased as such, but its
        aliases will not.
        
        :param command: Either a :class:`~clap.command.Command` class or an
                        instance thereof.
        """
        command = command()
        command.set_base(self)
        self.commands.append(command)
        self.command_map[command.name] = command
        for alias in command.aliases:
            self.command_map.setdefault(alias, command)
    
    def run(self, argv=None):
        """
        This is the entry point for running the program. Call this with the
        command-line arguments (or not, in which case it will use
        ``sys.argv[1:]``), and it will handle parsing options and invoking
        the command.
        """
        if argv is None:
            argv = sys.argv[1:]
        if self.use_help:
            self.add_command(HelpCommand)
        g_options, first_arguments = self.parse(self.global_options, argv,
            defaults=self.global_defaults,
            interspersed_options=False,
            callback=self.callback
        )
        if len(first_arguments) < 1:
            self.usage_error("no command was given")
            self.exit(1)
        command_name = first_arguments[0]
        try:
            command = self.command_map[command_name]
        except KeyError:
            self.usage_error("command %s does not exist" % command_name)
            self.exit(1)
        all_options = tuple(self.global_options) + command.all_options
        g_options.update(command.defaults)
        options, arguments = self.parse(all_options, first_arguments[1:],
            defaults=g_options,
            interspersed_options=command.interspersed_options,
            callback=self.callback
        )
        self.run_command(command, options, arguments)
    
    def callback(self, parser, option, value=None):
        """
        This is used as a callback when parsing options. If it returns
        something other than :obj:`None`, the value will not be stored.
        
        :param parser: The :class:`clap.parser.OptionParser` parsing the
                       options.
        :param option: The :class:`clap.parser.Option` instance being
                       processed.
        :param value: The value captured as the option's argument (or
                      :obj:`None` if it wasn't found).
        """
        pass
    
    def usage_error(self, msg, command=None):
        if command:
            print("Usage: %s %s %s" %
                  (self.program_name, command.name, command.usage))
            if self.use_help:
                print("(type %s help %s for more information)" %
                      (self.program_name, command.name))
            elif self.help_message:
                print self.help_message
            print("")
            print("%s: %s" % (self.program_name, msg))
        else:
            print("Usage: %s [OPTIONS] COMMAND" % self.program_name)
            if self.use_help:
                print("(type %s help for more information)" %
                      self.program_name)
            elif self.help_message:
                print self.help_message
            print("")
            print("%s: %s" % (self.program_name, msg))
