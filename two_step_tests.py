# this is used to test the two_step_core.py\

from two_step_core import Two_Stage_LLM_Processor
from cross_platform_tool_box import Tool_Box, Tool, Parameter
from primary_prompt_assembler import Primary_Prompt_Assembler
from secondary_prompt_assembler import Secondary_Prompt_Assembler
from two_step_core import Two_Stage_LLM_Processor
from gesture_manager import Gesture_Manager
from test_utills import llm_based_assertion

button_colors = ["red", "green", "blue"]
index_parameter = {"parameter_or_name": "button_index",
                   "description": "The index of the button to change. Buttons are numbered starting from 0 up to n - 1.",
                   "type": "integer"}


def get_prompt_assemblers(number_of_buttons = 3) -> (Primary_Prompt_Assembler, Secondary_Prompt_Assembler):
    primary_tool_box = Tool_Box()

    def get_button_color(button_index: int) -> (str, bool):
        print("get_button_color(", button_index, ")")
        color = button_colors[button_index]
        out = f"The color of button {button_index} is {color}. "
        return out, True

    tool = Tool(get_button_color,
                name = "get_button_color",
                description = "Get the background color of a button.")
    tool.add_required_parameter(**index_parameter)
    primary_tool_box.add_tool(tool)
    primary_prompt_assembler = Primary_Prompt_Assembler(primary_tool_box, number_of_buttons)

    # setup the secondary prompt assembler
    secondary_tool_box = Tool_Box()

    def set_button_color(button_index: int, color_name: str) -> (str, bool):
        print("set_button_color(", button_index, ",", color_name, ")")
        button_colors[button_index] = color_name
        out = f"Set button {button_index} to {color_name}"
        return out, False

    color_parameter = {"parameter_or_name": "color_name",
                       "description": "The name of the color to change the button to.",
                       "type": "string"}
    tool = Tool(set_button_color,
                name = "set_button_color",
                description = "Set the background color of a button.")

    tool.add_required_parameter(**index_parameter)
    tool.add_required_parameter(**color_parameter)
    secondary_tool_box.add_tool(tool)

    secondary_prompt_assembler = Secondary_Prompt_Assembler(secondary_tool_box, number_of_buttons)

    return primary_prompt_assembler, secondary_prompt_assembler


def single_step_test_1():
    # load the primary tool boxs
    primary_prompt_assembler = get_prompt_assemblers()[0]

    core = Two_Stage_LLM_Processor([primary_prompt_assembler, primary_prompt_assembler])
    command_1 = "what color is button 2"
    response = core.step(command_1)
    # print the type of response
    print(response)
    pqr1 = core.process_response(response)
    print ("pqr1 = ", pqr1)


def two_step_test_1():
    # load the primary tool boxs
    primary_prompt_assembler, secondary_prompt_assembler = get_prompt_assemblers()

    core = Two_Stage_LLM_Processor([primary_prompt_assembler, secondary_prompt_assembler])
    command_1 = "what color is button 2"
    response = core.step(command_1)
    # print the type of response
    print(response)
    pqr1 = core.process_response(response)
    print("pqr1 = ", pqr1)

    if pqr1[1]:
        print("We need to do another step")
        response_2 = core.step(command_1, response=pqr1[0], index=1)
        print(response_2)
        pqr2 = core.process_response(response_2, index=1)
        print("pqr2 = ", pqr2)


def test_step(Initial_colors :list, buttons_selected :list, command :str,
              resulting_colors :list = None, response_characterization :str = None) -> bool:
    # set the global variable button_colors
    global button_colors
    button_colors = Initial_colors
    number_of_buttons = len(button_colors)
    primary_prompt_assembler, secondary_prompt_assembler = get_prompt_assemblers(number_of_buttons)
    core = Two_Stage_LLM_Processor([primary_prompt_assembler, secondary_prompt_assembler])

    gesture_manager = Gesture_Manager()
    for button in buttons_selected:
        gesture_manager.button_clicked(button)

    r = core.process_command(command, gesture_manager)

    if resulting_colors:
        # convert the color lists to a string
        error_message = f". Expected the colors to be {resulting_colors} but they were {button_colors}"
        return button_colors == resulting_colors, error_message

    assert(response_characterization)
    error_message = f". Expected the response to be {response_characterization} but it was {r}"
    return llm_based_assertion(response_characterization, r, ), error_message


