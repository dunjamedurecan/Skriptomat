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

### 🚀 Brzi Start (PowerShell - Windows)
```powershell
# Automatski setup cijelog projekta
.\start-local.ps1
```

**Za detaljne upute, vidi:**
- 📘 **[BRZI-START.md](BRZI-START.md)** - TL;DR verzija s konkretnim stanjem projekta
- 📗 **[LOKALNO-POKRETANJE.md](LOKALNO-POKRETANJE.md)** - Kompletni vodič s troubleshooting sekcijom

### Manual Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/dunjamedurecan/Skriptomat.git
   cd Skriptomat
   ```

2. Backend setup:
   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate
   pip install -r requirements.txt
   cp .env.example .env  # Uredi .env s DB credentialima
   python manage.py migrate
   python manage.py create_oauth_app  # Kreira OAuth2 app
   python manage.py runserver 0.0.0.0:8000
   ```

3. Frontend setup (novi terminal):
   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

4. Open in browser:
   - Frontend: http://localhost:5173
   - Admin: http://localhost:8000/admin

### Helper Scripts
- `backend/check-users.ps1` - Provjera korisnika u bazi
- `backend/create-test-users.ps1` - Kreiranje test korisnika
- `start-local.ps1` - Automatski setup cijelog projekta

### When creating new features:
   - Create a new branch:
     ```bash
     git checkout -b feature/your-feature-name
     ```
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