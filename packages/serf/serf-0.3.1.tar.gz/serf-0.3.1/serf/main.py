import sys
import getopt
from wsgiref.simple_server import make_server
import serf
import types
import martian

def main():
    try:
        optlist, args = getopt.getopt(sys.argv[1:], '', ['port='])
    except getopt.GetoptError:
        exit()

    opts = dict(optlist)
    port = opts.get('--port', 8080)        
    try:
        port = int(port)
    except ValueError:
        exit()

    if not args:
        # XXX somehow start with current package?
        exit()
    elif len(args) == 1:
        dotted_name = args[0]
        try:
            module = resolve_dotted_name(dotted_name)
        except AttributeError:
            exit()
        if not isinstance(module, types.ModuleType):
            exit()
    else:
        exit()

    print "serf - base configuration"
    reg = serf.configure()
    print "serf - configuring module:", dotted_name
    martian.grok_dotted_name(dotted_name, reg) # reg.grok(dotted_name, module)
    print "serf - running on port:", port
    httpd = make_server('', port, serf.app)
    httpd.serve_forever()

def exit():
    print "Usage: serf [--port=<port>] <module or package dottedname>"
    sys.exit(1)

def resolve_dotted_name(name):
    steps = name.split('.')
    if not steps[0]:
        raise ValueError("Dotted name shouldn't start with dot")

    steps.reverse()
    
    partial_name = steps.pop()
    result = __import__(partial_name)
    while steps:
        step = step.pop()
        partial_name += '.' + step
        try:
            result = getattr(result, step)
        except AttributeError:
            __import__(partial_name)
            result = getattr(result, step)
    return result
