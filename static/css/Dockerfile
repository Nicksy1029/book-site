FROM python:3.11-slim

# Переменная, чтобы вывод Python не буферизировался (логи видны сразу)
ENV PYTHONUNBUFFERED=1

# Рабочая директория в контейнере
WORKDIR /app

# Копируем зависимости и ставим их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Команда запуска (для разработки; для продакшена лучше gunicorn/uwsgi)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]