from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Role, Faculty, Course
from django.contrib.auth import get_user_model

User = get_user_model()  # Koristi prilagođeni `User` model


class UserRegistrationTests(APITestCase):
    def setUp(self):
        # API URL konfiguracija
        self.register_url = reverse("register") 
        self.role = Role.objects.create(name="student")
        self.faculty = Faculty.objects.create(name="Fakultet elektrotehnike i računarstva")

        # Validni korisnički podaci
        self.valid_data = {
            "email": "dunja.medurecan@gmail.com",
            "username": "dunja804",
            "password": "dunjica123",
            "password_confirm": "dunjica123",
            "first_name": "Dunja",
            "last_name": "Medurečan",
            "role": "student",
            "faculty": "Fakultet elektrotehnike i računarstva"
        }

    def test_valid_registration(self):
        """Test validne registracije korisnika."""
        response = self.client.post(self.register_url, self.valid_data)

        # Provjerite status odgovora i ulogu korisnika
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Registration successful! Please login.")

        # Provjerite da li je korisnik kreiran u bazi
        user = User.objects.get(email=self.valid_data["email"])
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertEqual(user.role.name, self.valid_data["role"])
        self.assertEqual(user.faculty.name, self.valid_data["faculty"])

    def test_registration_missing_fields(self):
        """Test registracije sa nedostajućim obaveznim podacima."""
        invalid_data = {
            "email": "user@example.com",  # Nedostaje `username` i `role`
            "password": "password123",
            "password_confirm": "password123",
        }
        response = self.client.post(self.register_url, invalid_data)

        # Provjerite odgovor za greške validacije
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
        self.assertIn("role", response.data)

    def test_existing_email_registration(self):
        """Test registracije sa korisnikom koji već postoji."""
        # Kreirajte korisnika pre testa
        User.objects.create_user(
            email=self.valid_data["email"],
            username=self.valid_data["username"],
            password=self.valid_data["password"]
        )
        response = self.client.post(self.register_url, self.valid_data)

        # Provjerite grešku vezanu za postojeći email
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"][0], "user with this email already exists.")

    def test_password_mismatch_registration(self):
        """Test registracije sa lozinkama koje se ne podudaraju."""
        invalid_data = self.valid_data.copy()
        invalid_data["password_confirm"] = "different_password"

        response = self.client.post(self.register_url, invalid_data)

        # Provjerite poruku greške
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(response.data["password"][0], "Passwords do not match.")

    def test_registration_short_password(self):
        """Test registracije sa lozinkom kraćom od 8 znakova."""
        invalid_data = self.valid_data.copy()
        invalid_data["password"] = "123"
        invalid_data["password_confirm"] = "123"

        response = self.client.post(self.register_url, invalid_data)

        # Provjerite grešku validacije za lozinku
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(response.data["password"][0], "Ensure this field has at least 8 characters.")

    def test_registration_invalid_email_format(self):
        """RUBNI UVJET: Test registracije s nevažećim email formatom."""
        invalid_data = self.valid_data.copy()
        invalid_data["email"] = "not-a-valid-email"
        invalid_data["username"] = "testuser123"

        response = self.client.post(self.register_url, invalid_data)

        # Provjerite grešku validacije za email
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_registration_nonexistent_role(self):
        """IZAZIVANJE POGREŠKE: Test registracije s nepostojećom ulogom."""
        invalid_data = self.valid_data.copy()
        invalid_data["role"] = "superuser"  # Nepostojeća uloga
        invalid_data["email"] = "test@fer.hr"
        invalid_data["username"] = "testuser999"

        response = self.client.post(self.register_url, invalid_data)

        # Provjerite grešku za nepostojeću ulogu
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("role", response.data)


class UserModelTests(TestCase):
    """Testovi za User model i njegove metode."""

    def setUp(self):
        self.student_role = Role.objects.create(name="student")
        self.moderator_role = Role.objects.create(name="moderator")
        self.admin_role = Role.objects.create(name="admin")
        self.faculty = Faculty.objects.create(name="FER")

    def test_user_creation_with_role(self):
        """REDOVAN SLUČAJ: Kreiranje korisnika s ulogom studenta."""
        user = User.objects.create_user(
            email="student@fer.hr",
            username="student1",
            password="testpass123",
            role=self.student_role,
            faculty=self.faculty
        )

        self.assertEqual(user.email, "student@fer.hr")
        self.assertEqual(user.role.name, "student")
        self.assertTrue(user.is_student())
        self.assertFalse(user.is_moderator())
        self.assertFalse(user.is_admin())

    def test_user_role_methods(self):
        """REDOVAN SLUČAJ: Testiranje is_student, is_moderator, is_admin metoda."""
        student = User.objects.create_user(
            email="s@fer.hr",
            username="s1",
            password="pass",
            role=self.student_role
        )
        moderator = User.objects.create_user(
            email="m@fer.hr",
            username="m1",
            password="pass",
            role=self.moderator_role
        )
        admin = User.objects.create_user(
            email="a@fer.hr",
            username="a1",
            password="pass",
            role=self.admin_role
        )

        # Student provjere
        self.assertTrue(student.is_student())
        self.assertFalse(student.is_moderator())
        self.assertFalse(student.is_admin())

        # Moderator provjere
        self.assertFalse(moderator.is_student())
        self.assertTrue(moderator.is_moderator())
        self.assertFalse(moderator.is_admin())

        # Admin provjere
        self.assertFalse(admin.is_student())
        self.assertFalse(admin.is_moderator())
        self.assertTrue(admin.is_admin())

    def test_user_without_role(self):
        """RUBNI UVJET: Korisnik bez uloge."""
        user = User.objects.create_user(
            email="norole@fer.hr",
            username="norole1",
            password="testpass123"
        )

        self.assertIsNone(user.role)
        self.assertFalse(user.is_student())
        self.assertFalse(user.is_moderator())
        self.assertFalse(user.is_admin())


