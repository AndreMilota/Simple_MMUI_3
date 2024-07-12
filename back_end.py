# This class contains the business logic of the application,  it will also be used to track the application State history

class Back_End:
    def __init__(self):
        self.color = ["white", "white", "white"] # note we have something for button 0, but we don't have a button 0

    def get_button_color(self, button_index):
        return self.color[button_index]

    def set_button_color(self, button_index, color):
        self.color[button_index] = color