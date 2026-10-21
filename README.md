# 🏦 FastAPI Banking Application

A robust backend banking application built with FastAPI, SQLAlchemy, Alembic for database migrations, Supabase, and Docker support.

## 🚀 Features

- **Authentication & Authorization**: Secure OAuth2 implementation for user login and role-based access control (`role/`, `Oauth2/`).
- **Database Migrations**: Managed seamlessly using Alembic.
- **Real-time & Connection Management**: Built-in connection manager (`connection_manager.py`).
- **Profile Management**: Static file handling for user profiles (`static/profiles/`).
- **Cloud & Database Integration**: Configured to work with Supabase.
- **Containerized**: Fully dockerized for easy deployment and local development.

---

## 📁 Project Structure

```text
banking-app/
├── Oauth2/              # OAuth2 authentication modules
├── alembic/             # Database migration scripts
├── app/                 # Core application logic and configuration
├── role/                # Role-based access control logic
├── routers/             # API route handlers
├── static/profiles/     # User profile images/assets
├── alembic.ini          # Alembic configuration file
├── connection_manager.py# Connection handling
├── crud.py              # Database CRUD operations
├── model.py             # SQLAlchemy database models
├── supabase_client.py   # Supabase integration client
├── main.py              # FastAPI application entry point
├── requirements.txt     # Python dependencies
├── start.sh             # Startup script
├── Dockerfile           # Docker configuration
└── docker-compose.yml   # Docker Compose setup
