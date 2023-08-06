Manual
++++++

Caution
=======

A CommandTool command's ``on_run()`` method has been replased with a more
powerfull ``run()`` method in the latest CommandTool. All the documentation
here referes to ``on_run()`` which is now deprecated and shouldn't be used. The
new CommandTool library is eniterly backwards compatible so all the
funcitonality described here still works, it is just that f you are starting
with new commands you should write them with ``run()`` instead.

Here's a quick summary of how ``run()`` is different.

::

    class MyCmd(Cmd):
        def run(self, cmd)
            # Arguments:
            cmd.args
            # Options:
            cmd.opts
            
You can also chain commands now and you will get the ``cmd`` object from the
command above the chain by accessing ``cmd.chain[-1]``.

Also, you can get the unprocessed ``cmd.raw_args`` and ``cmd.raw_opts`` if you
really need them.

Finally, ``Cmd`` classes are now *marble-like* in the sense that they can have
aliases, etc. They also have their own flow for integration with PipeStack so
that you can do:

::

    cmd.service.enter('pipe')

When specifying multiple commands you can now use a list of tuples rather than
a dictionary, or you can use an ordered dictionary (``from bn import
OrderedDict``) to keep them in a specific order for the help.

Finally, if you use a command with PipeStack, you can specify the class, rather
than an instance, so that PipeStack can pass an existing service.

See the ``gallery.command`` redis example for how you can use Pipes and
Commands together with flows.

Introduction
============



CommandTool is a command line parser for Python in the same category as modules
such as ``getopt``, ``optparse``, ``argparse``. CommandTool differs from these
others in two ways:

    Firstly it is designed explicitly for the situation where you have one "main"
    program and a series of "commands". An example of a program which uses this
    pattern is Mercurial which allows you to run a main command ``hg`` and a series
    of commands such as ``status`` or ``commit``.
    
    Secondly, CommandTool builds in a separate step for converting the options and
    arguments to variables in your application rather than lumping the parsing and
    conversion into one step.

Just like the others, CommandTool can automatically generate help information
and automatically handle errors.

CommandTool isn't particularly useful if you aren't using a set of commands.
Although you can use it for single commands you might as well just learn
Python's built-in ``optparse`` module instead, it handles the single command
use case perfectly well.

Anatomy of a Command
====================

CommandTool allows you to specify both the main program and a series of
commands in such a way that both the main program and the command
chosen can each have their own options and arguments and CommandTool will work
out which options and args should be used where. Here's an example of a complex
command which will allow us to discuss the key features:

::

    program.py --logging error --help development.conf serve --one --two 2 three

Although it is hard to see at first glance, this command uses the ``serve``
command. The options and arguments before the word ``serve`` are main
program options, those afterwards are command options and arguments.

CommandTool uses a sophisticated algorithm to be able to tell which argument is
the command, which options and arguments go where and which of the options
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

    >>> res = handle_command(cmd, cmd_line_parts=['--help'])
    No help summary specified
    Usage: doc.py [OPTIONS] COMMAND
    <BLANKLINE>
    Options:
      -h --help             display this message
    <BLANKLINE>
    Commands:
      test                  search START_DIRECTORY for a filename matching
                            LETTERS
    <BLANKLINE>
    Type `doc.py COMMAND --help' for help on individual commands.

Now sub-command help:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--help'])
    search START_DIRECTORY for a filename matching LETTERS
    Usage: doc.py [OPTIONS] test [OPTIONS] LETTERS
    <BLANKLINE>
    Command 'test' options:
      -s                    a boolean option
      -c --config           the config file to use
      -h --help             display this message
    <BLANKLINE>
    Command 'test' arguments:
      LETTERS               The letters to seach for
    <BLANKLINE>
    Type `doc.py --help' for a full list of commands.

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


Here's a main program, we'll use ``Test()`` as a command:

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
    Usage: doc.py [OPTIONS] LETTERS COMMAND
    <BLANKLINE>
    Options:
      -s                         a boolean option
      -c CONFIG --config=CONFIG  the config file to use
      -h --help                  display this message
    <BLANKLINE>
    Global arguments:
      LETTERS               The letters to seach for
    <BLANKLINE>
    Commands:
      test                  search START_DIRECTORY for a filename matching
                            LETTERS
    <BLANKLINE>
    Type `doc.py LETTERS COMMAND --help' for help on individual commands.

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

You can also have commands which take a range of arguments, say from 2 to 4 arguments. Here's an example:

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
    Usage: doc.py [OPTIONS] test [OPTIONS] LETTERS
    <BLANKLINE>
    Command 'test' options:
      -s                    a boolean option
      -c --config           the config file to use
      -h --help             display this message
    <BLANKLINE>
    Command 'test' arguments:
      LETTERS               The letters to seach for
    <BLANKLINE>
    Type `doc.py --help' for a full list of commands.

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




