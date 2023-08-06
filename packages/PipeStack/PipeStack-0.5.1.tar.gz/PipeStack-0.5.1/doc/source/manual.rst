Manual
++++++

ToDo:

* Write some examples of the different types of Pipe
* Test that flows can be interrupted with an ensure decorator.

PipeStack is a new approach to building applications (including servers,
daemons, cron jobs etc.). PipeStack is a bit like WSGI, a bit like Paste and a
bit like Pylons but not quite like any of them.

In PipeStack your entire application is represented by a stack of *pipes*. Each
time your application has to do something, a *bag* passes through each of the
pipes in turn. Certain pipes add *marbles* to the bag whilst other pipes just
change the marbles that are already present. At any point a pipe can add another pipe
to the stack and send the bag through that too so that the pipestack can change
as the bag passes through it. Pipes can also stop the bag and send it back down
the pipestack. As the bag passes back down the stack, the pipes also have an
oppurtunity to change the marbles present. If none of the pipes send the bag
back it will get to the end of the pipestack where an optional ``run()`` script
is executed before the bag is sent back down the pipes. If an exception occurs 
the bag immediately passes back down the pipes but each pipe is notified that 
an error condition exists so that it has an opportunity to handle the error.

In this way a pipestack is a lot like a Unix pipeline except for two main
differences. In a pipestack:

* the thing that is piped is a bag of marbles rather than a character stream
* a pipestack is two-way, a pipeline is one way. That is to say that in a pipe
  stack the bag goes back through each pipe starting with the most recent one
  whereas in a pipeline the character stream reaches the end and is displayed
  without being passed back through each command.

Getting Started
===============

Here's a simple pipestack application that provides a database pipe (we're
actually using the ``pipestack.pipe:MarblePipe`` base class instead of a real
database pipe so that we don't need an actual database present for the examples
to run!):

::

    >>> from pipestack.app import App, pipe, do_nothing
    >>> class SimpleApp(App):
    ...     pipes = [
    ...         pipe('database', 'pipestack.pipe:MarblePipe')
    ...     ]

As you can see all PipeStack applications are derived from
``pipestack.app.App``. In this case our app is defined as the ``SimpleApp``
class. ``SimpleApp`` has one pipe which is specified with the ``pipe()``
function. All pipes have a unique name which is passed as the first argument of
the function and either a ``Pipe`` class or a string representing the import
location of a ``Pipe`` class. 

The advantage of using a string as the second argument is that the module will
only be imported if the pipe is needed. This has two advantages:

* You can design PipeStack applications where different pipes are used
  depending on the environment. This means end users will not have to install
  modules they don't need, just because your application references them.

* It can be slightly faster, for example in command line apps only the pipes
  that are needed for the particular set of tasks that need to be performed
  based on the command line options will need to be imported.

The advantage of using an actual object is that:

* You'll get a better error message if there was a problem importing the module

The ``pipe()`` function spec looks like this:

::

    pipe(name, object, aliases, *k, **p)

``name`` 
    A unique string representing the name of the pipe

``object``
    A class or string representing a ``Pipe``

``aliases=None``
    An optional dictionary specifying the names this pipe should use to access
    other pipes it depends on. This is so that you can name your pipes differently
    and still have other pipes which depend on them able to find the pipes they
    need. More on this in a minute.

``*k`` and ``**p``
    Any extra arguments you specify are passed straight onto the ``Pipe`` the
    first time it is initialised. Pipes only get intialised once, no matter how
    many times a pipe is used. Ordinarily there is no need to add extra arguments.
    Pipes are designed to be configured from a config file.


Let's create an instance of our application:

::

    >>> app = SimpleApp()

To create a bag and begin sending it down the a stack of pipes we use the
``start_flow()`` method:

::

    >>> app.start_flow()

Behind the scenes PipeStack created a new bag but because it there weren't any
pipes specified and because no terminator script was chosen to run, not a lot
happened.

The ``start_flow()`` function takes these arguments:

``bag=None``

    An existing bag containing marbles to send through the pipes. If not
    specified or the value is ``None``, PipeStack will create a new empty bag for
    you. Internally a bag is just a ``bn.AttributeDict`` instance. There are some
    restrictions on the attributes and keys a ``bag`` can have because PipeStack
    may replace some of them. The reserved keys can be determined like this:

    :: 

        >>> from pipestack.app import reserved
        >>> reserved
        ['command', 'enter', 'app', 'interrupt_flow', 'pipe', 'aliases', 'default_aliases', 'name']

