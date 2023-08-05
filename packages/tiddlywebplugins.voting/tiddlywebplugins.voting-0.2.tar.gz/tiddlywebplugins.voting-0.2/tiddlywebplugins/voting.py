import logging
from tiddlyweb.model import policy
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.filters import FILTER_PARSERS,sort_by_attribute, sort
from tiddlyweb.store import Store, NoBagError,NoTiddlerError
from tiddlywebplugins.utils import get_store

def stat_increment(parameters):
    value = parameters["value"]
    bag = parameters["bag"]
    field = "tiddlyvoting.hits"
    title =parameters["title"]
    tiddler =Tiddler(title, bag)
    try:
      tiddler = store.get(tiddler)
      logging.debug("tiddlywebplugins.voting got tiddler with title %s"%tiddler.title)
      logging.debug("tiddlywebplugins.voting got tiddler with text %s"%tiddler.text)
      try:
        count = int(tiddler.fields[field])
      except KeyError:
        count = 0
    except NoTiddlerError:
      logging.debug("tiddlywebplugins.voting tiddler %s doesn't exist!"%title)
      return (False,"tiddler doesn't exist")
    tiddler.fields[field] = str(count + value)
    logging.debug("tiddlywebplugins.voting putting tiddler %s"%tiddler.title)
    store.put(tiddler)
    return (True,"ok")
    
def allowed_operation(params):
    allowed = False
    reason = []
    #check the user has read access
    try:
      bag = store.get(Bag(params["bag"]))
      try:
        bag.policy.allows(params["user"],"read")
        allowed = True
      except (policy.UserRequiredError,policy.ForbiddenError):
        allowed = False
        reason.append("no read access to bag")
    except NoBagError:
      reason.append("bag doesn't exist")
      allowed = False

    #check the limit of votes for that user hasnt been exceeded
    if 'increment.limit' in params['config']:
      limit = int(params['config']['increment.limit'])
      if limit <= 0:
        allowed = False
        reason = "no votes are allowed in this bag"
      try:
        tid = store.get(Tiddler("%s increment %s in %s"%(params['username'],params['title'],params['bag']),"tiddlyvoting"))
        if tid.revision >= limit:
          allowed = False
          reason = "you have exceeded your maximum allowed votes"
      except NoTiddlerError:
        pass
    
    #check it meets the range
    value = int(params['value'])
    if 'increment.range' in params['config']:
      lower = params['config']['increment.range'][0]
      higher = params['config']['increment.range'][1]
      if value < lower or value > higher:
        allowed = False
    #what is the decision?
    return (allowed,",".join(reason))
           
def get_parameters(environ):
  result = {}
  try:
    bag = environ['tiddlyweb.query']['bag'][0]
  except KeyError:
    bag = False
  try:
    title= environ['tiddlyweb.query']['tiddler'][0]
  except KeyError:
    title = False
  try:
    value = environ['tiddlyweb.query']['value'][0]
  except KeyError:
    value = "1"
    
  username= environ['tiddlyweb.usersign']["name"]
  result["value"] = int(value)
  result["username"] = username
  result["title"]=title
  result["bag"] = bag
  result["user"]=environ["tiddlyweb.usersign"]
  result["vote_id"]= "%s increment %s in %s"%(username,title,bag)
  
  #load the config
  tvconfig = {}
  try:
    tvconfigname = "config::%s"%bag
    tiddler = store.get(Tiddler(tvconfigname,"tiddlyvoting"))
    splices = tiddler.text.split("\n")
    
    for splice in splices:
      try:
        name,val = splice.split("::")
        name = name.strip()
        val =val.strip()
        if name == 'increment.range':
          lower,higher = val.split(",")
          val = [int(lower),int(higher)]
        tvconfig[name]=val
      except ValueError:
        pass
  except NoTiddlerError:
    pass
  result['config'] = tvconfig
  return result

def perform_action(action,environ):
  success = True
  params = get_parameters(environ)
  allowed,reason = allowed_operation(params)
  if allowed:
    if action == 'INCREMENT':
  	  success,reason = stat_increment(params)
    else:
      success= False
  else:
    success = False
  if success:
    save_vote(params)
  return success
  
def save_vote(params):
  tiddler = Tiddler(params["vote_id"],"tiddlyvoting")
  tiddler.modifier = params["username"]
  tiddler.fields["topic"] = params["title"]
  tiddler.fields["value"] = params["value"]
  store.put(tiddler)
  
def operate_on_stats(environ,start_response):
  action = environ['wsgiorg.routing_args'][1]['action']
  result = perform_action(action,environ)
  logging.debug("operate_on_stats: operation done")
  #deal with success by preventing future success
  if success:
    logging.debug("operate_on_stats: put %s to votes"%(vote_id))
    start_response('303 See Other', [('Content-Type', 'text/html; charset=utf-8'),('Location',environ.get('HTTP_REFERER', '/'))])
    return "OK"
  else:
    start_response('303 See Other', [('Content-Type', 'text/html; charset=utf-8'),('Location',environ.get('HTTP_REFERER', '/'))])
    return "FAIL"

def do_reset(environ,start_response):
  start_response('303 See Other', [('Content-Type', 'text/html; charset=utf-8'),('Location',environ.get('HTTP_REFERER', '/'))])
  title = get_vote_topic(environ)
  try:
    bagname = environ["tiddlyweb.query"]["bag"][0]
  except KeyError:
    bagname = False
    
  try:
    field= environ['tiddlyweb.query']['field'][0].lower()
  except KeyError:
    field = False
    
  if bagname and field and title:
    b =Bag(bagname)
    try:
      bag = store.get(b)
    except KeyError:
      bag = False
    if bag and bag.policy.allows(environ["tiddlyweb.usersign"],"write"):
      tid = Tiddler(title,bagname)
      try:
        tiddler = store.get(tid)
        tid.fields[field] = "0"
        store.put(tid)
        return "OK"
      except NoTiddlerError:
        return "FAIL"    
  else:
    return "FAIL"    

def string_to_float(x):
    return float(x)
def string_to_int(x):
    return int(x)

sort.ATTRIBUTE_SORT_KEY["rating_average"] = string_to_float
sort.ATTRIBUTE_SORT_KEY["reports"] = string_to_float        
sort.ATTRIBUTE_SORT_KEY["points"] = string_to_int              

def setup_store(config):
    global store
    store = get_store(config)
    bag = Bag("tiddlyvoting")
    try:
      store.get(bag)
    except NoBagError:
      store.put(bag)
      
def init(config_in):
    global config
    #adds a selector stats which takes an action value and tiddler to operate on
    config = config_in
    setup_store(config)
    config["selector"].add("/tiddlyvoting/reset",POST=do_reset)
    config["selector"].add("/tiddlyvoting/{action:segment}",POST=operate_on_stats)