
import urlimport, sys, os
#sys.path.insert(0, "https://freeway.resheteva.lan/~alex/googlepages2")
#sys.path.insert(0, "http://alex:rama0ET4@freeway.resheteva.lan/~alex/googlepages")
#sys.path.insert(0, "http://alex:rama0ET4@resheteva.org/~alex/googlepages$PYTHON_VERSION")
sys.path.insert(0, "http://alex:rama0ET4@resheteva.org/~alex/googlepages")
#sys.path.insert(0, "http://www.imp17.com/urlimport/googlepages")

urlimport.config(
    **{'ssl_key.freeway.resheteva.lan':'resheteva_client_privkey.pem', 
       'ssl_cert.freeway.resheteva.lan':'resheteva_client_cert.pem', 
       'debug':4, 'no_cache.freeway.resheteva.lan':False, 
       'user_agent':'urllib2-urlimport', 
       'cache_dir':'urlimport-cache_dir'
      }
)

sys.path_importer_cache.clear()

from mod1 import ui, sui

print '------- mod2 -------'
import mod2
print '=============='
reload(mod2)
#print repr(mod2.__dict__)
print '------ submod.spam --------'
import submod.spam
print '=============='
#reload(submod.spam)
# segmentation fault below. but this module does reload if imported normally
status = submod.spam.system("cd" if os.name == "nt" else 'pwd')
print repr(submod.spam.__dict__)

#cache_reset()
