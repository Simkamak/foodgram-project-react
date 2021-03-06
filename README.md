# Продуктовый помошник Foodgram 

![api+db+front](https://github.com/Simkamak/foodgram-project-react/actions/workflows/foodgram_project.yml/badge.svg)
![api+db+front](https://img.shields.io/github/repo-size/Simkamak/foodgram-project-react)

## Описание

---

Проект Foodgram позволяет постить рецепты, делиться и скачивать списки продуктов

## Использованные технологии

- Docker
- postresql
- nginx
- gunicorn
- python
- Django
- Django REST framework

### Инструкции по запуску
- клонируйте репозиторий
```
git clone https://github.com/Simkamak/foodgram-project-react.git
```
- откройте терминал и перейдите в директорию проекта в папку infra/
```
docke-compouse up
```
- создание супрепользователя
```
docker-compose exec backend python manage.py createsuperuser
```
- сбор статики и миграци
```
docker-compose exec backend python manage.py collectstatic
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```
### Админ зона

>Superuser:
>
>login: admin@admin.ru
>
>password: admin
>
>url:  http://178.154.254.60

### Заполнение .env:

Чтобы добавить переменную в .env необходимо открыть файл .env в директории 
infra/ 
директории проекта и поместить туда переменную в формате имя_переменной=значение. 
Пример .env файла:

```
DB_ENGINE=my_db
DB_NAME=db_name
POSTGRES_USER=my_user
POSTGRES_PASSWORD=my_pass
DB_HOST=db_host
DB_PORT=db_port
SECRET_KEY=my_secret_key
```
### Автор:

Автор Максим Горностаев. Задание было выполнено в рамках курса от Yandex 
Praktikum python-бэкенд разработчик.
___
![Alt Text](https://avatars0.githubusercontent.com/u/30868400?s*)
