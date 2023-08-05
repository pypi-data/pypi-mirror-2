
import sys
from urlimport import UrlFinder, config, reset, DefaultErrorHandler

__all__ = ('config', 'reset', 'DefaultErrorHandler')

# register The Hook
sys.path_hooks = \
    [x for x in sys.path_hooks if x.__name__ != 'UrlFinder'] + [UrlFinder]


