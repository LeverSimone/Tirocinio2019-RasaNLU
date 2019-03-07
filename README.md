# ConWeb NLU

NLU engine for the ConWeb browser.

The models are described in markdown language in the `data` folder.


## Intallation
This project is built on [Rasa NLU](https://github.com/RasaHQ/rasa_nlu), [Spacy](https://spacy.io/) and
[NLTK](https://www.nltk.org/).

You can install the dependencies using `pipenv install`.

## Training the model
There is a script for -nix-based systems that simplifies this task. Simply run

```shell
$ ./train.sh
```
in our terminal, and the new trained models will be generated in `projects`. 

The nlu engine is organised as to understand how to interact with different types of web components.


## Deploying locally
You can deploy the module by invoking:

```shell
$ python server.py

```shell
$ heroku local
```

## Deploying to heroku

You can deploy it using any of the existing Heroku integration. The code is ready to be deployed using the git integration:

```shell
$ git init
$ heroku git:remote -a NAME_OF_YOUR_APP

$ git add .
$ git commit -m "initial commit"
$ git push heroku master
```

Check Heroku documentation: https://devcenter.heroku.com/articles/git


## REST API

Two endpoints are provied as described below. We are currently preparing a more detailed description.

### Configuring NLU
Receives the definition of the operations or intents exposed by the website.
`POST /configure
Content-type: application-json
BODY
{
   "url" : String, // Website URL
   intents : [{
       "component" : "list",       // the component
       "resource"  : "flights",    // the name of the resource
       "selector"  : "ul.movies",  // the dom selector
       "attributes" : []
   }]
RESPONSE
{ "id" :"[web configuration id]"}
`

### Parsing user queries
Parses the user input in natural language, and returns the extracted intents and entities (resources and attributes), as well as the result of the validation with the correctly identified entities (`matching`) as wella s those not found in the website (`matching_failed`)

`GET /parse?q=[user query]&conf=[website configuration id]
RESPONSE:
{ "intent" : {}, "entities" : [], "matching"; [], "matching_failed" : []}
`

## Testing console
We explose a testing console at `/static/index.html`

