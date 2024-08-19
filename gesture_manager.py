
class Gesture_Manager:
    def __init__(self):
        self.description = None

    def button_clicked(self, button_index):
        if self.description is not None:
            self.description += f" Then button {button_index} was indicated."
        else:
            self.description = f"Button {button_index} was indicated."

    def get_description(self):
        return self.description

    def reset(self):
        self.description = None

