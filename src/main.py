import supervisely as sly
from supervisely.app.widgets import Container

import src.globals as g
import src.ui.input as input

import time
import threading


layout = Container(widgets=[input.card])
app = sly.Application(layout=layout)

last_time = None


def main():
    global last_time
    while True:
        project_info = g.api.project.get_info_by_id(g.selected_project)
        if last_time != project_info.updated_at:
            sly.logger.info("Updating Grid")
            input.update_grid()
            last_time = project_info.updated_at
        time.sleep(g.delay)


thread = threading.Thread(target=main, daemon=True)
thread.start()
