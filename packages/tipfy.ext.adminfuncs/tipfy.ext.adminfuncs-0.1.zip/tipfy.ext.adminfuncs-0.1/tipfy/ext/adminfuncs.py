# -*- coding: utf-8 -*-
"""
    tipfy.ext.adminfuncs
    ~~~~~~~~~~~~~~~~~~~~

    Tipfy support for admin functions.

    :copyright: 2010 Brandon.
    :license: BSD, see LICENSE for more details.
"""

# monkey patch werkzeug
from tipfy.ext.debugger import app
# XXX: Might as well just pull the tb template in and render it using the
# application's jinja environment instead of creating a new one just for
# werkzeug... especially in production where it is not already created

from tipfy import RequestHandler, request, get_config
from tipfy.ext.jinja2 import render_response, render_template

from werkzeug.debug.tbtools import get_current_traceback

from jinja2 import Environment, FileSystemLoader

from ..adminfuncs import build_list, func_args_from_strings

is_dev = get_config('tipfy')['dev']

class FuncListHandler(RequestHandler):
    """Builds HTML with forms and list of all admin functions"""
    def get(self):
        from google.appengine.api import users

        is_deployed = not get_config('tipfy')['dev']
        module_paths = get_config('adminfuncs')['modules']

        funcs_by_module = build_list(is_deployed, module_paths)

        return render_response('admin/funclist.html',
            modules=funcs_by_module,
            body_class="dev" if is_dev else "deployed",
            deploy_mode="dev_appserver" if is_dev else "deployed",
            logout_url=users.create_logout_url(get_config('adminfuncs')['logout_url']),
            title=get_config('adminfuncs')['title'],
        )


def get_frame_locals(skip=0):
  """Returns a string with each frame of the active exception's local variables.

  Adapted from some recipe in the cookbook
  """
  import sys, traceback

  tb = sys.exc_info()[2]
  stack = []
  ret = ""

  for i in range(skip):
      tb = tb.tb_next

  while tb:
      stack.append(tb.tb_frame)
      tb = tb.tb_next

  ret += "<h3>Locals by frame <em>(most recent frame last)</em>:</h3>\n"
  ret += "<ul>"
  for frame in stack:
      ret += render_template("admin/frames.html",
                             name=frame.f_code.co_name,
                             file=frame.f_code.co_filename,
                             lineno=frame.f_lineno,
                             vars=frame.f_locals.items())
  ret += "</ul>"

  return ret

def get_production_traceback_response():
    """Render traceback response which is safe for production use"""

    tb = get_current_traceback(skip=1, show_hidden_frames=False,
                               ignore_system_exceptions=True)

    tb_html = tb.render_summary().encode('utf-8', 'replace')
    return render_response('admin/error.html',
                           traceback_html=tb_html,
                           locals=get_frame_locals(skip=1))

def get_func_and_args(farg, form_items):
    """
    Return function object and convert submitted form data into list of
    positional args which can be expanded into selected admin function using *
    operator
    """
    arg_strings = [y for x,y in form_items if x.startswith("arg_")]

    return func_args_from_strings(farg, arg_strings)

class ExecFuncHandler(RequestHandler):
    """Executes function of user choice with user args"""
    def get(self, farg):
        # Was thinking about allowing user to specify whether function has
        # side-effects or not, but it's not that important
        return self.post(farg)

    def post(self, farg):
        if farg == '_default':
            return render_response('admin/default.html')

        import time
        import sys
        import cStringIO

        func, args = get_func_and_args(farg, request.form.items())

        old_stdout = sys.stdout
        sys.stdout = out = cStringIO.StringIO()

        s = time.time()
        try:
            return_val = func(*args)
        except:
            if is_dev:
                raise # let the werkzeug middleware debugger handle it
            else:
                return get_production_traceback_response()
        finally:
            sys.stdout = old_stdout

        runtime = time.time() - s

        module_path, _, function_name = farg.rpartition('.')

        return render_response(
          'admin/result.html',
          arg_string=", ".join([repr(arg) for arg in args]),
          captured=out.getvalue(),
          exec_time="%0.1f" % (runtime*1000),
          function_name=function_name,
          module_path=module_path,
          return_val=return_val,
        )
