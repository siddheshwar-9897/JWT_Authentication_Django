# JWT Authentication Django

A complete Django REST API authentication system with custom user management and JWT (JSON Web Token) authentication.

## Features

- **Custom User Model**: Email-based authentication with username support
- **JWT Token Authentication**: Secure API access with access and refresh tokens
- **User Management**: Register, login, update profile, and delete users
- **Password Security**: Automatic password hashing and secure storage
- **RESTful API**: Clean API endpoints following REST principles
- **Permission System**: Role-based access control with staff permissions

## Technology Stack

- **Backend**: Django 4.x + Django REST Framework
- **Authentication**: JWT (rest_framework_simplejwt)
- **Database**: SQLite (development ready)
- **Python**: 3.8+

## Project Structure

```
DJango_AUTH/
├── DJANGO_AUTH/
│   ├── DJANGO_AUTH/          # Main project directory
│   │   ├── settings.py       # Django settings
│   │   ├── urls.py          # Main URL configuration
│   │   └── wsgi.py          # WSGI configuration
│   ├── Django_Auth_app/     # Authentication app
│   │   ├── models.py        # Custom user model
│   │   ├── views.py         # API views
│   │   ├── serializers.py   # Data serializers
│   │   ├── urls.py          # App URL configuration
│   │   ├── authentication.py # Custom auth backend
│   │   ├── admin.py         # Admin interface
│   │   └── migrations/      # Database migrations
│   ├── manage.py            # Django management script
│   └── db.sqlite3          # SQLite database
├── venv/                    # Virtual environment
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DJango_AUTH
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Authentication Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/register/` | POST | Register new user | No |
| `/api/login/` | POST | Simple login verification | No |
| `/api/token/` | POST | Get JWT tokens (login) | No |
| `/api/token/refresh/` | POST | Refresh access token | No |

### User Management Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/profiles/` | GET | List all user profiles | Yes (JWT) |
| `/api/update-username/` | PUT | Update current user's username | Yes (JWT) |
| `/api/delete-user/<id>/` | DELETE | Delete user by ID | Yes (JWT) |

### Utility Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Welcome message | No |

## API Usage Examples

### 1. User Registration

```bash
curl -X POST http://localhost:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "is_active": true,
  "is_staff": false
}
```

### 2. Get JWT Tokens (Login)

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user_id": 1,
  "email": "user@example.com",
  "username": "johndoe"
}
```

### 3. Access Protected Endpoint

```bash
curl -X GET http://localhost:8000/api/profiles/ \
  -H "Authorization: Bearer <access_token>"
```

### 4. Update Username

```bash
curl -X PUT http://localhost:8000/api/update-username/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newusername"
  }'
```

### 5. Refresh Token

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<refresh_token>"
  }'
```

## Custom User Model

The project uses a custom user model (`Profile`) with the following features:

- **Email as Username**: Users log in with their email address
- **Additional Fields**: Username, is_active, is_staff
- **Custom Manager**: Handles user creation with proper password hashing
- **JWT Integration**: Works seamlessly with JWT authentication

### Model Fields

| Field | Type | Description |
|-------|------|-------------|
| email | EmailField | Unique identifier for login |
| username | CharField | Display name (max 100 chars) |
| is_active | BooleanField | Account status (default: True) |
| is_staff | BooleanField | Admin access (default: False) |

## Security Features

- **Password Hashing**: Automatic password hashing using Django's built-in security
- **JWT Tokens**: Secure token-based authentication
- **Permission Classes**: Protected endpoints require valid JWT
- **Email Authentication**: Secure email-based login system
- **Write-Only Passwords**: Passwords never exposed in API responses

## Configuration

### JWT Settings

JWT tokens are configured with default settings. You can customize token expiration in `settings.py`:

```python
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}
```

### Custom Authentication Backend

The project uses `EmailBackend` for email-based authentication:

```python
# settings.py
AUTHENTICATION_BACKENDS = [
    'Django_Auth_app.authentication.EmailBackend',
]
```

## Development

### Running Tests

```bash
python manage.py test
```

### Creating New Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Admin

Access the admin interface at `http://localhost:8000/admin/` using your superuser credentials.

## Production Deployment

### Environment Variables

Set the following environment variables for production:

```bash
export DEBUG=False
export SECRET_KEY='your-secret-key'
export DATABASE_URL='your-database-url'
```

### Security Considerations

1. **Use HTTPS**: Always use HTTPS in production
2. **Environment Variables**: Store sensitive data in environment variables
3. **Database Security**: Use a production-grade database (PostgreSQL/MySQL)
4. **CORS Configuration**: Configure CORS for frontend applications
5. **Rate Limiting**: Implement rate limiting for API endpoints

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions, please open an issue on the GitHub repository.

---

**Note**: This project is for educational and development purposes. Ensure proper security measures before deploying to production.
