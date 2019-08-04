import syns

def composeConf(structure):
  listResources = {"component": "list", "resources": set()}
  result = {"id": structure["_id"], "comp_res": list()}
  for res in structure["intents"]:
    if res["component"] == "list":
      listResources["resources"].add(res["resource"])
    elif res["component"] == "article":
      result["comp_res"].append({"component": "article", "resources": list()})
  listResources["resources"] = list(listResources["resources"])
  if len(listResources["resources"]) > 0:
    result["comp_res"].append(listResources)
  return result


def init(intents, DB):
  websites = DB.websites
  website_id = websites.insert_one(intents)
  result = composeConf(intents)
  return result

def takeConf(site, DB):
  websites = DB.websites
  structure = websites.find_one({"_id": site})
  if structure == None:
    return None
  else:
    result = composeConf(structure)
    #with article-structure we need to send the complete structure of the site to check if the site requested is an article with Puppeteer
    result["structure"] = structure["intents"]
    return result

def siteMatchFunc (structures, originalLink):
  siteMatch = -1
  index = 0
  countMatch = 0
  countMax = 0
  for structure in structures:
    for idx, character in enumerate(structure["_id"]):
      if (idx < len(originalLink)):
        if (character == originalLink[idx]):
          countMatch+=1
    if (countMatch > countMax):
      countMax = countMatch
      siteMatch = structure
    index+=1
  if siteMatch < 0:
    return None
  else: 
    return siteMatch

def takeConfs(site, DB):
  websites = DB.websites
  #cerco il link esatto
  structure = websites.find_one({"_id": site})
  if structure!=None:
    result = composeConf(structure)
  elif structure==None:
    #link esatto non trovato, restituisco le struttura in cui il link fa maggiormente matching
    posSlash = site.index("/", 8)
    domainSite = site[:posSlash]
    structures = websites.find({"$and": [{"_id": {"$regex": domainSite}}, {"multiple": "true"}]})
    if structures.count() == 0:
      return None
    else:
      siteConf = siteMatchFunc(structures, site)
      if(siteConf != None):
        result = composeConf(siteConf)
  return result

def validate(nlux, conf_id, DB):
  # get the specific vocabulary using conf_id
  websites = DB.websites
  structure = websites.find_one({"_id": conf_id})
  intents = structure["intents"]
  compatibleIntents = []
  # verify extracted entities
  # TODO / comments:
  # - we are assuming only one "resource" at the moment, and this may not
  #   be the case in the future
  intentUser = nlux["intent"]["name"]
  for intent in intents:
    if(intent["component"] in intentUser):
      compatibleIntents.append(intent)
  #se compatibleIntents e' vuoto non ci sono componenti su cui applicare una determinata azione
  if (len(compatibleIntents)== 0):
    return {"intentNotCompatible": intentUser}
  elif "list" in intentUser:
    success = []
    failed = []
    dissambiguate = {"category": [], "resource": None}
    for entity in nlux["entities"]:
      if (entity["entity"] == "resource"):
        resource = match_entity(entity, lambda x : x["resource"], compatibleIntents, lambda x : x["category"])      
        category = match_entity(entity, lambda x : x["category"], compatibleIntents, None) 
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
  

  

