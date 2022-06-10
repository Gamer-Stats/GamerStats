# Other imports for the function
import os
from datetime import datetime
from pathlib import Path

from core.models import News, SetupSettings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from gs_wik.settings import MEDIA_URL
from PIL import Image


@receiver(pre_save, sender=SetupSettings)
def get_image_url(sender, instance, **kwargs):
    instance.image_url = instance.avatar.image.url


# News Image = 720*405 || 512*288 || 304*171
# Setup Profile Image = 180*180 || 140*140

# @receiver(pre_save, sender=News)
# def image_handler(sender, instance, **kwargs):
#     year = datetime.today().year
#     month = datetime.today().month
#     day = datetime.today().day

#     new_image = Path(instance.avatar.image.name).with_suffix(".webp")

#     new_image = os.path.basename(new_image)

#     sizes = [
#         (720, 405),
#         (512, 288),
#         (304, 171),
#     ]
#     open_image = Image.open(instance.avatar.image)

#     for size in sizes:
#         open_image.thumbnail(size)

#         os.makedirs("{0}/{1}/{2}/{3}/{4}/{5}".format(
#             "https://cdn.gamerstats.net/media/", "news", year, month, day, size[0]
#         ), exist_ok=True)

#         new_image_path = "{0}/{1}/{2}/{3}/{4}/{5}/{6}".format(
#             "https://cdn.gamerstats.net/media/", "news", year, month, day, size[0], new_image
#         )
#         open_image.save(new_image_path, "WEBP", quality=90)

