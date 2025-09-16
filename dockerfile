FROM python:3.10-slim

# Установка зависимостей
COPY requirements.txt /opt/build/
RUN pip install --no-cache-dir -r /opt/build/requirements.txt

# Копирование исходного кода
COPY . /opt/build

# Установка рабочей директории
WORKDIR /opt/build

# Запуск приложения на порту 8000
EXPOSE 8000
CMD ["uvicorn", "main:app_fastapi", "--host", "0.0.0.0", "--port", "8000"]
