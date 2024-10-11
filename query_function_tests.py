#Test prompts which should only result in a function being called to get information

from simple_LLM_call_tests import MODEL
from cross_platform_tool_box import Tool_Box
import test_utills as TU
#from agent_10_9_2024 import load_tools
# import library for seeing how long the tests take
import time
from model_manager import identify_model
from cross_platform_tool_box import Tool_Box, Tool
from typing import Tuple

class Mock_GUI():
    def get_button_color(self, button_index):
        print("get_button_color", button_index)
        return "red"

    def get_number_of_buttons(self):
        print("get_number_of_buttons")
        return 3

    # def set_button_color(self, button_index, color_name):
    #     print("set_button_color", button_index, color_name)
    #     pass


count_mode = True  # is this is true then tests should return a count of tests run and passed

def simple_tests(singe_step_call_tester, count_mode=count_mode):
    singe_step_call_tester.reset_ground_truth()
    tests_run = 0
    tests_failed = 0

    command = "make button 1 blue"
    r1 = singe_step_call_tester.test(command)
    if not r1:
        print("simple_tests: failed 'make button 1 blue'")
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # test 2
    singe_step_call_tester.reset_ground_truth()
    command = "what is the color of button 1"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed: " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # test 3
    singe_step_call_tester.reset_ground_truth()
    command = "copy the color from button 1 to button 0"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # test 4
    singe_step_call_tester.reset_ground_truth()
    command = "copy the color from button 1 to button 2"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # test 5
    singe_step_call_tester.reset_ground_truth()
    command = "make button 1 the same color as button 2"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 2})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1
    # test 6

    singe_step_call_tester.reset_ground_truth()
    command = "make button 2 and button 0 green"
    singe_step_call_tester.add_bad_call("set_button_color", {"button_index": 2, "color_name": "green"})
    singe_step_call_tester.add_bad_call("set_button_color", {"button_index": 0, "color_name": "green"})
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    singe_step_call_tester.reset_ground_truth()
    command = "What color is the sky during the day"
    singe_step_call_tester.add_non_call_condition("'Blue' is in the text")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    singe_step_call_tester.reset_ground_truth()
    command = "make button 2 and button 3 the same color as button 1"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command)
    if not r2:
        print("simple_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    if count_mode:
        return tests_run, tests_run - tests_failed
    else:
        return True


def deictic_tests(singe_step_call_tester, count_mode=count_mode):
    tests_run = 0
    tests_failed = 0

    singe_step_call_tester.reset_ground_truth()
    command = "make this blue"
    r1 = singe_step_call_tester.test(command, [1])
    if not r1:
        print("deictic_tests: failed: " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # test 2
    singe_step_call_tester.reset_ground_truth()
    command = "what is the color is this"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    r2 = singe_step_call_tester.test(command, [1])
    if not r2:
        print("deictic_tests: failed: " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # test 2.5
    singe_step_call_tester.reset_ground_truth()
    command = "copy the color from button 1 to this button"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command, [2])
    if not r2:
        print("deictic_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # test 3
    singe_step_call_tester.reset_ground_truth()
    command = "copy the color from here to here"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command, [1, 0])
    if not r2:
        print("deictic_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # test 4
    singe_step_call_tester.reset_ground_truth()
    command = "copy the color from this button to this one 2"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command, [1, 2])
    if not r2:
        print("deictic_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # test 5
    singe_step_call_tester.reset_ground_truth()
    command = "make this the same color as this button"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 2})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command, [1, 2])
    if not r2:
        print("deictic_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1
    # test 6

    singe_step_call_tester.reset_ground_truth()
    command = "make this button and this one green"
    singe_step_call_tester.add_bad_call("set_button_color", {"button_index": 2, "color_name": "green"})
    singe_step_call_tester.add_bad_call("set_button_color", {"button_index": 3, "color_name": "green"})
    r2 = singe_step_call_tester.test(command, [2, 3])
    if not r2:
        print("deictic_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    singe_step_call_tester.reset_ground_truth()
    command = "make this and button 3 the same color as this button"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 1})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command, [2, 1])
    if not r2:
        print("deictic_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    # this is not working
    singe_step_call_tester.reset_ground_truth()
    command = "make these 2 buttons the same color as this button"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 0})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command, [2, 1, 0])
    if not r2:
        print("deictic_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    singe_step_call_tester.reset_ground_truth()
    command = "make these 3 buttons green"
    singe_step_call_tester.add_bad_call("set_button_color", {"button_index": 0, "color_name": "green"})
    singe_step_call_tester.add_bad_call("set_button_color", {"button_index": 1, "color_name": "green"})
    singe_step_call_tester.add_bad_call("set_button_color", {"button_index": 2, "color_name": "green"})
    r2 = singe_step_call_tester.test(command, [2, 1, 0])
    if not r2:
        print("deictic_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    singe_step_call_tester.reset_ground_truth()
    command = "make these 2 buttons the same color as button 0"
    singe_step_call_tester.add_needed_call("get_button_color", {"button_index": 0})
    singe_step_call_tester.add_bad_call("set_button_color")
    r2 = singe_step_call_tester.test(command, [2, 1])
    if not r2:
        print("deictic_tests: failed " + command)
        if count_mode:
            tests_failed += 1
        else:
            return False
    tests_run += 1

    if count_mode:
        return tests_run, tests_run - tests_failed
    else:
        return True

def load_tools(gui, model) -> Tool_Box:
    out = Tool_Box()

    service = identify_model(model)
    index_parameter = {"parameter_or_name": "button_index",
                      "description": "The index of the button to change. Buttons are numbered starting from 0 up to n - 1.",
                      "type": "integer"}

    # add the tools here

    # add the get_button_color tool

    def get_button_color(button_index: int) -> Tuple[str, bool]:
        """Get the background color of a button."""
        out = gui.get_button_color(button_index)
        return out, True

    tool = Tool(get_button_color,
                name = "get_button_color",
                description = "Get the background color of a button.")
    tool.add_required_parameter(**index_parameter)
    out.add_tool(tool)

    return out;


def main():
    print("running main in simple_LLM_call_tests.py")
    # create a tool box
    mock_gui = Mock_GUI()
    tool_box = load_tools(mock_gui, MODEL)

    singe_step_call_tester = TU.Singe_Step_Call_Tester(tool_box, MODEL)

    instructions = """"Here is a cleaned-up version of the prompt with punctuation and speech recognition errors corrected:
    You are doing the first phase of processing for a multimodal user interface. You will be given the text of what the 
    user said and a description of the objects they indicated using gestures. First, combine these using the gesture descriptions 
    to resolve pronouns and ambiguous references in the text.
    Then, you will have to handle one of three situations as follows:
    1.	The user asks a question for which you already have the information to answer. In this case, print the answer. For example, 
    the user might ask: "What color are carrots typically?" You should respond: "Orange."
    2.	The user gives a command. In this case, you should return nothing. For example, the user might say: "Make this blue," and point 
    to button number one. In this case, don't do anything.
    3.	The user asks a question or gives a command that requires you to get information about the state of the system. For example, 
    the user might say: "Make button one and two the same color as button zero." In this case, you need to call the function to get 
    the color of button zero."""

    instructions += 'There are a total of 3 buttons with indexes starting at 0. '



    singe_step_call_tester.set_instructions(instructions)

    # get the time
    start_time = time.time()

    r1 = simple_tests(singe_step_call_tester)
    r2 = deictic_tests(singe_step_call_tester)

    # get the time
    end_time = time.time()

    print("simple_tests: ", r1)
    print("deictic_tests: ", r2)
    total = r1[0] + r2[0]
    passed = r1[1] + r2[1]
    print("results: ", passed, " out of ", total)
    print("time: ", end_time - start_time)


# run the main function
if __name__ == "__main__":
    main()