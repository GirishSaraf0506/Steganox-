# Multi-stage build for minimal image size
FROM python:3.9-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.9-slim

# Security: non-root user
RUN groupadd -r steganox && useradd -r -g steganox steganox

WORKDIR /app

COPY --from=builder /root/.local /home/steganox/.local
COPY steganox/ steganox/
COPY requirements.txt .

ENV PATH=/home/steganox/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

RUN chown -R steganox:steganox /app

USER steganox

EXPOSE 5000

CMD ["python", "-m", "steganox.ui.web.app"]
