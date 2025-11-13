from django.core.management.base import BaseCommand
from kudos_app.models import User

class Command(BaseCommand):
    help ="Resets all user' available kudos to 3."

    def handle(self, *args, **kwargs):
        users = User.objects.all()

        for user in users:
            user.kudos_left = 3
            user.save(update_fields=['kudos_left'])
        
        self.stdout.write(self.style.SUCCESS(
            f"{users.count()} users' kudos has been successfully reset for the week."
        ))