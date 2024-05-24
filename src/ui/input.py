import supervisely as sly
from supervisely.app.widgets import (
    Card,
    Container,
)

import src.globals as g
from datetime import datetime
from supervisely._utils import is_production


def get_latest_imgs(imginfos):
    infos_w_dates = [(image, datetime.fromisoformat(image.updated_at[:-1])) for image in imginfos]

    sorted_infos_with_dates = sorted(infos_w_dates, key=lambda x: x[1], reverse=True)
    sorted_infos = [image[0] for image in sorted_infos_with_dates]

    return sorted_infos[: g.col_num]


def update_grid():
    if g.selected_dataset:
        img_infos = g.api.image.get_list(
            g.selected_dataset, sort="updatedAt", sort_order="desc", limit=g.col_num
        )
    else:
        img_infos = []
        dataset_list = g.api.dataset.get_list(g.selected_project)
        for dataset in dataset_list:
            img_infos.extend(
                g.api.image.get_list(
                    dataset_id=dataset.id, sort="updatedAt", sort_order="desc", limit=g.col_num
                )
            )
        img_infos = get_latest_imgs(img_infos)

    img_ids = [img.id for img in img_infos]
    preview_urls = []
    for img in img_infos:
        if is_production() and not g.api.server_address.startswith("http://10.62.10.5:32977/"):
            preview_urls.append(img.path_original)
        else:
            preview_urls.append(
                img.preview_url.replace("http://10.62.10.5:32977/", "https://dev.supervisely.com/")
            )
    image_names = [img.name for img in img_infos]
    ann_jsons = [g.api.annotation.download(img_id) for img_id in img_ids]
    project_meta = sly.ProjectMeta.from_json(g.api.project.get_meta(g.selected_project))
    anns = [sly.Annotation.from_json(ann_json.annotation, project_meta) for ann_json in ann_jsons]
    if len(anns) == 0:
        anns = [None]
    g.grid.clean_up()
    # sly.logger.info("Grid Cleaned")
    for url, name, ann in zip(preview_urls, image_names, anns):
        g.grid.append(
            title=name,
            image_url=url,
            annotation=ann,
        )
    # sly.logger.info("Grid images added")


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
