from simple_LLM_call_tests import MODEL
from tool_box import Tool_Box
import test_utills as TU
from agent_8_15_2024_modular_1 import load_tools

class Mock_GUI():
    def get_button_color(self, button_index):
        print("get_button_color", button_index)
        return "red"

    def get_number_of_buttons(self):
        print("get_number_of_buttons")
        return 3

    def set_button_color(self, button_index, color_name):
        print("set_button_color", button_index, color_name)
        pass

from tool_box import Tool_Box

def simple_tests(singe_step_call_tester):
    singe_step_call_tester.reset_ground_truth()
    # test 1
    command = "make button 1 blue"
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 1, "color_name": "blue"})
    r1 = singe_step_call_tester.test(command)
    if not r1:
        print("simple_tests: failed 'make button 1 blue'")
        return False

    # test 2
    singe_step_call_tester.reset_ground_truth()
    command = "what is the color of button 1"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed: " + command)
        return False

    # test 3
    singe_step_call_tester.reset_ground_truth()
    command = "copy the color from button 1 to button 0"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        return False

    # test 4
    singe_step_call_tester.reset_ground_truth()
    command = "copy the color from button 1 to button 2"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        return False

        # test 5
    singe_step_call_tester.reset_ground_truth()
    command = "make button 1 the same color as button 2"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 2})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        return False
    # test 6

    singe_step_call_tester.reset_ground_truth()
    command = "make button 2 and button 3 green"
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 2, "color_name": "green"})
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 3, "color_name": "green"})
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        return False

    singe_step_call_tester.reset_ground_truth()
    command = "What color is the sky during the day"
    singe_step_call_tester.add_non_call_condition("'Blue' is in the text")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        return False

    singe_step_call_tester.reset_ground_truth()
    command = "make button 2 and button 3 the same color as button 1"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        return False


    return True

def main():
    print("running main in simple_LLM_call_tests.py")
    # create a tool box
    mock_gui = Mock_GUI()
    tool_box = load_tools(mock_gui)
    singe_step_call_tester = TU.Singe_Step_Call_Tester(MODEL, tool_box)

    # instructions = """You control a simple application that allows users to set button colors. """
    # # addendum = """If you don't have all the information you need to change anything just make the
    # # calls to get the information and the result from these calls will be given back to you in
    # # a later invocation."""
    # addendum = """When copying colors between buttons, always wait for the retrieved
    # color before proceeding. Only call the tool to set the color after the retrieved
    # data is provided."""
    # instructions += addendum


    # prompt from chat gpt failed
    # instructions = """"You control a simple application that allows users to get and set
    # button colors.
    # For commands that involve copying a color from one button to another,
    # this is a two-step process:
    # First, retrieve the color from the specified button.
    # Then, after receiving further input or confirmation,
    # set the retrieved color on the target button.
    # For the command 'copy the color from button 1 to button 0,'
    # you should first call the tool to get the color of button 1,
    # wait for confirmation, and then call the tool again to set that color to button 0."""

    # prompt from Gemini
    # this works on the color copying test
    instructions = """You are a helpful assistant for a simple application that allows users 
    to set button colors. 
    When given a task, break it down into a series of steps. 
    If a step requires information that is not immediately available, ask for it explicitly. 
    For example, if asked to 'copy the color from button 1 to button 0', 
    first ask for the color of button 1, then proceed to set the color of button 0."""
    instructions += " There are a total of 3 buttons with indexes starting at 0."
    instructions += " Sometimes the user may ask a question that has nothing to with controlling an application. If you know the answer just answer it."
    singe_step_call_tester.set_instructions(instructions)

    # command = "make button 1 blue"
    # singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 1, "color_name": "blue"})
    # r1 = singe_step_call_tester.test(command)
    r1 = simple_tests(singe_step_call_tester)
    print("r1", r1)
# run the main function
if __name__ == "__main__":
    main()