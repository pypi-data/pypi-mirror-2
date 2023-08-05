from rivr.http import ResponseRedirect
from rivr.templates import Template, Context

def redirect_to(request, url):
    return ResponseRedirect(url)

def direct_to_template(request, template, extra_context={}, **kwargs):
    t = Template(template)
    c = Context(extra_context)
    c['params'] = kwargs
    return Response(t.render(c))
