# adapted from z3c.hashedresource.hash

try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5
import os

def resource_hash(path):
    if os.path.isdir(path):
        files = _list_directory(path)
    else:
        files = [path]

    result = md5()
    for file in files:
        # ignore any svn droppings
        if file.startswith('.svn'):
            continue
        # ignore any vim .swp files
        if file.endswith('.swp'):
            continue
        f = open(file, 'rb')
        data = f.read()
        f.close()
        result.update(data)
    result = result.hexdigest()
    return result

def _list_directory(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)

