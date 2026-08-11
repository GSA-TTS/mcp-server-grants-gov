FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
ENV PORT=8080

WORKDIR /app

COPY requirements.txt .
COPY pyproject.toml .
COPY README.md .
COPY src ./src
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# PORT=8080 selects the HTTP transport at /mcp (see app.py transport selection).
CMD ["sh", "-c", "PORT=8080 python -m grants_gov_mcp.app"]
