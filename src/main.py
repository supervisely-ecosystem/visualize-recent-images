import supervisely as sly
from supervisely.app.widgets import Container

import src.globals as g
import src.ui.input as input

layout = Container(widgets=[input.card])

# * If the app uses static dir, it should be passed as a parameter.
# * If not needed the app can be initialized without static_dir parameter.
# * app = sly.Application(layout=layout)
app = sly.Application(layout=layout, static_dir=g.STATIC_DIR)
