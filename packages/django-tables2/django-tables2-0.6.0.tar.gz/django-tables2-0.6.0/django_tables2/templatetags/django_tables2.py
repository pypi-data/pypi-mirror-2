#! -*- coding: utf-8 -*-
"""
Allows setting/changing/removing of chosen url query string parameters, while
maintaining any existing others.

Expects the current request to be available in the context as ``request``.

Examples:

    {% set_url_param page=next_page %}
    {% set_url_param page="" %}
    {% set_url_param filter="books" page=1 %}

"""
import urllib
import tokenize
import StringIO
from django.conf import settings
from django import template
from django.template.loader import get_template
from django.utils.safestring import mark_safe


register = template.Library()


class SetUrlParamNode(template.Node):
    def __init__(self, changes):
        self.changes = changes

    def render(self, context):
        request = context.get('request', None)
        if not request:
            return ""
        # Note that we want params to **not** be a ``QueryDict`` (thus we
        # don't use it's ``copy()`` method), as it would force all values
        # to be unicode, and ``urllib.urlencode`` can't handle that.
        params = dict(request.GET)
        for key, newvalue in self.changes.items():
            newvalue = newvalue.resolve(context)
            if newvalue == '' or newvalue is None:
                params.pop(key, False)
            else:
                params[key] = unicode(newvalue)

        # ``urlencode`` chokes on unicode input, so convert everything to utf8.
        # Note that if some query arguments passed to the site have their
        # non-ascii characters screwed up when passed though this, it's most
        # likely not our fault. Django (the ``QueryDict`` class to be exact)
        # uses your projects DEFAULT_CHARSET to decode incoming query strings,
        # whereas your browser might encode the url differently. For example,
        # typing "ä" in my German Firefox's (v2) address bar results in "%E4"
        # being passed to the server (in iso-8859-1), but Django might expect
        # utf-8, where ä would be "%C3%A4"
        def mkstr(s):
            if isinstance(s, list):
                return map(mkstr, s)
            else:
                return s.encode('utf-8') if isinstance(s, unicode) else s
        params = dict([(mkstr(k), mkstr(v)) for k, v in params.items()])
        # done, return (string is already safe)
        return '?' + urllib.urlencode(params, doseq=True)


@register.tag
def set_url_param(parser, token):
    bits = token.contents.split()
    qschanges = {}
    for i in bits[1:]:
        try:
            a, b = i.split('=', 1)
            a = a.strip()
            b = b.strip()
            a_line_iter = StringIO.StringIO(a).readline
            keys = list(tokenize.generate_tokens(a_line_iter))
            if keys[0][0] == tokenize.NAME:
                # workaround bug #5270
                b = (template.Variable(b) if b == '""' else
                     parser.compile_filter(b))
                qschanges[str(a)] = b
            else:
                raise ValueError
        except ValueError:
            raise (template.TemplateSyntaxError,
                   "Argument syntax wrong: should be key=value")
    return SetUrlParamNode(qschanges)


class RenderTableNode(template.Node):
    def __init__(self, table_var_name):
        self.table_var = template.Variable(table_var_name)

    def render(self, context):
        try:
            # may raise VariableDoesNotExist
            table = self.table_var.resolve(context)
            if "request" not in context:
                raise AssertionError("{% render_table %} requires that the "
                                     "template context contains the HttpRequest in"
                                     " a 'request' variable, check your "
                                     " TEMPLATE_CONTEXT_PROCESSORS setting.")
            context = template.Context({"request": context["request"],
                                        "table": table})
            try:
                table.request = context["request"]
                return get_template("django_tables2/table.html").render(context)
            finally:
                del table.request
        except:
            if settings.DEBUG:
                raise
            else:
                return settings.TEMPLATE_STRING_IF_INVALID


@register.tag
def render_table(parser, token):
    try:
        _, table_var_name = token.contents.split()
    except ValueError:
        raise (template.TemplateSyntaxError,
               u'%r tag requires a single argument'
               % token.contents.split()[0])
    return RenderTableNode(table_var_name)