``ensure=[]``

    This is a list of strings representing pipe names which PipeStack should
    send the bag through.  PipeStack will send the bag through each in turn unless
    any of them interrupts the flow at which point PipeStack will send the bag
    through each of the pipes that it has already been through in reverse order
    starting with the one it entered before the flow was interrupted. Pipes can
    only be specified once.
    
    There are occasions when you just want all pipes to be entered in the order
    They are specified in the class definition for the ``App``. In this case you
    Can use ``app.default_pipeline``. Later on you'll learn about the
    ``app.exclude`` property. Any pipes specified in ``exclude`` are not considered
    Part of the default pipeline.

``run=None``

    A terminator is any Python object which takes a bag as its only argument.
    The terminator is run in the case when the bag passes through all the pipes
    specified by ``ensure`` (as well as any pipes which those pipes
    dynamically add to the pipeline) but before the bag is passed back down the
    pipeline. The terminator is only run if none of the pipes interrupt the flow.

    Technically speaking there is no need for terminators because you can always
    add a pipe at the end of the stack which always interrupts the flow. Pipes
    are slightly harder to write than simple Python functions though so 
    terminator functionality is provided as a convenience if you wish to use it.

Let's start another flow, this time one that uses the default pipeline and
which runs a terminator:

::

    >>> def terminator(bag):
    ...     if bag.has_key('database'):
    ...         print "Got to the end with the database pipe"
    ...     else:
    ...         print "The database marble is NOT present"
    ...
    >>> # Just so you can see what the default pipeline contains:
    >>> app.default_pipeline
    ['database']
    >>> # Now start the flow:
    >>> app.start_flow(ensure=app.default_pipeline, run=terminator)
    Got to the end with the database pipe

As you can see, this time the terminator function is run and because the
``bag`` has already passed through the ``database`` pipe, the ``database``
marble is present.

.. tip ::

    Marbles are always accessed from the ``bag`` with the same name as the pipe
    which added them.

Sometimes you want more control over the pipes that the bag is sent through. In
these cases you need to be able to dynamically add pipe to the pipeline as the
flow is happening. To do this you need to call ``bag.enter()`` with the name of
the pipe. You cannot send the bag through the same pipe twice so if you call
``bag.enter()`` for a pipe that has already been entered you will get an
exception.

Here's an example where we don't use the default pipeline so the ``database``
marble is not automatically added to the bag by the time the terminator is run:
 
::

    >>> def terminator(bag):
    ...     if bag.has_key('database'):
    ...         print "Got to the end with the database pipe"
    ...     else:
    ...         # We haven't passed the bag through the default pipeline
    ...         # so this is what will be executed
    ...         bag.enter('database')
    ...         print "Sent the bag through the database pipe"
    ...     try:
    ...         # This will fail when we try it because the bag has already
    ...         # entered the database pipe
    ...         bag.enter('database')
    ...     except Exception, e:
    ...         print 'Error: ', e
    ...
    >>> app.start_flow(run=terminator)
    Sent the bag through the database pipe
    Error:  The bag has already entered the 'database' pipe

A ``bag`` instance also has these methods and properties:

``enter()``
    Takes a string representing the name of the pipe as the only argument. When
    called, the pipe specified is added to the pipeline and the bag is immediately
    passed through it. If the pipe is a marble pipe, the marble will then
    immediately be available as an attribute of the bag with a name matching the
    name of the pipe. You can not get the bag to enter a pipe it has already entered.

``interrupt_flow()``
    application_handled=False, error_handled=False)``

``app``
    This is the ``app`` instance which the bag is associated with. In this case
    it is our instance of ``SimpleApp``. The ``bag.app`` object is usually used for
    access to the raw options a pipestack application is configured with or, more
    commonly, the corresponding converted config options. You'll learn about these
    later.

Marbles
    The bag will also contain a property for each marble the bag contains

It can be quite tedious to constantly check whether the bag already has a
particular marble so PipeStack provides a series of decorators to ensure the
bag has been sent through specific pipes before a function or method is run.
Here's the first example but using the ``@ensure`` decorator instead of a
default pipeline:

