# denvo-backend
[denvoRu/Backend](https://github.com/denvoRu/Backend) - это бекенд приложение для приложения УрФУ - Оценка пар

## Стек
* Fastapi
* SQLAlchemy
* Pydantic
* Uvicorn
* DDD


## Запуск

### Установка Зависимостей
Сначала нам необходимо установить зависимости:
```
pip install -r requirements.txt
```

### Файл конфигурации
Для работы с базой данных мы скрываем информацию о подключение в `.env` файле, выглядит его содержимое примерно так:
```
# Database 
DATABASE_DRIVER_NAME=""
DATABASE_HOST=""
DATABASE_PORT=3000
DATABASE_USERNAME=""
DATABASE_PASSWORD=""
DATABASE=""

# APP
PROJECT_NAME="Student Voice"
JWT_SECRET_KEY=""
```

### Исполнение
Для запуска сервера используем команду:
```python
python main.py
```
