# this version of the offline tests takes the agent as an argument, so you can run offline tests from the agent file
# older versions of the agent may not have all the functions this file needs

def simple_dectic_test(agent):
    gui = agent.get_gui()
    gui.click_button(2)
    gui.take_action("set this button to red")
    c = gui.get_button_color(2)
    if not c == "red":
        print("simple_dectic_test failed")
        return False
    print("simple_dectic_test passed")
    return True

def simple_description_test(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red")
    c = gui.get_button_color(2)
    if not c == "red":
        print("simple_description_test failed")
        return False
    print("simple_description_test passed")
    return True
def memory_of_action(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red") # we are not using a gesture in this test
    c2 = gui.get_button_color(2)
    if not c2 == "red":
        print("memory_of_action failed in step 1. b2 was", c2, "when it should have been", "red")
        return False
    c1 = gui.get_button_color(1)
    if not c1 == "white":
        print("memory_of_action failed in step 1.1. b1 was", c1, "when it should have been", "white")
        return False

    gui.take_action("make it green") # inorder to resolve "it" it needs to see what action it tool last
    c2 = gui.get_button_color(2)
    c1 = gui.get_button_color(1)
    if not c2 == "green":
        print("memory_of_action failed in step 2. b2 was", c2, "when it should have been", "green")
        print("b1 is ", c1)
        return False
    if not c1 == "white":
        print("memory_of_action failed in step 2.1 b1 was", c1, "when it should have been", "white")
        return False

    print("memory_of_action passed")
    return True

def read_button_color(agent):
    gui = agent.get_gui()
    gui.take_action("what is the color of button 2")

def simple_question_test(agent):
    gui = agent.get_gui()
    gui.take_action("What color is the sky")

def run_offline_tests(agent):
    agent.reset()
    simple_description_test(agent)
    agent.reset()
    simple_dectic_test(agent)
    agent.reset()
    memory_of_action(agent)
    agent.reset()
    simple_question_test(agent)