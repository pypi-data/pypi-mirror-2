from tiddlyweb.config import config
from tiddlywebplugins import voting
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.user import User
from tiddlyweb.model.policy import Policy
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.store import Store,NoTiddlerError, NoBagError, NoRecipeError
from tiddlyweb import control
import selector
from test_config import setup,votebag


def setup_module(module):
  module.store = Store(config['server_store'][0], config['server_store'][1],environ={'tiddlyweb.config': config})
  module.environ = {'tiddlyweb.store':module.store,'tiddlyweb.config': config}
  
def test_alloweduser_increments():
  setup(store)
  config['tiddlyweb.usersign']={"name":"jon"} 
  config['tiddlyweb.query'] = {"bag":["mr_and_mrs"],"tiddler":["mr strong"]}
  result = voting.perform_action('INCREMENT',config)
  assert result is True
  
  try:
    tiddler = store.get(Tiddler("mr strong","mr_and_mrs"))
    value = tiddler.fields["%s.hits"%votebag]
  except KeyError:
    value = False  
  assert value == "924"
  
  try:
    tiddler = store.get(Tiddler("jon increment mr strong in mr_and_mrs",votebag))
  except NoTiddlerError:
    tiddler = False
  assert tiddler is not False
    
def test_unauthenticated_user_increments():
  setup(store)
  config['tiddlyweb.usersign']={"name":"GUEST"} 
  config['tiddlyweb.query'] = {"bag":["mr_and_mrs"],"tiddler":["mr strong"]}
  result = voting.perform_action('INCREMENT',config)
  assert result is False

  try:
    tiddler = store.get(Tiddler("mr strong","mr_and_mrs"))
    value = tiddler.fields["%s.hits"%votebag]
  except KeyError:
    value = False  
  assert value == "923"
  

def test_unprivileged_user_increments():
  setup(store)
  config['tiddlyweb.usersign']={"name":"FND"} 
  config['tiddlyweb.query'] = {"bag":["mr_and_mrs"],"tiddler":["mr strong"]}
  result = voting.perform_action('INCREMENT',config)
  assert result is False

  try:
    tiddler = store.get(Tiddler("mr strong","mr_and_mrs"))
    value = tiddler.fields["%s.hits"%votebag]
  except KeyError:
    value = False  
  assert value == "923"
  
  
def test_multiple_votes():
  '''
  test 1  no limit
  
  '''
  setup(store)
  config['tiddlyweb.usersign']={"name":"jon"} 
  config['tiddlyweb.query'] = {"bag":["mr_and_mrs"],"tiddler":["mr small"]}
  for i in range(1,5): #there are no rules saying how big the vote can be used on this bag
    value = i * 10
    config['tiddlyweb.query']['value'] = ["%s"%value]
    voting.perform_action('INCREMENT',config)
    
  try:
    tiddler = store.get(Tiddler("mr small","mr_and_mrs"))
    value = tiddler.fields["%s.hits"%votebag]
  except KeyError:
    value = False  
  '''
  no limit in this bag so all 5 votes count
  votes = (1 * 10) + (2*10) + (3*10) + (4*10)
  = 10 + 20 + 30 + 40 = 100
  '''
  assert value == "100" 
  
  try:
    tiddler = store.get(Tiddler("jon increment mr small in mr_and_mrs",votebag))
    assert tiddler.revision == 4
  except NoTiddlerError:
    tiddler = False
  assert tiddler is not False
  
  '''
  test 2
  max 2 votes
  '''
  config['tiddlyweb.usersign']={"name":"jon"} 
  config['tiddlyweb.query'] = {"bag":["snow white"],"tiddler":["grumpy"]}
  for i in range(1,5): #the vote cannot exceed 10 in this case
     value = (i*10)
     config['tiddlyweb.query']['value'] = ["%s"%value]
     voting.perform_action('INCREMENT',config)

  try:
    tiddler = store.get(Tiddler("grumpy","snow white"))
    value = tiddler.fields["%s.hits"%votebag]
  except KeyError:
    value = False  
  '''
  votes = (1 * 10) + (2*10) + (3*10) + (4*10)
  = 10 + 20 + 30 + 40 = 100
  but a max 2 votes per user so only 10+  20 count
  '''
  assert value == "30" 

  try:
    tiddler = store.get(Tiddler("jon increment grumpy in snow white",votebag))
    assert tiddler.revision == 2
  except NoTiddlerError:
    tiddler = False
  assert tiddler is not False 
  
  
def test_minmax_votes():
  setup(store)
  config['tiddlyweb.usersign']={"name":"jon"} 
  config['tiddlyweb.query'] = {"bag":["snow white"],"tiddler":["grumpy"]}
  for i in range(-25,10): #the vote cannot exceed 10 in this case
     value = i
     config['tiddlyweb.query']['value'] = ["%s"%value]
     voting.perform_action('INCREMENT',config)

  try:
    tiddler = store.get(Tiddler("grumpy","snow white"))
    value = tiddler.fields["%s.hits"%votebag]
  except KeyError:
    value = False  
  '''
  the only votes that count bearing in mind the range -5 to 30 for values and the limit of 2 votes per user is -5 and -4 
  '''
  assert value == "-9"
