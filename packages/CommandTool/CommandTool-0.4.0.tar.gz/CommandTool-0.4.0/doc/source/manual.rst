Manual
++++++

CommandTool is a command line parser for Python in the same category as modules
such as ``getopt``, ``optparse``, ``argparse``. CommandTool differs from these
others in two ways:

    Firstly it is designed explicitly for the situation where you have one "main"
    command and a series of "sub-commands". An example of a program which uses this
    pattern is Mercurial which allows you to run a main command ``hg`` and a series
    of sub-commands such as ``status`` or ``commit``.
    
    Secondly, CommandTool builds in a separate step for converting the options and
    arguments to variables in your application rather than lumping the parsing and
    conversion into one step.

Just like the others, CommandTool can automatically generate help information
and automatically handle errors.

CommandTool isn't particularly useful if you aren't using sub-commands.
Although you can use it for single commands you might as well just learn
Python's built-in ``optparse`` module instead, it handles the single command
use case perfectly well.

Anatomy of a Command
====================

CommandTool allows you to specify both the main command and a series of
sub-commands in such a way that both the main command and the sub-command
chosen can each have their own options and arguments and CommandTool will work
out which options and args should be used where. Here's an example of a complex
command which will allow us to discuss the key features:

::

    program.py --logging error --help development.conf serve --one --two 2 three

Although it is hard to see at first glance, this command uses the ``serve``
subcommand. The options and arguments before the word ``serve`` are main
command options, those afterwards are sub-command options and arguments.

CommandTool uses a sophisticated algorithm to be able to tell which argument is
the sub-command, which options and arguments go where and which of the options
take values.

Example
=======

.. include :: ../../example/find/find.py
   :literal:

Some things this example doesn't show are that:

* Options without metavars can be used too. They come through as booleans in
  the ``opts`` argument to ``on_run()``.

* Variable numbers of arguments can be used. Just add an integer as the first
  item in the tuple that is the very last one on the arg spec. That integer
  referrs to the minimum number of extra arguments which should be allowed.

* Customising help

Tests
=====

Here are some expected behaviours of command tool:

::

    >>> from pprint import pprint
    >>> from commandtool import Cmd, handle_command, LoggingCmd
    >>> class Test(Cmd):
    ...     arg_spec=[
    ...         ('LETTERS', 'The letters to seach for'),
    ...     ]
    ...     option_spec = dict(
    ...         help = dict(
    ...             options = ['-h', '--help'],
    ...             help = 'display this message'
    ...         ),
    ...         config = dict(
    ...             options = ['-c', '--config'],
    ...             help = 'the config file to use',
    ...             metavar='CONFIG',
    ...         ),
    ...         start_directory = dict(
    ...             options = ['-s'],
    ...             help = 'a boolean option',
    ...         ),
    ...     )
    ...     help = {
    ...         'summary': 'search START_DIRECTORY for a filename matching LETTERS'
    ...     }
    ... 
    ...     def on_run(self, service, args, opts):
    ...         pprint(args)
    ...         pprint(opts)
    ... 
    >>> cmd = {
    ...     'test': Test(),
    ... }

Now some tests. First test help:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--help'])
    search START_DIRECTORY for a filename matching LETTERS
    Usage: doc.py [GLOBAL_OPTIONS] SUB_COMMAND [OPTIONS] LETTERS
    <BLANKLINE>
    Global options:
      -h --help             display this message
    <BLANKLINE>
    Sub-command 'test' options:
      -s                    a boolean option
      -c --config           the config file to use
      -h --help             display this message
    <BLANKLINE>
    Sub-command 'test' arguments:
      LETTERS               The letters to seach for
    <BLANKLINE>
    Type `doc.py --help' for a full list of sub-commands.

Options without arguments:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '-s', 'arg1'])
    ['arg1']
    {'help': False, 'start_directory': True}

Options with arguments:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--config', 'some.config', 'arg1'])
    ['arg1']
    {'config': 'some.config', 'help': False, 'start_directory': False}

Options with arguments containing spaces:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--config', 'some file with spaces.config', 'arg1'])
    ['arg1']
    {'config': 'some file with spaces.config',
     'help': False,
     'start_directory': False}


Here's a main command, we'll use ``Test()`` as a subcommand:

::

    >>> class Main(Cmd):
    ...     arg_spec=[
    ...         ('LETTERS', 'The letters to seach for'),
    ...     ]
    ...     option_spec = dict(
    ...         help = dict(
    ...             options = ['-h', '--help'],
    ...             help = 'display this message'
    ...         ),
    ...         config = dict(
    ...             options = ['-c', '--config'],
    ...             help = 'the config file to use',
    ...             metavar='CONFIG',
    ...         ),
    ...         start_directory = dict(
    ...             options = ['-s'],
    ...             help = 'a boolean option',
    ...         ),
    ...     )
    ...     help = {
    ...         'summary': 'Operations on files'
    ...     }
    ... 
    ...     def on_run(self, service, args, opts):
    ...         pprint(args)
    ...         pprint(opts)
    ... 
    >>> cmd = {
    ...     None: Main(),
    ...     'test': Test(),
    ... }


Now some tests. First test help:

::

    >>> res = handle_command(cmd, cmd_line_parts=['--help'])
    Operations on files
    Usage: doc.py [GLOBAL_OPTIONS] LETTERS SUB_COMMAND
    <BLANKLINE>
    Global options:
      -s                         a boolean option
      -c CONFIG --config=CONFIG  the config file to use
      -h --help                  display this message
    <BLANKLINE>
    Global arguments:
      LETTERS               The letters to seach for
    <BLANKLINE>
    Sub-commands:
      test                  search START_DIRECTORY for a filename matching
                            LETTERS
    <BLANKLINE>
    Type `doc.py LETTERS SUB_COMMAND --help' for help on individual commands.

