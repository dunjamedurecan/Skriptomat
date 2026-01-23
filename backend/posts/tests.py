from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User, Role, Faculty, Course
from posts.models import Document, validate_pdf
import io


class DocumentModelTests(TestCase):
    """Testovi za Document model."""

    def setUp(self):
        self.faculty = Faculty.objects.create(name="FER")
        self.role = Role.objects.create(name="student")
        self.user = User.objects.create_user(
            email="student@fer.hr",
            username="student1",
            password="testpass123",
            role=self.role,
            faculty=self.faculty
        )
        self.course = Course.objects.create(
            name="PROGI",
            faculty=self.faculty,
            semester=5
        )

    def test_document_creation(self):
        """Kreiranje dokumenta."""
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"PDF content here",
            content_type="application/pdf"
        )

        document = Document.objects.create(
            title="Test dokument",
            file=pdf_file,
            user=self.user,
            course=self.course,
            status=Document.Status.PENDING
        )

        self.assertEqual(document.title, "Test dokument")
        self.assertEqual(document.user, self.user)
        self.assertEqual(document.course, self.course)
        self.assertEqual(document.status, Document.Status.PENDING)

    def test_document_status_choices(self):
        """Testiranje različitih statusa dokumenta."""
        pdf_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")

        doc_pending = Document.objects.create(
            title="Pending",
            file=pdf_file,
            user=self.user,
            status=Document.Status.PENDING
        )
        self.assertEqual(doc_pending.status, "pending")

        pdf_file2 = SimpleUploadedFile("test2.pdf", b"content", content_type="application/pdf")
        doc_approved = Document.objects.create(
            title="Approved",
            file=pdf_file2,
            user=self.user,
            status=Document.Status.APPROVED
        )
        self.assertEqual(doc_approved.status, "approved")

    def test_document_likes_functionality(self):
        """Testiranje like funkcionalnosti."""
        pdf_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")
        document = Document.objects.create(
            title="Test",
            file=pdf_file,
            user=self.user
        )

        user2 = User.objects.create_user(
            email="user2@fer.hr",
            username="user2",
            password="pass123",
            role=self.role
        )

        # Dodaj like-ove
        document.likes.add(self.user, user2)

        self.assertEqual(document.total_likes(), 2)
        self.assertIn(self.user, document.likes.all())
        self.assertIn(user2, document.likes.all())

    def test_document_default_status(self):
        """Provjera defaultnog statusa."""
        pdf_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")
        document = Document.objects.create(
            title="Test",
            file=pdf_file,
            user=self.user
        )

        self.assertEqual(document.status, Document.Status.PENDING)

    def test_document_allow_download_default(self):
        """Provjera defaultne vrijednosti allow_download."""
        pdf_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")
        document = Document.objects.create(
            title="Test",
            file=pdf_file,
            user=self.user
        )

        self.assertTrue(document.allow_download)


class PDFValidationTests(TestCase):
    """Testovi za validaciju PDF datoteka."""

    def setUp(self):
        self.faculty = Faculty.objects.create(name="FER")
        self.role = Role.objects.create(name="student")
        self.user = User.objects.create_user(
            email="student@fer.hr",
            username="student1",
            password="pass123",
            role=self.role
        )

    def test_validate_pdf_valid_file(self):
        """Validacija ispravne PDF datoteke."""
        pdf_file = SimpleUploadedFile(
            "test.pdf",
            b"PDF content",
            content_type="application/pdf"
        )

        # Ne bi trebalo baciti iznimku
        try:
            validate_pdf(pdf_file)
        except ValidationError:
            self.fail("validate_pdf() podigao je ValidationError za valjan PDF")

    def test_validate_pdf_invalid_content_type(self):
        """Validacija datoteke koja nije PDF."""
        invalid_file = SimpleUploadedFile(
            "test.txt",
            b"Text content",
            content_type="text/plain"
        )

        with self.assertRaises(ValidationError) as context:
            validate_pdf(invalid_file)

        self.assertIn("Only PDF files are allowed", str(context.exception))

    def test_validate_pdf_file_too_large(self):
        """Validacija prevelike datoteke (> 50 MB)."""
        # Kreiraj veliku datoteku (51 MB)
        large_content = b"x" * (51 * 1024 * 1024)
        large_file = SimpleUploadedFile(
            "large.pdf",
            large_content,
            content_type="application/pdf"
        )

        with self.assertRaises(ValidationError) as context:
            validate_pdf(large_file)

        self.assertIn("File too large", str(context.exception))


class DocumentAPITests(APITestCase):
    """API testovi za Document endpoints."""

    def setUp(self):
        self.faculty = Faculty.objects.create(name="FER")
        self.student_role = Role.objects.create(name="student")
        self.moderator_role = Role.objects.create(name="moderator")
        
        self.student = User.objects.create_user(
            email="student@fer.hr",
            username="student1",
            password="pass123",
            role=self.student_role,
            faculty=self.faculty
        )
        
        self.moderator = User.objects.create_user(
            email="mod@fer.hr",
            username="mod1",
            password="pass123",
            role=self.moderator_role,
            faculty=self.faculty
        )

        self.course = Course.objects.create(
            name="PROGI",
            faculty=self.faculty,
            semester=5
        )

    def test_document_str_method(self):
        """Testiranje __str__ metode s naslovom i bez njega."""
        pdf_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")
        
        # Dokument s naslovom
        doc_with_title = Document.objects.create(
            title="Moj dokument",
            file=pdf_file,
            user=self.student
        )
        self.assertEqual(str(doc_with_title), "Moj dokument")

        # Dokument bez naslova
        pdf_file2 = SimpleUploadedFile("test2.pdf", b"content", content_type="application/pdf")
        doc_without_title = Document.objects.create(
            file=pdf_file2,
            user=self.student
        )
        self.assertIn("Post", str(doc_without_title))

    def test_document_course_relationship(self):
        """Provjera veze između dokumenta i kolegija."""
        pdf_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")
        document = Document.objects.create(
            title="Test",
            file=pdf_file,
            user=self.student,
            course=self.course
        )

        # Provjeri vezu
        self.assertEqual(document.course, self.course)
        self.assertIn(document, self.course.documents.all())

    def test_document_reviewed_by_moderator(self):
        """Provjera reviewed_by polja."""
        from django.utils import timezone
        
        pdf_file = SimpleUploadedFile("test.pdf", b"content", content_type="application/pdf")
        document = Document.objects.create(
            title="Test",
            file=pdf_file,
            user=self.student,
            status=Document.Status.APPROVED,
            reviewed_by=self.moderator,
            reviewed_at=timezone.now()
        )

        self.assertEqual(document.reviewed_by, self.moderator)
        self.assertIsNotNone(document.reviewed_at)
        self.assertEqual(document.status, Document.Status.APPROVED)

