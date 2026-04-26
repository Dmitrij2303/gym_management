Gym Management

Проект на Django для управления фитнес-клубом.

Установка и запуск

1. Создайте и активируйте виртуальное окружение:

   python -m venv venv
   source venv/bin/activate

2. Установите зависимости:

   pip install -r requirements.txt

3. Проверьте файл .env в корне проекта. В нем должен быть SECRET_KEY:

   SECRET_KEY=your-secret-key

4. Примените миграции:

   python manage.py migrate

5. Запустите сервер:

   python manage.py runserver

Приложение будет доступно по адресу:

   http://127.0.0.1:8000/

Структура проекта

- config/ - настройки Django-проекта
- core/ - главная страница
- clients/ - клиенты
- trainers/ - тренеры
- services/ - услуги
- bookings/ - бронирования
- docs/ - документация и схемы базы данных

Примечания

- Файл .env добавлен в .gitignore и не должен попадать в репозиторий.
- Локальная база данных SQLite хранится в db.sqlite3.
