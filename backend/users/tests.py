from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Role, Faculty
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

        # Proverite status odgovora i ulogu korisnika
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Registration successful! Please login.")

        # Proverite da li je korisnik kreiran u bazi
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

        # Provera odgovora za greške validacije
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

        # Proverite grešku vezanu za postojeći email
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(response.data["email"][0], "user with this email already exists.")

    def test_password_mismatch_registration(self):
        """Test registracije sa lozinkama koje se ne podudaraju."""
        invalid_data = self.valid_data.copy()
        invalid_data["password_confirm"] = "different_password"

        response = self.client.post(self.register_url, invalid_data)

        # Provera poruke greške
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(response.data["password"][0], "Passwords do not match.")

    def test_registration_short_password(self):
        """Test registracije sa lozinkom kraćom od 8 znakova."""
        invalid_data = self.valid_data.copy()
        invalid_data["password"] = "123"
        invalid_data["password_confirm"] = "123"

        response = self.client.post(self.register_url, invalid_data)

        # Proverite grešku validacije za lozinku
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertEqual(response.data["password"][0], "Ensure this field has at least 8 characters.")
# Create your tests here.
