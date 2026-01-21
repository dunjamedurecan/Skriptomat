from django.core.management.base import BaseCommand
from users.models import Faculty

class Command(BaseCommand):
    help = 'Seed database with Croatian faculties'

    def handle(self, *args, **kwargs):
        faculties = [
            "FER",
            "PMF",
            "FFSE",
            "FSB",
            "FFZG",
            "Fakultet elektrotehnike i računarstva (FER)",
            "Prirodoslovno-matematički fakultet (PMF)",
            "Fakultet strojarstva i brodogradnje (FSB)",
            "Ekonomski fakultet",
            "Pravni fakultet",
            "Filozofski fakultet",
            "Medicinski fakultet",
            "Građevinski fakultet",
            "Arhitektonski fakultet",
            "Fakultet prometnih znanosti",
            "Fakultet kemijskog inženjerstva i tehnologije",
            "Tekstilno-tehnološki fakultet",
            "Metalurški fakultet",
            "Rudarsko-geološko-naftni fakultet",
            "Agronomski fakultet",
            "Šumarski fakultet",
            "Prehrambeno-biotehnološki fakultet",
            "Veterinarski fakultet",
            "Farmaceutsko-biokemijski fakultet",
            "Edukacijsko-rehabilitacijski fakultet",
            "Kineziološki fakultet",
            "Učiteljski fakultet",
            "Akademija likovnih umjetnosti",
            "Glazbena akademija",
            "Akademija dramske umjetnosti",
        ]

        created_count = 0
        for faculty_name in faculties:
            faculty, created = Faculty.objects.get_or_create(name=faculty_name)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {faculty_name}'))
            else:
                self.stdout.write(f'  Already exists: {faculty_name}')

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Seeded {created_count} new faculties!'))
