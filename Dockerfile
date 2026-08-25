FROM python:3.12-slim
WORKDIR /app
COPY main.py ./main.py
RUN useradd --system --uid 10001 --create-home appuser
USER 10001:10001
ENTRYPOINT ["python", "main.py"]
