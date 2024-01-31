from django.core.management import BaseCommand
from accounts.models import UserProfile
import cloudinary.uploader


class Command(BaseCommand):
    help = "Migrate avatars to Cloudinary"

    def handle(self, *args, **kwargs):
        for user in UserProfile.objects.all():
            if user.avatar:
                response = cloudinary.uploader.upload(user.avatar.path)
                user.avatar = response["url"]
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully migrated avatar {user.pk}"
                    )
                )
