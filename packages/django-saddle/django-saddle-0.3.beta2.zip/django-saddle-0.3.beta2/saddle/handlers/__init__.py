from saddle.settings_wrapper import WWW_HANDLER
if WWW_HANDLER=='wsgi':
    from saddle.handlers.wsgi import *
elif WWW_HANDLER=='mod_python':
    from saddle.handlers.mod_python import *
else:
    raise NotImplementedError('Handler "%s" is not supported.'%WWW_HANDLER)
