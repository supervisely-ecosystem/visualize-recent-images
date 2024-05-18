import os

import supervisely as sly
from dotenv import load_dotenv

if sly.is_development():
    # * For convinient development, has no effect in the production.
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


# * Creating an instance of the supervisely API according to the environment variables.
api = sly.Api.from_env()


# * This variable requires SLY_APP_DATA_DIR in local.env file.
SLY_APP_DATA_DIR = sly.app.get_data_dir()


# * If the app needed static dir (showing local path in web UI), it should be created here.
# * If not needed, this code can be securely removed.
STATIC_DIR = os.path.join(SLY_APP_DATA_DIR, "static")
sly.fs.mkdir(STATIC_DIR)


class ModalState:
    """Modal state"""

    UPDATE_DELAY = "modal.state.UpdateDelay"
    GRID_WIDTH = "modal.state.GridWidth"
    # GRID_HEIGHT = "modal.state.GridHeight"

    def delay(self):
        return os.environ.get(self.UPDATE_DELAY, 2)

    def grid_size(self):
        return os.environ.get(self.GRID_WIDTH, 1)


# * To avoid global variables in different modules, it's better to use g.STATE (g.AppState) object
# * across the app. It can be accessed from any module by importing globals module.
class State:
    def __init__(self):
        # * This class should contain all the variables that are used across the app.
        # * For example selected team, workspace, project, dataset, etc.
        self.selected_team = sly.env.team_id()
        self.selected_workspace = sly.env.workspace_id()
        self.selected_project = sly.env.project_id(raise_not_found=False)
        self.selected_dataset = sly.env.dataset_id(raise_not_found=False)

        self.delay = ModalState().delay()
        self.col_num = ModalState().grid_size()
        self.displaying_imgs_paths = None

        self.continue_working = True


# * Class object to access from other modules.
# * import src.globals as g
# * selected_team = g.STATE.selected_team
STATE = State()
