from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from deep_translator import GoogleTranslator
from openai import OpenAI
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# OpenAI API key
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)
class ActionImproveSpeaking(Action):
    def name(self) -> Text:
        return "action_improve_speaking"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        response = "To improve your speaking skills, practice speaking with native speakers regularly."
        dispatcher.utter_message(text=response)
        return []

class ActionImproveVocabulary(Action):
    def name(self) -> Text:
        return "action_improve_vocabulary"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        response = "You can enhance your vocabulary by reading more books and writing down new words."
        dispatcher.utter_message(text=response)
        return []

class ActionImproveListening(Action):
    def name(self) -> Text:
        return "action_improve_listening"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        response = "Try listening to podcasts and watching movies without subtitles."
        dispatcher.utter_message(text=response)
        return []

class ActionImproveReadingWriting(Action):
    def name(self) -> Text:
        return "action_improve_reading_writing"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        response = "Practice reading books and writing essays to improve your skills."
        dispatcher.utter_message(text=response)
        return []

class ActionImproveGrammar(Action):
    def name(self) -> Text:
        return "action_improve_grammar"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        response = "Focus on sentence structure and practice writing more."
        dispatcher.utter_message(text=response)
        return []

class ActionLearnCulture(Action):
    def name(self) -> Text:
        return "action_learn_culture"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        response = "Learn about English-speaking culture by exploring their customs and traditions."
        dispatcher.utter_message(text=response)
        return []

class ActionAnalyzeEntities(Action):
    def name(self) -> Text:
        return "action_analyze_entities"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get('text')
        doc = nlp(user_message)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        dispatcher.utter_message(text=f"Entities detected: {entities}")
        return []

class ActionChatGPT(Action):
    def name(self) -> Text:
        return "action_chatgpt"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        try:
            user_message = tracker.latest_message.get('text')
            # Sử dụng API ChatCompletion mới của GPT-3.5
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150
            )
            gpt_reply = response['choices'][0]['message'].content.strip()
            dispatcher.utter_message(text=gpt_reply)
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred: {str(e)}")
        return []

class ActionTranslateToLanguage(Action):
    def name(self) -> Text:
        return "action_translate_to_language"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        try:
            user_message = tracker.latest_message.get('text')
            translator = GoogleTranslator(source='auto', target='vi')  # You can replace 'vi' with other languages
            translation = translator.translate(user_message)
            dispatcher.utter_message(text=f"Translation: {translation}")
        except Exception as e:
            dispatcher.utter_message(text=f"An error occurred while translating: {str(e)}")
        return []
