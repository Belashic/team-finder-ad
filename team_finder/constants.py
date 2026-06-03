from django.db import models

PROJECTS_PER_PAGE = 12
USERS_PER_PAGE = 12

USER_FIRST_NAME_MAX_LENGTH = 20
USER_LAST_NAME_MAX_LENGTH = 20
USER_PHONE_MAX_LENGTH = 15
USER_ABOUT_MAX_LENGTH = 512
USER_EMAIL_MAX_LENGTH = 254

PROJECT_NAME_MAX_LENGTH = 255
PROJECT_STATUS_MAX_LENGTH = 6
PROJECT_DESCRIPTION_MAX_LENGTH = 2000

class ProjectStatus(models.TextChoices):
    OPEN = 'open', 'Открыт'
    CLOSED = 'closed', 'Закрыт'

PROJECT_STATUS_OPEN = ProjectStatus.OPEN.value
PROJECT_STATUS_CLOSED = ProjectStatus.CLOSED.value
PROJECT_STATUS_CHOICES = ProjectStatus.choices

AVATAR_SIZE = (400, 400)
AVATAR_FONT_SIZE = 300
AVATAR_UPLOAD_DIR = 'avatars/'
AVATAR_TEXT_COLOR = 'white'
DEFAULT_AVATAR = 'images/default-avatar.png'

AVATAR_BG_COLORS = [
    (79, 70, 229),
    (5, 150, 105),
    (220, 38, 38),
    (37, 99, 235),
    (202, 138, 4),
    (124, 58, 237),
    (8, 145, 178),
    (255, 152, 0),
    (255, 193, 7),
    (233, 30, 99),
]

FILTER_OWNERS_OF_FAVORITES = 'owners-of-favorite-projects'
FILTER_OWNERS_OF_PARTICIPATING = 'owners-of-participating-projects'
FILTER_INTERESTED_IN_MY = 'interested-in-my-projects'
FILTER_PARTICIPANTS_OF_MY = 'participants-of-my-projects'

GITHUB_URL_PATTERN = 'github.com'

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Yekaterinburg'

MSG_PROFILE_UPDATED = 'Профиль обновлён'
MSG_PASSWORD_CHANGED = 'Пароль изменён'
MSG_WELCOME = 'Добро пожаловать!'