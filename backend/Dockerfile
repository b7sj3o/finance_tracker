# BACKEND
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# make entrypoint.sh executable
# RUN chmod +x /app/entrypoint.sh

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
# ENTRYPOINT [ "/app/entrypoint.sh" ]
