import taipy.gui.builder as tgb
from taipy import Gui

def say_hello(state):
    print("Hello, world!")

with tgb.Page() as page:
    tgb.button("Hello", on_action=say_hello)

gui = Gui(page)
gui.run()

