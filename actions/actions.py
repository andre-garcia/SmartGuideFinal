import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher



# action from Vijay
class ActionGetQA(Action):
    def name(self) -> Text:
        return "action_immigration_questions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        question = tracker.latest_message['text']

        response = self.get_immigration_qs(question)


        dispatcher.utter_message(text="Here is some information that might be useful to you, as well as the source where I took it from:")

        dispatcher.utter_message(text=response)
        return []


    @staticmethod
    def get_immigration_qs(question: str) -> str:
        base_url = "https://YOURFASTAPISERVER.cloud.okteto.net/api/v1/qa"
        params = {
            "prompt": question
        }

        try:
            print(f"API Request URL: {base_url}?{params}")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            api_response = response.json()
            print(f"API Response: {api_response}")
            return api_response
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            # return None  # Return {} in case of exception
            return f"API Request Error: {e}"




# Hello World action added for debugging purposes

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

# Action to be triggered when the bot starts
# talking before the user
class ActionHello(Action):

    def name(self) -> Text:
        return "action_hello"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello! You can ask me questions related to immigrating to Canada. Keep in mind I am still under development and always double-check the information I provide. :) Please explain your doubt with details.")

        return []
