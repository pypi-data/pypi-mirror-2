import pkg_resources
import urllib2
import os.path

from urlparse import urlsplit

from zope.interface import directlyProvides
from zope.interface import directlyProvidedBy

from zope.globalrequest import getRequest
from zope.globalrequest import setRequest

from ZPublisher.Publish import dont_publish_class
from ZPublisher.Publish import missing_name
from ZPublisher.mapply import mapply

from AccessControl import Unauthorized
from zExceptions import NotFound

from lxml import etree

from Products.CMFCore.utils import getToolByName

try:
    from zope.site.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

class ExternalResolver(etree.Resolver):
    """Resolver for external absolute paths (including protocol)
    """
    
    def resolve(self, system_url, public_id, context):
        
        # Expand python:// URI to file:// URI
        url = resolveURL(system_url)
        
        # Resolve file:// URIs as absolute file paths
        if url.startswith('file://'):
            filename = url[7:]
            return self.resolve_filename(filename, context)
        
        # Resolve other standard URIs with urllib2
        if (
            url.startswith('http://') or
            url.startswith('https://') or
            url.startswith('ftp://')
        ):
            return self.resolve_file(urllib2.urlopen(url), context)

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
            
        # Attempt to traverse
        
        clonedRequest = cloneRequest(request, url)
        try:
            
            try:
                traversed = traverse(clonedRequest, path)
            except (Unauthorized, NotFound,):
                return None
            
            invoked = invoke(clonedRequest, traversed)
        finally:
            clonedRequest.clear()
            
            if getRequest() is not request:
                setRequest(request)
        
        return self.resolve_string(invoked, context)

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
    

def resolveURL(url):
    """Resolve the input URL to an actual URL.
    
    This can resolve python://dotted.package.name/file/path URLs to file://
    URIs.
    """
    
    if not url:
        return url
    
    if url.lower().startswith('python://'):
        spec = url[9:]
        filename = pkg_resources.resource_filename(*spec.split('/', 1))
        if filename:
            if os.path.sep != '/':
                filename = filename.replace(os.path.sep, '/')
                return 'file:///%s' % filename
            return 'file://%s' % filename
    
    return url

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
    """Try to get HTTP host even if there's no HOST header.
    """
    
    base = request.get('BASE0')
    if base:
        divider = base.find('://')
        if divider > 0:
            base = base[divider+3:]
        
        if base:
            return base
    
    host = request.get('HTTP_HOST')
    if host:
        return host
    
    return "%s:%s" % (request.get('SERVER_NAME'), request.get('SERVER_PORT'))


# Functions used to perform an in-Zope traversal

def cloneRequest(request, url):
    """Clone the given request for use in traversal to the given URL.
    
    This will set up request.form as well.
    
    The returned request should be cleared with request.clear(). It should
    *not* be closed with request.close(), since this fires EndRequestEvent,
    which in turn disables the site-local component registry.
    """
    # normalise url and split query string
    _, _, urlPath, urlQuery, _ = urlsplit(url)
    
    # Clone the request so that we can traverse from it.
    requestClone = request.clone()
    
    # Make sure the new request provides the same markers as our old one
    directlyProvides(requestClone, *directlyProvidedBy(request))
    
    # Update the path and query string to reflect the new value
    requestClone.environ['PATH_INFO'] = urlPath
    requestClone.environ['QUERY_STRING'] = urlQuery
    
    requestClone.processInputs()
    
    return requestClone
    

def traverse(request, path):
    """Traverse to the given URL, simulating URL traversal.
    
    Returns the traversed-to object. May raise Unauthorized or NotFound.
    """
    
    return request.traverse(path)

def invoke(request, traversed):
    """Invoke a traversed-to object in the same manner that the publisher
    would.
    """
    
    return mapply(traversed, positional=request.args,
                  keyword=request,
                  debug=None,
                  maybe=1,
                  missing_name=missing_name,
                  handle_class=dont_publish_class,
                  context=request,
                  bind=1)
