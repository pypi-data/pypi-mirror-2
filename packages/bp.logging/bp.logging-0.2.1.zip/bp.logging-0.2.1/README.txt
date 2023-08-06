Introduction
============

Do you find yourself repeating the same statements over and over again to get your logging configured? I did.

bp.logging eases logging setup in that these kind of statements are reduced to a bare minimum. It does so by providing a getLogger function which returns the same as Python's standard library function with the same name: an instance of the Logger class (a.k.a. a logger object). The difference to the Python Library's getLogger are the arguments that can be passed and the default configuration of the returned logger object.

bp.logging might not be useful for anyone besides myself, as default logging is configured for my very own habits and you won't gain much from using it instead of Python's standard logging facilities if your's are quite different. Maybe one day bp.logging will be extended and much more generic and/or configurable, but that day might be long after the universe has collapsed.


Usage
=====

``from bp.logging import *``

``logger = getLogger(name, console_threshold=None, logfile_threshold=None, logfile_path=None, console_format="%(levelname)s: %(name)s - %(message)s", logfile_format="%(asctime)s - %(levelname)s: %(name)s - %(message)s")``

``logger.critical("critical message")``

``logger.error("error message")``

``logger.warning("warning message")``

``logger.info("info message")``

``logger.debug("debug message")``


Examples
********

debugging to console
--------------------

``logger = getLogger("my logger", console_threshold=debug)``

or

``logger = getLogger("my logger", debug)``


warnings to file
----------------

``logger = getLogger("my logger", logfile_path="/var/log/my.log", logfile_threshold=warning)``

infos to console, errors to file
--------------------------------

``logger = getLogger("my logger", console_threshold=info, logfile_path="/var/log/my.log", logfile_threshold=error)``

or

``logger = getLogger("my logger", info, error, "/var/log/my.log")``

