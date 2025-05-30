# SkyGate Airport API

A comprehensive RESTful API for managing airport operations, including flights, tickets, airports, and airplanes.

## 📋 Table of Contents

- [Features](#features)
- [Docker Setup](#docker-setup)
- [Manual Setup](#manual-setup)
- [API Structure](#api-structure)
- [Authentication](#authentication)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)

## ✨ Features

- **Airport Management**: Add, update and track airport information
- **Airplane Fleet**: Manage airplane types and specific airplanes
- **Flight Operations**: Schedule flights and assign crew
- **Ticket System**: Enable ticket booking and management
- **Order Processing**: Handle customer orders
- **JWT Authentication**: Secure API access
- **Swagger Documentation**: Interactive API docs
- **Dockerized**: Easy deployment with Docker

## 🐳 Docker Setup

### Prerequisites

- [Docker](https://www.docker.com/get-started) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)

### Quick Start

1. **Clone the repository**

   ```bash
   git clone https://github.com/BronkstoneBro/SkyGate-Airport-API
   cd skygate_airport_api
   ```

2. **Start the containers**

   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - API is available at: http://localhost:8000/
   - API documentation at: http://localhost:8000/swagger/

### Docker Environment Details

The setup includes:
- Web service (Django application)
- PostgreSQL database service

The configuration provides:
- Database persistence through Docker volumes
- Automatic migrations on startup
- Health checks to ensure service dependencies

### Development with Docker

- The project directory is mounted as a volume, so code changes apply immediately
- Database data persists between container restarts
- For requirement changes, rebuild the image:
  ```bash
  docker-compose build
  ```

## 🔧 Manual Setup

If you prefer running without Docker:

1. **Set up a virtual environment**

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the database**

   By default, the application uses SQLite in local development. 
   To use PostgreSQL, install `dj-database-url`:

   ```bash
   pip install dj-database-url
   ```

   And set the `DATABASE_URL` environment variable.

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the development server**

   ```bash
   python manage.py runserver
   ```

## 🏗️ API Structure

The API is organized into the following modules:

| Module | Description |
|--------|-------------|
| **Airports** | Airport locations and routes |
| **Airplanes** | Aircraft types and individual planes |
| **Flights** | Flight schedules and operations |
| **Tickets** | Seat bookings on flights |
| **Orders** | Customer ticket purchases |
| **Authentication** | User accounts and security |

## 🔐 Authentication

The API uses JWT (JSON Web Token) authentication:

1. **Register** a new user account:
   ```
   POST /api/auth/register/
   ```

2. **Login** to get your access token:
   ```
   POST /api/auth/login/
   ```

3. **Use the token** in API requests:
   ```
   Authorization: Bearer <your_token>
   ```

## 📖 API Documentation

Interactive documentation is available at:

- **Swagger UI**: `/swagger/` - Try API endpoints directly
- **ReDoc**: `/redoc/` - Alternative documentation viewer
- **OpenAPI Schema**: `/swagger.json` or `/swagger.yaml`

To test endpoints in Swagger UI:
1. Click the "Authorize" button
2. Enter your JWT token (without "Bearer" prefix)
3. Try out any endpoint

## 🔄 API Endpoints

| Resource | Endpoint | Description |
|----------|----------|-------------|
| Authentication | `/api/auth/` | User registration, login, token refresh |
| Airports | `/api/airports/` | Airport information and routes |
| Airplanes | `/api/airplanes/` | Aircraft types and specific planes |
| Flights | `/api/flights/` | Flight schedules and operations |
| Tickets | `/api/tickets/` | Ticket management |
| Orders | `/api/orders/` | Customer order processing |

### CRUD Operations

All resources support standard operations:

- **CREATE**: `POST /api/resource/`
- **READ**: `GET /api/resource/` or `GET /api/resource/{id}/`
- **UPDATE**: `PUT /api/resource/{id}/` or `PATCH /api/resource/{id}/`
- **DELETE**: `DELETE /api/resource/{id}/`

## 📝 License

[MIT License](LICENSE)
