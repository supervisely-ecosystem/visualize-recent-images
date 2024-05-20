import supervisely as sly
from supervisely.app.widgets import Container

import src.globals as g
import src.ui.input as input

import time
import threading


layout = Container(widgets=[input.card])

# * If the app uses static dir, it should be passed as a parameter.
# * If not needed the app can be initialized without static_dir parameter.
# * app = sly.Application(layout=layout)
app = sly.Application(layout=layout, static_dir=g.STATIC_DIR)


def main():
    while True:
        project_info = g.api.project.get_info_by_id(g.selected_project)
        g.current_time = project_info.updated_at
        if g.last_time == g.current_time:
            g.last_time = g.current_time
            continue
        else:
            sly.logger.info("Project Updated")
            time.sleep(g.delay)
            input.update_grid()
            g.last_time = g.current_time


thread = threading.Thread(target=main, daemon=True)
thread.start()
