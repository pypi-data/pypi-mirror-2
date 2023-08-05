import re
import logging

from lxml import etree
from repoze.xmliter.utils import getHTMLSerializer

from zope.interface import implements, Interface
from zope.component import adapts
from plone.transformchain.interfaces import ITransform

from threading import Lock
from plone.synchronize import synchronized

from Acquisition import aq_base
from Globals import DevelopmentMode

from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from xdv.compiler import compile_theme

from collective.xdv.interfaces import ITransformSettings, IXDVLayer
from collective.xdv.utils import getHost, resolveURL, expandAbsolutePrefix, ExternalResolver, InternalResolver

try:
    from zope.site.hooks import getSite
except ImportError:
    from zope.app.component.hooks import getSite

HTML_DOC_PATTERN = re.compile(r"^.*<\s*html(\s*|>).*$",re.I|re.M)
LOGGER = logging.getLogger('collective.xdv')

class _Cache(object):
    """Simple cache for the transform and notheme regular expressions
    """
    
    _lock = Lock()
    _notheme = None
    _themes = None
    _transform = {}
    
    @property
    @synchronized(_lock)
    def notheme(self):
        return self._notheme
    
    @property
    @synchronized(_lock)
    def themes(self):
        return self._themes
    
    @property
    @synchronized(_lock)
    def transform(self):
        return self._transform
    
    @synchronized(_lock)
    def clear(self):
        self._notheme = None
        self._themes = None
        self._transform = {}
    
    @synchronized(_lock)
    def update_notheme(self, notheme):
        self._notheme = notheme
    
    @synchronized(_lock)
    def update_themes(self, themes):
        self._themes = themes
    
    @synchronized(_lock)
    def update_transform(self, theme_id, transform):
        self._transform[theme_id] = transform

CACHES = {}

def getCache():
    site = getSite()
    if site is None:
        return None
    
    try:
        cacheKey = '/'.join(site.getPhysicalPath())
    except AttributeError:
        cacheKey = id(aq_base(site))
    
    if cacheKey not in CACHES:
        cache = CACHES[cacheKey] = _Cache()
        return cache
    
    return CACHES[cacheKey]

def invalidateCache(proxy, event):
    """When our settings are changed, invalidate the cache
    """
    for cache in CACHES.values():
        cache.clear()

class XDVTransform(object):
    """Late stage in the 8000's transform chain. When plone.app.blocks is
    used, we can benefit from lxml parsing having taken place already.
    """
    
    implements(ITransform)
    adapts(Interface, IXDVLayer)
    
    order = 8850
    
    def __init__(self, published, request):
        self.published = published
        self.request = request

    def setupTransform(self):
        
        request = self.request
        
        cache = getCache()
        if cache is None:
            return None
        
        # Never style 127.0.0.1 - we want to be able to get back into Plone
        # if things go really wrong.
        
        host = getHost(request)
        if not host or host.startswith('127.0.0.1:'):
            return None
        
        # Obtain xdv settings. Do nothing if not found
        
        registry = queryUtility(IRegistry)
        if registry is None:
            return None
        
        try:
            settings = registry.forInterface(ITransformSettings)
        except KeyError:
            return None
        
        if settings is None:
            return None
        
        if not settings.enabled:
            return None
        
        # Test that we're on a domain that should be themed
        
        domains = settings.domains
        if not domains:
            return None
        
        found_domain = False
        for domain in domains:
            if domain.lower() == host.lower():
                found_domain = True
                break
        if not found_domain:
            return None
        
        # Find real or virtual path - PATH_INFO has VHM elements in it
        actual_url = request.get('ACTUAL_URL')
        server_url = request.get('SERVER_URL')
        path = actual_url[len(server_url):]
        
        # Check if we're on a path that should be ignored
        notheme = None
        
        if not DevelopmentMode:
            notheme = cache.notheme
        
        if notheme is None:
            notheme = [re.compile(n) for n in (settings.notheme or [])]
        
            if not DevelopmentMode:
                cache.update_notheme(notheme)
        
        if notheme:
            if not path:
                path = '/'
            for pattern in notheme:
                if pattern.match(path):
                    return None
        
        theme = settings.theme
        rules = settings.rules
        theme_id = u'default'
        
        # If alternate_themes are set, resolve theme files
        alternate_themes = settings.alternate_themes
        if alternate_themes:
            themes = None
            if not DevelopmentMode:
                themes = cache.themes
            
            if themes is None:
                themes_settings = [ n.split('|') for n in alternate_themes]
                themes = [ (re.compile(n[0]),n[0],n[1],n[2]) for n in themes_settings]
                
                if not DevelopmentMode:
                    cache.update_themes(themes)
                
            # if we find a match, replace the original theme
            if themes:
                for pattern, i_theme_id, i_theme, i_rules in themes:
                    if pattern.match(path):
                        theme = i_theme
                        rules = i_rules
                        theme_id = i_theme_id
                        break
        
        if not theme or not rules or not theme_id:
            return None
        
        # Apply theme
        transform = None
        
        if not DevelopmentMode:
            transform = cache.transform.get(theme_id)
        
        if transform is None:
            extraurl = settings.extraurl or None
            absolute_prefix = settings.absolute_prefix or None
            xinclude = settings.xinclude or False
            
            if absolute_prefix:
                absolute_prefix = expandAbsolutePrefix(absolute_prefix)
        
            if extraurl:
                extraurl = resolveURL(extraurl)
                
            rules = resolveURL(rules)
            theme = resolveURL(theme)
            
            externalResolver = ExternalResolver()
            internalResolver = InternalResolver()
            
            rules_parser = etree.XMLParser(recover=False)
            rules_parser.resolvers.add(externalResolver)
            rules_parser.resolvers.add(internalResolver)
            
            theme_parser = etree.HTMLParser()
            theme_parser.resolvers.add(externalResolver)
            theme_parser.resolvers.add(internalResolver)
            
            compiler_parser = etree.XMLParser()
            compiler_parser.resolvers.add(externalResolver)
            compiler_parser.resolvers.add(internalResolver)
            
            compiled_theme = compile_theme(rules, theme,
                    extra=extraurl,
                    xinclude=xinclude,
                    absolute_prefix=absolute_prefix,
                    compiler_parser=compiler_parser,
                    parser=theme_parser,
                    rules_parser=rules_parser,
                )
            
            if not compiled_theme:
                return None
            
            transform = etree.XSLT(compiled_theme)
            
            if not DevelopmentMode:
                cache.update_transform(theme_id, transform)
        
        return transform
    
    
    def parseTree(self, result):
        content_type = self.request.response.getHeader('Content-Type')
        if content_type is None or not content_type.startswith('text/html'):
            return None
        
        content_encoding = self.request.response.getHeader('Content-Encoding')
        if content_encoding and content_encoding in ('zip', 'deflate', 'compress',):
            return None
        
        try:
            return getHTMLSerializer(result)
        except (TypeError, etree.ParseError):
            return None
    
    def transformString(self, result, encoding):
        return self.transformIterable([result], encoding)
    
    def transformUnicode(self, result, encoding):
        return self.transformIterable([result], encoding)
    
    def transformIterable(self, result, encoding):
        """Apply the transform if required
        """
        
        result = self.parseTree(result)
        if result is None:
            return None
        
        transform = self.setupTransform()
        if transform is None:
            return None
        
        result.tree = transform(result.tree)
        
        return result
