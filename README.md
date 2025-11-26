# Service Membership API

Backend API for managing service memberships (gym, coaching center, salon) built with FastAPI and PostgreSQL.

## Features

✅ Member management with status tracking  
✅ Flexible membership plans  
✅ Subscription handling with automatic end-date calculation  
✅ Attendance tracking with check-in validation  
✅ **Database trigger** for automatic check-in counter  
✅ Comprehensive error handling and validation  
✅ Interactive API documentation  

## Tech Stack

- **Python** 3.9+
- **FastAPI** - Modern web framework
- **PostgreSQL** - Primary database (SQLite supported)
- **SQLAlchemy** - ORM
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Quick Start

### 1. Clone or Setup Project

```bash
mkdir service-membership-api
cd service-membership-api
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Database

**PostgreSQL:**
```bash
createdb membership_db
```

**Or use existing database** - update .env file

### 5. Configure Environment

Create `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/membership_db
```

For SQLite (alternative):
```env
DATABASE_URL=sqlite:///./membership.db
```

### 6. Apply Database Trigger

**PostgreSQL:**
```bash
psql -d membership_db -f triggers.sql
```

**SQLite:**
```bash
sqlite3 membership.db < sqlite_trigger.sql
```

### 7. Run Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, access:

- **Swagger UI**: http://127.0.0.1:8000/docs)localhost:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Root**: http://127.0.0.1:8000 -> It will print in the logs

## API Endpoints

### Members

- `POST /members` - Create new member
- `GET /members` - List all members (optional status filter)
- `GET /members/{id}/current-subscription` - Get active subscription
- `GET /members/{id}/attendance` - Get attendance history

### Plans

- `POST /plans` - Create membership plan
- `GET /plans` - List all plans

### Subscriptions

- `POST /subscriptions` - Create subscription (auto end-date)

### Attendance

- `POST /attendance/check-in` - Check in member (requires active subscription)

## Example Requests

### Create Member

```bash
curl -X POST "http://localhost:8000/members" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aniket",
    "phone": "9876543210",
    "status": "active"
  }'
```

### Create Plan

```bash
curl -X POST "http://localhost:8000/plans" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monthly",
    "price": 999.00,
    "duration_days": 30
  }'
```

### Create Subscription

```bash
curl -X POST "http://localhost:8000/subscriptions" \
  -H "Content-Type: application/json" \
  -d '{
    "member_id": 1,
    "plan_id": 1,
    "start_date": "2025-11-25T00:00:00"
  }'
```

### Check In

```bash
curl -X POST "http://localhost:8000/attendance/check-in" \
  -H "Content-Type: application/json" \
  -d '{"member_id": 1}'
```

## Database Schema

### Member
- id (PK)
- name
- phone (unique)
- join_date
- status
- total_check_ins (auto-incremented)

### Plan
- id (PK)
- name
- price
- duration_days

### Subscription
- id (PK)
- member_id (FK → Member)
- plan_id (FK → Plan)
- start_date
- end_date (auto-calculated)

### Attendance
- id (PK)
- member_id (FK → Member)
- check_in_time

## Database Trigger

The project includes a **PostgreSQL trigger** that automatically increments `total_check_ins` in the Member table whenever a new attendance record is inserted.

**Location**: `triggers.sql`  
**Type**: AFTER INSERT trigger on attendance table  
**Function**: `increment_member_check_ins()`  

This is a **real database-level trigger**, not simulated in application code.

## Project Structure

```
service-membership-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── database.py          # DB config
│   ├── models.py            # ORM models
│   ├── schemas.py           # Pydantic models
│   └── routers/
│       ├── __init__.py
│       ├── members.py
│       ├── plans.py
│       ├── subscriptions.py
│       └── attendance.py
├── triggers.sql             # PostgreSQL trigger
├── sqlite_trigger.sql       # SQLite alternative
├── requirements.txt
├── .env
└── README.md
```

## Error Handling

The API properly handles errors:

- **404** - Resource not found
- **400** - Bad request (e.g., duplicate phone)
- **403** - Forbidden (e.g., no active subscription)
- **422** - Validation error

## Development

### Run with Auto-Reload

```bash
uvicorn app.main:app --reload
```
### or using this file
```bash
python ./run.py
```

### Run Tests (Not specified but will push them in repo)

```bash
pytest
```