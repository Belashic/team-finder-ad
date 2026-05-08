import io
import random
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile


def generate_avatar(letter):
    """Гарантированно крупная буква без внешних шрифтов"""
    
    colors = [
        (79, 70, 229), (5, 150, 105), (220, 38, 38),
        (37, 99, 235), (202, 138, 4), (124, 58, 237),
    ]
    
    # Создаём очень большое изображение
    size = 1000
    img = Image.new('RGB', (size, size), random.choice(colors))
    draw = ImageDraw.Draw(img)
    
    # Ищем любой шрифт
    font = None
    for path in [
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
        '/Library/Fonts/Arial.ttf',
    ]:
        try:
            font = ImageFont.truetype(path, 700)  # Огромный размер
            break
        except:
            pass
    
    if font is None:
        font = ImageFont.load_default()
    
    # Центрируем
    bbox = draw.textbbox((0, 0), letter, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) / 2
    y = (size - h) / 2 - 50
    
    draw.text((x, y), letter, fill='white', font=font)
    
    # Уменьшаем до 400x400
    img = img.resize((400, 400), Image.Resampling.LANCZOS)
    
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    
    return ContentFile(buf.getvalue(), name=f'{letter}.png')