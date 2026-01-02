from fastapi import APIRouter, UploadFile,BackgroundTasks
import shutil

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images",tags=["Изображения"])

@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    path = f"static/images/{file.filename}"
    with open(path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)

    #resize_image.delay(path)
    background_tasks.add_task(resize_image,path)
