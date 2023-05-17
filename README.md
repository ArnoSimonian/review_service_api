# api_yamdb
api_yamdb

### Описание:

Проект **api_final_yatube** является полноценным API для социальной сети ***Yatube***.

Разработано на базе учебного проекта ***Kittigram***.


### Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ArnoSimonian/api_final_yatube.git
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```


### Примеры запросов к API:

Получение публикаций:
GET api/v1/posts/

Создание публикации:
POST api/v1/posts/

Обновление публикации:
PUT api/v1/posts/{id}/

Частичное обновление комментария:
PATCH api/v1/posts/{post_id}/comments/{id}/

Подписка:
POST api/v1/follow/

Информация о сообществе:
GET api/v1/groups/{id}/
