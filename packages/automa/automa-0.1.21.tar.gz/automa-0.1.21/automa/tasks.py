#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: t -*-
#
# Copyright (C) 2010-2011 Marco Pantaleoni. All rights reserved.
# Marco Pantaleoni <marco.pantaleoni@gmail.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License version 2 as
#    published by the Free Software Foundation.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

__author__    = "Marco Pantaleoni"
__copyright__ = "Copyright (C) 2010-2011 Marco Pantaleoni"
__license__   = "GPL v2"

import sys
import traceback
import copy
import datetime

DEFAULT_EXTENDED_DEBUG = True

def get_active_context():
    return TaskContext.Active()

def call_task(*args, **kwargs):
    cntxt = TaskContext.Active()
    cntxt.call_task(*args, **kwargs)

class Task(object):
    __doc__ = ""
    _tasks            = []
    _task_by_name     = {}
    _task_by_fullname = {}

    def __init__(self, func):
        self.func     = func
        self.__name__ = func.__name__
        self.name     = func.__name__
        self.fullname = "%s.%s" % (func.__module__, func.__name__)
        if hasattr(func, '__doc__'):
            self.__doc__ = func.__doc__
        self.depends  = []
        self.cmdline_spec = []      # command line option specification
        self.propagate_cmdline = False

        self._started    = None
        self._completed  = None
        self._started_by = None

        self._tasks.append(self)
        self._task_by_name[self.name] = self
        self._task_by_fullname[self.fullname] = self

    def __call__(self, *args, **kwargs):
        ctxt = TaskContext(self, args, kwargs)
        return ctxt.run()

    def __str__(self):
        return '<Task %r>' % self.fullname

    def __repr__(self):
        return '<Task %r>' % self.fullname

    @classmethod
    def Tasks(cls):
        return list(cls._tasks)

    @classmethod
    def TaskFromShortName(cls, name):
        return cls._task_by_name.get(name, None)
    @classmethod
    def TaskFromFullName(cls, name):
        return cls._task_by_fullname.get(name, None)
    @classmethod
    def TaskFromName(cls, name):
        return cls.TaskFromFullName(name) or cls.TaskFromShortName(name)

    @property
    def optparser(self):
        import optparse
        from main import PROGNAME
        from setup_info import version
        parser = optparse.OptionParser(prog=PROGNAME,
                                       usage="usage: %%prog [options] ... %s [%s options] ..." % (self.name, self.name),
                                       add_help_option=False)
        parser.disable_interspersed_args()
        for spec in self.cmdline_spec:
            if isinstance(spec, dict):
                spec = dict(spec)
                opt_has_value = spec.has_key('dest')
                opt_longname  = spec.get('long', None)
                opt_shortname = spec.get('short', None)
                if opt_longname:
                    if opt_longname.endswith('='):
                        opt_longname = opt_longname[:-1]
                        opt_has_value = True
                    del spec['long']
                if opt_shortname:
                    if opt_shortname.endswith('='):
                        opt_shortname = opt_shortname[:-1]
                        opt_has_value = True
                    del spec['short']
                opt_action = "store_true"
                if opt_has_value:
                    opt_action = "store"
                if not spec.has_key('action'):
                    spec['action'] = opt_action
                if opt_longname and opt_shortname:
                    parser.add_option('--' + opt_longname, '-' + opt_shortname, **spec)
                elif opt_longname:
                    parser.add_option('--' + opt_longname, **spec)
                elif opt_shortname:
                    parser.add_option('-' + opt_shortname, **spec)
                else:
                    parser.add_option(**spec)
            else:
                assert isinstance(spec, (list, tuple))
                (opt_longname, opt_shortname, opt_default, opt_help) = spec
                opt_has_value = False
                if opt_longname.endswith('='):
                    opt_longname = opt_longname[:-1]
                    opt_has_value = True
                if opt_shortname.endswith('='):
                    opt_shortname = opt_shortname[:-1]
                    opt_has_value = True
                opt_action = "store_true"
                if opt_has_value:
                    opt_action = "store"
                parser.add_option('--' + opt_longname, '-' + opt_shortname, action=opt_action, default=opt_default, help=opt_help)
        parser.add_option('--help', '-h', dest='help', action='store_true',
                          help='show help for task %r' % self.name)
        return parser

def task(f):
    """@task decorator"""
    if isinstance(f, Task):
        return f
    return Task(f)

