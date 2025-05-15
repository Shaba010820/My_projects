# Task Manager API 
    Task Manager - это "проект" на FastApi для управления задачами. 
    Поддерживает CRUD-операции, фильтрацию по статусу и даже, а также авторизацию по токену.

## Описание API


1. Аутентификация

**POST `/login`**  
Авторизация с помощью `username` и `password`. Возвращает JWT токен.
    
Пример запроса:
        curl -X POST http://localhost:8000/login -d "username=admin&password=password"
        должны получить access_token и token_type в json формате

**POST `/register`**

Регистрация нового пользователя с `username` и `password`
    
Пример запроса:
        curl -X POST http://localhost:8000/register \
        -H "Content-Type: application/json" \
        -d '{"username": "newuser", "password": "newpassword"}'


2. Tasks

Все эндпоинты ниже требуют авторизацию(Authorization: Bearer <TOKEN> в заголовке)
    
**POST /tasks/**

Создаёт новую задачу
    
Пример запроса:
    curl -X POST http://localhost:8000/tasks/ \
    -H "Authorization: Bearer <TOKEN>" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Пример задачи",
        "description": "Описание задачи",
        "due_date": "2025-05-20T23:59:00",
        "status": "new"
    }' 

**GET /tasks/**

Возвращает список задач. Поддерживает фильтрацию
    
Фильтрации по параметрам:
    1. status - new, done, in_progress
    2. due_date_lt - До указанной даты (less than)
    3. due_date_gt - После указанной даты(greater than)
    
Пример запроса:
    curl -X GET "http://localhost:8000/tasks/?status=new&due_date__lt=2025-05-21" \
    -H "Authorization: Bearer <TOKEN>"
  
    
**GET /tasks/{id}**

Получить задачу по ID
    
Пример запроса:
    curl -X GET http://localhost:8000/tasks/1 -H "Authorization: Bearer <TOKEN>"

**PUT /tasks/{id}**

Полное обновление задачи
    
Пример запроса:
    curl -X PUT http://localhost:8000/tasks/1 \
    -H "Authorization: Bearer <TOKEN>" \
    -H "Content-Type: application/json" \
    -d '{
        "title": "Обновлённая задача",
        "description": "Новое описание",
        "due_date": "2025-05-22T23:59:00",
        "status": "in_progress"
    }

**PATCH /tasks/{id}**

Частичное обновление задач(меняется только одно поле, например, только статус)
    
Пример запроса:
    curl -X PATCH http://localhost:8000/tasks/1 \
    -H "Authorization: Bearer <TOKEN>" \
    -H "Content-Type: application/json" \
    -d '{ "status": "done" }'

**DELETE /tasks/{id}**

Удаление задачи

Пример запроса:
    curl -X DELETE http://localhost:8000/tasks/1 \
    -H "Authorization: Bearer <TOKEN>"


### Инструкция запуска

1. Клонируйте репозиторий:
    git clone https://github.com/Shaba010820/My_projects/tree/main/Reviro
    
    cd Reviro
2. Создайте виртуальное окружение и активируйте его:
    python -m venv venv
    source venv/bin/activate или на Windows venv/Scripts/activate
3. Установите зависимости:
    pip install -r requirements.txt
4. Запуск приложения:
    uvicorn backend.main:app --reload 
    (конечно правильно было бы запускать её в папке backend командой uvicorn main:app, 
     но такой запуск из за архитектуры)


### Ответы на вопросы (рефлексия)

**Что было самым сложным в задании?**
Самая сложная часть для меня была реализация авторизации и составление этого README файла:)

**Что получилось особенно хорошо**
Думаю авторизация и аутентификация вышли отлично

**Что бы вы доработали при наличии времени?**
Наверное раз уж я выбрал таблицу как Task Manager, то можно было бы связать таски к пользователям + использовали бы 
связи между таблицами.

**Сколько времени заняло выполнение?**
3 дня по 5-6 часов примерно

**Чему вы научились при выполнении?**
У меня мало опыта с FastAPI, поэтому фильтрацию и авторизацию впервые испробовал на практике


