from tiddlywebplugins import wikklytextplugins
from tiddlywebplugins.wikklytextplugins.plugins import macros
from tiddlyweb.config import config
from test_common import WikiArgument,WikiContext
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.config import config
from tiddlyweb.store import Store, NoBagError,NoTiddlerError

def setup_module(module):
    module.store = Store(config['server_store'][0], config['server_store'][1],environ={'tiddlyweb.config': config})
    module.environ = {'tiddlyweb.store':module.store,'tiddlyweb.config': config}

def test_tiddlers():
    #setup
    wikklytextplugins.init({})
    store.put(Bag("foo"))
    
    tid = Tiddler("jon robson","foo")
    tid.text = "My name is Jon Robson"
    tid.tags = ["Yes"]
    store.put(tid)
    tid = Tiddler("a tiddler in foo","foo")
    tid.text = "rainbow [[title]]"
    tid.tags = ["Yes"]
    store.put(tid)
    
    tid = Tiddler("nothereTiddler","foo")
    tid.text = "rainbow [[title]]"
    tid.tags = ["No"]
    store.put(tid)
    
    tid = Tiddler("template","foo")
    tid.text = "<<echo hello>>"
    store.put(tid)
     
    out = macros.tiddlers(WikiContext(tid,config),WikiArgument("template"),WikiArgument("filter:[tag[Yes]]"))
    assert "hello" in out

    
    #teardown
    store.delete(Bag("foo"))