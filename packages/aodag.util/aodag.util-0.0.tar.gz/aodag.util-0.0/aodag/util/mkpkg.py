import sys
import os
from optparse import OptionParser

init_tmpl = """\
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

"""

def main():
    parser = OptionParser()
    parser.add_option('-n', '--declare-namespace',
                      dest='declare_namespace',
                      help='add namespace statement to __init__.py',
                      action='store_true',
                      default=False)

    options, args = parser.parse_args()
    pkg = args[0]
    names = pkg.split('.')
    names = reduce(lambda x, y: x + [x[-1] + '/' + y], names, ['.'])
    for name in names:
        if not os.path.exists(name):
            os.mkdir(name)
            initpy = os.path.join(name, '__init__.py')
            f = open(initpy, 'w')
            if name != names[-1] and options.declare_namespace:
                f.write(init_tmpl)
            f.close()



