# Skriptomat

## Description
- Description of our app

## Status
- Development stage: Initial setup
- Maintainer(s): Leonarda, Dunja, Daniela, Lorena, Mihael, Jakov

## Tech stack
- Backend: Python, Django, Django REST Framework
- Frontend: React Vite
- Database: PostgreSQL (pgAdmin4 for management)

## Prerequisites
- Git
- Python 3.10+ (or project-chosen version)
- Node.js 18+ and npm or yarn
- PostgreSQL (or Docker Desktop / Docker Compose)
- pgAdmin4 (optional if using Docker)
- Recommended: VS Code

## Quickstart (developer setup)
1. Clone the repository:
   git clone https://github.com/your-username/skriptomat.git
   cd skriptomat

2. Backend setup:
   - Create and activate a virtual environment:
     python -m venv .venv
     .\.venv\Scripts\Activate
   - Install dependencies:
     pip install -r backend/requirements.txt
   - Copy .env.example to .env and fill in your database credentials
   - Run migrations:
     cd backend
     python manage.py migrate
   - Start the server:
     python manage.py runserver

3. Frontend setup:
   - cd frontend
   - npm install
   - Copy .env.example to .env
   - npm run dev

4. When creating new features:
   - Create a new branch:
     git checkout -b feature/your-feature-name
   - Make changes and commit regularly
   - Push to GitHub and create a pull request   

## Database setup (developer)
1. Install PostgreSQL and pgAdmin4
2. Create a new database called "Skriptomat"
3. Create a user with permission to access this database (default: postgres)
4. Copy credentials to personal, local .env file



## Migrations and fixtures

## Testing

## Development workflow and GitHub


## Contributing
- See CONTRIBUTING.md for code style, commit conventions, testing and review guidelines.

## License
- Add chosen license here (e.g., MIT). See LICENSE file.

## Contact

## Developers (Team "Jedan manje")
Leonarda
Dunja
Daniela
Lorena
Mihael
Jakov

Developed with <3 @ FER