def get_SUI_test_sets():
    out = []
    out.append((["red", "green", "blue"], [], "what color is button 0",
                None, "It should say something about red."))

    out.append((["red", "green", "blue"], [], "make button 1 blue",
                ["red", "blue", "blue"], None))

    out.append((["red", "green", "blue"], [], "copy the color from button 1 to button 0",
                ["green", "green", "blue"], None))

    out.append((["red", "green", "blue"], [], "copy the color from button 0 to button 1",
                ["red", "red", "blue"], None))

    out.append((["red", "green", "blue"], [], "copy the color from button 1 to button 2",
                ["red", "green", "green"], None))

    out.append((["red", "green", "blue"], [], "copy the color from button 2 to button 1",
                ["red", "blue", "blue"], None))


    out.append((["red", "green", "blue"], [], "make button 0 the same color as button 2",
                ["blue", "green", "blue"], None))

    out.append((["red", "green", "blue"], [], "make the second button the same color as the first",
                ["red", "red", "blue"], None))

    out.append((["red", "green", "blue"], [], "make the second button the same color as button 0",
                ["red", "red", "blue"], None))

    out.append((["red", "green", "blue"], [], "make button 1 the same color as button 0",
                ["red", "red", "blue"], None))

    out.append((["red", "green", "blue"], [],
                "make the button with index 1 the same color as button 2",
                ["red", "blue", "blue"], None))

    out.append((["red", "green", "blue"], [],
                "make button 2 the same color as button 0",
                ["red", "green", "red"], None))

    out.append((["red", "green", "blue"], [],
                "make button 2 the same color as button 1",
                ["red", "green", "green"], None))

    out.append((["red", "green", "blue"], [],
                "make button one the same color as button 2",
                ["red", "blue", "blue"], None))

    out.append((["red", "green", "blue"], [],
                "make button number one the same color as button 2",
                ["red", "blue", "blue"], None))

    out.append((["red", "green", "blue"], [],
                "make button number 1 the same color as button 2",
                ["red", "blue", "blue"], None))

    out.append((["red", "green", "blue"], [],
                "make button 1 the same color as button 2",
                ["red", "blue", "blue"], None))

    out.append((["red", "green", "blue"], [],
                "make the thrid button the same color as button 1",
                ["red", "green", "green"], None))

    out.append((["red", "green", "blue"], [],
                "make the button numbered 2 the same color as button 1",
                ["red", "green", "green"], None))

    out.append((["red", "green", "blue"], [],
                "make button two the same color as button 1",
                ["red", "green", "green"], None))

    out.append((["red", "green", "blue"], [], "what color is button 1",
                None, "It should say something about green."))

    out.append((["red", "green", "blue"], [], "what color is button 2",
                None, "It should say something about blue."))

    out.append((["red", "green", "blue"], [], "make button 2 black",
                ["red", "green", "black"], None))

    out.append((["red", "green", "blue", "black"], [], "make button 2 black",
                ["red", "green", "black", "black"], None))

    out.append((["red", "green", "blue"], [], "make button 1 black",
                ["red", "black", "blue"], None))

    out.append((["red", "green", "blue"], [], "make button 1 red",
                ["red", "red", "blue"], None))

    out.append((["red", "green", "blue"], [], "make button 0 black",
                ["black", "green", "blue"], None))
    return out


def two_step_test():
    correct = 0
    test_set = get_SUI_test_sets()
    number_of_tests = 0
    for i, test_set in enumerate(test_set):
        r, e = test_step(*test_set)
        if r:
            correct += 1
            print(i, "Passed:", test_set[2])
        else:
            print(i, "Failed:", test_set[2], e)
        number_of_tests += 1

    print(f"{correct} out of {number_of_tests} passed")


def main():
    two_step_test()

if __name__ == "__main__":
    main()