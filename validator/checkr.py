import syns

RESOURCE_LIST = [{
 "intents": [
  {
   "component": "list",
   "resource": "cat",
   "attributes": [
    "topic",
    "hours"
   ],
   "tag": "ul"
  }
 ],
 "site": "http://localhost:3000/exampleonelist.html"
}]

def init(intents):
  global RESOURCE_LIST
  RESOURCE_LIST = []
  RESOURCE_LIST.append(intents)
  return len(RESOURCE_LIST)

def takeConf_id(site):
  for posx,x in enumerate(RESOURCE_LIST):
    if site==x["site"]:
      return posx + 1

def validate(nlux, conf_id):
  # get the specific vocabulary using conf_id
  resources = RESOURCE_LIST[conf_id - 1]["intents"]
  #print("\n\nresources", resources)
  #print(RESOURCE_LIST[conf_id - 1]['site'])
  
  # verify extracted entities
  # TODO / comments:
  # - we are assuming only one "resource" at the moment, and this may not
  #   be the case in the future
  # - in principle a word could match more than one resource, an we
  #   we need a way to put a score on this, or ask the user to dissambiguate
  success = []
  failed = []
  for entity in nlux["entities"]:
    if (entity["entity"] == "resource"):
      resource = match_entity(entity, lambda x : x["resource"], resources)      
      if not resource:
        failed.append(entity)
      else:
        success.append(resource)
      break
  
  if success:
    # we verify the attribute for the matching resource
    for entity in nlux["entities"]:
      if (entity["entity"] == "attribute"):
        resource = match_entity(entity, lambda x : x, success[0].get("match").get("attributes"))
        if not resource:
          failed.append(entity)
        else:
          success.append(resource)
        break
      
  nlux["matching"] = success
  nlux["matching_failed"] = failed
  return nlux


def match_entity(entity, fn, items):
  match = {}
  for res in items:
    word = fn(res)
    rel = syns.get_relation(entity[u"value"], word)
    print rel
    if rel != "none":
      match = {"entity" : entity, "match" : res, "relation" : rel}
      break
  return match    
  

  

