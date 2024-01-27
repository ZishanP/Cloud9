from taipy import Gui

root_md="""
# Multi-page application
<|content|>

This application was created with [Taipy](https://www.taipy.io/).
"""
page1_md="## This is page 1"
page2_md="## This is page 2"

pages = {
    "/": root_md,
    "page1": page1_md,
    "page2": page2_md
}
Gui(pages=pages).run().debug(True)