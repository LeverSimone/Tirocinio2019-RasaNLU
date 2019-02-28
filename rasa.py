from rasa_nlu.model import Interpreter
import os

class Struct:
  def __init__(self, **entries):
    self.__dict__.update(entries)



def parse_utterance(ureq):

  nlout = interpreter.parse(unicode(ureq))
  return nlout

def get_latestmodel(d):

  dirs = [os.path.join(d, o) for o in os.listdir(d) 
                      if os.path.isdir(os.path.join(d,o))]
  
  dirs = ((os.stat(path).st_mtime, path) for path in dirs)

  return (sorted(dirs).pop())[1]


# get the latest model and load it
modeldir = get_latestmodel("./projects/components/")
interpreter = Interpreter.load(modeldir)
  
