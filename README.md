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
Для работы с базой данных мы скрываем информацию о подключение в `.env` файле, выглядит его содержимое примерно также, как в файле `.env.example`:

### Исполнение
Для запуска сервера используем команду:
```python
python main.py
```
