# Мэрия Лос-Сантоса — портал на Django

Полноценная замена vibecoded однофайлового сайта.  
Стек: **Django 5 + PostgreSQL + Apache** (native на Rocky Linux).

## Возможности

- Полная админ-панель Django (`/admin/`) с управлением пользователями и ролями
- История изменений (django-simple-history) + явный журнал аудита
- Уведомления для активных сессий администраторов (JSON endpoint + polling)
- Все разделы оригинала: бизнесы, новости, документы, отзывы, заявки на приём, сотрудники, частные организации, карта
- Загрузка изображений + поддержка внешних URL
- Безопасность: валидация, CSRF, хеширование паролей, роли

## Быстрый старт (разработка)

```bash
cd los_santos_cityhall
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройте PostgreSQL и создайте БД + пользователя
# Скопируйте и отредактируйте .env (см. ниже)

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Файл .env (пример)

```
SECRET_KEY=very-long-random-string-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=cityhall
DB_USER=cityhall
DB_PASSWORD=strongpassword
DB_HOST=localhost
DB_PORT=5432
```

## Развёртывание на Rocky Linux 9 (native + Apache)

1. Установите пакеты:
   ```bash
   sudo dnf install -y python3 python3-pip postgresql-server httpd mod_ssl
   sudo postgresql-setup --initdb
   sudo systemctl enable --now postgresql httpd
   ```

2. Создайте БД и пользователя PostgreSQL.

3. Разверните проект (например в `/opt/cityhall`), создайте venv, установите зависимости, выполните `migrate` и `collectstatic`.

4. Настройте Gunicorn + systemd unit и проксируйте через Apache (рекомендуется) или используйте mod_wsgi.

5. Пример фрагмента Apache VirtualHost (прокси на Gunicorn):
   ```apache
   <VirtualHost *:80>
       ServerName cityhall.example.com
       ProxyPreserveHost On
       ProxyPass /static/ !
       ProxyPass /media/ !
       Alias /static/ /opt/cityhall/staticfiles/
       Alias /media/ /opt/cityhall/media/
       ProxyPass / http://127.0.0.1:8000/
       ProxyPassReverse / http://127.0.0.1:8000/
   </VirtualHost>
   ```

6. Настройте HTTPS (certbot или свой сертификат).

## Дополнительно

- Роли пользователей: admin / editor / viewer
- Журнал аудита доступен в админке
- Endpoint уведомлений: `/notifications/` (только для авторизованных)
- Карта пока использует внешний URL (можно заменить на локальный файл)

Проект готов к расширению (Channels для настоящих WebSocket-уведомлений, бизнес-аккаунты, поиск и т.д.).
