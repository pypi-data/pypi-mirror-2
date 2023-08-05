from lib import MagickWand

#===============================================================================
# API
#===============================================================================
class API( object ):
    def __init__( self, lib ):
        self.lib = lib
        self.functions = {}

    def register( self, name, restype = None, argtypes = None ):
        self.functions[name] = self.lib[ name ]
        self.functions[name].restype = restype
        self.functions[name].argtypes = argtypes
        return self.functions[name]

    def register_all( self, list ):
        for ( name, restype, argtypes ) in list:
            self.register( name, restype, argtypes )

    def __getattr__( self, name ):
        if self.functions.has_key( name ): return self.functions[name]
        else:
            raise KeyError( 'please register the function %s' % name )

api = API( MagickWand )
