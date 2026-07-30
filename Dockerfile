FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY tools/ ./tools/
RUN pip install --no-cache-dir fastapi uvicorn

ENV PYTHONUNBUFFERED=1
ENV HYPERAI_CREDENTIALS=/run/secrets/credentials.env

EXPOSE 8765

CMD ["python", "-m", "uvicorn", "tools.hyperai_credentials_service:app", "--host", "0.0.0.0", "--port", "8765"]