::

    >>> from pipestack.ensure import ensure_function_bag as ensure
    >>>
    >>> @ensure('database')
    ... def terminator(bag):
    ...     if bag.has_key('database'):
    ...         print "Got to the end with the database pipe"
    ...     else:
    ...         print "The database marble is NOT present"
    ...
    >>> app.start_flow(run=terminator)
    Got to the end with the database pipe

Once again the ``database`` marble is present by the time the terminator
function is run.

Dealing with Configuration
==========================

Each pipe is designed to be configured from a set of options. The options for
the pipestack we've used so far might look like this:

::

    >>> option = {
    ...     u'database': {
    ...         u'plugin': 'sqlite',
    ...         u'database': ':memory:',
    ...     },
    ...     # Options for other pipes would go here...
    ... }

As you can see, the structure is a nested dictionary where the keys of the
outer dictionary match the names of the pipes and the keys of the inner
dictionary are the options for that pipe. Not all pipes take configurtaion
options. In this case we only have one pipe which requires configuration.

You can pass the options to the app when you instantiate it like this:

::

    >>> app = SimpleApp(option)

Pipes and other parts of your application can then access the raw options as
``bag.app.option.<pipe>`` or the configuration for a pipe from
``bag.app.config.<pipe>``. Both the ``option`` and ``config`` properties are
``bn.AttributeDict`` instances so you can also access options and config for
the pipe as so: ``bag.app.option[pipe]`` ``bag.app.config[pipe]``

To summarise, ``App`` instances have the following properties which are
designed to be accessed publicly:

``option``
    The raw (unicode) options to be used when each pipe is instantiated. The
    structure is a dictionary where the keys are pipe names and the values are
    dictionaries containg the options for each pipe. The options for each pipe have
    values which are unicode strings and keys which are strings in the format
    understood by the NestedRecord package. In simple cases these can just be
    strings like ``host`` or ``directory`` but in more complex cases you can use
    strings such as ``smtp.host`` or ``person[0].name`` so that when the pipe
    parses the options it can create sophisticated nested data structures for its
    configuration.

``config``
    This is a dictionary similar to ``option`` where the keys are the names of
    the pipes. It starts off empty but as pipes are instantiated for the first time
    they will add their converted options here as Python objects.

``api_version``
    This is a tuple of integers representing the API version used. The current
    API version is 0.8.0:

    ::

        >>> app.api_version
        (0, 8, 0)

The first time a pipe is used it will parse its options and place the 
converted Python objects in the config.

With a config file
------------------

It is often more useful to allow the user to specify options in a config file
than to specify options manually in Python code. ``App`` instances have a
``parse_config()`` method for just this task.

You would use it like this:

::

    app = SimpleApp()
    app.parse_config('/path/to/config')
    app.start_flow(...)

Notice that instead of passing the options directly to the ``SimpleApp``
constructor, you call ``parse_config()`` with the path to the config file you
wish to parse the options from. ``parse_config()`` will set the ``.option``
attribute and from then on the ``app`` instance will behave as before.

The config file must be in a format understood by ConfigConvert with all
options preceeded by the name of the pipe to which they apply. For example:

::

    # This is a comment, it will be ignored. Blank lines are also ignored.

    database.host = localhost
    database.plugin = psycopg2
    database.database = test

    mail.smtp.host = mail.example.com
    mail.smtp.username = foo
    mail.smtp.password = bar

See the ConfigConvert documentation for full details including how to deal with
multiline strings, but one important point is that there must be exactly
**one** space either side of the ``=`` sign. Extra spaces on the right will be
prepended onto the string associated with the option. 

Dealing with Logging
====================

PipeStack is rather strict about logging. It will use Python's ``warning``
module to warn you of any pipe that is used in an application which doesn't
have a corresponding logger set up for it.

Usually you'll use a ``logging.conf`` file or set up logging some other way.

Here's an example showing one way of using logging:

.. include :: ../../example/log_example.py
   :literal:

Without logging setup you see a warning message when the database pipe is used
and no log messages. With logging you don't get the warning message but you do
see the debug messages. You can adjust the verbosity of log messages by
changing the log level to ``logging.INFO`` or ``logging.WARN``.

PipeStack just uses Python's standard logging tools. See Python's ``logging``
module documentation for full information on the different ways these log
messages can be handled.

Using a logging config file
---------------------------

Although we won't go into the full details of Python's ``logging`` module, one
feature which is handy is the ability to specify a logging setup in a config
file.

Here's a sample config file for logging to the standard error stream called ``stderr.logging``:

