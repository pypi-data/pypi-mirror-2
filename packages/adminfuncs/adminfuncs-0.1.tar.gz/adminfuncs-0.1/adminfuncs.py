# -*- coding: utf-8 -*-
"""
    adminfuncs
    ~~~~~~~~~~

    Module for building simple admin page

    This module doesn't have much use by itself; for now it's only
    used with related tipfy extension

    :copyright: 2010 by Brandon Thomson
    :license: BSD, see LICENSE for more details.
"""

import functools

import inspect

from werkzeug import import_string

def get_nice_defaults(f):
    args = inspect.getargspec(f)[0]
    defaults = inspect.getargspec(f)[3]

    if defaults:
        defaults = list(defaults)
        defaults.reverse()
        defaults.extend([None]*(len(args)-len(defaults)))
        defaults.reverse()
    else:
        defaults = [None]*len(args)
    return defaults

def get_template_args(f):
    """
    Convert function arg data into a form that makes it more convenient for the
    template to generate the fields
    """
    args = inspect.getargspec(f)[0]
    defaults = get_nice_defaults(f)
    if defaults:
        arglist = zip(args, defaults)
        # for "def foo(a, b, c=3, d=4)"
        # arglist is [('a', None), ('b', None), ('c', 3), ('d', 4)]
    else:
        arglist = zip(args, [None]*len(args))
        #arglist = zip(args, args)
    t_args = []
    for argname, default in arglist:
        # Default arg value changed to a string for jinja
        box_text = str(default) if default else ""
        is_textarea = box_text.startswith("<big>") 
        if is_textarea:
          box_text = box_text[5:]

        t_args.append((argname, box_text, is_textarea))
    return t_args

def func_args_from_strings(farg, arg_strings):
  """
  Return function object and convert arg_strings list of positional args which
  can be expanded into selected admin function using * operator

  args with default values as ints in function definition are also converted
  from unicode to int
  """

  # XXX: probably a vulnerability if admin interface is not protected... could
  # check admin modules against the specified list for more safety
  func = import_string(farg)

  defaults = get_nice_defaults(func)

  args = []
  if arg_strings:
      for arg, default in zip(arg_strings, defaults):
          if type(default) == type(0):
              args.append(int(arg))
          else:
              args.append(arg)

  return func, args

def build_list(is_deployed, module_paths):
    """Import modules and generate giant list of all admin functions.

    Could be cached if you want to save cpu time
    """
    funcs_by_module = []

    for module_path in module_paths:
        module = import_string(module_path)
        funcs = []

        try:
          objects = module.ORDER
        except AttributeError:
          objects = [getattr(module, name) for name in dir(module)]

        for obj in objects:
            if inspect.isfunction(obj):
                func = obj
                t_args = get_template_args(func)

                func_settings = dict(module.DEFAULTS)
                func_settings.update(getattr(func, 'settings', {}))

                if is_deployed and func_settings['local_only']:
                  continue
                if not is_deployed and func_settings['production_only']:
                  continue

                do_confirm = (is_deployed and func_settings['confirm_deployed']
                              or func_settings['confirm'])

                funcs.append((func, t_args, do_confirm))
        funcs_by_module.append((module, funcs))

    return funcs_by_module

class settings(object):
    """Use to alter settings from module defaults for an individual function"""
    def __init__(self, **kwds):
        self.settings = kwds

    def __call__(self, f):
        """
        Attach settings dict created from keyword args passed to this decorator to
        the function object for later reference.
        """
        @functools.wraps(f)
        def wrapper(*args, **kwds):
            return f(*args, **kwds)

        # Save settings dict on function object
        wrapper.settings = self.settings

        return wrapper
