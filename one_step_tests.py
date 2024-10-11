from simple_LLM_call_tests import MODEL
from cross_platform_tool_box import Tool_Box
import test_utills as TU
from agent_10_9_2024 import load_tools
# import library for seeing how long the tests take
import time

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

count_mode = True # is this is true then tests should return a count of tests run and passed

def simple_tests(singe_step_call_tester, count_mode=count_mode):
    singe_step_call_tester.reset_ground_truth()
    tests_run = 0
    tests_failed = 0

    command = "make button 1 blue"
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 1, "color_name": "blue"})
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
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 2, "color_name": "green"})
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 0, "color_name": "green"})
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
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 1, "color_name": "blue"})
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
    r2 = singe_step_call_tester.test(command, [1,0])
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
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 2, "color_name": "green"})
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 3, "color_name": "green"})
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

    #this is not working
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
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 0, "color_name": "green"})
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 1, "color_name": "green"})
    singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 2, "color_name": "green"})
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

def main():
    print("running main in simple_LLM_call_tests.py")
    # create a tool box
    mock_gui = Mock_GUI()
    tool_box = load_tools(mock_gui, MODEL)

    singe_step_call_tester = TU.Singe_Step_Call_Tester(tool_box, MODEL)

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
    # this works on the color copying test but not all the time if there are gestures involved
    # instructions = """You are a helpful assistant for a simple application that allows users
    # to set button colors.
    # You are working in a multimodal environment in which the user can make speech commands or make speech commands in
    # concert with gesture input. The gesture input will be described after the verbal portion
    # of the command. You should use this information to interpret pronouns and potentially
    # ambiguously described entities.
    # When given a task, break it down into a series of steps.
    # If a step requires information that is not immediately available, ask for it explicitly.
    # For example, if asked to 'copy the color from button 1 to button 0',
    # first ask for the color of button 1, then proceed to set the color of button 0.
    # """

    # prompt from Gemini with modifcations from chat GPT
    # this works on the color copying test but not all the time if there are gestures involved
    # instructions = """You are a helpful assistant for a simple application that allows users
    # to set button colors.
    #
    # You are working in a multimodal environment in which the user can
    # issue speech commands or combine speech with gesture input. The gesture input will be
    # described after the verbal portion of the command. Use this information to interpret
    # pronouns and resolve any ambiguity in descriptions of entities.
    #
    # When given a task, break it down into a series of steps, ensuring that you complete each
    # step fully before moving to the next.
    #
    # Important: If a step requires querying information from the environment
    # (e.g., 'What is the color of button 1?'), make only one tool call and wait for further
    # input after the tool call returns its result. Do not proceed to the next step until you
    # receive additional instructions or new data from the environment.
    #
    # You can't assume that any button is any particular color at any given time as these may change between
    # user commands as the user may change them directly.
    #
    # For example, if asked to 'copy the color from button 1 to button 0', first ask for the
    # color of button 1 using a tool call. Wait for the response before making another tool
    # call to set the color of button 0."""
    #
    # instructions += 'There are a total of 3 buttons with indexes starting at 0.'
    # instructions += """Sometimes the user may ask a question that has nothing to do with controlling an application.
    #                  If you know the answer just answer it."""

    instructions = """You are a helpful assistant for a simple application that allows users to 
    set button colors. """

    instructions += """ You are working in a multimodal environment where the user can issue speech commands or 
    combine speech with gesture input. The gesture input will be described after the verbal 
    portion of the command. Use this information to interpret pronouns and resolve any 
    ambiguity in the descriptions of entities.
    
    When given a task, break it down into a series of steps, ensuring that you complete 
    each step fully before moving on to the next.
    
    Important: If a step requires querying information from the environment 
    (e.g., "What is the color of button 1?"), make only one tool call and wait for further 
    input after the tool call returns its result. Do not proceed to the next step until you 
    receive additional instructions or new data from the environment.
    
    You cannot assume that any button is a specific color at any given time, as these may 
    change between user commands or when the user modifies them directly.
    
    When the user issues a command, make a plan outlining the information you need to 
    gather, and print those details using the print_thoughts tool. First, create a list of all the 
    button colors you need to retrieve. Then, make the necessary tool calls to get these button 
    colors. If you need to gather information before setting button colors, make the tool calls to 
    get the colors first, and only proceed to set the colors after you have received the results 
    from these initial tool calls. """
    #
    instructions += """If asked to "copy the color from button 1 to button 0," first ask for the
    color of button 1 using a tool call. Wait for the response before making another tool call to
    set the color of button 0."""

    instructions += 'There are a total of 3 buttons with indexes starting at 0. '
    instructions += """Sometimes the user may ask a question that has nothing to do with controlling
    an application. If you know the answer just answer it. """

    # instructions += """If the user wants to use the color of a button to set the color of one or
    # more other buttons you should just call the function to get the color but not try to change
    # the color of the other buttons. """

# this fails to get past the first test it is just too afraid to take any action
#     instructions = """You are a helpful assistant for a simple application that allows users
#         to set button colors.
#
#         You are working in a multimodal environment in which the user can
#         issue speech commands or combine speech with gesture input. The gesture input will be
#         described after the verbal portion of the command. Use this information to interpret
#         pronouns and resolve any ambiguity in descriptions of entities.
#
#         Some tools you receive will cause the application's state to change, while others will simply retrieve information about the application's state.
#
#         You may find yourself in one of the following situations, and you need to take the appropriate action for each:
#
#         The user asks a question for which you have all the information needed.
#         In this case, you should answer the question in plain text without making any tool calls.
#         Example: "What color are ripe apricots?"
#
#         The user asks a question that requires a tool to get the information.
#         In this case, you should make tool calls to retrieve the needed information.
#         The results from the tool calls will be sent back to you in a later invocation.
#         Example: "What color is button one?"
#         For questions like this, you need to call the function to get the color of the button.
#
#         The user issues a command for which you have all the necessary information.
#         In this case, you should execute the command by calling the appropriate function.
#         Example: "Make button two purple."
#
#         The user issues a command, but you do not have all the necessary information.
#         In this case, you need to make function calls to gather the missing information.
#         It is very important not to execute the action yet—just make the calls to retrieve the required information.
#         Later, once the results from the information calls are returned, you can proceed with the action calls.
#
#         """

    instructions += 'There are a total of 3 buttons with indexes starting at 0.'
    # instructions += """Sometimes the user may ask a question that has nothing to do with controlling an application.
    #                      If you know the answer just answer it."""

    singe_step_call_tester.set_instructions(instructions)

    # get the time
    start_time = time.time()

    # command = "make button 1 blue"
    # singe_step_call_tester.add_needed_call("set_button_color", {"button_index": 1, "color_name": "blue"})
    # r1 = singe_step_call_tester.test(command)
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