::

    # Logging configuration
    
    [loggers]
    keys = root,pipestack,database
    
    [logger_root]
    level = WARNING
    handlers = console
            
    [handlers]
    keys = console
    
    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic
    propagate = 1
    
    [formatters]
    keys = generic
    
    [formatter_generic]
    format = %(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] %(message)s
    datefmt = %H:%M:%S
    
    # PipeStack logging
    
    [logger_pipestack]
    level = WARNING
    handlers = 
    qualname = flows
    propagate = 1
    
    [logger_database]
    level = WARNING
    handlers = 
    qualname = httpkit.service.wsgi
    propagate = 1


As you can see it is in two parts. The first part is configuration for the
Python logging system itself, the second part is the important part and it
specifies how the messages from PipeStack and key pipes should be handled.
Let's look at one of the handlers in the second part in more detail:

::

    [logger_database]
    level = WARNING
    handlers = 
    qualname = databasepipe
    propagate = 1

The only parts of this configuration you should change are marked with a word
in brackets below:

::

    [logger_(pipe name)]
    level = (log level)
    handlers = 
    qualname = (root logger)
    propagate = 1

In this example *pipe name* is ``database``, *log level* is ``WARNING`` and the
*root logger name* is ``databasepipe``. You shouldn't change anything else. In
particular you should always leave ``propagate`` as ``1`` and ``handlers``
empty. This will ensure that the messages get handled correctly.

.. caution ::

    Watch the spelling of ``propagate``. If you get it wrong things won't work
    and you won't get a warning from Python's logging system.

pipe name
    The name of the pipe which this section configures. For example
    if you accessed the service as ``bag.database`` in your application then
    ``database`` would be the service name.

log level
    The allowed levels are ``ERROR``, ``WARNING``, ``INFO``, ``DEBUG`` and
    ``NOTSET``. It is not wise to set the level to ``ERROR`` otherwise you
    could miss important warnings from the application. Most developers will
    log key messages at the ``INFO`` level and very verbose debugging messages
    to at the ``DEBUG`` level so if you want to enable log output from a
    particular service you should set the level to ``DEBUG`` or ``INFO``.

root logger
    This is the name of the logger to log messages from. Unless the developer
    of the module has done something unusual, the logger name is usually the same
    as the module name of the module where the log messages originate.  For
    example, the ``database`` pipe here comes from the ``databasepipe`` module so
    the root logger will usually be named ``databasepipe``. When writing Pipes 
    it is important that the logger names are always the same as the module names
    the loggers are for. Not all Python code follows this convention though 
    so on occasion you will need to investigate what the root logger should be
    for a particular piece of code. There is `more about root loggers in the Python docs <http://docs.python.org/library/logging.html#module-level-functions>`_.

You can use these setups by changing the two lines in the logging example from
this:

::

    import logging
    logging.basicConfig(level=logging.DEBUG)

to this:

::

    import logging
    logging.fileConfig('stderr.logging')

The beauty of using a config file is that it makes it very easy to control the
log output for various different pipes so that you can get more detailed log
messages for an area you are trying to debug without getting detailed messages
from other pipes. 

Changing the log levels
-----------------------

There are two ways to change the log levels. If you want to change the log
level for everything, change this section:

::

    [logger_root]
    level = WARNING
    handlers = console

so that ``level`` is the level of your choice.

If you just want to change the logging level for a particular pipe, change its
log level. For example:

::

    [logger_database]
    level = INFO
    handlers = 
    qualname = databasepipe
    propagate = 1

Messages for a particular pipe will be logged at whichever the lower log level
of the ``logger_root`` or ``logger_<pipe>`` is.

Adding a logging for a pipe
----------------------------

When you add a new pipe to PipeStack you should also add another logging
section. First add the name of the service to the ``keys`` variable of the
``[loggers]`` section and then add a handler section.

Here's an example for adding looging for the ``url`` service which you'll
need if you are setting up a dynamic application with URL routing:

::

    # Logging configuration
    
    [loggers]
    keys = root,pipestack,database,url

    ...

    # PipeStack logging
    
    ...
    
    [logger_url]
    level = WARNING
    handlers = 
    qualname = urlconvert.service
    propagate = 1

Adding other loggers
--------------------

Of course, you can also set up logging for things which aren't pipes.
Just add a handler for them in exactly the same way but make up a name
to use in the ``keys`` key and as the name of the handler section.

