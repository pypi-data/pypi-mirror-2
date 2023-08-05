"""
clap
====
Clap is a library written in Python for making command-line applications,
inspired by Denis Defreyne's Cri. It provides support for single-command or
multi-command applications.

:copyright: 2010 Matthew "LeafStorm" Frazier
:license:   MIT/X11, see COPYING for details
"""

__version__ = '0.7'

from clap.base import SingleBase, MultiBase, ScriptError
from clap.command import Command, command, DOC
from clap.help import HelpFormatter, IndentedHelpFormatter
from clap.parser import Option
