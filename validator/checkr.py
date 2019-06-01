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
  dissambiguate = {"category": [], "resource": None}
  for entity in nlux["entities"]:
    if (entity["entity"] == "resource"):
      resource = match_entity(entity, lambda x : x["resource"], resources, lambda x : x["category"])      
      category = match_entity(entity, lambda x : x["category"], resources, None) 
      print(resource)
      print("------------------")
      print(category)
      if not resource and not category:
        failed.append(entity)
      elif category:
        if (len(category) > 1):
          count = 0
          for cat in category:
            if (cat["relation"] == "equal"):
              success.append(cat)
              break
          if not success:
            for cat in category:
              dissambiguate["category"].append(cat["match"]["category"])
            dissambiguate["resource"] = entity["value"]
        else:
          success.append(category[0])
      elif resource:
        if (len(resource) > 1):
          count = 0
          for res in resource:
            if (res["relation"] == "equal"):
              temp = res
              count +=1
          if (count==1):
            success.append(temp)
          if not success:
            for res in resource:
              dissambiguate["category"].append(res["category"])
            dissambiguate["resource"] = resource[0]["match"]["resource"]
        else:
          success.append(resource[0])
      break
  
  if success:
    # we verify the attribute for the matching resource
    for entity in nlux["entities"]:
      if (entity["entity"] == "attribute"):
        resource = match_entity(entity, lambda x : x, success[0].get("match").get("attributes"), None)
        if not resource:
          failed.append(entity)
        else:
          success.append(resource[0])
        break
      
  nlux["matching"] = success
  nlux["matching_failed"] = failed
  nlux["dissambiguate"] = dissambiguate
  return nlux


def match_entity(entity, fn, items, fnCat):
  match = []
  for res in items:
    word = fn(res)
    if(isinstance(word, dict)):
      word=word["name"]
    rel = syns.get_relation(entity[u"value"], word)
    if rel != "none":
      if fnCat and res["category"]:
        match.append({"entity" : entity, "match" : res, "relation" : rel, "category": fnCat(res)})
      else:
        match.append({"entity" : entity, "match" : res, "relation" : rel})
  return match    
  

  