For example to add logging for TornadoPack you could do this:

::

    # Logging configuration
    
    [loggers]
    keys = root,pipestack,database,url,tornadopack

    ...

    # PipeStack logging
    
    ...
    
    [logger_tornadopack]
    level = DEBUG
    handlers = 
    qualname = tornadopack
    propagate = 1

Logging to a File
-----------------

By default, logging information is sent to ``stderr`` but you can send it to a
file if you prefer. Simply change the following lines:

::

    [logger_root]
    level = WARNING
    handlers = console

    [handlers]
    keys = console

    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic
    propagate = 1

to these:

::

    [logger_root]
    level = WARNING
    handlers = file

    [handlers]
    keys = file

    [handler_file]
    class = FileHandler
    args = ('application.log', 'a')
    level = INFO
    formatter = generic
    propagate = 1

The log output will then go to ``application.log`` in the same directory as
the config file instead.

Dealing with Commands
=====================

PipeStack is frequently used to write applications that are designed to run
from the command line. One options is to parse your config file and call
``start_flow()`` from within your code as the examples so far have been doing.
A better way is to use a PipeStack *command*.

A simple command might look like this:

::

    >>> from commandtool import Cmd
    >>>
    >>> class EchoCmd(Cmd):
    ...     help = dict(summary='Echo the args and opts specified')
    ...     def on_run(self, app, args, opts):
    ...         print args, opts


Let's write a slightly more complicated one that takes a couple of options and some arguments:

::

    >>> class EchoCmd(Cmd):
    ...     help = dict(summary='Echo the args and opts specified')
    ...     arg_spec = [
    ...         ('ARG_ONE', 'The first argument'),
    ...         ('ARG_TWO', 'The second argument'),
    ...         (2, 'At least two further arguments', 'Not enough extra arguments specified', 'ARG_MULTI'),
    ...     ]
    ...     # Here we inherit the options from Cmd and then extend them
    ...     option_spec = Cmd.option_spec.copy()
    ...     option_spec.update({
    ...         'option': dict(
    ...             options = ['-o', '--option'],
    ...             help = 'An option without an argument',
    ...         ),
    ...         'option_with_arg': dict(
    ...             options = ['-a', '--arg'],
    ...             help = 'An option with an argument',
    ...             metavar = 'OPT_ARG',
    ...         ),
    ...     })
    ...     def on_run(self, app, args, opts):
    ...         print args, opts

Here's a PipeStack application that uses our command:

::

    >>> from pipestack.app import pipe, command, App
    >>> 
    >>> class CommandApp(App):
    ...     pipes = [
    ...         pipe('database', 'database.service.connection:DatabasePipe'),
    ...     ]
    ...     commands = [
    ...         command('echo', EchoCmd)
    ...     ]

To run this command you would use ``app.handle_command_line()``. By default,
``handle_command_line()`` will take its input from ``sys.argv`` but you can
also specify the arguments it should take as its input manually. This is handy
for writing documentation examples. In the examples that follow, the strings
specified in the list that is the first argument to
``app.handle_command_line()`` represent the options and arguments a user has
specified on the command line. So if a user typed:

::

    python doc.py --help

we can simulate that here by running:

::

    app.handle_command_line(['--help'], exit=do_nothing)

In fact, we'll do this in a minute. Fisrt let's try with no input:

::

    >>> app = CommandApp()
    >>> app.handle_command_line([], exit=do_nothing)
    Error: No command specified
    Try `doc.py --help' for more information.


In the help output you will see, ``doc.py`` will be automatically replaced with
the name of the file you are executing.

Now let's see which commands are available:

::

    >>> app.handle_command_line(['--help'], exit=do_nothing)
    Run a PipeStack command
    Usage: doc.py [OPTIONS] COMMAND
    <BLANKLINE>
    Options:
      -l LOGGING_FILE         the logging file
      --logging=LOGGING_FILE
      -q --quiet              only show error and warning messages
      -d CONFIG_FILE          the config file
      --config=CONFIG_FILE
      -h --help               display this message
      -v --verbose            show all log messages
    <BLANKLINE>
    Commands:
      echo                  Echo the args and opts specified
    <BLANKLINE>
    Type `doc.py COMMAND --help' for help on individual commands.

