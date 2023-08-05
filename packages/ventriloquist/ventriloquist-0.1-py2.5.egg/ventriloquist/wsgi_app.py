import urllib

import jinja2
from webob import Request, exc

from ventriloquist import loader


class VentriloquistApp(object):
    def __init__(self, template_env, document_root, setup_path='setup.json'):
        self.template_env = template_env
        # create the mapping
        self.pagemap = loader.recursive_page_load(
            setup_path, document_root, template_env, {})

    def __call__(self, environ, start_response):
        # Create a webob wrapper of the request object
        request = Request(environ)
        path_info = request.path_info

        # Try to get a matching page
        page = self.pagemap.get(path_info)

        # No matchinv page?
        if not page:
            # Try to do see if we have a match with a trailing slash
            # added and if so, redirect
            if not path_info.endswith('/') \
                    and request.method == 'GET' \
                    and self.pagemap.get(path_info + '/'):
                new_path_info = path_info + '/'
                if request.GET:
                    new_path_info = '%s?%s' % (
                        new_path_info, urllib.urlencode(request.GET))
                redirect = exc.HTTPTemporaryRedirect(location=new_path_info)
                return request.get_response(redirect)(environ, start_response)

            # Okay, no matches.  404 time!
            return exc.HTTPNotFound()(environ, start_response)

        # Since we do have a matching page, let's process it and
        # return the results.
        return page(request)(environ, start_response)


def ventriloquist_app_factory(global_config, **kwargs):
    template_loader = jinja2.FileSystemLoader(kwargs['document_root'])
    template_env = jinja2.Environment(loader=template_loader, autoescape=True)
    return VentriloquistApp(
        template_env, kwargs['document_root'],
        kwargs.get('setup_path', '/setup.json'))
