
An Example
==========

Below is a very simple main command which can either display a help message and
a list of sub-commands or set up the Python logging system. This command
doesn't take any arguments and uses the default help messages provided by
CommandTool. It also uses the ``to_internal()`` function to automatically
convert the parsed options to an internal data structure which is easier to
work with.

::

    >>> import getopt
    >>> import logging
    >>> from commandtool import handle_command, to_internal
    >>> from bn import AttributeDict
    >>>
    >>> def mainCmd():
    ...  
    ...     def convert(service, option_spec, parsed_args, parsed_options):
    ...         args = parsed_args, 
    ...         opts = to_internal(option_spec, parsed_options)
    ...         if opts.has_key('logging') and opts.logging not in ['debug', 'info', 'warning', 'error']:
    ...             raise getopt.GetoptError('Invalid log level %r'%opts.logging) 
    ...         return args, opts
    ...
    ...     def run(service, show_help, args, opts):
    ...         if opts.help:
    ...             print show_help(service)
    ...             return 1
    ...         if opts.logging:
    ...             print "Setting log level to ", opts.logging
    ...             logging.basicConfig(level=getattr(logging, opts.logging))
    ...         return 0
    ...
    ...     return AttributeDict(
    ...         arg_spec = [],
    ...         option_spec = {
    ...             'help': dict(
    ...                 options = ['-h', '--help'],
    ...                 help = 'display this message'
    ...             ),
    ...             'logging': dict(
    ...                 options = ['-l', '--logging'],
    ...                 help = 'Set the log level to one of debug|info|warning|error',
    ...                 metavar = 'LEVEL',
    ...             ),
    ...         },
    ...         help = {},
    ...         run = run,
    ...         convert = convert,
    ...     )

Let's also have a sub-command called ``echo`` which simply echos the converted
``opts`` and ``args`` it recieves:

::

    >>> def echoCmd():
    ...
    ...     def convert(service, option_spec, parsed_args, parsed_options):
    ...         args = parsed_args, 
    ...         opts = to_internal(option_spec, parsed_options)
    ...         return args, opts
    ...
    ...     def run(service, show_help, args, opts):
    ...         if opts.help:
    ...             print show_help(service)
    ...             return 1
    ...         print "Subcommand echo recieved: ", args, opts
    ...         return 0
    ... 
    ...     return AttributeDict(
    ...         arg_spec = [],
    ...         option_spec = {
    ...             'help': dict(
    ...                 options = ['-h', '--help'],
    ...                 help = 'display this message'
    ...             ),
    ...             'one': dict(
    ...                 options = ['-o', '--one'],
    ...                 help = 'set the one option'
    ...             ),
    ...             'two': dict(
    ...                 options = ['-t', '--two'],
    ...                 help = 'Set the two option to VALUE',
    ...                 metavar = 'VALUE',
    ...             ),
    ...         },
    ...         help = {},
    ...         run = run,
    ...         convert = convert,
    ...     )

Here's a program which can use these two commands. Notice that the command to
be used as the main command as specified under the key ``None``. For all other
commands the key will be used as the sub-command name.

::

    handle_command(
        commands={
            None: mainCmd(),
            'echo': echoCmd(),
        },
    )

If the ``convert()`` or ``run()`` functions need access to any configuration
you can design the command itself to take arguments. Since the ``convert()``
and ``run()`` functions are defined inside the outer function, they'll have
access to those variables too.

Testing the example
===================

The code for the example is available in the ``example`` directory of the
source distribution as ``program.py`` but we can also test it here by calling
``handle_command()`` with optional arguments ``program`` and ``cmd_line``. If
these aren't specified the ``handle_command()`` function would obtain the
information it needs from ``sys.argv``.

::

    >>> commands={
    ...     None: mainCmd(),
    ...     'echo': echoCmd(),
    ... }