You can use this "range of arguments" technique in both the main program and the command.


Finally, you can specify arguments that start with ``--`` only in the command, and only by adding ``--`` to the argument list, before the arguments you are adding. Here's an example:

::

    >>> res = handle_command(cmd, cmd_line_parts=['test', '--', '-- some file with dashes and spaces.config', 'arg 1', 'arg 2', 'arg 3'])
    ['-- some file with dashes and spaces.config', 'arg 1', 'arg 2', 'arg 3']
    {'help': False, 'start_directory': False}

It is better to design your API to not need arguments starting with ``--`` though.


Multiple Options
================

Sometimes it is helpful to have commands that take more than one option of the
same name. In such cases the values returned for those options by CommandTool
will be lists rather than strings. If the option has a metavar associated with
it, it will be a list of values, if not it will be a list of ``True``
statements, one for each time the option appears. To mark an option as taking
multiple values you use ``multiple=True``. Here's an example:

::

    >>> class MultiTest(Cmd):
    ...     option_spec=dict(
    ...         boolean = dict(
    ...             options = ['-b'],
    ...             help = 'multiple boolean options',
    ...             multiple=True,
    ...         ),
    ...         val = dict(
    ...             options = ['--val'],
    ...             help = 'option that takes a variable and can be used multiple times',
    ...             metavar='CONFIG',
    ...             multiple=True,
    ...         ),
    ...     )
    ...     def on_run(self, state, args, opts):
    ...         pprint(opts)
    ...
    >>> cmd = {
    ...     'test': MultiTest(),
    ... }
    >>> res = handle_command(cmd, cmd_line_parts=['test', '-b', '-b', '-b', '--val', 'one', '--val', 'two'])
    {'boolean': [True, True, True], 'val': ['one', 'two']}
    >>> res = handle_command(cmd, cmd_line_parts=['test'])
    {'boolean': []}


Nested Commands
===============

Sometimes you may want to have a command under an existing command. For
example, in PipeStack you can have lots of commands, one of which is the
``config`` command. The ``config`` command has its own commands such as ``set``
and ``get``. Here's how you can set this up:

::

    >>> class Config(Cmd):
    ...     help = dict(summary='Config')
    >>> class Get(Cmd):
    ...     help = dict(summary='Get')
    ...     def on_run(self, state, args, opts):
    ...         pprint(opts)
    >>> class Set(Cmd):
    ...     help = dict(summary='Set')
    ...     def on_run(self, state, args, opts):
    ...         pprint(opts)
    >>> cmd = {
    ...     None: Cmd(),
    ...     'config': {
    ...         None: Config(),
    ...         'get': Get(),
    ...         'set': Set(),
    ...     }
    ... }
    >>> res = handle_command(cmd, cmd_line_parts=['--help'])
    No help summary specified
    Usage: doc.py [OPTIONS] COMMAND
    <BLANKLINE>
    Options:
      -h --help             display this message
    <BLANKLINE>
    Commands:
      config                Config
    <BLANKLINE>
    Type `doc.py COMMAND --help' for help on individual commands.
    >>> res = handle_command(cmd, cmd_line_parts=['config', '--help'])
    Config
    Usage: doc.py config [OPTIONS] COMMAND
    <BLANKLINE>
    Options:
      -h --help             display this message
    <BLANKLINE>
    Commands:
      set                   Set
      get                   Get
    <BLANKLINE>
    Type `doc.py config COMMAND --help' for help on individual commands.
    >>> res = handle_command(cmd, cmd_line_parts=['config', 'get', '--help'])
    Get
    Usage: doc.py config [OPTIONS] get [OPTIONS]
    <BLANKLINE>
    Command 'get' options:
      -h --help             display this message
    <BLANKLINE>
    Type `doc.py config --help' for a full list of commands.
    >>> res = handle_command(cmd, cmd_line_parts=['config', 'get'])
    {'help': False}



Exit Status
===========

Any value you return from ``on_run()`` on a command is eventually returned from
``handle_command()``. If you raise a ``getopt.GetoptError`` a value of ``1`` is
assumed. If you don't return anything or return ``None``, a value of ``0`` is
assumed. You can therefore use the return value from ``on_run()`` as an exit
status to pass to ``sys.exit()`` to set as the result code from running the
command line application.

Sometimes you want to print an error message and still set a non-zero return
code. As long as your code is set up to pass the return value of
``handle_command()`` to ``sys.exit()`` you can do this by returning a non-zero
integer from ``on_run()``.

Here's an example:

::

    >>> class Get(Cmd):
    ...     help = dict(summary='Get')
    ...     def on_run(self, state, args, opts):
    ...         print "Error: this is an example error"
    ...         return 1
    >>> cmd = {
    ...     None: Get(),
    ... }
    >>> res = handle_command(cmd, cmd_line_parts=['get'])
    Error: this is an example error
    >>> print res
    1




