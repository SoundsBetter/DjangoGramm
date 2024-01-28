from django.core.management import BaseCommand
from posts.models import Photo
import cloudinary.uploader


class Command(BaseCommand):
    help = "Migrate images to Cloudinary"

    def handle(self, *args, **kwargs):
        for photo in Photo.objects.all():
            print(str(photo.picture))
            response = cloudinary.uploader.upload(str(photo.picture))
            print(response)
            photo.picture = response["url"]
            photo.save()

            self.stdout.write(
                self.style.SUCCESS(f"Successfully migrated {photo.pk}")
            )
