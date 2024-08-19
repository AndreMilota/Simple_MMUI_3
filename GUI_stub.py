# # this is an offline test class for the simple GUI
# # it should have all the functions that the agents uses
# class Window():
#     def __init__(self, title):
#         self.button_colors = ['white', 'white', 'white']
#         self.run_callback_function = None
#
#     def set_button_color(self, button_index, color):
#         self.todo.append(lambda: self.button_colors[button_index] (background=color))
#
#     def set_run_callback(self, run_callback_function):
#         self.run_callback_function = run_callback_function
#
#     def run(self):
#         None
#
#     # def button1_clicked(self):
#     #     self.gestures += "button 1 was indicated"
#     #
#     # def button2_clicked(self):
#     #     self.gestures += "button 2 was indicated"
#
#     def take_action(self, command):
#         self.run_callback_function(command, self.gestures)
#         self.gestures = ""
#         # if self.todo != None:
#         #    self.set_button_color(self.todo[0], self.todo[1])
#         for c in self.todo:
#             c()
#         self.todo = []  # clear the todo list