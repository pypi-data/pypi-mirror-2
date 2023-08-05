# -*- coding: utf-8 -*-
import tenjin
from tenjin.helpers import *
import re

##
## message catalog to translate message
##
MESSAGE_CATALOG = {
    'en': { 'Hello': 'Hello',
            'Good bye': 'Good bye',
	  },
    'fr': { 'Hello': 'Bonjour',
            'Good bye': 'Au revoir',
	  },
}

##
## create translation function and return it.
## ex.
##    _ = create_m18n_func('fr')
##    print _('Hello')   #=> 'Bonjour'
##
def create_m18n_func(lang):
    dct = MESSAGE_CATALOG.get(lang)
    if not dct:
        raise ValueError("%s: unknown lang." % lang)
    def _(message_key):
        return dct.get(message_key)
    return _
    # or return dct.get
    
##
## cache storage class to cache template object for each language
##
class M17nCacheStorage(tenjin.MarshalCacheStorage):

    lang = 'en'       # default language

    def __init__(self, *args, **kwargs):
        if 'lang' in kwargs:
	    lang = kwargs.pop('lang')
	    if lang: 
	        self.lang = lang
	tenjin.MarshalCacheStorage.__init__(self, *args, **kwargs)

    ## change cache filename to 'file.pyhtml.lang.cache'
    def _cachename(self, fullpath):
        return "%s.%s.cache" % (fullpath, self.lang)

##
## test program
##
if __name__ == '__main__':

    ## create cache storage and engine for English
    m17ncache = M17nCacheStorage(lang='en')
    engine_en = tenjin.Engine(preprocess=True, cache=m17ncache)

    ## render html for English
    context = { 'username': 'World' }
    context['_'] = create_m18n_func('en')
    html = engine_en.render('m18n.pyhtml', context)
    print("--- lang: en ---")
    print(html)
    
    ## create cache storage and engine for French
    m17ncache = M17nCacheStorage(lang='fr')
    engine_fr = tenjin.Engine(preprocess=True, cache=m17ncache)

    ## render html for French
    context = { 'username': 'World' }
    context['_'] = create_m18n_func('fr')
    html = engine_fr.render('m18n.pyhtml', context)
    print("--- lang: fr ---")
    print(html)