As you can see there are quite a few options and arguments. By default
PipeStack uses a ``pipestack.app.AppCmd()`` instance for the main commnad. This
is derived from a ``commandtool.LoggingCmd``. The default logging level is
``INFO``. If you sepcify ``-v`` or ``--verbose`` the logging level will be
changed to ``DEBUG``, if you specify ``-q`` or ``--quiet``, the logging level
will be set to ``WARNING``.

You'll also notice that you can specify ``-l`` or ``--logging`` and the path to
a logging configuration file. If this is specified the logging will instead be
set up according to the configuration in that file.

The other important options to notice are the ``-d`` and ``--config-file``
options. These allow you to specify the config file to be used. If they are
secified, the PipeStack ``AppCmd`` will automatically parse the config file by
calling ``app.parse_config()``.

This all means that the individual commands you write will automatically gain
logging and config file functionality without any effort from you. This is why
it is usually best to write command line handling code as commands rather than
in Python.

.. tip ::

   All the options specified so far must be given *before* the name of the command to run.

As you can see there is currently only one command available, called ``echo``.
Let's see what help it provides:

::

    >>> app.handle_command_line(['echo', '--help'], exit=do_nothing)
    Echo the args and opts specified
    Usage: doc.py [OPTIONS] echo [OPTIONS] ARG_ONE ARG_TWO ARG_MULTI
    <BLANKLINE>
    Command 'echo' options:
      -a --arg              An option with an argument
      -h --help             display this message
      -o --option           An option without an argument
    <BLANKLINE>
    Command 'echo' arguments:
      ARG_ONE               The first argument
      ARG_TWO               The second argument
      ARG_MULTI             At least two further arguments
    <BLANKLINE>
    Type `doc.py --help' for a full list of commands.

The global options are shown again as a reminder but notice that the help text
at the top has changed and that there are now sections at the bottom called
"Command 'echo' options" and "Command 'echo' arguments". 

Let's test out some examples to see how they get parsed as to the ``opts`` and
``args`` arguments to the ``on_run()`` method:

::

    >>> app.handle_command_line(['-q', 'echo', '--option', '-a', 'arg', 'ONE', 'TWO', 'THREE', 'FOUR'], exit=do_nothing)
    ['ONE', 'TWO', 'THREE', 'FOUR'] {'option_with_arg': 'arg', 'help': False, 'option': True}

Here we are specifying the global opt ``-q`` before the command and then
choosing the ``echo`` command with a range of options and arguments.  As you
can see the arguments get passed directly to the ``args`` variable. The options
are more interesting. The key used in the ``option_spec`` dictionary is
considered an *internal variable*. If the corresponding option doesn't take an
argument the internal variable is treated as a boolean, being ``True`` if the
option is present, and ``False`` otherwise. If it does take an argument the
internal variable will only be present if the option is and its value will be
the argument specified. In this example we have set up the ``arg_spec`` so that
you can have a variable number of arguments, but added a constraint that after
``ARG_ONE`` and ``ARG_TWO`` are specified, at least 2 more arguments must be
specified (this is the number 2 in the last item in the ``arg_spec``).

If the user makes any errors when entering the command line options, they will
get an appropriate short error message: 

::

    >>> app.handle_command_line(['-q', 'echo', '--option', '-a', 'arg', 'ONE', 'TWO', 'THREE'], exit=do_nothing)
    Error: Not enough extra arguments specified
    Try `doc.py echo --help' for more information.

Converting parsed options and arguments
---------------------------------------

At this point you have parsed some options and arguments but not done much with
them. CommandTool (on which this code is based) is designed with the concept of
internal variables so that after parsing the options and arguments you have
obtained can be passed directly into a Python function like this:

::

    def some_api_function(one, two, three, option, *extra_args, **optional_args):
        # Do something here
        pass

You could call it like this:

::

    some_api_function(*args, **opts)

In most instances though you will need to perform some conversions on the
options and arguments specified though. To do this you can use ConversionKit
converters. The important thing to note though is that if you want an error
message to be printed on the command line you must raise it as a
``getopt.GetoptError`` instance like this:

::

    import getopt
    raise getopt.GetoptError(conversion.error)

Starting a Flow
---------------

The first argument to the ``on_run()`` method is the app instance itself so
once the options and arguments have been converted you can go ahead and start a
flow. A useful tip is that you can use a class method as a terminator and this
allows you to write your command handling code the same way you would write any
PipeStack handler taking a ``bag`` argument. Here's an example:

