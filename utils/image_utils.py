import os
from PIL import Image


def resize_image(source_path, dest_path, max_size=(1920, 1080), keep_ratio=True):
    img = Image.open(source_path)
    if keep_ratio:
        img.thumbnail(max_size, Image.LANCZOS)
    else:
        img = img.resize(max_size, Image.LANCZOS)
    img.save(dest_path, 'PNG')
    return dest_path


def crop_to_circle(source_path, dest_path, size=(256, 256)):
    img = Image.open(source_path)
    img = img.resize(size, Image.LANCZOS)

    from PIL import ImageDraw
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)

    output = Image.new('RGBA', size, (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    output.save(dest_path, 'PNG')
    return dest_path


def get_image_size(path):
    if os.path.exists(path):
        with Image.open(path) as img:
            return img.size
    return (0, 0)
