import io
import os
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from team_finder.constants import AVATAR_BG_COLORS


def generate_avatar(letter):
    letter = letter[0].upper() if letter else 'U'
    bg_color = random.choice(AVATAR_BG_COLORS)

    size = 1000
    image = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(image)

    font = None
    font_size = 700

    font_paths = [
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/Library/Fonts/Arial.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSans.ttf',
        '/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf',
        'C:/Windows/Fonts/arialbd.ttf',
        'C:/Windows/Fonts/arial.ttf',
    ]

    for path in font_paths:
        try:
            if os.path.exists(path):
                font = ImageFont.truetype(path, font_size)
                break
        except:
            continue

    if font is None:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size - text_width) / 2 - bbox[0]
    y = (size - text_height) / 2 - bbox[1]

    draw.text((x, y), letter, fill='white', font=font)

    image = image.resize((400, 400), Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    image.save(buffer, format='PNG')

    return ContentFile(buffer.getvalue(), name=f'{letter}.png')