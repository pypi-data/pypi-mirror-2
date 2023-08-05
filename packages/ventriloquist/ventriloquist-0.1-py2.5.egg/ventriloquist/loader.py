try:
    import json
except ImportError:
    import simplejson as json

import os
import copy
import simplejson

from ventriloquist import util
from ventriloquist.page import Page


def recursive_page_load(setup_path, document_root, template_env,
                        global_context, pages=None):
    pages = pages or {}

    setup_data = simplejson.loads(
        file(util.safe_path_join(document_root, setup_path)).read())

    global_context = copy.copy(global_context)
    if setup_data.has_key('context'):
        global_context.update(setup_data['context'])

    if setup_data.has_key('python_context'):
        global_context.update(
            util.python_context_load(setup_data['python_context']))

    # load all the pages
    for page_data in setup_data.get('pages', []):
        page_context = copy.copy(global_context)
        if page_data.has_key('context'):
            page_context.update(page_data['context'])
        if page_data.has_key('python_context'):
            page_context.update(
                util.python_context_load(page_data['python_context']))

        pages[page_data['url']] = Page(
            template_env.get_template(page_data['template']), page_context)

    # append all the pages from the global page_mounts
    for page_mount in setup_data.get('page_mounts', []):
        recursive_page_load(
            page_mount, document_root, template_env,
            global_context, pages)

    return pages
