FROM python:3.12-slim

WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod +x /app/healthcheck.sh

ENV DEBUG_LEVEL=DEBUG
ENV RATE_DEFAULT_URL=https://api.exchangerate.host
ENV FIXER_DATE_FMT=%Y-%m-%d
ENV FIXER_DEFAULT_URL=http://data.fixer.io/api/latest
ENV WEATHER_DEFAULT_URL=http://api.weatherapi.com/v1/current.json
ENV AWS_REGION_ID=il-central-1

ENV USER_POOL_ID=il-central-1_0zf0LNlSD
ENV USER_POOL_APP_ID=2chpfairj5rakt9lffar3gnv3h

ENV HEALTH_PATH=http://localhost:8000/health


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]