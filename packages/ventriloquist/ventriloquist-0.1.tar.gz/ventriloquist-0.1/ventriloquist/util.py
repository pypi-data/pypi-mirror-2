import os
import sys


def load_controller(string):
    module_name, func_name = string.split(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, func_name)
    return func


def python_context_load(context):
    """
    """
    python_context = {}

    for key, import_string in context.iteritems():
        if u':' in import_string:
            # pass in an function/attribute of the module
            python_context[key] = load_controller(import_string)
        else:
            # pass in the whole module
            __import__(import_string)
            python_context[key] = sys.modules[import_string]

    return python_context


class InsecurePath(Exception): pass


def safe_path_join(base_path, join_path, minimum_path=None):
    """
    Safely join a path with its base, without the danger of going back
    a bunch of levels and opening /etc/passwd or whatever.

    A path won't be allowed if it goes lower than minimum_path (which
    is the same as base_path if not provided)
    """
    if not minimum_path:
        minimum_path = base_path

    new_path = os.path.abspath(os.path.join(base_path, join_path.lstrip('/')))

    if not new_path.startswith(os.path.abspath(minimum_path)):
        raise InsecurePath(
            '%s does not start with minimum_path %s, cannot be trusted' % (
                new_path, minimum_path))

    return new_path
