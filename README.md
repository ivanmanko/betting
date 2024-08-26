Here's the README in English:

---

# Betting Service

## Overview

This service is an API for managing events and bets placed on them. The service includes the following main components:

- **BetMaker**: A module for managing events and bets.
- **LineProvider**: A module for providing event data.
- **CeleryWorker**: A background process that checks events every 30 seconds, updates their status, and updates the status of related bets.

### How It Works

1. **Creating Events and Bets:**
   - You can add new events and bets on those events through the API routes available in the Swagger interface.
   
2. **Background Event Processing:**
   - Every 30 seconds, the `celery_worker` checks for new events and their deadlines.
   - If an event's deadline has passed, `celery_worker` randomly changes the event's status to `1` (won) or `2` (lost).
   - Then, `celery_worker` checks the bets associated with this event and updates their status to match the event's status.

3. **Checking the Results:**
   - You can verify that the status of events and related bets are automatically updated by using the Swagger interface to view the current data.

### API Routes

Detailed API route descriptions are available through the Swagger interface at:
- `http://localhost:8080/docs` for LineProvider
- `http://localhost:8081/docs` for BetMaker

- **GET /events** - Retrieve a list of active events.
- **POST /bet** - Create a new bet.
- **GET /bets** - Retrieve a list of all bets.
- **PUT /bet** - Update the state of a bet.

### Running in Docker

To run the service in Docker, follow these steps:

1. **Create a `.env` file with the necessary environment variables:**

   Example `.env` file:
   ```env
# Database settings for bet_maker
POSTGRES_BET_MAKER_USER=bet_maker_user
POSTGRES_BET_MAKER_PASSWORD=bet_maker_password
POSTGRES_BET_MAKER_DB=bet_maker_db
POSTGRES_BET_MAKER_HOST=postgres_bet_maker
POSTGRES_BET_MAKER_PORT=5432

# Database settings for line_provider
POSTGRES_LINE_PROVIDER_USER=line_provider_user
POSTGRES_LINE_PROVIDER_PASSWORD=line_provider_password
POSTGRES_LINE_PROVIDER_DB=line_provider_db
POSTGRES_LINE_PROVIDER_HOST=postgres_line_provider
POSTGRES_LINE_PROVIDER_PORT=5432

# Settings for celery_worker
CELERY_WORKER_LINE_PROVIDER_HOST=line_provider
CELERY_WORKER_LINE_PROVIDER_PORT=8080
CELERY_WORKER_BET_MAKER_HOST=bet_maker
CELERY_WORKER_BET_MAKER_PORT=8081
CELERY_WORKER_REDIS_HOST=redis
CELERY_WORKER_REDIS_PORT=6379
CELERY_WORKER_REDIS_DB=1

# Settings for the line_provider service
LINE_PROVIDER_HOST=localhost
LINE_PROVIDER_PORT=8080

# Settings for the bet_maker service
BET_MAKER_HOST=localhost
BET_MAKER_PORT=8081

   ```

2. **Run Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   This will create and start containers for each service:

   - `bet_maker` on port `8081`
   - `line_provider` on port `8080`
   - `celery_worker` for background tasks
   - `postgres_bet_maker` and `postgres_line_provider` for databases
   - `redis` for task queues

3. **Initialize Databases:**

    Initialize Databases:

    After the containers are created, the SQL scripts to initialize the databases are automatically executed. These scripts create the necessary users and databases.

    For example, when the postgres_bet_maker and postgres_line_provider containers start, they automatically run the corresponding SQL scripts (init-bet_maker.sql and init-line_provider.sql). These scripts create the required users and databases, so no manual execution is needed.

4. **Using Swagger for Testing:**

   Open the following URLs to access the Swagger interfaces:

   - For BetMaker: `http://localhost:8081/docs`
   - For LineProvider: `http://localhost:8080/docs`

   Use Swagger to test and verify the API functionality.

---
