import copy

from webob import Response


class Page(object):
    """
    The basic page object in puppetcms.
    """
    def __init__(self, template, context):
        self.template = template
        self.context = context

    def __call__(self, request):
        context = copy.copy(self.context)
        context['request'] = request

        return Response(self.template.render(context))
