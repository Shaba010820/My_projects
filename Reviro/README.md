# Task Manager API 
    Task Manager - это "проект" на FastApi для управления задачами. 
    Поддерживает CRUD-операции, фильтрацию по статусу и даже, а также авторизацию по токену.

## Описание API

### Аутентификация

**POST `/login`**  
# Авторизация с помощью `username` и `password`. Возвращает JWT токен.

    Пример запроса:
        curl -X POST http://localhost:8000/login -d "username=admin&password=password"
        должны получить access_token и token_type в json формате
    
#### Tasks

    Все эндпоинты ниже требуют авторизацию(Authorization: Bearer <TOKEN> в заголовке)
    
**POST /tasks/**
# Создаёт новую задачу
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
# Возвращает список задач. Поддерживает фильтрацию
    
    Фильтрации по параметрам:
    1. status - new, done, in_progress
    2. due_date_lt - До указанной даты (less than)
    3. due_date_gt - После указанной даты(greater than)
    
    Пример запроса:
    curl -X GET "http://localhost:8000/tasks/?status=new&due_date__lt=2025-05-21" \
    -H "Authorization: Bearer <TOKEN>"
  
    
**GET /tasks/{id}**
# Получить задачу по ID
    
    Пример запроса:
    curl -X GET http://localhost:8000/tasks/1 -H "Authorization: Bearer <TOKEN>"

**PUT /tasks/{id}**
# Полное обновление задачи
    
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
# Частичное обновление задач(меняется только одно поле, например, только статус)
    
    Пример запроса:
    curl -X PATCH http://localhost:8000/tasks/1 \
    -H "Authorization: Bearer <TOKEN>" \
    -H "Content-Type: application/json" \
    -d '{ "status": "done" }'

**DELETE /tasks/{id}**
# Удаление задачи

    Пример запроса:
    curl -X DELETE http://localhost:8000/tasks/1 \
    -H "Authorization: Bearer <TOKEN>"

