import syns

def init(intents, DB):
  websites = DB.websites
  website_id = websites.insert_one(intents)
  return intents["_id"]

def takeConf_id(site, DB):
  websites = DB.websites
  structure = websites.find_one({"_id": site})
  if structure == None:
    return None
  else:
    return structure["_id"]

def validate(nlux, conf_id, DB):
  # get the specific vocabulary using conf_id
  websites = DB.websites
  structure = websites.find_one({"_id": conf_id})
  resources = structure["intents"]
  
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
    if rel != "none":
      match = {"entity" : entity, "match" : res, "relation" : rel}
      break
  return match    
  

  

