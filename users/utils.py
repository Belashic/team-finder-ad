import io
import random
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile


def generate_avatar(letter):
    """Генерация аватарки с крупной буквой на цветном фоне."""
    
    colors = [
        (79, 70, 229),   # Индиго
        (5, 150, 105),   # Зелёный
        (220, 38, 38),   # Красный
        (37, 99, 235),   # Синий
        (202, 138, 4),   # Жёлтый
        (124, 58, 237),  # Фиолетовый
    ]
    
    letter = letter[0].upper() if letter else 'U'
    bg_color = random.choice(colors)
    
    # Создаём большое изображение (будет уменьшено потом)
    size = 1000
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Пробуем загрузить системный шрифт большого размера
    font = None
    font_size = 700
    
    # Список шрифтов для разных ОС
    font_paths = [
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
        # Windows (если запускается через WSL или нативно)
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    
    import os
    for path in font_paths:
        try:
            if os.path.exists(path):
                font = ImageFont.truetype(path, font_size)
                break
        except:
            continue
    
    # Если шрифт не найден - используем стандартный
    if font is None:
        font = ImageFont.load_default()
    
    # Вычисляем размеры текста и центрируем
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) / 2 - bbox[0]
    y = (size - text_height) / 2 - bbox[1]
    
    # Рисуем белую букву
    draw.text((x, y), letter, fill='white', font=font)
    
    # Уменьшаем до нужного размера
    img = img.resize((400, 400), Image.Resampling.LANCZOS)
    
    # Сохраняем в буфер
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    
    return ContentFile(buf.getvalue(), name=f'{letter}.png')