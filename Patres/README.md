# Library API

RESTful API для управления библиотекой. Реализован на FastAPI 
с использованием SQLAlchemy, Alembic и JWT-аутентификации.


## Возможности

- Аутентификация библиотекарей через JWT
- CRUD для книг и читателей
- Выдача и возврат книг
- Валидация с Pydantic
- Покрытие тестами через Pytest


## Основной стек технологий

- Python
- FastAPI
- SQLAlchemy
- Alembic
- SQLite/PostgreSQL
- Pydantic
- Pytest


## Установка и запуск

```bash
git clone https://github.com/Shaba010820/My_projects/Patres
cd Patres
python -m venv venv
source venv/bin/activate или на Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --port 8000


Также есть Docker compose с использованием Postgres вместо sqlite. 
Сборка по команде:

docker-compose up --build

Запуск тестов командой "pytest"


После запуска перейдите на http://localhost:8000/docs для просмотра Swagger UI.
