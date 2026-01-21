from django.core.management.base import BaseCommand
from users.models import Faculty, Course


class Command(BaseCommand):
    help = 'Seed database with courses for different faculties'

    def handle(self, *args, **kwargs):
        # Get faculties (or create if not exists)
        fer, _ = Faculty.objects.get_or_create(name="FER")
        medicinski, _ = Faculty.objects.get_or_create(name="Medicinski fakultet")
        fsb, _ = Faculty.objects.get_or_create(name="FSB")
        ekonomski, _ = Faculty.objects.get_or_create(name="Ekonomski fakultet")
        glazbena, _ = Faculty.objects.get_or_create(name="Glazbena akademija")
        
        courses_data = [
            # FER courses
            {"name": "Vjekom", "semester": 1, "faculty": fer},
            {"name": "DigLog", "semester": 1, "faculty": fer},
            {"name": "Komre", "semester": 4, "faculty": fer},
            {"name": "Matan2", "semester": 2, "faculty": fer},
            {"name": "ARH", "semester": 3, "faculty": fer},
            {"name": "DisMat", "semester": 3, "faculty": fer},
            {"name": "BazePod", "semester": 3, "faculty": fer},
            
            # Medicinski fakultet courses
            {"name": "Anatomija", "semester": 1, "faculty": medicinski},
            {"name": "Fiziologija", "semester": 1, "faculty": medicinski},
            
            # FSB courses
            {"name": "Mehatronika", "semester": 2, "faculty": fsb},
            {"name": "Termodinamika", "semester": 4, "faculty": fsb},
            
            # Ekonomski fakultet courses
            {"name": "Uvod u statistiku", "semester": 1, "faculty": ekonomski},
            
            # Glazbena akademija courses
            {"name": "Polifonija", "semester": 1, "faculty": glazbena},
        ]

        created_count = 0
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                name=course_data["name"],
                faculty=course_data["faculty"],
                defaults={"semester": course_data["semester"]}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created: {course.name} ({course.faculty.name}, Sem {course.semester})'
                    )
                )
            else:
                self.stdout.write(f'  Already exists: {course.name} ({course.faculty.name})')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Seeded {created_count} new courses!'))
