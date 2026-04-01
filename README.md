# Finance Dashboard Application

This project consists of a **FastAPI backend** and a **React (Vite) frontend**.

## Backend Setup (Production Ready)

### 1. Requirements
- Python 3.10+
- PostgreSQL database

### 2. Installation
Navigate to the `backend` directory:
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Configuration
Update the `.env` file in the `backend` folder:
- `DATABASE_URL`: Your PostgreSQL connection string.
- `SECRET_KEY`: A strong secret key for JWT tokens.
- `BACKEND_CORS_ORIGINS`: List of allowed origins (e.g., `http://localhost:5173` for React).

### 4. Database Schema
The database schema is automatically applied on startup via SQLAlchemy models. You can also find the raw SQL in `backend/database_schema.sql`.

### 5. Running the Backend
**Development:**
```bash
cd backend
uvicorn app.main:app --reload
```

**Production:**
```bash
cd backend
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 6. API Documentation
Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`
- Summary: Check `backend/api.txt` for detailed endpoint descriptions.

## Frontend Setup (Coming Soon)
- React (Vite)
- Axios for API calls
- Tailwind CSS for styling
- React Router for navigation
