# Skriptomat

## Opis projekta
Trenutno, studenti često koriste različite platforme za dijeljenje bilješki, poput društvenih mreža ili e-mailova, što može biti neučinkovito i kaotično. Ovaj način dijeljenja informacija često rezultira gubitkom vremena i nemogućnošću pronalaska relevantnih materijala kada su najpotrebniji. Zato smo mi smislili rješenje za taj problem! Platforma „Skriptomat“ omogućuje dijeljenje vlastitih materijala među studentima čime se olakšava pristup relevantnim i ažurnim materijalima s predavanja. Studenti će imati brži i lakši pristup relevantnim materijalima za učenje te time uštedjeti vrijeme koje bi inače posvetili prikupljanju svih materijala potrebnih za učenje. Nadalje, poboljšat će se i kvaliteta bilješki sustavom ocjenjivanja koji omogućuje jednostavno identificiranje najkvalitetnijih materijala za učenje. Također, aplikacija potiče suradnju među studentima zato što međusobnom pomoći dolazi do boljeg razumijevanja gradiva, odnosno većeg akademskog uspjeha. 

Ovaj projekt je rezultat timskog rada u sklopu projektnog zadatka kolegija Programsko inženjerstvo na Fakultetu elektrotehnike i računarstva Sveučilišta u Zagrebu.

## Funkcijski zahtjevi

## Tehnologije
- Backend: Python, Django, Django REST Framework
- Frontend: React Vite
- Database: PostgreSQL (pgAdmin4 for management)

## Članovi tima
- Leonarda Laušić - voditeljica
- Dunja Međurečan
- Lorena Pratljačić
- Daniela Jovanović
- Jakov Miličić
- Mihael Smud

## Status
- Development stage: Initial setup
- Maintainer(s): Leonarda, Dunja, Daniela, Lorena, Mihael, Jakov

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


## Contributing
- See CONTRIBUTING.md for code style, commit conventions, testing and review guidelines.

## License
- Add chosen license here (e.g., MIT). See LICENSE file.

## Contact

Developed with <3 @ FER
