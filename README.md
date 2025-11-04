# Celery Calculator

A distributed calculator using Celery with Redis as the message broker and result backend.

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis:**
   ```bash
   brew services start redis
   ```

## Running the App

**Terminal 1 - Start Worker:**

```bash
celery -A app worker --loglevel=info
```

**Terminal 2 - Run App:**

```bash
python main.py
```

## Features

- Four operations: add, subtract, multiply, divide
- Asynchronous task processing with Celery
- Redis as message broker and result backend
- Modular pub-sub architecture (app and worker)
- **Bonus:** Operation frequency tracking

## How It Works

1. User submits a calculation task via `main.py`
2. Task is sent to Redis queue
3. Worker picks up the task and executes it
4. Result is stored in Redis backend
5. User retrieves the result
6. Operation frequency is tracked in Redis

## Project Structure

```
app/
├── __init__.py          - Celery app setup
├── calculator.py        - Calculator logic
└── tasks.py             - Celery tasks
worker/
└── worker.py            - Worker process
celery_config.py         - Redis configuration
main.py                  - Client application
```

## Troubleshooting

- **"Connection refused"**: Start Redis with `brew services start redis`
- **"No module named 'app'"**: Run commands from project root directory
- **Worker not responding**: Make sure worker is running in separate terminal
