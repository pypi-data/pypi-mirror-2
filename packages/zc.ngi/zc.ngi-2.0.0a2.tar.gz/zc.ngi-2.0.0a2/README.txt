Network Gateway Interface
*************************

The Network Gateway Interface provides:

- the ability to test application networking code without use of
  sockets, threads or subprocesses

- clean separation of application code and low-level networking code

- a fairly simple inheritence free set of networking APIs

- an event-based framework that makes it easy to handle many
  simultaneous connections while still supporting an imperative
  programming style.

To learn more, see http://packages.python.org/zc.ngi/

Changes
*******

====================
2.0.0a2 (2010-07-22)
====================

New Features:

- There's a new experimental zc.ngi.async.Implementation.listener
  option to run each client (server connection) in it's own thread.

  (It's not documented. It's experimental, but there is a doctest.)

Bugs Fixed:

- There was a bug in handling connecting to testing servers that
  caused printing handlers to be used when they shouldn't have been.


====================
2.0.0a1 (2010-07-08)
====================

New Features:

- New improved documentation

- Support for writing request handlers in an imperative style using
  generators.

- Cleaner testing interfaces

- Refactored ``zc.ngi.async`` thread management to make the blocking
  APIs unnecessary. ``zc.ngi.async.blocking`` is now deprecated.

- Added support for running multiple ``async`` implementations in
  separate threads. This is useful in applications with fewer network
  connections and with handlers that tend to perform long-lating
  computations that would be unacceptable with a single select loop.

- Renamed IConnection.setHandler to set_handler.

- Dropped support for Python 2.4.

Bugs Fixed:

- The ``Sized`` request adapter's ``writelines`` method was broken.

- There we a number of problems with error handling in the ``async``
  implementation.

==================
1.1.6 (2010-03-01)
==================

Bug fixed:

- Fixed bad logging of ``listening on ...``. The message was emitted
  before the actual operation was successful.  Emits now a warning
  ``unable to listen on...`` if binding to the given address fails.

==================
1.1.5 (2010-01-19)
==================

Bug fixed:

- Fixed a fatal win32 problem (socket.AF_UNIX usage).

- Removed impropper use of the SO_REUSEADDR socket option on windows.

- The sized adapter performed poorly (because it triggered Nagle's
  algorithm).


==================
1.1.4 (2009-10-28)
==================

Bug fixed:

- Spurious warnings sometimes occurred due to a race condition in
  setting up servers.
- Added missing "writelines" method to zc.ngi.adapters.Lines.

==================
1.1.3 (2009-07-30)
==================

Bug fixed:

- zc.ngi.async bind failures weren't handled properly, causing lots of
  annoying log messages to get spewed, which tesnded to fill up log
  files.

==================
1.1.2 (2009-07-02)
==================

Bugs fixed:

- The zc.ngi.async thread wasn't named. All threads should be named.

==================
1.1.1 (2009-06-29)
==================

Bugs fixed:

- zc.ngi.blocking didn't properly handle connection failures.

==================
1.1.0 (2009-05-26)
==================

Bugs fixed:

- Blocking input and output files didn't properly synchronize closing.

- The testing implementation made muiltiple simultaneous calls to
  handler methods in violation of the promise made in interfaces.py.

- Async TCP servers used too low a listen depth, causing performance
  issues and spurious test failures.

New features:

- Added UDP support.

- Implementation responsibilities were clarified through an
  IImplementation interface.  The "connector" attribute of the testing
  and async implementations was renamed to "connect". The old name
  still works.

- Implementations are now required to log handler errors and to close
  connections in response to connection-handler errors. (Otherwise,
  handlers, and especially handler adapters, would have to do this.)

==================
1.0.1 (2007-05-30)
==================

Bugs fixed:

- Server startups sometimes failed with an error like::

    warning: unhandled read event
    warning: unhandled write event
    warning: unhandled read event
    warning: unhandled write event
    ------
    2007-05-30T22:22:43 ERROR zc.ngi.async.server listener error
    Traceback (most recent call last):
      File "asyncore.py", line 69, in read
        obj.handle_read_event()
      File "asyncore.py", line 385, in handle_read_event
        self.handle_accept()
      File "/zc/ngi/async.py", line 325, in handle_accept
        sock, addr = self.accept()
    TypeError: unpack non-sequence
