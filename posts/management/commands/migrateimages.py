from django.core.management import BaseCommand
from posts.models import Photo
import cloudinary.uploader


class Command(BaseCommand):
    help = "Migrate images to Cloudinary"

    def handle(self, *args, **kwargs):
        for photo in Photo.objects.all():
            response = cloudinary.uploader.upload(photo.picture.path)
            photo.picture = response["url"]
            photo.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully migrated {photo.pk}")
            )
