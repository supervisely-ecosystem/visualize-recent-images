import supervisely as sly
from supervisely.app.widgets import (
    Card,
    Container,
)

import src.globals as g

import datetime


def get_latest_imgs(imginfos):
    infos_w_dates = [
        (image, datetime.fromisoformat(image.updated_at.replace("Z", "+00:00")))
        for image in imginfos
    ]

    sorted_infos_with_dates = sorted(infos_w_dates, key=lambda x: x[1], reverse=True)
    sorted_infos = [image[0] for image in sorted_infos_with_dates]

    return sorted_infos[: g.col_num]


def update_grid():
    if g.selected_dataset:
        img_infos = g.api.image.get_list(
            g.selected_dataset, sort="updatedAt", sort_order="desc", limit=g.col_num
        )
    else:
        filters = [{"field": "updatedAt", "operator": "gt", "value": g.last_time}]
        img_infos = []
        dataset_list = g.api.dataset.get_list(g.selected_project, filters)
        (
            img_infos.extend(
                g.api.image.get_list(
                    dataset_id=dataset.id, sort="updatedAt", sort_order="desc", limit=g.col_num
                )
            )
            for dataset in dataset_list
        )
        img_infos = get_latest_imgs(img_infos)

    img_ids = [img.id for img in img_infos]
    preview_urls = [
        img.preview_url.replace("http://10.62.10.5:32977/", f"{g.api.server_address}/")
        for img in img_infos
    ]
    image_names = [img.name for img in img_infos]
    ann_jsons = [g.api.annotation.download(img_id) for img_id in img_ids]
    anns = [sly.Annotation.from_json(ann_json.annotation, g.project_meta) for ann_json in ann_jsons]
    if len(anns) == 0:
        anns = [None]
    g.grid.clean_up()
    for url, name, ann in zip(preview_urls, image_names, anns):
        g.grid.append(
            title=name,
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
