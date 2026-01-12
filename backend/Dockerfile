
FROM python:3.10-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*


COPY backend/requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY model/saved_models /app/model_files/saved_models


RUN mkdir -p /app/logs


EXPOSE 8030


HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8030/ || exit 1


CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8030"]