# DriveNow Car Rental API

A car rental management system  
**Stack:** 
- FastAPI
- PostgreSQL
- Docker
- Prometheus

## Features

- Separation of concerns (services, repositories, models)
- **Car CRUD**: Cars (create, read, update status, list/filter)
- **Rental (C)R(U)D**: Create rental → End rental (auto car status update)
- **Production Docker**: Postgres + App with healthchecks
- **Metrics**: Prometheus metrics (Counters, Gauges and Histograms)
- **Docs**: `/docs` (Swagger UI)

## Installation & Start

1. **Copy environment variables:**
   ```bash
   cp .env.template .env
   ```

2. **Edit `.env` with your credentials:**
   ```
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_secure_password  
   POSTGRES_DB=your_db_name
   ```

3. **Run with Docker:**
   ```bash
   docker compose up --build
   ```

4. **Access:**
   - **API**: `http://localhost:7777/docs`
   - **Metrics**: Metrics endpoint: `http://localhost:7777/metrics` Prometheus: `http://localhost:9090`
   - **pgAdmin**: `localhost:7778` (user/password/db name from `.env`)

## API Endpoints

### Car Management (`/car`)

| Method | Endpoint | Description                                          | Parameters |
|--------|----------|------------------------------------------------------|------------|
| `POST` | `/car/` | Create new car                                       | `{"model": "Toyota", "year": 2023}` |
| `GET` | `/car/` | List cars (with pagination)                          | `?status=AVAILABLE&limit=10` |
| `GET` | `/car/{car_id}` | Get single car via its id                            | `car_id=1` |
| `PATCH` | `/car/{car_id}` | Update status (**"AVAILABLE"**, **"IN_USE"**, **"UNDER_MAINTENANCE"**) | `{"status": "IN_USE"}` |

### Rental Management (`/rental`)

| Method | Endpoint | Description      | Parameters                                              |
|--------|----------|------------------|---------------------------------------------------------|
| `GET`  | `/rental/` | Get rental by ID | `{"rental_id": 1}`                                        |
| `POST` | `/rental/` | Start rental     | `?car_id=1&customer_name=John`                          |
| `POST` | `/rental/{rental_id}/end` | End rental       | `{"end_date": "2026-02-11T15:00:00"}` ( date is optional) |


## Architecture

```
src/
├── api/         # FastAPI routers + endpoints
├── services/    # Business logic (CarService, RentalService)
├── db/          # SQLAlchemy models + session
      └── models/      # Enums (CarStatus: AVAILABLE, IN_USE, MAINTENANCE)
```

**Layers**: API → Services → DB (dependency injection via `Depends(get_db)`)

## Local Development

```bash
# Install deps
pip install -r requirements.txt

# Run (uses SQLite)
python main.py
```

## Docker Compose

- **App**: `localhost:7777`
- **Postgres DB**: `localhost:7778`
- **Healthchecks**: App waits for DB ready
- **Volumes**: Persistent data + live code reload

## Example Flow

```bash
# 1. Add a new car
curl -X POST "http://localhost:7777/car/" \
  -H "Content-Type: application/json" \
  -d '{"model": "Toyota Corolla", "year": 2023}'

# 2. List available cars
curl "http://localhost:7777/car/?status=AVAILABLE"

# 3. Rent one car via its id
curl -X POST "http://localhost:7777/rental/?car_id=1&customer_name=SomePerson"

# 4. End rental (car will be set back to being AVAILABLE)
curl -X POST "http://localhost:7777/rental/1/end"
```

## .env.template

Create `.env` from the `.env.template` file:
```
POSTGRES_USER=admin
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=drivenow
```

**Don't commit push the .env file filled with sensitive data!!!**

## Answers

> #### Why did I choose PostgreSQL?
> I chose PostgreSQL because the data structures of my models are persistent. For example, a "car" will have a consistent set of attributes unless explicitly changed

> This eliminates the need for flexible, JSON-like schemas that databases such as MongoDB provide

> Other reason is because I was already familiar with the documentation of the docker-compose structure
> of postgres and liked the way it was well [documented there too](https://hub.docker.com/_/postgres).