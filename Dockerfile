FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install cryptography

CMD ["python", "aphb_agent.py", "--help"]
