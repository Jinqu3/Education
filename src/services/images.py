from fastapi import UploadFile, BackgroundTasks
import shutil

from src.services.base import BaseService
from src.tasks.tasks import resize_image


class ImageService(BaseService):

    def upload_image(
        self,
        file: UploadFile,
        background_tasks: BackgroundTasks
    ):
        path = f"static/images/{file.filename}"
        with open(path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image.delay(path)
        background_tasks.add_task(resize_image, path)