First let's run the example from the beginning of this manual:

    >>> result = handle_command(
    ...     commands, 
    ...     program='program.py',
    ...     cmd_line='--logging error --help echo --one --two 2 three'
    ... )
    Usage: program.py [GLOBAL_OPTIONS] SUB_COMMAND 
    <BLANKLINE>
    Global options:
      -l LEVEL --logging=LEVEL  Set the log level to one of
                                debug|info|warning|error   
      -h --help                 display this message       
    Sub-commands:
      echo                                      
    <BLANKLINE>
    Type `program.py SUB_COMMAND --help' for help on individual commands.
    >>> result
    1

.. note :: 

   The ``<BLANKLINE>`` string is simply there so that the test system knows to
   test for a blank line, they aren't part of the output.

Because CommandTool has calculated that ``echo`` is the sub-command it is able
to split the options and arguments into two groups:

main command:
    ``--logging error --help``

echo command:
    ``--one --two 2 three``

The main command always get's run first and in this case it will set up logging
with the log level to ``error``. It knows that ``error`` isn't the sub-command
because the ``option_spec`` for the main command has a ``metavar`` argument for
the ``logging`` internal variable. The next option is ``--help``. This cauese
``opt.help`` to be set to ``True`` because of the conversion which occurs in
the main command's ``convert()`` method. Then the ``run()`` method is executed
the call to ``show_help()`` generates the help text which is then printed.

The return value from a command should always be a non-negative integer. ``0``
means that everything ran without an error and that the sub-command should now
be run, any other integer means an error occurred and the sub-command should
not be run. If you forget to return a value, then ``0`` is assumed. In this
case, because the text was printed we don't want the sub-command to be run so
``1`` is returned.

Let's run the same command but without the ``--help`` option:

::

    >>> result = handle_command(
    ...     commands, 
    ...     program='program.py',
    ...     cmd_line='--logging error echo --one --two 2 three'
    ... )
    Setting log level to  error
    Subcommand echo recieved:  (['three'],) {'help': False, 'two': '2', 'one': True}
    >>> result
    0

This time the main command is run but the help isn't printed. Instead the
``echo`` sub-command is executed. Let's look at the ``args`` and ``opts`` it
recieved more closely.

The sub-command part of the command line is ``--one --two 2 three``. If a
``metavar`` is specified in the options spec it means that the option takes an
argument. In this case ``--two`` takes an argument but ``--one`` doesn't. This
means that the value ``2`` is the value of the metavar for the ``--two`` option
which means that ``three`` is treated as an argument.

Behind the scenes the argument parsing is done by the ``getopt`` module. It
returns the options it has matched as a list of ``(option, value)`` pairs and
sets the value to ``''`` if the option doesn't take an argument. In this case
the parsed options look like this: ``[('--one', ''), ('--two', '2')]``. 

The sub-command's ``convert()`` function uses ``to_internal()`` to generate a
default representation of these options. This function treats any internal
varialbes associated with options that don't take arguments as being booleans.
If the option is present the internal variable is given the value ``True``,
otherwise ``False``. In this case the ``--one`` option is present but
``--help`` is not so the internal values associated with those options are
given the values ``True`` and ``False`` respectively. This is reflected in the
``opts`` recieved by ``run()`` as you can see from the example.


Building your own Command
=========================

In order to work out how to structure the command line options for your own
program you need to answer the following questions:

#. What are the sub-commands I need?
#. What are the internal variables used in each sub-command?
#. What options are needed to control each of the internal variables?
#. Are any of the options not optional? If they are they should be arguments.

To build your own command you should always start with the template below:

::

    from bn import AttributeDict
    from commandtool import to_internal
    import getopt

    def myCmd():
    
        def convert(service, option_spec, parsed_args, parsed_options):
            args = parsed_args
            process = to_internal(option_spec, parsed_options)
            opts = process.opts
            # Manually check the length of the args in the case of a
            # sub-command
            if len(args) < 2:
                raise getopt.GetoptError(
                    'Expected two arguments, arg1 and arg2'
                )
            elif len(args) > 2:
                raise getopt.GetoptError(
                    'Unexpected argument %r'%args[2]
                )
            return args, opts
    
        def run(service, show_help, args, opts):
            if opts.help:
                print show_help(service)
                return 1
            print "Subcommand recieved: ", (opts, args)
            return 0
    
        return AttributeDict(
            arg_spec = [
                # These are used in the help files.
                # If this is a main command, these are treated as compulsory, 
                # otherwise they are optional and must be checked in the 
                ('arg1', 'First imaginary argument'),
                ('arg2', 'Second imaginary argument'),
            ],
            # The option_spec specifies which options are associated with 
            # each internal variable
            option_spec = dict(
                help = dict(
                    options = ['-h', '--help'],
                    help = 'display this message'
                ),
                one = dict(
                    # You can specify as many options as you like for each 
                    # internal variable, as long as you don't use the same
                    # option for different internal variables.
                    options = ['-o', '--one', '-n'],
                    help = 'set the one option'
                ),
                two = dict(
                    options = ['-t', '--two'],
                    help = 'Set the two option to VALUE',
                    # If you specify a metavar, it means the option takes an
                    # optional argument
                    metavar = 'VALUE',
                ),
            ),
            help = {
                # Allows you to specify your own help text, substituted with
                # fragments such as the options list etc. All % signs should 
                # be escaped as %% to avoid a crash when the template is 
                # rendered.
                # If you leave start and end as None, values will be 
                # automatically generated
                # You'll need to delete some of these depending on whether 
                # this is a command or subcommand
                'template': """\
    %(sub_command)s - %(summary)s
    %(usage)s
    
    %(global_args)s

    %(global_options)s
    
    %(sub_commands)s
    
    %(sub_command_args)s
    
    %(sub_command_options)s
    
    %(tip)s""",
                # Used in the main command help to describe this command
                'summary': 'Example command',
            },
            run = run,
            convert = convert,
        )




Execution Analysis
==================

When a command is specified on the command line, execution flows like this:

* parse main program options and arguments
* the first argument after the ones we were expecting must be the sub-command, save it
* remove all the main program options and arguments from the command line and save it
* run the main command
* if the main command doesn't exit, continue parsing the sub-command
* parse the remaining parts of the command line
* run the sub-command with the parsed args and options

Each time a command is run (whether the main command or a sub-command) the following happens:

* a function is constructed which when called will generate an appropriate help screen
* the command's ``convert()`` function is called to take the parsed options and arguments for that command and return an internal data structure the application can use
* if during the convert process the data isn't valid a ``getopt.Getopt()`` exception is raised with a message explaining the problem, this gets displayed on the command line
* the command's ``run()`` function is called

The arguments passed to the ``convert()`` function are:

``service``
    An optional object passed throughout the CommandTool code

``option_spec``
    The options specification associated with the command run

``parsed_args``
    A list of strings representing the arguments parsed from the command line

``parsed_options``
    A list of ``(option, value)`` pairs, one for each option specified. If the option doesn't take a value, an empty string is used. eg ``[('--help', ''), ('--logging', 'error')]``

The arguments passed to the ``run()`` function are:

``service``
    An optional object passed throughout the CommandTool code

``show_help``
    A function which when called will return a help string suitable for printing out to display help

``args``
    A list of args returned from the ``convert()`` function. Often this is just the same as the ``parsed_args`` value passed to ``convert()``

``opts``
    An object returned from ``convert()`` representing the options specified. Often this is a dictionary where the keys are the internal variables specified in the ``option_spec`` for the command and the values are the values associated with those internal variables.

This is all much clearer when you see an example.




