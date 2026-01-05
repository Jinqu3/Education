import logging

from PIL import Image
import asyncio
import os

from src.database import async_session_maker
from src.utils.db_manager import DBManager
from src.tasks.celery_app import celery_instance


@celery_instance.task
def resize_image(image_path: str):
    logging.debug(f"Вызывается функция resize_image: с image_path {image_path}")
    sizes = [10000, 500, 200]
    output_folder = "static/images"
    image_path = f"{image_path}"

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Исходный файл не найден: {image_path}")

    # Открываем изображение
    img = Image.open(image_path)

    # Получаем имя файла и его расширение
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    # Проходим по каждому размеру
    for size in sizes:
        # Сжимаем изображение
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )

        # Формируем имя нового файла
        new_file_name = f"{name}_{size}px{ext}"

        # Полный путь для сохранения
        output_path = os.path.join(output_folder, new_file_name)

        # Сохраняем изображение
        img_resized.save(output_path)

    logging.info(f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}")


async def get_bookings_with_today_check_in_helper():
    async with DBManager(session_factory=async_session_maker) as db:
        bookings = await db.bookings.get_bookings_with_today_check_in()
        loggin.debug(f"{bookings}=")


@celery_instance.task(name="booking_today_check_in")
def send_emails_to_users_with_today_check_in():
    asyncio.run(get_bookings_with_today_check_in_helper())