#         print(new_image_path, size)

    # @receiver(pre_save, sender=Game)
    # @receiver(pre_save, sender=Team)
    # @receiver(pre_save, sender=PcSpecs)
    # @receiver(pre_save, sender=Content_Creator)
    # @receiver(pre_save, sender=Esports_Player)
    # def image_profile(sender, instance, **kwargs):
    #     if (
    #         instance.class_type == "esports"
    #         or instance.class_type == "content_creator"
    #         or instance.class_type == "profile"
    #     ):
    #         if instance.image.name == "profiles/gs-profile.jpg":
    #             print("not doing")
    #             pass
    #         else:
    #             if instance.image_status == "A":
    #                 new_image_webp = Path(instance.image.name).with_suffix(".webp")
    #                 new_image_jpeg = Path(instance.image.name).with_suffix(".jpeg")
    #                 sizes = [
    #                     (400, 400),
    #                     (200, 200),
    #                     (312, 312),
    #                     (156, 156),
    #                 ]
    #                 for i in sizes:
    #                     base_image = Image.open(instance.image)
    #                     base_image.thumbnail(i)
    #                     new_webp_path = "{0}/{1}/{2}/{3}/{4}".format(
    #                         MEDIA_ROOT, "profiles", "webp", i[0], new_image_webp.name
    #                     )
    #                     base_image.save(new_webp_path, "WEBP", quality=90)
    #                     new_jpeg_path = "{0}/{1}/{2}/{3}/{4}".format(
    #                         MEDIA_ROOT, "profiles", "jpeg", i[0], new_image_jpeg.name
    #                     )
    #                     base_image.load()
    #                     try:
    #                         base_image_rgb = Image.new(
    #                             "RGB", base_image.size, (255, 255, 255)
    #                         )
    #                         base_image_rgb.paste(base_image, mask=base_image.split()[3])
    #                         base_image_rgb.save(new_jpeg_path, "JPEG", quality=90)
    #                     except IndexError:
    #                         base_image.save(new_jpeg_path, "JPEG", quality=90)

    #     elif instance.class_type == "game":
    #         if instance.main_image.name != instance.main_image.name:
    #             new_image_webp_main = Path(instance.main_image.name).with_suffix(".webp")
    #             new_image_jpeg_main = Path(instance.main_image.name).with_suffix(".jpeg")

    #             sizes = [
    #                 (416, 554),
    #                 (208, 277),
    #                 (156, 208),
    #                 (312, 416),
    #             ]
    #             for i in sizes:
    #                 base_image_main = Image.open(instance.main_image)
    #                 base_image_main.thumbnail(i)

    #                 os.makedirs(
    #                     "{0}/{1}/{2}/{3}/{4}".format(
    #                         MEDIA_ROOT, "games", "main", "webp", i[0]
    #                     ),
    #                     exist_ok=True,
    #                 )
    #                 os.makedirs(
    #                     "{0}/{1}/{2}/{3}/{4}".format(
    #                         MEDIA_ROOT, "games", "main", "jpeg", i[0]
    #                     ),
    #                     exist_ok=True,
    #                 )

    #                 new_webp_path = "{0}/{1}/{2}/{3}/{4}/{5}".format(
    #                     MEDIA_ROOT, "games", "main", "webp", i[0], new_image_webp_main.name
    #                 )
    #                 base_image_main.save(new_webp_path, "WEBP", quality=90)
    #                 new_jpeg_path = "{0}/{1}/{2}/{3}/{4}/{5}".format(
    #                     MEDIA_ROOT, "games", "main", "jpeg", i[0], new_image_jpeg_main.name
    #                 )
    #                 if base_image_main.format == "PNG" or base_image_main.format == "png":
    #                     base_image_main.save(new_jpeg_path, "JPEG", quality=90)
    #                 else:
    #                     base_image_main.save(new_jpeg_path, "JPEG", quality=90)

    #     elif instance.class_type == "team":
    #         new_image_webp_main = Path(instance.main_image.name).with_suffix(".webp")
    #         new_image_jpeg_main = Path(instance.main_image.name).with_suffix(".png")

    #         sizes = [
    #             (400, 400),
    #             (200, 200),
    #             (312, 312),
    #             (156, 156),
    #         ]
    #         for i in sizes:
    #             base_image_main = Image.open(instance.main_image)
    #             base_image_main.thumbnail(i)

    #             os.makedirs(
    #                 "{0}/{1}/{2}/{3}/{4}".format(MEDIA_ROOT, "teams", "main", "webp", i[0]),
    #                 exist_ok=True,
    #             )
    #             os.makedirs(
    #                 "{0}/{1}/{2}/{3}/{4}".format(MEDIA_ROOT, "teams", "main", "png", i[0]),
    #                 exist_ok=True,
    #             )

    #             new_webp_path = "{0}/{1}/{2}/{3}/{4}/{5}".format(
    #                 MEDIA_ROOT, "teams", "main", "webp", i[0], new_image_webp_main.name
    #             )
    #             base_image_main.save(new_webp_path, "WEBP", quality=90)
    #             new_jpeg_path = "{0}/{1}/{2}/{3}/{4}/{5}".format(
    #                 MEDIA_ROOT, "teams", "main", "png", i[0], new_image_jpeg_main.name
    #             )
    #             base_image_main.save(new_jpeg_path, "PNG", quality=90)

    #     elif instance.class_type == "specs":
    #         new_image_webp = Path(instance.image.name).with_suffix(".webp")
    #         new_image_png = Path(instance.image.name).with_suffix(".png")

    #         sizes = [
    #             (260, 260),
    #             (180, 180),
    #             (134, 134),
    #         ]
    #         for i in sizes:
    #             base_image_main = Image.open(instance.image)
    #             base_image_main.thumbnail(i)

    #             os.makedirs(
    #                 "{0}/{1}/{2}/{3}".format(MEDIA_ROOT, "specs", "webp", i[0]),
    #                 exist_ok=True,
    #             )
    #             os.makedirs(
    #                 "{0}/{1}/{2}/{3}".format(MEDIA_ROOT, "specs", "png", i[0]),
    #                 exist_ok=True,
    #             )

    #             new_webp_path = "{0}/{1}/{2}/{3}/{4}".format(
    #                 MEDIA_ROOT, "specs", "webp", i[0], new_image_webp.name
    #             )
    #             base_image_main.save(new_webp_path, "WEBP", quality=90)

    #             new_png_path = "{0}/{1}/{2}/{3}/{4}".format(
    #                 MEDIA_ROOT, "specs", "png", i[0], new_image_png.name
    #             )
    #             base_image_main.save(new_png_path, "PNG", quality=90)
