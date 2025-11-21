from django.core.management.base import BaseCommand
from faker import Faker
from random import randint, choice
from django.utils import timezone
from datetime import timedelta
from kudos_app.models import Organization, User, Kudo

class Command(BaseCommand):
    help = "Creates demo data for organizations, users and kudos."

    def handle(self, *args, **options):
        fake = Faker()
        Kudo.objects.all().delete()
        User.objects.all().delete()
        Organization.objects.all().delete()

        orgs = [Organization.objects.create(name=fake.company()) for _ in range(2)]
        users = []

        for org in orgs:
            for _ in range(6):
                users.append(User.objects.create(
                    username = fake.user_name(),
                    password = "1234",
                    organization = org,
                    # kudos_left = randint(1,3),
                ))
        kudosCnt = 20
        for _ in range(kudosCnt):
            sender = choice(users)
            receiver = choice([u for u in users if u != sender])
            message = fake.sentence(nb_words=randint(6, 12))

            day = randint(0, 20)
            created_at = timezone.now() -timedelta(days=day)

            k = Kudo(sender=sender, receiver=receiver, message=message, created_at=created_at)
            k.skip_kudos_validation = True
            k.save()
        
        self.stdout.write(self.style.SUCCESS("Demo data loaded successfully"))