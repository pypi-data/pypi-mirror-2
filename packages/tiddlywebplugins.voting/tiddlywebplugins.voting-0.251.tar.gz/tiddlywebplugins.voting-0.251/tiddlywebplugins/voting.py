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
    field = "tiddlyvoting.increment"
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
      return (False,6)
    tiddler.fields[field] = str(count + value)
    logging.debug("tiddlywebplugins.voting putting tiddler %s"%tiddler.title)
    store.put(tiddler)
    return (True,"ok")
    
def allowed_operation(params):
    allowed = False
    reason = 0
    #check the user has read access
    try:
      bag = store.get(Bag(params["bag"]))
      try:
        bag.policy.allows(params["user"],"read")
        allowed = True
      except (policy.UserRequiredError,policy.ForbiddenError):
        allowed = False
        reason = 1
    except NoBagError:
      reason = 2
      allowed = False

    #check the limit of votes for that user hasnt been exceeded
    if 'increment.limit' in params['config']:
      limit = int(params['config']['increment.limit'])
      if limit <= 0:
        allowed = False
        reason = 3
      try:
        tid = store.get(Tiddler("%s increment %s in %s"%(params['username'],params['title'],params['bag']),"tiddlyvoting"))
        if tid.revision >= limit:
          allowed = False
          reason = 4
      except NoTiddlerError:
        pass
    
    #check it meets the range
    value = int(params['value'])
    if 'increment.range' in params['config']:
      lower = params['config']['increment.range'][0]
      higher = params['config']['increment.range'][1]
      if value < lower or value > higher:
        allowed = False
        reason = 7
    #what is the decision?
    return (allowed,reason)
           
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
  reason = -1
  params = get_parameters(environ)
  allowed,reason = allowed_operation(params)
  if allowed:
    if action == 'INCREMENT':
  	  success,reason = stat_increment(params)
    else:
      reason = 5
  else:
    success = False
  if success:
    save_vote(params)
  return (success,reason)
  
def save_vote(params):
  tiddler = Tiddler(params["vote_id"],"tiddlyvoting")
  tiddler.modifier = params["username"]
  tiddler.fields["topic"] = params["title"]
  tiddler.fields["value"] = params["value"]
  store.put(tiddler)


'''
reasons for failure:
"-1": "unknown error"
"1": "user not allowed to read that bag",
"2": "bag doesn't exist",
"3": "voting not allowed in bag",
"4": "user has exceeded their amount of votes",
"5": "don't know what action this is",
"6": "tiddler voting on doesn't exist"
"7": "vote is too big or too small"
'''
def operate_on_stats(environ,start_response):
  action = environ['wsgiorg.routing_args'][1]['action']
  (success,reason) = perform_action(action,environ)
  logging.debug("operate_on_stats: operation done")
  #deal with success by preventing future success
  if success:
    logging.debug("operate_on_stats: put %s to votes"%(vote_id))
    start_response('303 See Other', [('Content-Type', 'text/html; charset=utf-8'),('Location',environ.get('HTTP_REFERER', '/'))])
    return "OK"
  else:
    start_response('405 Method Not Allowed', [('Content-Type', 'text/html; charset=utf-8')])
    return reason


def string_to_float(x):
    return float(x)
def string_to_int(x):
    return int(x)

sort.ATTRIBUTE_SORT_KEY["tiddlyvoting.increment"] = string_to_float          

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