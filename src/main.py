import supervisely as sly
from supervisely.app.widgets import Container

import src.globals as g
import src.ui.input as input

import time
import threading


layout = Container(widgets=[input.card])
app = sly.Application(layout=layout)


def main():
    while True:
        project_info = g.api.project.get_info_by_id(g.selected_project)
        g.current_time = project_info.updated_at
        if g.last_time != g.current_time:
            sly.logger.info("Project Updated")
            input.update_grid()
            g.last_time = g.current_time
        time.sleep(g.delay)


thread = threading.Thread(target=main, daemon=True)
thread.start()
