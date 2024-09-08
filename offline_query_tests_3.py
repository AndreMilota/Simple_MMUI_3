# this version of the offline tests takes the agent as an argument, so you can run offline tests from the agent file
# older versions of the agent may not have all the functions this file needs

import test_utills


def deictic_query_test(agent):
    gui = agent.get_gui()
    gui.click_button(2)
    r = gui.take_action("what color is this")  # users input
    r2 = test_utills.llm_based_assertion("it should be white", r)
    return r2

def deictic_query_test_2(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red")
    c = gui.get_button_color(2)
    if not c == "red":
        print("deictic_query_test_2 failed")
        return False
    gui.click_button(2)
    r = gui.take_action("what color is this")  # users input
    r2 = test_utills.llm_based_assertion("it should be red", r)
    return r2

def read_button_color(agent):
    gui = agent.get_gui()
    r = gui.take_action("what is the color of button 2")
    r2 = test_utills.llm_based_assertion("it should be white", r)
    return r2

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
        print("deictic_copy_color_1 failed")
        return False

    gui.take_action("make button one blue")
    c1 = gui.get_button_color(1)
    if not c1 == "blue":                 # 1 is blue
        print("deictic_copy_color_1 failed")
        return False

    gui.click_button(2)
    gui.take_action("make this the same color as button one") # 2 is blue now

    c1 = gui.get_button_color(1)
    c2 = gui.get_button_color(2)
    if not c1 == c2:
        print("deictic_copy_color_1 failed")
        return False
    if not c1 == "blue":
        print("deictic_copy_color_1 failed")
        return False
    print("deictic_copy_color_1 passed")
    return True

def double_deictic_copy_color_1(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red") # 2 is red
    c2 = gui.get_button_color(2)
    if not c2 == "red":
        print("double_deictic_copy_color_1 failed")
        return False

    gui.take_action("make button one blue") # 1 is blue
    c1 = gui.get_button_color(1)
    if not c1 == "blue":
        print("double_deictic_copy_color_1 failed")
        return False

    gui.click_button(2)
    gui.click_button(1)
    gui.take_action("make this the same color as that") # 1 is red now

    c_b1_2 = gui.get_button_color(1)
    c_b2_2 = gui.get_button_color(2)
    if not c_b1_2 == c_b2_2:
        print("double_deictic_copy_color_1 failed")
        return False
    if not c_b2_2 == "blue":
        print("double_deictic_copy_color_1 failed")
        return False
    print("double_deictic_copy_color_1 passed")
    return True

def double_deictic_copy_color_2(agent):
    gui = agent.get_gui()
    gui.take_action("make button two red") # 2 is red
    c1 = gui.get_button_color(2)
    if not c1 == "red":
        print("double_deictic_copy_color_2 failed")
        return False

    gui.take_action("make button one blue") # 1 is blue
    c1 = gui.get_button_color(2)
    if not c1 == "blue":
        print("double_deictic_copy_color_2 failed")
        return False

    gui.click_button(1)
    gui.click_button(2)
    gui.take_action("copy the color from here to here") # 2 is now blue

    c1 = gui.get_button_color(1)
    c2 = gui.get_button_color(2)
    if not c1 == c2:
        print("double_deictic_copy_color_2 failed")
        return False
    if not c1 == "blue":
        print("double_deictic_copy_color_2 failed")
        return False
    print("double_deictic_copy_color_2 passed")
    return True

def run_offline_tests(agent):
    # for i in range(6):
    #     agent.reset()
    #     r = deictic_query_test(agent)
    #     if not r:
    #         print("deictic_query_test failed")
    #         return False
    #
    #     agent.reset()
    #     r = deictic_query_test_2(agent)
    #     if not r:
    #         print("deictic_query_test_2 failed")
    #         return False
    #
    #     agent.reset()
    #     r = read_button_color(agent)
    #     if not r:
    #         print("read_button_color failed")
    #         return False
    #
    #     agent.reset()
    #     r = copy_color(agent)
    #     if not r:
    #         print("copy_color failed")
    #         return False

    agent.reset()
    r = deictic_copy_color_1(agent)
    if not r:
        return False

    agent.reset()
    r = double_deictic_copy_color_1(agent)
    if not r:
        return False

    agent.reset()
    r = double_deictic_copy_color_2(agent)
    if not r:
        return False

    agent.reset()

    print("all tests passed")