Options without arguments:

::

    >>> res = handle_command(cmd, cmd_line_parts=['main arg 1', 'test', '-s', 'arg 1'])
    ['main arg 1']
    {'help': False, 'start_directory': False}
    ['arg 1']
    {'help': False, 'start_directory': True}

Options with arguments:

::

    >>> res = handle_command(cmd, cmd_line_parts=['main arg 1', 'test', '--config', 'some.config', 'arg 1'])
    ['main arg 1']
    {'help': False, 'start_directory': False}
    ['arg 1']
    {'config': 'some.config', 'help': False, 'start_directory': False}

Options with arguments containing spaces:

::

    >>> res = handle_command(cmd, cmd_line_parts=['main arg 1', 'test', '--config', 'some file with spaces.config', 'arg 1'])
    ['main arg 1']
    {'help': False, 'start_directory': False}
    ['arg 1']
    {'config': 'some file with spaces.config',
     'help': False,
     'start_directory': False}

You can also have sub-commands which take a range of arguments, say from 2 to 4 arguments. Here's an example:

::

    >>> class NewTest(Test):
    ...     arg_spec=[
    ...         (2, 'The letters to seach for', 'Not enough letters', 'LETTERS'),
    ...     ]
    >>> cmd = {
    ...     'test': NewTest(),
    ... }
    >>> res = handle_command(cmd, cmd_line_parts=['test', '--help'])
    search START_DIRECTORY for a filename matching LETTERS
    Usage: doc.py [GLOBAL_OPTIONS] SUB_COMMAND [OPTIONS] LETTERS
    <BLANKLINE>
    Global options:
      -h --help             display this message
    <BLANKLINE>
    Sub-command 'test' options:
      -s                    a boolean option
      -c --config           the config file to use
      -h --help             display this message
    <BLANKLINE>
    Sub-command 'test' arguments:
      LETTERS               The letters to seach for
    <BLANKLINE>
    Type `doc.py --help' for a full list of sub-commands.


This will ensure there are at least two arguments:

With 0 arguments:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--config', 'some file with spaces.config'])
    Error: Not enough letters
    Try `doc.py test --help' for more information.

With one argument:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--config', 'some file with spaces.config', 'arg 1'])
    Error: Not enough letters
    Try `doc.py test --help' for more information.

With two arguments:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--config', 'some file with spaces.config', 'arg 1', 'arg 2'])
    ['arg 1', 'arg 2']
    {'config': 'some file with spaces.config',
     'help': False,
     'start_directory': False}

With three arguments:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--config', 'some file with spaces.config', 'arg 1', 'arg 2', 'arg 3'])
    ['arg 1', 'arg 2', 'arg 3']
    {'config': 'some file with spaces.config',
     'help': False,
     'start_directory': False}

You can also have commands which take a range of arguments, say from 2 to 4 arguments. Here's an example:




You can use this "range of arguments" technique in both the main command and the sub_command.


Finally, you can specify arguments that start with ``--`` only in the subcommand, and only by adding ``--`` to the argument list, before the arguments you are adding. Here's an example:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--', '-- some file with dashes and spaces.config', 'arg 1', 'arg 2', 'arg 3'])
    ['-- some file with dashes and spaces.config', 'arg 1', 'arg 2', 'arg 3']
    {'help': False, 'start_directory': False}

It is better to design your API to not need arguments starting with ``--`` though.





