FROM python:3.12-slim AS builder
WORKDIR /app
COPY app.py .
RUN pip install --target=/app/libs flask requests

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app /app
ENV PORT=5000
ENV PYTHONPATH=/app/libs
EXPOSE 5000

LABEL org.opencontainers.image.title="Weather App"
LABEL org.opencontainers.image.authors="Dominik Majchrzak"

HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1

CMD ["python", "app.py"]
