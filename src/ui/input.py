import os
import time

import supervisely as sly
from supervisely.app.widgets import (
    Card,
    Container,
    GridGallery,
)

import src.globals as g
from supervisely._utils import abs_url


# def clean_static_dir():
#     # * Utility function to clean static directory, it can be securely removed if not needed.
#     static_files = os.listdir(g.STATIC_DIR)

#     sly.logger.debug(f"Cleaning static directory. Number of files to delete: {len(static_files)}.")

#     for static_file in static_files:
#         os.remove(os.path.join(g.STATIC_DIR, static_file))


def list_difference(list1, list2):
    set2 = set(list2)
    difference = [item for item in list1 if item not in set2]
    return difference


def update_grid():
    img_infos = g.api.image.get_list(
        g.selected_dataset, sort="updatedAt", sort_order="desc", limit=g.col_num
    )
    img_ids = [img.id for img in img_infos]
    preview_urls = [
        img.preview_url.replace("http://10.62.10.5:32977/", f"{g.api.server_address}/")
        for img in img_infos
    ]
    ann_jsons = [g.api.annotation.download(img_id) for img_id in img_ids]
    anns = [sly.Annotation.from_json(ann_json.annotation, g.project_meta) for ann_json in ann_jsons]
    if len(anns) == 0:
        anns = [None]
    new_img_paths = [os.path.join(g.STATIC_DIR, img.name) for img in img_infos]
    # g.api.image.download_paths(g.selected_dataset, img_ids, new_img_paths)
    g.local_images_paths = new_img_paths

    g.grid.clean_up()
    new_img_paths = [os.path.join("static", os.path.basename(path)) for path in new_img_paths]
    for url, ann in zip(preview_urls, anns):
        g.grid.append(
            # title=sly.fs.get_file_name_with_ext(path),
            image_url=url,
            annotation=ann,
        )


update_grid()
card = Card(
    "Recently updated images",
    "The most recently updated images",
    content=Container(
        widgets=[
            g.grid,
        ]
    ),
)