class CourseTests(TestCase):
    """Testovi za Course model."""

    def setUp(self):
        self.faculty = Faculty.objects.create(name="FER")
        self.course1 = Course.objects.create(
            name="Programsko inženjerstvo",
            faculty=self.faculty,
            semester=5
        )

    def test_course_creation(self):
        """REDOVAN SLUČAJ: Kreiranje novog kolegija."""
        course = Course.objects.create(
            name="Baze podataka",
            faculty=self.faculty,
            semester=4
        )

        self.assertEqual(course.name, "Baze podataka")
        self.assertEqual(course.faculty, self.faculty)
        self.assertEqual(course.semester, 4)
        self.assertIn("Baze podataka", str(course))

    def test_course_unique_constraint(self):
        """IZAZIVANJE POGREŠKE: Kreiranje kolegija s istim imenom na istom fakultetu."""
        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            Course.objects.create(
                name="Programsko inženjerstvo",  # Isto ime kao course1
                faculty=self.faculty,  # Isti fakultet
                semester=6
            )

    def test_course_faculty_relationship(self):
        """REDOVAN SLUČAJ: Provjera veze između kolegija i fakulteta."""
        courses = self.faculty.courses.all()
        self.assertEqual(courses.count(), 1)
        self.assertEqual(courses.first(), self.course1)


class FacultyTests(TestCase):
    """Testovi za Faculty model."""

    def test_faculty_creation(self):
        """REDOVAN SLUČAJ: Kreiranje fakulteta."""
        faculty = Faculty.objects.create(name="PMF")
        self.assertEqual(faculty.name, "PMF")
        self.assertEqual(str(faculty), "PMF")

    def test_faculty_unique_name(self):
        """IZAZIVANJE POGREŠKE: Kreiranje fakulteta s istim imenom."""
        from django.db import IntegrityError

        Faculty.objects.create(name="FER")
        with self.assertRaises(IntegrityError):
            Faculty.objects.create(name="FER")


class UserCourseSubscriptionTests(TestCase):
    """Testovi za pretplatu korisnika na kolegije."""

    def setUp(self):
        self.faculty = Faculty.objects.create(name="FER")
        self.role = Role.objects.create(name="student")
        self.user = User.objects.create_user(
            email="student@fer.hr",
            username="student1",
            password="pass123",
            role=self.role,
            faculty=self.faculty
        )
        self.course1 = Course.objects.create(
            name="PROGI",
            faculty=self.faculty,
            semester=5
        )
        self.course2 = Course.objects.create(
            name="OOP",
            faculty=self.faculty,
            semester=3
        )

    def test_user_subscribe_to_course(self):
        """REDOVAN SLUČAJ: Korisnik se pretplaćuje na kolegij."""
        self.user.subscribed_courses.add(self.course1)
        self.assertIn(self.course1, self.user.subscribed_courses.all())
        self.assertEqual(self.user.subscribed_courses.count(), 1)

    def test_user_subscribe_to_multiple_courses(self):
        """REDOVAN SLUČAJ: Korisnik se pretplaćuje na više kolegija."""
        self.user.subscribed_courses.add(self.course1, self.course2)
        self.assertEqual(self.user.subscribed_courses.count(), 2)
        self.assertIn(self.course1, self.user.subscribed_courses.all())
        self.assertIn(self.course2, self.user.subscribed_courses.all())

    def test_course_subscribers(self):
        """REDOVAN SLUČAJ: Provjera broja pretplatnika na kolegij."""
        user2 = User.objects.create_user(
            email="student2@fer.hr",
            username="student2",
            password="pass123",
            role=self.role,
            faculty=self.faculty
        )

        self.course1.subscribers.add(self.user, user2)
        self.assertEqual(self.course1.subscribers.count(), 2)
        self.assertIn(self.user, self.course1.subscribers.all())
        self.assertIn(user2, self.course1.subscribers.all())