class depends(object):
    """@depends decorator"""
    def __init__(self, *args):
        self.args = args

    def __call__(self, f):
        if not isinstance(f, Task):
            f = Task(f)
        f.depends = self.args
        return f

class cmdline(object):
    """
    @cmdline decorator

    Sets the command line arguments specification for this task.
    The decorator argument must be a list of specifications.
    Each specification can be either a dictionary or a tuple.
    The dictionary is more or less corresponding to OptionParser.add_option()
    keyword arguments, with the addition of the 'long' and 'short' keys, for
    long and short option names.
    The tuple has the format:
      (long_name, short_name, default_value, help_text)

    In both cases, if the long name or the short name ends with '=', the option
    takes a value.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        if not isinstance(f, Task):
            f = Task(f)
        f.cmdline_spec = self.args[0]
        if 'propagate' in self.kwargs:
            f.propagate_cmdline = self.kwargs['propagate']
        return f

class TaskContext(object):
    _task_contexts       = []
    _active_task_context = None
    EXTENDED_DEBUG = DEFAULT_EXTENDED_DEBUG

    def __init__(self, task, args=None, kwargs=None,
                 global_cmdline_opts=None,
                 called_from=None, level=1):
        self.task   = task
        self.args   = args or []
        self.kwargs = kwargs or {}
        self.global_cmdline_opts = global_cmdline_opts      # global command line options (optparse.Values instance)
        self.cmdline_opts = copy.copy(global_cmdline_opts)  # processed command line options (optparse.Values instance)
        self.cmdline_args = None          # processed command line args (sequence)

        self.called_from = called_from
        self.level       = level
        self._logger     = None

        self.executed    = []  # tasks which have been started
        self.completed   = []  # tasks which have been executed up to completion

    def __repr__(self):
        return '<TaskContext 0x%X task:%r>' % (id(self), self.task.fullname)

    def parse_args(self, args):
        import optparse
        parser = self.task.optparser
        self.cmdline_opts = self.cmdline_opts or optparse.Values()
        self.cmdline_args = args
        (opts, args) = parser.parse_args(args)
        self.cmdline_opts._update(opts.__dict__, mode="loose")
        if opts.help:
            self.display_help(parser)
            sys.exit(0)
        return args

    def display_help(self, parser=None):
        parser = parser or self.task.optparser
        heading = "Task %r (%r)" % (self.task.name, self.task.fullname)
        print heading
        print '-' * len(heading)
        parser.print_help()
        if self.task.__doc__:
            print
            print self.task.__doc__
        print
        return self

    def run(self):
        TaskContext._task_contexts.append(TaskContext._active_task_context)
        TaskContext._active_task_context = self
        from_id = "--"
        if self.called_from:
            assert isinstance(self.called_from, TaskContext)
            from_id = self.called_from.identification
        self.notify("TASK %s CALLED (ctxt:0x%X) (from %s)" % (self.task.name, id(self), from_id), color='bold magenta', level=self.level-1)
        if self.EXTENDED_DEBUG:
            if self.cmdline_args:
                self.debug("command-line args:%s" % repr(self.cmdline_args))
            if self.cmdline_opts:
                self.debug("command-line opts:%s" % repr(self.cmdline_opts))
        assert isinstance(self.task, Task)
        if len(self.task.depends) > 0:
            self.notify("DEPENDS ON %s" % str(self.task.depends), color='bold magenta')
            for item in self.task.depends:
                if isinstance(item, basestring):
                    item = Task.TaskFromName(item)
                if isinstance(item, Task):
                    if not self.task_is_needed(item):
                        self.notify("TASK %s IS NOT NEEDED" % item.name, color='bold magenta')
                        continue
                    self.notify("NEEDED %s BY %s (current ctxt:0x%X)" % (item, self.task, id(self)), color='bold magenta')
                    assert isinstance(item, Task)
                    ctxt = TaskContext(item, global_cmdline_opts=self.global_cmdline_opts)
                    ctxt._logger = self._logger
                    ctxt.called_from = self
                    ctxt.level = self.level + 1
                    if item.propagate_cmdline:
                        ctxt.cmdline_args = self.cmdline_args
                        ctxt.parse_args(self.cmdline_args)
                    ctxt.run()
        self.notify("TASK %s STARTED" % self.task.name, color='bold magenta', level=self.level-1)
        self.executed.append(self.task)
        if self.called_from:
            self.task._started_by = self.called_from.task
        self.task._started = datetime.datetime.now()
        rv = self.task.func(self)
        self.task._completed = datetime.datetime.now()
        self.completed.append(self.task)
        self.notify("TASK %s COMPLETED" % self.task.name, color='bold magenta', level=self.level-1)
        context = TaskContext._task_contexts.pop()
        TaskContext._active_task_context = context
        return rv

    def task_is_needed(self, task):
        assert isinstance(task, Task)
        return task._started is None

    def __call__(self, *args, **kwargs):
        self.args   = args or self.args
        self.kwargs = kwargs or self.kwargs
        return self.run()

    def call_task(self, taskname, *args, **kwargs):
        if self.EXTENDED_DEBUG:
            self.debug("TaskContext.call_task(name:%r, %s, %s)" % (taskname, repr(args), repr(kwargs)))
        cmdline = kwargs.get('cmdline', None)
        if cmdline is not None:
            del kwargs['cmdline']
        task = Task.TaskFromName(taskname)
        ctxt = TaskContext(task, args=args, kwargs=kwargs, global_cmdline_opts=self.global_cmdline_opts)
        assert isinstance(task, Task)
        ctxt._logger = self._logger
        ctxt.called_from = self
        ctxt.level = self.level + 1
        if cmdline is not None:
            ctxt.parse_args(cmdline)
        elif task.propagate_cmdline:
            assert cmdline is None
            ctxt.cmdline_args = self.cmdline_args
            ctxt.parse_args(self.cmdline_args)
        return ctxt.run()

    @classmethod
    def Active(cls):
        return TaskContext._active_task_context

    @property
    def identification(self):
        """Return a complete context/task identification string."""
        tname = ""
        if self.task:
            tname = self.task.name
        return '[0x%X %-15s]' % (id(self), tname[:15])

    @property
    def logger(self):
        if self._logger:
            return self._logger
        if self.global_cmdline_opts:
            self._logger = self.global_cmdline_opts.logger
        else:
            import cmdutils, sys
            self._logger = cmdutils.log.Logger([(cmdutils.log.Logger.NOTIFY, sys.stderr)])
        return self._logger

    def _indent_text(self, text, amount, space="  "):
        indent = space * amount
        lines = text.split('\n')
        return '\n'.join([(indent + line) for line in lines])

    def debug(self, msg, color='cyan', level=None, extra_indent=0, *args, **kwargs):
        if level is None:
            level = self.level
        level += extra_indent
        prefix = ""
        if self.EXTENDED_DEBUG:
            prefix = '%s DEBUG: ' % self.identification
        else:
            prefix = 'DEBUG: '
        return self.logger.debug(self._indent_text(prefix + msg, level),  color=color)
    def info(self, msg, color=None, level=None, extra_indent=0, *args, **kwargs):
        if level is None:
            level = self.level
        level += extra_indent
        return self.logger.info(self._indent_text(msg, level), color=color)
    def notify(self, msg, color='green', level=None, extra_indent=0, *args, **kwargs):
        if level is None:
            level = self.level
        level += extra_indent
        return self.logger.notify(self._indent_text(msg, level), color=color)
    def warn(self, msg, color='bold yellow', level=None, extra_indent=0, *args, **kwargs):
        if level is None:
            level = self.level
        level += extra_indent
        return self.logger.warn(self._indent_text('WARN: ' + msg, level), color=color)
    def error(self, msg, color='bold red', level=None, extra_indent=0, ignore_errors=None, *args, **kwargs):
        if level is None:
            level = self.level
        level += extra_indent
        if ignore_errors is None:
            if self.global_cmdline_opts:
                ignore_errors = self.global_cmdline_opts.ignore_errors
        prefix = 'ERROR: '
        if ignore_errors:
            prefix = 'ERROR (ignored): '
        text = prefix + msg
        exctype, value = sys.exc_info()[:2]
        if exctype is not None:
            text += "\nEXCEPTION\n%s" % traceback.format_exc()
        rv = self.logger.error(self._indent_text(text, level), color=color)
        if not ignore_errors:
            sys.exit(1)
        return rv
    def fatal(self, msg, color='bold red_bg', level=None, extra_indent=0, *args, **kwargs):
        if level is None:
            level = self.level
        level += extra_indent
        text = '\n\nFATAL: ' + msg
        exctype, value = sys.exc_info()[:2]
        if exctype is not None:
            text += "\nEXCEPTION\n%s" % traceback.format_exc()
        text += '\n\n'
        rv = self.logger.error(self._indent_text(text, level), color=color)
        sys.exit(1)
        return rv
