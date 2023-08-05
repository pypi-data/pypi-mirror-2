import pkg_resources
import urllib2
import os.path

from urlparse import urlsplit

from zope.globalrequest import getRequest
from plone.subrequest import subrequest

from AccessControl import Unauthorized
from zExceptions import NotFound

from lxml import etree

from Products.CMFCore.utils import getToolByName

try:
    from zope.site.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

class PythonResolver(etree.Resolver):
    """Resolver for python:// paths
    """
    
    def resolve(self, system_url, public_id, context):
        if not system_url.lower().startswith('python://'):
            return None
        filename = resolvePythonURL(system_url)
        return self.resolve_filename(filename, context)


def resolvePythonURL(url):
    """Resolve the python resource url to it's path
    
    This can resolve python://dotted.package.name/file/path URLs to paths.
    """
    assert url.lower().startswith('python://')
    spec = url[9:]
    package, resource_name = spec.split('/', 1)
    filename = pkg_resources.resource_filename(package, resource_name)
    return filename


class InternalResolver(etree.Resolver):
    """Resolver for internal absolute and relative paths (excluding protocol).
    If the path starts with a /, it will be resolved relative to the Plone
    site navigation root.
    """
    
    def resolve(self, system_url, public_id, context):
        
        request = getRequest()
        if request is None:
            return None
        
        # Ignore URLs with a scheme
        if '://' in system_url:
            return None
        
        # Ignore the special 'xdv:' resolvers
        if system_url.startswith('xdv:'):
            return None
        
        # Try to turn a relative path into an absolute one
        if not system_url.startswith('/'):
            
            currentURL = request.get('ACTUAL_URL', None)
            if currentURL is None:
                return None
            
            _, _, currentPath, _, _ = urlsplit(currentURL)
            
            path = normalizePath(currentPath, system_url)
            url = request.get('SERVER_URL', '') + path
            
        else:
            prefix = getPloneSitePath()
            path = normalizePath(prefix, system_url)
            url = request.get('SERVER_URL', '') + path
            
        try:
            response = subrequest(path)
        except (Unauthorized, NotFound,):
            return None
        result = response.body or response.stdout.getvalue()
        return self.resolve_string(result, context)

def normalizePath(prefix, path):
    """Like os.path.join(os.path.normpath(prefix, path)), but always use /
    as path separator.
    """
    
    if path.startswith('/'):
        path = path[1:]
    
    path = os.path.normpath(os.path.join(prefix, path))
    if os.path.sep != '/':
        path = path.replace(os.path.sep, '/')
    return path

def getPloneSitePath():
    """Return the path to the Plone site root
    """
    
    site = getSite()
    if site is None:
        return ''
        
    portal_url = getToolByName(site, 'portal_url', None)
    if portal_url is None:
        return ''
    
    path = portal_url.getPortalObject().absolute_url_path()
    if path and path.endswith('/'):
        path = path[:-1]
    
    return path

def expandAbsolutePrefix(prefix):
    """Prepend the Plone site URL to the prefix if it starts with /
    """
    
    if not prefix:
        return prefix
    
    if not prefix.startswith('/'):
        return prefix
    
    return getPloneSitePath() + prefix

def getHost(request):
    """Return the host (possibly including the _vh_ path)
    """
    base = request.get('BASE1')
    _, base = base.split('://', 1)
    return base.lower()
