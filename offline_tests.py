# for running offline tests

import GUI_stub_wrapper as GUI
import agent_1 as Agent
#import agent_2_with_dialogue_memory as Agent



prompt_template = Agent.prompt_template

def fresh_start(prompt_template=prompt_template, model=None, window_name="malkup"):
    gui = GUI.Window("window_name")
    Agent.run_MMUI(gui=gui)
    return gui, Agent

def simple_dectic_test(model = None):
    gui, agent = fresh_start(model)
    gui.click_button(2)
    gui.take_action("set this button to red")
    c = gui.get_button_color(2)
    if not c == "red":
        print("simple_dectic_test failed")
        return False
    print("simple_dectic_test passed")
    return True
def simple_description_test(model = None):
    gui, agent = fresh_start(model)
    gui.take_action("make button two red")
    c = gui.get_button_color(2)
    if not c == "red":
        print("simple_description_test failed")
        return False
    print("simple_description_test passed")
    return True
def memory_of_action(model = None):
    gui, agent = fresh_start(model)
    gui.take_action("make button two red")
    c2 = gui.get_button_color(2)
    if not c2 == "red":
        print("memory_of_action failed in step 1")
        return False
    c1 = gui.get_button_color(1)
    if not c1 == "white":
        print("memory_of_action failed in step 1.1")
        return False

    gui.take_action("make it green")
    c2 = gui.get_button_color(2)
    if not c2 == "green":
        print("memory_of_action failed in step 2")
        return False
    c1 = gui.get_button_color(1)
    if not c1 == "white":
        print("memory_of_action failed in step 2.1")
        return False

    print("memory_of_action passed")
    return True

def main():
    simple_description_test()
    simple_dectic_test()
    memory_of_action()


if __name__ == "__main__":
    main()