## SmartGuide final version

This is the code for deploying the SmartGuide chatbot in a cluster in Okteto which contains Rasa server, Action server, Chatbot/front-end server and FastAPI server (where the model to answer the immigration questions is). 

There are two files that are missing, and you can find them both in the repository https://github.com/andre-garcia/SmartGuideFinal because they were too big to be uploaded to github via web:

- `models/20230927-090242-rounded-line.tar.gz` - the file with the latest trained Rasa model (not to be confused with the model in the fastAPI app). This file should be put in the ./models folder (you can also train your own model, but keep in mind this will take a LONG time, given the size of our NLU file)
- `fastAPI/bert.pkl` - this file is the pickled version of the SentenceTransformer model, used to get the answers to the immigration queries, which should be put in the ./fastAPI folder. i

if you prefer to create your own `bert.pkl` file instead, all you have to do is run this code locally: 

`from sentence_transformers import SentenceTransformer`
`import pickle`
`bert = SentenceTransformer('all-MiniLM-L6-v2')`
`with open("bert-2.pkl", 'wb') as f:`
`    pickle.dump(bert, f)`

Setting-up
--------------------

Please follow Irene's instructions for general set-up/deployment:

https://github.com/OmdenaAI/toronto-canada-smartguide/tree/task-8-chatbot-deployment-isam007#readme

Only extra thing to keep in mind is that you need to change some endpoints in some files in order for things to work. You need to replace the text there with your own Rasa/Action/FastAPI/Chatbot server:

1. in `credentials.yml`: 
- cors_origins: ["https://YOURFRONTENDSERVER.cloud.okteto.net"] # replace YOURFRONTENDSERVER with your Okteto front-end (chatbot) server
- rasa:
  url: "https://YOURRASASERVER.cloud.okteto.net/api" # replace YOURRASASERVER with your Okteto Rasa server

2. in `endpoints.yml`:
- action_endpoint:
  url: "https://YOURACTIONSERVER.cloud.okteto.net/webhook" # replace YOURACTIONSERVER with your Okteto Rasa server

3. in `actions/actions.py`:
- base_url = "https://YOURFASTAPISERVER.cloud.okteto.net/api/v1/qa" # replace YOURFASTAPISERVER with your Okteto FastAPI server

4. in `chatbot/static/js/constants.js`:
- const rasa_server_url = "https://YOURRASASERVER.cloud.okteto.net/webhooks/rest/webhook"; # replace YOURRASASERVER with your okteto Rasa server
