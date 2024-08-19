# this version of the offline tests takes the agent as an argument, so you can run offline tests from the agent file
# older versions of the agent may not have all the functions this file needs

def deictic_query_test(agent):
    gui = agent.get_gui()
    gui.click_button(2)
    gui.take_action("what color is this")  # users input
    print("IT SHOULD BE WHITE")
    return True

def deictic_query_test_2(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red")
    c = gui.get_button_color(2)
    if not c == "red":
        print("simple_description_test failed")
        return False
    gui.click_button(2)
    gui.take_action("what color is this")  # users input
    print("IT SHOULD BE RED")
    return True

def read_button_color(agent):
    gui = agent.get_gui()
    gui.take_action("what is the color of button 2")
    print("IT SHOULD BE WHITE")
    return True
def copy_color(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red")
    c = gui.get_button_color(2)
    if not c == "red":
        print("copy_color failed")
        return False

    gui.take_action("make button one the same color as button two")
    c1 = gui.get_button_color(1)
    c2 = gui.get_button_color(2)
    if not c1 == c2:
        print("copy_color failed")
        return False
    if not c1 == "red":
        print("copy_color failed")
        return False
    print("copy_color passed")
    return True

def deictic_copy_color_1(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red")
    c1 = gui.get_button_color(2)
    if not c1 == "red":                   # 2 is red
        print("copy_color failed")
        return False

    gui.take_action("make button one blue")
    c1 = gui.get_button_color(1)
    if not c1 == "blue":                 # 1 is blue
        print("copy_color failed")
        return False

    gui.click_button(2)
    gui.take_action("make this the same color as button one") # 2 is blue now

    c1 = gui.get_button_color(1)
    c2 = gui.get_button_color(2)
    if not c1 == c2:
        print("copy_color failed")
        return False
    if not c1 == "blue":
        print("copy_color failed")
        return False
    print("deictic_copy_color_1 passed")
    return True

def double_deictic_copy_color_1(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red") # 2 is red
    c1 = gui.get_button_color(2)
    if not c1 == "red":
        print("copy_color failed")
        return False

    gui.take_action("make button one blue") # 1 is blue
    c1 = gui.get_button_color(1)
    if not c1 == "blue":
        print("copy_color failed")
        return False

    gui.click_button(1)
    gui.click_button(2)
    gui.take_action("make this the same color as that") # 1 is red now

    c1 = gui.get_button_color(1)
    c2 = gui.get_button_color(2)
    if not c1 == c2:
        print("copy_color failed")
        return False
    if not c1 == "red":
        print("copy_color failed")
        return False
    print("double_deictic_copy_color_1 passed")
    return True

def double_deictic_copy_color_2(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red") # 2 is red
    c1 = gui.get_button_color(2)
    if not c1 == "red":
        print("copy_color failed")
        return False

    gui.take_action("make button one blue") # 1 is blue
    c1 = gui.get_button_color(2)
    if not c1 == "blue":
        print("copy_color failed")
        return False

    gui.click_button(1)
    gui.click_button(2)
    gui.take_action("copy the color from here to here") # 2 is now blue

    c1 = gui.get_button_color(1)
    c2 = gui.get_button_color(2)
    if not c1 == c2:
        print("copy_color failed")
        return False
    if not c1 == "blue":
        print("copy_color failed")
        return False
    print("double_deictic_copy_color_2 passed")
    return True
def run_offline_tests(agent):
    # agent.reset()
    # deictic_query_test(agent)
    #
    # agent.reset()
    # deictic_query_test_2(agent)
    #
    # agent.reset()
    # read_button_color(agent)

    # agent.reset()
    #copy_color(agent)

    # agent.reset()
    # deictic_copy_color_1(agent)

    agent.reset()
    double_deictic_copy_color_1(agent)

    agent.reset()
    double_deictic_copy_color_2(agent)

    agent.reset()
