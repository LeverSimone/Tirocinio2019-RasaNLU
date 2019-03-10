from flask import Flask, jsonify, request, session
from eventlet import wsgi
import eventlet
import pymongo

import os

from validator import checkr
import rasa

app = Flask(__name__, static_url_path="/static")
app.debug = True

@app.route("/parse", methods=["GET"])
def parse_command():  
  """ Parses the user command
  Args:
       q : the user command
       conf: configuration id
  Returns:
       the parsed user command, 
       including validation against the page vocabulary
  """
  q = request.args.get('q').strip()
  conf_id = request.args.get('conf').strip()
  if not q or not conf_id:
    abort(400)  

  # parse the utterance using rasa
  nlx = rasa.parse_utterance(q)  

  # validate the user command based on vocabulary
  conf_id = int(conf_id)
  nlv = checkr.validate(nlx, conf_id)
  return jsonify(nlv)
    
  
@app.route("/configure", methods=["POST"])
def configure_nlu():
  """ Configures the vocabulary of the NLU server
  Args:
       intents : [{  
          "intent" : String, 
          "resource" : String,
          "attributes" : [String]
       }]       
  Returns:
       the configuration URI
  """  
  conf = request.json
  if not conf or not conf["intents"]:
    abort(400) 
    
  conf_id = checkr.init(conf)

  return jsonify({ "id" : conf_id}), 201

@app.route("/site", methods=["GET"])
def take_conf_id():
  """ Get the site's conf_id if it is already learned
  Args:
      site : site you want the conf_id
  Returns:
      { conf_id : conf_id }
  """
  site = request.args.get('site').strip()
  if not site:
    abort(400) 

  conf_id = checkr.takeConf_id(site)

  return jsonify({ "id" : conf_id}), 201
  
if __name__ == '__main__':
  # deploy as an eventlet WSGI server
  port = int(os.environ.get('PORT', 8080))
  client = pymongo.MongoClient("mongodb+srv://browser:dcdg45g6j@pythondb-k16qx.mongodb.net/test?retryWrites=true")
  db = client.test

  #collection = db.websites
  data = {
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
  }
  websites = db.websites
  #website_id = websites.insert_one(data).inserted_id
  #print("website_id", website_id)
  #obj = ObjectId('5c855f0082ea96347c077951')
  print(websites.find_one({"site": "http://localhost:3000/exampleonelist.html"}))
  #print(websites.find_one({"_id": obj}))
  wsgi.server(eventlet.listen(('', port)), app)    
  




