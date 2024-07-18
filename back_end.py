# This class contains the business logic of the application,  it will also be used to track the application State history
from langchain.agents import tool
class Back_End:
    def __init__(self, number_of_buttons=3):
        #self.color = ["white", "white", "white"] # note we have something for button 0, but we don't have a button 0
        self.color = ["white"] * (number_of_buttons)

    def get_button_color(self, button_index):
        return self.color[button_index]

    def set_button_color(self, button_index, color):
        self.color[button_index] = color
    def get_number_of_buttons(self):
        return len(self.color)

    def get_all_colors_as_string(self):
        return " ".join(self.color)

# bug when this is used it does not work correctly
    # def get_tools(self):
    #     tools = []
    #
    #     @tool
    #     def set_button_color(button_index: int, new_color: str) -> None:
    #         """Set the background color of a button."""
    #         self.set_button_color(button_index, new_color)
    #
    #     tools.append(set_button_color)
    #     return tools