::

    from bn import AttributeDict
    from pipestack.ensure import ensure_method_bag

    class EchoCmd(Cmd):
        ... help, arg_spec and option_spec all as before

        def on_run(self, app, args, opts):
            # ... convert opts and args if needed
            bag = AttributeDict(
                command=AttributeDict(
                    opts=opts,
                    args=args,
                )
            )
            app.start_flow(bag=bag, run=self.handle)

        @ensure_method_bag('database')
        def handle(self, bag):
            print bag.command.args, bag.command.opts, bag.has_key('database')
            # ... code away as normal

With this little bit of boilerplate you now have an environment where you can
access the args and options as if they were a ``cmd`` pipe but you can also
access the other pipes in the app and code your command line handler in exactly
the same way as you would write any such code.

@@@ In future we could go further and have a converter associated with the
option spec entries with matavars so that args and opts are automatically converted.

Writing a Pipe
==============

Basically subclass one of ``pipestack.pipe.Pipe``,
``pipestack.pipe.ConfigPipe`` or ``pipestack.pipe.MarblePipe`` depending on
your needs. They have clear docstrings.

XXX Add some examples.

Pipe Naming
-----------

It is sometimes tempting to have pipes named in a nested fashion. For example
you might like to access HTTP data like this

::

    bag.environ
    bag.input
    bag.response

In this case you might not always want HTTP post data input parsed so you might
want a pipe called ``http.input`` so that when it was started it would form a
sort of "plugin" to the main ``http`` pipe. I've experimented with this design
quite a lot. The drawback is configuration. If I write:

::

    http.input.parse_method = once

does this mean that ``http`` package should recieve an option
``input.parse_method`` or does it mean that the ``http.input`` pipe recieves
``parse_method``. The solution is to change the config format to support
differentitaion of these two cases but I think it highlights a deeper problem:
what exactly should a pipe be?

I think a pipe should be any useful piece of functionality that works well on
its own or would have an unnecessary cost if it was integrated with another
pipe. In this case, is it important that an HTTP request is related to an HTTP
response or that HTTP input from post data is related to an HTTP request? I've
come to the conculsion that it is not. Instead we have different pipes for the
three things. This leaves you as the developer with two choices:

* Name things differently, for example you could have an ``http_request`` pipe

* Automatically nest marbles if they are present. For example, the ``http``
  pipe could look for the presence of an ``input`` pipe and then allow access
  to it as ``bag.http.input`` in addition to the already allowed ``bag.input``.
  Of course, you'd still need to reference the pipe as ``input`` in ``@ensure``
  decorators. 





Designing an Application
========================

In order to write a PipeStack application you need to ask yourself these questions:

* What functionality of my application could best be modelled as a pipestack?
* What marbles should already be in the bag before it enters the pipestack?
* Do I need a terminator script to be executed when the bag gets to the end of the pipeline?

Let's think about two use cases to give you an idea of how these questions might be answered:

Case Study 1: A webserver
-------------------------

Webservers are designed to serve pages to multiple people at once using the
HTTP protocol. When a user visits a page an HTTP request is sent to the server.
The server processes the request and sends back an HTTP response.

In this case it would make a lot of sense to have a different pipestack for
each HTTP request. The HTTP request could pass up the pipestack, be handled by
one of the pipes and then return back down the pipestack to be converted into
an HTTP response.

In order for the pipes to be know something about the HTTP request it would
make sense for the bag to contain a marble representing the HTTP request before
it enters the pipestack. The pipes will also need a way of creating an HTTP
response. It would also make sense for the marble containing the HTTP request
to also provide some way for the pipes to specify what information should
appear in the response. You could even have a separate marble for the HTTP
request and response if you prefered.

Now we need to think about the terminator at the end of the pipestack. Web
servers usually return a "404 Not Found" page if a page could not be found.
We'd design our pipestack so that one of the pipes will handle the request if
it can, if not the terminator will generate a 404 page.

Case Study 2: A cron job accessing a database
---------------------------------------------

In this case the program will get executed at regular intervals. It will be
expected to start up, make some changes to a database and then to stop. In this
case it makes sense to model the entire program flow as a single journey of a
bag up and down the pipestack.

In this case the database connection might as well be a marble that is set up
by a pipe and the bag won't need any marbles in to start with. The terminator
can be the actually application which can access the database via the
connection in the marble that the database pipe added to the bag.

