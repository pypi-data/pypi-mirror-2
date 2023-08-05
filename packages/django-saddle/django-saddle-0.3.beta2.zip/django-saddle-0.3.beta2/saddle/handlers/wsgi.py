'''
mod_wsgi handler
'''

from saddle import settings_wrapper
import os, site

os.environ['DJANGO_SETTINGS_MODULE']='saddle.settings_wrapper'
os.environ['PYTHON_EGG_CACHE']=os.path.join(
    settings_wrapper.VIRTUALENV_ROOT, '.egg-cache',)

site.addsitedir(settings_wrapper.VIRTUALENV)

from django.core.handlers import wsgi
application=wsgi.WSGIHandler()
