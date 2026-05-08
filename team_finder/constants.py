# Пагинация
PROJECTS_PER_PAGE = 12
USERS_PER_PAGE = 12


# Пользователь
USER_NAME_MAX_LENGTH = 128
USER_SURNAME_MAX_LENGTH = 128
USER_PHONE_MAX_LENGTH = 15
USER_ABOUT_MAX_LENGTH = 512
USER_EMAIL_MAX_LENGTH = 254
USER_PHONE_REGEX = r'^\+7\d{10}$'
USER_PHONE_ALT_REGEX = r'^8\d{10}$'
USER_PHONE_PREFIX = '+7'


# Проект
PROJECT_NAME_MAX_LENGTH = 255
PROJECT_STATUS_MAX_LENGTH = 6
PROJECT_DESCRIPTION_MAX_LENGTH = 2000
PROJECT_STATUS_CHOICES = [
    ('open', 'Открыт'),
    ('closed', 'Закрыт'),
]
PROJECT_STATUS_OPEN = 'open'
PROJECT_STATUS_CLOSED = 'closed'


# Аватар
AVATAR_SIZE = (400, 400)  # Большой размер для качественной картинки
AVATAR_FONT_SIZE = 300    # Крупный шрифт — буква на весь аватар
AVATAR_UPLOAD_DIR = 'avatars/'
AVATAR_TEXT_COLOR = 'white'
DEFAULT_AVATAR = 'images/default-avatar.png'

# Цвета фона аватара (RGB кортежи для Pillow)
AVATAR_BG_COLORS = [
    (79, 70, 229),    # Индиго
    (5, 150, 105),    # Зелёный
    (220, 38, 38),    # Красный
    (37, 99, 235),    # Синий
    (202, 138, 4),    # Жёлтый
    (124, 58, 237),   # Фиолетовый
    (8, 145, 178),    # Голубой
    (255, 152, 0),    # Оранжевый
    (255, 193, 7),    # Янтарный
    (233, 30, 99),    # Розовый
]


# Фильтрация пользователей (Вариант 1)
FILTER_OWNERS_OF_FAVORITES = 'owners-of-favorite-projects'
FILTER_OWNERS_OF_PARTICIPATING = 'owners-of-participating-projects'
FILTER_INTERESTED_IN_MY = 'interested-in-my-projects'
FILTER_PARTICIPANTS_OF_MY = 'participants-of-my-projects'


# GitHub
GITHUB_URL_PATTERN = 'github.com'


# Язык и время
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Yekaterinburg'

# Сообщения
MSG_PROFILE_UPDATED = 'Профиль обновлён'
MSG_PASSWORD_CHANGED = 'Пароль изменён'
MSG_WELCOME = 'Добро пожаловать!'