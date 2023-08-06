#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2010 Adrian Perez <aperez@igalia.com>

"""
Useful mix-in classes to add prebuilt behavior to custom bots.
"""

import inspect


class HelpCommandMixin(object):
    """
    Mix-in class which adds a "help" command to a :class:`WhistlerBot`. To
    use it in your custom bot, do something like:

    >>> class MyBot(WhistlerBot, HelpCommandMixin):
    ...     pass

    """
    def __get_commands(self):
        for (name, kind, _, _) in inspect.classify_class_attrs(self.__class__):
            if name.startswith("cmd_") and kind == "method":
                yield name[4:]

    def cmd_help(self, cmd, args):
        """Obtains a list of commands, or help about a particular command."""
        if not args:
            return "Available commands: " + ", ".join(self.__get_commands())

        func = getattr(self, "cmd_" + args[0], None)
        if func is None:
            return "No such command '%s'" % args[0]

        return "%s: %s" % (args[0], inspect.getdoc(func))

