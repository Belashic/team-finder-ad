import os
from django.core.management import BaseCommand, call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Загружает готовую базу данных (пользователи, проекты, админ) из seed_data.json'

    def handle(self, *args, **options):
        fixture_path = os.path.join(settings.BASE_DIR, 'seed_data.json')

        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(f'❌ Файл seed_data.json не найден в корне проекта!'))
            return

        self.stdout.write(self.style.SUCCESS('📦 Загружаю данные...'))
        call_command('loaddata', fixture_path)
        self.stdout.write(self.style.SUCCESS('✅ Готово!'))
        self.stdout.write(self.style.SUCCESS('   Админ: admin@teamfinder.ru / admin123'))