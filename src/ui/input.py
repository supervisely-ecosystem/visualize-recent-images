import supervisely as sly
from collections import defaultdict
from supervisely.app.widgets import (
    Card,
    Container,
)

import src.globals as g
from datetime import datetime

from supervisely.app.widgets import GridGallery

grid = GridGallery(
    g.col_num,
)


def get_latest_imgs(imginfos):
    return sorted(
        imginfos,
        key=lambda img_info: datetime.fromisoformat(img_info.updated_at[:-1]),
        reverse=True,
    )[: g.col_num]


def ann_is_empty(ann_info: sly.api.annotation_api.AnnotationInfo) -> bool:
    annotation = ann_info.annotation
    if not annotation.get("objects"):
        return False
    else:
        return True


@sly.timeit
def get_image_infos():
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
    return img_infos


@sly.timeit
def update_grid():
    img_infos = get_image_infos()

    ds_imgids_dict = defaultdict(list)
    for img_info in img_infos:
        ds_imgids_dict[img_info.dataset_id].append(img_info.id)

    ann_jsons = []
    for ds_id, img_ids in ds_imgids_dict.items():
        ann_jsons.extend(g.api.annotation.download_batch(ds_id, img_ids))

    need_project_meta = any([ann_is_empty(ann) for ann in ann_jsons])
    sly.logger.debug(f"need_project_meta:{need_project_meta}")
    if need_project_meta:
        project_meta = sly.ProjectMeta.from_json(g.api.project.get_meta(g.selected_project))
        anns = [
            sly.Annotation.from_json(ann_json.annotation, project_meta) for ann_json in ann_jsons
        ]
    else:
        anns = [None] * len(img_ids)

    grid.clean_up()
    for info, ann in zip(img_infos, anns):
        grid.append(
            title=info.name,
            image_url=info.preview_url,
            annotation=ann,
        )


card = Card(
    "Recently updated images",
    "The most recently updated images",
    content=Container(
        widgets=[
            grid,
        ]
    ),
)
