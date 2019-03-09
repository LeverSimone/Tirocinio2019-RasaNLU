from flask import Flask, jsonify, request, session
from eventlet import wsgi
import eventlet

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
    
  conf_id = checkr.init(conf["intents"])

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

  return jsonify({ "conf_id" : conf_id}), 201
  
if __name__ == '__main__':
  # deploy as an eventlet WSGI server
  port = int(os.environ.get('PORT', 8080))
  wsgi.server(eventlet.listen(('', port)), app)    
  




