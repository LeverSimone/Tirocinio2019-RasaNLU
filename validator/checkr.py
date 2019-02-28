import syns

resources = [{ "resource" : "proposals", "attributes" : ["topics", "price"]},
            { "resource" : "cat", "attributes" : []}]

def init(intents):
  return

def validate(nlux, conf_id):
  # get the specific vocabulary using conf_id
  # TBD
  
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
      success.append(resource)
      break
  
  # we verify the attribute for the matching resource
  for entity in nlux["entities"]:
    if (entity["entity"] == "attribute"):
      resource = match_entity(entity, lambda x : x, success[0].attributes)
      success.append(resource)
      break 
      
  if not resource:
    failed.append(resource)

  print resource
  nlux["matching"] = [resource]
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
  

  

