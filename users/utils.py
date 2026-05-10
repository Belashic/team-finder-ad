import io
import random
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile


def generate_avatar(letter):
    """Гарантированно крупная буква на цветном фоне."""
    
    colors = [
        (79, 70, 229),   # Индиго
        (5, 150, 105),   # Зелёный
        (220, 38, 38),   # Красный
        (37, 99, 235),   # Синий
        (202, 138, 4),   # Жёлтый
        (124, 58, 237),  # Фиолетовый
        (8, 145, 178),   # Голубой
        (255, 152, 0),   # Оранжевый
    ]
    
    # Создаём большое изображение — чем больше, тем лучше качество буквы
    size = 400
    img = Image.new('RGB', (size, size), random.choice(colors))
    draw = ImageDraw.Draw(img)
    
    # Используем стандартный шрифт Pillow, но с ОЧЕНЬ большим размером
    # Это работает на любой ОС без внешних файлов
    try:
        # Пробуем загрузить дефолтный шрифт и увеличить его размер
        font = ImageFont.load_default()
        # Стандартный шрифт маленький, поэтому рисуем букву как текст,
        # но масштабируем само изображение
        font_size = 1
        # Подбираем размер шрифта так, чтобы буква занимала ~70% ширины
        while True:
            test_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size) if __import__('os').path.exists("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf") else None
            if test_font is None:
                # Если DejaVu нет — попробуем другие системные шрифты
                font_paths = [
                    "/System/Library/Fonts/Helvetica.ttc",
                    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                    "/Library/Fonts/Arial.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
                ]
                test_font = None
                for path in font_paths:
                    if __import__('os').path.exists(path):
                        test_font = ImageFont.truetype(path, font_size)
                        break
                if test_font is None:
                    # Совсем нет шрифтов — рисуем крупно стандартным
                    font = ImageFont.load_default()
                    break
            
            bbox = draw.textbbox((0, 0), letter, font=test_font)
            w = bbox[2] - bbox[0]
            if w > size * 0.7 or font_size > 200:
                font = test_font
                break
            font_size += 5
    except:
        # Если совсем ничего не работает — используем стандартный шрифт
        font = ImageFont.load_default()
    
    # Центрируем букву
    bbox = draw.textbbox((0, 0), letter, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]
    
    # Рисуем белую букву
    draw.text((x, y), letter.upper(), fill='white', font=font)
    
    # Сохраняем в буфер
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    
    # Имя файла
    filename = f'{letter.upper()}.png'
    
    return ContentFile(buf.getvalue(), name=filename)