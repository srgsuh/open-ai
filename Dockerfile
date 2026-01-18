FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV DEBUG_LEVEL=DEBUG
ENV OLLAMA_URL=http://localhost:11434/api/chat
ENV OLLAMA_MODEL=phi3:mini
ENV RATE_DEFAULT_URL=https://api.exchangerate.host
ENV FIXER_DATE_FMT=%Y-%m-%d
ENV FIXER_DEFAULT_URL=http://data.fixer.io/api/latest
ENV WEATHER_DEFAULT_URL=http://api.weatherapi.com/v1/current.json
ENV AWS_REGION_ID=il-central-1

ENV USER_POOL_ID=il-central-1_0zf0LNlSD
ENV USER_POOL_APP_ID=2chpfairj5rakt9lffar3gnv3h


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]