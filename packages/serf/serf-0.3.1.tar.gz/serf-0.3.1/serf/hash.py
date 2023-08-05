# adapted from z3c.hashedresource.hash

try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5
import os

def resource_hash(path):
    # ignored extensions
    ignored_extensions = ['.swp', '.tmp']

    if os.path.isdir(path):
        files = _list_directory(path)
    else:
        files = [path]

    result = md5()
    for file in files:
        # ignore any vim .swp files
        for ext in ignored_extensions:
            if file.endswith(ext):
               continue
        f = open(file, 'rb')
        data = f.read()
        f.close()
        result.update(data)
    result = result.hexdigest()
    return result

def _list_directory(path):
    # ignore any VCS directories
    ignored_dirs = ['.svn', '.git', '.bzr']
    for root, dirs, files in os.walk(path):
        for dir in ignored_dirs:
            try:
              dirs.remove(dir)
            except ValueError:
              pass
        for file in files:
            yield os.path.join(root, file)

