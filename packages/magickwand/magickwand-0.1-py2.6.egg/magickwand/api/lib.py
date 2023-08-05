from ctypes import CDLL
from ctypes.util import find_library

MagickWand = CDLL( find_library( 'MagickWand' ) )
