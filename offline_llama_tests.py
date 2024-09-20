# this is for Lee to test offline tests using a local copy of lama

import os
import unittest
from enum import Enum

from dotenv import load_dotenv
from groq import Groq


class BtnType(Enum):
    """
    This is the enum for the button type
    """

    CLICK = 0
    UNCLICK = 1


class GUIOffline:
    """
    This is the class for the GUI
    """

    def __init__(self):
        self.__btn_state__ = [(BtnType.UNCLICK, "white"), (BtnType.UNCLICK, "white")]

    def set_button_color(self, button_index, color):
        """
        Set the background color of a button.
        """
        self.__btn_state__[button_index][1] = color

    def set_btn_gesture(self, btn_index):
        """
        Set the button to be clicked
        """
        self.__btn_state__[btn_index][0] = BtnType.CLICK

    def clear_btn_gesture(self, btn_index):
        """
        Set the button to be unclicked
        """
        self.__btn_state__[btn_index][0] = BtnType.UNCLICK

    def get_btn_state(self, btn_index):
        """
        return the state of the button
        """
        return self.__btn_state__[btn_index][0]


class TestBtnAgent(unittest.TestCase):

    def setUp(self):
        # load the key for the Groq API
        load_dotenv()
        groq_key = os.getenv("GROQ_API_KEY")
        # get the key and create a        self.__model__ = "llama3-groq-70b-8192-tool-use-preview" client
        self.__client__ = Groq(api_key=groq_key)
        self.__gui__ = GUIOffline()

    def test_groq_simple_case(self):
        """
        This is a test to make sure the groq API is working
        """
        chat_completion = self.__client__.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Explain the importance of fast language models",
                }
            ],
            model=self.__model__,
        )

        print(chat_completion.choices[0].message.content)

    def test_groq_btn_agent(self):
        """
        This is a test to make sure the btn agent is working
        """
        self.__gui__.set_btn_gesture(0)
        chat_completion = self.__client__.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Explain the importance of fast language models",
                }
            ],
            model=self.__model__,
        )

        print(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    unittest.main()
