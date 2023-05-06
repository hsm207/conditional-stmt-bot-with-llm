from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.openai_parser import parse_device_instruction


class ActionParseDeviceInstruction(Action):
    def __init__(self) -> None:

        super().__init__()

    def name(self) -> Text:
        return "action_parse_device_instruction"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        msg = tracker.latest_message["text"]

        response = parse_device_instruction(msg)

        dispatcher.utter_message(response["acknowledgement"])

        return [
            SlotSet("condition", response["condition"]),
            SlotSet("action", response["action"]),
            SlotSet("action_intent", tracker.latest_message["intent"]["name"]),
        ]
